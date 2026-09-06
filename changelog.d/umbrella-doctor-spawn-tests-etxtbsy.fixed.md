doctor's two spawn tests retry past ETXTBSY: another test thread's fork inherits the just-written fake's write fd, so Linux refuses the exec. Both flaked ~1 run in 20 (task umbrella/019).
