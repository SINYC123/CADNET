"""Staged morning rules for the October 2 catalog. Not armed.

Nothing in this module submits an order, edits a launcher, or changes a live exit.
ARMED stays False. Ultra Ratchet stays unarmed. No chandelier parameter is written.
Callers that try to flip an arm flag are refused.
"""

from __future__ import annotations

from datetime import time

ARMED = False
ULTRA_RATCHET_ARMED = False
CHANDELIER_UNTOUCHED = True

# Evaluation origin. 09:30 is the packaged entry finder's skip floor
# (entry_generator.DEFAULT_SESSION_OPEN). It is not the minimum-bar origin
# and it is not a minimum bar count.
EVAL_START = time(8, 30)
FINDER_SKIP_BEFORE = time(9, 30)
FIRST_FILL_TARGET = time(9, 35)
FIRST_FILL_DEADLINE = time(10, 30)

# Builder window for the S100 handoff. End is exclusive.
# 09:30 is not inside this window and is not required before a bar can count.
HANDOFF_WINDOW_START = time(8, 30)
HANDOFF_WINDOW_END = time(9, 0)
HANDOFF_BAR_SECONDS = 10

# Trend lane size from the first fill. The packaged harness default is 50000
# (entry_generator.DEFAULT_NOTIONAL). That default is the wrong trend size.
HARNESS_NOTIONAL_DEFAULT = 50_000.0
TREND_NOTIONAL = 100_000.0
TREND_NOTIONAL_LOCKED_FROM_FIRST_FILL = True
TREND_LANES = ("ma2", "earn_trend", "trend")

# Recorded V1 startup peak-lock (rows_V1.jsonl exit_config). Cited, not retuned.
# ATC_PEAK_LOCK_KEEP=0.80, ATC_PEAK_LOCK_TAKE=0.90, ATC_PEAK_LOCK_FRAC=0 on that row.
RECORDED_PEAK_LOCK_KEEP = 0.80
RECORDED_PEAK_LOCK_TAKE = 0.90

# Gates this stage does not loosen. They stay held for ordinary names.
GATES_HELD = ("midday", "FIX-BA", "strength", "C30")

# Exit looks. Recorded startup keep/take is quoted, not retuned.
# Ultra Ratchet is not armed. No chandelier parameter is written.
EXIT_LOOKS = (
    "as_traded_giveback",
    "keep_peak_look",
    "trend_keep_peak_look",
    "peak_lock_keep_80_look",
)

# cf12 10s file is BBO (bid_o/ask_o). Quote bars are not trade bars.
BARS10S_SHA256 = "e615fdcc3669651444e4274ec010a75bb2cd0a49ce288b18127457abb1447ea5"
BARS10S_WIN = r"C:\ATC\claude_harness\cf12_20261002\data\bars10s_2026-10-02.csv.gz"
BARS10S_PACK_REL = "bars10s_2026-10-02.csv.gz"
SIGNALS_WIN = (
    r"C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V1.jsonl",
    r"C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V2.jsonl",
    r"C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V3.jsonl",
)

# The 31-file oct2_pack inventory has no tick file and no meta_2026-10-02.json.
# build_bars.py clocks ticks on received_ts. The exact raw-tick filename is not
# in this repo; STALIE must pack the trade ticks for the window below.
STALIE_RAW_TICKS = (
    "raw trade ticks 2026-10-02 08:30:00-09:00:00 ET "
    "(clock field received_ts; trade price, not bid/ask; "
    "no tick file in oct2_pack)"
)

# Tape a later run must load before it can score a name at 09:30 under EVAL_START.
MISSING_TAPE = (
    STALIE_RAW_TICKS
    + " and/or "
    + BARS10S_WIN
    + " (sha256 "
    + BARS10S_SHA256
    + "; omitted from the pack; the October 2 simulation starts at 09:00; "
    + "quote bars are not trade bars)"
)

# No REST quote capture is in the pack. Do not invent a Windows path for it.
MISSING_REST_QUOTES = (
    "native REST quote tape for 2026-10-02 "
    "(absent from this repo pack; the 31-file oct2_pack inventory has no quote capture; "
    "stream BBO / bars10s bid_o ask_o cannot stand in)"
)


class ArmRefused(RuntimeError):
    """Raised if a caller tries to arm a staged rule."""


def _refuse_if_armed() -> None:
    if ARMED or ULTRA_RATCHET_ARMED or not CHANDELIER_UNTOUCHED:
        raise ArmRefused("staged morning rules refuse to arm")


def ordinary_gates_held() -> tuple[str, ...]:
    """Midday, FIX-BA, strength, and C30 stay held for ordinary names."""
    _refuse_if_armed()
    return GATES_HELD


def trend_notional_from_first_fill(lane: str) -> float:
    """Staged trend size from the first fill.

    Returns the locked $100k trend notional. Does not return a P&L.
    A resized dollar that needs bars stays BLOCKED at the catalog layer.
    The harness $50k default is not the trend-lane size.
    """
    _refuse_if_armed()
    if not TREND_NOTIONAL_LOCKED_FROM_FIRST_FILL:
        raise ArmRefused("staged trend notional is locked at 100000 from the first fill")
    if lane in TREND_LANES:
        if TREND_NOTIONAL != 100_000.0:
            raise ArmRefused("staged trend notional must stay 100000")
        return TREND_NOTIONAL
    return HARNESS_NOTIONAL_DEFAULT


def spy_blocks_name(
    *,
    own_rvol_strong: bool,
    trend_strong: bool,
    minute: time,
    lane: str,
    earnings_or_news: bool = False,
) -> bool:
    """SPY waiver spec. Ordinary names keep the SPY check.

    The waiver is the high-own-RVOL/trend exemption for earnings/news-strength
    names only, and only through the 10:30 first-fill deadline.
    Midday, FIX-BA, strength, and C30 are not touched.
    """
    _refuse_if_armed()
    open_gate = minute <= FIRST_FILL_DEADLINE
    trend_lane = lane in TREND_LANES or lane in ("earnings", "news", "news_strength")
    if open_gate and earnings_or_news and own_rvol_strong and trend_strong and trend_lane:
        return False
    return True


def stage_forced_highest_conviction(candidates: list[dict] | None, *, filled_by_deadline: bool) -> dict:
    """Stage the 10:30 highest-conviction submit. Does not submit.

    If the book already has a fill, the rule stays idle.
    If it does not, the plan names the highest score in `candidates`.
    An empty candidate list stays blocked; this function does not invent a name.
    """
    _refuse_if_armed()
    plan = {
        "armed": False,
        "rule": "if nothing has filled by 10:30 ET, submit the highest-conviction name at that minute",
        "idle": False,
        "symbol": None,
        "blocked": None,
    }
    if filled_by_deadline:
        plan["idle"] = True
        plan["blocked"] = None
        return plan
    if not candidates:
        plan["blocked"] = "missing signals_V1.jsonl, signals_V2.jsonl, signals_V3.jsonl"
        return plan
    best = max(candidates, key=lambda row: float(row.get("score") or 0))
    plan["symbol"] = best.get("symbol")
    plan["score"] = best.get("score")
    return plan


def ratchet_status() -> dict:
    """Record that Ultra Ratchet and the chandelier stay untouched."""
    _refuse_if_armed()
    return {
        "ultra_ratchet_armed": False,
        "chandelier_untouched": True,
        "peak_lock_keep_recorded": RECORDED_PEAK_LOCK_KEEP,
        "peak_lock_take_recorded": RECORDED_PEAK_LOCK_TAKE,
        "retuned": False,
    }
