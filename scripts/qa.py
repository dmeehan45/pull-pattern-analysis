#!/usr/bin/env python3
from __future__ import annotations
import subprocess
import sys

COMMANDS = [
    [sys.executable, "-m", "py_compile", "scripts/validate_corpus.py", "scripts/generate_index.py", "scripts/validate_change_set.py"],
    [sys.executable, "scripts/validate_corpus.py", "--root", "."],
    [sys.executable, "scripts/generate_index.py", "--root", ".", "--check"],
]

for cmd in COMMANDS:
    print("+", " ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode:
        raise SystemExit(result.returncode)

print("QA passed.")
