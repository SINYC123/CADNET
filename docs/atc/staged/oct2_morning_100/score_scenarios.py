"""Score the staged October 2 morning catalog from the unpacked pack.

Reads journals, the broker day file, the scorer JSON, and the packaged
entry-generator receipt. Writes catalog.json, CATALOG.md, and NOTE.md.

Does not arm a rule, does not invent a dollar, and does not treat a missing
08:30-09:00 tape as a built hour. Exit dollars that need bars or a peak
stay BLOCKED.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

from rules_staged import (
    ARMED,
    BARS10S_SHA256,
    BARS10S_WIN,
    EXIT_LOOKS,
    FINDER_SKIP_BEFORE,
    FIRST_FILL_DEADLINE,
    FIRST_FILL_TARGET,
    HARNESS_NOTIONAL_DEFAULT,
    MISSING_TAPE,
    SIGNALS_WIN,
    TREND_NOTIONAL,
    ordinary_gates_held,
    spy_blocks_name,
    stage_forced_highest_conviction,
    trend_notional_from_first_fill,
)

ET = ZoneInfo("America/New_York")
DAY = "2026-10-02"
HERE = Path(__file__).resolve().parent

# Pack layout after `tar -xzf oct2_pack.tgz`.
DEFAULT_PACK = Path("/tmp/oct2_pack/oct2_pack")

BARS_REL = r"bars10s_2026-10-02.csv.gz"
BARS_WIN = BARS10S_WIN

PREMARKET = ("absent", "present")
DEADLINES = ("935", "1030", "force_hc_1030")
SPY_MODES = ("off_strong_own_rvol_trend", "on")
SIZES = (50_000, 100_000)


def parse_ts(ts: str) -> datetime:
    dt = datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ET)
    return dt.astimezone(ET)


def clock_ok(dt: datetime, deadline: time) -> bool:
    """True when the ET clock is at or before deadline."""
    c = dt.time()
    return (c.hour, c.minute, c.second) <= (deadline.hour, deadline.minute, deadline.second)


def load_oct2_fills(pack: Path) -> list[dict]:
    fills = []
    for arm in ("V1", "V2", "V3"):
        path = pack / "journals" / f"rows_{arm}.jsonl"
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("type") != "fill":
                continue
            if float(row.get("qty_filled") or 0) <= 0 or not row.get("ts"):
                continue
            dt = parse_ts(row["ts"])
            if dt.date().isoformat() != DAY:
                continue
            px = float(row.get("fill_px") or 0)
            qty = float(row.get("qty_filled") or 0)
            fills.append(
                {
                    "arm": arm,
                    "ts": dt.isoformat(),
                    "clock": dt.strftime("%H:%M:%S"),
                    "symbol": row.get("symbol"),
                    "lane": row.get("lane"),
                    "qty": qty,
                    "fill_px": px,
                    "notional": round(qty * px, 2),
                }
            )
    fills.sort(key=lambda r: r["ts"])
    return fills


def load_giveback(pack: Path) -> list[dict]:
    out = []
    for arm in ("V1", "V2", "V3"):
        path = pack / "journals" / f"rows_{arm}.jsonl"
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("type") != "exit" or not row.get("ts"):
                continue
            dt = parse_ts(row["ts"])
            if dt.date().isoformat() != DAY:
                continue
            reason = str(row.get("reason") or "")
            if "GIVEBACK" not in reason.upper() and "PEAK" not in reason.upper():
                continue
            if row.get("qty") is None:
                continue
            out.append(
                {
                    "arm": arm,
                    "clock": dt.strftime("%H:%M:%S"),
                    "symbol": row.get("symbol"),
                    "pl": row.get("pl"),
                    "reason": reason,
                    "peak": row.get("peak_pl") or row.get("peak") or row.get("mfe"),
                }
            )
    return out


def load_demo_entries(pack: Path) -> list[dict]:
    path = pack / "entry_generator" / "demo_entries_pre1030_sample.jsonl"
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    rows.sort(key=lambda r: r["entry_ts"])
    return rows


def reference_dollars(pack: Path) -> dict:
    journal = 0.0
    n = 0
    for line in (pack / "journal_closed" / "batch_c_4162.jsonl").read_text().splitlines():
        if not line.strip():
            continue
        journal += float(json.loads(line)["pnl"])
        n += 1
    broker = 0.0
    for line in (pack / "broker_day" / "day_pnl_20261002.jsonl").read_text().splitlines():
        if line.strip():
            broker += float(json.loads(line)["pnl"])
    scorer = json.loads(
        (pack / "journals" / "inv_price_v3_2026-10-02_2026-10-02.json").read_text()
    )["total"]["ACTUAL"]
    return {
        "journal_synthetic": round(journal, 2),
        "journal_cycles": n,
        "broker_day": round(broker, 2),
        "scorer_actual": round(float(scorer), 2),
    }


def demo_before(rows: list[dict], deadline: time) -> list[dict]:
    kept = []
    for row in rows:
        dt = parse_ts(row["entry_ts"])
        if clock_ok(dt, deadline):
            kept.append(
                {
                    "clock": dt.strftime("%H:%M:%S"),
                    "symbol": row.get("symbol"),
                    "arm": row.get("arm"),
                    "side": row.get("side"),
                    "lane": row.get("lane"),
                    "score": row.get("score"),
                    "notional": row.get("notional"),
                    "qty": row.get("qty"),
                    "entry_px": row.get("entry_px"),
                    "reason": row.get("reason"),
                }
            )
    return kept


def build_grid() -> list[dict]:
    cells = []
    n = 1
    # Absent and SPY-off come first so the search reaches the recorded receipt early.
    for pre in PREMARKET:
        for spy in SPY_MODES:
            for size in SIZES:
                for deadline in DEADLINES:
                    for exit_look in EXIT_LOOKS:
                        cells.append(
                            {
                                "id": f"S{n:03d}",
                                "kind": "grid",
                                "premarket": pre,
                                "deadline": deadline,
                                "spy": spy,
                                "trend_notional": size,
                                "exit_look": exit_look,
                            }
                        )
                        n += 1
    assert n == 97, n
    cells.extend(
        [
            {
                "id": "S097",
                "kind": "reference",
                "book": "journal",
                "premarket": "absent",
                "deadline": "as_traded",
                "spy": "unrecorded",
                "trend_notional": "as_filled",
                "exit_look": "as_traded_giveback",
            },
            {
                "id": "S098",
                "kind": "reference",
                "book": "broker",
                "premarket": "absent",
                "deadline": "as_traded",
                "spy": "unrecorded",
                "trend_notional": "as_filled",
                "exit_look": "as_traded_giveback",
            },
            {
                "id": "S099",
                "kind": "reference",
                "book": "scorer",
                "premarket": "absent",
                "deadline": "as_traded",
                "spy": "unrecorded",
                "trend_notional": "as_filled",
                "exit_look": "as_traded_giveback",
            },
            {
                "id": "S100",
                "kind": "handoff",
                "premarket": "present",
                "deadline": "935",
                "spy": "off_strong_own_rvol_trend",
                "trend_notional": int(TREND_NOTIONAL),
                "exit_look": "keep_peak_look",
                "note": "eval origin 08:30 so 09:30 already has an hour of bars; tape slot empty",
            },
        ]
    )
    assert len(cells) == 100
    return cells


def score_cell(cell: dict, *, observed_hit: bool) -> dict:
    """Attach time-bar and dollar results. Never fills in a computed P/L."""
    out = dict(cell)
    pre = cell["premarket"]
    spy = cell["spy"]
    kind = cell["kind"]

    if kind == "reference":
        book = cell["book"]
        dollars = {
            "journal": -2647.77,
            "broker": -2208.95,
            "scorer": -2041.95,
        }[book]
        out.update(
            {
                "by_935": "FAIL",
                "by_1030": "FAIL",
                "dollars": dollars,
                "dollar_source": f"pack reference {book}",
                "missing": "",
                "evidence": "journal first fill 11:09:03 ET V3 TSLA; 0 fills before 10:30",
            }
        )
        return out

    if pre == "present" or kind == "handoff":
        out.update(
            {
                "by_935": "BLOCKED",
                "by_1030": "BLOCKED",
                "dollars": "BLOCKED",
                "dollar_source": "",
                "missing": "TAPE_0830",
                "evidence": MISSING_TAPE,
            }
        )
        return out

    # Premarket absent. The packaged generator receipt is the only entry clock
    # in the pack before 10:30, and it does not apply a SPY check.
    if spy == "on":
        out.update(
            {
                "by_935": "BLOCKED",
                "by_1030": "BLOCKED",
                "dollars": "BLOCKED",
                "dollar_source": "",
                "missing": "SPY_LOG",
                "evidence": (
                    "no SPY-gate decision row in the pack; "
                    + ", ".join(SIGNALS_WIN)
                    + " are not in the pack"
                ),
            }
        )
        return out

    # spy off, premarket absent. Entry clock is the generator receipt.
    # Only S001 is the observed run (50k, deadline 935, exit as traded).
    # Siblings reuse that clock. They do not gain a dollar.
    observed = (
        cell["trend_notional"] == 50_000
        and cell["deadline"] == "935"
        and cell["exit_look"] == "as_traded_giveback"
        and observed_hit
    )
    missing_parts = ["BARS_EXIT"]
    if cell["exit_look"] != "as_traded_giveback":
        missing_parts.append("PEAK")
    if cell["deadline"] == "force_hc_1030":
        missing_parts.append("SIGNALS")
    if cell["trend_notional"] == 100_000:
        missing_parts.append("BARS_EXIT")
    # unique, stable order
    missing = "+".join(dict.fromkeys(missing_parts))
    out.update(
        {
            "by_935": "HIT" if observed else "SAME_CLOCK",
            "by_1030": "HIT" if observed else "SAME_CLOCK",
            "dollars": "BLOCKED",
            "dollar_source": "",
            "missing": missing,
            "evidence": (
                "demo_entries_pre1030_sample.jsonl sim entries at 09:33:50 and 09:34:00 ET; "
                "exit P/L needs "
                + BARS_WIN
            ),
        }
    )
    return out


def render_catalog(payload: dict) -> str:
    lines = [
        "# October 2 morning catalog — 100 staged cells",
        "",
        "Draft only. `ARMED` is false. This file is the results table. Nothing here merges.",
        "",
        "Handoff S100: `build_bars10s_0830.py` writes 10s trade bars for 08:30–09:00 ET only from raw ticks. "
        "If those ticks are absent the status is `BLOCKED_INPUTS` (`BLOCKED_INPUTS.md`) and no bars are written. "
        "09:30 stays the finder skip floor and is not a minimum bar count. "
        "The giveback counterfactual is `BLOCKED_INPUTS` when `bars10s` or a native REST quote tape is missing "
        "(`GIVEBACK_COUNTERFACTUAL.md`). Ultra Ratchet stays unarmed. The chandelier is untouched. "
        "Prior counts stay: 100 cells, 3 dollar-priced, 97 dollar BLOCKED, 1 hit (S001), "
        "49 missing the 08:30 tape, 24 missing a SPY-gate record.",
        "",
        "Time-bar legend: `HIT` is the one observed generator receipt. "
        "`SAME_CLOCK` reuses that entry clock and adds no dollar. "
        "`FAIL` is a reference book whose first journal fill is 11:09:03 ET. "
        "`BLOCKED` has no tape or no gate record.",
        "",
        "Dollar legend: the three reference books are cited. Every other dollar cell is `BLOCKED`.",
        "",
        "Missing codes:",
        "",
        "| Code | File |",
        "|---|---|",
        f"| TAPE_0830 | {MISSING_TAPE} |",
        f"| BARS_EXIT | `{BARS_WIN}` (sha256 {BARS10S_SHA256}), omitted from the pack. Quote bars are not trade bars. |",
        "| PEAK | journal exit rows have no peak / MFE field |",
        f"| SPY_LOG | no SPY refuse log; missing {', '.join(f'`{p}`' for p in SIGNALS_WIN)} |",
        f"| SIGNALS | {', '.join(f'`{p}`' for p in SIGNALS_WIN)} |",
        "",
        "| id | kind | premarket | deadline | spy | notional | exit | by 9:35 | by 10:30 | dollars | missing |",
        "|---|---|---|---|---|---:|---|---|---|---:|---|",
    ]
    for cell in payload["cells"]:
        dollars = cell["dollars"]
        dollars_s = f"{dollars:.2f}" if isinstance(dollars, float) else str(dollars)
        kind = cell["kind"]
        if cell.get("book"):
            kind = f"reference:{cell['book']}"
        lines.append(
            "| {id} | {kind} | {premarket} | {deadline} | {spy} | {notional} | {exit_look} | {by_935} | {by_1030} | {dollars_s} | {missing} |".format(
                id=cell["id"],
                kind=kind,
                premarket=cell["premarket"],
                deadline=cell["deadline"],
                spy=cell["spy"],
                notional=cell["trend_notional"],
                exit_look=cell["exit_look"],
                by_935=cell["by_935"],
                by_1030=cell["by_1030"],
                dollars_s=dollars_s,
                missing=cell["missing"] or "",
            )
        )
    lines.append("")
    return "\n".join(lines)


def render_note(payload: dict) -> str:
    c = payload["counts"]
    hit = payload["morning_entries"]
    hit_lines = "\n".join(
        f"- {row['clock']} ET {row['arm']} {row['symbol']} {row['side']} {row['lane']} "
        f"score {row['score']} entry {row['entry_px']} qty {row['qty']} at notional {row['notional']}"
        for row in hit
    )
    gb = payload["giveback"]
    gb_lines = "\n".join(
        f"  - {row['arm']} {row['clock']} ET {row['symbol']} P/L {row['pl']} reason {row['reason']}; peak field {row['peak']}"
        for row in gb
    ) or "  - none"
    step = payload["notional_step"]
    return f"""# October 2 morning scenarios — what is still blocked

Draft only. This catalog does not arm a bot, does not merge, and does not change an exit.

## Counts

| | |
|---|---|
| Cells | 100 |
| Dollar-priced | {c['priced']} |
| Dollar BLOCKED | {c['dollars_blocked']} |
| Observed set that hits a trade by 9:35 ET | {c['hit_935_observed']} ({payload['first_hit']}) |
| Cells that reuse that entry clock | {c['same_clock']} |
| Failed the 9:35 bar | {c['fail_935']} |
| Failed the 10:30 bar | {c['fail_1030']} |
| Time-bar BLOCKED | {c['time_blocked']} |
| Of which missing the 08:30 tape | {c['blocked_tape']} |
| Of which missing a SPY-gate record | {c['blocked_spy']} |

The morning number is a trade that can print by 9:35 ET, with 10:30 ET as the latest acceptable first fill. The {c['priced']} priced cells are the three reference books. They fail both clocks. No knob cell has a dollar.

## Reference books (cited from the pack)

| Book | Dollars | Source in the pack |
|---|---:|---|
| Journal synthetic ENTRY pairing | -2647.77 | `journal_closed/batch_c_4162.jsonl` ({payload['reference']['journal_cycles']} cycles) and `journal_closed/batch_C.md` |
| Broker day | -2208.95 | `broker_day/day_pnl_20261002.jsonl` |
| Scorer ACTUAL | -2041.95 | `journals/inv_price_v3_2026-10-02_2026-10-02.json` and `smoke_inv_price_v3_20261002.txt` |

First October 2 journal fill: {payload['first_fill']['clock']} ET {payload['first_fill']['arm']} {payload['first_fill']['symbol']} ({payload['first_fill']['lane']}), notional {payload['first_fill']['notional']:.0f}. Journal fills before 09:35: {payload['journal_fills_before_935']}. Journal fills before 10:30: {payload['journal_fills_before_1030']}. That day fails the new bar.

## The set that hits

{payload['first_hit']} is the packaged entry-generator receipt (`entry_generator/demo_entries_pre1030_sample.jsonl`): premarket hour absent, harness notional {HARNESS_NOTIONAL_DEFAULT:.0f}. `entry_generator.py` has no SPY check. The finder skip floor is {FINDER_SKIP_BEFORE.strftime('%H:%M')} (`DEFAULT_SESSION_OPEN`). These sim entries are in the pack. Exit dollars for them are BLOCKED.

{hit_lines}

{c['same_clock']} other cells (premarket absent, SPY off for the strong-own-RVOL trend case) stay on this same entry clock. A {TREND_NOTIONAL:.0f} size, a different exit look, or the 10:30 forced-submit flag leaves the dollar cell BLOCKED. On this receipt the forced rule stays idle, because a sim entry is already on the book before 10:30.

The generator receipt is the source of these four entries. NVDA and IWM are `[TREND-RAW]` MA2 names and the reason text has no RVOL multiple, so the SPY waiver stays closed for them. The waiver opens only for an earnings/news-strength name that also has high own RVOL and trend, and only through 10:30. Ordinary names stay blocked. The only explicit RVOL in the pre-10:30 sample is SPCX at 09:59:10 ET (`RVOL=3.5x`), which is after 09:35 and before 10:30, and that row is a continuation name. The dollar difference between SPY on and SPY off is BLOCKED.

## Still blocked

- **08:30–09:00 tape.** {c['blocked_tape']} cells, including the handoff cell {payload['handoff_id']}, need the hour so a name at 09:30 already has 60 minutes of bars. 09:30 remains the finder skip floor and is not a minimum bar count. Missing file: {MISSING_TAPE}. `rules_staged.EVAL_START` is 08:30. `build_bars10s_0830.py` builds that window only from raw trade ticks already in the pack. This checkout has none, so the handoff status is BLOCKED_INPUTS (`BLOCKED_INPUTS.md`) and no bars were written.
- **SPY-on cells.** {c['blocked_spy']} cells. Missing file: a SPY-gate decision record, and the signal files {', '.join(SIGNALS_WIN)}. Midday, FIX-BA, strength, and C30 are unchanged in `rules_staged.GATES_HELD`.
- **Exit giveback look.** Recorded giveback rows:
{gb_lines}
  Keep-peak, trend-keep-peak, and the recorded peak-lock keep 0.80 / take 0.90 are looks. Journal exits store no peak. The staged counterfactual (`giveback_counterfactual.py`, `GIVEBACK_COUNTERFACTUAL.md`) cites V1 NKE +227.40 at 11:15:25 ET and does not invent a peak. It stays BLOCKED_INPUTS while `{BARS_WIN}` or a native REST quote tape is missing. Quote bars are not trade bars. A stream-only BBO study cannot stand in for native REST quotes. The look leaves the chandelier and Ultra Ratchet untouched.
- **Forced 10:30 submit.** Staged in `rules_staged.stage_forced_highest_conviction`. `ARMED` is {str(ARMED)}. On the journal book the rule is eligible (0 fills by 10:30). The name is BLOCKED. Missing files: {', '.join(SIGNALS_WIN)}.
- **Trend size.** Staged trend notional is locked at {TREND_NOTIONAL:.0f} from the first fill (`trend_notional_from_first_fill`). The packaged harness default is {HARNESS_NOTIONAL_DEFAULT:.0f}, and that default is the wrong trend size. Measured October 2 fill notionals step up later on V1 and V2 and stay near 50k on V3. First `earn_trend` fill is {step['first_earn_trend']}. A later 100k fill on that lane is {step['later_earn_trend']}. Startup `ATC_SLOT_AM` on the 11:06 ET rows is 100000, and the first fills of the day are still about 50k. A resized 100k dollar stays BLOCKED because `{BARS_REL}` is not in the pack.

## How this was scored

`score_scenarios.py` reads the unpacked pack, checks the three reference totals, counts journal fills against 09:35 and 10:30, and reads the packaged generator receipt. Cells that need the 08:30 tape stay BLOCKED. `build_bars10s_0830.py` and `giveback_counterfactual.py` are stage-only and refuse to invent bars or peaks. The script refuses to run when `rules_staged.ARMED` is true.
"""


def main() -> int:
    if ARMED:
        print("REFUSED armed rules")
        return 2
    pack = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACK
    if not pack.is_dir():
        print(f"BLOCKED pack missing: {pack}")
        return 2

    refs = reference_dollars(pack)
    if refs["journal_synthetic"] != -2647.77:
        raise SystemExit(f"journal reference mismatch {refs}")
    if refs["broker_day"] != -2208.95:
        raise SystemExit(f"broker reference mismatch {refs}")
    if refs["scorer_actual"] != -2041.95:
        raise SystemExit(f"scorer reference mismatch {refs}")

    fills = load_oct2_fills(pack)
    if not fills:
        raise SystemExit("no October 2 fills in journals")
    first = fills[0]
    if first["clock"] != "11:09:03" or first["symbol"] != "TSLA" or first["arm"] != "V3":
        raise SystemExit(f"unexpected first fill {first}")
    before_935 = [f for f in fills if clock_ok(parse_ts(f["ts"]), FIRST_FILL_TARGET)]
    before_1030 = [f for f in fills if clock_ok(parse_ts(f["ts"]), FIRST_FILL_DEADLINE)]
    if before_935 or before_1030:
        raise SystemExit("journal book has a fill inside the morning window; catalog assumptions broke")

    demo = load_demo_entries(pack)
    morning = demo_before(demo, FIRST_FILL_TARGET)
    if len(morning) < 1:
        raise SystemExit("generator receipt has no entry by 09:35; morning number not in the pack")
    by_1030 = demo_before(demo, FIRST_FILL_DEADLINE)
    # Ordinary MA2 stays blocked. The waiver is earnings/news-strength only.
    if spy_blocks_name(
        own_rvol_strong=False, trend_strong=True, minute=time(9, 33), lane="ma2"
    ) is not True:
        raise SystemExit("SPY waiver opened without own RVOL")
    if spy_blocks_name(
        own_rvol_strong=True, trend_strong=True, minute=time(9, 33), lane="ma2"
    ) is not True:
        raise SystemExit("SPY waiver opened for an ordinary MA2 name")
    if spy_blocks_name(
        own_rvol_strong=True,
        trend_strong=True,
        minute=time(9, 33),
        lane="earn_trend",
        earnings_or_news=True,
    ) is not False:
        raise SystemExit("SPY waiver failed to open for an earnings/news-strength name")
    if spy_blocks_name(
        own_rvol_strong=True,
        trend_strong=True,
        minute=time(12, 0),
        lane="earn_trend",
        earnings_or_news=True,
    ) is not True:
        raise SystemExit("SPY waiver opened after the 10:30 deadline")
    if ordinary_gates_held() != ("midday", "FIX-BA", "strength", "C30"):
        raise SystemExit("held gates changed")
    if trend_notional_from_first_fill("earn_trend") != 100_000.0:
        raise SystemExit("trend notional is not locked at 100000")
    if trend_notional_from_first_fill("vwap_revert") == 100_000.0:
        raise SystemExit("non-trend lane took the trend notional")

    # Journal path: forced rule is eligible and has no candidate file.
    journal_force = stage_forced_highest_conviction([], filled_by_deadline=False)
    if journal_force["armed"] or journal_force["symbol"] is not None:
        raise SystemExit("forced rule armed or invented a symbol")
    # Receipt path: entries already exist, so the forced rule stays idle.
    receipt_force = stage_forced_highest_conviction(
        [{"symbol": morning[0]["symbol"], "score": morning[0]["score"]}],
        filled_by_deadline=True,
    )
    if not receipt_force["idle"]:
        raise SystemExit("forced rule should stay idle once a fill exists")

    earn = [f for f in fills if f["lane"] == "earn_trend"]
    later_100k = next((f for f in earn if f["notional"] >= 90_000), None)

    cells = []
    first_hit = None
    for raw in build_grid():
        scored = score_cell(raw, observed_hit=True)
        cells.append(scored)
        if scored["by_935"] == "HIT" and first_hit is None:
            first_hit = scored["id"]

    if first_hit != "S001":
        raise SystemExit(f"expected the observed hit at S001, got {first_hit}")

    # No knob cell may carry a dollar. Reference dollars must match the pack.
    for cell in cells:
        if cell["kind"] == "reference":
            continue
        if cell["dollars"] != "BLOCKED":
            raise SystemExit(f"invented dollars on {cell['id']}")
        if cell["premarket"] == "present" and cell["missing"] != "TAPE_0830":
            raise SystemExit(f"present cell missing tape mark {cell['id']}")

    counts = {
        "priced": sum(1 for c in cells if isinstance(c["dollars"], float)),
        "dollars_blocked": sum(1 for c in cells if c["dollars"] == "BLOCKED"),
        "hit_935_observed": sum(1 for c in cells if c["by_935"] == "HIT"),
        "same_clock": sum(1 for c in cells if c["by_935"] == "SAME_CLOCK"),
        "fail_935": sum(1 for c in cells if c["by_935"] == "FAIL"),
        "fail_1030": sum(1 for c in cells if c["by_1030"] == "FAIL"),
        "time_blocked": sum(1 for c in cells if c["by_935"] == "BLOCKED"),
        "blocked_tape": sum(1 for c in cells if c["missing"] == "TAPE_0830"),
        "blocked_spy": sum(1 for c in cells if c["missing"] == "SPY_LOG"),
    }
    if counts["priced"] + counts["dollars_blocked"] != 100:
        raise SystemExit(counts)
    if counts["hit_935_observed"] + counts["same_clock"] + counts["fail_935"] + counts["time_blocked"] != 100:
        raise SystemExit(counts)

    payload = {
        "armed": False,
        "day": DAY,
        "pack": str(pack),
        "first_hit": first_hit,
        "handoff_id": "S100",
        "counts": counts,
        "reference": refs,
        "first_fill": first,
        "journal_fills_before_935": len(before_935),
        "journal_fills_before_1030": len(before_1030),
        "demo_entries_pre_1030": len(demo),
        "demo_entries_by_935": len(morning),
        "demo_entries_by_1030": len(by_1030),
        "morning_entries": morning,
        "giveback": load_giveback(pack),
        "notional_step": {
            "first_earn_trend": (
                f"{earn[0]['clock']} ET {earn[0]['arm']} {earn[0]['symbol']} notional {earn[0]['notional']:.0f}"
                if earn
                else "none"
            ),
            "later_earn_trend": (
                f"{later_100k['clock']} ET {later_100k['arm']} {later_100k['symbol']} notional {later_100k['notional']:.0f}"
                if later_100k
                else "none"
            ),
        },
        "forced_rule_journal": journal_force,
        "forced_rule_receipt": receipt_force,
        "cells": cells,
    }

    (HERE / "catalog.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (HERE / "CATALOG.md").write_text(render_catalog(payload), encoding="utf-8")
    (HERE / "NOTE.md").write_text(render_note(payload), encoding="utf-8")
    print(json.dumps({"first_hit": first_hit, "counts": counts, "morning": len(morning)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
