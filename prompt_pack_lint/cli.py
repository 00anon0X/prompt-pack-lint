from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .linter import lint_files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint prompt packs for placeholders, leaked secrets, and missing agent guardrails.")
    parser.add_argument("paths", nargs="+", type=Path, help="Prompt files or directories")
    args = parser.parse_args(argv)
    findings = lint_files(args.paths)
    for finding in findings:
        print(f"{finding.path}:{finding.line}: {finding.code}: {finding.message}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
