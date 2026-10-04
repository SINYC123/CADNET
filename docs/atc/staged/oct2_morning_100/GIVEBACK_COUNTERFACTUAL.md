# Giveback counterfactual — stage only

Status: BLOCKED_INPUTS
ARMED: false
Ultra Ratchet armed: false
Chandelier: untouched
Counterfactual P&L: BLOCKED
Peak invented: false

Nothing in this overlay submits an order, retunes an exit, arms Ultra Ratchet, or writes a chandelier parameter.

## Recorded evidence

V1 NKE 227.40 at 11:15:25 ET, reason `EARN TREND GIVEBACK`, peak field None.
Journal value is 227.4 (`journal exit pl 227.4 on rows_V1.jsonl`). This overlay does not replace that figure and does not invent the missing peak.

Recorded startup peak-lock on the V1 row, cited and not retuned: keep 0.80 / take 0.90.

## Inputs checked

- `/tmp/oct2_pack/oct2_pack`: absent
- `/workspace/oct2_pack`: absent
- `/workspace/oct2_pack/oct2_pack`: absent

- bars10s: absent
- native REST quotes: absent

Required bar path: `C:\ATC\claude_harness\cf12_20261002\data\bars10s_2026-10-02.csv.gz`
sha256 `e615fdcc3669651444e4274ec010a75bb2cd0a49ce288b18127457abb1447ea5`
Pack-relative `bars10s_2026-10-02.csv.gz`

native REST quote tape for 2026-10-02 (absent from this repo pack; the 31-file oct2_pack inventory has no quote capture; stream BBO / bars10s bid_o ask_o cannot stand in)

cf12 `bars10s` columns are 10-second BBO (`bid_o` / `ask_o`). Quote bars are not trade bars. A stream-only exit study cannot stand in for native REST quotes. Both inputs are required before a keep-peak look can be priced. This run did not price one.

## What stays blocked

Keep-peak, trend-keep-peak, and peak-lock keep 0.80 / take 0.90 stay looks. Dollar cells that need them stay BLOCKED. The 49-cell 08:30 tape block is unchanged. The three reference books stay the only priced dollars.
