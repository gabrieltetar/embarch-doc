`doc regparse --template ti` reads width-prefixed binary resets (`2b10`), `[Reset = 0x11]` and `[Reset = X]`; before, a layout printing them got no reset and no conflicts (EMB-33, atlas DESIGN.md).
