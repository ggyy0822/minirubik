# Pipeline observation sheet — complete from your Ripes session

AI-authored teaching prompts, not a completed assignment analysis. Reference
model: ordinary RV32_5S, source revision 5b8a616edcb6f0a2ddb07e78951348b72497f1e1.
Record real observations; the expected signals below are code-derived predictions,
not screenshots or measurements from your GUI.

## Setup

Open heuristic_walkthrough.s, select 32-bit / 5-stage processor with forwarding
and hazard detection, no extensions. Reset, choose Processor, and single-step
clock cycles. Use the stage table to identify which instruction occupies each
stage. Do not assume every wire currently shown belongs to the same instruction.
The complete demonstration prints 1 and exits 0.

## 1. Load and writeback

Follow `lbu a1, 0(t1)` (example table value 6).

| Stage | Record from the GUI |
|---|---|
| IF | Cycle ___ ; PC ___ ; instruction ___ |
| ID | Cycle ___ ; t1 value ___ ; decoded destination ___ |
| EX | Cycle ___ ; address calculation ___ + ___ = ___ |
| MEM | Cycle ___ ; byte read ___ ; extension applied ___ |
| WB | Cycle ___ ; destination ___ ; value written ___ |

At WB inspect `registerFile.wr_en` and `reg_wr_src.select`.
Expected for the load's valid writeback: wr_en=1, select=MEMREAD (0).
Describe in your own words why the ALU's calculated address is not the value
that should be written into a1: ________________________________.

## 2. Arithmetic writeback

Follow `addi a0, a1, 0`. At its WB stage, inspect the same two signals.
Expected: wr_en=1; reg_wr_src.select=ALURES (1); a0 becomes 6.
Explain what changed compared with lbu: ________________________.

## 3. Store and memory state

Follow `sw t4, 0(t5)`. t4 should be 1 after the comparison 7 < 8.
Record t5/address ___ ; previous word ___ ; new word ___ .
At the store's MEM stage, inspect `data_mem.wr_en` (expected 1).
At its corresponding valid WB slot, register write enable is 0. The writeback
mux value then does not cause a register write; identify the enabling signal.
Explain why sw changes memory but not its source register t4: ____________.

## 4. Control / hazards

Observe `bgeu a0,a1,heuristic_done`: operands should be 5 and 6, branch not taken.
Record any stall/forwarding you actually see; do not invent a cycle count from
this worksheet. Explain which data dependency required it: ______________.

## Evidence to collect

Capture the relevant load WB, arithmetic WB and store MEM views (or enough
annotated images to clearly identify all three events), plus the final memory
word. Write your analysis in English in the report, using your actual observed
values. Later repeat the explanation on the corresponding instructions of the
final solver; this teaching harness alone is not a full solver walkthrough.

## Source basis for expected values

- Ripes src/processors/RISC-V/rv5s/rv5s.h: lines 97–104 connect the writeback mux
  and register enable; lines 140–156 connect ALU inputs and memory write enable.
- src/processors/RISC-V/rv_control.h: load instructions select MEMREAD;
  arithmetic instructions select ALURES; stores assert memory write enable.
- src/processors/RISC-V/riscv.h: RegWrSrc={MEMREAD,ALURES,PC4} gives 0,1,2.

If the disassembly pane still shows Unknown instruction after changing model,
reset and reassemble/reload the small source. Treat this as a diagnostic attempt,
not a guaranteed fix. Do not alter the solver to hide the display discrepancy.
