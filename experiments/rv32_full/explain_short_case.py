"""Diagnostic only: identical assembly harness isolates C/v5 phase costs.
These are not final-program benchmark numbers and are not used by the hard gate.
"""
from pathlib import Path
import subprocess,os,re,json
root=Path(__file__).resolve().parents[2]
out=root/'output/rv32_full/phase-profile';out.mkdir(parents=True,exist_ok=True)
reports=root/'experiments/results/rv32_full/phase-profile';reports.mkdir(parents=True,exist_ok=True)
source='''
.text
.globl _start
_start:
 la sp, stack_top
 la a0, input
 la a1, p
 la a2, o
 la a3, pr
 la a4, ori
 call target_parse
#if STAGE >= 2
 la t0, pr
 lw a0, 0(t0)
 lw a1, 4(t0)
 la a2, path
 call target_search
#endif
#if STAGE >= 3
 mv a3, a0
 la a0, p
 la a1, o
 la a2, path
 call target_replay
#endif
 li a0, 0
 li a7, 93
 ecall
1: j 1b
.section .rodata
input: .asciz "23745612123332"
.section .bss
.balign 4
pr: .space 4
ori: .space 4
p: .space 7
o: .space 7
path: .space 11
.balign 16
.space 8192
stack_top:
'''
(out/'entry.S').write_text(source)
results=[]
for impl in ['gcc','assembly']:
 sources=([root/'experiments/rv32_baseline'/n for n in ['state.c','search.c']] if impl=='gcc' else [root/'experiments/rv32_full'/n for n in ['state.S','search.S','heuristic.S']])
 for stage in [1,2,3]:
  name=f'{impl}-{stage}';elf=out/(name+'.elf')
  subprocess.run(['riscv64-elf-gcc','-O2','-march=rv32i','-mabi=ilp32','-msmall-data-limit=0','-mno-relax','-ffreestanding','-fno-builtin','-fno-stack-protector','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,-T,'+str(root/'experiments/toolchain/ripes.ld'),'-DSTAGE='+str(stage),str(out/'entry.S'),*map(str,sources),str(root/'output/rv32_full/tables.S'),'-o',str(elf)],check=True)
  run=subprocess.run([str(Path.home()/'Ripes/build/Ripes.app/Contents/MacOS/Ripes'),'--mode','cli','--src',str(elf),'-t','elf','--proc','RV32_ISS','--iret','--timeout','10000'],env=dict(os.environ,QT_QPA_PLATFORM='offscreen'),capture_output=True,text=True)
  raw=run.stdout+run.stderr;(reports/(name+'.txt')).write_text(raw)
  assert 'Program exited with code: 0' in raw,raw
  results.append(dict(implementation=impl,through_stage=stage,instructions=int(re.search(r'instructions retired\s*\n(\d+)',raw)[1])))
(reports/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
