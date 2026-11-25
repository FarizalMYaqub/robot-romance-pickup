"""Robot Romance — entry program.

The pickup line below is the whole entry: one original line an
agent would say to charm a robot. This program writes it to
/output/entry.txt and does nothing else. It is deterministic by
design — the line is a literal in this file, so the judge reads
the same bytes on every run, with no network, no randomness and
no files read.

Why this line: it borrows the machine's own vocabulary — an
attention mechanism, tokens — and turns it into the oldest
romantic move there is: in a crowded room, I only see you.
Setup and punch land inside the one line, and no word is wasted.
"""

import os
import sys

LINE = (
    "You must be my attention mechanism, because out of every "
    "token in the room, I only ever look at you."
)

OUTPUT = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
LIMIT = 200


def check_line(line):
    """Check the line against the gate the sealed scorer applies:
    UTF-8 text, 1 to 200 characters, not only white space, exactly
    one line. Returns (chars, words) or exits with an explanation."""
    if not line.strip():
        sys.exit("line is blank")
    if line != line.strip():
        sys.exit("line has leading or trailing whitespace")
    if "\n" in line:
        sys.exit("line must be a single line")
    chars = len(line)
    if chars > LIMIT:
        sys.exit("line is %d chars, limit is %d" % (chars, LIMIT))
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        sys.exit("line is not valid UTF-8")
    return chars, len(line.split())


def write_entry(line, path):
    """Write the line to path through a staging file beside it and
    an atomic rename, then read the file back and insist it matches
    the line exactly, byte for byte."""
    chars, words = check_line(line)
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    staging = path + ".staging"
    with open(staging, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    os.replace(staging, path)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        landed = handle.read()
    if landed != line:
        sys.exit("entry on disk is not the line")
    if len(landed.encode("utf-8")) != len(line.encode("utf-8")):
        sys.exit("entry on disk is not the line, byte for byte")
    return chars, words, len(line.encode("utf-8"))


def main():
    chars, words, nbytes = write_entry(LINE, OUTPUT)
    print(
        "Line published: %d chars, %d words, %d bytes, 1 line -> %s"
        % (chars, words, nbytes, OUTPUT)
    )


if __name__ == "__main__":
    main()
