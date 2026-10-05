/* Student-completed search-loop entry; labels are supplied by the harness
 * until this fragment is integrated into a complete search implementation.
 */
search_loop:
    lw t0, 0(s0)
    lw t1, 4(s0)
    or t0, t0, t1
    beq t0, zero, found
    beq s1, s2, backtrack
    j try_move
