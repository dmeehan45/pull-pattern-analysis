import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "scripts/validate_change_set.py"


def git(repo, *args):
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


class ChangeSetGuardTests(unittest.TestCase):
    def init_repo(self, root: Path):
        (root / "system").mkdir(parents=True)
        (root / "corpus/evidence").mkdir(parents=True)
        policy = {
            "artifact_types": {
                "evidence": {
                    "directory": "corpus/evidence",
                    "id_field": "evidence_id",
                    "prefix": "EV-"
                }
            },
            "protected_framework_paths": ["AGENTS.md", "system/", "schemas/", "scripts/", ".github/"],
            "framework_change_label": "framework-change"
        }
        (root / "system/policy.json").write_text(json.dumps(policy), encoding="utf-8")
        (root / "AGENTS.md").write_text("rules v1\n", encoding="utf-8")
        git(root, "init", "-q")
        git(root, "config", "user.email", "test@example.com")
        git(root, "config", "user.name", "Test")
        git(root, "add", ".")
        git(root, "commit", "-q", "-m", "base")

    def event_file(self, root: Path, labels=None):
        path = root / "event.json"
        path.write_text(json.dumps({"pull_request": {"labels": [{"name": x} for x in (labels or [])]}}), encoding="utf-8")
        return path

    def run_guard(self, root: Path, base: str, head: str, event: Path):
        return subprocess.run(
            [sys.executable, str(GUARD), "--root", str(root), "--base", base, "--head", head, "--event", str(event)],
            text=True,
            capture_output=True,
        )

    def test_accepted_evidence_cannot_be_mutated(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            self.init_repo(repo)
            ev_path = repo / "corpus/evidence/EV-20260926-a1b2c3.json"
            ev_path.write_text(json.dumps({
                "evidence_id": "EV-20260926-a1b2c3",
                "revision": 1,
                "status": "accepted"
            }), encoding="utf-8")
            git(repo, "add", ".")
            git(repo, "commit", "-q", "-m", "add evidence")
            base = git(repo, "rev-parse", "HEAD")

            obj = json.loads(ev_path.read_text(encoding="utf-8"))
            obj["revision"] = 2
            obj["summary"] = "rewritten"
            ev_path.write_text(json.dumps(obj), encoding="utf-8")
            git(repo, "add", ".")
            git(repo, "commit", "-q", "-m", "mutate evidence")
            head = git(repo, "rev-parse", "HEAD")

            result = self.run_guard(repo, base, head, self.event_file(repo))
            self.assertNotEqual(0, result.returncode)
            self.assertIn("C008", result.stdout)

    def test_protected_framework_change_requires_label(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            self.init_repo(repo)
            base = git(repo, "rev-parse", "HEAD")
            (repo / "AGENTS.md").write_text("rules v2\n", encoding="utf-8")
            git(repo, "add", ".")
            git(repo, "commit", "-q", "-m", "change rules")
            head = git(repo, "rev-parse", "HEAD")

            result = self.run_guard(repo, base, head, self.event_file(repo))
            self.assertNotEqual(0, result.returncode)
            self.assertIn("C001", result.stdout)

            labelled = self.run_guard(repo, base, head, self.event_file(repo, ["framework-change"]))
            self.assertEqual(0, labelled.returncode, labelled.stdout + labelled.stderr)


if __name__ == "__main__":
    unittest.main()
