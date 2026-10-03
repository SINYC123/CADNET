#!/usr/bin/env python3
"""Harness behavior on synthetic rows. These rows are not the Oct 2 books."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

import oct2_three_book as gate

ROOT = Path(__file__).resolve().parent.parent
TARGETS = ("-2647.77", "-2208.95", "-2041.95")


class GateTests(unittest.TestCase):
    def test_live_tree_is_blocked_and_prints_no_totals(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "harness" / "oct2_three_book.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, gate.EXIT_BLOCKED, proc.stdout + proc.stderr)
        self.assertIn("RESULT BLOCKED", proc.stdout)
        self.assertIn("computed=NONE", proc.stdout)
        for target in TARGETS:
            self.assertNotIn(target, proc.stdout)
        self.assertIn("packs/oct2/journal_closed/batch_c_4162.jsonl", proc.stdout)
        self.assertIn("packs/oct2/broker_day/day_pnl_20261002.jsonl", proc.stdout)
        self.assertIn("packs/oct2/scorer/inv_price_v3.py", proc.stdout)
        self.assertIn("packs/oct2/bars_sample/bars10s_2026-10-02.csv.gz", proc.stdout)

    def test_manifest_arm_arithmetic_is_consistent(self):
        manifest = gate.load_manifest(ROOT / "harness" / "oct2_three_book_manifest.json")
        arms = manifest["journal_closed"]["expect"]["arms"]
        self.assertEqual(
            sum(Decimal(arms[name]["pnl"]) for name in gate.ARMS),
            Decimal("-2647.77"),
        )

    def test_journal_sum_drops_nvda_intc(self):
        rows = [
            {"arm": "V1", "symbol": "AAA", "pnl": Decimal("10.00")},
            {"arm": "V1", "symbol": "NVDA", "pnl": Decimal("999.00")},
            {"arm": "V2", "symbol": "intc", "pnl": Decimal("-50.00")},
            {"arm": "V2", "symbol": "BBB", "pnl": Decimal("-1.50")},
            {"arm": "V3", "symbol": "CCC", "pnl": Decimal("0.25")},
        ]
        got = gate.sum_journal(rows, {"NVDA", "INTC"})
        self.assertEqual(got["n"], 3)
        self.assertEqual(gate.money(got["pnl"]), "8.75")
        self.assertEqual(got["arms"]["V1"]["n"], 1)

    def test_prebaked_total_fails_schema(self):
        with self.assertRaises(gate.SchemaError):
            gate.sum_journal([{"total": Decimal("-2647.77")}], {"NVDA", "INTC"})

    def test_broker_sum(self):
        got = gate.sum_broker(
            [
                {"symbol": "AAA", "pnl": Decimal("1.10")},
                {"symbol": "BBB", "pnl": Decimal("-2.20")},
            ]
        )
        self.assertEqual(gate.money(got), "-1.10")

    def test_parse_actual_column(self):
        stdout = "day n ACTUAL\nTOTAL        41   -12.50   -3.00\n"
        self.assertEqual(gate.parse_actual(stdout), Decimal("-12.50"))

    def test_remap_rejects_unknown_constants(self):
        with self.assertRaises(gate.SchemaError):
            gate.remap_scorer("BASE=r'C:\\somewhere'\n", Path("/j"), Path("/b"), "C:\\ATC\\x", "C:\\ATC\\y")

    def test_synthetic_journal_fail_shows_computed(self):
        manifest = gate.load_manifest(ROOT / "harness" / "oct2_three_book_manifest.json")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / manifest["journal_closed"]["path"]
            path.parent.mkdir(parents=True)
            path.write_text(
                '{"arm":"V1","symbol":"AAA","pnl":1.00}\n',
                encoding="utf-8",
            )
            results = gate.evaluate(root, manifest)
        journal = results[0]
        self.assertEqual(journal["status"], "FAIL")
        self.assertEqual(journal["computed"], "1.00")
        self.assertNotIn("-2647.77", journal["computed"])

    def test_hash_mismatch_does_not_run(self):
        manifest = json.loads((ROOT / "harness" / "oct2_three_book_manifest.json").read_text())
        manifest["scorer_actual"]["inputs"] = []
        manifest["scorer_actual"]["scorer"]["bytes"] = 4
        manifest["scorer_actual"]["scorer"]["sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / manifest["scorer_actual"]["scorer"]["path"]
            path.parent.mkdir(parents=True)
            path.write_text("nope", encoding="utf-8")
            # satisfy the other two books as missing
            results = gate.evaluate(root, manifest)
        scorer = [row for row in results if row["book"] == "scorer_actual"][0]
        self.assertEqual(scorer["status"], "FAIL")
        self.assertEqual(scorer["computed"], "NONE")
        self.assertIn("hash", scorer["detail"])

    def test_synthetic_pack_pass_uses_constructed_rows(self):
        """PASS path only. Symbols AAA/BBB/CCC are not Oct 2 trades."""
        manifest = json.loads((ROOT / "harness" / "oct2_three_book_manifest.json").read_text())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_journal(root, manifest)
            self._write_broker(root, manifest)
            self._write_fake_scorer_tree(root, manifest)
            results = gate.evaluate(root, manifest)
        self.assertEqual([row["status"] for row in results], ["PASS", "PASS", "PASS"])
        self.assertEqual(results[2]["computed"], "-2041.95")

    def _write_journal(self, root: Path, manifest: dict) -> None:
        arms = manifest["journal_closed"]["expect"]["arms"]
        lines = []
        for arm in gate.ARMS:
            count = arms[arm]["n"]
            lines.append('{"arm":"%s","symbol":"AAA","pnl":%s}' % (arm, arms[arm]["pnl"]))
            for _ in range(count - 1):
                lines.append('{"arm":"%s","symbol":"BBB","pnl":0.00}' % arm)
        path = root / manifest["journal_closed"]["path"]
        path.parent.mkdir(parents=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _write_broker(self, root: Path, manifest: dict) -> None:
        path = root / manifest["broker_day"]["path"]
        path.parent.mkdir(parents=True)
        path.write_text(
            '{"symbol":"AAA","pnl":-2000.00}\n{"symbol":"BBB","pnl":-208.95}\n',
            encoding="utf-8",
        )

    def _write_fake_scorer_tree(self, root: Path, manifest: dict) -> None:
        book = manifest["scorer_actual"]
        script = (
            "BASE=r'C:\\ATC\\claude_harness\\inv_20261002'\n"
            "BARS=r'C:\\ATC\\claude_harness\\cf12_20261002\\data'\n"
            "print('TOTAL        41   -2041.95   0   0')\n"
        )
        scorer = root / book["scorer"]["path"]
        scorer.parent.mkdir(parents=True)
        scorer.write_text(script, encoding="utf-8")
        raw = script.encode()
        book["scorer"]["bytes"] = len(raw)
        book["scorer"]["sha256"] = hashlib.sha256(raw).hexdigest()
        for spec in book["inputs"]:
            path = root / spec["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            blob = b"synthetic\n"
            path.write_bytes(blob)
            spec["bytes"] = len(blob)
            spec["sha256"] = hashlib.sha256(blob).hexdigest()


if __name__ == "__main__":
    unittest.main()
