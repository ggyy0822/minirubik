# Actual solver GUI evidence index

AI-organized evidence index; not student report prose.
Build: output/assembly_search/23745612123332.elf, frozen v4.
Processor: ordinary RV32I 5-stage processor.

| Observation | Evidence |
|---|---|
| Load MEM address 0x100007ad and data 3 at cycle 667 | [Address](cycle667-load-address.png), [data](cycle667-load-data.png) |
| Load WB register write enable 1 at cycle 668 | [Write enable](cycle668-load-write-enable.png) |
| WB mux input 0 contains 3; select itself not observed | [Input data](cycle668-writeback-input0.png) |
| a0 committed as 3 at cycle 669 | [Register](cycle669-a0-committed.png) |
| Child permutation memory before store: 945 | [Cycle 750](cycle750-store-before.png) |
| Store MEM write enable 1; a0=1905 | [Cycle 753](cycle753-store-enable.png) |
| Memory 0x10009ef8 becomes 1905; bytes 71 07 00 00 | [Cycle 754](cycle754-store-full.png) |
| Complete run: 3 moves, replay PASS, exit 0, 4996 cycles / 3887 instructions | [Completion](solver-completed-4996-cycles.png) |

Signal source predictions must be distinguished from tooltip observations.
These screenshots do not constitute exhaustive correctness or the student's own
English pipeline analysis. A changed final build needs applicable revalidation.
