# Host path checker

AI-generated testing assistance. The helper includes the unchanged upstream
`solver.c` to reuse its input parser, move model, and exact BFS table.
It checks a supplied path; it does not implement the student's search.

Build from the repository root:

```sh
mkdir -p output
cc -O3 -std=c99 -Wall -Wextra -Wpedantic tests/verify_path.c -o output/verify_path
```

Check a solved state with an empty path:

```sh
./output/verify_path 12345671111111 ""
```

Check the assignment's reference vector with the upstream solution:

```sh
./output/verify_path 21345671111111 "B' R' D2 R' B R B' R D2 B R'"
```

Check a valid but nonoptimal path for the solved state:

```sh
./output/verify_path 12345671111111 "R R'"
```

The last example intentionally reports `solved: yes`, `optimal: no` and exits
with status 1. Exit 0 means solved and optimal; exit 1 means failed validation
or an internal/output error; exit 2 means invalid input or an unknown move.

Limitations: native host execution only; shares the upstream cube model rather
than providing an independent model. These examples do not discharge exhaustive
H3, target T5, or the target performance gate. Full BFS storage is used only
in the host checker, never proposed as target data.
