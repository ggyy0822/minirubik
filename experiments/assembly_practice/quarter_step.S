/* Student-authored instructions, transcribed unchanged from the conversation.
 * Assistant added assembler metadata only.
 */
.text
.globl quarter_step
.type quarter_step, @function
quarter_step:
    slli t0, a0, 1
    add t0, a2, t0
    slli t1, a1, 1
    add t1, a3, t1
    lhu a0, 0(t0)
    lhu a1, 0(t1)
    ret
.size quarter_step, .-quarter_step
