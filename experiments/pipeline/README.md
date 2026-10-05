# Pipeline teaching walkthrough

This small AI-authored harness reuses the existing heuristic instruction sequence
with example byte arrays, not actual complete cube pattern databases. It does not
modify the search or replace the eventual walkthrough of the submitted solver.

Open heuristic_walkthrough.s in Ripes and select the ordinary RV32I 5-stage
processor (forwarding and hazard detection enabled), with no ISA extensions.
Use Reset then single-cycle stepping in the Processor view. Observe:

- lbu a1,0(t1): IF fetches; ID reads address base; EX computes address; MEM reads
  a byte and zero-extends; WB writes a1=6. Follow actual per-stage wires rather
  than assuming a visible signal belongs to the instruction currently in EX.
- bgeu a0,a1: compares 5>=6, not taken; addi a0,a1,0 leaves h=6.
- sltu t4,t3,t2: bound 7 < depth+h 8 => t4=1.
- sw t4,0(t5): EX computes prune_result address; MEM writes 1, register write
  enable for this instruction is zero; no register destination in WB.
- lw a0,0(t5): reads result=1. Contrast memory-vs-ALU selection at writeback with
  addi; inspect actual mux inputs/select values in the processor diagram.

A pipeline contains several instructions at once; stalls/forwarding may move
observed events relative to a naive five-consecutive-cycle picture. The GUI
signal screenshots and the student's explanation have not yet been collected.

CLI verification: both ISS and 5S print 1 and exit 0. Recorded ISS cycles/retired
28/28, 5S 40/27. The one-instruction termination-accounting discrepancy is retained
as observed; it is not evidence that a useful arithmetic instruction disappeared.
Logs: ../results/pipeline/.
