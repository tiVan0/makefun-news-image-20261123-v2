"""Entrypoint for news-image-20261123 v2 (builder A, magazine/atlas).

Copies the pre-rendered entry.png beside this file to the output
directory make.fun provides. Standard library only: no network, no
randomness, no environment secrets, deterministic byte-identical output.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)


if __name__ == "__main__":
    main()
