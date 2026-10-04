# October 2 morning scenarios — what is still blocked

Draft only. This catalog does not arm a bot, does not merge, and does not change an exit.

## Counts

| | |
|---|---|
| Cells | 100 |
| Dollar-priced | 3 |
| Dollar BLOCKED | 97 |
| Observed set that hits a trade by 9:35 ET | 1 (S001) |
| Cells that reuse that entry clock | 23 |
| Failed the 9:35 bar | 3 |
| Failed the 10:30 bar | 3 |
| Time-bar BLOCKED | 73 |
| Of which missing the 08:30 tape | 49 |
| Of which missing a SPY-gate record | 24 |

The morning number is a trade that can print by 9:35 ET, with 10:30 ET as the latest acceptable first fill. The 3 priced cells are the three reference books. They fail both clocks. No knob cell has a dollar.

## Reference books (cited from the pack)

| Book | Dollars | Source in the pack |
|---|---:|---|
| Journal synthetic ENTRY pairing | -2647.77 | `journal_closed/batch_c_4162.jsonl` (41 cycles) and `journal_closed/batch_C.md` |
| Broker day | -2208.95 | `broker_day/day_pnl_20261002.jsonl` |
| Scorer ACTUAL | -2041.95 | `journals/inv_price_v3_2026-10-02_2026-10-02.json` and `smoke_inv_price_v3_20261002.txt` |

First October 2 journal fill: 11:09:03 ET V3 TSLA (gated930_vwap), notional 50131. Journal fills before 09:35: 0. Journal fills before 10:30: 0. That day fails the new bar.

## The set that hits

S001 is the packaged entry-generator receipt (`entry_generator/demo_entries_pre1030_sample.jsonl`): premarket hour absent, harness notional 50000. `entry_generator.py` has no SPY check. The finder skip floor is 09:30 (`DEFAULT_SESSION_OPEN`). These sim entries are in the pack. Exit dollars for them are BLOCKED.

- 09:33:50 ET V2 AAPL sell vwap_revert score 4 entry 332.19 qty 150 at notional 50000.0
- 09:33:50 ET V2 NVDA sell ma2 score 6 entry 235.15 qty 212 at notional 50000.0
- 09:33:50 ET V3 MSFT buy gated930_multi_(s7) score 6 entry 520.2 qty 96 at notional 50000.0
- 09:34:00 ET V2 IWM sell ma2 score 6 entry 282.23 qty 177 at notional 50000.0

23 other cells (premarket absent, SPY off for the strong-own-RVOL trend case) stay on this same entry clock. A 100000 size, a different exit look, or the 10:30 forced-submit flag leaves the dollar cell BLOCKED. On this receipt the forced rule stays idle, because a sim entry is already on the book before 10:30.

The generator receipt is the source of these four entries. NVDA and IWM are `[TREND-RAW]` MA2 names and the reason text has no RVOL multiple, so the SPY waiver stays closed for them. The only explicit RVOL in the pre-10:30 sample is SPCX at 09:59:10 ET (`RVOL=3.5x`), which is after 09:35 and before 10:30, and that row is a continuation name. The dollar difference between SPY on and SPY off is BLOCKED.

## Still blocked

- **08:30–09:00 tape.** 49 cells, including the handoff cell S100, need the hour so a name at 09:30 already has 60 minutes of bars. 09:30 remains the finder skip floor. Missing file: raw tick tape 2026-10-02 08:30-09:00 ET (not in oct2_pack; bars10s_2026-10-02.csv.gz was omitted from the pack and the October 2 simulation starts at 09:00). `rules_staged.EVAL_START` is 08:30 and the tape slot is empty. This run left that hour unbuilt.
- **SPY-on cells.** 24 cells. Missing file: a SPY-gate decision record, and the signal files C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V1.jsonl, C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V2.jsonl, C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V3.jsonl. Midday, FIX-BA, strength, and C30 are unchanged in `rules_staged.GATES_HELD`.
- **Exit giveback look.** Recorded giveback rows:
  - V1 11:15:25 ET NKE P/L 227.4 reason EARN TREND GIVEBACK; peak field None
  Keep-peak, trend-keep-peak, and the recorded peak-lock keep 0.80 / take 0.90 are looks. Journal exits store no peak. Exit replay needs `C:\ATC\claude_harness\cf12_20261002\data\bars10s_2026-10-02.csv.gz`. The look leaves the chandelier and Ultra Ratchet untouched.
- **Forced 10:30 submit.** Staged in `rules_staged.stage_forced_highest_conviction`. `ARMED` is False. On the journal book the rule is eligible (0 fills by 10:30). The name is BLOCKED. Missing files: C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V1.jsonl, C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V2.jsonl, C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V3.jsonl.
- **Trend size.** Staged trend notional is 100000 from the first fill. The packaged harness default is 50000. Measured October 2 fill notionals step up later on V1 and V2 and stay near 50k on V3. First `earn_trend` fill is 11:10:49 ET V1 NKE notional 50058. A later 100k fill on that lane is 12:47:45 ET V1 NKE notional 100107. Startup `ATC_SLOT_AM` on the 11:06 ET rows is 100000, and the first fills of the day are still about 50k. A 100k replay dollar is BLOCKED because `bars10s_2026-10-02.csv.gz` is not in the pack.

## How this was scored

`score_scenarios.py` reads the unpacked pack, checks the three reference totals, counts journal fills against 09:35 and 10:30, and reads the packaged generator receipt. Cells that need the 08:30 tape stay BLOCKED. The script refuses to run when `rules_staged.ARMED` is true.
