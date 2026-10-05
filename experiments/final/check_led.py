"""AI-authored pixel-by-pixel oracle for actual Ripes assembly execution."""
from pathlib import Path
import subprocess,os,re,json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'led'))
import geometry
root=Path(__file__).resolve().parents[2]
out=root/'experiments/results/final/led';out.mkdir(parents=True,exist_ok=True)
ripes=Path.home()/'Ripes/build/Ripes.app/Contents/MacOS/Ripes'
results=[]
cases=[('12345671111111','RV32_ISS'),('25314672313211','RV32_ISS'),('25314672313211','RV32_5S'),('21345671111111','RV32_ISS')]
for state,proc in cases:
 subprocess.run(['python3',str(root/'experiments/final/build.py'),state,'--render','1'],check=True,capture_output=True)
 source=root/'output/final'/(state+'-render-buffer.s')
 run=subprocess.run([str(ripes),'--mode','cli','--src',str(source),'-t','asm','--proc',proc,'--iret','--cycles','--timeout','120000'],env=dict(os.environ,QT_QPA_PLATFORM='offscreen'),text=True,capture_output=True,timeout=180)
 raw=run.stdout+run.stderr
 (out/(state+'-'+proc+'.txt')).write_text(raw)
 assert run.returncode==0 and 'Program exited with code: 0' in raw and 'replay: PASS' in raw,raw[-1000:]
 moves=re.search(r'^path:([^\n]*)',raw,re.M)[1].split()
 length=int(re.search(r'^length: (\d+)',raw,re.M)[1]);assert len(moves)==length
 # Exact BFS optimality oracle, separate from target replay.
 oracle=subprocess.run([str(root/'output/verify_path'),state,' '.join(moves)],capture_output=True,text=True)
 (out/(state+'-'+proc+'-oracle.txt')).write_text(oracle.stdout+oracle.stderr)
 assert oracle.returncode==0
 p=[int(x)-1 for x in state[:7]];o=[int(x)-1 for x in state[7:]]
 expected=[geometry.frame(p,o)]
 for move in moves:
  for _ in range(2 if move.endswith('2') else 3 if move.endswith("'") else 1):
   p,o=geometry.turn(p,o,{'R':0,'B':1,'D':2}[move[0]])
  expected.append(geometry.frame(p,o))
 actual=[[int(x) for x in line.split()] for line in re.findall(r'^pixels:(.*)$',raw,re.M)]
 assert actual==expected, 'Full framebuffer mismatch'
 assert p==list(range(7)) and o==[0]*7
 result=dict(input=state,processor=proc,frames=len(actual),pixels_per_frame=875,exact_pixel_comparison='PASS',optimality='PASS',instructions=int(re.search(r'^===== instructions retired\s*\n(\d+)',raw,re.M)[1]))
 results.append(result);print(json.dumps(result),flush=True)
 (out/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
 # Independent view artifact for reviewing layout, not a Ripes GUI screenshot.
 if state=='25314672313211':
  rects=[]
  for y in range(25):
   for x in range(35):
    rects.append(f'<rect x="{x*12}" y="{y*12}" width="11" height="11" fill="#{expected[0][y*35+x]:06x}"/>')
  (out/'initial-frame.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="420" height="300" viewBox="0 0 420 300"><rect width="420" height="300" fill="#222"/>'+''.join(rects)+'</svg>')
