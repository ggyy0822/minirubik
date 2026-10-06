"""T5 replay + exact oracle, T6 reference-11, T7 ISS/five-stage cases.
Default runs the complete representative T5–T7 suite. --quick excludes the
11-move case and therefore does not claim full T6/T7 in that invocation.
"""
import argparse,json,csv,hashlib,tarfile
from common import ROOT,measure
p=argparse.ArgumentParser();p.add_argument('--quick',action='store_true');p.add_argument('--all-hard',action='store_true');a=p.parse_args()
cases=json.loads((ROOT/'tests/cases/smoke.json').read_text())[:3 if a.quick else 4]
rows=[]
for proc in ['RV32_ISS','RV32_5S']:
 for case in cases:
  r=measure(case['input'],'assembly',proc);assert r['length']==case['length'];rows.append(r)
  print(case['input'],proc,'PASS',r['instructions'],flush=True)
(ROOT/'results/raw/current'/('target-quick.json' if a.quick else 'target-full.json')).write_text(json.dumps(rows,indent=2)+'\n')
if a.all_hard:
 manifest=list(csv.DictReader((ROOT/'tests/cases/distance11.csv').open()));hard=[]
 for i,case in enumerate(manifest,1):
  r=measure(case['state'],'assembly');assert r['length']==11 and r['instructions']<=50000000;hard.append(r)
  (ROOT/'results/raw/current/hard-rerun.json').write_text(json.dumps(hard,indent=2)+'\n')
  print(i,'/2644 PASS',flush=True)
print('T5 passed; '+('T6/T7 reference-11 omitted (--quick).' if a.quick else 'T6/T7 passed.'))
