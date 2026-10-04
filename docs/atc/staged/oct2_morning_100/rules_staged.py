"""Staged morning rules for the October 2 catalog. Not armed.

Nothing in this module submits an order, edits a launcher, or changes a live exit.
ARMED stays False. Callers that try to flip it are refused.
"""

from __future__ import annotations

from datetime import time

ARMED = False

# Evaluation origin. 09:30 is the packaged entry finder's skip floor
# (entry_generator.DEFAULT_SESSION_OPEN). It is not the minimum-bar origin.
EVAL_START = time(8, 30)
FINDER_SKIP_BEFORE = time(9, 30)
FIRST_FILL_TARGET = time(9, 35)
FIRST_FILL_DEADLINE = time(10, 30)

# Trend lane size out of the gate. The packaged harness default is 50000
# (entry_generator.DEFAULT_NOTIONAL). That default is the wrong trend size.
HARNESS_NOTIONAL_DEFAULT = 50_000.0
TREND_NOTIONAL = 100_000.0

# Gates this stage does not loosen.
GATES_HELD = ("midday", "FIX-BA", "strength", "C30")

# Exit looks. Recorded startup keep/take is quoted, not retuned.
# Ultra Ratchet is not armed. No chandelier parameter is written.
EXIT_LOOKS = (
    "as_traded_giveback",
    "keep_peak_look",
    "trend_keep_peak_look",
    "peak_lock_keep_80_look",
)

# Tape a later run must load before it can score a name at 09:30 under EVAL_START.
MISSING_TAPE = (
    "raw tick tape 2026-10-02 08:30-09:00 ET "
    "(not in oct2_pack; bars10s_2026-10-02.csv.gz was omitted from the pack "
    "and the October 2 simulation starts at 09:00)"
)


class ArmRefused(RuntimeError):
    """Raised if a caller tries to arm a staged rule."""


def _refuse_if_armed() -> None:
    if ARMED:
        raise ArmRefused("staged morning rules refuse to arm")


def spy_blocks_name(
    *,
    own_rvol_strong: bool,
    trend_strong: bool,
    minute: time,
    lane: str,
) -> bool:
    """SPY waiver spec. Ordinary names keep the SPY check.

    The waiver applies only when the name's own RVOL and trend are both
    strong and the clock is still at the open (through the 10:30 deadline).
    Midday, FIX-BA, strength, and C30 are not touched.
    """
    _refuse_if_armed()
    open_gate = minute <= FIRST_FILL_DEADLINE
    trend_lane = lane in ("ma2", "earn_trend", "trend")
    if open_gate and own_rvol_strong and trend_strong and trend_lane:
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
