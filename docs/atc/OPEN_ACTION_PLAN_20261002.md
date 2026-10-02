# ATC open action plan — 2026-10-02 (~12:53 ET)

Observation: sequenced attack order. Owners: Grok=APPLY/orchestrate, Claude=stage/dig, Codex=verify/rerun, Farid=GO/secrets.

Status key: OPEN / PARTIAL / DONE / NEEDS-GO

---

## Sequence (attack order)

### P0 — Direction safety (today class of mistake)
| # | Item | Status | Blocker | Owner | Next |
|---|------|--------|---------|-------|------|
| 4 | V2 CHALLENGER INVERT_SIGNALS still ON | OPEN | Flag true in C:\ATC\CHALLENGER\atc_state.json; V3 LAB already OFF (#3920) | **Grok** APPLY hot-toggle; Farid if per-version approve-ON instead | Hot POST /api/gates inv=false on V2 :5051 (same path as V3), persist state; or Farid explicit approve-ON |
| 7 | QA alignment MD + confirm-before-finish/deploy | PARTIAL | MD + ledger #3921 exist; confirm gates must be live on APPLY/mint | **Grok** finish wire; Claude/Codex must cite list | Verify C:\ATC\qa\PRE_DEPLOY_QA_ALIGNMENT.md blocks APPLY without stamp |

### P1 — Paper / V4 actually trading
| # | Item | Status | Blocker | Owner | Next |
|---|------|--------|---------|-------|------|
| 5 | Paper V1–V3 0-orders (lease + BBO) | PARTIAL | Lease+BBO8 GO applied #3894 (build F37…); Claude #3901 saw fills after 11:06 — residual BBO lag still possible | **Grok** measure live refuse mix; Codex second-check | If still 0 new orders: report top refuse; Farid GO only if further BBO relax |
| V4-CF12 paper loop | PARTIAL | Window was blocking; now scanning_in_window orders=True on :5056 | **Grok** watch first fill | Confirm fill hits; no fleet promote |
| 1 | V4 Tradier VA4414585 401 balances | OPEN | Market-data token is for live acct not sandbox VA4414585 | **Farid** supply sandbox-capable TRADIER_TOKEN; Grok wire | Until token: dash stays degraded; orders stay off |
| 2 | Register V4 on combined :5053 | PARTIAL | Multitab has V4; ABC BOTS may already include v4→5055 — confirm row | **Grok** | Verify ABC board shows V4 row; patch if missing |

### P2 — Fleet tools / ledger hygiene
| # | Item | Status | Blocker | Owner | Next |
|---|------|--------|---------|-------|------|
| 3 | Push-to-Fleet dry-run S1–S10 | OPEN | PROTOTYPE_NO_ARM; arming needs QA-align confirm + Farid GO | **Farid** GO when; **Grok** checklist | Checklist must include PRE_DEPLOY_QA_ALIGNMENT confirm before arm |
| 6 | Codex #3886 needs-action | DONE-work / STALE-row | JOB A #3897+#3899 PASS; JOB B #3895 stage receipt; row never closed | **Grok** | Flip #3886 closed/verified; no reassign |
| 8 | Bake-off ChatGPT vs Claude vs Cursor | OPEN | Scoreboard exists; observation only | **Grok** score; Claude+Codex cycle tasks | Keep all; Cursor baseline; no firings |

### P3 — Overnight (already owned)
| Item | Status | Owner | Deadline |
|------|--------|-------|----------|
| Remint Ready tasks 6EC1 → F37DA134 | OPEN | Grok (+ Codex re-verify) | before 03:30 ET Sat 2026-10-03 |
| INV origin writeup | PARTIAL | Grok | INVERT_SIGNALS_ORIGIN_20261002.md |

---

## Recommended attack order (now → close)
1. **Kill V2 INV** (or Farid approve-ON) — same class as V3; do not leave asymmetric.
2. **Seal QA-align confirm gates** on APPLY/deploy paths (#3921 / PRE_DEPLOY_QA_ALIGNMENT.md).
3. **Prove V4-CF12 first paper fill** now that window is open; watch :5056.
4. **Measure paper V1–V3 refuse mix** post-BBO8; only ask Farid if still blocked.
5. **Farid: sandbox Tradier token** for VA4414585 → then Grok clears 401 + ABC V4 row proof.
6. **Close ledger #3886** as satisfied; bake-off cycle-1 scoring continues observation-only.
7. **P2F arm** only after QA-align confirm + explicit Farid GO.
8. **F37 remint** before 03:30 ET Sat.

## Explicit non-goals without Farid GO
- Gate loosen / Ultra Ratchet live enforce / paper promote of CF12 onto V1–V3
- Push-to-Fleet live arm
- Firing any bake-off bot

Updated: 2026-10-02 12:55 ET
