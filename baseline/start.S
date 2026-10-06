/* AI-generated test runtime, not the hand-written solver. */
.section .text.start,"ax",@progbits
.globl _start
_start:
    la sp, stack_top
    call target_main
    li a7, 93
    ecall
1:  j 1b

.globl ripes_puts
ripes_puts:
    mv t0, a0
2:  lbu a0, 0(t0)
    beq a0, zero, 3f
    li a7, 11
    ecall
    addi t0, t0, 1
    j 2b
3:  ret

.globl ripes_putint
ripes_putint:
    li a7, 1
    ecall
    ret

.section .bss.stack,"aw",@nobits
.balign 16
    .space 8192
stack_top:
