"""AI-authored geometry oracle/table generator for the teaching renderer."""
from itertools import product
# Positions 0..7, front viewed from outside: x right, y up, z front.
POS=[(-1,1,1),(1,1,1),(1,-1,1),(-1,-1,1),(1,1,-1),(1,-1,-1),(-1,-1,-1),(-1,1,-1)]
NORMAL=[(0,1,0),(-1,0,0),(0,0,1),(1,0,0),(0,0,-1),(0,-1,0)] # U L F R B D
RGB=[0xffffff,0xff8000,0x00cc00,0xff0000,0x0044ff,0xffff00]
SRC=[[0,2,5,3,1,4,6,7],[0,1,2,3,5,6,7,4],[0,1,3,6,4,2,5,7]]
TWIST=[[0,1,2,0,2,1,0,0],[0,0,0,0,1,2,1,2],[0,0,0,0,0,0,0,0]]
def rot(v,axis,sign):
 x,y,z=v
 if axis==0: return x,-sign*z,sign*y
 if axis==1: return sign*z,y,-sign*x
 return -sign*y,sign*x,z
AXES=[0,2,1]
SIGNS=[]
for f,axis in enumerate(AXES):
 candidates=[sgn for sgn in (-1,1) if all(rot(POS[SRC[f][d]],axis,sgn)==POS[d] for d in range(8) if SRC[f][d]!=d)]
 assert len(candidates)==1
 SIGNS.append(candidates[0])
# Choose cyclic local sticker order consistent with the existing twist convention.
for flips in product((0,1),repeat=8):
 slots=[]
 for (x,y,z),flip in zip(POS,flips):
  sides=[NORMAL.index((x,0,0)),NORMAL.index((0,0,z))]
  if flip: sides.reverse()
  slots.append([NORMAL.index((0,y,0))]+sides)
 valid=True
 for f in range(3):
  for d,src in enumerate(SRC[f]):
   if d==src: continue
   for k,face in enumerate(slots[src]):
    destface=NORMAL.index(rot(NORMAL[face],AXES[f],SIGNS[f]))
    if slots[d][(k+TWIST[f][d])%3]!=destface: valid=False
 if valid: break
else: raise AssertionError('No orientation-compatible sticker order')
SLOTS=slots
# View each face from outside; right/down axes form its unfolded net.
RIGHT=[(1,0,0),(0,0,1),(1,0,0),(0,0,-1),(-1,0,0),(1,0,0)]
DOWN=[(0,0,1),(0,-1,0),(0,-1,0),(0,-1,0),(0,-1,0),(0,0,-1)]
ORIGIN=[(9,0),(0,7),(9,7),(18,7),(27,7),(9,14)]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
CELLS=[]
for face,normal in enumerate(NORMAL):
 for row in range(2):
  for col in range(2):
   corners=[i for i,v in enumerate(POS) if dot(v,normal)==1 and dot(v,RIGHT[face])==2*col-1 and dot(v,DOWN[face])==2*row-1]
   assert len(corners)==1
   corner=corners[0];x=ORIGIN[face][0]+4*col;y=ORIGIN[face][1]+3*row
   CELLS.append((corner,SLOTS[corner].index(face),x,y))
def state_colors(p,o):
 return [SLOTS[0 if c==0 else p[c-1]+1][(slot-(0 if c==0 else o[c-1]))%3] for c,slot,x,y in CELLS]
def frame(p,o):
 pixels=[0]*875
 for (_,_,x,y),color in zip(CELLS,state_colors(p,o)):
  for dy in range(3):
   for dx in range(4): pixels[(y+dy)*35+x+dx]=RGB[color]
 return pixels
def turn(p,o,face):
 pp=[0]+[x+1 for x in p];oo=[0]+o
 return [pp[SRC[face][d]]-1 for d in range(1,8)],[(oo[SRC[face][d]]+TWIST[face][d])%3 for d in range(1,8)]
def geometric_turn(stickers,face):
 result={}
 for (corner,normal),color in stickers.items():
  if dot(POS[corner],NORMAL[[3,4,5][face]])==1:
   corner=POS.index(rot(POS[corner],AXES[face],SIGNS[face]));normal=rot(normal,AXES[face],SIGNS[face])
  result[corner,normal]=color
 return result
if __name__=='__main__':
 from pathlib import Path
 import random
 p=list(range(7));o=[0]*7
 stickers={(c,NORMAL[face]):face for c in range(8) for face in SLOTS[c]}
 rng=random.Random(2026)
 for step in range(1000):
  f=rng.randrange(3);p,o=turn(p,o,f);stickers=geometric_turn(stickers,f)
  actual=state_colors(p,o)
  assert actual==[stickers[c,NORMAL[SLOTS[c][slot]]] for c,slot,x,y in CELLS]
 text='/* AI-generated tables; independently checked against 3D sticker rotations. */\n.section .rodata\n.balign 4\nled_rgb:\n.word '+','.join(hex(c) for c in RGB)+'\nled_cubie_colors:\n.byte '+','.join(str(c) for row in SLOTS for c in row)+'\nled_cells:\n.byte '+','.join(str(v) for row in CELLS for v in row)+'\n'
 Path(__file__).with_name('geometry.inc').write_text(text)
 print('1000 seeded geometric quarter-turn comparisons passed; 24 facelets, 288 lit pixels.')
