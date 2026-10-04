"""Futuristic-fix exit-owner overlay. COUNTERFACTUAL, propose-only.

Does not submit, does not arm Ultra Ratchet, does not write a chandelier
parameter, and does not invent an 08:30 bar or an exit P&L. Cells that still
need the 08:30 tape stay BLOCKED_INPUTS. Stream BBO and quote bars do not
stand in for native REST quotes.
"""

from __future__ import annotations

import json
import sys
from datetime import time
from pathlib import Path

import book_receipt
import build_bars10s_0830 as bars
import giveback_counterfactual as giveback
from rules_staged import (
    ARMED,
    TREND_LANES,
    ArmRefused,
    _refuse_if_armed,
    spy_blocks_name,
    stage_exit_owner,
    stage_forced_highest_conviction,
    trend_notional_from_first_fill,
)

HERE = Path(__file__).resolve().parent
CATALOG = HERE / "catalog.json"


def _clock(value: str) -> time:
    hour, minute, second = (int(part) for part in value.split(":"))
    return time(hour, minute, second)


def waiver_for_entry(entry: dict) -> dict:
    """Classify one catalog entry. Does not invent RVOL or a fill."""
    reason = str(entry.get("reason") or "")
    lane = str(entry.get("lane") or "")
    upper = reason.upper()
    own_rvol_strong = "RVOL=" in upper or "RVOL " in upper
    trend_strong = lane in TREND_LANES or "TREND" in upper
    earnings_or_news = "EARN" in upper or lane in ("earn_trend", "earnings", "news", "news_strength")
    minute = _clock(str(entry.get("clock") or "09:35:00"))
    blocked = spy_blocks_name(
        own_rvol_strong=own_rvol_strong,
        trend_strong=trend_strong,
        minute=minute,
        lane=lane,
        earnings_or_news=earnings_or_news,
    )
    return {
        "clock": entry.get("clock"),
        "symbol": entry.get("symbol"),
        "lane": lane,
        "catalog_notional": entry.get("notional"),
        "staged_notional": trend_notional_from_first_fill(lane),
        "resized_dollar": "BLOCKED",
        "own_rvol_strong": own_rvol_strong,
        "trend_strong": trend_strong,
        "earnings_or_news": earnings_or_news,
        "spy_blocks": blocked,
        "exemption_opened": not blocked,
    }


def classify_cells(cells: list[dict]) -> dict:
    hit_935 = [cell["id"] for cell in cells if cell.get("by_935") == "HIT"]
    same_clock = [cell["id"] for cell in cells if cell.get("by_935") == "SAME_CLOCK"]
    only_by_1030 = [
        cell["id"]
        for cell in cells
        if cell.get("by_935") not in ("HIT", "SAME_CLOCK") and cell.get("by_1030") in ("HIT", "SAME_CLOCK")
    ]
    force = [cell for cell in cells if cell.get("deadline") == "force_hc_1030"]
    force_groups: dict[str, list[str]] = {}
    for cell in force:
        key = cell.get("missing") or cell.get("by_935") or "unmarked"
        force_groups.setdefault(str(key), []).append(cell["id"])
    tape = [
        cell["id"]
        for cell in cells
        if "TAPE_0830" in str(cell.get("missing") or "")
    ]
    unprofitable = []
    overlay_unpriced = []
    for cell in cells:
        look = str(cell.get("exit_look") or "")
        dollars = cell.get("dollars")
        giveback_look = "giveback" in look or "peak" in look
        if not giveback_look:
            continue
        if isinstance(dollars, (int, float)) and dollars < 0:
            unprofitable.append({"id": cell["id"], "dollars": dollars, "exit_look": look, "kind": cell.get("kind")})
        elif dollars == "BLOCKED":
            overlay_unpriced.append(cell["id"])
    return {
        "hit_935": hit_935,
        "same_clock": same_clock,
        "only_by_1030": only_by_1030,
        "force_hc_1030": force_groups,
        "force_hc_1030_n": len(force),
        "tape_0830": tape,
        "tape_0830_n": len(tape),
        "unprofitable_giveback": unprofitable,
        "exit_overlay_unpriced_n": len(overlay_unpriced),
        "exit_overlay_unpriced": overlay_unpriced,
    }


def _load_catalog(path: Path) -> dict:
    if not path.is_file():
        raise SystemExit(f"BLOCKED catalog missing: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    cells = payload.get("cells") or []
    if len(cells) != 100:
        raise SystemExit("refusing a catalog that is not the 100-cell book")
    return payload


def assess(pack: Path | None = None, catalog_path: Path | None = None) -> dict:
    """Propose the exit owner from the staged catalog. Does not write bars."""
    _refuse_if_armed()
    catalog_path = catalog_path or CATALOG
    payload = _load_catalog(catalog_path)
    proposal = stage_exit_owner()
    tape = bars.assess(pack)
    inputs = giveback.assess(pack)
    # Never persist builder rows. A missing hour stays BLOCKED_INPUTS.
    if tape["status"] == "BLOCKED_INPUTS" or not tape.get("bars"):
        tape_status = "BLOCKED_INPUTS"
        tape_note = "08:30-09:00 trade ticks are absent; no bars were invented"
    else:
        tape_status = "SEEN_NOT_WRITTEN"
        tape_note = (
            "builder saw in-window trade ticks in memory; this overlay wrote 0 bars "
            "and did not price from them"
        )
    exit_inputs = "BLOCKED_INPUTS" if inputs["status"] == "BLOCKED_INPUTS" else inputs["status"]
    if tape_status == "BLOCKED_INPUTS" or exit_inputs == "BLOCKED_INPUTS":
        overlay_status = "BLOCKED_INPUTS"
    else:
        overlay_status = "COUNTERFACTUAL"
    cells = classify_cells(payload["cells"])
    morning = [waiver_for_entry(row) for row in payload.get("morning_entries") or []]
    journal_force = stage_forced_highest_conviction([], filled_by_deadline=False)
    receipt_filled = bool(payload.get("demo_entries_by_935"))
    receipt_force = stage_forced_highest_conviction([], filled_by_deadline=receipt_filled)
    if journal_force["armed"] or journal_force["symbol"] is not None:
        raise ArmRefused("forced rule armed or invented a symbol")
    if receipt_force["armed"] or not receipt_force["idle"]:
        raise ArmRefused("forced rule must stay idle once the 09:35 receipt has a fill")
    for row in morning:
        if row["exemption_opened"] and not (row["own_rvol_strong"] and row["trend_strong"]):
            raise ArmRefused("SPY exemption opened without own RVOL and trend")
        if row["resized_dollar"] != "BLOCKED":
            raise ArmRefused("resized dollar must stay BLOCKED")
    return {
        "mode": "COUNTERFACTUAL",
        "apply": proposal["apply"],
        "armed": False,
        "submits": False,
        "status": overlay_status,
        "counterfactual_pl": "BLOCKED",
        "peak_invented": False,
        "bars_written_to_disk": 0,
        "invented_bars": False,
        "proposed_exit_owner": proposal["proposed_exit_owner"],
        "incumbent_exit_owner": proposal["incumbent_exit_owner"],
        "first_fill_target_et": proposal["first_fill_target_et"],
        "first_fill_deadline_et": proposal["first_fill_deadline_et"],
        "trend_notional": proposal["trend_notional"],
        "harness_notional_default": proposal["harness_notional_default"],
        "gates_held": proposal["gates_held"],
        "spy_exemption": proposal["spy_exemption"],
        "ultra_ratchet_armed": False,
        "chandelier_untouched": True,
        "tape_0830_status": tape_status,
        "tape_0830_note": tape_note,
        "builder_status": tape["status"],
        "builder_bars_in_memory": tape["bars_written"],
        "exit_inputs_status": exit_inputs,
        "giveback_status": inputs["status"],
        "native_rest_quotes_present": inputs["native_rest_quotes_present"],
        "bars10s_present": inputs["bars10s_present"],
        "stream_bbo_cannot_stand_in_for_rest": True,
        "quote_bars_are_not_trade_bars": True,
        "recorded_giveback": inputs["recorded_giveback"],
        "cells": cells,
        "morning_waiver": morning,
        "forced_rule_journal": journal_force,
        "forced_rule_receipt": receipt_force,
        "reference": payload.get("reference"),
        "first_fill": payload.get("first_fill"),
        "journal_fills_before_935": payload.get("journal_fills_before_935"),
        "journal_fills_before_1030": payload.get("journal_fills_before_1030"),
        "demo_entries_by_935": payload.get("demo_entries_by_935"),
        "demo_entries_by_1030": payload.get("demo_entries_by_1030"),
        "catalog_forced_rule_journal": payload.get("forced_rule_journal"),
        "catalog_forced_rule_receipt": payload.get("forced_rule_receipt"),
    }


def _ids(values: list[str]) -> str:
    return ", ".join(values) if values else "(none)"


def render(result: dict) -> str:
    cells = result["cells"]
    unprofitable = cells["unprofitable_giveback"]
    unprof_lines = "\n".join(
        f"- {row['id']} {row['dollars']} `{row['exit_look']}` ({row['kind']})"
        for row in unprofitable
    ) or "- (none)"
    force_lines = "\n".join(
        f"- {key}: {_ids(ids)}"
        for key, ids in cells["force_hc_1030"].items()
    ) or "- (none)"
    morning_lines = "\n".join(
        f"- {row['clock']} {row['symbol']} lane `{row['lane']}` catalog notional {row['catalog_notional']} "
        f"staged notional {row['staged_notional']:.0f} resized dollar BLOCKED "
        f"own_rvol={row['own_rvol_strong']} trend={row['trend_strong']} "
        f"spy_blocks={row['spy_blocks']}"
        for row in result["morning_waiver"]
    ) or "- (none)"
    gb = result["recorded_giveback"]
    return f"""# Exit-owner counterfactual — propose only

Mode: COUNTERFACTUAL
APPLY: NOT_APPLIED
ARMED: false
Status: {result['status']}
Counterfactual P&L: BLOCKED
Proposed exit owner: `{result['proposed_exit_owner']}`
Incumbent exit owner: `{result['incumbent_exit_owner']}`
Ultra Ratchet armed: false
Chandelier: untouched
Bars written to disk: 0

This overlay does not submit, does not arm a bot, and does not retune an exit. The 08:30 hour is not invented. Quote bars are not trade bars. A stream-only BBO study cannot stand in for native REST quotes.

## Clocks and size

First-fill target: {result['first_fill_target_et']} ET. Latest acceptable first fill: {result['first_fill_deadline_et']} ET.
Trend notional from the first fill: {result['trend_notional']:.0f}. Harness default {result['harness_notional_default']:.0f} is the wrong size for the trend lane.
Gates held: {', '.join(result['gates_held'])}.
SPY exemption: {result['spy_exemption']}.

## Cells from catalog.json

First fill by 09:35 (`by_935=HIT`): {_ids(cells['hit_935'])}.
Same entry clock, not a new first fill (`SAME_CLOCK`): {_ids(cells['same_clock'])}.
First fill only by 10:30: {_ids(cells['only_by_1030'])}.
Journal fills before 09:35: {result['journal_fills_before_935']}. Journal fills before 10:30: {result['journal_fills_before_1030']}.
Generator receipt entries by 09:35: {result['demo_entries_by_935']}. Entries by 10:30: {result['demo_entries_by_1030']}.

Forced highest-conviction cells (`deadline=force_hc_1030`, n={cells['force_hc_1030_n']}):

{force_lines}

Journal forced plan: idle={result['forced_rule_journal']['idle']} armed={result['forced_rule_journal']['armed']} symbol={result['forced_rule_journal']['symbol']} blocked={result['forced_rule_journal']['blocked']}.
Receipt forced plan: idle={result['forced_rule_receipt']['idle']} armed={result['forced_rule_receipt']['armed']} symbol={result['forced_rule_receipt']['symbol']}.

08:30 tape cells (`missing` contains TAPE_0830, n={cells['tape_0830_n']}): {_ids(cells['tape_0830'])}.
Tape status this run: {result['tape_0830_status']}. {result['tape_0830_note']}.

## Exit-giveback

Priced as-traded giveback books that stayed negative:

{unprof_lines}

Exit-look cells with dollars BLOCKED (not a profit): {cells['exit_overlay_unpriced_n']}.
Recorded giveback row, cited and not repriced: {gb['arm']} {gb['symbol']} {gb['pl']} at {gb['clock_et']} ET `{gb['reason']}`, peak None.

## Morning receipt versus the SPY exemption

{morning_lines}

None of those catalog rows open the exemption. NVDA and IWM are trend names without an RVOL multiple in the reason text. A resized $100k dollar for the trend lanes stays BLOCKED.
"""


def catalog_summary(result: dict) -> dict:
    cells = result["cells"]
    return {
        "mode": "COUNTERFACTUAL",
        "apply": "NOT_APPLIED",
        "status": result["status"],
        "counterfactual_pl": "BLOCKED",
        "armed": False,
        "proposed_exit_owner": result["proposed_exit_owner"],
        "incumbent_exit_owner": result["incumbent_exit_owner"],
        "trend_notional": result["trend_notional"],
        "gates_held": result["gates_held"],
        "hit_935": cells["hit_935"],
        "only_by_1030": cells["only_by_1030"],
        "tape_0830_n": cells["tape_0830_n"],
        "tape_0830_status": result["tape_0830_status"],
        "unprofitable_giveback": cells["unprofitable_giveback"],
        "ultra_ratchet_armed": False,
        "chandelier_untouched": True,
        "bars_written_to_disk": 0,
    }


def attach_to_catalog(payload: dict, summary: dict) -> dict:
    cells = payload.get("cells") or []
    if len(cells) != 100:
        raise SystemExit("refusing to touch a catalog that is not the 100-cell book")
    for cell in cells:
        if cell.get("kind") == "reference":
            continue
        if cell.get("dollars") != "BLOCKED":
            raise SystemExit(f"refusing to keep invented dollars on {cell['id']}")
    payload["exit_owner_counterfactual"] = summary
    payload["armed"] = False
    return payload


def render_receipt(result: dict, books: dict) -> str:
    cells = result["cells"]
    book_rows = []
    for name in ("journal", "broker", "scorer"):
        row = books["books"][name]
        computed = row["fresh_computed"] if row["fresh_computed"] is not None else "NONE"
        book_rows.append(
            f"- {name}: fresh {row['fresh_status']} computed={computed} target={row['target']} "
            f"catalog_cited={row['catalog_cited']} catalog_citation={row['catalog_citation']}"
        )
    unprof = ", ".join(
        f"{row['id']} {row['dollars']}" for row in cells["unprofitable_giveback"]
    ) or "(none)"
    return f"""# RECEIPT

APPLY: NOT_APPLIED
ARMED: false
Mode: COUNTERFACTUAL
Ultra Ratchet: unarmed
Chandelier: untouched
Fleet bots: not restarted
Gates held: {', '.join(result['gates_held'])}

Nothing in this receipt was applied live. No midday, FIX-BA, strength, C30, or C30-age gate was loosened. Ultra Ratchet was not armed. No bot was restarted.

## Morning-sweep cells

Source: `docs/atc/staged/oct2_morning_100/catalog.json` on the October 2 morning catalog (PR #7 counts, unchanged by the later handoff).

- First fill by 09:35: {_ids(cells['hit_935'])} (`by_935=HIT`). Exit dollars for that cell stay BLOCKED (`BARS_EXIT`).
- Same clock, not a separate first fill: {_ids(cells['same_clock'])}.
- First fill only by 10:30: {_ids(cells['only_by_1030'])}. Journal fills before 09:35: {result['journal_fills_before_935']}. Journal fills before 10:30: {result['journal_fills_before_1030']}. Generator entries by 09:35: {result['demo_entries_by_935']}. Generator entries by 10:30: {result['demo_entries_by_1030']}.
- Forced highest-conviction at 10:30 (n={cells['force_hc_1030_n']}): {', '.join(f'{key}={_ids(ids)}' for key, ids in cells['force_hc_1030'].items())}. Journal plan symbol={result['forced_rule_journal']['symbol']} blocked={result['forced_rule_journal']['blocked']}. Receipt plan idle={result['forced_rule_receipt']['idle']}.
- Missing 08:30 tape (n={cells['tape_0830_n']}): {_ids(cells['tape_0830'])}. This run: {result['tape_0830_status']}. No bars written.
- Exit-giveback books that stayed negative: {unprof}. Other exit-look cells with dollars BLOCKED: {cells['exit_overlay_unpriced_n']}. Recorded V1 NKE giveback stays {result['recorded_giveback']['pl']} at {result['recorded_giveback']['clock_et']} ET with peak None. Counterfactual P&L: BLOCKED.

## Three October 2 books

Fresh result: {books['fresh_result']}
{chr(10).join(book_rows)}

catalog_citation is a comparison of `catalog.json` `reference` to the targets. It is not a fresh sum. Fresh computed=NONE means the pack file is not on this checkout.

## Exit owner

Proposed owner `{result['proposed_exit_owner']}` replaces nothing. Incumbent owner stays `{result['incumbent_exit_owner']}`. Status {result['status']}. Trend notional {result['trend_notional']:.0f}. SPY exemption stays closed unless own RVOL and trend are both strong, on an earnings or news trend name, at or before 10:30. The four 09:35 catalog entries do not open it.
"""


def write_outputs(result: dict, dest: Path | None = None, *, books: dict | None = None, update_catalog: bool = False) -> Path:
    if result["counterfactual_pl"] != "BLOCKED":
        raise SystemExit("REFUSED dollar on the exit-owner overlay")
    if result["bars_written_to_disk"] != 0 or result["invented_bars"]:
        raise SystemExit("REFUSED bar write")
    if result["apply"] != "NOT_APPLIED" or result["armed"]:
        raise SystemExit("REFUSED apply")
    dest = dest or HERE
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "exit_owner_counterfactual.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    path = dest / "EXIT_OWNER_COUNTERFACTUAL.md"
    path.write_text(render(result), encoding="utf-8")
    if books is not None:
        (dest / "RECEIPT.md").write_text(render_receipt(result, books), encoding="utf-8")
    if update_catalog and dest == HERE:
        payload = _load_catalog(CATALOG)
        attach_to_catalog(payload, catalog_summary(result))
        CATALOG.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    if ARMED:
        print("REFUSED armed rules")
        return 2
    try:
        _refuse_if_armed()
    except ArmRefused as exc:
        print(f"REFUSED {exc}")
        return 2
    pack = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    result = assess(pack)
    if result["status"] not in ("BLOCKED_INPUTS", "COUNTERFACTUAL"):
        print("REFUSED unexpected status")
        return 2
    if result["counterfactual_pl"] != "BLOCKED" or result["bars_written_to_disk"] != 0:
        print("REFUSED dollar or bar write")
        return 2
    books = book_receipt.evaluate(pack)
    book_receipt.write_outputs(books)
    path = write_outputs(result, books=books, update_catalog=True)
    print(
        json.dumps(
            {
                "status": result["status"],
                "apply": result["apply"],
                "fresh_result": books["fresh_result"],
                "wrote": str(path),
                "hit_935": result["cells"]["hit_935"],
                "only_by_1030": result["cells"]["only_by_1030"],
                "tape_0830_n": result["cells"]["tape_0830_n"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
