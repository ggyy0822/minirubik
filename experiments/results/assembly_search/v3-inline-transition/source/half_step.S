/* Student supplied this version after an assistant demonstration.
 * Guided practice, not claimed as independently authored assignment code.
 * Calls the specific quarter_step implementation that preserves a2/a3.
 */
.text
.globl half_step
.type half_step, @function
half_step:
    addi sp, sp, -16
    sw ra, 12(sp)
    call quarter_step
    call quarter_step
    lw ra, 12(sp)
    addi sp, sp, 16
    ret
.size half_step, .-half_step
