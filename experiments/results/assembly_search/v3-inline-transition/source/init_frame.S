/* Student-completed exercise. Assistant normalized pasted whitespace and
 * added assembler metadata; instruction operands are unchanged.
 */
.text
.globl init_frame
.type init_frame, @function
init_frame:
    sw a1, 0(a0)
    sw a2, 4(a0)
    sw a1, 8(a0)
    sw a2, 12(a0)
    sw zero, 16(a0)
    sw a3, 20(a0)
    ret
.size init_frame, .-init_frame
