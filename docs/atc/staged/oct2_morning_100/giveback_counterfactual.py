"""Staged keep-peak / giveback counterfactual. Not armed.

Cites the recorded October 2 giveback row and stops when bars10s or a native
REST quote tape is missing. Does not invent a peak, a fill, or a P&L.
Quote bars are not trade bars. A stream-only BBO file cannot stand in for
native REST quotes. Ultra Ratchet and the chandelier stay untouched.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from rules_staged import (
    ARMED,
    BARS10S_PACK_REL,
    BARS10S_SHA256,
    BARS10S_WIN,
    MISSING_REST_QUOTES,
    ArmRefused,
    _refuse_if_armed,
    ratchet_status,
)

HERE = Path(__file__).resolve().parent
DAY = "2026-10-02"

# Recorded journal exit already extracted into catalog.json from rows_V1.jsonl.
# 2026-10-02T15:15:25Z == 11:15:25 ET. Peak field on that row is null.
RECORDED_GIVEBACK = {
    "arm": "V1",
    "clock_et": "11:15:25",
    "symbol": "NKE",
    "pl": 227.40,
    "pl_source": "journal exit pl 227.4 on rows_V1.jsonl",
    "reason": "EARN TREND GIVEBACK",
    "lane": "earn_trend",
    "peak": None,
}

PACK_CANDIDATES = (
    Path("/tmp/oct2_pack/oct2_pack"),
    Path("/workspace/oct2_pack"),
    Path("/workspace/oct2_pack/oct2_pack"),
)


def _find_named(roots: list[Path], needle: str) -> list[str]:
    hits = []
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_file() and needle in path.name.lower():
                if path.parent == HERE and path.suffix in {".md", ".py", ".json"}:
                    continue
                hits.append(str(path))
    return hits


def assess(pack: Path | None = None) -> dict:
    """Counterfactual status from files that exist. Does not compute a new P&L."""
    _refuse_if_armed()
    roots = []
    if pack is not None:
        roots.append(pack)
    for candidate in PACK_CANDIDATES:
        if candidate not in roots:
            roots.append(candidate)
    checked = [{"root": str(root), "exists": root.is_dir()} for root in roots]
    bars = _find_named(roots, "bars10s_2026-10-02")
    # Native REST quotes only. Do not treat bars10s / bid_o / ask_o as this input.
    rest = []
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            name = path.name.lower()
            if path.parent == HERE:
                continue
            if "rest" in name and "quote" in name:
                rest.append(str(path))
    ratchet = ratchet_status()
    blocked = not bars or not rest
    return {
        "status": "BLOCKED_INPUTS" if blocked else "READY_TO_LOOK",
        "armed": False,
        "day": DAY,
        "counterfactual_pl": "BLOCKED",
        "peak_invented": False,
        "recorded_giveback": RECORDED_GIVEBACK,
        "bars10s_present": bars,
        "bars10s_required": BARS10S_WIN,
        "bars10s_sha256": BARS10S_SHA256,
        "bars10s_pack_rel": BARS10S_PACK_REL,
        "bars10s_are_quote_bars": True,
        "quote_bars_are_not_trade_bars": True,
        "native_rest_quotes_present": rest,
        "missing_rest_quotes": MISSING_REST_QUOTES if not rest else "",
        "stream_bbo_cannot_stand_in_for_rest": True,
        "ultra_ratchet_armed": ratchet["ultra_ratchet_armed"],
        "chandelier_untouched": ratchet["chandelier_untouched"],
        "peak_lock_keep_recorded": ratchet["peak_lock_keep_recorded"],
        "peak_lock_take_recorded": ratchet["peak_lock_take_recorded"],
        "checked_roots": checked,
        "cells_affected": "keep_peak_look, trend_keep_peak_look, peak_lock_keep_80_look stay dollar BLOCKED",
    }


def render(result: dict) -> str:
    gb = result["recorded_giveback"]
    bars = result["bars10s_present"] or ["absent"]
    rest = result["native_rest_quotes_present"] or ["absent"]
    roots = "\n".join(
        f"- `{row['root']}`: {'present' if row['exists'] else 'absent'}"
        for row in result["checked_roots"]
    )
    return f"""# Giveback counterfactual — stage only

Status: {result['status']}
ARMED: false
Ultra Ratchet armed: false
Chandelier: untouched
Counterfactual P&L: BLOCKED
Peak invented: false

Nothing in this overlay submits an order, retunes an exit, arms Ultra Ratchet, or writes a chandelier parameter.

## Recorded evidence

{gb['arm']} {gb['symbol']} {gb['pl']:.2f} at {gb['clock_et']} ET, reason `{gb['reason']}`, peak field None.
Journal value is 227.4 (`{gb['pl_source']}`). This overlay does not replace that figure and does not invent the missing peak.

Recorded startup peak-lock on the V1 row, cited and not retuned: keep {result['peak_lock_keep_recorded']:.2f} / take {result['peak_lock_take_recorded']:.2f}.

## Inputs checked

{roots}

- bars10s: {', '.join(bars)}
- native REST quotes: {', '.join(rest)}

Required bar path: `{result['bars10s_required']}`
sha256 `{result['bars10s_sha256']}`
Pack-relative `{result['bars10s_pack_rel']}`

{result['missing_rest_quotes']}

cf12 `bars10s` columns are 10-second BBO (`bid_o` / `ask_o`). Quote bars are not trade bars. A stream-only exit study cannot stand in for native REST quotes. Both inputs are required before a keep-peak look can be priced. This run did not price one.

## What stays blocked

Keep-peak, trend-keep-peak, and peak-lock keep 0.80 / take 0.90 stay looks. Dollar cells that need them stay BLOCKED. The 49-cell 08:30 tape block is unchanged. The three reference books stay the only priced dollars.
"""


def write_outputs(result: dict, dest: Path | None = None) -> Path:
    dest = dest or HERE
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "giveback_counterfactual.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    path = dest / "GIVEBACK_COUNTERFACTUAL.md"
    path.write_text(render(result), encoding="utf-8")
    catalog = dest / "catalog.json"
    if catalog.is_file() and dest == HERE:
        payload = json.loads(catalog.read_text(encoding="utf-8"))
        if len(payload.get("cells") or []) != 100:
            raise SystemExit("refusing to touch a catalog that is not the 100-cell book")
        payload["giveback_counterfactual"] = {
            "status": result["status"],
            "counterfactual_pl": "BLOCKED",
            "peak": None,
            "recorded": result["recorded_giveback"],
            "ultra_ratchet_armed": False,
            "chandelier_untouched": True,
        }
        payload["armed"] = False
        catalog.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
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
    if result["recorded_giveback"]["peak"] is not None:
        print("REFUSED invented peak")
        return 2
    if result["counterfactual_pl"] != "BLOCKED" and result["status"] == "BLOCKED_INPUTS":
        print("REFUSED dollar on a blocked overlay")
        return 2
    path = write_outputs(result)
    print(json.dumps({"status": result["status"], "wrote": str(path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
