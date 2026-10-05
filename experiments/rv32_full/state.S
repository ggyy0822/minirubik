# AI-authored RV32I parser and independent physical replay. No C runtime.
.text
.globl target_parse
# a0=input; a1=p[7]; a2=o[7]; a3=&rank_p; a4=&rank_o.
target_parse:
    li a5, 7
    li a6, 0
1:  lbu t0, 0(a0)
    beqz t0, 9f
    addi t0, t0, -49
    li t1, 7
    bgeu t0, t1, 9f
    li t1, 1
    sll t1, t1, t0
    and t2, a6, t1
    bnez t2, 9f
    or a6, a6, t1
    sb t0, 0(a1)
    addi a0, a0, 1
    addi a1, a1, 1
    addi a5, a5, -1
    bnez a5, 1b
    li a5, 7
    li a6, 0
2:  lbu t0, 0(a0)
    beqz t0, 9f
    addi t0, t0, -49
    li t1, 3
    bgeu t0, t1, 9f
    add a6, a6, t0
    sb t0, 0(a2)
    addi a0, a0, 1
    addi a2, a2, 1
    addi a5, a5, -1
    bnez a5, 2b
    lbu t0, 0(a0)
    bnez t0, 9f
3:  bltu a6, t1, 4f
    addi a6, a6, -3
    j 3b
4:  bnez a6, 9f
    addi t0, a1, -7
    li t2, 0
    li t3, 7
    li a5, 1
5:  lbu t5, 0(t0)
    addi t6, t0, 1
    li t4, 0
6:  beq t6, a1, 7f
    lbu a6, 0(t6)
    sltu a6, a6, t5
    add t4, t4, a6
    addi t6, t6, 1
    j 6b
7:  li a6, 0
    beqz t2, 11f
    mv a7, t3
8:  add a6, a6, t2
    addi a7, a7, -1
    bnez a7, 8b
11: add t2, a6, t4
    addi t0, t0, 1
    addi t3, t3, -1
    bne t3, a5, 5b
    sw t2, 0(a3)
    addi t0, a2, -7
    addi a2, a2, -1
    li t2, 0
10: lbu t1, 0(t0)
    slli t3, t2, 1
    add t2, t2, t3
    add t2, t2, t1
    addi t0, t0, 1
    bne t0, a2, 10b
    sw t2, 0(a4)
    li a0, 1
    ret
9:  li a0, 0
    ret

.globl target_replay
# a0=p; a1=o; a2=path; a3=length. Mutates p/o, returns solved predicate.
target_replay:
    li t0, 11
    bltu t0, a3, replay_bad_length
    addi sp, sp, -16
    add a4, a2, a3
    li a3, 3
replay_move:
    beq a2, a4, replay_check
    lbu t0, 0(a2)
    li t1, 9
    bgeu t0, t1, replay_bad
    li t1, 0
1:  bltu t0, a3, 2f
    addi t0, t0, -3
    addi t1, t1, 1
    j 1b
2:  addi a7, t0, 1
    slli t0, t1, 3
    sub t0, t0, t1
    la t1, replay_sources
    add t1, t1, t0
    la t2, replay_twists
    add t2, t2, t0
replay_quarter:
    li a6, 0
3:  add t3, t1, a6
    lbu t3, 0(t3)
    add t4, a0, t3
    lbu t4, 0(t4)
    add t5, sp, a6
    sb t4, 0(t5)
    add t3, a1, t3
    lbu t3, 0(t3)
    add t4, t2, a6
    lbu t4, 0(t4)
    add t3, t3, t4
    bltu t3, a3, 4f
    addi t3, t3, -3
4:  sb t3, 8(t5)
    addi a6, a6, 1
    li t6, 7
    bne a6, t6, 3b
    li a6, 0
5:  add t3, sp, a6
    lbu t4, 0(t3)
    lbu t5, 8(t3)
    add t3, a0, a6
    sb t4, 0(t3)
    add t3, a1, a6
    sb t5, 0(t3)
    addi a6, a6, 1
    bne a6, t6, 5b
    addi a7, a7, -1
    bnez a7, replay_quarter
    addi a2, a2, 1
    j replay_move
replay_check:
    li t0, 0
    li t1, 7
6:  lbu t2, 0(a0)
    lbu t3, 0(a1)
    bne t2, t0, replay_bad
    bnez t3, replay_bad
    addi a0, a0, 1
    addi a1, a1, 1
    addi t0, t0, 1
    bne t0, t1, 6b
    li a0, 1
    addi sp, sp, 16
    ret
replay_bad:
    addi sp, sp, 16
replay_bad_length:
    li a0, 0
    ret
.section .rodata
replay_sources: .byte 1,4,2,0,3,5,6, 0,1,2,4,5,6,3, 0,2,5,3,1,4,6
replay_twists: .byte 1,2,0,2,1,0,0, 0,0,0,1,2,1,2, 0,0,0,0,0,0,0
