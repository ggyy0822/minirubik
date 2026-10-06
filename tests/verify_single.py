"""Execute the committed single-file Ripes program using a RAM LED substitute."""
import json,re,os,sys,subprocess
from common import ROOT,OUT,RIPES
import geometry
source=(ROOT/'asm/minirubik.s').read_text()
state=re.search(r'^# Input: (\d{14})',source,re.M)[1]
# Substitute only the three peripheral symbols and delay for headless testing.
for a,b in [('LED_MATRIX_0_BASE','0x20000000'),('LED_MATRIX_0_WIDTH','35'),('LED_MATRIX_0_HEIGHT','25'),('.equ FRAME_DELAY, 1000000','.equ FRAME_DELAY, 0')]:source=source.replace(a,b)
OUT.mkdir(parents=True,exist_ok=True);file=OUT/'single-file-buffer.s';file.write_text(source)
r=subprocess.run([RIPES,'--mode','cli','--src',str(file),'-t','asm','--proc','RV32_ISS','--iret','--timeout','180000'],env=dict(os.environ,QT_QPA_PLATFORM='offscreen'),capture_output=True,text=True,timeout=210)
raw=r.stdout+r.stderr;dest=ROOT/'results/raw/current';dest.mkdir(parents=True,exist_ok=True);(dest/'single-file.txt').write_text(raw)
assert r.returncode==0 and 'Program exited with code: 0' in raw and 'replay: PASS' in raw,raw[-1000:]
moves=re.search(r'^path:([^\n]*)',raw,re.M)[1].split()
p=[int(x)-1 for x in state[:7]];o=[int(x)-1 for x in state[7:]];expected=[geometry.frame(p,o)]
for move in moves:
 for _ in range(2 if move.endswith('2') else 3 if move.endswith("'") else 1):p,o=geometry.turn(p,o,{'R':0,'B':1,'D':2}[move[0]])
 expected.append(geometry.frame(p,o))
actual=[[int(x) for x in s.split()] for s in re.findall(r'^pixels:(.*)$',raw,re.M)]
assert actual==expected and p==list(range(7)) and o==[0]*7
result=dict(input=state,frames=len(actual),pixels_per_frame=875,result='PASS',scope='single-file payload with peripheral symbols substituted for headless execution')
(dest/'single-file.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
