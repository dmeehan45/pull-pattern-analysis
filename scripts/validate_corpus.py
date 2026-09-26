#!/usr/bin/env python3
"""Validate the live analytical corpus.

Mechanical checks intentionally cover only rules that can be enforced
reliably. Semantic truth remains a review problem, but malformed,
duplicated, unlinked, overgrown, or illegally promoted artifacts should
not enter the working set silently.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    print("ERROR E000: jsonschema is not installed. Run: pip install -r requirements-dev.txt")
    sys.exit(2)


IGNORED_NAMES = {"README.md", "AGENTS.md", ".gitkeep", "INDEX.md"}


def words(value) -> int:
    if isinstance(value, str):
        return len(re.findall(r"\b\w+\b", value))
    if isinstance(value, list):
        return sum(words(v) for v in value)
    if isinstance(value, dict):
        return sum(words(v) for v in value.values())
    return 0


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def iso_date(value):
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, code, message):
        self.errors.append((code, message))

    def warn(self, code, message):
        self.warnings.append((code, message))

    def print(self):
        for code, message in self.errors:
            print(f"ERROR {code}: {message}")
        for code, message in self.warnings:
            print(f"WARN  {code}: {message}")
        print(f"\nCorpus validation: {len(self.errors)} error(s), {len(self.warnings)} warning(s).")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    report = Report()

    policy_path = root / "system/policy.json"
    if not policy_path.exists():
        report.error("E001", "system/policy.json is missing")
        report.print()
        return 1

    try:
        policy = load_json(policy_path)
    except Exception as exc:
        report.error("E002", f"cannot parse system/policy.json: {exc}")
        report.print()
        return 1

    artifact_cfg = policy["artifact_types"]
    schemas = {}
    records = {}
    records_by_kind = defaultdict(dict)
    paths_by_id = {}

    # Validate schemas before trusting them.
    for kind, cfg in artifact_cfg.items():
        schema_path = root / cfg["schema"]
        try:
            schema = load_json(schema_path)
            Draft202012Validator.check_schema(schema)
            schemas[kind] = schema
        except Exception as exc:
            report.error("E003", f"invalid schema {cfg['schema']}: {exc}")

    # Corpus top-level boundary.
    corpus = root / "corpus"
    corpus.mkdir(exist_ok=True)
    allowed = set(policy.get("corpus_allowed_top_level", []))
    for child in corpus.iterdir():
        if child.name not in allowed:
            report.error("E004", f"unexpected corpus top-level path: {child.relative_to(root)}")

    active_files = []
    curated_words = 0

    for kind, cfg in artifact_cfg.items():
        directory = root / cfg["directory"]
        if not directory.exists():
            report.warn("W001", f"artifact directory missing: {cfg['directory']}")
            continue

        # Only JSON is canonical inside live artifact directories.
        for p in directory.rglob("*"):
            if p.is_dir() or p.name in IGNORED_NAMES:
                continue
            if p.suffix != ".json":
                report.error("E005", f"non-JSON canonical artifact in {p.relative_to(root)}")
                continue

            active_files.append(p)
            try:
                obj = load_json(p)
            except Exception as exc:
                report.error("E006", f"{p.relative_to(root)} is not valid JSON: {exc}")
                continue

            if kind in schemas:
                validator = Draft202012Validator(schemas[kind], format_checker=FormatChecker())
                for err in sorted(validator.iter_errors(obj), key=lambda e: list(e.absolute_path)):
                    where = ".".join(str(x) for x in err.absolute_path) or "<root>"
                    report.error("E007", f"{p.relative_to(root)} schema violation at {where}: {err.message}")

            id_field = cfg["id_field"]
            artifact_id = obj.get(id_field)
            if not artifact_id:
                continue

            if artifact_id in set(policy.get("reserved_example_ids", [])):
                report.error("E035", f"{artifact_id} is a reserved template/example ID; generate a new collision-resistant ID")

            if artifact_id in records:
                report.error("E008", f"duplicate artifact ID {artifact_id}: {p.relative_to(root)} and {paths_by_id[artifact_id].relative_to(root)}")
            else:
                records[artifact_id] = obj
                records_by_kind[kind][artifact_id] = obj
                paths_by_id[artifact_id] = p

            if not str(artifact_id).startswith(cfg["prefix"]):
                report.error("E009", f"{artifact_id} does not use required prefix {cfg['prefix']}")

            if p.stem != artifact_id:
                report.error("E010", f"filename must equal stable ID: {p.relative_to(root)} should be {artifact_id}.json")

            if kind == "evidence":
                packet_words = words(obj)
                curated_words += packet_words
                if packet_words > cfg.get("max_words", 800):
                    report.error("E011", f"{artifact_id} has ~{packet_words} words; limit is {cfg.get('max_words', 800)}")
                if len(obj.get("excerpts", [])) > policy["working_set_limits"]["evidence_packet_excerpts"]:
                    report.error("E012", f"{artifact_id} has too many excerpts")
    # Working-set word budget is intentionally based on curated evidence,
    # not downstream interpretations.
    
    # Include archived IDs so historical links stay resolvable.
    archive = corpus / "archive"
    if archive.exists():
        for p in archive.rglob("*.json"):
            try:
                obj = load_json(p)
            except Exception as exc:
                report.error("E013", f"archived artifact {p.relative_to(root)} is invalid JSON: {exc}")
                continue
            found = None
            for cfg in artifact_cfg.values():
                candidate = obj.get(cfg["id_field"])
                if candidate and candidate.startswith(cfg["prefix"]):
                    found = candidate
                    break
            if found:
                if found in records:
                    # Same ID may not exist active and archived simultaneously.
                    report.error("E014", f"artifact ID {found} exists in both active corpus and archive")
                else:
                    records[found] = obj
                    paths_by_id[found] = p

    # Working-set boundaries.
    evidence_count = len(records_by_kind["evidence"])
    if evidence_count > policy["working_set_limits"]["evidence_packets"]:
        report.error("E015", f"active evidence packet count {evidence_count} exceeds working-set limit {policy['working_set_limits']['evidence_packets']}")
    if curated_words > policy["working_set_limits"]["curated_words"]:
        report.error("E016", f"active curated corpus ~{curated_words} words exceeds working-set limit {policy['working_set_limits']['curated_words']}")

    # Duplicate source fingerprints.
    fingerprints = defaultdict(list)
    for ev_id, ev in records_by_kind["evidence"].items():
        fp = ev.get("source_fingerprint")
        if fp:
            fingerprints[fp].append(ev_id)
    for fp, ids in fingerprints.items():
        if len(ids) > 1:
            supersession_pairs = {(records_by_kind["evidence"][i].get("supersedes"), i) for i in ids}
            linked = any(a in ids and b in ids for a, b in supersession_pairs if a)
            if linked:
                report.warn("W002", f"source fingerprint {fp!r} appears in superseding evidence packets: {ids}")
            else:
                report.error("E017", f"duplicate source fingerprint {fp!r}: {ids}")

    # Deployment privacy boundary.
    if policy.get("deployment_mode") == "public_framework":
        for ev_id, ev in records_by_kind["evidence"].items():
            if ev.get("privacy_state") not in {"public_safe", "redacted"}:
                report.error("E027", f"{ev_id} privacy_state={ev.get('privacy_state')!r} is not allowed in public_framework mode")

    # Explore handoffs are deliberately compact and downstream of a DH.
    handoff_dir = root / "handoffs/explore"
    if handoff_dir.exists():
        for p in handoff_dir.rglob("*"):
            if p.is_dir() or p.name == "README.md":
                continue
            if p.suffix != ".md":
                report.error("E028", f"Explore handoff must be Markdown: {p.relative_to(root)}")
                continue
            text_value = p.read_text(encoding="utf-8")
            count = words(text_value)
            max_words = policy["working_set_limits"].get("explore_handoff_words", 2500)
            if count > max_words:
                report.error("E029", f"{p.relative_to(root)} has ~{count} words; Explore handoff limit is {max_words}")
            dh_refs = set(re.findall(r"DH-[0-9]{8}-[A-Za-z0-9]{6,}", text_value))
            if not dh_refs:
                report.error("E030", f"{p.relative_to(root)} must reference at least one demand hypothesis ID")
            for dh_ref in dh_refs:
                if dh_ref not in records:
                    report.error("E031", f"{p.relative_to(root)} references missing demand hypothesis {dh_ref}")
                    continue
                dh_obj = records_by_kind["hypothesis"].get(dh_ref)
                if dh_obj and (
                    dh_obj.get("impact_state") != "current"
                    or dh_obj.get("status") in {"rejected", "superseded", "stale"}
                ):
                    report.error("E034", f"{p.relative_to(root)} references demand hypothesis {dh_ref} that is not current/usable")
            pp_refs = set(re.findall(r"PP-[0-9]{8}-[A-Za-z0-9]{6,}", text_value))
            for pp_ref in pp_refs:
                if pp_ref not in records:
                    report.error("E033", f"{p.relative_to(root)} references missing PULL pattern {pp_ref}")

    def require_ref(owner_id, target_id, expected_prefix, field):
        if not target_id:
            return
        if not str(target_id).startswith(expected_prefix):
            report.error("E018", f"{owner_id}.{field} references {target_id}; expected {expected_prefix}*")
        elif target_id not in records:
            report.error("E019", f"{owner_id}.{field} has broken reference to {target_id}")

    # Typed and structural cross-references.
    for kind, by_id in records_by_kind.items():
        for artifact_id, obj in by_id.items():
            for rel in obj.get("relations", []):
                target = rel.get("target_id")
                if target and target not in records:
                    report.error("E020", f"{artifact_id} relation {rel.get('type')} points to missing {target}")

            supersedes = obj.get("supersedes")
            if supersedes:
                expected_prefix = artifact_id.split("-", 1)[0] + "-"
                require_ref(artifact_id, supersedes, expected_prefix, "supersedes")

            if kind == "anecdote":
                for target in obj.get("source_ids", []):
                    require_ref(artifact_id, target, "EV-", "source_ids")
            elif kind == "pattern":
                for target in obj.get("supporting_anecdote_ids", []):
                    require_ref(artifact_id, target, "PA-", "supporting_anecdote_ids")
                for target in obj.get("negative_case_ids", []):
                    require_ref(artifact_id, target, "PA-", "negative_case_ids")
                for target in obj.get("falsification_queue_ids", []):
                    require_ref(artifact_id, target, "FQ-", "falsification_queue_ids")
                for group in obj.get("dependent_case_groups", []):
                    for target in group:
                        require_ref(artifact_id, target, "PA-", "dependent_case_groups")
            elif kind == "hypothesis":
                for target in obj.get("derived_from_pattern_ids", []):
                    require_ref(artifact_id, target, "PP-", "derived_from_pattern_ids")
                    pattern = records_by_kind["pattern"].get(target)
                    if pattern and obj.get("status") in {"candidate", "active"} and pattern.get("state") != "supported":
                        report.error("E021", f"{obj.get('status')} {artifact_id} derives from non-supported pattern {target} ({pattern.get('state')})")
            elif kind == "falsification":
                target = obj.get("pattern_id")
                require_ref(artifact_id, target, "PP-", "pattern_id")
                if obj.get("status") == "resolved" and not obj.get("resolution"):
                    report.error("E022", f"resolved falsification item {artifact_id} requires a non-empty resolution")

    # Current downstream objects may not silently depend on stale/unreviewed upstreams.
    for pattern_id, pattern in records_by_kind["pattern"].items():
        if pattern.get("impact_state") == "current":
            for pa_id in pattern.get("supporting_anecdote_ids", []) + pattern.get("negative_case_ids", []):
                pa = records_by_kind["anecdote"].get(pa_id)
                if pa and pa.get("impact_state") in {"needs_review", "stale"}:
                    report.error("E023", f"{pattern_id} is current but linked anecdote {pa_id} is {pa.get('impact_state')}")
            for fq_id in pattern.get("falsification_queue_ids", []):
                fq = records_by_kind["falsification"].get(fq_id)
                if fq and fq.get("impact_state") in {"needs_review", "stale"}:
                    report.error("E032", f"{pattern_id} is current but linked falsification item {fq_id} is {fq.get('impact_state')}")

    for dh_id, dh in records_by_kind["hypothesis"].items():
        if dh.get("impact_state") == "current":
            for pp_id in dh.get("derived_from_pattern_ids", []):
                pp = records_by_kind["pattern"].get(pp_id)
                if pp and pp.get("impact_state") in {"needs_review", "stale"}:
                    report.error("E024", f"{dh_id} is current but source pattern {pp_id} is {pp.get('impact_state')}")
        due = iso_date(dh.get("next_commitment_by"))
        if due and due < date.today() and dh.get("status") == "active":
            report.warn("W003", f"{dh_id} next_commitment_by {due.isoformat()} has passed; reconcile or revalidate")

    # Supported patterns should show evidence of challenge rather than pure promotion.
    for pp_id, pp in records_by_kind["pattern"].items():
        if pp.get("state") == "supported":
            fq_ids = pp.get("falsification_queue_ids", [])
            resolved = [fid for fid in fq_ids if records_by_kind["falsification"].get(fid, {}).get("status") == "resolved"]
            if not fq_ids:
                report.error("E025", f"supported pattern {pp_id} has no falsification queue items")
            elif not resolved:
                report.error("E026", f"supported pattern {pp_id} has no resolved falsification item")

    report.print()
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
