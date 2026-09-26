#!/usr/bin/env python3
"""Generate the active corpus navigation index from canonical JSON artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def short(value, n=80):
    value = " ".join(str(value or "").split())
    return value if len(value) <= n else value[: n - 1] + "…"


def render(root: Path) -> str:
    policy = load(root / "system/policy.json")
    sections = []
    total = 0

    labels = {
        "evidence": ("Evidence packets", "summary", "status"),
        "anecdote": ("PULL anecdotes", "project", "impact_state"),
        "pattern": ("PULL patterns", "name", "state"),
        "hypothesis": ("Demand hypotheses", "canonical_statement", "status"),
        "falsification": ("Falsification queue", "target_uncertainty", "status"),
    }

    for kind, cfg in policy["artifact_types"].items():
        title, summary_field, state_field = labels[kind]
        directory = root / cfg["directory"]
        rows = []
        if directory.exists():
            for p in sorted(directory.glob("*.json")):
                obj = load(p)
                artifact_id = obj.get(cfg["id_field"], p.stem)
                summary = short(obj.get(summary_field) or obj.get("project") or obj.get("pattern_claim_at_risk"))
                state = obj.get(state_field) or obj.get("impact_state") or ""
                rel = p.relative_to(root / "corpus")
                rows.append((artifact_id, summary, state, rel.as_posix()))
        total += len(rows)
        lines = [f"## {title} ({len(rows)})", "", "| ID | State | Summary |", "|---|---|---|"]
        for artifact_id, summary, state, rel in rows:
            lines.append(f"| [{artifact_id}](./{rel}) | {state} | {summary} |")
        if not rows:
            lines.append("| — | — | None |")
        sections.append("\n".join(lines))

    return (
        "# Corpus index\n\n"
        "<!-- GENERATED FILE. Run: python scripts/generate_index.py -->\n\n"
        f"Active canonical artifacts: **{total}**\n\n"
        + "\n\n".join(sections)
        + "\n"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    path = root / "corpus/INDEX.md"
    expected = render(root)

    if args.check:
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != expected:
            print("ERROR I001: corpus/INDEX.md is stale. Run: python scripts/generate_index.py")
            return 1
        print("Corpus index is current.")
        return 0

    path.write_text(expected, encoding="utf-8")
    print(f"Wrote {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
