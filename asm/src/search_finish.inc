/* Student-supplied completion of the guided search-control worksheet. */
child_check:
    # Student optimization: use a0/a1 from advance_child fall-through.
    # Student-completed inline pruning, replacing evaluate_state call.
    add t0, t3, a0
    lbu t0, 0(t0)
    add t1, t4, a1
    lbu t1, 0(t1)
    bgeu t0, t1, child_h_ready
    addi t0, t1, 0
child_h_ready:
    addi t2, s1, 1
    add t2, t2, t0
    bltu s2, t2, search_loop
    # AI v5: initialize child directly from live child ranks.
    addi t0, s0, 32
    sw a0, 0(t0)
    sw a1, 4(t0)
    sw a0, 8(t0)
    sw a1, 12(t0)
    sw zero, 16(t0)
    sw s3, 20(t0)
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
    sw s4, 0(s0)
    sw s5, 4(s0)
    sw s4, 8(s0)
    sw s5, 12(s0)
    sw zero, 16(s0)
    li t0, 3
    sw t0, 20(s0)
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
