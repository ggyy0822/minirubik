# GCC RV32I educational baseline

AI-generated teaching/reference code and experiments, not student-authored
design, analysis, or handwritten assembly. This is a compiler baseline for the
candidate algorithm, not a final coursework submission.

## Split between host and target

- `generate.c` runs only on the Mac and writes immutable quarter-turn transition
  tables and two projection distance tables. It does not solve the query.
- `search.c` runs on the target. It uses iterative bounds, a fixed explicit
  stack, max(permutation distance, orientation distance), and same-face pruning.
- `state.c` parses arbitrary compile-time 14-character input and replays the
  returned moves using physical corner permutations/twists, without relying on
  the generated transition tables for replay.
- `main.c` invokes search and checks replay before printing the solution.
- `start.S` initializes the stack and implements Ripes output/exit calls. This
  is infrastructure assembly; the solver is still GCC-generated machine code.
- `verify_native.c` compiles the **same** `search.c` and `state.c` for host-side
  validation against the upstream exact BFS oracle.

The host BFS and host generation queues are never linked into the target ELF.
No full-domain distance table is included in the target data.

## Build and measure

From the repository root:

```sh
python3 experiments/rv32_baseline/run.py 21345671111111
python3 experiments/rv32_baseline/run.py 25314672313211 --processor RV32_5S
python3 experiments/rv32_baseline/audit.py
```

The run helper builds the chosen input, runs Ripes, verifies target replay and
exit status, and checks the printed path with the native upstream oracle.
Specify `--ripes /absolute/path` if needed. Raw logs, JSON measurements,
ELFs, maps, disassembly, and section reports are under `output/rv32_baseline/`.
The immutable input string is linked into the ELF; no host-generated solution
is embedded. Change it with the run helper or `make -C experiments/rv32_baseline
INPUT=...`.

Compiler: Homebrew `riscv64-elf-gcc` 16.2.0, `-O2 -march=rv32i -mabi=ilp32`.
Additional flags disable library/builtin assumptions, stack protectors, small
data addressing, and relaxation. No standard library or compiler arithmetic
helper is linked. Actual compiler name differs from the assignment's
`riscv64-unknown-elf-gcc`; retain this identity in any comparison.

The target arithmetic avoids multiply/divide helpers: move classification uses
small lookup tables; transition row pointers avoid variable row multiplication;
input ranking uses explicit shift/add and conditional subtraction.
The algorithm, ordering and pruning are otherwise the educational reference's.
Search counters were removed from the measured target build.

## Measurement conventions

The renderer is absent. `.text` is the complete linked target code, including
input parsing, path replay, text output and startup. `--iret` counts the complete
program, not only the search. Static data means `.data + .bss + .rodata`, including
the 8 KiB reserved stack. All four tested input ELFs have `.text` 1,764 bytes and
static data 48,872 bytes (`.rodata` 40,680 + `.bss` 8,192).

Tests use `QT_QPA_PLATFORM=offscreen`. Do not combine their wall times with the
earlier user-run normal-backend speed probes. Some runs overlapped native
validation, so wall times are execution records rather than controlled speed
benchmarks; retired instruction counts do not depend on host scheduling.
Raw model counts are reported unchanged, including the observed one-instruction
ISS/pipeline difference at program termination.

The first string-output attempt used ecall 4, whose observed output contained
NUL bytes. The recorded current runtime emits characters via ecall 11 instead.
The preliminary `21345671111111-ISS.txt` file predates this change and is not a
current baseline measurement; use `*-RV32_ISS.txt` and their matching JSON files.

## Checks and scope

- Exported table equality to host generation, transition range/bijection/maxima,
  solved successors, and PDB population/maxima/solved entries are checked.
- H1 checks all states against the exact host BFS distance.
- Native quick checks cover eight reference vectors and all nine one-move states,
  plus invalid inputs. Both target replay and upstream physical replay are used.
- `verify_native --all` checks parsing/ranking, optimal length, and both path
  replays over every state. This completed successfully for all 3,674,160
  states; loop wall time 323.239 seconds. It includes H1 traversal, parsing and
  replay work, excludes oracle/table construction, and overlapped some target
  runs. See `../results/rv32_baseline/native-all.txt` for the raw result.
- No packed accessors exist; H4 is not applicable to this candidate.
- The instruction audit checks decoded instructions against base RV32I,
  requires 32-bit encodings, and rejects undefined symbols/arithmetic helpers.

Native commands:

```sh
make -C experiments/rv32_baseline native-check
./output/rv32_baseline/verify_native --all
```

## Recorded target results

| Input | Model | Optimal length | Retired instructions |
|---|---|---:|---:|
| `12345671111111` | RV32_ISS | 0 | 1,003 |
| `25314672313211` | RV32_ISS | 1 | 1,785 |
| `21345671111111` | RV32_ISS | 11 | 15,239,117 |
| `54721631111111` | RV32_ISS | 11 | 41,665,257 |
| `12345671111111` | RV32_5S | 0 | 1,002 |
| `25314672313211` | RV32_5S | 1 | 1,784 |

Every row completed with target replay PASS and a separate host oracle check
of the printed path and its optimal length. The distance-11 stress case was
chosen for the largest generated-child count in the native reference, not an
established maximum of target instruction counts. Results do not prove the
universal target performance gate. Source/table/ELF hashes, compiler identity,
raw reports, and instruction/section audit results are retained in
`../results/rv32_baseline/`.

## Outstanding

No handwritten solver assembly, LED renderer, or GUI signal walkthrough exists
yet. Target testing currently covers solved/one-move states on both models and
two distance-11 examples on ISS. It does not establish full T7 or the universal
50,000,000-instruction bound. The largest native generated-child count is a
candidate for instruction stress testing, not proof of the maximum target count.
All 2,644 distance-11 inputs still need the required target performance coverage.
