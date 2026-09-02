`scripts/check-doc-size.py` enforces per-file size caps by role as a ratchet: a file may shrink freely, but never grow past `min(cap, baseline)`.
