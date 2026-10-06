# minirubik — RV32I coursework

An optimal 2×2×2 cube solver using iterative IDA*, factored transition tables and
`max(permutation distance, orientation distance)`. The final target is directly
written RV32I assembly, including input parsing, search, independent replay and
output. AI assistance and guided student contributions are disclosed in the report.

- [HackMD report](https://hackmd.io/@tang930822/HksBNm-jGe)
- [Report backup](docs/report.md)
- [Optimization history](docs/optimization.md)
- [Correctness summary](results/correctness.md)
- [GCC comparison CSV](results/comparison.csv)

## Layout

```text
minirubik/
├── README.md
├── Makefile
├── baseline/                 # Final C algorithm compiled with GCC -O2
│   ├── main.c
│   ├── search.c
│   └── state.c               # Also target.h and start.S
├── asm/
│   ├── minirubik.s           # Standalone Ripes program; LED rendering ON
│   └── src/                  # Readable, maintained handwritten assembly
├── tests/
│   ├── cases/                # Representative inputs and all 2644 hard states
│   ├── verify_host.py        # H1–H3; H4 explicitly not applicable
│   ├── verify_ripes.py       # T5–T7 and optional full hard-state rerun
│   ├── compare.py           # Actual GCC/assembly Ripes measurements
│   ├── verify_layout.py     # Relocation equivalence and archived gate audit
│   └── verify_single.py     # Standalone .s pixel check in a RAM framebuffer
├── results/
│   ├── correctness.md
│   ├── comparison.csv
│   ├── layout-equivalence.json
│   └── raw/                 # Original evidence archive and new measurements
├── docs/
│   ├── report.md
│   └── optimization.md
└── tools/                   # Build, host table generator, linker script
```

`experiments/` and `submission/` retain historical versions/evidence and the
HackMD-ready export. They are not the primary entry points. The original
`solver.c` and `mini.c` remain the upstream BFS baseline and independent oracle.

## Build

Requires Python 3, a native C compiler, `riscv64-elf-gcc`/binutils and Ripes with
RV32_ISS. Validated compiler: GCC 16.2.0; Ripes commit
`5b8a616edcb6f0a2ddb07e78951348b72497f1e1`. The compiler prefix differs from the
assignment's example `riscv64-unknown-elf-`; flags and version are disclosed.

```sh
make                         # Build C + assembly ELF, export asm/minirubik.s
make asm INPUT=25314672313211 # Change the inline cube and regenerate single file
make baseline INPUT=21345671111111
```

The committed single file uses the three-step input `23745612123332`. It needs no
includes or compiler to load in Ripes: create **LED Matrix 0**, set **Width 35,
Height 25**, select **RV32_ISS**, load `asm/minirubik.s`, and run. The generated
file adapts the linked handwritten assembly to Ripes syntax; it is not C output.
Edit maintained code in `asm/src/` and regenerate; do not edit numeric labels in
the exported file. Host C only generates constant tables for the assembly build.

The single file has rendering enabled. **Measure renderer-off ELF files** under
`output/coursework/` through the commands below; do not count the GUI bootstrap
or rendering as solver-only measurements.

## Test and compare

```sh
make test          # Equivalence + H1/H2 + sampled H3 + short ISS/5S + single file
make compare       # Fresh five-input GCC vs assembly instruction/text comparison
make measure INPUT=21345671111111
make verify-host   # Full H1/H2/H3; H4 N/A (several minutes)
make verify-ripes  # Full representative T5–T7, including 11 moves on five-stage
make verify-full   # Full host checks + T5–T7 + all 2644 hard inputs (hours)
make check-upstream # Original BFS/mini checks
```

`make test` explicitly does **not** rerun exhaustive H3 or the full hard-state
simulation. It checks preserved complete evidence and executable equivalence;
long rerun commands are separate. Original outputs are retained under
`results/raw/`; fresh logs go under `results/raw/current/`.

For a different installation, export `RIPES=/path/to/Ripes`,
`CROSS=riscv64-unknown-elf-` and/or `CC=clang` before running make. Measurements
from a different toolchain/model require fresh validation.

## Validated results

All **2644/2644 distance-11 states** pass, maximum **40,894,417** instructions.
Reference input: **14,958,590**. Assembly text: **1564 bytes**, GCC: **1764**.
The three-step case is a documented exception: **3803 vs GCC 3730** instructions.
Do not claim an instruction win for every input.

The structured source copies and eight representative ELF layouts/sections are
identical to validated v5. Historical `phase1-v5` is retained; the organized
snapshot is `phase1-structured-v1`. Formal course submission and its `accepted`
email are separate from building, testing or tagging the repository.
