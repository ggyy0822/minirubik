"""Audit emitted GCC baseline ELFs; no instruction-count inference."""
import argparse
import json
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--directory", type=Path, default=root / "output/rv32_baseline")
out = parser.parse_args().directory
allowed = set("lui auipc jal jalr beq bne blt bge bltu bgeu lb lh lw lbu lhu sb sh sw addi slti sltiu xori ori andi slli srli srai add sub sll slt sltu xor srl sra or and fence ecall ebreak".split())
rows = []
for elf in sorted(out.glob("*.elf")):
    disasm = subprocess.check_output(["riscv64-elf-objdump", "-d", "-M", "no-aliases", str(elf)], text=True)
    ops = []
    for line in disasm.splitlines():
        match = re.match(r"\s*[0-9a-f]+:\s+([0-9a-f]+)\s+(\S+)", line)
        if match:
            assert len(match[1]) == 8, "non-32-bit instruction: " + line
            ops.append(match[2])
    assert ops and set(ops) <= allowed, set(ops) - allowed
    symbols = subprocess.check_output(["riscv64-elf-nm", str(elf)], text=True)
    assert not re.search(r"__(?:mul|div|mod|udiv|umod)", symbols)
    undefined = subprocess.check_output(["riscv64-elf-nm", "-u", str(elf)], text=True)
    assert not undefined.strip(), undefined
    sizes = {}
    size_report = subprocess.check_output(["riscv64-elf-size", "-A", str(elf)], text=True)
    for line in size_report.splitlines():
        match = re.match(r"(\.\S+)\s+(\d+)\s+", line)
        if match:
            sizes[match[1]] = int(match[2])
    static = sum(sizes.get(section, 0) for section in (".data", ".bss", ".rodata"))
    assert static <= 131072
    rows.append(dict(input=elf.stem, text_bytes=sizes[".text"], static_data_bytes=static,
                     rv32i_instruction_audit="PASS", undefined_symbols=0))
assert rows, "no ELF files found; build first"
(out / "audit.json").write_text(json.dumps(rows, indent=2) + "\n")
print(json.dumps(rows, indent=2))
