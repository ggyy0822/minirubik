/* Student-completed transition lookup and call. The advance_child label is
 * at the end of prepare_child.inc; instructions transcribed unchanged.
 */
    lw a0, 8(s0)
    lw a1, 12(s0)
    slli t2, s3, 2
    la t0, permutation_rows
    add t0, t0, t2
    lw a2, 0(t0)
    la t0, orientation_rows
    add t0, t0, t2
    lw a3, 0(t0)
    call quarter_step
    sw a0, 8(s0)
    sw a1, 12(s0)
