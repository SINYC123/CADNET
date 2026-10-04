"""Checks for the unarmed exit-owner overlay and the three-book receipt."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import book_receipt
import exit_owner_counterfactual as overlay
import rules_staged as rules

HERE = Path(__file__).resolve().parent


class BookReceiptTest(unittest.TestCase):
    def _write_pack(self, root: Path, *, journal: str, broker: str, actual: str) -> None:
        journal_path = root / "journal_closed" / "batch_c_4162.jsonl"
        broker_path = root / "broker_day" / "day_pnl_20261002.jsonl"
        scorer_path = root / "journals" / "inv_price_v3_2026-10-02_2026-10-02.json"
        journal_path.parent.mkdir(parents=True)
        broker_path.parent.mkdir(parents=True)
        scorer_path.parent.mkdir(parents=True)
        journal_path.write_text(journal, encoding="utf-8")
        broker_path.write_text(broker, encoding="utf-8")
        scorer_path.write_text(
            json.dumps({"total": {"ACTUAL": actual}}),
            encoding="utf-8",
        )

    def test_missing_pack_is_blocked_and_catalog_citation_matches(self) -> None:
        result = book_receipt.evaluate(Path("/tmp/does_not_exist_oct2_pack"))
        self.assertEqual(result["apply"], "NOT_APPLIED")
        self.assertFalse(result["armed"])
        self.assertEqual(result["fresh_result"], "BLOCKED")
        for name, target in (
            ("journal", "-2647.77"),
            ("broker", "-2208.95"),
            ("scorer", "-2041.95"),
        ):
            row = result["books"][name]
            self.assertEqual(row["fresh_status"], "BLOCKED")
            self.assertIsNone(row["fresh_computed"])
            self.assertEqual(row["target"], target)
            self.assertEqual(row["catalog_cited"], target)
            self.assertEqual(row["catalog_citation"], "MATCH")
        self.assertEqual(result["books"]["journal"]["catalog_cycles"], 41)
        self.assertEqual(result["books"]["journal"]["catalog_cycles_status"], "MATCH")

    def test_synthetic_pack_matches_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rows = [{"pnl": "0"} for _ in range(40)]
            rows.append({"pnl": "-2647.77"})
            journal = "".join(json.dumps(row) + "\n" for row in rows)
            self._write_pack(root, journal=journal, broker='{"pnl": "-2208.95"}\n', actual="-2041.95")
            result = book_receipt.evaluate(root, catalog_path=HERE / "catalog.json")
        self.assertEqual(result["fresh_result"], "MATCH")
        self.assertEqual(result["apply"], "NOT_APPLIED")
        for name in ("journal", "broker", "scorer"):
            self.assertEqual(result["books"][name]["fresh_status"], "MATCH")
            self.assertEqual(result["books"][name]["fresh_computed"], result["books"][name]["target"])
        self.assertEqual(result["books"]["journal"]["cycles"], 41)

    def test_synthetic_pack_drift_prints_the_computed_figure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rows = [{"pnl": "0"} for _ in range(40)]
            rows.append({"pnl": "-1.00"})
            journal = "".join(json.dumps(row) + "\n" for row in rows)
            self._write_pack(root, journal=journal, broker='{"pnl": "-2208.95"}\n', actual="-2041.95")
            result = book_receipt.evaluate(root, catalog_path=HERE / "catalog.json")
        self.assertEqual(result["fresh_result"], "DRIFT")
        self.assertEqual(result["books"]["journal"]["fresh_status"], "DRIFT")
        self.assertEqual(result["books"]["journal"]["fresh_computed"], "-1.00")
        self.assertEqual(result["books"]["journal"]["target"], "-2647.77")
        self.assertEqual(result["books"]["broker"]["fresh_status"], "MATCH")

    def test_live_apply_is_refused(self) -> None:
        with self.assertRaises(RuntimeError):
            book_receipt.evaluate(apply_live=True)


class ExitOwnerTest(unittest.TestCase):
    def tearDown(self) -> None:
        rules.ARMED = False
        rules.ULTRA_RATCHET_ARMED = False
        rules.CHANDELIER_UNTOUCHED = True

    def test_proposal_stays_unarmed(self) -> None:
        proposal = rules.stage_exit_owner()
        self.assertEqual(proposal["mode"], "COUNTERFACTUAL")
        self.assertEqual(proposal["apply"], "NOT_APPLIED")
        self.assertFalse(proposal["armed"])
        self.assertFalse(proposal["submits"])
        self.assertEqual(proposal["proposed_exit_owner"], "keep_peak_look")
        self.assertEqual(proposal["incumbent_exit_owner"], "as_traded_giveback")
        self.assertEqual(proposal["counterfactual_pl"], "BLOCKED")
        self.assertEqual(proposal["trend_notional"], 100_000.0)
        self.assertEqual(
            tuple(proposal["gates_held"]),
            ("midday", "FIX-BA", "strength", "C30", "C30-age"),
        )
        self.assertEqual(proposal["first_fill_target_et"], "09:35")
        self.assertEqual(proposal["first_fill_deadline_et"], "10:30")

    def test_spy_exemption_needs_both_flags(self) -> None:
        self.assertTrue(
            rules.spy_blocks_name(
                own_rvol_strong=True,
                trend_strong=False,
                minute=rules.FIRST_FILL_TARGET,
                lane="earn_trend",
                earnings_or_news=True,
            )
        )
        self.assertTrue(
            rules.spy_blocks_name(
                own_rvol_strong=False,
                trend_strong=True,
                minute=rules.FIRST_FILL_TARGET,
                lane="ma2",
                earnings_or_news=True,
            )
        )
        self.assertFalse(
            rules.spy_blocks_name(
                own_rvol_strong=True,
                trend_strong=True,
                minute=rules.FIRST_FILL_TARGET,
                lane="earn_trend",
                earnings_or_news=True,
            )
        )

    def test_overlay_blocks_without_writing_bars_or_dollars(self) -> None:
        result = overlay.assess(Path("/tmp/does_not_exist_oct2_pack"))
        self.assertEqual(result["status"], "BLOCKED_INPUTS")
        self.assertEqual(result["apply"], "NOT_APPLIED")
        self.assertEqual(result["counterfactual_pl"], "BLOCKED")
        self.assertEqual(result["bars_written_to_disk"], 0)
        self.assertFalse(result["invented_bars"])
        self.assertFalse(result["armed"])
        self.assertFalse(result["ultra_ratchet_armed"])
        self.assertTrue(result["chandelier_untouched"])
        self.assertEqual(result["tape_0830_status"], "BLOCKED_INPUTS")
        self.assertEqual(result["cells"]["hit_935"], ["S001"])
        self.assertEqual(result["cells"]["only_by_1030"], [])
        self.assertEqual(result["cells"]["tape_0830_n"], 49)
        self.assertEqual(result["cells"]["same_clock"].__len__(), 23)
        self.assertEqual(result["cells"]["force_hc_1030_n"], 32)
        self.assertIsNone(result["forced_rule_journal"]["symbol"])
        self.assertFalse(result["forced_rule_journal"]["armed"])
        self.assertTrue(result["forced_rule_receipt"]["idle"])
        priced = {row["id"]: row["dollars"] for row in result["cells"]["unprofitable_giveback"]}
        self.assertEqual(priced, {"S097": -2647.77, "S098": -2208.95, "S099": -2041.95})
        self.assertEqual(result["cells"]["exit_overlay_unpriced_n"], 97)
        self.assertTrue(result["morning_waiver"])
        for row in result["morning_waiver"]:
            self.assertFalse(row["exemption_opened"])
            self.assertEqual(row["resized_dollar"], "BLOCKED")
            self.assertEqual(row["catalog_notional"], 50000.0)
        trend = [row for row in result["morning_waiver"] if row["lane"] == "ma2"]
        self.assertEqual({row["symbol"] for row in trend}, {"NVDA", "IWM"})
        for row in trend:
            self.assertEqual(row["staged_notional"], 100_000.0)
            self.assertFalse(row["own_rvol_strong"])
        self.assertIsNone(result["recorded_giveback"]["peak"])
        self.assertEqual(result["recorded_giveback"]["pl"], 227.4)

    def test_writer_does_not_invent_a_bar_file(self) -> None:
        result = overlay.assess(Path("/tmp/does_not_exist_oct2_pack"))
        books = book_receipt.evaluate(Path("/tmp/does_not_exist_oct2_pack"))
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            overlay.write_outputs(result, dest, books=books, update_catalog=False)
            self.assertFalse(any(dest.glob("*.csv")))
            self.assertFalse((dest / "bars10s_trade_2026-10-02_0830_0900.csv").exists())
            payload = json.loads((dest / "exit_owner_counterfactual.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["counterfactual_pl"], "BLOCKED")
            self.assertEqual(payload["bars_written_to_disk"], 0)
            receipt = (dest / "RECEIPT.md").read_text(encoding="utf-8")
            self.assertIn("APPLY: NOT_APPLIED", receipt)
            self.assertIn("S001", receipt)
            self.assertIn("-2647.77", receipt)
            self.assertIn("-2208.95", receipt)
            self.assertIn("-2041.95", receipt)
            self.assertIn("computed=NONE", receipt)

    def test_catalog_attach_keeps_cell_dollars(self) -> None:
        payload = json.loads((HERE / "catalog.json").read_text(encoding="utf-8"))
        before = [(cell["id"], cell["dollars"], cell["by_935"]) for cell in payload["cells"]]
        result = overlay.assess(Path("/tmp/does_not_exist_oct2_pack"))
        updated = overlay.attach_to_catalog(payload, overlay.catalog_summary(result))
        after = [(cell["id"], cell["dollars"], cell["by_935"]) for cell in updated["cells"]]
        self.assertEqual(before, after)
        self.assertEqual(updated["exit_owner_counterfactual"]["apply"], "NOT_APPLIED")
        self.assertFalse(updated["armed"])


if __name__ == "__main__":
    unittest.main()
