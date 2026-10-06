# v5: complete assembly target (AI-assisted)

This is the current coursework candidate. Unlike v1–v4, no target C source is
compiled or linked: entry, inline-input parsing/ranking, IDA* search, independent
physical replay, console output and optional LED integration are assembly.
The search retains the student's guided fragments; v5 edits and runtime are
AI-authored. This is directly written assembly, not compiler-generated C assembly;
it is not a claim that the student independently authored every instruction.

## Build and run

```sh
python3 experiments/rv32_full/build.py 23745612123332 --render 0
python3 experiments/rv32_full/run.py 23745612123332
python3 experiments/rv32_full/build.py 25314672313211 --render 1
```

The measured ELF is `output/rv32_full/STATE-measure.elf`. Load
`output/rv32_full/STATE-render-gui.s` into Ripes with LED Matrix 0 at Width=35,
Height=25. The wrapper uses peripheral base/width/height symbols. It represents
the linked handwritten payload as Ripes-compatible source; it does not translate
C into assembly. Renderer-off and renderer-on are compile-time choices in the
same assembly implementation. Never include renderer-on counts in the 50M gate.

Host C generates immutable PDB/transition constants. The builder converts their
numeric declarations into `.byte`/`.half` tables; target executable inputs are
only `.S` files. No allocator, recursion, M extension or compiler helper routines
are linked. Input text is `.asciz CUBE_INPUT`; the target itself validates ranges,
unique cubies, exact length and twist sum, then computes ranks.

## Design and optimization

- The algorithm remains iterative IDA*: `h=max(pd[p],od[o])`, bound increments,
  an explicit 12-frame array, and same-face pruning.
- Each frame is 32 bytes, with the same field offsets as v4.
- `t3/t4` hold PDB base addresses during search. The only called search helper,
  `heuristic`, uses `t0/t1` and does not clobber those bases. Path copying may
  reuse `t3` only after searching finishes.
- Child/root frame initialization is inline. Child ranks remain in `a0/a1`, so
  storing them directly removes argument setup, reloads and call overhead.
- Parser multiplication is bounded integer addition. The final trivial Lehmer
  digit is omitted; a zero prefix skips multiplying zero.
- Physical replay uses its own corner permutation/twist rules, not search tables.
  A 16-byte temporary buffer prevents overwriting corners still needed by a turn.

## Evidence and limitations

[Measured cases](../results/rv32_full/measurements/summary.json),
[GCC comparison](../results/rv32_full/comparison.json),
[ISA/static audit](../results/rv32_full/audit.json),
[parser/replay tests](../results/rv32_full/state-check/summary.json), and
[all-pixel render checks](../results/rv32_full/led/summary.json).

Renderer off: `.text=1564`, `.rodata+.bss+.data=49217` bytes, including an 8192-byte
reserved stack. GCC reference text is 1764 bytes. The reference and stress inputs
use 14,958,590 and 40,894,417 instructions, respectively. A three-step exception
uses 3803 versus GCC's 3730; do not claim an instruction win for every input.
The exact reference compiler is the installed `riscv64-elf-gcc` 16.2.0, using
`-O2 -march=rv32i -mabi=ilp32` plus the documented freestanding/no-relax flags.

The full 2644-case gate passed with zero failures; see
[complete evidence](../results/rv32_full/completed-gate/README.md).
It is separate from v4. To reproduce (can take hours):

```sh
python3 experiments/rv32_full/run_hard.py --all
```

Results are fingerprinted under `experiments/results/rv32_full/hard-target/`.
Do not change executable source files during a run. Only a complete summary
with 2644 passes supports the universal distance-11 instruction claim.
The older GUI pipeline screenshots refer to v4; their addresses/cycles must not
be presented as v5 observations. New cross-model runtime results are in the v5
measurement summary.
