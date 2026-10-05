/* Student-completed face selection and same-face pruning fragment. */
select_face:
    la t1, move_faces
    add t1, t1, t0
    lbu s3, 0(t1)
    lw t2, 20(s0)
    beq s3, t2, search_loop
