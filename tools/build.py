"""Canonical coursework build. Target assembly is never compiled from C."""
import argparse, os, pathlib, re, shutil, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'output/coursework'
CROSS=os.environ.get('CROSS','riscv64-unknown-elf-')
FLAGS=['-O2','-std=c99','-march=rv32i','-mabi=ilp32','-msmall-data-limit=0','-mno-relax','-ffreestanding','-fno-builtin','-fno-stack-protector','-Wall','-Wextra','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,-T,'+str(ROOT/'tools/ripes.ld')]
def execute(args,**kw):return subprocess.run(list(map(str,args)),check=True,**kw)
def tables():
 OUT.mkdir(parents=True,exist_ok=True)
 inputs=[ROOT/'tools/generate_tables.c',ROOT/'tools/host_model.c',ROOT/'solver.c']
 target=OUT/'tables.c'
 if not target.exists() or any(p.stat().st_mtime>target.stat().st_mtime for p in inputs):
  execute([os.environ.get('CC','cc'),'-O2','-std=c99','-Wno-unused-function',inputs[0],'-o',OUT/'generate_tables'])
  data=subprocess.check_output([str(OUT/'generate_tables')],text=True)
  target.write_text(data)
 text=target.read_text();lines=['.section .rodata'];counts={}
 for kind,name,body in re.findall(r'const uint(8|16)_t (rt_\w+)\[[^=]+?=\s*(.*?);',text,re.S):
  values=re.findall(r'\d+',body);counts[name]=len(values)
  lines+=['.balign 2','.globl '+name,name+':']
  lines += [('.byte ' if kind=='8' else '.half ')+','.join(values[i:i+16]) for i in range(0,len(values),16)]
 assert counts==dict(rt_perm=15120,rt_orient=2187,rt_pd=5040,rt_od=729),counts
 dest=OUT/'tables.S';data='\n'.join(lines)+'\n'
 if not dest.exists() or dest.read_text()!=data:dest.write_text(data)
 return target

def build(state,implementation='assembly',render=False):
 if not re.fullmatch(r'[1-7]{7}[1-3]{7}',state):raise ValueError('Expected seven cubie digits and seven orientation digits')
 ctable=tables();prefix=OUT/(state+'-'+implementation+('-render' if render else ''))
 if implementation=='assembly':
  sources=[ROOT/'asm/src'/n for n in ['main.S','search.S','heuristic.S','state.S']]+[OUT/'tables.S']
  if render:sources+=[ROOT/'asm/src/render.S']
 else:
  if render:raise ValueError('GCC measurements use rendering off')
  sources=[ROOT/'baseline'/n for n in ['search.c','state.c','main.c','start.S']]+[ctable]
 elf=prefix.with_suffix('.elf')
 execute([CROSS+'gcc',*FLAGS,'-DRENDER='+str(int(render)),'-DCUBE_INPUT="'+state+'"',*sources,'-o',elf])
 for suffix,args in [('sections.txt',['size','-A']),('disasm',['objdump','-d','-M','no-aliases'])]:
  prefix.with_suffix('.'+suffix).write_text(subprocess.check_output([CROSS+args[0],*args[1:],str(elf)],text=True))
 return elf

def export_single(elf,state):
 """Ripes-compatible symbol-aware loader of the handwritten linked payload."""
 report=elf.with_suffix('.sections.txt').read_text()
 sections={a:(int(b),int(c)) for a,b,c in re.findall(r'^(\.\S+)\s+(\d+)\s+(\d+)',report,re.M)}
 lines=[]
 for line in elf.with_suffix('.disasm').read_text().splitlines():
  m=re.match(r'\s*([0-9a-f]+):\s+[0-9a-f]{8}\s+(\S+)\s*(.*)',line)
  if not m:continue
  address,op,args=m.groups();args=args.split('#')[0].strip()
  if op=='jalr':args=re.sub(r'([^,]+),(-?\d+)\(([^)]+)\)',r'\1,\3,\2',args)
  args=re.sub(r'([0-9a-f]+) <[^>]+>',lambda m:'insn_'+m[1],args)
  lines += ['insn_'+address+':',op+' '+args]
 assert len(lines)//2*4==sections['.text'][0]
 data=bytearray()
 for name in ['.rodata','.data']:
  if name not in sections:continue
  binary=elf.with_suffix(name+'.bin')
  execute([CROSS+'objcopy','-O','binary','--only-section='+name,elf,binary])
  size,addr=sections[name];data.extend(bytes(max(0,addr-0x10000000-len(data))));data.extend(binary.read_bytes())
 header=f'''# Generated from handwritten asm/src; no target C object is linked.
# Input: {state}. Regenerate: make asm INPUT={state}
# Ripes: add LED Matrix 0, Width 35, Height 25; use RV32_ISS.
# Renderer is ON. Benchmark the renderer-off ELF from make measure instead.
.equ FRAME_DELAY, 1000000
.text
li a0, LED_MATRIX_0_BASE
li a1, LED_MATRIX_0_WIDTH
li a2, LED_MATRIX_0_HEIGHT
li a3, FRAME_DELAY
j led_payload
.align 4096
led_payload:
'''
 text=header+'\n'.join(lines)+'\n.data\n'+'\n'.join('.byte '+','.join(map(str,data[i:i+24])) for i in range(0,len(data),24))+'\n'
 dest=ROOT/'asm/minirubik.s';dest.write_text(text)
 return dest

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',default='23745612123332');p.add_argument('--implementation',choices=['assembly','gcc','both'],default='both');p.add_argument('--export',action='store_true');a=p.parse_args()
 for impl in (['gcc','assembly'] if a.implementation=='both' else [a.implementation]):print(build(a.input,impl))
 if a.export:print(export_single(build(a.input,'assembly',True),a.input))
