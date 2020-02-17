#!/usr/bin/env python3
import sys

from python_utils import ROOT, colors


def getopt(opt: str) -> str:
    manifest_path = f"{ROOT}/manifest.sh"
    try:
        for line in open(manifest_path, "r"):
            if line.startswith(f"{opt}="):
                return line.split("=")[-1].strip()
    except FileNotFoundError:
        raise SystemExit(
            f"{colors.red}could not find manifest. please run: "
            f"{colors.green}'./scripts/init.py'{colors.reset}"
        )
    raise SystemExit(f"{colors.red}could not find option {opt!r}{colors.reset}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(f"Usage: {__file__} <opt-name>")
    print(getopt(sys.argv[1]))
    sys.exit(0)
