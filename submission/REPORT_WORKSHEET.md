# Assignment 1 — student report worksheet

This file is an AI-generated outline with questions, not completed report prose.
Replace prompts with your own reasoning, observations and verified measurements.
Do not claim the AI reference implementation or AI-run measurements as your own.
Keep actual, substantive development revisions; do not fabricate earlier dates.

Author: [fill in]
GitHub fork: [fill in]
Submission commit/tag: [fill in after final validation]
HackMD URL/revision: [fill in]
Ripes commit/build fingerprint: [verify and fill in]
Compiler version/target flags: [verify and fill in]

## 1. Baseline and the target machine

- Explain what the original BFS solver computes and why it produces shortest paths.
- Define the seven movable corners, permutation rank, and orientation rank.
- Derive the state count, identify the group/generators and Cayley graph, and
  explain the modulo-3 orientation constraint. Distinguish HTM from QTM.
- Explain what exhaustive BFS proves about diameter 11; distinguish this from
  solving one particular input in 11 moves.
- Account for the baseline's memory allocations. Critically assess the upstream
  report's advice to retain the full distance table when moving to Ripes.
- Describe YOUR memory/speed experiments, controls, repetitions, measurements,
  limitations and projection to the full baseline. Link raw logs and source.

## 2. Representation and search design

- State the design you personally chose and why it meets the target constraints.
- Explain the factored transition tables, what the PDBs abstract, and why the
  selected heuristic cannot overestimate. Explain max vs addition.
- Describe the iterative-deepening bound, explicit search frames, pruning,
  backtracking, path reconstruction, termination and shortest-path guarantee.
- Identify the costs this choice removes, adds, or trades against memory.

## 3. C refinement

- Identify the starting and final C versions, YOUR modifications and rationale.
- Compare operation counts and measured results, including negative results.
- Explain how multiplication/division, branches and memory accesses are handled.

## 4. RV32I implementation and measured refinements

- Identify handwritten and compiler-generated components explicitly.
- Explain the ABI, saved registers, frame fields, halfword/byte indexing and
  the instruction sequences used to avoid unsupported arithmetic.
- Link each real revision and same-input measurement. State .text and retired
  instruction conventions, renderer status, processor and toolchain versions.
- Compare the final assembly with GCC -O2 on the SAME final C algorithm.
  Discuss any case where assembly does not win; do not mix runtime variants.

## 5. Correctness and resource gates

- H1/H2/H3/H4: input domain, independent oracle, coverage, outcome, elapsed time.
- T5/T6/T7: on-target replay, reference 11-step case, three-case cross-model tests
  and additional arbitrary inputs. Clearly distinguish host and target evidence.
- Memory: every table, buffers, stack, section totals and peak working set.
- Final renderer-disabled RV32_ISS worst-case gate: all 2644 distance-11 inputs,
  coverage/failures, maximum count and its state, plus the separately reported
  reference input. A sampled maximum is not the full-domain maximum.

## 6. LED visualization

- Derive coordinate-to-address mapping and the unfolded-net layout.
- Explain cubie orientation to sticker color mapping, RGB words and actual-path
  replay. Include GUI evidence and distinguish it from host-rendered previews.
- Explain GUI/CLI build generation and exactly what the render switch excludes.

## 7. Pipeline walkthrough

- Follow selected instructions through IF/ID/EX/MEM/WB using actual screenshots.
- Explain observed register write enable, mux choices, forwarding/stalls, and
  memory updates. Tie each signal to its instruction and pipeline stage.
- Use the final submitted program, with the small practice harness as preparation.

## 8. Limitations, authorship, AI disclosure and reproducibility

- Accurately identify every AI-assisted artifact/action and what you did yourself.
- Explain accepted/rejected suggestions in your own words. Disclosure alone does
  not waive the assignment's own-work requirements.
- List remaining limitations and reproducible build/test instructions.
- Link your code in your fork; quote only short relevant fragments in this note.

## Revision record

Record at least three REAL substantive revisions as development proceeds:
1. [date/revision link; actual additions or changes]
2. [date/revision link; actual additions or changes]
3. [date/revision link; actual additions or changes]

## Publication checklist

[ ] All report writing is English and is your own analysis.
[ ] Publicly readable HackMD; owner-only editing.
[ ] Fork contains meaningful commits, source, tests and measurement evidence.
[ ] Final commit tagged; tag and HackMD revision recorded on the submission form.
[ ] Form receipt retained. Check the course page/instructor for the missing link.
