# Store observation from user screenshots

AI-organized evidence notes, not student-authored report analysis.

- Cycle 750: memory word at 0x10009ef8 is 0x000003b1 (945); instruction 0x1164 is in IF.
- Cycle 753: instruction 0x1164 (sw a0,8(s0)) is in MEM; Data memory wr_en tooltip is 1. a0 is 0x771 (1905), while the memory display still shows 945.
- Cycle 754: memory word at 0x10009ef8 is 0x00000771 (1905), with bytes 71 07 00 00. Original parent permutation at 0x10009ef0 remains 945.
- The next store (0x1168) is now in MEM. a1 is 0x161 (353), but memory at 0x10009efc remains 0x128 (296); its completed write is not yet evidenced.

This completes the observed before/enable/after sequence for the first child permutation store. It does not establish completion of the entire pipeline/report requirement.
