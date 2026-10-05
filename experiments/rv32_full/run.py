"""Build and measure one educational GCC baseline input in Ripes."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser()
parser.set_defaults(implementation="full-assembly-v5")
parser.add_argument("state", help="14-character cube input")
parser.add_argument("--processor", choices=["RV32_ISS", "RV32_5S"], default="RV32_ISS")
parser.add_argument("--timeout-ms", type=int, default=180000)
parser.add_argument("--ripes", type=Path, default=Path.home() / "Ripes/build/Ripes.app/Contents/MacOS/Ripes")
args = parser.parse_args()
if not re.fullmatch(r"[1-7]{7}[1-3]{7}", args.state):
    parser.error("expected seven cubie digits and seven orientation digits")
root = Path(__file__).resolve().parents[2]
out = root / 'output/rv32_full'
out.mkdir(parents=True, exist_ok=True)
build=subprocess.run(['python3',str(root/'experiments/rv32_full/build.py'),args.state,'--render','0'],capture_output=True,text=True)
(out/(args.state+'-build.txt')).write_text(build.stdout+build.stderr)
build.check_returncode()
elf=out/(args.state+'-measure.elf')
prefix = out / (args.state + "-" + args.processor)
env = dict(os.environ, QT_QPA_PLATFORM="offscreen")
command = [str(args.ripes), "--mode", "cli", "--src", str(elf), "-t", "elf",
           "--proc", args.processor, "--iret", "--cycles", "--exectime", "--runinfo",
           "--timeout", str(args.timeout_ms)]
run = subprocess.run(command, env=env, capture_output=True, text=True,
                     timeout=args.timeout_ms / 1000 + 30)
raw = run.stdout + run.stderr
prefix.with_suffix(".txt").write_text(raw)
if run.returncode or "Program exited with code: 0" not in raw or "replay: PASS" not in raw:
    raise SystemExit("Ripes execution failed; inspect " + str(prefix.with_suffix('.txt')))
path = re.search(r"^path:([^\n]*)", raw, re.M).group(1).strip()
checker = root / "output/verify_path"
subprocess.run(["cc", "-O3", "-std=c99", str(root / "tests/verify_path.c"), "-o", str(checker)], check=True)
verified = subprocess.run([str(checker), args.state, path], capture_output=True, text=True)
prefix.with_name(prefix.name + "-oracle.txt").write_text(verified.stdout + verified.stderr)
verified.check_returncode()
def number(label):
    return int(re.search(r"^===== " + re.escape(label) + r"\s*\n(\d+)", raw, re.M).group(1))
sizes = {}
for line in elf.with_suffix('.sections.txt').read_text().splitlines():
    match = re.match(r'(\.\S+)\s+(\d+)\s+', line)
    if match:
        sizes[match[1]] = int(match[2])
result = dict(implementation=args.implementation, input=args.state, processor=args.processor,
              instructions=number("instructions retired"), cycles=number("cycles"),
              model_ms=number("wall-clock model execution time (ms)"),
              text_bytes=sizes['.text'],
              static_data_bytes=sum(sizes.get(s, 0) for s in ('.data', '.bss', '.rodata')),
              length=int(re.search(r'^length: (\d+)', raw, re.M).group(1)),
              path=path, target_replay="PASS", host_optimality="PASS",
              qt_backend="offscreen")
prefix.with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
