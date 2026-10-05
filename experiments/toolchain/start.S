/* Minimal Ripes runtime for the infrastructure smoke test. */
.section .text.start,"ax",@progbits
.globl _start
_start:
    la sp, stack_top
    call smoke_main
    li t0, 12
    bne a0, t0, failed
    li a7, 1
    ecall
    li a0, 0
    li a7, 93
    ecall
failed:
    li a0, 1
    li a7, 93
    ecall

.section .bss.stack,"aw",@nobits
.balign 16
    .space 4096
stack_top:
