# Walkthrough on the actual solver (v4, three-move input)

AI-authored preparation based on source and linked instructions, not completed
student observations. Open ../../output/assembly_search/23745612123332.elf as an
ELF executable in Ripes and choose the ordinary RV32I 5-stage processor. It needs
no LED peripheral. This is the actual v4 solver, not the small example table.

Input: 23745612123332. Verified output: D' B' R', length 3, replay PASS, exit 0.
ISS: 3888 instructions. RV32_5S: 3887 instructions, 4996 cycles.
ELF SHA256: 5be81ef49e560dcb2448aae4cc4c34bcf656fc5f6ac86bb485d932939405050e.
Addresses below apply only to this exact build; re-check disassembly after edits.

## Initial heuristic

The input ranks are p=945 and o=296. Both actual PDB distances are 3.
Reset, then use a breakpoint around 0x1264 and single-cycle stepping. Identify
this instruction in each stage rather than assuming the breakpoint stops all
stages at the same logical point.

| Address | Instruction | What to inspect |
|---|---|---|
| 0x125c | add t0,a2,a0 | Computes pd base + rank: 0x100003fc + 945 |
| 0x1260 | add t1,a3,a1 | Computes od base + rank: 0x10000120 + 296 |
| 0x1264 | lbu a0,0(t0) | Byte value 3; WB enable=1, writeback mux MEMREAD=0 |
| 0x1268 | lbu a1,0(t1) | Byte value 3; same load/writeback path |
| 0x126c | bgeu a0,a1,heuristic_done | 3>=3, taken; h stays 3 |

Record actual IF/ID/EX/MEM/WB cycles, addresses/data and screenshots. Explain
why the memory byte, rather than its address, is written to the register.

## First generated child and memory update

After root initialization, the first attempted move is R. Root p/o are 945/296;
the transition produces child p/o 1905/353. These are predictions from the table
and independent geometric replay, not a substitute for observing the GUI.

| Address | Instruction | Meaning |
|---|---|---|
| 0x115c | lhu a0,0(t0) | Read 16-bit child permutation rank |
| 0x1160 | lhu a1,0(t1) | Read 16-bit child orientation rank |
| 0x1164 | sw a0,8(s0) | At MEM write 1905 to root child_p |
| 0x1168 | sw a1,12(s0) | At MEM write 353 to root child_o |

The root frame starts at 0x10009ef0. Inspect memory words 0x10009ef8 and
0x10009efc before/after these first stores. Initial values 945/296 should change
to 1905/353. For each store, data_mem.wr_en=1 in its MEM stage; it has no register
writeback. Contrast with the earlier load's registerFile.wr_en=1 in WB.

Follow an arithmetic instruction such as `add t0,a2,a0` for the ALURES=1 writeback
mux selection. The opcode-control values apply to each instruction as it moves
through the pipeline; other instructions execute concurrently.

## What the student must provide

- Actual stage-by-stage observations and enough clearly labeled GUI screenshots.
- Explanation of register enable, ALU/memory writeback selection, and memory writes.
- Explanation of any stalls/forwarding actually observed.
- Own English report analysis tied to this code (eventually the final submission
  build), rather than copying these preparation notes as personal observations.
