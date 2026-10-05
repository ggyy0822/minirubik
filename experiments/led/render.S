/* AI-authored teaching renderer. Review provenance before submission.
 * a0=p[7], a1=o[7], a2=framebuffer/MMIO base, a3=width (35).
 * All registers used are caller-saved; no heap, multiplication or recursion.
 */
#include "geometry.inc"
.text
.globl led_draw
.type led_draw,@function
led_draw:
    mv t0, a2
    li t1, 875
.Lclear:
    sw zero, 0(t0)
    addi t0, t0, 4
    addi t1, t1, -1
    bne t1, zero, .Lclear
    la a4, led_cells
    addi a5, a4, 96
.Lcell:
    lbu t0, 0(a4)       # Physical corner: 0 fixed, 1..7 movable.
    lbu t1, 1(a4)       # Local sticker slot.
    li a6, 0
    beq t0, zero, .Lcolor
    addi t0, t0, -1
    add t2, a0, t0
    lbu a6, 0(t2)
    addi a6, a6, 1      # Convert stored cubie ID to physical ID.
    add t2, a1, t0
    lbu t2, 0(t2)
    sub t1, t1, t2
    bge t1, zero, .Lcolor
    addi t1, t1, 3      # (slot - orientation) mod 3, range -2..2.
.Lcolor:
    slli t2, a6, 1
    add t2, t2, a6      # Three sticker colors per cubie.
    add t2, t2, t1
    la t0, led_cubie_colors
    add t0, t0, t2
    lbu t0, 0(t0)
    slli t0, t0, 2
    la t1, led_rgb
    add t0, t0, t1
    lw a7, 0(t0)
    lbu t0, 2(a4)       # Pixel x.
    lbu t1, 3(a4)       # Pixel y.
    slli t2, t1, 5
    slli t3, t1, 1
    add t2, t2, t3
    add t2, t2, t1      # y * 35 = y*32 + y*2 + y.
    add t0, t0, t2
    slli t0, t0, 2
    add t0, a2, t0      # base + 4*(y*35+x).
    slli t3, a3, 2      # Byte stride between rows.
    li t4, 3
.Lrow:
    li t5, 4
    mv t6, t0
.Lpixel:
    sw a7, 0(t6)
    addi t6, t6, 4
    addi t5, t5, -1
    bne t5, zero, .Lpixel
    add t0, t0, t3
    addi t4, t4, -1
    bne t4, zero, .Lrow
    addi a4, a4, 4
    bltu a4, a5, .Lcell
    ret
.size led_draw,.-led_draw
