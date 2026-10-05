"""Extract existing user-run Ripes logs; does not run any measurements."""
import csv
import re
import statistics
from pathlib import Path

root = Path(__file__).resolve().parent

def report_number(text, label):
    match = re.search(r"^===== " + re.escape(label) + r"\s*\n(\d+)", text, re.M)
    return int(match.group(1)) if match else None

rows = []
for path in sorted(root.glob("*.txt")):
    text = path.read_text()
    rss = re.search(r"^\s*(\d+)\s+maximum resident set size", text, re.M)
    proc = re.search(r"^processor: (\S+)", text, re.M)
    ok = "Program exited with code: 0" in text and "ERROR:" not in text
    rows.append({
        "file": path.name,
        "status": "complete" if ok else "incomplete",
        "processor": proc.group(1) if proc else "",
        "guest_instructions": report_number(text, "instructions retired"),
        "model_ms": report_number(text, "wall-clock model execution time (ms)"),
        "cycles": report_number(text, "cycles"),
        "max_rss_bytes": int(rss.group(1)) if rss else None,
    })

with (root / "results.csv").open("w", newline="") as out:
    writer = csv.DictWriter(out, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

for proc in ("RV32_ISS", "RV32_5S"):
    group = [r for r in rows if r["file"].startswith("speed_probe_" + proc + "_")]
    assert len(group) == 3 and all(r["status"] == "complete" for r in group)
    assert all(r["guest_instructions"] == 262149 for r in group)
    ms = statistics.median(r["model_ms"] for r in group)
    print(f"{proc}: median {ms} ms; {262149 * 1000 / ms:,.2f} guest instructions/s")

medians = {}
for size in ("small", "large"):
    group = [r for r in rows if r["file"].startswith("memory_probe_" + size)]
    assert len(group) == 3 and all(r["status"] == "complete" for r in group)
    medians[size] = statistics.median(r["max_rss_bytes"] for r in group)
slope = (medians["large"] - medians["small"]) / (4194304 - 4096)
print(f"Difference of median RSS / difference of guest ranges: {slope:.4f} bytes/byte")
print("Incomplete runs retained in CSV, excluded from calculations.")
