/* Student exercise after feedback: assistant corrected the save comma and
 * demonstrated the p load/store pair; student corrected the o load/store pair.
 */
prepare_child:
    sw t0, 24(s0)
    la t1, first_turn
    add t1, t1, t0
    lbu t2, 0(t1)
    beq t2, zero, advance_child
    lw t1, 0(s0)
    sw t1, 8(s0)
    lw t1, 4(s0)
    sw t1, 12(s0)
advance_child:
