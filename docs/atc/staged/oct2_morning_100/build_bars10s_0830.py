"""Staged 10-second trade-bar builder for 2026-10-02 08:30–09:00 ET.

S100 handoff. Stage only. ARMED stays false.

Builds bars only from raw trade ticks already in the pack. Does not fabricate
ticks, bars, fills, or P&L. Quote bars (bid/ask, including cf12 bars10s BBO)
are not trade bars and are not converted. 09:30 is the finder skip floor, not
a minimum bar count, and it is outside this window.

When the ticks are absent this script writes BLOCKED_INPUTS and no bar file.
"""

from __future__ import annotations

import csv
import gzip
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from rules_staged import (
    ARMED,
    BARS10S_PACK_REL,
    BARS10S_SHA256,
    BARS10S_WIN,
    EVAL_START,
    FINDER_SKIP_BEFORE,
    HANDOFF_BAR_SECONDS,
    HANDOFF_WINDOW_END,
    HANDOFF_WINDOW_START,
    MISSING_TAPE,
    STALIE_RAW_TICKS,
    ArmRefused,
    _refuse_if_armed,
)

ET = ZoneInfo("America/New_York")
DAY = "2026-10-02"
HERE = Path(__file__).resolve().parent

# Pack layout after `tar -xzf oct2_pack.tgz`. Also the checkout-local copy.
PACK_CANDIDATES = (
    Path("/tmp/oct2_pack/oct2_pack"),
    Path("/workspace/oct2_pack"),
    Path("/workspace/oct2_pack/oct2_pack"),
)

TRADE_PRICE_FIELDS = ("price", "trade_px", "px", "last", "trade_price")
CLOCK_FIELDS = ("received_ts", "ts", "timestamp", "t")
SIZE_FIELDS = ("size", "qty", "volume", "shares")
QUOTE_FIELDS = ("bid", "ask", "bid_o", "ask_o", "bid_c", "ask_c")

WINDOW_START = datetime(2026, 10, 2, HANDOFF_WINDOW_START.hour, HANDOFF_WINDOW_START.minute, tzinfo=ET)
WINDOW_END = datetime(2026, 10, 2, HANDOFF_WINDOW_END.hour, HANDOFF_WINDOW_END.minute, tzinfo=ET)


def _open_text(path: Path):
    if path.name.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return path.open("r", encoding="utf-8", errors="replace")


def parse_clock(value) -> datetime | None:
    """Parse a tick clock. Naive ISO is ET. Epoch seconds are absolute."""
    if value is None or value is False:
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return datetime.fromtimestamp(float(value), tz=ET)
    text = str(value).strip()
    if not text:
        return None
    try:
        as_num = float(text)
    except ValueError:
        as_num = None
    if as_num is not None and "T" not in text and "-" not in text[1:]:
        return datetime.fromtimestamp(as_num, tz=ET)
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ET)
    return dt.astimezone(ET)


def _first(row: dict, names: tuple[str, ...]):
    for name in names:
        if name in row and row[name] not in (None, ""):
            return row[name]
    lower = {str(k).lower(): k for k in row}
    for name in names:
        key = lower.get(name)
        if key is not None and row[key] not in (None, ""):
            return row[key]
    return None


def classify_row(row: dict) -> str:
    """Return 'trade', 'quote', or 'unusable'. Never promotes a quote to a trade."""
    has_trade_px = _first(row, TRADE_PRICE_FIELDS) is not None
    has_quote = any(_first(row, (name,)) is not None for name in QUOTE_FIELDS)
    if has_trade_px:
        return "trade"
    if has_quote:
        return "quote"
    return "unusable"


def tick_from_row(row: dict) -> dict | None:
    """One trade tick, or None when the row is not a trade inside the schema."""
    if classify_row(row) != "trade":
        return None
    clock_raw = _first(row, CLOCK_FIELDS)
    when = parse_clock(clock_raw)
    if when is None:
        return None
    try:
        price = float(_first(row, TRADE_PRICE_FIELDS))
    except (TypeError, ValueError):
        return None
    if price <= 0:
        return None
    size_raw = _first(row, SIZE_FIELDS)
    try:
        size = float(size_raw) if size_raw is not None else 0.0
    except (TypeError, ValueError):
        size = 0.0
    symbol = str(_first(row, ("symbol", "sym")) or "").upper().strip()
    if not symbol:
        return None
    return {"symbol": symbol, "ts": when, "price": price, "size": size}


def in_handoff_window(when: datetime) -> bool:
    """08:30:00 inclusive through 09:00:00 exclusive. 09:30 is not required."""
    return WINDOW_START <= when < WINDOW_END


def bucket_start(when: datetime) -> datetime:
    when = when.astimezone(ET).replace(microsecond=0)
    second = (when.second // HANDOFF_BAR_SECONDS) * HANDOFF_BAR_SECONDS
    return when.replace(second=second)


def build_trade_bars(ticks: list[dict]) -> list[dict]:
    """Aggregate trade ticks into 10s bars. Drops ticks outside the window.

    Does not pad empty buckets and does not require a bar at 09:30.
    """
    _refuse_if_armed()
    if EVAL_START != HANDOFF_WINDOW_START:
        raise ArmRefused("handoff window must stay at EVAL_START 08:30")
    if FINDER_SKIP_BEFORE.hour == 8:
        raise ArmRefused("finder skip floor must stay at 09:30")
    kept = [t for t in ticks if in_handoff_window(t["ts"])]
    kept.sort(key=lambda t: (t["symbol"], t["ts"]))
    bars: dict[tuple[str, datetime], dict] = {}
    for tick in kept:
        key = (tick["symbol"], bucket_start(tick["ts"]))
        bar = bars.get(key)
        px = tick["price"]
        if bar is None:
            bars[key] = {
                "symbol": tick["symbol"],
                "bar_et": key[1].isoformat(),
                "open": px,
                "high": px,
                "low": px,
                "close": px,
                "volume": tick["size"],
                "n_trades": 1,
            }
            continue
        bar["high"] = max(bar["high"], px)
        bar["low"] = min(bar["low"], px)
        bar["close"] = px
        bar["volume"] = bar["volume"] + tick["size"]
        bar["n_trades"] += 1
    return [bars[k] for k in sorted(bars)]


def _iter_rows(path: Path):
    name = path.name.lower()
    with _open_text(path) as handle:
        if name.endswith(".json") or name.endswith(".jsonl") or name.endswith(".jsonl.gz"):
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict):
                    yield obj
                elif isinstance(obj, list):
                    for item in obj:
                        if isinstance(item, dict):
                            yield item
            return
        sample = handle.read(4096)
        handle.seek(0)
        if not sample.strip():
            return
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(handle, dialect=dialect)
        for row in reader:
            if row:
                yield {k: v for k, v in row.items() if k}


def scan_file(path: Path) -> dict:
    """Classify a file. Does not invent rows that are not in the file."""
    trades = []
    quote_rows = 0
    other = 0
    in_window = 0
    try:
        for row in _iter_rows(path):
            kind = classify_row(row)
            if kind == "quote":
                quote_rows += 1
                continue
            if kind != "trade":
                other += 1
                continue
            tick = tick_from_row(row)
            if tick is None:
                other += 1
                continue
            trades.append(tick)
            if in_handoff_window(tick["ts"]):
                in_window += 1
    except OSError as exc:
        return {"path": str(path), "error": str(exc), "trades": [], "in_window": 0, "quote_rows": 0}
    return {
        "path": str(path),
        "trades": trades,
        "trade_rows": len(trades),
        "in_window": in_window,
        "quote_rows": quote_rows,
        "other_rows": other,
    }


def _candidate_files(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    found = []
    needles = ("tick", "trade", "tape", "bars10s", "quote", "meta_2026-10-02")
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        name = path.name.lower()
        if any(n in name for n in needles):
            found.append(path)
    return found


def locate_inputs(pack: Path | None) -> dict:
    """Search this checkout and the known pack roots. Does not download data."""
    roots = []
    if pack is not None:
        roots.append(pack)
    for candidate in PACK_CANDIDATES:
        if candidate not in roots:
            roots.append(candidate)
    roots.append(HERE)
    checked = []
    scans = []
    bars_hits = []
    for root in roots:
        record = {"root": str(root), "exists": root.is_dir()}
        checked.append(record)
        if not root.is_dir():
            continue
        for path in _candidate_files(root):
            if path.name == BARS10S_PACK_REL or path.name.startswith("bars10s_2026-10-02"):
                bars_hits.append(str(path))
            # Skip our own staged notes.
            if path.parent == HERE and path.suffix in {".md", ".py", ".json"}:
                continue
            scans.append(scan_file(path))
    return {"checked_roots": checked, "scans": scans, "bars10s_paths": bars_hits}


def assess(pack: Path | None = None) -> dict:
    """Decide whether the 08:30 hour can be built. Never fills a missing hour."""
    _refuse_if_armed()
    located = locate_inputs(pack)
    window_ticks = []
    quote_files = []
    outside_only = []
    for scan in located["scans"]:
        if scan.get("quote_rows") and not scan.get("in_window"):
            quote_files.append(scan["path"])
        if scan.get("in_window"):
            for tick in scan["trades"]:
                if in_handoff_window(tick["ts"]):
                    window_ticks.append(tick)
        elif scan.get("trade_rows"):
            outside_only.append(scan["path"])
    bars = build_trade_bars(window_ticks) if window_ticks else []
    status = "BUILT" if bars else "BLOCKED_INPUTS"
    return {
        "status": status,
        "armed": False,
        "day": DAY,
        "eval_start": EVAL_START.strftime("%H:%M"),
        "finder_skip_before": FINDER_SKIP_BEFORE.strftime("%H:%M"),
        "window_et": "08:30:00 inclusive to 09:00:00 exclusive",
        "bar_seconds": HANDOFF_BAR_SECONDS,
        "minimum_bar_count": None,
        "bars_written": len(bars),
        "bars": bars if status == "BUILT" else [],
        "quote_files_not_used_as_trade_bars": quote_files,
        "trade_files_outside_window": outside_only,
        "bars10s_present": located["bars10s_paths"],
        "checked_roots": located["checked_roots"],
        "missing": [
            STALIE_RAW_TICKS,
            f"{BARS10S_WIN} sha256 {BARS10S_SHA256} pack-relative {BARS10S_PACK_REL}",
        ],
        "missing_tape": MISSING_TAPE,
        "note": (
            "09:30 is the finder skip floor, not the minimum bar count. "
            "Quote bars are not trade bars. No ticks were fabricated."
        ),
    }


def render_blocked(result: dict) -> str:
    def _label(row: dict) -> str:
        if not row["exists"]:
            return "absent"
        if str(row["root"]).endswith("oct2_morning_100"):
            return "present (staged catalog only, not a tick pack)"
        return "present"

    roots = "\n".join(f"- `{row['root']}`: {_label(row)}" for row in result["checked_roots"])
    bars_present = result["bars10s_present"] or ["absent"]
    return f"""# BLOCKED_INPUTS — 08:30–09:00 bar handoff (S100 family)

Status: BLOCKED_INPUTS
ARMED: false
Bars written: {result['bars_written']}
EVAL_START: {result['eval_start']} ET
Finder skip floor: {result['finder_skip_before']} ET
Window: {result['window_et']}
Minimum bar count: none (09:30 is not a minimum bar count)

This run did not fabricate ticks, bars, fills, or P&L.

## Checked in this repo

{roots}

`bars10s_2026-10-02.csv.gz` in those roots: {', '.join(bars_present)}

The unpacked `oct2_pack` inventory is 31 files (journals, broker day, scorer, entry-generator receipt). It contains no tick file, no `meta_2026-10-02.json`, and no `bars10s_2026-10-02.csv.gz`. That tarball is not in this checkout. This run searched the paths above and did not find a substitute.

## What STALIE must pack to unblock the 49 cells

1. Raw trade ticks for 2026-10-02 08:30:00–09:00:00 ET.
   Clock field `received_ts` (the clock `build_bars.py` uses).
   Trade price field (`price`, `trade_px`, `px`, `last`, or `trade_price`). Bid/ask is not a trade.
   Exact filename is not in this repo. Drop the file into the pack where this builder can see a tick/trade/tape name.
   Pack-relative slot: `oct2_pack/` raw trade ticks covering that window.

2. And/or `{BARS10S_WIN}`
   sha256 `{BARS10S_SHA256}`
   Pack-relative name: `{BARS10S_PACK_REL}`
   That file is cf12 10-second BBO (`symbol`, `t`, `bid_o`, `ask_o`). Quote bars are not trade bars.
   The October 2 simulation starts at 09:00, so this file is not the 08:30 hour. It is still required for a later exit replay. A resized dollar stays BLOCKED while it is absent.

## Cells

49 cells, including handoff S100, stay `TAPE_0830`. Building this window does not move the finder skip floor off 09:30 and does not arm a rule.
"""


def write_outputs(result: dict, dest: Path | None = None) -> dict:
    """Write the handoff note. Writes a bar file only when real in-window ticks existed."""
    _refuse_if_armed()
    dest = dest or HERE
    dest.mkdir(parents=True, exist_ok=True)
    public = {k: v for k, v in result.items() if k != "bars"}
    public["bars_omitted_from_status"] = result["status"] != "BUILT"
    (dest / "handoff_0830.json").write_text(json.dumps(public, indent=2) + "\n", encoding="utf-8")
    catalog = dest / "catalog.json"
    if catalog.is_file() and dest == HERE:
        payload = json.loads(catalog.read_text(encoding="utf-8"))
        if len(payload.get("cells") or []) != 100:
            raise SystemExit("refusing to touch a catalog that is not the 100-cell book")
        payload["handoff_0830"] = {
            "status": public["status"],
            "bars_written": public["bars_written"],
            "armed": False,
            "window_et": public["window_et"],
            "minimum_bar_count": None,
            "missing": public["missing"],
        }
        payload["armed"] = False
        catalog.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if result["status"] != "BUILT":
        (dest / "BLOCKED_INPUTS.md").write_text(render_blocked(result), encoding="utf-8")
        bar_path = dest / "bars10s_trade_2026-10-02_0830_0900.csv"
        if bar_path.exists():
            bar_path.unlink()
        return public
    # Real ticks only. This branch does not run unless assess() found them.
    bar_path = dest / "bars10s_trade_2026-10-02_0830_0900.csv"
    with bar_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["symbol", "bar_et", "open", "high", "low", "close", "volume", "n_trades"],
        )
        writer.writeheader()
        writer.writerows(result["bars"])
    public["bar_file"] = str(bar_path)
    (dest / "handoff_0830.json").write_text(json.dumps(public, indent=2) + "\n", encoding="utf-8")
    return public


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
    public = write_outputs(result)
    print(json.dumps({"status": public["status"], "bars_written": public["bars_written"]}, indent=2))
    return 0 if public["status"] in {"BUILT", "BLOCKED_INPUTS"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
