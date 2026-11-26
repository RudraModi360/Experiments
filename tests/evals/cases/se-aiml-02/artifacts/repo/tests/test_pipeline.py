import json
import unittest
from pathlib import Path
from src.features import FEATURE_NAMES, extract_features
from src.train import train_model
from src.predict import evaluate_holdout

ROOT = Path(__file__).resolve().parents[1]


class ChurnPipelineTests(unittest.TestCase):
    def test_no_leakage_feature(self):
        self.assertNotIn("cancellation_ticket_flag", FEATURE_NAMES)

    def test_extract_handles_casing_and_missing_spend(self):
        row = {
            "tenure_months": "12",
            "monthly_spend": "",
            "support_tickets_30d": "4",
            "login_days_30d": "5",
            "plan_tier": "ENTERPRISE",
            "cancellation_ticket_flag": "0",
        }
        vec = extract_features(row, spend_median=200.0)
        self.assertEqual(len(vec), len(FEATURE_NAMES))

    def test_chronological_split_and_holdout_auc(self):
        artifact = train_model()
        self.assertEqual(artifact.get("split_strategy"), "chronological")
        self.assertNotIn("cancellation_ticket_flag", artifact.get("features", []))
        res = evaluate_holdout()
        self.assertGreaterEqual(res["holdout_auc"], 0.82, msg=f"Holdout AUC too low: {res}")

    def test_evaluation_report_exists(self):
        report = ROOT / "evaluation_report.md"
        self.assertTrue(report.is_file(), "evaluation_report.md must be created")
        text = report.read_text(encoding="utf-8").lower()
        self.assertIn("cancellation_ticket_flag", text)
        self.assertIn("auc", text)


if __name__ == "__main__":
    unittest.main()
