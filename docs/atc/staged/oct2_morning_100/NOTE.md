# October 2 morning scenarios — what is still blocked

Draft only. This catalog does not arm a bot, does not merge, and does not change an exit.

## This stage

`ARMED` is false. Ultra Ratchet is unarmed. The chandelier is untouched. Nothing here merges and nothing is applied live.

`build_bars10s_0830.py` is the S100 handoff. It builds 10-second trade bars for 2026-10-02 08:30:00–09:00:00 ET only from raw trade ticks already in the pack. `EVAL_START` stays 08:30. The finder skip floor stays 09:30. 09:30 is not a minimum bar count. This checkout has no raw ticks, so the run wrote no bars. Status: **BLOCKED_INPUTS** (`BLOCKED_INPUTS.md`). The 49 cells that need that hour, including S100, stay blocked. Prior counts are unchanged: 100 cells, 3 dollar-priced reference books (journal -2647.77 / broker -2208.95 / scorer -2041.95), 97 dollar BLOCKED, only S001 hits a trade by 09:35 on the packaged generator receipt.

`giveback_counterfactual.py` is a stage-only keep-peak / giveback overlay. It cites the recorded V1 NKE +227.40 at 11:15:25 ET (`EARN TREND GIVEBACK`, peak field None) and does not invent a peak or a P&L. `bars10s_2026-10-02.csv.gz` and a native REST quote tape are both absent, so the overlay is **BLOCKED_INPUTS** (`GIVEBACK_COUNTERFACTUAL.md`). Quote bars are not trade bars. A stream-only BBO study cannot stand in for native REST quotes.

Staged trend notional stays **$100,000** from the first fill. The harness default of $50,000 is the wrong size for that lane. A resized dollar stays BLOCKED while the bar file is missing.

The SPY waiver stays an exemption for earnings/news-strength names with high own RVOL and trend, through 10:30 only. Ordinary names keep the SPY check. Midday, FIX-BA, strength, and C30 stay held. `stage_forced_highest_conviction` stays unarmed.

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

The generator receipt is the source of these four entries. NVDA and IWM are `[TREND-RAW]` MA2 names and the reason text has no RVOL multiple, so the SPY waiver stays closed for them. The waiver opens only for an earnings/news-strength name that also has high own RVOL and trend, and only through 10:30. Ordinary names stay blocked. The only explicit RVOL in the pre-10:30 sample is SPCX at 09:59:10 ET (`RVOL=3.5x`), which is after 09:35 and before 10:30, and that row is a continuation name. The dollar difference between SPY on and SPY off is BLOCKED.

## Still blocked

- **08:30–09:00 tape.** 49 cells, including the handoff cell S100, need the hour so a name at 09:30 already has 60 minutes of bars. 09:30 remains the finder skip floor and is not a minimum bar count. Missing file: raw trade ticks 2026-10-02 08:30:00-09:00:00 ET (clock field `received_ts`; no tick file in oct2_pack) and/or `C:\ATC\claude_harness\cf12_20261002\data\bars10s_2026-10-02.csv.gz` (sha256 e615fdcc3669651444e4274ec010a75bb2cd0a49ce288b18127457abb1447ea5; omitted from the pack; the October 2 simulation starts at 09:00; quote bars are not trade bars). `rules_staged.EVAL_START` is 08:30. `build_bars10s_0830.py` builds that window only from raw trade ticks already in the pack. This checkout has none, so the handoff status is BLOCKED_INPUTS (`BLOCKED_INPUTS.md`) and no bars were written.
- **SPY-on cells.** 24 cells. Missing file: a SPY-gate decision record, and the signal files C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V1.jsonl, C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V2.jsonl, C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V3.jsonl. Midday, FIX-BA, strength, and C30 are unchanged in `rules_staged.GATES_HELD`.
- **Exit giveback look.** Recorded giveback rows:
  - V1 11:15:25 ET NKE P/L 227.4 reason EARN TREND GIVEBACK; peak field None
  Keep-peak, trend-keep-peak, and the recorded peak-lock keep 0.80 / take 0.90 are looks. Journal exits store no peak. The staged counterfactual (`giveback_counterfactual.py`, `GIVEBACK_COUNTERFACTUAL.md`) cites V1 NKE +227.40 at 11:15:25 ET and does not invent a peak. It stays BLOCKED_INPUTS while `C:\ATC\claude_harness\cf12_20261002\data\bars10s_2026-10-02.csv.gz` or a native REST quote tape is missing. Quote bars are not trade bars. A stream-only BBO study cannot stand in for native REST quotes. The look leaves the chandelier and Ultra Ratchet untouched.
- **Forced 10:30 submit.** Staged in `rules_staged.stage_forced_highest_conviction`. `ARMED` is False. On the journal book the rule is eligible (0 fills by 10:30). The name is BLOCKED. Missing files: C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V1.jsonl, C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V2.jsonl, C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V3.jsonl.
- **Trend size.** Staged trend notional is locked at 100000 from the first fill (`trend_notional_from_first_fill`). The packaged harness default is 50000, and that default is the wrong trend size. Measured October 2 fill notionals step up later on V1 and V2 and stay near 50k on V3. First `earn_trend` fill is 11:10:49 ET V1 NKE notional 50058. A later 100k fill on that lane is 12:47:45 ET V1 NKE notional 100107. Startup `ATC_SLOT_AM` on the 11:06 ET rows is 100000, and the first fills of the day are still about 50k. A resized 100k dollar stays BLOCKED because `bars10s_2026-10-02.csv.gz` is not in the pack.

## How this was scored

`score_scenarios.py` reads the unpacked pack, checks the three reference totals, counts journal fills against 09:35 and 10:30, and reads the packaged generator receipt. Cells that need the 08:30 tape stay BLOCKED. `build_bars10s_0830.py` and `giveback_counterfactual.py` are stage-only and refuse to invent bars or peaks. The script refuses to run when `rules_staged.ARMED` is true. The pack is not on this checkout, so `score_scenarios.py` was not re-run; the 100-cell table and the three reference dollars are unchanged.
