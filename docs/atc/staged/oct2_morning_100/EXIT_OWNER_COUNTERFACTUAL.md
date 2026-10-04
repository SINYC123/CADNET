# Exit-owner counterfactual — propose only

Mode: COUNTERFACTUAL
APPLY: NOT_APPLIED
ARMED: false
Status: BLOCKED_INPUTS
Counterfactual P&L: BLOCKED
Proposed exit owner: `keep_peak_look`
Incumbent exit owner: `as_traded_giveback`
Ultra Ratchet armed: false
Chandelier: untouched
Bars written to disk: 0

This overlay does not submit, does not arm a bot, and does not retune an exit. The 08:30 hour is not invented. Quote bars are not trade bars. A stream-only BBO study cannot stand in for native REST quotes.

## Clocks and size

First-fill target: 09:35 ET. Latest acceptable first fill: 10:30 ET.
Trend notional from the first fill: 100000. Harness default 50000 is the wrong size for the trend lane.
Gates held: midday, FIX-BA, strength, C30, C30-age.
SPY exemption: opens only when own RVOL and trend are both strong, the name is earnings or news, the lane is a trend lane, and the clock is at or before 10:30 ET.

## Cells from catalog.json

First fill by 09:35 (`by_935=HIT`): S001.
Same entry clock, not a new first fill (`SAME_CLOCK`): S002, S003, S004, S005, S006, S007, S008, S009, S010, S011, S012, S013, S014, S015, S016, S017, S018, S019, S020, S021, S022, S023, S024.
First fill only by 10:30: (none).
Journal fills before 09:35: 0. Journal fills before 10:30: 0.
Generator receipt entries by 09:35: 4. Entries by 10:30: 42.

Forced highest-conviction cells (`deadline=force_hc_1030`, n=32):

- BARS_EXIT+SIGNALS: S009, S021
- BARS_EXIT+PEAK+SIGNALS: S010, S011, S012, S022, S023, S024
- SPY_LOG: S033, S034, S035, S036, S045, S046, S047, S048
- TAPE_0830: S057, S058, S059, S060, S069, S070, S071, S072, S081, S082, S083, S084, S093, S094, S095, S096

Journal forced plan: idle=False armed=False symbol=None blocked=missing signals_V1.jsonl, signals_V2.jsonl, signals_V3.jsonl.
Receipt forced plan: idle=True armed=False symbol=None.

08:30 tape cells (`missing` contains TAPE_0830, n=49): S049, S050, S051, S052, S053, S054, S055, S056, S057, S058, S059, S060, S061, S062, S063, S064, S065, S066, S067, S068, S069, S070, S071, S072, S073, S074, S075, S076, S077, S078, S079, S080, S081, S082, S083, S084, S085, S086, S087, S088, S089, S090, S091, S092, S093, S094, S095, S096, S100.
Tape status this run: BLOCKED_INPUTS. 08:30-09:00 trade ticks are absent; no bars were invented.

## Exit-giveback

Priced as-traded giveback books that stayed negative:

- S097 -2647.77 `as_traded_giveback` (reference)
- S098 -2208.95 `as_traded_giveback` (reference)
- S099 -2041.95 `as_traded_giveback` (reference)

Exit-look cells with dollars BLOCKED (not a profit): 97.
Recorded giveback row, cited and not repriced: V1 NKE 227.4 at 11:15:25 ET `EARN TREND GIVEBACK`, peak None.

## Morning receipt versus the SPY exemption

- 09:33:50 AAPL lane `vwap_revert` catalog notional 50000.0 staged notional 50000 resized dollar BLOCKED own_rvol=False trend=False spy_blocks=True
- 09:33:50 NVDA lane `ma2` catalog notional 50000.0 staged notional 100000 resized dollar BLOCKED own_rvol=False trend=True spy_blocks=True
- 09:33:50 MSFT lane `gated930_multi_(s7)` catalog notional 50000.0 staged notional 50000 resized dollar BLOCKED own_rvol=False trend=False spy_blocks=True
- 09:34:00 IWM lane `ma2` catalog notional 50000.0 staged notional 100000 resized dollar BLOCKED own_rvol=False trend=True spy_blocks=True

None of those catalog rows open the exemption. NVDA and IWM are trend names without an RVOL multiple in the reason text. A resized $100k dollar for the trend lanes stays BLOCKED.
