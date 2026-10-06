"""Prove relocation preserves v5 inputs and executable sections; check archived gate."""
import hashlib,json,pathlib,subprocess,tarfile,csv
from common import ROOT,OUT,CROSS,build
raw=ROOT/'results/raw';provenance=json.loads((raw/'hard-provenance.json').read_text())
# Canonical source copies must exactly match the fully measured source bytes.
pairs={}
for p in (ROOT/'asm/src').iterdir():
 original=ROOT/'experiments'/('led' if p.name in ['render.S','geometry.inc'] else 'rv32_full')/p.name
 assert p.read_bytes()==original.read_bytes(),p
 if str(original.relative_to(ROOT)) in provenance:
  assert hashlib.sha256(p.read_bytes()).hexdigest()==provenance[str(original.relative_to(ROOT))]
 pairs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in (ROOT/'baseline').iterdir():assert p.read_bytes()==(ROOT/'experiments/rv32_baseline'/p.name).read_bytes(),p
rows=[]
for state in ['12345671111111','25314672313211','23745612123332','21345671111111']:
 for render in [False,True]:
  elf=build(state,'assembly',render)
  subprocess.run(['python3',str(ROOT/'experiments/rv32_full/build.py'),state,'--render',str(int(render))],check=True,stdout=subprocess.DEVNULL)
  old=ROOT/'output/rv32_full'/(state+('-render' if render else '-measure')+'.elf')
  hashes={}
  for section in ['.text','.rodata','.data']:
   blobs=[]
   for i,file in enumerate([old,elf]):
    dest=OUT/('layout-'+str(i)+'.bin')
    subprocess.run([CROSS+'objcopy','-O','binary','--only-section='+section,str(file),str(dest)],check=True)
    blobs.append(dest.read_bytes())
   assert blobs[0]==blobs[1],(state,render,section)
   hashes[section]=hashlib.sha256(blobs[1]).hexdigest()
  # Sizes and addresses include BSS: equal bytes alone would not establish layout.
  import re
  get=lambda e:re.findall(r'^(\.\S+)\s+(\d+)\s+(\d+)',e.with_suffix('.sections.txt').read_text(),re.M)
  assert get(old)==get(elf),(state,render,'section layout')
  rows.append(dict(input=state,render=render,sections=hashes,result='BYTE_IDENTICAL'))
summary=json.loads((raw/'hard-summary.json').read_text());assert summary['passed']==2644 and summary['failed']==0 and summary['complete']
manifest=list(csv.DictReader((ROOT/'tests/cases/distance11.csv').open()))
with tarfile.open(raw/'raw-evidence.tar.gz','r:gz') as t:
 for case in manifest:
  r=json.load(t.extractfile('c0deaa63ee983de7/'+case['state']+'.json'))
  assert r['input']==case['state'] and r['gate_pass'] and r['length']==11 and r['instructions']<=50000000
  assert r['target_replay']==r['host_optimality']=='PASS'
(ROOT/'results/layout-equivalence.json').write_text(json.dumps(dict(source_sha256=pairs,executables=rows,archived_hard_cases_verified=2644),indent=2)+'\n')
print('PASS: canonical sources, eight ELF layouts/sections, 2644 archived case records.')
