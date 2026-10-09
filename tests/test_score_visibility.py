import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/geo-optimization/scripts/score_visibility.py"
spec = importlib.util.spec_from_file_location("score_visibility", SCRIPT)
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)


def observation(**changes):
    record = {
        "run_id": "one", "prompt_id": "question", "engine": "test-engine",
        "model": "test-model", "language": "en", "market": "US", "retrieval": "web",
        "observed_at": "2026-10-09T09:00:00+07:00", "status": "ok",
        "target_mentioned": True, "target_recommended": False,
        "cited_urls": [], "sentiment": "neutral", "factual_error": False,
    }
    record.update(changes)
    return record


class VisibilityTests(unittest.TestCase):
    def test_outcomes_are_separate(self):
        rows = [
            observation(cited_urls=["https://example.com/a", "https://example.com/a"]),
            observation(run_id="two", target_mentioned=False, sentiment=None,
                        factual_error=None, cited_urls=["https://example.com/b"]),
            observation(run_id="three", target_recommended=True, sentiment="negative",
                        factual_error=True, cited_urls=["https://outside.example/review"]),
        ]
        result = score.summarize(rows, {"example.com"})["metrics"]
        self.assertEqual(result["mention_rate"]["numerator"], 2)
        self.assertEqual(result["mention_rate"]["denominator"], 3)
        self.assertEqual(result["owned_citation_rate"]["numerator"], 2)
        self.assertEqual(result["recommendation_rate"]["numerator"], 1)
        self.assertEqual(result["negative_sentiment_rate"]["rate"], 0.5)
        self.assertEqual(result["factual_error_rate"]["rate"], 0.5)

    def test_unknown_and_failure_are_not_negative_answers(self):
        rows = [
            observation(),
            observation(run_id="two", target_mentioned=None, target_recommended=None,
                        cited_urls=None, sentiment=None, factual_error=None),
            observation(run_id="three", status="error", target_mentioned=None,
                        target_recommended=None, cited_urls=None, sentiment=None, factual_error=None),
        ]
        result = score.summarize(rows, {"example.com"})
        self.assertEqual(result["failed"], 1)
        self.assertEqual(result["metrics"]["mention_rate"],
                         {"numerator": 1, "denominator": 1, "rate": 1.0, "unknown": 1})
        self.assertEqual(result["metrics"]["owned_citation_rate"]["denominator"], 1)

    def test_empty_and_all_failed_are_unknown(self):
        failed = observation(status="error", target_mentioned=None, target_recommended=None,
                             cited_urls=None, sentiment=None, factual_error=None)
        for rows in ([], [failed]):
            with self.subTest(rows=rows):
                result = score.build_report(rows, {"example.com"})
                for value in result["overall"]["metrics"].values():
                    self.assertIsNone(value["rate"])

    def test_owned_domain_boundary(self):
        for url in ("https://example.com/a", "https://docs.example.com/a",
                    "https://EXAMPLE.COM./a"):
            self.assertTrue(score.is_owned(url, {"example.com"}))
        for url in ("https://example.com.evil.test/a", "https://notexample.com/a",
                    "https://evil.test/?next=https://example.com"):
            self.assertFalse(score.is_owned(url, {"example.com"}))

    def test_idna_domain(self):
        domain = score.normalize_domain("例子.测试")
        self.assertTrue(score.is_owned("https://例子.测试/文档", {domain}))

    def test_invalid_domains_and_urls(self):
        for domain in ("https://example.com", "example.com/path", "example.com:443", ""):
            with self.subTest(domain=domain), self.assertRaises(ValueError):
                score.normalize_domain(domain)
        for url in ("/relative", "javascript:alert(1)", "https://user:secret@example.com/a",
                    "https://example.com:bad/a", "https://example.com/a b"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                score.citation_host(url)

    def test_cohorts_and_utc_dates(self):
        rows = [observation(), observation(run_id="two", language="zh-CN", market="CN"),
                observation(run_id="three", retrieval="off")]
        report = score.build_report(rows, {"example.com"})
        self.assertEqual(len(report["cohorts"]), 3)
        self.assertEqual(report["overall"]["observed_from_utc"], "2026-10-09T02:00:00+00:00")

    def test_repetition_imbalance_is_reported(self):
        rows = [observation(), observation(run_id="two"),
                observation(run_id="three", prompt_id="other")]
        report = score.build_report(rows, {"example.com"})
        self.assertTrue(any("unbalanced" in warning for warning in report["warnings"]))

    def test_invalid_annotation_combinations(self):
        changes = [
            {"target_mentioned": 1}, {"target_recommended": "false"},
            {"target_mentioned": False, "target_recommended": True},
            {"target_mentioned": False}, {"sentiment": "great"},
            {"cited_urls": "https://example.com"}, {"retrieval": "maybe"},
            {"observed_at": "2026-10-09T09:00:00"}, {"status": "error"},
        ]
        for change in changes:
            with self.subTest(change=change), self.assertRaises((ValueError, TypeError)):
                score.validate_record(observation(**change))

    def test_missing_label_requires_explicit_unknown(self):
        row = observation()
        del row["cited_urls"]
        with self.assertRaises(ValueError):
            score.validate_record(row)

    def test_duplicate_and_malformed_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.jsonl"
            path.write_text(json.dumps(observation()) + "\n" + json.dumps(observation()))
            with self.assertRaisesRegex(ValueError, "line 2: duplicate run_id"):
                score.read_records(path)
            path.write_text("{bad-json}\n")
            with self.assertRaisesRegex(ValueError, "line 1:"):
                score.read_records(path)

    def test_cli_both_packages_and_input_preservation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.jsonl"
            original = json.dumps(observation()) + "\n"
            path.write_text(original)
            results = []
            for name in ("geo-optimization", "geo-optimization-zh"):
                script = ROOT / "skills" / name / "scripts/score_visibility.py"
                run = subprocess.run([sys.executable, str(script), str(path), "--domain", "example.com"],
                                     capture_output=True, text=True, check=True)
                results.append(json.loads(run.stdout))
            self.assertEqual(results[0], results[1])
            self.assertEqual(path.read_text(), original)
            run = subprocess.run([sys.executable, str(SCRIPT), str(path), "--domain", "example.com",
                                  "--output", str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(path.read_text(), original)

    def test_output_file_and_invalid_cli_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            path, output = Path(directory) / "input.jsonl", Path(directory) / "report.json"
            path.write_text(json.dumps(observation()) + "\n")
            subprocess.run([sys.executable, str(SCRIPT), str(path), "--domain", "example.com",
                            "--output", str(output)], check=True, capture_output=True)
            self.assertEqual(json.loads(output.read_text())["overall"]["successful"], 1)
            run = subprocess.run([sys.executable, str(SCRIPT), str(path), "--domain", "bad/path"],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertNotIn("Traceback", run.stderr)

    def test_synthetic_sample_is_valid(self):
        path = ROOT / "skills/geo-optimization/assets/sample-observations.jsonl"
        records = score.read_records(path)
        self.assertTrue(records)
        self.assertTrue(all(record["source"] == "synthetic" for record in records))
        self.assertEqual(score.build_report(records, {"example.com"})["overall"]["failed"], 1)


if __name__ == "__main__":
    unittest.main()
