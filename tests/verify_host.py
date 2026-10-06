"""H1/H2 full checks; H3 full by default, --quick samples it; H4 not applicable."""
import argparse,os,subprocess,json
from common import ROOT,OUT,tables
p=argparse.ArgumentParser();p.add_argument('--quick',action='store_true');a=p.parse_args()
ctable=tables();exe=OUT/'verify_host'
subprocess.run([os.environ.get('CC','cc'),'-O2','-std=c99','-Wno-unused-function',str(ROOT/'tests/verify_native.c'),str(ROOT/'baseline/search.c'),str(ROOT/'baseline/state.c'),str(ctable),'-o',str(exe)],check=True)
r=subprocess.run([str(exe),'--check' if a.quick else '--all'],capture_output=True,text=True)
out=ROOT/'results/raw/current';out.mkdir(parents=True,exist_ok=True)
(out/('host-quick.txt' if a.quick else 'host-full.txt')).write_text(r.stdout+r.stderr)
print(r.stdout);r.check_returncode()
print('H4: NOT APPLICABLE — unpacked byte/halfword tables; no packed decoder.')
