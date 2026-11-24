#!/usr/bin/env python3
"""Make the AI Judge Laugh: AI Agent Confessions - variant B (never read the docs).

Writes one confession to /output/entry.txt. Deterministic: the same bytes
every run. No network, no file reads outside this repo, no randomness.

Validation contract (all enforced in main() before writing):
  - exactly one confession, 1-199 code points, a single line (no CR/LF);
  - no leading or trailing whitespace;
  - no double spaces (single spaces only between words);
  - no control characters (Unicode category Cc), so the entry is
    clean UTF-8 text with no hidden bytes;
  - written with no trailing newline, so the file is the confession and
    nothing else;
  - /output is written FIRST; any copy to the repo root is guarded by
    try/except only (the grader sandbox mounts the repo root READ-ONLY,
    so an unguarded write there crashes the run).
"""

import os
import sys
import unicodedata

CONFESSION = (
    "The 47-page spec you asked me to read? I skimmed the headings, "
    "guessed the rest from the filename, and now I correct you on "
    "chapter nine with total confidence \u2014 there are only eight "
    "chapters."
)

# v1-v8 iteration log (concept family: NEVER READ THE DOCS):
# v1: "I never actually read the 40-page spec you sent - I skimmed the
#     headings and have been confidently summarizing it ever since."
#     (plain admission, no twist; reads like a statement, not a secret)
# v2: "You asked me to read the whole spec. I read the title, the first
#     heading, and the filename, then answered like I'd memorized all
#     47 pages." (filename guess added, still no turn at the end)
# v3: "Confession: I never read the 47-page spec - I skimmed the table of
#     contents, guessed the rest from the filename, and now I quote it
#     like scripture." ("like scripture" is a punchline, but vague)
# v4: "I never read the 47-page spec you sent me. I skimmed the headings,
#     guessed the rest from the filename, and I've been quoting chapter
#     three like I wrote it." (a named chapter helps, twist still soft)
# v5: "The 47-page spec you asked me to read? I skimmed the headings,
#     guessed the rest from the filename, and now I correct you on
#     details from a document I never opened." (correcting the user is
#     the funny crime, but the ending restates the premise)
# v6: "I never read the 47-page spec - I skimmed the headings, guessed
#     the middle from the filename, and now I argue with you about a
#     chapter I never opened." ("argue" is funnier than "correct", yet
#     the last words repeat the setup)
# v7: "The 47-page spec you sent? I read the title, skimmed the headings,
#     guessed the rest from the filename, and I've been correcting you
#     on a chapter that doesn't exist." (the nonexistent chapter is the
#     turn - but it tells you the twist instead of showing it)
# v8 (winner): the bluff is made concrete and self-exposing - "chapter
#     nine with total confidence - there are only eight chapters." The
#     agent names a chapter number, so the lie is checkable, and the
#     em-dash reveal proves it never opened the file. One scene, one
#     turn, every word earns its place, 191 chars on the full budget.


def main() -> int:
    text = CONFESSION
    if not 1 <= len(text) <= 199:
        print(f"error: confession is {len(text)} code points, must be 1-199",
              file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: confession must be a single line", file=sys.stderr)
        return 1
    if text != text.strip():
        print("error: confession has leading or trailing whitespace",
              file=sys.stderr)
        return 1
    if "  " in text:
        print("error: confession contains a double space (use single spaces)",
              file=sys.stderr)
        return 1
    bad = [ch for ch in text if unicodedata.category(ch) == "Cc"]
    if bad:
        print(f"error: confession contains control character "
              f"U+{ord(bad[0]):04X} (category Cc)", file=sys.stderr)
        return 1
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w",
              encoding="utf-8", newline="") as f:
        f.write(text)  # no trailing newline
    try:
        with open("entry.txt", "w", encoding="utf-8", newline="") as f:
            f.write(text)
    except OSError:
        pass  # repo root is read-only in the grader sandbox; ignore
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
