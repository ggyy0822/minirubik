# Submission readiness — 2026-10-06

The student reports updated instructor permission for AI assistance. Actual
student/AI contributions remain identified; no independent-authorship claim.

| Item | Current status |
|---|---|
| Current candidate | `asm/src/` and `asm/minirubik.s`, byte-identical full assembly v5 |
| Inline input / target parsing / replay / output | Implemented directly in RV32I; no target C executable linked |
| Algorithm | Iterative IDA*, static frames, admissible maximum of two PDBs |
| ISA/static audit | PASS; renderer off 49,217 static bytes, 1,564 text bytes |
| GCC comparison | Text smaller; 4/5 measured instruction wins, 3-step exception documented with phase attribution |
| Parser/replay component tests | 5,769 rank cases, 11 invalid inputs, 1,000 physical moves PASS |
| Final cross-model tests | Solved, one-step, three-step, reference-11 PASS on ISS and 5S |
| v5 LED pixel checks | 17 frames × 875 pixels PASS |
| GUI pipeline screenshots | Historical v4 evidence, addresses/cycles not relabeled as v5 |
| Host full-domain H1/H2/H3 | PASS for C/reference; not exhaustive assembly verification |
| All 2,644 distance-11 target cases | v5 complete: 2644 PASS, 0 FAIL, maximum 40894417; provenance matches |
| English report | Local draft updated for v5, including non-winning case |
| HackMD | User reports permissions fixed; updated structured report still needs online paste |
| GitHub fork | v5 code pushed; complete evidence included in phase1-v5 snapshot |
| Final tag / pinned note revision / submission form | Tag phase1-structured-v1 (phase1-v5 retained); HackMD revision and accepted email pending |

Do not change the frozen v5 executable sources during its complete gate. Tests
and source completion do not by themselves mean the coursework was submitted.

Canonical layout: baseline/, asm/, tests/, results/, docs/, tools/. Root make/build, test, compare passed; eight ELF section/layout comparisons and all archived hard case records passed. Fresh five-input comparisons reproduce v5 counts; standalone Ripes source passed four-frame pixel comparison.
