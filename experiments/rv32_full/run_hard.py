"""AI-authored resumable Ripes gate. Host work ranking is not target-count proof."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

root = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--limit', type=int, help='test top N host-work-ranked cases')
group.add_argument('--all', action='store_true', help='test all 2644 cases; may take hours')
args = parser.parse_args()
if args.limit is not None and not 1 <= args.limit <= 2644:
    parser.error('--limit must be between 1 and 2644')
manifest = root/'experiments/validation/hard-manifest.csv'
rows = list(csv.DictReader(manifest.open()))
assert len(rows) == 2644 and len({r['state'] for r in rows}) == 2644
ripes = Path.home() / 'Ripes/build/Ripes.app/Contents/MacOS/Ripes'
files = list((root/'experiments/rv32_full').glob('*.inc')) + list((root/'experiments/rv32_full').glob('*.S'))
files += [root/'experiments/rv32_full'/n for n in ('build.py','run.py')]
files += [root/'experiments/toolchain/ripes.ld',root/'output/rv32_baseline/tables.c',root/'tests/verify_path.c',root/'solver.c',manifest,Path(__file__)]
versions = {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
versions['ripes_binary_sha256'] = hashlib.sha256(ripes.read_bytes()).hexdigest()
versions['compiler_version'] = subprocess.check_output(['riscv64-elf-gcc','--version'],text=True)
versions['platform'] = 'RV32_ISS; QT_QPA_PLATFORM=offscreen; renderer absent'
fingerprint = hashlib.sha256(json.dumps(versions,sort_keys=True).encode()).hexdigest()
out=root/'experiments/results/rv32_full/hard-target'/fingerprint[:16]
out.mkdir(parents=True,exist_ok=True)
(out/'provenance.json').write_text(json.dumps(versions,indent=2)+'\n')
print('Reports:',out,flush=True)

def save_summary():
    results=[json.loads((out/(row['state']+'.json')).read_text())
             for row in rows if (out/(row['state']+'.json')).exists()]
    passed=[r for r in results if r.get('gate_pass')]
    summary=dict(total_required=2644,passed=len(passed),failed=len(results)-len(passed),
                 complete=len(passed)==2644 and len(results)==2644,
                 maximum_measured_instructions=max((r['instructions'] for r in passed),default=None),
                 fingerprint=fingerprint)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary

for index,row in enumerate(rows[:args.limit] if args.limit else rows,1):
    state=row['state']; report=out/(state+'.json')
    if report.exists() and json.loads(report.read_text()).get('gate_pass'):
        print(f'{index}: {state} cached PASS',flush=True)
        continue
    start=time.monotonic()
    command=['python3',str(root/'experiments/rv32_full/run.py'),state,'--timeout-ms','180000']
    try:
        run=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=240)
        (out/(state+'-driver.txt')).write_text(run.stdout+run.stderr)
        if run.returncode: raise RuntimeError('runner failed; see driver log')
        result=json.loads((root/'output/rv32_full'/(state+'-RV32_ISS.json')).read_text())
        result['gate_pass']=(result['input']==state and result['processor']=='RV32_ISS' and
            result['length']==int(row['expected_length']) and result['instructions']<=50000000 and
            result['target_replay']==result['host_optimality']=='PASS')
        for suffix in ('.txt','-oracle.txt'):
            p=root/'output/rv32_full'/(state+'-RV32_ISS'+suffix)
            shutil.copy2(p,out/p.name)
    except Exception as error:
        result=dict(input=state,gate_pass=False,error=str(error))
    result['wall_seconds']=round(time.monotonic()-start,3)
    report.write_text(json.dumps(result,indent=2)+'\n')
    summary=save_summary()
    print(f"{index}: {state}: {'PASS' if result['gate_pass'] else 'FAIL'}; instructions={result.get('instructions')}; coverage={summary['passed']}/2644",flush=True)
    if not result['gate_pass']: raise SystemExit(1)
print(json.dumps(save_summary(),indent=2),flush=True)
