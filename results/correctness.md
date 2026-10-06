# Correctness and measurement evidence

This layout preserves the validated full-assembly v5 algorithm and machine code.
`layout-equivalence.json` records byte-identical text/rodata/data and equal section
sizes/addresses for four inputs with rendering off and on. Maintained assembly
sources match the completed gate provenance; this is a relocation, not a new
algorithm. Existing results are distinguished from newly executed checks.

| Gate | Evidence / scope | Status |
|---|---|---|
| H1 | All 3,674,160 states: h never exceeds exact distance | PASS |
| H2 | Complete transition/PDB generation, ranges, maxima 7/6, solved=0 | PASS |
| H3 | Native final C search/parser/independent replay over 3,674,160 states | PASS, archived full run |
| H4 | No packed tables/decoder used | NOT APPLICABLE |
| T5 | Target replay plus separate exact host oracle | PASS |
| T6 | 21345671111111 returns an optimal 11-move solution | PASS |
| T7 | Solved, one-step, three-step, reference-11 on ISS and ordinary 5S | PASS, archived full suite |
| Universal instruction gate | All 2644 exact-distance-11 states on RV32_ISS | PASS |
| Static/ISA | Base RV32I; renderer-off text1564/static49217 bytes | PASS |
| Standalone export | Actual .s execution with LED symbols replaced by RAM constants | Fresh pixel check |

The complete target maximum is **40,894,417** at `54721631111111`, below 50M.
Reference `21345671111111`: **14,958,590**. Counts include parsing, search, replay,
console output and exit, with rendering compiled out. The exact source/model
fingerprint and each case's counts/path are in `raw/hard-provenance.json` and
`raw/hard-all-cases.csv`. `raw/raw-evidence.tar.gz` preserves every raw case log.
No archive results are relabeled as fresh simulations after rearranging files.

- [Full gate summary](raw/hard-summary.json)
- [Per-case table](raw/hard-all-cases.csv)
- [Historical full native H3](raw/host-full-v5.txt)
- [Historical full cross-model suite](raw/cross-model-v5.json)
- [New logs](raw/current/)
- [GCC comparison](comparison.csv)

`make test` reruns H1/H2, samples H3, executes three short cases on both models,
and checks the standalone export and byte equivalence. Use `make verify-host`
and `make verify-ripes` for the full named gates, or `make verify-full` to rerun
all 2644 simulations. The GUI pipeline screenshots remain v4 observations; their
addresses/cycles are not relabeled as current GUI observations.
