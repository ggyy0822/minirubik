# Submission readiness — 2026-10-05

Administrative evidence map prepared by AI. Not a finished student report or a
claim that AI-authored reference artifacts satisfy the assignment's own-work rule.
Assignment: https://hackmd.io/@sysprog/2026-arch-homework1

| Requirement / original section | Current evidence | Remaining work |
|---|---|---|
| Stages 1: memory and speed measurements | ../measurements/stage1/ | Student explains method, interpretation and limitations |
| Correctness H1/H2/H3 | ../experiments/results/ (host reference checks) | Identify exact final implementation and applicable evidence |
| Constraints: own RV32I implementation, measured refinements | ../experiments/assembly_practice/ and ../experiments/results/assembly_search/ | Resolve authorship and final source scope; do not claim AI reference components as own work |
| Stages: <=128 KiB static data | Existing v4 audit/static total 49252 bytes | Recheck final build; distinguish LED runtime variant |
| Stages: all distance-11 inputs <=50M retired instructions | Full frozen-v4 gate launched under ../experiments/results/hard-target/da7aaa48b90f7555/ | Wait for completion and inspect results; partial coverage is not full proof |
| T5/T6/T7 target replay and cross-model runs | ../experiments/results/cross-model-v4/ | Revalidate if final build changes |
| LED actual path visualization | ../experiments/results/led/ | Explain mapping; static screenshots alone do not establish animation timing |
| Pipeline load/store walkthrough | ../experiments/results/pipeline/gui/README.md | Student analysis; mux select was inferred from source, not directly observed |
| Constraints: compare assembly to same-algorithm GCC -O2 | Versioned assembly measurements and C reference | Explain nonwinning results; use consistent runtime/build conventions |
| Documentation: English analysis and >=3 substantive revisions | REPORT_WORKSHEET.md is only an unanswered outline | Student writes analysis; preserve real revisions, no fabricated history |
| Documentation / Submission: fork, public HackMD, tag/revision/form | URLs not yet provided | Create or identify destinations, review source, commit/push/tag, publish and submit |

## Suggested order while the long test runs

1. Student writes the baseline/design explanation in their own words.
2. Check reasoning and refine the student's English without supplying missing analysis.
3. Identify the GitHub fork and HackMD note and retain genuine development revisions.
4. Resolve final source authorship/build scope before claiming submission readiness.
5. Inspect completed performance results and validate any changed final build.
6. Complete remaining report sections and submission metadata.

Technical progress estimate remains 64%; this is not a grading percentage.
