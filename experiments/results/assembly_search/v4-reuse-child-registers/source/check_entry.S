/* AI-generated test adapter. Return 1=found, 2=backtrack, 0=try_move.
 * Preserve ABI callee-saved registers used by the student's fragment.
 */
.text
.globl classify_entry
.type classify_entry, @function
classify_entry:
    addi sp, sp, -16
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    mv s0, a0
    mv s1, a1
    mv s2, a2
#include "search_entry.inc"
found:
    li a0, 1
    j restore_entry
backtrack:
    li a0, 2
    j restore_entry
try_move:
    li a0, 0
restore_entry:
    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    addi sp, sp, 16
    ret
.size classify_entry, .-classify_entry
