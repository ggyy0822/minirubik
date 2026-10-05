"""AI-authored target parser/replay gates independent of search tables."""
import itertools,json,os,pathlib,random,re,subprocess,sys
root=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'experiments/led'))
import geometry
out=root/'output/rv32_full/state-check';out.mkdir(parents=True,exist_ok=True)
reports=root/'experiments/results/rv32_full/state-check';reports.mkdir(parents=True,exist_ok=True)
start='''.text
.globl _start
_start:
 la sp, stack_top
 la s0, cases
 li s1, 0
'''
finish='''
 li a0, 0
 j exit
bad:
 li a0, 1
exit:
 li a7, 93
 ecall
 j exit
.section .bss
.balign 16
p: .space 7
o: .space 7
.balign 4
pr: .space 4
ori: .space 4
.space 256
stack_top:
'''
parse='''
 mv a0, s0
 la a1, p
 la a2, o
 la a3, pr
 la a4, ori
 call target_parse
'''
valid=[''.join(str(x+1) for x in perm)+'1111111' for perm in itertools.permutations(range(7))]
for ori in itertools.product(range(3),repeat=6):
 valid.append('1234567'+''.join(str(x+1) for x in (*ori,(-sum(ori))%3)))
source=start+'loop:\n'+parse+''' beqz a0, bad
 la t0, pr
 lw t0, 0(t0)
 la t1, ori
 lw t1, 0(t1)
 li t2, 5040
 bgeu s1, t2, orientation
 bne t0, s1, bad
 bnez t1, bad
 j advance
orientation:
 bnez t0, bad
 sub t2, s1, t2
 bne t1, t2, bad
advance:
 addi s0, s0, 15
 addi s1, s1, 1
 li t0, 5769
 bne s1, t0, loop
'''+finish+'.section .rodata\ncases:\n'+''.join('.asciz "'+s+'"\n' for s in valid)
# Empty, short, long, range errors, duplicate cubies, invalid twist sum.
invalid=['','1234567','1234567111111','123456711111111','02345671111111','82345671111111','11345671111111','12345670111111','12345674111111','12345672111111','abcdefg1111111']
negative=start+'loop:\n'+parse+''' bnez a0, bad
 addi s0, s0, 16
 addi s1, s1, 1
 li t0, 11
 bne s1, t0, loop
'''+finish+'.section .rodata\ncases:\n'+''.join('.byte '+','.join(map(str,s.encode()+bytes(16-len(s))))+'\n' for s in invalid)
rng=random.Random(20261006);records=[]
for n in range(1000):
 p=list(range(7));rng.shuffle(p);o=[rng.randrange(3) for _ in range(6)];o.append(-sum(o)%3)
 move=n%9;np,no=p,o
 for _ in range(move%3+1):np,no=geometry.turn(np,no,move//3)
 records.append(bytes(p+o+[move]+np+no))
replay=start+'''loop:
 la t0, p
 la t1, o
 li t2, 0
copy:
 add t3, s0, t2
 lbu t4, 0(t3)
 lbu t5, 7(t3)
 sb t4, 0(t0)
 sb t5, 0(t1)
 addi t0, t0, 1
 addi t1, t1, 1
 addi t2, t2, 1
 li t6, 7
 bne t2, t6, copy
 la a0, p
 la a1, o
 addi a2, s0, 14
 li a3, 1
 call target_replay
 la t0, p
 la t1, o
 addi t2, s0, 15
 li t3, 7
compare:
 lbu t4, 0(t0)
 lbu t5, 0(t2)
 bne t4, t5, bad
 lbu t4, 0(t1)
 lbu t5, 7(t2)
 bne t4, t5, bad
 addi t0, t0, 1
 addi t1, t1, 1
 addi t2, t2, 1
 addi t3, t3, -1
 bnez t3, compare
 addi s0, s0, 29
 addi s1, s1, 1
 li t0, 1000
 bne s1, t0, loop
'''+finish+'.section .rodata\ncases:\n'+''.join('.byte '+','.join(map(str,b))+'\n' for b in records)
results=[]
for name,src,count in [('parser-ranks',source,5769),('parser-invalid',negative,11),('physical-replay',replay,1000)]:
 asm=out/(name+'.S');asm.write_text(src);elf=out/(name+'.elf')
 subprocess.run(['riscv64-elf-gcc','-march=rv32i','-mabi=ilp32','-mno-relax','-nostdlib','-Wl,--no-relax','-Wl,-T,'+str(root/'experiments/toolchain/ripes.ld'),str(asm),str(root/'experiments/rv32_full/state.S'),'-o',str(elf)],check=True)
 run=subprocess.run([str(pathlib.Path.home()/'Ripes/build/Ripes.app/Contents/MacOS/Ripes'),'--mode','cli','--src',str(elf),'-t','elf','--proc','RV32_ISS','--iret','--timeout','120000'],env=dict(os.environ,QT_QPA_PLATFORM='offscreen'),capture_output=True,text=True,timeout=150)
 raw=run.stdout+run.stderr;(reports/(name+'.txt')).write_text(raw)
 assert run.returncode==0 and 'Program exited with code: 0' in raw,raw
 results.append(dict(test=name,cases=count,result='PASS',instructions=int(re.search(r'instructions retired\s*\n(\d+)',raw)[1])))
 print(results[-1],flush=True)
(reports/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
