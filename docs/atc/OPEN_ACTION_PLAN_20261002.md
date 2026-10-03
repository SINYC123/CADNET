# ATC open action plan — 2026-10-02 (~12:53 ET)

Observation: sequenced attack order. Owners: Grok=APPLY/orchestrate, Claude=stage/dig, Codex=verify/rerun, Farid=GO/secrets.

Status key: OPEN / PARTIAL / DONE / NEEDS-GO

---

## Sequence (attack order)

### P0 — Direction safety (today class of mistake)
| # | Item | Status | Blocker | Owner | Next |
|---|------|--------|---------|-------|------|
| 4 | V2 CHALLENGER INVERT_SIGNALS still ON | DONE-SNAPSHOT | Ledger #3929 (12:57 ET): live gate_status.invert_signals=False on :5051; CHALLENGER atc_state.json false. Cloud VM cannot re-probe the port. | **Grok** live reconfirm on next Windows sync | Reconfirm gates + on-disk state still OFF before any later APPLY |
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
| 6 | Codex #3886 needs-action | DONE | Ledger #3930 annotated #3886 SATISFIED. JOB A #3897+#3899; JOB B #3895. No reassign. | — | none |
| 8 | Bake-off ChatGPT vs Claude vs Cursor | OPEN | Scoreboard exists; observation only | **Grok** score; Claude+Codex cycle tasks | Keep all; Cursor baseline; no firings |

### P3 — Overnight (already owned)
| Item | Status | Owner | Deadline |
|------|--------|-------|----------|
| Remint Ready tasks 6EC1 → F37DA134 | OPEN | Grok (+ Codex re-verify) | before 03:30 ET Sat 2026-10-03 |
| INV origin writeup | PARTIAL | Grok | INVERT_SIGNALS_ORIGIN_20261002.md |

---

## Recommended attack order (now → close)
1. **Reconfirm V2 INV stays OFF** on the next Windows sync (#3929 DONE-SNAPSHOT). Do not toggle it again from this repo.
2. **Seal QA-align confirm gates** on APPLY/deploy paths (#3921 / PRE_DEPLOY_QA_ALIGNMENT.md). In this repo: stage the gap only. The enforcer scripts are not synced here.
3. **Prove V4-CF12 first paper fill** on the box (`:5056`). Cloud agents may only summarize ledger evidence.
4. **Measure paper V1–V3 refuse mix** post-BBO8 on the box; only ask Farid if still blocked.
5. **Farid: sandbox Tradier token** for VA4414585 → then Grok clears 401 + ABC V4 row proof.
6. **#3886 is closed** (#3930). Bake-off cycle-1 scoring continues observation-only.
7. **P2F arm** only after QA-align confirm + explicit Farid GO.
8. **F37 remint** before 03:30 ET Sat. Stage the preflight here; Grok executes on STALIE-MINI.

## Cloud reconciliation (2026-10-02 17:55 ET)

Cursor cloud read the 13:00 ET snapshot and updated items 4 and 6 above. No live port was measured. Three stage-only agents were opened for review (cycle 1 INV audit, QA-align gap, remint preflight + P1 evidence). See `CURSOR_CLOUD_LEDGER.md` CC-0001.

## Explicit non-goals without Farid GO
- Gate loosen / Ultra Ratchet live enforce / paper promote of CF12 onto V1–V3
- Push-to-Fleet live arm
- Firing any bake-off bot

Updated: 2026-10-02 17:55 ET (cloud reconciliation of #3929 and #3930; no live probe)
