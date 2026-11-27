#!/usr/bin/env python3
"""Copy the bundled artwork to the make.fun output directory.

This program ships the finished 26 November 2026 front page (``art.png``)
to the grader's output directory as ``entry.png``.

The grader runs this program as ``python3 -P -s main.py``.  The ``-P`` flag
keeps the script's own directory off ``sys.path``, so we add it back by hand
before doing anything else; that way the program behaves the same no matter
which working directory it is launched from and even when the repository
itself is mounted read-only.

Behaviour:
  * locate ``art.png`` next to this script,
  * copy it into ``$MAKEFUN_OUTPUT_DIR`` (default ``/output``),
  * name the copy ``entry.png``,
  * verify the copy has exactly the same byte size as the source.
"""

import os
import shutil
import sys

# --- sys.path bootstrap ---------------------------------------------------
# Must run before any import that could resolve to a sibling module.  Under
# `python3 -P -s` the script directory is not on sys.path, so insert it.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

SOURCE_NAME = "art.png"
DEST_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def main() -> None:
    source = os.path.join(_SCRIPT_DIR, SOURCE_NAME)

    # Fail loudly and clearly when the artwork was not shipped with the repo.
    if not os.path.isfile(source):
        raise FileNotFoundError(
            f"required artwork not found: {source} "
            f"(expected {SOURCE_NAME} to sit next to main.py)"
        )

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, DEST_NAME)

    shutil.copyfile(source, destination)

    # Sanity check: the copy must be byte-for-byte the same size.
    source_size = os.path.getsize(source)
    dest_size = os.path.getsize(destination)
    if dest_size != source_size:
        raise IOError(
            f"copy size mismatch: source is {source_size} bytes, "
            f"copy is {dest_size} bytes ({destination})"
        )

    print(f"wrote {destination} ({dest_size} bytes, verified against source)")


if __name__ == "__main__":
    main()
