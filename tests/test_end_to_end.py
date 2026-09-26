import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class EndToEndWorkflowTests(unittest.TestCase):
    def build_repo(self, temp_root: Path):
        shutil.copytree(ROOT / "system", temp_root / "system")
        shutil.copytree(ROOT / "schemas", temp_root / "schemas")

        policy = load(temp_root / "system/policy.json")
        for cfg in policy["artifact_types"].values():
            (temp_root / cfg["directory"]).mkdir(parents=True, exist_ok=True)
        (temp_root / "corpus/archive").mkdir(parents=True, exist_ok=True)

        ev = load(ROOT / "templates/evidence-packet.json")
        pa = load(ROOT / "templates/pull-anecdote.json")
        pp = load(ROOT / "templates/pull-pattern.json")
        fq = load(ROOT / "templates/falsification-item.json")
        dh = load(ROOT / "templates/demand-hypothesis.json")

        # Exercise the actual promotion gate.
        pp["state"] = "supported"
        pp["reason_for_state"] = "Synthetic fixture survived one resolved falsification test."
        fq["status"] = "resolved"
        fq["resolution"] = "Synthetic result did not disconfirm the pattern."
        dh["status"] = "candidate"

        objects = [
            ("evidence", ev, "evidence_id"),
            ("anecdote", pa, "anecdote_id"),
            ("pattern", pp, "pattern_id"),
            ("falsification", fq, "item_id"),
            ("hypothesis", dh, "hypothesis_id"),
        ]
        for kind, obj, id_field in objects:
            directory = temp_root / policy["artifact_types"][kind]["directory"]
            (directory / f"{obj[id_field]}.json").write_text(json.dumps(obj, indent=2), encoding="utf-8")

        return policy, pp

    def run_validator(self, temp_root):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_corpus.py"), "--root", str(temp_root)],
            text=True,
            capture_output=True,
        )

    def test_full_chain_validates_and_indexes(self):
        with tempfile.TemporaryDirectory() as td:
            temp_root = Path(td)
            self.build_repo(temp_root)

            result = self.run_validator(temp_root)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

            generate = subprocess.run(
                [sys.executable, str(ROOT / "scripts/generate_index.py"), "--root", str(temp_root)],
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, generate.returncode, generate.stdout + generate.stderr)

            check = subprocess.run(
                [sys.executable, str(ROOT / "scripts/generate_index.py"), "--root", str(temp_root), "--check"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, check.returncode, check.stdout + check.stderr)
            index = (temp_root / "corpus/INDEX.md").read_text(encoding="utf-8")
            self.assertIn("EV-20260926-a1b2c3", index)
            self.assertIn("DH-20260926-a1b2c3", index)

    def test_demand_hypothesis_cannot_precede_supported_pattern(self):
        with tempfile.TemporaryDirectory() as td:
            temp_root = Path(td)
            policy, _ = self.build_repo(temp_root)
            pp_path = temp_root / policy["artifact_types"]["pattern"]["directory"] / "PP-20260926-a1b2c3.json"
            pp = load(pp_path)
            pp["state"] = "candidate"
            pp_path.write_text(json.dumps(pp, indent=2), encoding="utf-8")

            result = self.run_validator(temp_root)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("E021", result.stdout)


if __name__ == "__main__":
    unittest.main()
