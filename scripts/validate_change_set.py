#!/usr/bin/env python3
"""Protect corpus history and framework files in a pull-request change set."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def run(*args):
    return subprocess.check_output(args, text=True).strip()


def load_json_text(text, label):
    try:
        return json.loads(text)
    except Exception as exc:
        raise RuntimeError(f"{label} is not valid JSON: {exc}") from exc


def git_json(ref, path):
    try:
        text = run("git", "show", f"{ref}:{path}")
    except subprocess.CalledProcessError:
        return None
    return load_json_text(text, f"{ref}:{path}")


def is_under(path, prefix):
    return path == prefix.rstrip("/") or path.startswith(prefix)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--event")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    os.chdir(root)

    policy = json.loads((root / "system/policy.json").read_text(encoding="utf-8"))
    protected = policy["protected_framework_paths"]
    framework_label = policy["framework_change_label"]
    artifact_dirs = {cfg["directory"]: cfg for cfg in policy["artifact_types"].values()}

    event = {}
    if args.event and Path(args.event).exists():
        event = json.loads(Path(args.event).read_text(encoding="utf-8"))
    labels = {x.get("name") for x in event.get("pull_request", {}).get("labels", [])}

    diff = run("git", "diff", "--name-status", "--find-renames", f"{args.base}...{args.head}")
    changes = []
    for line in diff.splitlines():
        if not line:
            continue
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("R"):
            changes.append((status, parts[1], parts[2]))
        else:
            changes.append((status, parts[1], None))

    errors = []

    protected_changed = []
    for status, old, new in changes:
        candidates = [old] + ([new] if new else [])
        if any(any(is_under(p, pref) for pref in protected) for p in candidates):
            protected_changed.append((status, old, new))

    if protected_changed and framework_label not in labels:
        changed = ", ".join((n or o) for _, o, n in protected_changed[:8])
        errors.append(
            f"C001 protected framework files changed without PR label '{framework_label}': {changed}"
        )

    def artifact_cfg_for(path):
        for directory, cfg in artifact_dirs.items():
            if path.startswith(directory + "/") and path.endswith(".json"):
                return cfg
        return None

    for status, old, new in changes:
        path = new or old
        cfg = artifact_cfg_for(path) or artifact_cfg_for(old)
        if not cfg:
            continue

        if status == "A":
            head_obj = git_json(args.head, path)
            if head_obj and head_obj.get("revision") != 1:
                errors.append(f"C002 new artifact {path} must start at revision 1")
            continue

        if status == "D":
            base_obj = git_json(args.base, old)
            artifact_id = base_obj.get(cfg["id_field"]) if base_obj else None
            if not artifact_id:
                errors.append(f"C003 cannot verify deleted artifact {old}")
                continue
            # Deletion is allowed only if the same stable ID now exists under archive.
            archive_paths = run("git", "ls-tree", "-r", "--name-only", args.head, "corpus/archive").splitlines()
            found = False
            for ap in archive_paths:
                if not ap.endswith(".json"):
                    continue
                obj = git_json(args.head, ap)
                if obj and obj.get(cfg["id_field"]) == artifact_id:
                    found = True
                    break
            if not found:
                errors.append(f"C004 active artifact {artifact_id} cannot be deleted; move it to corpus/archive with history preserved")
            continue

        if status.startswith("R"):
            # Renames are only valid when moving to archive. Stable active paths are ID-addressed.
            if not (new and new.startswith("corpus/archive/")):
                errors.append(f"C005 canonical artifact rename not allowed: {old} -> {new}")
            continue

        if status == "M":
            base_obj = git_json(args.base, old)
            head_obj = git_json(args.head, path)
            if not base_obj or not head_obj:
                errors.append(f"C006 cannot compare revisions for {path}")
                continue

            old_id = base_obj.get(cfg["id_field"])
            new_id = head_obj.get(cfg["id_field"])
            if old_id != new_id:
                errors.append(f"C007 stable ID changed in {path}: {old_id} -> {new_id}")

            # Evidence packets are immutable once accepted.
            if cfg["prefix"] == "EV-" and base_obj.get("status") == "accepted":
                errors.append(f"C008 accepted evidence packet {old_id} is immutable; add a superseding EV artifact instead")
                continue

            old_rev = base_obj.get("revision")
            new_rev = head_obj.get("revision")
            if not isinstance(old_rev, int) or new_rev != old_rev + 1:
                errors.append(f"C009 modified artifact {old_id} must increment revision exactly once ({old_rev} -> {old_rev + 1 if isinstance(old_rev, int) else '?'})")

    if errors:
        for error in errors:
            print("ERROR", error)
        return 1

    print(f"Change-set guard passed ({len(changes)} changed path(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
