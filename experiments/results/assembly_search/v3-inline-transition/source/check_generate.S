/* AI-generated adapter integrating student control and transition fragments. */
#include "search_tables.inc"
.globl generate_action
.type generate_action, @function
generate_action:
    addi sp, sp, -32
    sw ra, 28(sp)
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    sw s3, 12(sp)
    mv s0, a0
    mv s1, a1
    mv s2, a2
#include "search_entry.inc"
#include "search_progress.inc"
#include "select_face.inc"
#include "prepare_child.inc"
#include "advance_child.inc"
    lw a0, 24(s0)
    j return_generate
found:
    li a0, 10
    j return_generate
next_bound:
    li a0, 11
return_generate:
    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    lw ra, 28(sp)
    addi sp, sp, 32
    ret
.size generate_action, .-generate_action
