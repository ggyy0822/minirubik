"""AI build adapter: linked RV32I payload plus Ripes symbol-aware bootstrap.
Ripes at the pinned revision lacks .if; rendering is selected by host CPP.
"""
import argparse, pathlib, subprocess, re
root=pathlib.Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('state');p.add_argument('--render',type=int,choices=[0,1],default=1);args=p.parse_args()
assert len(args.state)==14 and args.state.isdigit()
out=root/'output/led';out.mkdir(exist_ok=True)
prefix=out/(args.state+('-render' if args.render else '-measure'))
assembly=root/'experiments/assembly_practice'
sources=[assembly/n for n in ('student_search.S','heuristic.S','init_frame.S')]
sources += [root/'experiments/rv32_baseline'/n for n in ('state.c','start.S')]
sources += [root/'experiments/led/main.c',root/'output/rv32_baseline/tables.c']
if args.render: sources += [root/'experiments/led/render.S']
cmd=['riscv64-elf-gcc','-O2','-std=c99','-march=rv32i','-mabi=ilp32','-msmall-data-limit=0','-mno-relax','-ffreestanding','-fno-builtin','-fno-stack-protector','-Wall','-Wextra','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,-T,'+str(root/'experiments/toolchain/ripes.ld'),'-DRENDER='+str(args.render),'-DCUBE_INPUT="'+args.state+'"',*map(str,sources),'-o',str(prefix.with_suffix('.elf'))]
subprocess.run(cmd,check=True)
for section in ('.text','.rodata','.data'):
 subprocess.run(['riscv64-elf-objcopy','-O','binary','--only-section='+section,str(prefix.with_suffix('.elf')),str(prefix)+section+'.bin'],check=True)
report=subprocess.check_output(['riscv64-elf-size','-A',str(prefix.with_suffix('.elf'))],text=True)
prefix.with_suffix('.sections.txt').write_text(report)
prefix.with_suffix('.disasm').write_text(subprocess.check_output(['riscv64-elf-objdump','-d','-M','no-aliases',str(prefix.with_suffix('.elf'))],text=True))
sections={line.split()[0]:(int(line.split()[1]),int(line.split()[2])) for line in report.splitlines() if line.startswith('.')}
# Ripes source uses default text base 0 and data base 0x10000000.
# This constant-size bootstrap loads peripheral symbols at assembly time, then
# jumps to a prelinked payload at 0x1000. Readable assembly/C sources live above.
text=(pathlib.Path(str(prefix)+'.text.bin')).read_bytes()
assert len(text)%4==0
lines=[]
for line in prefix.with_suffix('.disasm').read_text().splitlines():
 match=re.match(r'\s*([0-9a-f]+):\s+[0-9a-f]{8}\s+(\S+)\s*(.*)',line)
 if not match:continue
 address,opcode,operands=match.groups()
 operands=operands.split('#')[0].strip()
 if opcode=='jalr':
  operands=re.sub(r'([^,]+),(-?\d+)\(([^)]+)\)',r'\1,\3,\2',operands)
 operands=re.sub(r'([0-9a-f]+) <[^>]+>',lambda m:'insn_'+m[1],operands)
 lines.extend(['insn_'+address+':',opcode+' '+operands])
assert len(lines)//2 == len(text)//4, 'Disassembly omitted executable bytes'
payload='\n'.join(lines)

data=bytearray()
for section in ('.rodata','.data'):
 if section not in sections:continue
 size,addr=sections[section];offset=addr-0x10000000
 data.extend(bytes(max(0,offset-len(data))))
 data.extend(pathlib.Path(str(prefix)+section+'.bin').read_bytes())
data_src='\n'.join('.byte '+','.join(str(x) for x in data[i:i+24]) for i in range(0,len(data),24))
for mode in (['gui','buffer'] if args.render else ['cli']):
 base='LED_MATRIX_0_BASE' if mode=='gui' else '0x20000000'
 width='LED_MATRIX_0_WIDTH' if mode=='gui' else '35'
 height='LED_MATRIX_0_HEIGHT' if mode=='gui' else '25'
 # Ripes supports .align but not .space/.if at the pinned revision.
 boot=f'''# Generated loader, input={args.state}, RENDER={args.render}, mode={mode}.
# Readable sources: experiments/led/ and experiments/assembly_practice/.
# GUI: add LED Matrix 0, Width 35, Height 25; select RV32_ISS for animation.
.equ FRAME_DELAY, {1000000 if mode=='gui' else 0}
.text
li a0, {base}
li a1, {width}
li a2, {height}
li a3, FRAME_DELAY
j led_payload
.align 4096
led_payload:
'''
 path=out/(prefix.name+'-'+mode+'.s');path.write_text(boot+payload+'\n.data\n'+data_src+'\n')
 print(path)
