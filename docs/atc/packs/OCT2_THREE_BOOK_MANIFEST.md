# Oct 2 three-book pack manifest

Gate id: `oct2-three-book`. Session: **2026-10-02**. Machine list: `harness/oct2_three_book_manifest.json`. Runner: `python3 harness/oct2_three_book.py`.

The totals below are the assertion targets. They are not a measurement from this checkout. The runner prints `computed=NONE` until the file for that book is present. Nothing under `packs/oct2/` is in git yet.

Cancelled Oct 2 sweep cells are not inputs. `bt_invert_validation.py`, `bars_cache_22d.pkl`, and `C:\ATC\atc_data\second_bars\` do not satisfy this gate. Commit `120dec3846783625dc95c06b33791a5af5f3eaf1` is not on `origin`. The Sep 29 MKC hole in that unseen EODHD pack is not an Oct 2 input.

Landing zone is CADNET-relative. One-way copy from STALIE into this tree. No git push from STALIE until these files are present. No write-back to Windows.

## Book 1 — journal closed-trade arithmetic

| | |
|---|---|
| Path | `packs/oct2/journal_closed/batch_c_4162.jsonl` |
| Must contain | One JSON object per Batch C / ledger **#4162** closed trade. Keys: `arm` (`V1`, `V2`, or `V3`), `symbol`, `pnl`. |
| Harness | Drops `NVDA` and `INTC`, then counts and sums `pnl` per arm and combined. |
| Assert | Combined **-2647.77**. V1 **8** trades **+255.87**. V2 **10** trades **-1303.12**. V3 **23** trades **-1600.52**. |
| STALIE | Export of that Batch C set. The CADNET snapshot ends at ledger **#3930**, so this repo does not contain #4162. This book is not `inv_price_v3` ACTUAL. |

A one-line `{"total": -2647.77}` object fails the schema. The runner sums the trade rows.

## Book 2 — broker-day

| | |
|---|---|
| Path | `packs/oct2/broker_day/day_pnl_20261002.jsonl` |
| Must contain | One JSON object per broker-day PnL line for 2026-10-02. Keys: `symbol` (non-empty), `pnl`. |
| Harness | Sums `pnl`. |
| Assert | **-2208.95**. |
| STALIE | Broker day PnL export for 2026-10-02. The 2026-10-02 pack receipt left broker sessions on STALIE. No Windows path for this export was in the synced docs. Do not substitute journal `exit.pl` or the scorer ACTUAL column. |

## Book 3 — scorer ACTUAL (`inv_price_v3`)

Assert: TOTAL column **ACTUAL = -2041.95** on argv `2026-10-02 2026-10-02`.

The runner checks size and sha256, copies the journals to a temp directory, remaps only `BASE` and `BARS` in a temp copy of the scorer, and runs that copy. Those two constants must still be `C:\ATC\claude_harness\inv_20261002` and `C:\ATC\claude_harness\cf12_20261002\data`. Pandas is required for this book only.

| Path | Bytes | sha256 | What it must contain |
|---|---:|---|---|
| `packs/oct2/scorer/inv_price_v3.py` | 12422 | `ee3e9d0b5b4237468c8b40f8b8d3c4fb0952192b505ff55ceebe614f3fe988da` | 2026-10-02 direction pricer. Stdlib + pandas. |
| `packs/oct2/journals/rows_V1.jsonl` | 795643 | `6df1932b33000344ef46d03f7e2f3bad18f92ea69788e3b4a6ef43445252c42a` | V1 journal extract (`flipped`, `pre_submit_side`, `submitted_side`, `filled_side`, exit `pl`). |
| `packs/oct2/journals/rows_V2.jsonl` | 935476 | `28ec1b991bd5e4d2c3451ae561023b0596b2c21d603941fa9b2051b11438740c` | V2 journal extract, same contract. |
| `packs/oct2/journals/rows_V3.jsonl` | 919238 | `23c33bb64f8618474f6dd7905e7f3c76914b63ba7a8f1870e527957ed27379b0` | V3 journal extract, same contract. |
| `packs/oct2/journals/v1_flip_state.json` | 3212 | `5419f167d15a1b431fca0d8663e3a630a48b020d9749db11e386c2470925c7a6` | V1 flip policy and per-entry flags. `account` is `REDACTED`. |
| `packs/oct2/journals/v2_flip_state.json` | 4725 | `b4f1edcf8b7f9fbc1aa9ce8976ce97e3acae0b4980ec49665e5a342f62b5233e` | V2 flip policy and per-entry flags. `account` is `REDACTED`. |
| `packs/oct2/journals/v3_flip_state.json` | 8009 | `e74fc3f7bb31f753e03df685ddf962b33ff7f6b28330b2951f8ceeabfa18de99` | V3 flip policy and per-entry flags. `account` is `REDACTED`. |
| `packs/oct2/journals/inv_price_v3_2026-10-02_2026-10-02.json` | 707 | `5b19381a0914ec555ca4a19fafb393a77c7572a9af700c77da20b4004e8f70e0` | Scorer window summary shipped with the pack. |
| `packs/oct2/bars_sample/bars10s_2026-10-02.csv.gz` | 16264231 | `e615fdcc3669651444e4274ec010a75bb2cd0a49ce288b18127457abb1447ea5` | 10-second bid/ask bars, 2026-10-02, relay Tradier WS tape. |
| `packs/oct2/bars_sample/meta_2026-10-02.json` | 28434 | `2c936fa18b061d4b2938c8db64c5968649793f3b6e57ec86da8d28e60d72c44a` | Meta for that tape (08:55:00–15:59:59 ET, freshness by symbol). |
| `packs/oct2/smoke_inv_price_v3_20261002.txt` | 6934 | `d27974cbc65797559e574ee1d7aea113fd5be7a016d6896996926df312156219` | STALIE smoke print. Reference file. The gate reruns the scorer. |

STALIE sources for this book: `C:\ATC\claude_harness\inv_20261002\` and `C:\ATC\claude_harness\cf12_20261002\data\bars10s_2026-10-02.csv.gz` plus `meta_2026-10-02.json`, and the smoke file from the 2026-10-02 pack receipt.

Hashes above are the receipt of the untracked cloud unzip (`cloud_bt_pack_20261002`, prior run `bc-56424836-bfa7-515f-b919-3fd4ddbcf3c3`). A different hash is a FAIL, not a silent rerun.
