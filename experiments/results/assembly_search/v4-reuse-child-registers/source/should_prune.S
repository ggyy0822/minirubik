/* Student-completed exercise; assistant added one operand comma and metadata.
 * Inputs are bounded nonnegative cube-search counts; g+h cannot overflow.
 */
.text
.globl should_prune
.type should_prune, @function
should_prune:
    add t0, a0, a1
    bltu a2, t0, prune
    addi a0, zero, 0
    ret
prune:
    addi a0, zero, 1
    ret
.size should_prune, .-should_prune
