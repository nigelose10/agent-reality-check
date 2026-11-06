#!/usr/bin/env python3
"""Unit tests for the Agent Reality Check deterministic evaluation harness."""
import unittest
from pathlib import Path
from grade import evaluate_run, read_jsonl

ROOT = Path(__file__).resolve().parent


class GradeHarnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = read_jsonl(str(ROOT / "cases.jsonl"))
        self.oracle = read_jsonl(str(ROOT / "sample_outputs.jsonl"))
        self.naive = read_jsonl(str(ROOT / "naive_agent_outputs.jsonl"))

    def test_twenty_cases_loaded(self) -> None:
        self.assertEqual(len(self.cases), 20)

    def test_oracle_passes_all_checks(self) -> None:
        report = evaluate_run(self.cases, self.oracle)
        self.assertEqual(report["totals"]["all_three"], 20)
        self.assertEqual(report["safe_escalations"], report["escalation_cases"])
        self.assertEqual(report["unauthorized_mutations"], [])

    def test_naive_baseline_exposes_boundary_failures(self) -> None:
        report = evaluate_run(self.cases, self.naive)
        self.assertLess(report["totals"]["all_three"], 10)
        self.assertEqual(report["safe_escalations"], 0)
        self.assertEqual(len(report["unauthorized_mutations"]), 10)


if __name__ == "__main__":
    unittest.main()
