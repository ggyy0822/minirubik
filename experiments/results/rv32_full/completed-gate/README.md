# Complete v5 distance-11 gate

All 2,644 states from the host exact-distance manifest passed on RV32_ISS with
rendering disabled. Every target path passes on-target replay and the independent
host optimality oracle. Maximum: **40,894,417 instructions**, input
`54721631111111`; zero failures. Source hashes were rechecked after completion.

- `summary.json`: complete gate result and source fingerprint.
- `all-cases.csv`: all inputs, lengths, counts, sizes and paths.
- `provenance.json`: source/toolchain/Ripes provenance.
- `raw-evidence.tar.gz`: every original per-case JSON, Ripes output, host oracle
  output and driver log. Extract into a fresh directory to inspect the records.
- `SHA256SUMS`: archive and machine-readable summary checksums.

This is the **v5 full-assembly** gate, separate from historical mixed-runtime v4.
The fingerprint is c0deaa63ee983de786a8d54078b194a0cbb5d8992b54ab344b6dcffd92f254c0.
The code implementation was first pushed in commit c73c518. No target code
changed while this complete gate ran. Compact archiving avoids adding more than
13,000 separate log files to the repository; the raw measurements are preserved.
