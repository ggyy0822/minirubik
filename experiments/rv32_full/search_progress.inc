/* Student-completed backtracking and action enumeration, transcribed unchanged.
 * Falls through after try_move with the current action in t0.
 */
backtrack:
    beq s1, zero, next_bound
    addi s1, s1, -1
    addi s0, s0, -32
    j search_loop
try_move:
    lw t0, 16(s0)
    addi t1, zero, 9
    beq t0, t1, backtrack
    addi t1, t0, 1
    sw t1, 16(s0)
