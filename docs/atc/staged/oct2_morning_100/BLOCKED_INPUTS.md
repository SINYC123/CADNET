# BLOCKED_INPUTS — 08:30–09:00 bar handoff (S100 family)

Status: BLOCKED_INPUTS
ARMED: false
Bars written: 0
EVAL_START: 08:30 ET
Finder skip floor: 09:30 ET
Window: 08:30:00 inclusive to 09:00:00 exclusive
Minimum bar count: none (09:30 is not a minimum bar count)

This run did not fabricate ticks, bars, fills, or P&L.

## Checked in this repo

- `/tmp/oct2_pack/oct2_pack`: absent
- `/workspace/oct2_pack`: absent
- `/workspace/oct2_pack/oct2_pack`: absent
- `/workspace/docs/atc/staged/oct2_morning_100`: present (staged catalog only, not a tick pack)

`bars10s_2026-10-02.csv.gz` in those roots: absent

The unpacked `oct2_pack` inventory is 31 files (journals, broker day, scorer, entry-generator receipt). It contains no tick file, no `meta_2026-10-02.json`, and no `bars10s_2026-10-02.csv.gz`. That tarball is not in this checkout. This run searched the paths above and did not find a substitute.

## What STALIE must pack to unblock the 49 cells

1. Raw trade ticks for 2026-10-02 08:30:00–09:00:00 ET.
   Clock field `received_ts` (the clock `build_bars.py` uses).
   Trade price field (`price`, `trade_px`, `px`, `last`, or `trade_price`). Bid/ask is not a trade.
   Exact filename is not in this repo. Drop the file into the pack where this builder can see a tick/trade/tape name.
   Pack-relative slot: `oct2_pack/` raw trade ticks covering that window.

2. And/or `C:\ATC\claude_harness\cf12_20261002\data\bars10s_2026-10-02.csv.gz`
   sha256 `e615fdcc3669651444e4274ec010a75bb2cd0a49ce288b18127457abb1447ea5`
   Pack-relative name: `bars10s_2026-10-02.csv.gz`
   That file is cf12 10-second BBO (`symbol`, `t`, `bid_o`, `ask_o`). Quote bars are not trade bars.
   The October 2 simulation starts at 09:00, so this file is not the 08:30 hour. It is still required for a later exit replay. A resized dollar stays BLOCKED while it is absent.

## Cells

49 cells, including handoff S100, stay `TAPE_0830`. Building this window does not move the finder skip floor off 09:30 and does not arm a rule.
