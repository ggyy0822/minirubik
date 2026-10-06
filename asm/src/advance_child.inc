/* Student-completed inline transition lookup. The advance_child label is
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
    slli t0, a0, 1
    add t0, a2, t0
    slli t1, a1, 1
    add t1, a3, t1
    lhu a0, 0(t0)
    lhu a1, 0(t1)
    sw a0, 8(s0)
    sw a1, 12(s0)
