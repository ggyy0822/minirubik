/* Student-supplied completion of the guided search-control worksheet. */
child_check:
    lw a0, 8(s0)
    lw a1, 12(s0)
    la a2, rt_pd
    la a3, rt_od
    addi a4, s1, 1
    addi a5, s2, 0
    call evaluate_state
    bne a0, zero, search_loop
    addi a0, s0, 32
    lw a1, 8(s0)
    lw a2, 12(s0)
    addi a3, s3, 0
    call init_frame
    addi s0, s0, 32
    addi s1, s1, 1
    j search_loop
next_bound:
    addi s2, s2, 1
    addi t0, zero, 12
    bgeu s2, t0, no_solution
    j start_bound
start_bound:
    addi s0, s7, 0
    addi s1, zero, 0
    addi a0, s0, 0
    addi a1, s4, 0
    addi a2, s5, 0
    addi a3, zero, 3
    call init_frame
    j search_loop
found:
    addi t0, s7, 0
    addi t1, s6, 0
    addi t2, zero, 0
copy_path:
    beq t2, s1, solved_return
    lw t3, 24(t0)
    sb t3, 0(t1)
    addi t0, t0, 32
    addi t1, t1, 1
    addi t2, t2, 1
    j copy_path
solved_return:
    addi a0, s1, 0
    j search_return
no_solution:
    addi a0, zero, -1
    j search_return
