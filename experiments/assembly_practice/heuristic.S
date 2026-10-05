/* Teaching exercise: address calculations completed by the student.
 * Comparison skeleton supplied by the assistant; load addressing syntax
 * corrected by the assistant from `lbu a0, t0` to `lbu a0, 0(t0)` (and a1).
 */
.text
.globl heuristic
.type heuristic, @function
heuristic:
    add t0, a2, a0
    add t1, a3, a1
    lbu a0, 0(t0)
    lbu a1, 0(t1)
    bgeu a0, a1, heuristic_done
    addi a0, a1, 0
heuristic_done:
    ret
.size heuristic, .-heuristic
