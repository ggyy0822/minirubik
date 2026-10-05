/* Student-authored function, transcribed from the conversation.
 * Assistant changes: operand commas and assembler metadata only.
 */
.text
.globl max_distance
.type max_distance, @function
max_distance:
    bgeu a0, a1, done
    addi a0, a1, 0
done:
    ret
.size max_distance, .-max_distance
