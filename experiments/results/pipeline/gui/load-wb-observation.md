User GUI evidence, 2026-10-05: cycle 668, 0x1264 lbu a0,0(t0) in WB.
Register file wr_en tooltip is 0x1. WB mux in_0 tooltip is 0x00000003.
This second tooltip is data on input 0, not the mux select control value.
a0 remains 0x000003b1 in the displayed register snapshot; its committed value
has not yet been observed after the next edge. EX shows nop(stall), branch 0x126c
remains in ID, following load 0x1268 is in MEM. Selection tooltip and a0=3
confirmation remain pending. No additional completed-stage claim is made.

## Committed register value, cycle 669

User screenshot `cycle669-a0-committed.png` shows x10/a0 = 0x00000003, highlighted after the next step. The instruction at 0x1264 has left WB; 0x1268 is now in WB. Together with the cycle 667 memory output and cycle 668 write enable, this confirms the first byte load committed value 3. Mux select itself was not observed; input 0 data must not be described as the select control.
