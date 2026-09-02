#!/usr/bin/env bash
# Start a long-lived, phone-drivable supervisor session under tmux.
#
# Remote Control attaches a phone or browser to a Claude Code process running
# HERE; it does not start one. And "the local process must keep running" is its
# hardest limitation -- close the terminal or quit VS Code and the session goes
# offline. tmux is what makes the process outlive the window you started it in,
# which is the whole point of driving it from a phone.
#
# Idempotent: run it again to attach to the session that is already up.
#
# Usage:
#   scripts/supervise-remote.sh              start or attach
#   scripts/supervise-remote.sh --status     is it running?
#   scripts/supervise-remote.sh --stop       kill it
set -uo pipefail

SESSION="embarch-supervisor"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

case "${1:-}" in
  --status)
    if tmux has-session -t "$SESSION" 2>/dev/null; then
      echo "running: tmux session '$SESSION'"
      tmux list-panes -t "$SESSION" -F '  pane #{pane_index}: #{pane_current_command}'
    else
      echo "not running"
    fi
    exit 0 ;;
  --stop)
    tmux kill-session -t "$SESSION" 2>/dev/null \
      && echo "stopped '$SESSION'" || echo "'$SESSION' was not running"
    exit 0 ;;
esac

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux is not installed; it is what keeps the session alive after you close the window." >&2
  exit 1
fi

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "'$SESSION' is already running -- attaching. (Detach with Ctrl-b d.)"
  exec tmux attach -t "$SESSION"
fi

if ! command -v claude >/dev/null 2>&1; then
  cat >&2 <<'MSG'
No `claude` CLI on PATH, so there is nothing for tmux to run.

This machine drives Claude Code through the VS Code extension, which bundles its
own copy and exposes no CLI. Two ways forward:

  A. No install, available now: run `/rc` in the VS Code session and drive that
     from your phone. Cost: VS Code has to stay open on this machine.

  B. Install the CLI, then re-run this script. The session then survives closing
     VS Code, closing the terminal, and dropping an SSH connection -- which is
     what you want if the batch is meant to run while you are away from the desk.

See embarch-parallel-agents.md §15.
MSG
  exit 1
fi

echo "starting '$SESSION' in $REPO"
tmux new-session -d -s "$SESSION" -c "$REPO" \
  "claude --remote-control 'EmbArch supervisor'"

sleep 1
if ! tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "session exited immediately -- run 'claude --remote-control' by hand to see why." >&2
  exit 1
fi

cat <<MSG
'$SESSION' is up.

  Attach here:   tmux attach -t $SESSION      (detach: Ctrl-b d)
  Get the link:  type /remote-control in the session; it prints the URL and a QR code
  From a phone:  open the session at claude.ai/code, then send: run a supervisor batch

Closing this window no longer stops it. Stop it with:
  scripts/supervise-remote.sh --stop
MSG
