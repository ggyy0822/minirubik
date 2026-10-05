# Target validation of the frozen v4 assembly search

The host-only exporter builds the exact oracle, enumerates every distance-11
state, checks the teaching reference solution by physical replay, and emits
2644 unique inputs. The manifest is sorted by host generated-child count to
prioritize demanding cases; this ordering does not prove target instruction order.
Neither the full oracle nor this manifest is linked into the target executable.

Regenerate the manifest from repository root:

```sh
cc -O2 -std=c99 -Wno-unused-function experiments/validation/export_hard.c -o output/export_hard
./output/export_hard > output/hard-manifest.csv
python3 - <<'PYTHON'
import csv
rows=list(csv.DictReader(open('output/hard-manifest.csv')))
rows.sort(key=lambda r:int(r['generated']), reverse=True)
with open('experiments/validation/hard-manifest.csv','w') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
PYTHON
```

Run from repository root:

```sh
python3 experiments/validation/run_hard.py --limit 3
# Full run, potentially several hours; Ctrl-C may interrupt the current case.
python3 experiments/validation/run_hard.py --all
```

Repeat the same command to resume. Only completed passing cases with matching
source/toolchain/Ripes/manifest fingerprint are reused. Failed/incomplete cases
are rerun. Summary always distinguishes partial coverage from full coverage.
The runner stops on failure, including timeout, wrong path/length or exceeding
50 million instructions. Each target report includes C input parsing, assembly
search, target physical replay, printing and exit. Host exact-distance checking
is a separate process. Ripes uses RV32_ISS and the offscreen Qt backend; no LED
renderer is linked. Search implementation is not changed by these tools.

The manifest contains 546,298,522 generated children in the teaching host solver.
Scaling by the measured 26.152 seconds for 639,792 children estimates about
6.2 model-hours plus build/startup/checking overhead for all states. This is a
rough planning estimate, not a measured total or a guarantee. Subset coverage
must never be described as full target validation.

AI authored this validation harness; student search fragments retain their
existing provenance. Raw reports and fingerprints: ../results/hard-target/.
