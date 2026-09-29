import json
import unittest
from pathlib import Path

from api_compatibility.analysis import compare_documents, review_document, validate_sample
from api_compatibility.report import render_report


ROOT = Path(__file__).resolve().parents[1]


class CompatibilityTests(unittest.TestCase):
    def test_compare_reports_breaking_requirement(self):
        result = compare_documents(str(ROOT / "fixtures/user_v1.json"), str(ROOT / "fixtures/user_v2.json"), resolve=False)
        self.assertTrue(result["valid"])
        self.assertTrue(any(item["kind"] == "required" and item["breaking"] for item in result["changes"]))

    def test_validation_gate(self):
        good = validate_sample(str(ROOT / "fixtures/sample_valid.json"), str(ROOT / "fixtures/user_v2.json"), resolve=False)
        bad = validate_sample(str(ROOT / "fixtures/sample_invalid.json"), str(ROOT / "fixtures/user_v2.json"), resolve=False)
        self.assertTrue(good["valid"])
        self.assertFalse(bad["valid"])

    def test_review_is_harmless(self):
        result = review_document(str(ROOT / "fixtures/user_v1.json"))
        self.assertTrue(result["valid"])
        self.assertEqual(result["properties"], ["id", "name", "status"])

    def test_report_is_deterministic(self):
        result = compare_documents(str(ROOT / "fixtures/user_v1.json"), str(ROOT / "fixtures/user_v2.json"), resolve=False)
        first = render_report(result, "before.json", "after.json")
        second = render_report(result, "before.json", "after.json")
        self.assertEqual(first, second)
        self.assertIn("Compatible: no", first)


if __name__ == "__main__":
    unittest.main()
