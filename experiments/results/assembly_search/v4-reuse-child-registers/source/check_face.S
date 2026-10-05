/* AI-generated integration adapter. Codes: action 0..8, found=10, exhausted=11.
 * a3 points to output {frame, depth, face}. All used s registers are preserved.
 */
.section .rodata
move_faces:
    .byte 0,0,0,1,1,1,2,2,2
.text
.globl select_action
.type select_action, @function
select_action:
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
    mv a0, t0
    j return_face
found:
    li a0, 10
    j return_face
next_bound:
    li a0, 11
return_face:
    sw s0, 0(a3)
    sw s1, 4(a3)
    sw s3, 8(a3)
    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    addi sp, sp, 16
    ret
.size select_action, .-select_action
