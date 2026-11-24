study-designer: the image-segment reader checks a segment's end address; one past u64::MAX is an ImageError, not a panic (EMB-399).
