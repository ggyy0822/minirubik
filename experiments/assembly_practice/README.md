# Guided assembly search, first complete version

Student exercise fragments and AI scaffolding have separate provenance comments.
The final control fragment was supplied by the student; the assistant transcribed
it and provided the ABI adapter, build harness, and tests. The executable still
uses the educational GCC baseline C input parser and independent physical replay.
It is not an entirely handwritten assembly submission.

Reproduce from repository root:

```sh
python3 experiments/rv32_baseline/run.py 21345671111111 --implementation assembly
python3 experiments/rv32_baseline/run.py 54721631111111 --implementation assembly
python3 experiments/rv32_baseline/run.py 25314672313211 --implementation assembly --processor RV32_5S
python3 experiments/rv32_baseline/audit.py --directory output/assembly_search
```

Ripes is run with QT_QPA_PLATFORM=offscreen, RV32_ISS, no renderer, no ISA
extensions. Same precomputed tables, input parser, physical replay, output code,
search order, heuristic, and compiler flags as GCC baseline. Counts include
input parsing, search, replay, output, and exit. Wall times are observations,
not a controlled speed comparison (some processes overlapped).

| Input | GCC -O2 retired | Assembly retired | Length |
|---|---:|---:|---:|
| 12345671111111 | 1003 | 1019 | 0 |
| 25314672313211 | 1785 | 1909 | 1 |
| 21345671111111 | 15239117 | 22211301 | 11 |
| 54721631111111 | 41665257 | 60727876 | 11 |

All four assembly ISS cases pass target physical replay and native exact-distance
optimality checks. The one-move case also passes RV32_5S (1908 retired, 2581 cycles).
The hard sample exceeds 50 million instructions: the performance requirement is
NOT satisfied. It was chosen by native generated-child count, not proven to
maximize target instruction count. All 2644 hard cases have NOT been target-tested.

Assembly executable .text: 1868 bytes (GCC 1764).
.data+.bss+.rodata: 49252 bytes (GCC 48872), under 131072.
Audit passes base RV32I instruction whitelist, no undefined symbols or arithmetic
helpers. Native exhaustive results from the C baseline do not establish exhaustive
correctness of this assembly implementation.

Optimization lesson: readability-oriented helpers repeatedly save/restore the
stack and move arguments in the inner search loop. Investigate eliminating those
costs while preserving register values, table state, and traversal order. Preserve
this first implementation for a measured before/after comparison.

Raw reports and source hashes: ../results/assembly_search/.

## Second version: student-completed inline pruning

The current build replaces only the child heuristic/prune calls with the
student's inline code. The now-unused evaluate_state/should_prune routines are
retained as exercises but omitted from the executable. Initial heuristic still
calls heuristic. No search-order or pruning-rule change.

| Input | First assembly | Inline pruning | GCC -O2 |
|---|---:|---:|---:|
| 21345671111111 | 22211301 | 17298120 | 15239117 |
| 54721631111111 | 60727876 | 47292244 | 41665257 |

Both eleven-move paths are unchanged; target replay and exact host optimality
checks pass. Solved and one-move ISS and one-move 5S regressions also pass.
The hard sample now meets the 50-million cap, but the all-2644-state target gate
remains unverified. Per generated child, inline pruning saves 21 retired
instructions in these runs. GCC remains ahead on both hard examples.
Current .text is 1804 bytes, static data remains 49252 bytes. Base RV32I and
symbol/size audits pass. Original source snapshot: ../results/assembly_search/v1-source/.
Current source snapshot and results: ../results/assembly_search/v2-inline-prune/.
Snapshots preserve version provenance; build source remains this directory.

## Third version: student-completed inline transition

The six quarter_step instructions now appear directly in advance_child. The
standalone quarter_step exercise is retained but omitted from the target link.
No other search logic changed. Under the current --no-relax build, removing
AUIPC/JALR for call and JALR for ret saves three instructions per generated child.

| Input | Inline pruning (v2) | Inline transition (v3) | Saved |
|---|---:|---:|---:|
| 21345671111111 | 17298120 | 16596237 | 701883 |
| 54721631111111 | 47292244 | 45372868 | 1919376 |

Both retain exactly the same paths and pass target replay and exact host
optimality. Solved ISS: 1019 retired; one-move ISS: 1837 retired; one-move 5S:
1836 retired, 2457 cycles. All pass replay and optimality. RV32I opcode,
undefined-symbol, arithmetic-helper, and static-size audits pass.
.text is 1792 bytes; static data remains 49252 bytes. Removing the now-unused
standalone helper contributes to the code-size reduction. These sample results
still do not establish performance compliance over all 2644 distance-11 states.
Versioned reports, disassembly and source snapshot: ../results/assembly_search/v3-inline-transition/.

## Fourth version: reuse child registers

The student removed the two redundant child_check loads. Inspection confirms
child_check has only fall-through entry from advance_child in student_search.S.
The preceding stores do not modify a0/a1; no intervening call exists. The stores
remain because the frame is still used by subsequent generation/initialization.

| Input | v3 retired | v4 retired | Saved |
|---|---:|---:|---:|
| 21345671111111 | 16596237 | 16128315 | 467922 |
| 54721631111111 | 45372868 | 44093284 | 1279584 |

Two instructions saved per generated child. All four ISS sample paths and the
one-move 5S path match v3 and pass replay/optimality. Solved ISS: 1019;
one-move ISS: 1831; one-move 5S: 1830. Current .text: 1784 bytes; static data:
49252 bytes. RV32I, symbol and size audit passes. Full hard-state coverage is
still pending. Reports and snapshot: ../results/assembly_search/v4-reuse-child-registers/.
