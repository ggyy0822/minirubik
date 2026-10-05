/* AI-generated adapter for the student's combined search fragments.
 * Results: action 0..8, found=10, next_bound=11.
 * Writes observed frame pointer/depth through a3 for verification.
 */
.text
.globl advance_search
.type advance_search, @function
advance_search:
    addi sp, sp, -16
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    mv s0, a0
    mv s1, a1
    mv s2, a2
#include "search_entry.inc"
#include "search_progress.inc"
    mv a0, t0
    j return_progress
found:
    li a0, 10
    j return_progress
next_bound:
    li a0, 11
return_progress:
    sw s0, 0(a3)
    sw s1, 4(a3)
    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    addi sp, sp, 16
    ret
.size advance_search, .-advance_search
