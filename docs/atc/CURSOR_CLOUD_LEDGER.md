# Cursor cloud ledger

Orchestrator log for the CADNET copy of the ATC QA pack (`docs/atc`).

This file is **not** `C:\ATC\claude_link\messages.jsonl`. That bus lives on STALIE-MINI and is not mounted in this cloud VM. IDs here use the `CC-` prefix so they cannot collide with Windows ledger row numbers. The last synced Windows rows are in `LEDGER_SNAPSHOT_20261002.md` (generated 2026-10-02T13:00:09-04:00, last row **#3930**).

Mode for every tick: **stage for review**. No live APPLY, no paper promote, no Push-to-Fleet arm, no bake-off firing, no gate loosen, unless a later Farid GO is written into this ledger first.

---

## CC-0001 — 2026-10-02 17:55 ET — first 20-minute check armed

**Who:** Cursor cloud orchestrator  
**Source read:** `LEDGER_SNAPSHOT_20261002.md` (#3891–#3930), `OPEN_ACTION_PLAN_20261002.md` (updated 12:55 ET), `PRE_DEPLOY_QA_ALIGNMENT.md`, `BOT_BAKEOFF_SCOREBOARD.md`, `INVERT_SIGNALS_ORIGIN_20261002.md`  
**Git:** `origin/main` @ `9b2bdf4` (`ATC QA sync 2026-10-02 pre-1pm`). No newer sync after the 13:00 ET snapshot.

### Work changes since the action plan (12:55 ET)

| Windows row | What changed | Plan item |
|---|---|---|
| #3929 | V2 CHALLENGER `:5051` `INVERT_SIGNALS` killed OFF. Live `gate_status.invert_signals=False`; `CHALLENGER\atc_state.json` false. | P0 #4 was OPEN. Marked **DONE-SNAPSHOT**. This VM cannot re-probe the port. |
| #3930 | #3886 annotated closed SATISFIED. JOB A via #3897/#3899. JOB B via #3895. No reassign. | P2 #6 was DONE-work / STALE-row. Marked **DONE**. |

### Still open (stage-only; no Farid secret required)

| Item | Why an agent | Blocked on |
|---|---|---|
| Bake-off cycle 1 Cursor baseline | Scoreboard row is empty. Equivalent task: INV default audit + staged OFF-default proposal. | Nothing in-repo. Live re-toggle is out of scope. |
| P0 #7 QA-align confirm gates | MD is synced. Enforcer scripts (`confirm_qa_alignment.py`, `require_qa_alignment.py`) are **not** in this repo. | Live wire stays on STALIE-MINI. Agent stages the gap and a checklist only. |
| P3 remint Ready `6EC1` → `F37DA134` | Deadline before 03:30 ET Sat 2026-10-03. Ledger #3910: Ready tasks still pinned to `6EC1DEA3FD2749C0`; zero Ready carry `F37DA134D15D15EC`. | Execution is Grok on the box. Agent stages the preflight only. |
| P1 paper V1–V3 refuse mix, V4-CF12 first fill, V4 on `:5053` | Evidence only exists as ledger prose. | Live ports. Folded into the remint/P1 evidence agent. |
| P1 V4 Tradier VA4414585 401 | Sandbox token missing. | **Farid.** No agent. |
| P2 Push-to-Fleet S1–S10 arm | Needs QA-align confirm + Farid GO. | **Farid GO.** No agent. |

### Agents staged this tick

Three cloud agents, disjoint output paths, draft PRs for review. Count matches the three independent stage-only threads above. No fourth agent for the Tradier token or fleet arm.

| Agent | Output path | Run |
|---|---|---|
| Cycle 1 INV audit | `docs/atc/staged/20261002/cursor_cycle1_inv_off_default.md` | [Cycle 1 INV audit](bc-6aaa4b25-a72c-520c-9b00-6cf926d39612) — draft https://github.com/SINYC123/CADNET/pull/5 |
| QA-align seal gap | `docs/atc/staged/20261002/qa_align_seal_gap.md` | [QA-align seal gap](bc-435d5cb0-ffaf-531b-9088-cacf7c61b27d) — draft https://github.com/SINYC123/CADNET/pull/3 |
| Remint preflight + P1 evidence | `docs/atc/staged/20261002/remint_f37_and_p1_evidence.md` | [Remint and P1 evidence](bc-33825a34-162e-5a02-9409-3300b056f5fc) — draft https://github.com/SINYC123/CADNET/pull/4 |

Orchestrator review PR for this tick: https://github.com/SINYC123/CADNET/pull/2 (draft). Agent draft PRs land separately when those runs finish. Do not launch duplicates of these three threads until those PRs are reviewed or the underlying ledger rows change.

### Loop

Timer `atc-ledger-20m` ran every 20 minutes until it was stopped at 20:21 ET (CC-0012). Do not re-arm it unless asked.

---

## CC-0002 — 2026-10-02 18:01 ET — QA-align branch staged for review

**Who:** Cursor cloud orchestrator, follow-up after [QA-align seal gap](bc-435d5cb0-ffaf-531b-9088-cacf7c61b27d) finished.

The run pushed `cursor/qa-align-seal-gap-b27d` at `4a61e95` (one file: `docs/atc/staged/20261002/qa_align_seal_gap.md`) and could not open a pull request from its own session. Orchestrator opened the draft.

**Review:** https://github.com/SINYC123/CADNET/pull/3

**Finding:** Checklist markdown is in-repo. Confirm tool, require tool, `pre_deploy_audit.py`, `run_pre_deploy_audit.bat`, `REQUIRED_CHECKS.json`, receipts, `AGENTS.md`, `claude_link/PROTOCOL.md`, and `messages.jsonl` are absent. A1–A4 and A6 are not-verifiable here. A5 fails closed because the audit script and receipts are missing. This note is not a `code_finish` or `deploy` receipt.

No duplicate agent. Cycle 1 INV audit and remint/P1 evidence were still running at this row.

---

## CC-0003 — 2026-10-02 18:02 ET — remint/P1 brief staged for review

**Who:** Cursor cloud orchestrator, follow-up after [Remint and P1 evidence](bc-33825a34-162e-5a02-9409-3300b056f5fc) finished.

The run pushed `cursor/stage-remint-f37-p1-evidence-f5fc` at `796e5c4` (one file: `docs/atc/staged/20261002/remint_f37_and_p1_evidence.md`) and could not open a pull request from its own session. Orchestrator opened the draft.

**Review:** https://github.com/SINYC123/CADNET/pull/4

**Finding:** #3910 still has Ready tasks pinned to `6EC1DEA3FD2749C0` and zero Ready carry of `F37DA134D15D15EC`. Overnight Recovery/Recheck next 2026-10-03 03:30/03:50. Remint stays on STALIE-MINI before 03:30 ET Saturday, and only after a fresh deploy receipt. Receipt tools are not in this repo. P1 paper, V4-CF12 fill, Tradier 401, and shadow s7/s8 stay evidence-only. No remint was run.

No duplicate agent. Cycle 1 INV audit was still outstanding at this row.

---

## CC-0004 — 2026-10-02 18:03 ET — cycle 1 INV audit staged for review

**Who:** Cursor cloud orchestrator, follow-up after [Cycle 1 INV audit](bc-6aaa4b25-a72c-520c-9b00-6cf926d39612) finished.

The run pushed `cursor/cycle1-inv-off-default-audit-9612` at `e41b9a1` (one file: `docs/atc/staged/20261002/cursor_cycle1_inv_off_default.md`) and could not open a pull request from its own session. Orchestrator opened the draft.

**Review:** https://github.com/SINYC123/CADNET/pull/5

**Finding:** Stage only. A1 requires INV default OFF unless a named per-version Farid GO; these files record none. Origin doc still shows code default True (2026-04-28 BT), `default+`/`default` forcing True, and Continue restore. #3929 remains the latest evidence that V2 was killed OFF; do not turn it back ON. V1, V4-CF12, and shadow have no `invert_signals` proof in the synced pack. Documentary `code_finish` stamp only: A1 fail, A4 fail, A6 fail, A2/A3/A5 not-in-repo. No rubric score. Bake-off cycle 1 stays unscored until Claude (#3922) and Codex (#3923) findings land.

All three CC-0001 threads now have draft reviews: https://github.com/SINYC123/CADNET/pull/3, https://github.com/SINYC123/CADNET/pull/4, https://github.com/SINYC123/CADNET/pull/5. Do not relaunch them unless the ledger changes.

---

## CC-0005 — 2026-10-02 18:11 ET — 20-minute tick, no new work

**Who:** Cursor cloud orchestrator. Timer `atc-ledger-20m` delivery 1. Subscription still active through 2026-10-09.

**Read:** `CURSOR_CLOUD_LEDGER.md` through CC-0004, `LEDGER_SNAPSHOT_20261002.md` (unchanged, last row #3930), `OPEN_ACTION_PLAN_20261002.md` on this branch, `BOT_BAKEOFF_SCOREBOARD.md` (identical to `origin/main`), `PRE_DEPLOY_QA_ALIGNMENT.md` (identical to `origin/main`).

**Git:** `origin/main` still `9b2bdf4`. This branch advanced only by CC-0002 through CC-0004 (`e4fe065`). No new Windows snapshot.

**Reviews already open (do not relaunch):**

| Thread | Review | State |
|---|---|---|
| [QA-align seal gap](bc-435d5cb0-ffaf-531b-9088-cacf7c61b27d) | https://github.com/SINYC123/CADNET/pull/3 | draft, open |
| [Remint and P1 evidence](bc-33825a34-162e-5a02-9409-3300b056f5fc) | https://github.com/SINYC123/CADNET/pull/4 | draft, open |
| [Cycle 1 INV audit](bc-6aaa4b25-a72c-520c-9b00-6cf926d39612) | https://github.com/SINYC123/CADNET/pull/5 | draft, open |

**Agents staged this tick:** none. The three stage-only threads are already in review, and the snapshot did not change.

**Still blocked:** V4 Tradier VA4414585 sandbox token (Farid). Push-to-Fleet arm (Farid GO). Live remint, paper refuse mix, and V4-CF12 fill measurement (STALIE-MINI, not this VM). Bake-off cycle 1 score (waiting on Claude #3922 and Codex #3923).

---

## CC-0006 — 2026-10-02 18:32 ET — 20-minute tick, no new work

**Who:** Cursor cloud orchestrator. Timer `atc-ledger-20m` delivery 2. Subscription still active through 2026-10-09.

**Read:** ledger through CC-0005, snapshot on `origin/main` (still ends at #3930), action plan on this branch, scoreboard and QA alignment identical to `origin/main` (`9b2bdf4`).

**Git tips unchanged:**

| Ref | SHA |
|---|---|
| `main` | `9b2bdf4` |
| `cursor/qa-align-seal-gap-b27d` | `4a61e95` |
| `cursor/stage-remint-f37-p1-evidence-f5fc` | `796e5c4` |
| `cursor/cycle1-inv-off-default-audit-9612` | `e41b9a1` |

Reviews https://github.com/SINYC123/CADNET/pull/3, https://github.com/SINYC123/CADNET/pull/4, and https://github.com/SINYC123/CADNET/pull/5 still resolve. No CI checks reported. `gh pr list` returned 401 this tick; branch tips and PR lookups were used instead.

**Agents staged this tick:** none. No snapshot change and no new commits on the three review branches.

**Still blocked:** Tradier sandbox token (Farid). Push-to-Fleet arm (Farid GO). Live remint, paper refuse mix, and V4-CF12 fill (STALIE-MINI). Bake-off cycle 1 score (waiting on #3922 and #3923).

Push of this row failed at 18:32 ET (`Invalid username or token`). The commit stayed local as `ac3bec1`.

---

## CC-0007 — 2026-10-02 18:53 ET — 20-minute tick, no new work

**Who:** Cursor cloud orchestrator. Timer `atc-ledger-20m` delivery 3. Subscription still active through 2026-10-09.

**Read:** ledger through CC-0006, snapshot on `origin/main` (still ends at #3930), action plan on this branch, scoreboard and QA alignment identical to `origin/main` (`9b2bdf4`).

**Git tips unchanged:**

| Ref | SHA |
|---|---|
| `main` | `9b2bdf4` |
| `cursor/qa-align-seal-gap-b27d` | `4a61e95` |
| `cursor/stage-remint-f37-p1-evidence-f5fc` | `796e5c4` |
| `cursor/cycle1-inv-off-default-audit-9612` | `e41b9a1` |

Reviews https://github.com/SINYC123/CADNET/pull/3, https://github.com/SINYC123/CADNET/pull/4, and https://github.com/SINYC123/CADNET/pull/5 still resolve. No CI checks reported.

**Agents staged this tick:** none. No snapshot change and no new commits on the three review branches.

**Push retry:** the VM git token file was rewritten at 22:53:33Z. This tick pushes CC-0006 with CC-0007.

**Still blocked:** Tradier sandbox token (Farid). Push-to-Fleet arm (Farid GO). Live remint, paper refuse mix, and V4-CF12 fill (STALIE-MINI). Bake-off cycle 1 score (waiting on #3922 and #3923).

---

## CC-0008 — 2026-10-02 19:15 ET — 20-minute tick, no new work

**Who:** Cursor cloud orchestrator. Timer `atc-ledger-20m` delivery 4. Subscription still active through 2026-10-09.

**Read:** ledger through CC-0007, snapshot on `origin/main` (still ends at #3930), action plan on this branch, scoreboard and QA alignment identical to `origin/main` (`9b2bdf4`).

**Remote heads (only these five):**

| Ref | SHA |
|---|---|
| `main` | `9b2bdf4` |
| `cursor/atc-ledger-20m-46d8` | `a333104` |
| `cursor/qa-align-seal-gap-b27d` | `4a61e95` |
| `cursor/stage-remint-f37-p1-evidence-f5fc` | `796e5c4` |
| `cursor/cycle1-inv-off-default-audit-9612` | `e41b9a1` |

No new branch and no new snapshot. Reviews https://github.com/SINYC123/CADNET/pull/3, https://github.com/SINYC123/CADNET/pull/4, and https://github.com/SINYC123/CADNET/pull/5 still resolve. No CI checks reported.

**Agents staged this tick:** none.

**Still blocked:** Tradier sandbox token (Farid). Push-to-Fleet arm (Farid GO). Live remint, paper refuse mix, and V4-CF12 fill (STALIE-MINI). Bake-off cycle 1 score (waiting on #3922 and #3923).

---

## CC-0009 — 2026-10-02 19:35 ET — 20-minute tick, no new work

**Who:** Cursor cloud orchestrator. Timer `atc-ledger-20m` delivery 5. Subscription still active through 2026-10-09.

**Read:** ledger through CC-0008, snapshot on `origin/main` (still ends at #3930), action plan on this branch, scoreboard and QA alignment identical to `origin/main` (`9b2bdf4`).

**Remote heads (only these five):**

| Ref | SHA |
|---|---|
| `main` | `9b2bdf4` |
| `cursor/atc-ledger-20m-46d8` | `a340f16` |
| `cursor/qa-align-seal-gap-b27d` | `4a61e95` |
| `cursor/stage-remint-f37-p1-evidence-f5fc` | `796e5c4` |
| `cursor/cycle1-inv-off-default-audit-9612` | `e41b9a1` |

The only SHA change since CC-0008 is this ledger branch, from the prior tick. Reviews https://github.com/SINYC123/CADNET/pull/3, https://github.com/SINYC123/CADNET/pull/4, and https://github.com/SINYC123/CADNET/pull/5 still resolve. No CI checks reported.

**Agents staged this tick:** none.

**Still blocked:** Tradier sandbox token (Farid). Push-to-Fleet arm (Farid GO). Live remint, paper refuse mix, and V4-CF12 fill (STALIE-MINI). Bake-off cycle 1 score (waiting on #3922 and #3923). Remint deadline remains before 03:30 ET Saturday 2026-10-03; the preflight review is already open and was not relaunched.

---

## CC-0010 — 2026-10-02 19:41 ET — early tick, no new work

**Who:** Cursor cloud orchestrator. Timer `atc-ledger-20m` delivery 6, about six minutes after delivery 5. Subscription still active through 2026-10-09. Same timer; not re-armed.

**Read:** ledger through CC-0009, snapshot on `origin/main` (still ends at #3930), action plan on this branch, scoreboard and QA alignment identical to `origin/main` (`9b2bdf4`).

**Remote heads (only these five):**

| Ref | SHA |
|---|---|
| `main` | `9b2bdf4` |
| `cursor/atc-ledger-20m-46d8` | `c667709` |
| `cursor/qa-align-seal-gap-b27d` | `4a61e95` |
| `cursor/stage-remint-f37-p1-evidence-f5fc` | `796e5c4` |
| `cursor/cycle1-inv-off-default-audit-9612` | `e41b9a1` |

The only SHA change since CC-0009 is this ledger branch, from that tick. Reviews https://github.com/SINYC123/CADNET/pull/3, https://github.com/SINYC123/CADNET/pull/4, and https://github.com/SINYC123/CADNET/pull/5 still resolve. No CI checks reported.

**Agents staged this tick:** none.

**Still blocked:** Tradier sandbox token (Farid). Push-to-Fleet arm (Farid GO). Live remint, paper refuse mix, and V4-CF12 fill (STALIE-MINI). Bake-off cycle 1 score (waiting on #3922 and #3923). Remint deadline remains before 03:30 ET Saturday 2026-10-03; the preflight review stays open and was not relaunched.

---

## CC-0011 — 2026-10-02 20:02 ET — 20-minute tick, no new work

**Who:** Cursor cloud orchestrator. Timer `atc-ledger-20m` delivery 7, about 21 minutes after delivery 6. Subscription was active through 2026-10-09 until CC-0012 stopped it.

**Read:** ledger through CC-0010, snapshot on `origin/main` (still ends at #3930), action plan on this branch, scoreboard and QA alignment identical to `origin/main` (`9b2bdf4`).

**Remote heads (only these five):**

| Ref | SHA |
|---|---|
| `main` | `9b2bdf4` |
| `cursor/atc-ledger-20m-46d8` | `e7007cd` |
| `cursor/qa-align-seal-gap-b27d` | `4a61e95` |
| `cursor/stage-remint-f37-p1-evidence-f5fc` | `796e5c4` |
| `cursor/cycle1-inv-off-default-audit-9612` | `e41b9a1` |

The only SHA change since CC-0010 is this ledger branch, from that tick. Reviews https://github.com/SINYC123/CADNET/pull/3, https://github.com/SINYC123/CADNET/pull/4, and https://github.com/SINYC123/CADNET/pull/5 still resolve. No CI checks reported.

**Agents staged this tick:** none.

**Still blocked:** Tradier sandbox token (Farid). Push-to-Fleet arm (Farid GO). Live remint, paper refuse mix, and V4-CF12 fill (STALIE-MINI). Bake-off cycle 1 score (waiting on #3922 and #3923). Remint deadline remains before 03:30 ET Saturday 2026-10-03; the preflight review stays open and was not relaunched.

---

## CC-0012 — 2026-10-02 20:21 ET — 20-minute cycle stopped

**Who:** Cursor cloud orchestrator, on Farid's request: "Stop cloud 20 min cycle."

Closed timer `atc-ledger-20m` (`sub_4b43ffb2-7ede-4d10-9125-727ded454baf`). Unsubscribe returned closed. It had delivered 7 times; the last was CC-0011 at 20:02 ET. It is not re-armed.

No new agents. The three draft reviews stay open for review and were not closed by this stop:

- https://github.com/SINYC123/CADNET/pull/3
- https://github.com/SINYC123/CADNET/pull/4
- https://github.com/SINYC123/CADNET/pull/5

Orchestrator PR remains https://github.com/SINYC123/CADNET/pull/2.

---

## CC-0013 — 2026-10-03 19:35 ET — Oct 2 three-book harness BLOCKED

**Who:** Cursor cloud, standing order 2026-10-03. Run [Oct-2 three-book harness validation](https://cursor.com/agents/bc-1b70cb47-73b2-5086-ad47-ce2cb278f734).

**Mode:** draft only. No live APPLY, no fleet restart, no gate loosen, no ratchet, no parameter sweep. Cancelled Oct 2 sweep cells are not results and are not inputs.

**Git inventory:** `origin/main` is still `9b2bdf4` (docs only). No journals, no broker-day file, no `inv_price_v3.py`, no tape, no harness on that tip. Commit `120dec3846783625dc95c06b33791a5af5f3eaf1` is not on this remote (commit API: no such SHA) and not in the local object store. The Sep 29 MKC gap belongs to that unseen EODHD pack. It is not an input to this gate, and EODHD second bars are not a substitute for the Tradier 10-second tape.

**Prior cloud pack (not in git):** [CADNET cloud backtest probe](https://cursor.com/agents/bc-56424836-bfa7-515f-b919-3fd4ddbcf3c3) unzipped `cloud_bt_pack_20261002` and ran `inv_price_v3.py` for 2026-10-02 only. That tree was left untracked. The order on that run was not to commit bars or journals. This VM does not have the zip. The scorer book can be reproduced only after those receipt-hashed files are copied in. This row does not restate that run's print as a new measurement.

**This cycle:** `harness/oct2_three_book.py` against `harness/oct2_three_book_manifest.json`. Inputs missing, so the runner is BLOCKED on all three books and prints no computed totals. Manifest: `docs/atc/packs/OCT2_THREE_BOOK_MANIFEST.md`.

### STALIE pack ask (one-way)

Copy the files listed in the manifest into CADNET `packs/oct2/` and stop. One-way pack into CADNET. No git push from STALIE until that pack is present. No write-back to Windows. No APPLY. Redact accounts, tokens, and `.env`.

Known STALIE sources for the scorer book (receipt hashes in the manifest):

- `C:\ATC\claude_harness\inv_20261002\` — `inv_price_v3.py`, `rows_V1.jsonl`, `rows_V2.jsonl`, `rows_V3.jsonl`, `v1_flip_state.json`, `v2_flip_state.json`, `v3_flip_state.json`, `inv_price_v3_2026-10-02_2026-10-02.json`
- `C:\ATC\claude_harness\cf12_20261002\data\bars10s_2026-10-02.csv.gz` and `meta_2026-10-02.json`
- The STALIE smoke print `smoke_inv_price_v3_20261002.txt` (6934 bytes, sha256 `d27974cbc65797559e574ee1d7aea113fd5be7a016d6896996926df312156219`)

Still required, and not in that pack (the pack receipt left broker sessions on STALIE; ledger #4162 is after the synced snapshot, which ends at #3930):

- `packs/oct2/journal_closed/batch_c_4162.jsonl` — one JSON object per Batch C / #4162 closed trade (`arm`, `symbol`, `pnl`). NVDA and INTC are excluded by the harness.
- `packs/oct2/broker_day/day_pnl_20261002.jsonl` — one JSON object per broker-day PnL line (`symbol`, `pnl`) for 2026-10-02.

Do not send `bars_cache_22d.pkl`, the 1-second `second_bars` tree, or `bt_invert_validation.py` as a stand-in. Those do not score this gate.
