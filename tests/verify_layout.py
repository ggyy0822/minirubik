"""Compare current target with the independently recorded validated-v5 fixture."""
import hashlib,json,re,subprocess,tarfile,csv
from common import ROOT,OUT,CROSS,build
fixture=json.loads((ROOT/'tests/cases/v5-layout.json').read_text())
for name,digest in fixture['source_sha256'].items():
 assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
rows=[]
for expected in fixture['executables']:
 state,render=expected['input'],expected['render'];elf=build(state,'assembly',render)
 hashes={}
 for section,digest in expected['sections'].items():
  dest=OUT/('layout'+section+'.bin')
  subprocess.run([CROSS+'objcopy','-O','binary','--only-section='+section,str(elf),str(dest)],check=True)
  hashes[section]=hashlib.sha256(dest.read_bytes()).hexdigest()
  assert hashes[section]==digest,(state,render,section)
 layout=re.findall(r'^(\.\S+)\s+(\d+)\s+(\d+)',elf.with_suffix('.sections.txt').read_text(),re.M)
 assert [list(x) for x in layout]==fixture['section_layouts'][state+str(render)]
 rows.append(dict(input=state,render=render,sections=hashes,result='BYTE_IDENTICAL'))
raw=ROOT/'results/raw';summary=json.loads((raw/'hard-summary.json').read_text())
assert summary['passed']==2644 and summary['failed']==0 and summary['complete']
manifest=list(csv.DictReader((ROOT/'tests/cases/distance11.csv').open()))
assert len(manifest)==2644 and len({x['state'] for x in manifest})==2644
with tarfile.open(raw/'raw-evidence.tar.gz','r:gz') as t:
 for case in manifest:
  r=json.load(t.extractfile('c0deaa63ee983de7/'+case['state']+'.json'))
  assert r['input']==case['state'] and r['gate_pass'] and r['length']==11 and r['instructions']<=50000000
  assert r['target_replay']==r['host_optimality']=='PASS'
(ROOT/'results/layout-equivalence.json').write_text(json.dumps(dict(source_sha256=fixture['source_sha256'],executables=rows,archived_hard_cases_verified=2644,fixture='tests/cases/v5-layout.json'),indent=2)+'\n')
print('PASS: validated source hashes, eight ELF layouts/sections, 2644 archived cases.')
