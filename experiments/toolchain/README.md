# RV32I toolchain smoke test

AI-generated infrastructure test, not the student's handwritten solver.

Installed Homebrew's official `riscv64-elf-gcc` formula (GCC 16.2.0) and its
dependencies. Formula source: https://formulae.brew.sh/formula/riscv64-elf-gcc
Executable prefix is `riscv64-elf-`, and `-dumpmachine` reports `riscv64-elf`.
This is not the literal `riscv64-unknown-elf-gcc` command named in the assignment;
record the actual compiler/version rather than creating a misleading alias.
The compiler provides an `rv32i/ilp32` multilib configuration.

From the repository root:

```sh
make -C experiments/toolchain check
```

The test compiles C with `-O2 -march=rv32i -mabi=ilp32`, supplies a minimal
startup and linker script, and runs the same ELF on Ripes ISS and RV32_5S.
Both must print 12 and exit with status 0. The C object uses a volatile value
so the compiler actually emits the memory reads and write.

The recipe sets `QT_QPA_PLATFORM=offscreen` only for these CLI processes.
The default Cocoa Qt backend aborted inside the agent sandbox while connecting
to macOS services; offscreen execution succeeded without changing system or
application preferences. Earlier user-run measurements used the normal backend;
do not silently combine those wall times with offscreen results.

Outputs are under `output/toolchain/`: ELF, linker map, disassembly, ELF
attributes, section sizes, compiler identity, and the two execution logs.
The smoke ELF is ELF32 with `Tag_RISCV_arch: rv32i2p1`, `.text` 84 bytes,
`.data` 4 bytes, and `.bss` 4096 bytes (the reserved stack). No standard library
is linked; `nm -u` reports no undefined symbols. Its decoded instructions are
base RV32I instructions. The 16-byte data-to-stack alignment gap is distinct
from the section payload sizes.

Ripes path defaults to `$(HOME)/Ripes/build/Ripes.app/Contents/MacOS/Ripes`.
Override using `make ... RIPES=/absolute/path/to/Ripes` when necessary.
The Ripes checkout was inspected at commit
`5b8a616edcb6f0a2ddb07e78951348b72497f1e1`; only untracked probe/log files were
reported. This does not independently prove which sources built the binary.

Passing this smoke test verifies toolchain plumbing only. It does not fulfill
solver T5-T7, prove solver static-data compliance, or provide the required
C-versus-handwritten-assembly performance comparison.

Recorded smoke reports: ISS 19 retired instructions / 19 cycles; RV32_5S
18 retired instructions / 31 cycles. Both print 12 and exit successfully.
The difference in terminal instruction accounting has not been diagnosed;
do not describe these reports as identical instruction counts. The short
offscreen runs report 0 ms, so they cannot be used to estimate simulation rate.
Raw reports and the executable hash are preserved in `../results/toolchain/`.
