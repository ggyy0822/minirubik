"""Rebuild and measure matching GCC and assembly algorithms on Ripes ISS."""
import argparse,csv,json
from common import ROOT,measure
p=argparse.ArgumentParser();p.add_argument('--input');a=p.parse_args()
cases=[a.input] if a.input else [r['input'] for r in json.loads((ROOT/'tests/cases/smoke.json').read_text())]
rows=[]
for state in cases:
 for impl in ['gcc','assembly']:
  r=measure(state,impl);rows.append(r);print(state,impl,r['instructions'],r['text_bytes'],flush=True)
name='comparison.csv' if not a.input else 'comparison-selected.csv'
with (ROOT/'results'/name).open('w') as f:
 w=csv.DictWriter(f,fieldnames=['input','implementation','processor','length','instructions','cycles','text_bytes','static_data_bytes'],extrasaction='ignore');w.writeheader();w.writerows(rows)
