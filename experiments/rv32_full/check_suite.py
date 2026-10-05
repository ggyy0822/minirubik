"""Measure five cases and cross-model gates; preserve raw evidence."""
from pathlib import Path
import subprocess,shutil,json,hashlib
root=Path(__file__).resolve().parents[2]
out=root/'experiments/results/rv32_full/measurements';out.mkdir(parents=True,exist_ok=True)
cases=['12345671111111','25314672313211','23745612123332','21345671111111','54721631111111']
rows=[]
for proc in ['RV32_ISS','RV32_5S']:
 for state in (cases if proc=='RV32_ISS' else cases[:4]):
  run=subprocess.run(['python3',str(root/'experiments/rv32_full/run.py'),state,'--processor',proc,'--timeout-ms','900000'],text=True,capture_output=True)
  (out/(state+'-'+proc+'-driver.txt')).write_text(run.stdout+run.stderr)
  assert run.returncode==0,run.stdout+run.stderr
  prefix=state+'-'+proc
  for suffix in ['.json','.txt','-oracle.txt']:
   shutil.copy2(root/'output/rv32_full'/(prefix+suffix),out/(prefix+suffix))
  row=json.loads((out/(prefix+'.json')).read_text());rows.append(row)
  (out/'summary.json').write_text(json.dumps(rows,indent=2)+'\n')
  print(state,proc,row['instructions'],'PASS',flush=True)
files=list((root/'experiments/rv32_full').glob('*.S'))+list((root/'experiments/rv32_full').glob('*.inc'))
(out/'sources.json').write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},indent=2)+'\n')
