# AI-authored full target entry/output and optional LED integration.
#ifndef CUBE_INPUT
#define CUBE_INPUT "21345671111111"
#endif
.text
.globl _start
_start:
    la sp, stack_top
#if RENDER
    mv s8, a0
    mv s11, a3
    li t0, 35
    bne a1, t0, display_error
    li t0, 25
    bne a2, t0, display_error
#endif
    call parse_input
    beqz a0, invalid_input
    la t0, ranks
    lw a0, 0(t0)
    lw a1, 4(t0)
    la a2, path
    call target_search
    mv s0, a0
    la a0, cube_p
    la a1, cube_o
    la a2, path
    mv a3, s0
    call target_replay
    beqz a0, failed_path
    la a0, input_label
    call ripes_puts
    la a0, input
    call ripes_puts
    la a0, length_label
    call ripes_puts
    mv a0, s0
    call ripes_putint
    la a0, path_label
    call ripes_puts
    la s1, path
    add s2, s1, s0
1:  beq s1, s2, 2f
    la t0, path
    beq s1, t0, 3f
    la a0, space
    call ripes_puts
3:  lbu a0, 0(s1)
    call print_move
    addi s1, s1, 1
    j 1b
2:  la a0, pass_label
    call ripes_puts
#if RENDER
    call parse_input
    call draw_frame
    la s1, path
4:  beq s1, s2, 5f
    la a0, cube_p
    la a1, cube_o
    mv a2, s1
    li a3, 1
    call target_replay
    la a0, move_label
    call ripes_puts
    lbu a0, 0(s1)
    call print_move
    la a0, newline
    call ripes_puts
    call draw_frame
    addi s1, s1, 1
    j 4b
5:
#endif
    li a0, 0
exit:
    li a7, 93
    ecall
    j exit
invalid_input:
    la a0, invalid_label
    call ripes_puts
    li a0, 2
    j exit
failed_path:
    la a0, fail_label
    call ripes_puts
    li a0, 1
    j exit
parse_input:
    la a0, input
    la a1, cube_p
    la a2, cube_o
    la a3, ranks
    addi a4, a3, 4
    tail target_parse
print_move:
    slli t0, a0, 1
    add t0, t0, a0
    la a0, names
    add a0, a0, t0
    # Tail call preserves original caller's return address.
ripes_puts:
    mv t0, a0
1:  lbu a0, 0(t0)
    beqz a0, 2f
    li a7, 11
    ecall
    addi t0, t0, 1
    j 1b
2:  ret
ripes_putint:
    li a7, 1
    ecall
    ret
#if RENDER
#include "display.inc"
#endif
.section .rodata
input: .asciz CUBE_INPUT
input_label: .asciz "input: "
length_label: .asciz "\nlength: "
path_label: .asciz "\npath: "
pass_label: .asciz "\nreplay: PASS\n"
invalid_label: .asciz "INVALID INPUT\n"
fail_label: .asciz "PATH CHECK FAILED\n"
space: .asciz " "
newline: .asciz "\n"
names: .ascii "R\0\0R2\0R'\0B\0\0B2\0B'\0D\0\0D2\0D'\0"
.section .bss
.balign 4
ranks: .space 8
cube_p: .space 7
cube_o: .space 7
path: .space 11
.balign 16
stack: .space 8192
stack_top:
