# Only compiled when RENDER=1. s8=base, s11=delay; s0-s2 retained.
display_error:
    la a0, display_label
    call ripes_puts
    li a0, 3
    j exit
draw_frame:
    addi sp, sp, -16
    sw ra, 12(sp)
    sw s3, 0(sp)
    sw s4, 4(sp)
    la a0, cube_p
    la a1, cube_o
    mv a2, s8
    li a3, 35
    call led_draw
    mv t0, s8
    li t1, 875
    li s3, 0
1:  slli t2, s3, 5
    srli t3, s3, 27
    xor s3, t2, t3
    lw t2, 0(t0)
    xor s3, s3, t2
    addi t0, t0, 4
    addi t1, t1, -1
    bnez t1, 1b
    la a0, frame_label
    call ripes_puts
    mv a0, s3
    call ripes_putint
    la a0, newline
    call ripes_puts
    bnez s11, 3f
    la a0, pixels_label
    call ripes_puts
    mv s3, s8
    li s4, 875
2:  la a0, space
    call ripes_puts
    lw a0, 0(s3)
    call ripes_putint
    addi s3, s3, 4
    addi s4, s4, -1
    bnez s4, 2b
    la a0, newline
    call ripes_puts
3:  mv t0, s11
4:  beqz t0, 5f
    addi t0, t0, -1
    j 4b
5:  lw s3, 0(sp)
    lw s4, 4(sp)
    lw ra, 12(sp)
    addi sp, sp, 16
    ret
.section .rodata
frame_label: .asciz "frame: "
pixels_label: .asciz "pixels:"
move_label: .asciz "move: "
display_label: .asciz "Set LED Width=35 Height=25\n"
.text
