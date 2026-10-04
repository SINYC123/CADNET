"""Checks for the unarmed October 2 handoff. No network. No fabricated catalog bars."""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import build_bars10s_0830 as bars
import giveback_counterfactual as giveback
import rules_staged as rules

ET = ZoneInfo("America/New_York")


class RulesTest(unittest.TestCase):
    def tearDown(self) -> None:
        rules.ARMED = False
        rules.ULTRA_RATCHET_ARMED = False
        rules.CHANDELIER_UNTOUCHED = True

    def test_flags_stay_unarmed(self) -> None:
        self.assertFalse(rules.ARMED)
        self.assertFalse(rules.ULTRA_RATCHET_ARMED)
        self.assertTrue(rules.CHANDELIER_UNTOUCHED)
        status = rules.ratchet_status()
        self.assertFalse(status["ultra_ratchet_armed"])
        self.assertTrue(status["chandelier_untouched"])
        self.assertFalse(status["retuned"])
        self.assertEqual(status["peak_lock_keep_recorded"], 0.80)
        self.assertEqual(status["peak_lock_take_recorded"], 0.90)

    def test_arm_is_refused(self) -> None:
        rules.ARMED = True
        with self.assertRaises(rules.ArmRefused):
            rules.spy_blocks_name(
                own_rvol_strong=True,
                trend_strong=True,
                minute=rules.FIRST_FILL_TARGET,
                lane="earn_trend",
                earnings_or_news=True,
            )

    def test_spy_waiver_is_earnings_news_only(self) -> None:
        self.assertTrue(
            rules.spy_blocks_name(
                own_rvol_strong=True,
                trend_strong=True,
                minute=datetime(2026, 10, 2, 9, 33).time(),
                lane="ma2",
            )
        )
        self.assertFalse(
            rules.spy_blocks_name(
                own_rvol_strong=True,
                trend_strong=True,
                minute=datetime(2026, 10, 2, 9, 33).time(),
                lane="earn_trend",
                earnings_or_news=True,
            )
        )
        self.assertTrue(
            rules.spy_blocks_name(
                own_rvol_strong=True,
                trend_strong=True,
                minute=datetime(2026, 10, 2, 12, 0).time(),
                lane="earn_trend",
                earnings_or_news=True,
            )
        )
        self.assertEqual(
            rules.ordinary_gates_held(),
            ("midday", "FIX-BA", "strength", "C30", "C30-age"),
        )

    def test_trend_notional_locked(self) -> None:
        self.assertEqual(rules.trend_notional_from_first_fill("earn_trend"), 100_000.0)
        self.assertEqual(rules.trend_notional_from_first_fill("ma2"), 100_000.0)
        self.assertEqual(rules.trend_notional_from_first_fill("vwap_revert"), 50_000.0)
        self.assertEqual(rules.FIRST_FILL_TARGET.hour, 9)
        self.assertEqual(rules.FIRST_FILL_TARGET.minute, 35)
        self.assertEqual(rules.FIRST_FILL_DEADLINE.hour, 10)
        self.assertEqual(rules.FIRST_FILL_DEADLINE.minute, 30)
        self.assertEqual(rules.EVAL_START.hour, 8)
        self.assertEqual(rules.FINDER_SKIP_BEFORE.hour, 9)
        self.assertEqual(rules.FINDER_SKIP_BEFORE.minute, 30)

    def test_forced_rule_stays_idle_or_blocked(self) -> None:
        idle = rules.stage_forced_highest_conviction(
            [{"symbol": "NKE", "score": 9}], filled_by_deadline=True
        )
        self.assertTrue(idle["idle"])
        self.assertFalse(idle["armed"])
        self.assertIsNone(idle["symbol"])
        blocked = rules.stage_forced_highest_conviction([], filled_by_deadline=False)
        self.assertFalse(blocked["armed"])
        self.assertIsNone(blocked["symbol"])
        self.assertIn("signals_V1", blocked["blocked"])


class BarBuilderTest(unittest.TestCase):
    def test_window_keeps_0830_and_drops_0930(self) -> None:
        ticks = [
            {"symbol": "NKE", "ts": datetime(2026, 10, 2, 8, 29, 59, tzinfo=ET), "price": 10.0, "size": 1},
            {"symbol": "NKE", "ts": datetime(2026, 10, 2, 8, 30, 0, tzinfo=ET), "price": 11.0, "size": 2},
            {"symbol": "NKE", "ts": datetime(2026, 10, 2, 8, 30, 4, tzinfo=ET), "price": 12.0, "size": 3},
            {"symbol": "NKE", "ts": datetime(2026, 10, 2, 8, 59, 59, tzinfo=ET), "price": 9.0, "size": 4},
            {"symbol": "NKE", "ts": datetime(2026, 10, 2, 9, 0, 0, tzinfo=ET), "price": 8.0, "size": 5},
            {"symbol": "NKE", "ts": datetime(2026, 10, 2, 9, 30, 0, tzinfo=ET), "price": 7.0, "size": 6},
        ]
        built = bars.build_trade_bars(ticks)
        self.assertEqual(len(built), 2)
        self.assertEqual(built[0]["open"], 11.0)
        self.assertEqual(built[0]["high"], 12.0)
        self.assertEqual(built[0]["close"], 12.0)
        self.assertEqual(built[0]["volume"], 5)
        self.assertEqual(built[0]["n_trades"], 2)
        self.assertTrue(built[0]["bar_et"].startswith("2026-10-02T08:30:00"))
        self.assertTrue(built[1]["bar_et"].startswith("2026-10-02T08:59:50"))
        self.assertLess(len(built), 180)

    def test_quote_rows_are_not_trade_bars(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bars10s_2026-10-02.csv"
            path.write_text(
                "symbol,t,bid_o,ask_o\nNKE,1,10,10.01\n",
                encoding="utf-8",
            )
            scan = bars.scan_file(path)
            self.assertEqual(scan["trade_rows"], 0)
            self.assertGreater(scan["quote_rows"], 0)
            self.assertEqual(bars.build_trade_bars([]), [])

    def test_raw_ticks_in_a_file_build_only_the_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ticks_2026-10-02.csv"
            path.write_text(
                "received_ts,symbol,price,size\n"
                "2026-10-02T08:45:01-04:00,NKE,70.5,10\n"
                "2026-10-02T09:30:01-04:00,NKE,71.0,10\n",
                encoding="utf-8",
            )
            scan = bars.scan_file(path)
            self.assertEqual(scan["in_window"], 1)
            built = bars.build_trade_bars(scan["trades"])
            self.assertEqual(len(built), 1)
            self.assertEqual(built[0]["symbol"], "NKE")
            self.assertTrue(built[0]["bar_et"].startswith("2026-10-02T08:45:00"))

    def test_blocked_writer_does_not_emit_a_bar_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            result = {
                "status": "BLOCKED_INPUTS",
                "armed": False,
                "bars_written": 0,
                "bars": [],
                "eval_start": "08:30",
                "finder_skip_before": "09:30",
                "window_et": "08:30:00 inclusive to 09:00:00 exclusive",
                "quote_files_not_used_as_trade_bars": [],
                "checked_roots": [{"root": str(dest), "exists": True}],
                "bars10s_present": [],
                "missing": ["raw ticks", rules.BARS10S_WIN],
            }
            public = bars.write_outputs(result, dest)
            self.assertEqual(public["status"], "BLOCKED_INPUTS")
            self.assertFalse((dest / "bars10s_trade_2026-10-02_0830_0900.csv").exists())
            text = (dest / "BLOCKED_INPUTS.md").read_text(encoding="utf-8")
            self.assertIn("BLOCKED_INPUTS", text)
            self.assertIn(rules.BARS10S_WIN, text)
            self.assertIn("received_ts", text)


class GivebackTest(unittest.TestCase):
    def test_overlay_blocks_without_inventing_a_peak(self) -> None:
        result = giveback.assess(Path("/tmp/does_not_exist_oct2_pack"))
        self.assertEqual(result["status"], "BLOCKED_INPUTS")
        self.assertEqual(result["counterfactual_pl"], "BLOCKED")
        self.assertIsNone(result["recorded_giveback"]["peak"])
        self.assertEqual(result["recorded_giveback"]["pl"], 227.40)
        self.assertEqual(result["recorded_giveback"]["symbol"], "NKE")
        self.assertFalse(result["ultra_ratchet_armed"])
        self.assertTrue(result["chandelier_untouched"])
        self.assertTrue(result["quote_bars_are_not_trade_bars"])
        self.assertEqual(result["bars10s_present"], [])
        self.assertEqual(result["native_rest_quotes_present"], [])

    def test_writer_leaves_peak_null(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            result = giveback.assess(dest)
            giveback.write_outputs(result, dest)
            payload = json.loads((dest / "giveback_counterfactual.json").read_text(encoding="utf-8"))
            self.assertIsNone(payload["recorded_giveback"]["peak"])
            self.assertEqual(payload["counterfactual_pl"], "BLOCKED")
            note = (dest / "GIVEBACK_COUNTERFACTUAL.md").read_text(encoding="utf-8")
            self.assertIn("peak field None", note)
            self.assertIn("BLOCKED", note)


if __name__ == "__main__":
    unittest.main()
