/* Student-completed integration exercise based on the assistant's skeleton.
 * Instructions transcribed unchanged; assistant added assembler metadata.
 */
.text
.globl evaluate_state
.type evaluate_state, @function
evaluate_state:
    addi sp, sp, -16
    sw ra, 12(sp)
    sw a4, 0(sp)
    sw a5, 4(sp)
    call heuristic
    addi a1, a0, 0
    lw a0, 0(sp)
    lw a2, 4(sp)
    call should_prune
    lw ra, 12(sp)
    addi sp, sp, 16
    ret
.size evaluate_state, .-evaluate_state
