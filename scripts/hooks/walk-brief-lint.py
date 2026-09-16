#!/usr/bin/env python3
"""Walk-brief lint -- ADVISOR.md rule 48 and §8 rule 6, as a program.

Rule 48 and §8 rule 6 were both prose when walkrun-4 spent 139 M tokens: its brief
ORDERED the poll ("You watch ORIGIN (poll every 60-90 s)", walkrun-2, inherited by
walkrun-5/-9/-12) and named an Opus coordinator. The seat obeyed its brief. Prose was
never the missing part, so this checks the brief before it can be launched (§8 rule 5:
a brief is on origin BEFORE launch).

Checks only EXPLICIT DECLARATIONS, never prose meaning. Leg COUNT is deliberately not
checked: walkrun-5 states its legs in prose with no table, and walkrun-2 packs eight
legs into a single "live-case-1 ... live-case-8" row, so any row count is wrong on real
briefs. A classifier that guesses is the STATUS-entry mistake repeated; the coordinator's
span stays an advisor judgment.

Usage: walk-brief-lint.py <rev> <path>...   rev "" = the staged index.
Exit 1 on a finding. Override: WALK_BRIEF_OVERRIDE=1.
"""
import os, re, subprocess, sys

POLL = re.compile(r"poll(?:s|ing|ed)?\s+(?:every|origin|the\s+origin)"
                  r"|origin\s+polling|poll\s+the\s+origin", re.I)
YOUARE = re.compile(r"^\s*YOU ARE:(.*)$", re.M)
BIGMODEL = re.compile(r"\b(opus|fable)\b", re.I)
WAKE = re.compile(r"orca terminal wait|^\s*WAKE:", re.I | re.M)
# "never poll origin" is the brief saying the RIGHT thing; only an instruction to poll counts.
NEGATED = re.compile(r"(never|not|no|don'?t|do not|forbidden|avoid|instead of|rather than|"
                     r"stop)\W{0,12}$", re.I)
WALKSTEM = re.compile(r"(^|[-_.])walk([-_.]|$)", re.I)


def is_walk_brief(path):
    b = os.path.basename(path)
    if not b.endswith(".md"):
        return False
    return b.startswith("walk-brief-") or (
        path.startswith("docs/lane-briefs/") and bool(WALKSTEM.search(b[:-3])))


def read(rev, path):
    spec = ("%s:%s" % (rev, path)) if rev else (":%s" % path)
    try:
        return subprocess.run(["git", "show", spec], capture_output=True,
                              check=True).stdout.decode("utf-8", "replace")
    except subprocess.CalledProcessError:
        return None


def check(text):
    out = []
    m = None
    for cand in POLL.finditer(text):
        if NEGATED.search(text[max(0, cand.start() - 30):cand.start()]):
            continue
        m = cand
        break
    if m:
        line = text[:m.start()].count("\n") + 1
        out.append(("poll instruction on line %d: %r" % (line, m.group(0)),
                    "estate ADVISOR.md 8 rule 6: a waiting lane's terminal is re-read at "
                    "most once per 20 min. Wake on the walker's LANE-SIGNAL (its mandated "
                    "last act), then verify origin ONCE with git ls-remote."))
    y = YOUARE.search(text)
    if y:
        big = BIGMODEL.search(y.group(1))
        if big:
            out.append(("coordinator declared as %r" % big.group(1),
                        "estate ADVISOR.md 48: a walk coordinator runs on a machine-read "
                        "model, not Opus/Fable. The Grok legs do the reading that needs a "
                        "big model; the coordinator sends, waits, reads and rolls up."))
    if not WAKE.search(text):
        out.append(("no wake declared",
                    "estate ADVISOR.md 48 / 8 rule 2b: the brief names its wake. Use "
                    "`orca terminal wait --for exit|tui-idle --timeout-ms <ms>` or a line "
                    "beginning `WAKE:` that names the signal the coordinator blocks on."))
    return out


def main(argv):
    if os.environ.get("WALK_BRIEF_OVERRIDE"):
        return 0
    rev, paths = argv[0], argv[1:]
    bad = []
    for p in paths:
        if not is_walk_brief(p):
            continue
        t = read(rev, p)
        if t is None:
            continue
        for finding, why in check(t):
            bad.append((p, finding, why))
    if not bad:
        return 0
    where = " at push" if rev else ""
    print("", file=sys.stderr)
    print("  BLOCKED%s: %d walk-brief defect(s). A brief is launched as written."
          % (where, len(bad)), file=sys.stderr)
    for p, finding, why in bad:
        print("", file=sys.stderr)
        print("    %s" % p, file=sys.stderr)
        print("      %s" % finding, file=sys.stderr)
        print("      %s" % why, file=sys.stderr)
    print("", file=sys.stderr)
    print("  Attribution: walkrun-4, 2026-09-08 -- 270 `orca terminal read` calls in 35",
          file=sys.stderr)
    print("  minutes at a median gap of 3 s, 139,490,678 tokens, because its brief said so.",
          file=sys.stderr)
    print("  Deliberate exception: WALK_BRIEF_OVERRIDE=1 git commit/push ...", file=sys.stderr)
    print("", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
