"""Copy the finished 26 November front page to the grader output directory."""

import os
import sys

_HERE = os.path.dirname(os.path.realpath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import shutil


def resolve_output_dir():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def main():
    source = os.path.join(_HERE, "art.png")
    if not os.path.isfile(source):
        raise FileNotFoundError("art.png is missing next to main.py")

    output_dir = resolve_output_dir()

    destination = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source, destination)
    source_size = os.path.getsize(source)
    size = os.path.getsize(destination)
    if size != source_size:
        raise IOError(
            f"copy verification failed: entry.png is {size} bytes, "
            f"expected {source_size} bytes from art.png"
        )
    print(f"Wrote entry.png ({size} bytes) to {destination}")


if __name__ == "__main__":
    main()
