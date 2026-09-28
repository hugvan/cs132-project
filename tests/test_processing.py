"""Synthetic unit tests. These records are not observations or study data."""

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.process_data import FIELDS, MAP_FIELDS, process, write_csv


class ProcessingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "input.csv"
        self.mapping = self.root / "mapping.csv"
        self.output = self.root / "out"
        write_csv(self.mapping, [{"status": "Test fulfilled", "outcome": "successful", "is_closed": "true", "definition": "Synthetic test mapping only", "source_url": "https://example.com/test"}], MAP_FIELDS)

    def row(self, **changes):
        return dict(dict(tracking_number="SYNTHETIC-001", agency="Test agency", agency_group="NGA", filed_at="2025-01-01T08:00:00+08:00", first_response_at="2025-01-02T20:00:00+08:00", status="Test fulfilled", purpose="Synthetic test", source_url="https://example.com/test", collected_at="2026-01-01"), **changes)

    def run_rows(self, rows):
        write_csv(self.source, rows, FIELDS)
        report = process(self.source, self.mapping, self.output)
        with (self.output / "requests_clean.csv").open(newline="") as handle:
            clean = list(csv.DictReader(handle))
        return report, clean

    def test_elapsed_time_and_mapping(self):
        report, clean = self.run_rows([self.row()])
        self.assertEqual(report["clean_rows"], 1)
        self.assertEqual(clean[0]["first_response_days"], "1.5")
        self.assertEqual(clean[0]["outcome"], "successful")

    def test_missing_reply_and_unknown_status_are_not_zero_or_failure(self):
        _, clean = self.run_rows([self.row(first_response_at="", status="Unreviewed")])
        self.assertEqual(clean[0]["first_response_days"], "")
        self.assertEqual(clean[0]["outcome"], "unknown")
        self.assertEqual(clean[0]["is_closed"], "")

    def test_conflicting_duplicates_all_quarantined(self):
        report, clean = self.run_rows([self.row(), self.row(agency="Different")])
        self.assertEqual(clean, [])
        self.assertEqual(report["quarantined_rows"], 2)

    def test_identical_duplicates_count_once(self):
        report, _ = self.run_rows([self.row(), self.row()])
        self.assertEqual(report["clean_rows"], 1)
        self.assertEqual(report["identical_duplicates_removed"], 1)

    def test_invalid_temporal_order_quarantined(self):
        for changes in [dict(first_response_at="2024-12-31"), dict(collected_at="2024-12-31"), dict(first_response_at="2026-02-01")]:
            with self.subTest(changes=changes):
                report, _ = self.run_rows([self.row(**changes)])
                self.assertEqual(report["quarantined_rows"], 1)

    def test_timezone_sets_study_year_and_allows_later_reply(self):
        report, clean = self.run_rows([self.row(filed_at="2024-12-31T20:00:00Z", first_response_at="2026-01-01")])
        self.assertEqual(report["clean_rows"], 1)
        self.assertTrue(clean[0]["filed_at"].startswith("2025-01-01"))
        report, _ = self.run_rows([self.row(filed_at="2025-12-31T20:00:00Z", first_response_at="")])
        self.assertEqual(report["quarantined_rows"], 1)

    def test_mixed_precision_same_day_is_not_negative(self):
        _, clean = self.run_rows([self.row(first_response_at="2025-01-01")])
        self.assertEqual(clean[0]["first_response_days"], "0")
        self.assertIn("mixed_date_precision", clean[0]["quality_flags"])

    def test_unexpected_fields_rejected(self):
        write_csv(self.source, [], FIELDS + ["requester_name"])
        with self.assertRaises(ValueError):
            process(self.source, self.mapping, self.output)

    def test_invalid_mapping_rejected(self):
        write_csv(self.mapping, [{"status": "Test", "outcome": "pending", "is_closed": "true", "definition": "Synthetic", "source_url": "https://example.com"}], MAP_FIELDS)
        with self.assertRaises(ValueError):
            self.run_rows([self.row()])

    def test_empty_input_not_reported_as_collected(self):
        report, clean = self.run_rows([])
        self.assertEqual(clean, [])
        self.assertFalse(report["size_thresholds"]["100"])

    def test_input_cannot_be_overwritten(self):
        self.source = self.output / "requests_clean.csv"
        self.output.mkdir()
        write_csv(self.source, [self.row()], FIELDS)
        original = self.source.read_bytes()
        with self.assertRaises(ValueError):
            process(self.source, self.mapping, self.output)
        self.assertEqual(self.source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
