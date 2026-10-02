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

Recurring timer `atc-ledger-20m`, every 20 minutes. Each fire re-reads this ledger and the snapshot, launches agents only for new or still-open stage-only work that is not already in review, and appends the next `CC-` row.

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
