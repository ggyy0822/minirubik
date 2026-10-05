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
