# embarch-ui decisions: The live sample series

**Status:** active, 2026-11-24.

How the Live Study tab keeps and draws one tap's samples once there are too many to draw a point each. The session rings around it are [live-study.md](live-study.md) 31.

### 105 — Past its cap a live series folds into min and max per column, and a block at the ADC rails is drawn in the warning colour

Decimating 2:1 past 50,000 points (decision 31) kept about one sample in 200 of a 5-minute 32 ksps series (9.6 M samples), so a burst a few milliseconds long vanished: the thing an audio-rate capture is looked at for (EMB-476, analog-capture decision 11).

**Up to 50,000 samples a series is one point per sample, as before. Past that it folds into at most 4,000 columns of N consecutive samples, each keeping its lowest and highest value; when the columns run out, neighbours merge pairwise and N doubles.** Merging minima and maxima is exact, so a column's extremes are those of the samples it stands for however often the series has been folded. 4,000 is above the width of a 4K screen, so a column is never finer than a pixel the browser could draw. Memory and the snapshot stay bounded, and a sample costs a constant amount. The `samples` frame carries the columns the browser has not seen, or all of them (`columns_replace`) after a fold; `stride` is now N, the samples per column, and the plot's note says each column is drawn from its lowest to its highest. The series still never drops its oldest samples.

*Rejected:* reducing in the browser from the full series (9.6 M numbers in every snapshot); a fixed time bin (the samples of a block share one arrival stamp, so a column's width would not follow the signal).

**The clip indicator is a colour, not a marker line.** A series of raw codes (`Unit::Raw`) carries ADC rails `[0, 4095]`. A column or point that reaches one is drawn in the warning colour; a block (one `SampleBatch`) with at least one sample at a rail is counted in `clipped_blocks` and the samples in `clipped_samples`, and the note line says so. A series of any other unit has no rails and is never flagged.

**The 12-bit width is assumed, not read.** The resolution is in the start header of an analog tap's record, which Core does not forward to the live view, and a tap's source declares a rate and a channel but no resolution. The live view has the codes and nothing else, so the note line says "12-bit assumed". *Reversal condition:* Core forwarding the resolution (in a batch, or in the stream index), at which point the rails come from it. *Known false positive:* a raw counter that is not an ADC, whenever it reads 0.

*Consequences.* A series reaching 50,000 points changes shape once, from points to columns, and the browser redraws it from the columns in that frame; nothing is lost, since every column holds the extremes of what it replaced.
