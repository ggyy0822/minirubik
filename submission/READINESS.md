# Submission readiness — 2026-10-06

The student reports updated instructor permission for AI assistance. Actual
student/AI contributions remain identified; no independent-authorship claim.

| Item | Current status |
|---|---|
| Current candidate | `experiments/rv32_full`, full assembly v5 |
| Inline input / target parsing / replay / output | Implemented directly in RV32I; no target C executable linked |
| Algorithm | Iterative IDA*, static frames, admissible maximum of two PDBs |
| ISA/static audit | PASS; renderer off 49,217 static bytes, 1,564 text bytes |
| GCC comparison | Text smaller; 4/5 measured instruction wins, 3-step exception documented with phase attribution |
| Parser/replay component tests | 5,769 rank cases, 11 invalid inputs, 1,000 physical moves PASS |
| Final cross-model tests | Solved, one-step, three-step, reference-11 PASS on ISS and 5S |
| v5 LED pixel checks | 17 frames × 875 pixels PASS |
| GUI pipeline screenshots | Historical v4 evidence, addresses/cycles not relabeled as v5 |
| Host full-domain H1/H2/H3 | PASS for C/reference; not exhaustive assembly verification |
| All 2,644 distance-11 target cases | v5 fingerprinted background run pending; v4 evidence remains separate |
| English report | Local draft updated for v5, including non-winning case |
| HackMD | Latest online synchronization and owner-only editing still unverified |
| GitHub fork | Existing; final v5 publication status must be checked against Git |
| Final tag / pinned note revision / submission form | Pending; no submission receipt |

Do not change the frozen v5 executable sources during its complete gate. Tests
and source completion do not by themselves mean the coursework was submitted.
