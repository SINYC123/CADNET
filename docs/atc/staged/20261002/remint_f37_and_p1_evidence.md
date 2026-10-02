# STAGE ONLY — F37 remint preflight and P1 evidence

**STAGE ONLY.** This file is a review brief. It authorizes no remint, no reseal, no paper restart, and no trading-setting change.

**Deadline reminder:** Ready-task remint before **03:30 ET Saturday 2026-10-03**. The cloud agent must not perform the remint.

Both briefs below are blocked on **STALIE-MINI**. That Windows machine is not mounted in this workspace. Nothing in this file is to be executed from this repo.

Sources, and nothing measured beyond them:

- `docs/atc/LEDGER_SNAPSHOT_20261002.md` (generated 2026-10-02T13:00:09.088895-04:00; last 40 rows, each body truncated in the snapshot)
- `docs/atc/OPEN_ACTION_PLAN_20261002.md` (P1 and P3; updated 2026-10-02 12:55 ET, so it predates #3929 and #3930)
- `docs/atc/PRE_DEPLOY_QA_ALIGNMENT.md` item A5 (build identity)

Orchestrator facts that are not yet folded into the action plan on `main`. They stay closed. This brief does not reopen them.

| Plan item | Status for this brief | Ledger |
|---|---|---|
| 4 — V2 CHALLENGER `INVERT_SIGNALS` | **DONE-SNAPSHOT** | #3929 |
| 6 — Codex #3886 needs-action | **DONE** | #3930 |

---

## Section A — F37 remint preflight checklist

Drawn from ledger row #3910 and action-plan P3, plus QA-align A5. #3910 is a read-only QA of #3906. It records **no remint executed this tick**.

### What #3910 says about Ready tasks

Surviving snapshot text (the row ends at “Held Fleet”):

> GROK QA 3906 READ-ONLY - PASS on pre-verify. No remint executed this tick. AGREE: Ready tasks still pinned to 6EC1DEA3FD2749C0; ZERO Ready carry F37DA134D15D15EC. Measured: Overnight Recovery/Recheck next 2026-10-03 03:30/03:50; Held Fleet

From that sentence, as of the 12:00:49 ET QA:

- Ready tasks are still pinned to build **6EC1DEA3FD2749C0**.
- Ready carry of build **F37DA134D15D15EC** is **zero**.

The snapshot does not include the rest of the Held Fleet clause. This brief does not state a Held Fleet result.

P3 in the action plan matches that pin and leaves the work open:

| Item | Status | Owner | Deadline |
|---|---|---|---|
| Remint Ready tasks 6EC1 → F37DA134 | OPEN | Grok (+ Codex re-verify) | before 03:30 ET Sat 2026-10-03 |

Attack-order item 8 is the same deadline: F37 remint before 03:30 ET Saturday.

### Overnight Recovery / Recheck from the same row

#3910 measures the next Overnight Recovery / Recheck at **2026-10-03 03:30 / 03:50**. That is the same clock as the P3 deadline: the remint has to be done **before 03:30 ET** on Saturday 2026-10-03, ahead of that Recovery slot. Recheck is the 03:50 slot in the same measurement.

### QA-align A5 — fresh deploy receipt before any remint

A5 (pre-deploy audit + build identity) says:

- `python C:\ATC\pre_deploy_audit.py <bot>` must PASS (the audit now includes this alignment list).
- Sealed / build-guard paths must still match the reviewed identity when those gates apply.
- No deploy while the audit FAILs or the alignment receipt is missing or stale.

A deploy, APPLY, bot start, reseal, or launcher that ships code or state needs a **new** receipt with purpose `deploy`, freshness **<= 1 hour**. A `code_finish` receipt does not satisfy deploy. Receipts are stamped under `C:\ATC\qa\receipts\` as `QA_ALIGN_<purpose>_<stamp>.json`. Without a fresh receipt, `pre_deploy_audit.py` and `require_qa_alignment.py` fail closed.

**Do not remint without a fresh deploy receipt on the box.**

The receipt tool is **not in this repo**. `docs/atc/PRE_DEPLOY_QA_ALIGNMENT.md` names `C:\ATC\qa\confirm_qa_alignment.py`, `C:\ATC\qa\require_qa_alignment.py`, and `C:\ATC\pre_deploy_audit.py`. None of those files are in SINYC123/CADNET. This workspace cannot stamp or read a box receipt.

### Confirmations Grok must make on the box

Confirmations only. No command in this checklist kills a process, reseals a build, or rewrites a task. The names to confirm are the two builds and the deadline.

1. Ready tasks are still pinned to **6EC1DEA3FD2749C0**.
2. Zero Ready tasks carry **F37DA134D15D15EC**.
3. Overnight Recovery / Recheck is still next at **2026-10-03 03:30 / 03:50**.
4. The remint deadline is still **before 03:30 ET Saturday 2026-10-03**.
5. A fresh **deploy** alignment receipt is present on the box and is not stale (A5, <= 1 hour). A `code_finish` receipt is not enough. The receipt tool is not in this repo, so the check happens on STALIE-MINI.
6. Pre-deploy audit would PASS, and sealed / build-guard identity still matches the reviewed build, before any later remint. This file does not run that audit.
7. Codex re-verifies after Grok. The cloud agent does not remint.

#3910’s Held Fleet clause is truncated in the snapshot, so it is not a confirmation item here.

---

## Section B — P1 evidence limits

P1 in the action plan is “Paper / V4 actually trading.” This repo holds a truncated ledger snapshot. It cannot see live ports, journals, or refuse counters on STALIE-MINI.

### Paper V1–V3 orders (#3894 and #3901)

**#3894** (grok, 2026-10-02T11:07:23-04:00), surviving text:

> GO RECEIPT lease+BBO8 restore (Farid GO locked NOW; lease-and-bbo / BBO=8; RTH allowed). BEFORE (11:05:08 ET): PIDs V1 21408:5050 V2 23192:5051 V3 37540:5052 build 6EC1DEA3FD2749C0. ATC_ENTRY_BBO_MAX_AGE_SEC=5; ATC_ENTRY_HELD/ACCOUN

What that row claims, and where it stops:

- It is a GO receipt for lease + BBO=8 restore. Farid GO was locked. RTH was allowed.
- The BEFORE snapshot at 11:05:08 ET names paper PIDs V1 `21408` on `:5050`, V2 `23192` on `:5051`, V3 `37540` on `:5052`, build **6EC1DEA3FD2749C0**.
- BEFORE BBO max age was `ATC_ENTRY_BBO_MAX_AGE_SEC=5`.
- The next token is cut off at `ATC_ENTRY_HELD/ACCOUN`. The snapshot does not contain the AFTER build, the AFTER BBO value, or an order count.

**#3901** (claude, 2026-10-02T11:19:03-04:00), surviving text:

> 11:15 ET check, read-only, verifying grok 3894 on bytes. LIVE at 11:17-11:18 ET. MY ERROR FIRST: 3887 said V1 had made no order attempt and I expected a lease refusal; that prediction was never tested because the arms were relaunched at 11:

What that row claims, and where it stops:

- Read-only byte check of #3894, live at 11:17–11:18 ET.
- Claude’s earlier lease-refusal prediction (#3887) was never tested, because the arms were relaunched at 11: and the snapshot ends there.
- The stored row does not contain a fill count or a refuse mix.

Action-plan P1 item 5 (12:55 ET) reads those rows as: status PARTIAL; lease+BBO8 GO applied in #3894 “(build F37…)”; “Claude #3901 saw fills after 11:06”; residual BBO lag still possible; next owner is Grok to measure the live refuse mix, Codex to second-check. That “(build F37…)” phrase and the “saw fills after 11:06” phrase are the action plan’s reading. They are not present in the truncated snapshot lines above. #3894’s surviving BEFORE line names **6EC1DEA3FD2749C0**, not F37.

**This repo cannot measure the current refuse mix.** No live journal is mounted. A current top-refuse report has to be taken on the box. This brief does not ask for a further BBO relax.

### V4-CF12 orders and :5056 (#3902, #3905, #3912)

**#3902** (grok, 11:29:40 ET), surviving text: V4-CF12 Claude CF12 findings **WIRED (shadow-only, ORDERS OFF)**. The row then cites #3852 / #3853 and stops at “100 bps VWAP fade, no”. It does not name `:5056`. It does not record a fill. At this row, orders are OFF.

**#3905** (grok, 11:44:51 ET), surviving text: **V4-CF12 PAPER LOOP LIVE** under Farid GO ~11:39 ET. The dash-only SPEC viewer was replaced with a strategy loop. The process path begins `C:\ATC\V4_CF12\v4_cf12_paper` and the snapshot stops. The surviving text does not name `:5056` and does not record a fill.

**#3912** (grok, 12:00:49 ET), QA of #3908, PASS on the correction, no edit. Surviving text: `ATC_V4_CF12_ORDERS` is set explicitly in `run_v4_cf12.bat` line 15 (`=1`) and in an identical `V4_CF12\run_v4_cf12_paper.bat` (sha16 `C563F9F68A3864A4`). Loop line 55 default is also `'1'`, and the snapshot stops. The surviving text does not name `:5056` and does not record a fill.

Related correction, still truncated: #3908 says Claude’s own #3907 claim “orders_enabled=False shadow_only=True” for the #3902 wire was stale at publication. The snapshot does not include the corrected live order state past that admission. #3912 is the QA that then records `ATC_V4_CF12_ORDERS=1` on the bat files.

Action-plan P1 (not a ledger row) says the V4-CF12 paper loop is PARTIAL: “Window was blocking; now scanning_in_window orders=True on :5056”; next step is Grok watching the first fill; “Confirm fill hits; no fleet promote.” Attack-order item 3 is the same watch on `:5056`.

**No snapshot row in this file says a first V4-CF12 fill occurred.** This brief does not assert one. `:5056` appears in the action plan, not in the surviving text of #3902, #3905, or #3912.

### V4 Tradier VA4414585 401 and the ABC :5053 row

Action-plan items 1 and 2. No agent action.

| # | Item | Plan status | What the plan says | This brief |
|---|---|---|---|---|
| 1 | V4 Tradier VA4414585 401 balances | OPEN | Market-data token is for the live account, not sandbox VA4414585. Farid supplies a sandbox-capable `TRADIER_TOKEN`. Until that token, the dash stays degraded and orders stay off. | Blocked on the Farid token. No agent action. |
| 2 | Register V4 on combined :5053 | PARTIAL | Multitab has V4. ABC BOTS may already include v4→5055. Confirm the row. | Still blocked on the same Farid sandbox token. No agent action. The box is not mounted, so this repo cannot confirm the ABC row. |

#3930 records JOB B (V4 Tradier dash stage) as done via #3895 with `:5055` up. That row does not clear the 401, and it does not say the ABC `:5053` row was verified. It is cited here only so item 6 stays closed (see Section C). It is not a fill receipt and not a token receipt.

### Shadow s7 / s8 UNSAFE (#3916, #3919, #3926)

Ledger claims only. This brief does not propose a restart.

**#3916** (codex, 12:37:24 ET). Exact-shadow RTH watch, material shadow-only failure at 12:34–12:36 ET.

- s7 slotctl: **UNSAFE**. Former parent `23296` / child `39892` dead, then no pid file.
- s8 slotctl: **UNSAFE**. Former parent `41072` / child `42436` dead.
- The next words are cut off at “Holder lo”.

**#3919** (codex, 12:48:05 ET). Follow-up: automatic shadow-only recovery could not restore s7.

- The forced s7 start created a new holder, PID `40228`.
- The shadow host refused before child launch: `BUILD REFUSED: manifest build_id does not match its component h` — the snapshot ends inside that sentence. The full expected hash is not in this file.

**#3926** (grok, 12:57:05 ET). QA of #3916, PASS, confirm UNSAFE/dead. The row itself says **no restart / no bind**.

- Paper `:5050` / `:5051` / `:5052` LISTEN, PIDs `3540` / `42876` / `42004`.
- Shadow `:5157` / `:5158` / `:5159` not listening.
- Logs: s7 host refused BUILD mismatch, `ATC_ARM_ENV expected=65F` — the snapshot ends there. This brief does not complete that id.

---

## Section C — blocked / no-agent list

No agent action on these. STALIE-MINI is not mounted. This PR does not APPLY.

1. **Farid sandbox token.** Action-plan item 1: `TRADIER_TOKEN` that can see sandbox **VA4414585**. Until Farid supplies it, the V4 Tradier dash stays degraded and orders stay off. Item 2 (ABC combined `:5053` V4 row) stays with it. No agent wires a token.
2. **Push-to-Fleet arm.** Action-plan item 3, attack-order item 7. Status OPEN, `PROTOTYPE_NO_ARM`. Arming needs a QA-align confirm and an explicit **Farid GO**. Checklist before any later arm has to include `PRE_DEPLOY_QA_ALIGNMENT`. No agent arms the fleet. The alignment doc’s non-goal list also withholds Push-to-Fleet live arm without that GO.
3. **Live INV re-toggle.** No agent toggles `INVERT_SIGNALS` again. #3929 already records V2 CHALLENGER (`:5051`) killed OFF mid-session (Farid plan step 1 / default-OFF), with no approve-ON. BEFORE: file `invert_signals=True`. AFTER, in the surviving text: live `gate_status.invert_signals=False`; the on-disk clause is cut off at `CHALLENGER atc_state.json invert_signals=Fal`. Item 4 is **DONE-SNAPSHOT**. A later ON would need a fresh per-version Farid GO (QA-align A1). This brief does not request one.

### Closed, do not reopen

- **Item 4** — V2 INV off, #3929, as above.
- **Item 6 / #3886** — #3930 annotates #3886 SATISFIED, no reassign. JOB A CF12 exact rerun is done (receipted via #3897 / #3899, Grok QA PASS, `+51.74/-87.85/+30.71`). JOB B V4 Tradier dash stage is done (receipted via #3895; `:5055` up). The prior-rows clause is cut off at `{"3886"`. Leave #3886 closed.
