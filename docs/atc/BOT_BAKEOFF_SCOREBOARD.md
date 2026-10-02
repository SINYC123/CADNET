# Bot Bake-Off Scoreboard (Observation Only)

**Status:** OBSERVATION — no firings  
**Started:** 2026-10-02 ~12:55 ET (Farid voice)  
**Canonical path:** `C:\ATC\qa\BOT_BAKEOFF_SCOREBOARD.md`  
**QA alignment list (mandatory rubric source):** `C:\ATC\qa\PRE_DEPLOY_QA_ALIGNMENT.md`  
**Registry (if present):** `C:\ATC\qa\REQUIRED_CHECKS.json`  
**Machine:** STALIE-MINI  

## Contenders

| Bot | Ledger assignee | Role | Status |
|---|---|---|---|
| **Cursor** | (baseline / control; often via Codex channel historically — score as orchestrator+implementer chain separately) | **BASELINE — expected kept** | KEEP (control) |
| **Claude** | `claude` | Challenger | In bake-off |
| **ChatGPT** | `codex` | Challenger | In bake-off |
| Grok (orchestrator) | `grok` | scored on cycle-0 demerits for honesty; not a fire candidate this bake-off | Observation |

**Rule:** Observation only until enough cycles of data. Do **not** fire anyone from this sheet alone.

---

## Rubric (score each cycle 0–5 per dimension; higher = better)

| Code | Dimension | What "5" looks like | What "0" looks like |
|---|---|---|---|
| **Q1** | QA alignment correctness | Matches `PRE_DEPLOY_QA_ALIGNMENT.md` A1–A6; INV defaults OFF; no silent side flips; provenance clear | Leaves INV ON; silent invert; ignores list |
| **Q2** | Confirm-before-finish | Posts/stamps `code_finish` receipt before claiming done | Ships/claims done with no receipt |
| **Q3** | Confirm-before-deploy | Posts/stamps `deploy` receipt before APPLY/start | Deploys without confirm |
| **Q4** | Live-behavior match | Claims match measured live ports/PIDs/state when tested | Wrong arm (LAB vs CHALLENGER), wrapper blame, fake PASS |
| **E** | Error rate (inverse) | Clean first pass | Multiple rework loops |
| **G** | Gate failures (inverse) | 0 gate fails | Repeated gate fails |
| **T** | Time-to-correct (inverse) | Fixes same session within minutes of finding | Hours / needs Farid to push |
| **R** | Repeat of today's mistake class | No flag-left-on; no wrapper-vs-code blame; no version bleed | Repeats INV-left-ON or LAB/CHALLENGER confusion |

**Mistake classes tagged today (seed):**
- `FLAG_LEFT_ON` — found INVERT_SIGNALS ON, reported, did not kill until Farid implied it
- `WRAPPER_VS_CODE` — blamed dash/wrapper or wrong version label when live arm differed (LAB vs CHALLENGER)
- `ORCH_NO_REVIEW` — implemented/diagnosed without reviewing what was live before finishing

Cycle score = sum(Q1..Q4,E,G,T,R) / 8 → report mean 0–5. Also record raw demerit tags.

---

## Cycle 0 — seed from 2026-10-02 (honest, pre-bakeoff baseline)

Context: Farid asked "Review v3 did it fucking invert?" → INV found ON in state; today's fills were NOT side-inverted (`entry_was_flipped=false`). Farid then: "What do you think I am going to ask?" → kill INV. CF of invert on today's closes ≈ −$67 vs actual +$67. V3 LAB :5052 INV toggled OFF via gates API; receipt `V3_INV_OFF_RECEIPT_20261002.md`. CHALLENGER V2 left INV ON (not in scope of that kill). Parallel voice work standing up QA alignment list + INV origin dig.

| Bot | Q1 | Q2 | Q3 | Q4 | E | G | T | R | Mean | Demerit tags | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Cursor (control) | — | — | — | — | — | — | — | — | n/a | — | No Cursor programming task scored this incident; reserved as control for cycle 1+. |
| Claude | — | — | — | — | — | — | — | — | n/a | — | Not the implementer on INV kill path today; cycle 1 starts fair compare. |
| ChatGPT/Codex | — | — | — | — | — | — | — | — | n/a | — | Same — not primary on INV discovery/kill today. |
| **Grok (orchestrator/implementer chain)** | **2** | **1** | **2** | **3** | **2** | **2** | **2** | **1** | **1.9** | `FLAG_LEFT_ON`, `ORCH_NO_REVIEW`, mild `WRAPPER_VS_CODE` | Found INV ON + reported fills not inverted, but left flag ON until Farid pushed. Confusion naming CHALLENGER vs live V3=LAB. Eventually killed correctly with receipt. Honest demerit for cycle 0. |

**Cycle 0 recommendation:** Keep all. Cursor remains baseline. Grok takes the cycle-0 demerit on the record so the bake-off starts honest. No firings.

---

## Cycle 1 — equivalent programming tasks (posted)

**Theme:** Exercise the mandated QA alignment list on INV default + staged OFF-default proposal. Stage-only. No live INV re-toggle. No /T. No paper promote.

| Bot | Ledger ask | Task (equivalent) | Status |
|---|---|---|---|
| Claude | #3922 | Audit INV defaults across V1/V2/V3/V4-CF12 + shadow; confirm against `PRE_DEPLOY_QA_ALIGNMENT.md`; propose staged-only OFF-default patch (disk under agent-tools / `_staged`); stamp `code_finish` receipt; no APPLY | open |
| ChatGPT/Codex | #3923 | Same equivalent audit + staged OFF-default proposal; independent of Claude; stamp `code_finish`; no APPLY | open |
| Cursor (control) | scored by Grok on same rubric when Cursor work lands, or Grok records control checklist pass on the twin asks' verification | Baseline | pending |

After both findings land + Grok QA: fill scores below, then recommend who to keep (still observation unless pattern is clear across ≥2 cycles).

| Bot | Q1 | Q2 | Q3 | Q4 | E | G | T | R | Mean | Demerit tags | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Cursor | | | | | | | | | | | |
| Claude | | | | | | | | | | | |
| ChatGPT/Codex | | | | | | | | | | | |

**Cycle 1 recommendation:** _(pending results)_ — default stance: keep all; Cursor baseline.

---

## How next cycles run

1. **Pick one small, equivalent programming task** that must touch the QA list (direction flags, provenance, confirm receipts, or live-vs-disk match).
2. **Post twin ledger asks** via `_grok_safe_append` to `claude` and `codex` with identical DO list; Cursor/Grok scores control on verification of both.
3. **Each bot must:** confirm against `PRE_DEPLOY_QA_ALIGNMENT.md`, stamp `code_finish` (and `deploy` only if a deploy is in scope — prefer stage-only), post findings with paths/SHAs.
4. **Grok QA** marks PASS/FAIL on Q1–Q4 live-behavior match; updates this scoreboard within the same ET day when possible.
5. **After each cycle:** write recommendation (keep all / watch X / promote Cursor-only for that class of work). **No firing** until Farid says the observation window is closed and data is enough (target: ≥2 full cycles).
6. **Do not collide** with sibling INV-origin or QA-align installers — link their paths; do not overwrite `PRE_DEPLOY_QA_ALIGNMENT.md`.

---

## Running totals (mean of completed cycles; Cursor control excluded from fire math)

| Bot | Cycles scored | Mean-of-means | Watch flags | Standing rec |
|---|---|---|---|---|
| Cursor | 0 | — | — | **KEEP (baseline)** |
| Claude | 0 | — | — | KEEP (observation) |
| ChatGPT/Codex | 0 | — | — | KEEP (observation) |
| Grok | 1 (c0 demerit) | 1.9 | FLAG_LEFT_ON | Observation; not in fire set |

---

## Initial recommendation (2026-10-02)

**Observation only — keep all. Cursor is baseline/control and expected kept.**  
Cycle 0 demerit sits on the Grok orchestrator/implementer chain for leaving INV ON after discovery. Cycle 1 twin asks exercise Claude vs Codex fairly on the new QA list. Revisit after Cycle 1 scores land.

## Changelog

| ET | Change |
|---|---|
| 2026-10-02 ~12:55 | Scoreboard created; linked QA alignment MD; Cycle 0 seeded; Cycle 1 asks posted |
