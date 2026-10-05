# Unified submission candidate

AI-assisted integration, with original guided search provenance preserved.
The student reports that the instructor now permits AI use; this repository
continues to disclose the actual assistance. Technical validation is independent
of that permission.

## Build from repository root

```sh
python3 experiments/final/build.py 23745612123332 --render 0
python3 experiments/final/build.py 25314672313211 --render 1
```

The builder generates tables when missing. Requirements: Python 3, a native C
compiler, riscv64-elf-gcc/binutils, and the pinned Ripes build.

Renderer off: load `output/final/23745612123332-measure.elf` as an ELF in Ripes,
or run it through CLI with `-t elf --proc RV32_ISS --iret --cycles`.
Renderer on: add LED Matrix 0 (35 wide, 25 high), select RV32_ISS, then load
`output/final/25314672313211-render-gui.s` as assembly source.
Do not use the renderer ELF directly: GUI peripheral arguments are supplied by
the symbol-aware source bootstrap. The buffer source is only a pixel-check aid.

Both modes compile main.c with RENDER=0/1 and use the same frozen v4 search,
parser, physical replay, tables and startup. Only the display-enabled build adds
drawing, dimension checks, frame diagnostic output and delay/replay animation.
The renderer-off CLI executes the ELF directly, without extra bootstrap instructions.

## Evidence

`../results/final/equivalence.json` confirms .text/.rodata/.data equality and
section layout equality with existing v4 ELFs for solved, one-move, three-move
and reference distance-11 inputs. Preprocessed RENDER=0 runtime tokens are also
identical to the frozen original. Same compiler flags and source ordering are
used, so this unification preserves the measured v4 runtime rather than changing
its algorithm or adding unmeasured wrapper overhead.

`check_equivalence.py` reproduces the checks when the four original v4 ELFs
exist in output/assembly_search. On a fresh checkout first build those four
inputs with the assembly_practice Makefile. Do not regenerate the original
outputs during an unrelated active measurement run.

`check_led.py` validates actual Ripes buffer pixels and optimal paths. The new
integration passed 17 frames of 875 pixels each across four runs; its renderer
off text/static sizes are 1784/49252 bytes, renderer-on payload sizes 2668/49452.
GUI source includes a bootstrap/padding before the payload; payload .text size
must not be mistaken for total GUI source executable footprint.

The full 2644-case gate remains the frozen-v4 run. Completion is not asserted by
this README. Original GUI screenshots describe the identical renderer-off v4
program and the older display integration; new buffer tests validate the updated
renderer integration. No new GUI animation timing observation is claimed.
