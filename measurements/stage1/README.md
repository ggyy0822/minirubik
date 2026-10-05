# Stage 1 measurement records

These are raw logs from commands executed by the student, copied from the
Ripes directory. They are not measurements newly executed by the assistant.

- minirubik checkout inspected: `3811ad0a87bd490e45099c3cb179ec33caf46cb5`.
- Ripes source checkout reported by the student:
  `5b8a616edcb6f0a2ddb07e78951348b72497f1e1`, with clean `git status --short`.
  The executable's correspondence to that checkout has not been independently verified.
- Host described by the student: Apple Silicon Mac. Exact chip, RAM, macOS
  version, and build configuration have not yet been recorded.
- Memory probes write 1,024 or 1,048,576 distinct aligned 32-bit words.
- Speed probes write 65,536 words, using the same source on both processors.
- Ripes `--iret` measures guest instructions; host `time` instruction counters
  must not be substituted for it.
- Memory metric: macOS `/usr/bin/time -l` maximum resident set size in bytes.
  This is distinct from the reported peak memory footprint.
- The 4 MiB `RV32_5S` run timed out. Retain its log, but exclude it from
  completed-run speed and memory comparisons.

Run `python3 measurements/stage1/summarize.py` from the repository root to
regenerate `results.csv` and print descriptive statistics. The script reads
the existing logs only. It matches the Ripes report headers so it does not
confuse host and guest instruction counts.

The memory statistic uses the difference of median RSS values divided by the
difference in written guest ranges. It is a two-size empirical slope, not a
guaranteed conversion factor or a measurement of the complete solver.
Speed figures describe these probes, not arbitrary search workloads.

## AI assistance record (working record, student review required)

The assistant explained baseline code and architecture concepts, supplied
the standalone probe assembly and measurement commands, and generated the
log extraction script and this record. The student executed the probes and
provided the outputs. The original logs are retained. This record does not
claim the probes or their methodology were independently student-authored.
Check the assignment's hand-written-component requirements with the
instructor before using AI-generated probe assembly as assessed work.
The student's own analysis and design decisions remain to be written.
