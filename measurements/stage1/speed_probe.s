.equ WORDS, 65536

.text
main:
    li   t0, 0x10000000
    li   t1, WORDS
    addi t2, zero, 1

write_loop:
    sw   t2, 0(t0)
    addi t0, t0, 4
    addi t1, t1, -1
    bne  t1, zero, write_loop

    addi a7, zero, 10
    ecall
