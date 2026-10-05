# AI-authored small teaching harness around the existing heuristic instruction
# sequence. pd/od here are example bytes, NOT the full cube pattern databases.
# Expected: h=6, depth+h=8, bound=7, prune_result=1; prints 1 and exits 0.
.data
pd_demo: .byte 0, 3, 5, 4
od_demo: .byte 0, 2, 4, 6
.align 4
prune_result: .word 0
.text
main:
    la a2, pd_demo
    la a3, od_demo
    addi a0, zero, 2
    addi a1, zero, 3
    call heuristic
    addi t2, a0, 2       # depth=2, f=g+h=8
    addi t3, zero, 7     # bound=7
    sltu t4, t3, t2      # 7 < 8 => prune
    la t5, prune_result
    sw t4, 0(t5)        # Demonstrate memory write; should write 1.
    lw a0, 0(t5)        # Read it back, then print.
    addi a7, zero, 1
    ecall
    addi a0, zero, 0
    addi a7, zero, 93
    ecall
heuristic:
    add t0, a2, a0
    add t1, a3, a1
    lbu a0, 0(t0)       # pd_demo[2] = 5
    lbu a1, 0(t1)       # od_demo[3] = 6
    bgeu a0, a1, heuristic_done
    addi a0, a1, 0
heuristic_done:
    ret
