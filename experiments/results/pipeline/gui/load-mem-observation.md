User GUI evidence, 2026-10-05 15:53.
Actual v4 solver, RV32_5S: cycle 667, instruction 0x1264 lbu a0,0(t0) in MEM.
Address tooltip 0x100007ad, data_out tooltip 0x00000003. Register a0 still
0x000003b1; t0 is 0x100007ad. The simultaneous WB instruction shown above the
circuit is add t1,a3,a1, not the load. This evidence confirms the memory read,
not the load's WB register-enable or mux-selection values. Those remain pending.
