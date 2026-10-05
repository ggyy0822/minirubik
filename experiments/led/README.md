# LED teaching implementation: actual solution replay

Status: pixel-buffer validation passes. User screenshots now confirm the live
GUI peripheral solved net and successful one-move execution; intermediate animation
timing is not independently established by static screenshots. This module is AI-authored reference/integration work, distinct
from the student-completed search fragments. Do not represent it as entirely
student-authored. The assignment's remaining handwritten-code/authorship work
and oral explanation are still outstanding.

## Open the one-move demonstration

1. Open Ripes. Select the 32-bit ISA simulator (RV32_ISS) without extensions.
2. In I/O, add LED Matrix (first instance, LED_MATRIX_0). Width=35, Height=25.
   The panel places Height above Width; do not swap them.
3. Open output/led/25314672313211-render-gui.s as assembly source, NOT its ELF.
4. Assemble/reset and run. Inspect the I/O tab. Expected: initial net, then R',
   then six uniform faces. Console shows length: 1, path: R', replay: PASS.
5. An initial delay separates frames. FRAME_DELAY in the generated file controls
   an approximate simulation delay; it is not a calibrated real-time timer.
   Use ISS for animation; one million delay iterations will be slow on a pipeline.

Layout (faces viewed from outside):

        U
    L   F   R   B
        D

U white, L orange, F green, R red, B blue, D yellow. Each facelet is 4x3 pixels.
Each face is 8x6, separated from adjacent face slots by one black column/row.
Origins: U=(9,0), L=(0,7), F=(9,7), R=(18,7), B=(27,7), D=(9,14).
Occupied bounding rectangle: 35x20; last five rows remain black. All 24 stickers
have fixed physical geometry; orientation changes their colors according to the
actual cubie state. The fixed corner is included in rendering.

## Build / validate from repository root

```sh
python3 experiments/led/geometry.py
python3 experiments/led/build.py 25314672313211 --render 1
python3 experiments/led/build.py 21345671111111 --render 1
python3 experiments/led/build.py 25314672313211 --render 0
python3 experiments/led/check.py
python3 experiments/rv32_baseline/audit.py --directory output/led
```

--render 1 emits GUI and diagnostic-buffer source files; --render 0 emits a CLI
source with drawing/replay animation compiled out. Rendering is selected via C
preprocessing, because the pinned Ripes assembler rejects .if and .space. It also
uses .align in BYTES (4096 here), unlike GNU assembly's power-of-two convention.
These differences were tested directly. The GUI bootstrap obtains the peripheral
base/width/height from LED_MATRIX_0_* assembler symbols, never a literal MMIO
address. It jumps to a linked RV32I payload at 0x1000. The source adapter uses
real decoded RV32I instructions and labeled branch targets, and translates GNU
jalr rd,offset(rs) into the syntax accepted by this Ripes revision. Default
assembler text=0, data=0x10000000 layout is required. Original readable sources,
not the generated numeric labels/table listing, are the code to study.

All variants use the unchanged v4 student search. Existing baseline measurements
and original full-gate runner have not been replaced. The LED-integrated RENDER=0
runtime is a separate build with slightly different wrapper instructions, so its
counts must not be silently substituted for old baseline counts. A full gate on
the eventual final submission build is still required.

## What was checked

- 1000 deterministic 3D quarter-turn sequences verify sticker mapping against
  rotation of physical corner coordinates and face normals.
- Actual assembly renderer output is dumped from a diagnostic RAM framebuffer
  (0x20000000; 3500 bytes) and compared pixel-for-pixel, including black areas.
- Solved input: 1 frame; one-move input: 2 frames on ISS and 5S; reference eleven-
  move input: 12 frames on ISS. All 875 pixels of every frame match.
- Every tested solution passes target physical replay and separate native exact-
  distance optimality checking. Frame states are updated from target_search's
  actual path, never a prerecorded animation.
- RENDER=0 test prints the same one-move solution with no frame/pixel output.
- RV32I-only opcode/symbol checks pass. Rendered payload .text=2652 bytes and
  .rodata+.bss=49416 bytes. Ripes source adds 4096 bytes of bootstrap/padding to
  text; the RAM-only diagnostic framebuffer adds 3500 guest bytes outside ELF
  sections. GUI uses peripheral MMIO instead. All are below the static-data cap.

main.c validates the full path before display, then re-parses the initial state.
It calls target_replay with one move to advance each frame. That function mutates
state even when its return is false (not yet solved); this intentional use is
separate from the prior full-path validity check. led_draw in render.S owns the
actual pixel stores and uses shifts/adds instead of multiply/divide. No heap or
recursive search is introduced. GUI and diagnostic buffer share the same payload;
buffer mode sets delay=0, enabling complete pixel dumps. GUI uses nonzero delay.

Raw reports: ../results/led/. initial-frame.svg is a host-generated rendering of
the expected pixel buffer, NOT a screenshot of the Ripes GUI.
