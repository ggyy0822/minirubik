/* AI-generated adapter for all student control fragments through preparation. */
.section .rodata
move_faces:
    .byte 0,0,0,1,1,1,2,2,2
first_turn:
    .byte 1,0,0,1,0,0,1,0,0
.text
.globl prepare_action
.type prepare_action, @function
prepare_action:
    addi sp, sp, -16
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
    mv a0, t0
    j return_prepare
found:
    li a0, 10
    j return_prepare
next_bound:
    li a0, 11
return_prepare:
    sw s0, 0(a3)
    sw s1, 4(a3)
    sw s3, 8(a3)
    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    addi sp, sp, 16
    ret
.size prepare_action, .-prepare_action
