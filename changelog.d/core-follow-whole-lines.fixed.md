`/logs/stream` no longer splits a log line across two SSE frames; its offset advances past a `\n` or not at all (embarch-core decision 44).
