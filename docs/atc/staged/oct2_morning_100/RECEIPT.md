# RECEIPT

APPLY: NOT_APPLIED
ARMED: false
Mode: COUNTERFACTUAL
Ultra Ratchet: unarmed
Chandelier: untouched
Fleet bots: not restarted
Gates held: midday, FIX-BA, strength, C30, C30-age

Nothing in this receipt was applied live. No midday, FIX-BA, strength, C30, or C30-age gate was loosened. Ultra Ratchet was not armed. No bot was restarted.

## Morning-sweep cells

Source: `docs/atc/staged/oct2_morning_100/catalog.json` on the October 2 morning catalog (PR #7 counts, unchanged by the later handoff).

- First fill by 09:35: S001 (`by_935=HIT`). Exit dollars for that cell stay BLOCKED (`BARS_EXIT`).
- Same clock, not a separate first fill: S002, S003, S004, S005, S006, S007, S008, S009, S010, S011, S012, S013, S014, S015, S016, S017, S018, S019, S020, S021, S022, S023, S024.
- First fill only by 10:30: (none). Journal fills before 09:35: 0. Journal fills before 10:30: 0. Generator entries by 09:35: 4. Generator entries by 10:30: 42.
- Forced highest-conviction at 10:30 (n=32): BARS_EXIT+SIGNALS=S009, S021, BARS_EXIT+PEAK+SIGNALS=S010, S011, S012, S022, S023, S024, SPY_LOG=S033, S034, S035, S036, S045, S046, S047, S048, TAPE_0830=S057, S058, S059, S060, S069, S070, S071, S072, S081, S082, S083, S084, S093, S094, S095, S096. Journal plan symbol=None blocked=missing signals_V1.jsonl, signals_V2.jsonl, signals_V3.jsonl. Receipt plan idle=True.
- Missing 08:30 tape (n=49): S049, S050, S051, S052, S053, S054, S055, S056, S057, S058, S059, S060, S061, S062, S063, S064, S065, S066, S067, S068, S069, S070, S071, S072, S073, S074, S075, S076, S077, S078, S079, S080, S081, S082, S083, S084, S085, S086, S087, S088, S089, S090, S091, S092, S093, S094, S095, S096, S100. This run: BLOCKED_INPUTS. No bars written.
- Exit-giveback books that stayed negative: S097 -2647.77, S098 -2208.95, S099 -2041.95. Other exit-look cells with dollars BLOCKED: 97. Recorded V1 NKE giveback stays 227.4 at 11:15:25 ET with peak None. Counterfactual P&L: BLOCKED.

## Three October 2 books

Fresh result: BLOCKED
- journal: fresh BLOCKED computed=NONE target=-2647.77 catalog_cited=-2647.77 catalog_citation=MATCH
- broker: fresh BLOCKED computed=NONE target=-2208.95 catalog_cited=-2208.95 catalog_citation=MATCH
- scorer: fresh BLOCKED computed=NONE target=-2041.95 catalog_cited=-2041.95 catalog_citation=MATCH

catalog_citation is a comparison of `catalog.json` `reference` to the targets. It is not a fresh sum. Fresh computed=NONE means the pack file is not on this checkout.

## Exit owner

Proposed owner `keep_peak_look` replaces nothing. Incumbent owner stays `as_traded_giveback`. Status BLOCKED_INPUTS. Trend notional 100000. SPY exemption stays closed unless own RVOL and trend are both strong, on an earnings or news trend name, at or before 10:30. The four 09:35 catalog entries do not open it.
