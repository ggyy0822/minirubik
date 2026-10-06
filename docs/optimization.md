# Optimization history

The following measured development stages are retained from the full report.
The directory reorganization changes no algorithm or target instruction.

## 4. Assembly refinement and comparison

Versions v1–v4 combine guided student exercise fragments with AI-provided ABI
and build scaffolding, plus compiled C parsing/replay/runtime. They are historical
mixed-language versions. The current v5 candidate directly implements the entire
target in assembly, including input validation/ranking, physical replay and output.
The v5 runtime and optimizations are AI-authored; provenance is not relabeled as
independent student authorship.

Each frame uses offsets 0/4 for parent p/o, 8/12 for child p/o, 16 for the next
move, 20 for the previous face and 24 for the selected move. The stride is 32
bytes. Transition reads use lhu; PDB reads use lbu; frame fields use lw/sw.
Callers preserve live caller-saved values, non-leaf helpers preserve ra, and the
search entry saves and restores its callee-saved registers.

The renderer-disabled measurements count the entire program, including parsing,
search, replay, output and exit. Code size is linked .text bytes.

| Version | Reference input instructions | Stress input instructions | .text bytes |
|---|---:|---:|---:|
| GCC -O2 | 15,239,117 | 41,665,257 | 1,764 |
| Assembly v1: helper calls | 22,211,301 | 60,727,876 | 1,868 |
| v2: inline child pruning | 17,298,120 | 47,292,244 | 1,804 |
| v3: inline quarter transition | 16,596,237 | 45,372,868 | 1,792 |
| v4: reuse child registers | 16,128,315 | 44,093,284 | 1,784 |
| v5: full assembly, hoisted bases, inline frames | 14,958,590 | 40,894,417 | 1,564 |

Reference input: 21345671111111. Stress input: 54721631111111.
Inlining pruning removes argument movement and helper overhead. Inlining the
transition removes three retired call/return instructions per generated child
under the recorded no-relax build. Finally, a0/a1 already hold the child ranks,
so eliminating their two reloads saves two instructions per generated child.
Stores remain because later search steps need the frame contents.

The historical v4 assembly loses to GCC on both displayed inputs and on code size
(20 additional text bytes). Disassembly provides concrete remaining costs:
GCC loads the two PDB base addresses into t4/t3 once at entry (0x1048–0x1054)
and reuses them for child lookups (0x1174–0x1180). Assembly v4 reconstructs both
addresses with two `la` pseudoinstructions for every generated child, four real
instructions under this no-relax build. GCC also initializes child frames inline,
where v4 still calls init_frame and moves arguments. These explain avoidable
costs, but are not a complete dynamic attribution of the measured gap: GCC has
its own frame-index arithmetic and differing branches. These v4 results
show improvement over v1 but do not beat GCC. That version remains frozen for
its separate historical gate; v5 has its own target gate.

Evidence: [versioned refinements](../experiments/assembly_practice/README.md).

### v5 full-assembly candidate

The current build links only assembly executable sources. Host-generated immutable
numbers become `.byte`/`.half` table declarations; no C parser, C replay, C main,
allocator or compiler arithmetic helper is linked. The 14-character input is
inlined with `.asciz` and validated on the target. The algorithm and move ordering
remain iterative IDA* with the same admissible maximum-of-projections heuristic.

Search now retains the PDB bases in t3/t4, eliminating four instructions per
child lookup. Its only called helper preserves those caller-saved registers by
construction. Root and child frames are initialized inline, using live child
ranks. The parser omits the final trivial Lehmer digit and skips multiplication
of zero. The RV32I/static audit finds no non-RV32I instructions, undefined symbols
or arithmetic helpers. Renderer-off static storage is 49,217 bytes, including
an 8,192-byte reserved stack; text is 1,564 bytes, 200 bytes below GCC.

| Input | GCC -O2 ISS instructions | v5 ISS instructions | v5 instruction win |
|---|---:|---:|---|
| 12345671111111 | 1,003 | 947 | Yes |
| 25314672313211 | 1,785 | 1,781 | Yes |
| 23745612123332 | 3,730 | 3,803 | No |
| 21345671111111 | 15,239,117 | 14,958,590 | Yes |
| 54721631111111 | 41,665,257 | 40,894,417 | Yes |

The three-step exception is retained. An identical assembly diagnostic harness
calls each implementation through parsing, then search, then replay. C cumulative
counts are 523/1504/3260; v5 counts are 515/1560/3325. Thus v5 saves 8 in parsing,
spends 64 more in search and 9 more in replay for this particular input. The
remaining 8-instruction whole-program difference is in the entry/output wrapper.
The short search does not amortize its control overhead as effectively as the
longer reference/stress searches. This phase attribution is measured; it is not
a claim that every individual overhead instruction has been traced. The diagnostic
harness counts are separate from final-program measurements. No universal GCC
instruction win is claimed.

Evidence: [v5 source/build](../experiments/rv32_full/README.md),
[whole-program comparison](../experiments/results/rv32_full/comparison.json),
[phase attribution](../experiments/results/rv32_full/phase-profile/summary.json),
[ISA/static audit](../experiments/results/rv32_full/audit.json).

