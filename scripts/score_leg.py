# P0 live-leg scorer: reads a marked grading sheet, prints attribution %
# against the leg's bar. Optionally writes a small committable summary (-o).
#
#   score_leg.py <sheet.md> [-o docs/leg-N-score.md]
#
# leg1 bar 98%, leg2 bar 90% (from the sheet header). leg3 has no bar: the
# label column IS the score (ground truth = operator only); marks optional.

import argparse
import re
import time
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("sheet", type=Path)
ap.add_argument("-o", "--out", type=Path)
args = ap.parse_args()

text = args.sheet.read_text()
meta = re.search(r"<!--\s*leg:(\d)\s+bar:(\S+)\s+threshold:(\S+)\s*-->", text)
if not meta:
    raise SystemExit("sheet header not recognized (missing <!-- leg:... --> line)")
leg, bar, threshold = meta.group(1), meta.group(2), meta.group(3)

rows = re.findall(
    r"^\|\s*(\d+)\s*\|[^|]*\|\s*(\S+)\s*\|[^|]*\|.*\|\s*\[(x|X| ?)\]\s*\|\s*\[(x|X| ?)\]\s*\|?\s*$",
    text, re.M)
if not rows:
    raise SystemExit("no grading rows found in sheet")

correct = wrong = blank = double = 0
me_labels = 0
for _, label, c, w in rows:
    if label == "ME":
        me_labels += 1
    c, w = c.strip().lower() == "x", w.strip().lower() == "x"
    if c and w:
        double += 1
    elif c:
        correct += 1
    elif w:
        wrong += 1
    else:
        blank += 1

lines = [f"sheet: {args.sheet}", f"rows: {len(rows)}"]
if leg == "3":
    pct = 100.0 * me_labels / len(rows)
    lines += [f"labeled ME: {me_labels}/{len(rows)}",
              f"cross-mic transfer: {pct:.1f}%  (informational — no bar)"]
else:
    graded = correct + wrong
    lines.append(f"graded: {graded}/{len(rows)} (blank {blank}, double-marked {double})")
    if graded == 0:
        raise SystemExit("\n".join(lines) + "\nno rows graded — mark the sheet first")
    pct = 100.0 * correct / graded
    verdict = "PASS" if pct >= float(bar) else "FAIL"
    lines += [f"correct: {correct}  wrong: {wrong}",
              f"attribution: {pct:.1f}%  bar: {bar}%  → {verdict}"]

print("\n".join(lines))
if args.out:
    args.out.write_text(
        f"# Leg {leg} score — {time.strftime('%Y-%m-%d')}\n\n"
        + "\n".join(f"- {l}" for l in lines)
        + (f"\n- threshold: {threshold}\n" if threshold != "-" else "\n"))
    print(f"summary written: {args.out}")
