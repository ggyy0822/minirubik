# Working progress tracker

The student requests an approximate overall homework completion percentage at
the end of every conversational response. Use a stable, deliverable-based
estimate, not a quiz score, number of dialogue turns, or claimed grading weight.
Do not increase it merely for another short explanation or repeated test.

Current rough overall estimate: **62%** (including deliverable/authorship gaps).

Completed technical preparation: Ripes/toolchain setup, baseline program
reading, student-executed memory/speed probes, AI teaching C prototype and
native exhaustive checks, AI GCC RV32I baseline and limited target checks.
The generated prototype/baseline is reference work, not automatically a valid
student-authored submission under the assignment rules.

Assembly learning: maximum, heuristic byte lookup, quarter-turn halfword lookup,
and a guided half-turn function using saved return address. The student's
completed `evaluate_state` exercise now integrates heuristic lookup and pruning
with saved arguments/return address; 864 real-table combinations passed on
each of ISS and RV32_5S. Integrated control through child generation now passes
108 actual transitions and 16 exhausted enumerations on both models. The student has completed the remaining search-control fragments. The full
assembly search now links with the existing C parser/replay/runtime. Solved,
one-move, and reference eleven-move target cases pass replay and host optimality
checks. This remains a mixed C/assembly program; full target-domain performance
coverage and optimization are pending. The student-completed inline pruning optimization reduces the hard sample
from 60,727,876 to 47,292,244 instructions. The reference case falls from
22,211,301 to 17,298,120. Both preserve paths and pass replay/optimality;
all 2644 hard target cases remain unverified, so overall performance compliance
is not established. Source comments
record student and assistant contributions.

Major remaining deliverables: student design/reasoning and required authorship,
remaining handwritten RV32I deliverables, C/assembly iterative optimization, performance
coverage of all distance-11 states, complete target cross-model validation,
LED renderer, pipeline walkthrough, English HackMD revisions/disclosure,
fork/tag/submission record, and final oral preparation.

Latest optimization: student inlined the six quarter_step lookup instructions.
Reference ISS count is now 16,596,237, hard sample 45,372,868 (three instructions
saved per generated child). Paths unchanged, replay/optimality and small ISS/5S
regressions pass; .text 1792, static data 49252. Overall estimate stays 52%:
this is another local optimization, not completion of the full performance gate.

Student removed two redundant child_check loads (v4). Sole entry is fall-through
from advance_child, which preserves updated a0/a1 through stores. Reference count
16,128,315; hard sample 44,093,284. All four ISS samples and short 5S replay/optimality
checks pass with unchanged paths. .text 1784; static data 49252. Estimate remains 52%.

Validation phase (search frozen): exported all 2644 exact-distance-11 states
and built a fingerprinted resumable Ripes runner. Top three by host generated
children pass target replay, host optimality and <=50M gate: 54721631111111
44,093,284; 14325671111111 43,343,199; 41752632313211 42,285,895.
Formal batch coverage 3/2644, not exhaustive. Rerun verified cached resume.
Full batch estimated about 6.2 model-hours plus overhead; not started in background.
Assembly/Makefile bytes confirmed unchanged from frozen v4. Next delivery focus:
LED renderer and pipeline/report work; full target gate remains outstanding.

LED teaching/reference module implemented (AI-authored, clearly separated from
student assembly): actual path replay, six-face 35x25 net, RV32I pixel stores,
GUI symbolic peripheral bootstrap and compile-time renderer switch. Actual Ripes
RAM rendering matches all 875 pixels per frame: solved/one-move/reference-11 on
ISS and one-move on 5S. Native 1000-turn 3D mapping oracle passes; renderer-off
CLI test and ISA/size audits pass. GUI view/animation is NOT yet observed because
native-app tool stalled awaiting access; user must confirm in Ripes. Search v4
unchanged. Estimate 58%, reflecting tested display implementation but not live GUI
completion or authorship compliance. Next: GUI confirmation, walkthrough/report,
remaining handwritten work, and full final-build target performance gate.

2026-10-05 user supplied two GUI screenshots: one-move R' solved net displays
correctly, console replay PASS and exit 0; initial/final hashes match tested frames.
GUI peripheral output now confirmed. Static screenshots alone do not confirm
animation timing. Disassembly panel shows Unknown instruction, cause unresolved;
not evidence of a runtime failure. Evidence copied under results/led/gui-confirmation.
Approximate progress now 60%; next is pipeline walkthrough and report, plus
outstanding final-build full gate/authorship work.

Pipeline next step prepared: small heuristic/pruning harness, tested ISS and 5S
(print 1, exit 0). Fixture distances are explicitly not full cube PDBs. GUI IF/ID/
EX/MEM/WB signal/mux/reg-write observations not yet supplied; progress stays 60%.

Cross-model v4 tests completed: solved, one-step, new three-step 23745612123332,
and reference 11-step 21345671111111 all pass on ISS and ordinary 5S, with identical
paths and host optimality. Reference 5S took 395311 ms, 16128314 instructions,
19952587 cycles. T7 three-case coverage exists for this v4 mixed-runtime version;
final submission build and GUI signal observations remain outstanding. Actual
solver walkthrough (fixed addresses/hash) and blank English report worksheet
prepared. No fork/HackMD links supplied yet; no commits, tag, publication or
submission made. Rough technical progress now 62%, not submission compliance.

User GUI evidence confirms actual solver lbu at cycle 667 in MEM: address
0x100007ad, data_out=3, a0 still 945. Images archived under results/pipeline/gui.
Load WB and store observations remain pending; estimate stays 62%.

2026-10-05 evening: User GUI observations now confirm load writeback (a0=3 at cycle669), store enable at cycle753, and child permutation memory update 945->1905 at cycle754. Full three-move run finishes with replay PASS, exit0, 4996 cycles/3887 instructions. Evidence indexed in results/pipeline/gui/README.md. Mux select was not observed directly. Technical estimate64%, not submission compliance. Full 2644-case frozen-v4 RV32_ISS gate launched with run_hard.py --all, reusing three passing cases. Completion must be checked from fingerprinted summary; do not assume the ongoing process has passed.

Full gate restart: fixed summary discovery accidentally matching isa-size-audit.json (a list). Summary now selects exact manifest state filenames. Old directory contains four passing case reports; selection check confirms audit excluded. Runner source fingerprint changed to da7aaa48b90f7555, so fresh run was launched without copying cached reports across fingerprints. Solver source unchanged. Inspect new summary for live coverage.

Unified runtime implemented in experiments/final: renderer-off preprocessed main identical to frozen v4, four ELF executable/data/layout comparisons pass. Updated renderer passes 17 frames/875 pixels; all new ELFs pass RV32I/static audits. Full-gate source untouched and not polled. User reports instructor now permits AI; provenance retained. GCC comparison explanation now grounded in base-hoisting/frame-initialization disassembly.

2026-10-06 current status (supersedes estimates above): approximate preparation
85%. Current candidate is experiments/rv32_full, AI-assisted full target assembly,
including inline parser, independent replay and console/LED integration. v5 text
1564 bytes; reference/stress counts14958590/40894417 beat GCC, with a documented
three-step exception3803 vs3730. Eight ISS/5S final-case checks pass; 5769 parser
rank,11 invalid-input,1000 replay and17 framebuffer checks pass. New v5 full gate
runs independently under fingerprint c0deaa63ee983de7. Historical v4 gate is not
proof for v5. Pending: v5 all2644 result, online report/permissions, final tag and
submission receipt. User reports AI permission; preserve provenance.

Completed v5 gate: 2644/2644 PASS, zero failures; max40894417 at54721631111111. Rechecked every result and all available source hashes. Complete raw evidence compactly archived in results/rv32_full/completed-gate. Submission snapshot phase1-v5 prepared. Overall estimate95%; online HackMD owner login/update/owner-only write and accepted submission receipt remain pending. Latest course page now has forms.gle/2ZupDEdJyJkHM8Y6A. Current browser guest; share dialog confirms signed-in-user write, which needs owner correction.

User-requested project layout implemented in baseline/ asm/ tests/ results/ docs/ tools/. Root Makefile defaults to coursework build with test/compare/full validation commands, retaining upstream under named targets. Sources copied byte-identically; all eight ELF layouts/sections match v5. Fresh H1/H2, sampled H3, six short ISS/5S cases, five GCC/assembly comparison pairs and four-frame single-file pixel test pass. Tag phase1-structured-v1 preserves oldphase1-v5. Completion remains95%: updated HackMD paste/revision and formal accepted receipt still pending.
