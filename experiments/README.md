# Educational IDA* reference experiment

**Provenance:** AI-generated teaching/reference implementation. The assistant
authored and executed this experiment. It is not represented as student-written
design, analysis, or assembly, and is not a ready-to-submit assignment artifact.
The student's own design and the assignment's authorship requirements still apply.

## What it does

The existing upstream `solver.c` is unchanged. The experiment includes it to
reuse cube parsing, rank/unrank, physical moves, and the exact host BFS oracle.
It generates quarter-turn permutation/orientation transitions on the host, then
builds two byte-per-entry projection distance tables. The heuristic is their
maximum. Search iterates bounds from the root heuristic through 11 and uses an
explicit 12-frame stack, with no allocation or recursion inside `search()`.
Consecutive turns of the same face are skipped. Moves are visited in the
upstream order: R, R2, R', B, B2, B', D, D2, D'.

Read these functions in order:

1. `heuristic`: lookup and combine the two estimates.
2. `search`: bounded depth-first traversal using an explicit stack.
3. `prepare` and `make_distances`: host-only table construction.
4. `oracle_distances`, `verify_path`, `check`: host-only validation.

`expanded` counts frames entered, including root frames on repeated iterations
and terminal goal frames. `generated` counts child states produced after
same-face pruning but before heuristic pruning, across all iterations.
Neither count is a retired instruction count.

## Run from the repository root

```sh
cc -O2 -std=c99 -Wall -Wextra -Wpedantic experiments/ida_reference.c -o output/ida_reference
./output/ida_reference 21345671111111
./output/ida_reference --check
./output/ida_reference --check-hard
```

`--check` checks heuristic admissibility over the complete domain, PDB
population/maxima/solved entries, eight supplied vectors, and all nine
one-move states. It does not search the whole domain.

`--check-hard` searches every one of the 2,644 distance-11 states and checks
both exact path length and path replay using the upstream physical move model.

For exhaustive host search validation, run:

```sh
./output/ida_reference --check-all > output/ida_reference_all.txt 2> output/ida_reference_all_progress.txt
```

The printed wall time for this command covers the search and path-replay loop,
not host table generation or the preceding admissibility check.

## Results obtained so far

- Heuristic admissibility: all 3,674,160 states passed.
- Both PDBs fully populated, solved entries zero; maxima 7 (permutation) and
  6 (orientation).
- Eight reference vectors plus nine one-move states passed optimal-length and
  physical path-replay checks. AddressSanitizer/UndefinedBehaviorSanitizer run
  of `--check` completed without diagnostics.
- All 2,644 distance-11 states passed host search/path verification; measured
  loop wall time 3.125 seconds on this execution environment.
- Full-domain H3-style validation completed: all 3,674,160 searches returned
  the exact BFS length and paths replayed to solved. Search/path-replay loop
  wall time: 342.518 seconds. See `results/full-domain-check.txt`.
- Required vector `21345671111111`: initial h=7, length=11, five bounds,
  38,999 entered frames and 233,961 generated children.
- Worst generated-child count among distance-11 states: 639,792 at
  `54721631111111` (106,636 entered frames, initial h=6, six bounds).
- Table payload: 34,614 bytes of transitions plus 5,769 bytes of PDBs =
  40,383 bytes. Explicit search stack: 120 bytes on this native build.
  These are component sizes, not a measurement of a linked RV32I image.

## Remaining work and limits

- The full-domain host result applies only to this recorded C experiment;
  subsequent algorithm changes require appropriate revalidation, and target
  assembly requires separate target checks.
- No packed tables are used, so there is no packed accessor to check (H4).
- This host executable includes full BFS validation and host generation data.
  It must not be used to claim target static-data compliance. A target build
  needs separately generated read-only tables and removal of the host oracle.
- No target assembly, GCC RV32I reference build, target instruction measurement,
  T5-T7 validation, or renderer has been implemented in this experiment.
- The 50,000,000-instruction worst-case gate remains unmeasured. Native speed
  and node counts do not establish that gate.
- The checker shares upstream cube/ranking routines; it is not an independent
  implementation of the physical cube model.
- A subsequent environment setup installed Homebrew's `riscv64-elf-gcc` 16.2.0
  and binutils, then ran an RV32I ELF smoke test on ISS and RV32_5S. See
  `toolchain/README.md` for the actual compiler naming and reproducible command.
  The solver itself has not yet been cross-compiled or measured.
