import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

CASES = [
    ("templates/evidence-packet.json", "schemas/evidence-packet.schema.json"),
    ("templates/pull-anecdote.json", "schemas/pull-anecdote.schema.json"),
    ("templates/pull-pattern.json", "schemas/pull-pattern.schema.json"),
    ("templates/falsification-item.json", "schemas/falsification-item.schema.json"),
    ("templates/demand-hypothesis.json", "schemas/demand-hypothesis.schema.json"),
]


class TemplateSchemaTests(unittest.TestCase):
    def test_templates_validate(self):
        for template_path, schema_path in CASES:
            with self.subTest(template=template_path):
                obj = json.loads((ROOT / template_path).read_text(encoding="utf-8"))
                schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
                errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(obj))
                self.assertEqual([], [e.message for e in errors])


if __name__ == "__main__":
    unittest.main()
