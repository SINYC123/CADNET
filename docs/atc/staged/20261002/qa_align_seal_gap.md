# QA alignment seal gap

**STAGE ONLY.** Date: 2026-10-02. Agent: Cursor.

This is a gap analysis, not an enforcer install. No APPLY, no bot start, no reseal. It does not install confirm or require tools, does not write a receipt, and does not change `docs/atc/PRE_DEPLOY_QA_ALIGNMENT.md`.

Source of the named seal: `docs/atc/PRE_DEPLOY_QA_ALIGNMENT.md`, section **Enforcement map** (P0 item 7 in `docs/atc/OPEN_ACTION_PLAN_20261002.md` is PARTIAL: the alignment markdown and a ledger snapshot row exist; confirm-before-finish and confirm-before-deploy are not sealed in this repository).

Inventory method: full working-tree listing of SINYC123/CADNET at `origin/main` (`9b2bdf4`, 2026-10-02). Absence below was checked by that listing, not assumed in advance.

---

## What is in this repo

Working tree (excluding `.git`):

| Path | Role relative to the seal |
|---|---|
| `README.md` | Repository title only (`# CADNET`). |
| `docs/atc/README.md` | Index of the synced QA pack. |
| `docs/atc/PRE_DEPLOY_QA_ALIGNMENT.md` | Checklist text, including the Enforcement map. Header names the canonical copy as `C:\ATC\qa\PRE_DEPLOY_QA_ALIGNMENT.md` (a Windows path, not a path in this git tree). |
| `docs/atc/OPEN_ACTION_PLAN_20261002.md` | P0 item 7 recorded PARTIAL. |
| `docs/atc/LEDGER_SNAPSHOT_20261002.md` | Truncated excerpt of `C:\ATC\claude_link\messages.jsonl`. Row #3921 mentions registration on the Windows box and is cut off. This file is not `messages.jsonl`. |
| `docs/atc/INVERT_SIGNALS_ORIGIN_20261002.md` | Historical origin writeup. Not an enforcer and not live state. |
| `docs/atc/BOT_BAKEOFF_SCOREBOARD.md` | Observation rubric. Points at `C:\ATC\qa\REQUIRED_CHECKS.json` only "if present". |

No Python, JSON, or batch files are in the tree. No `receipts` directory. No `claude_link` directory.

---

## Enforcement map: present vs absent

The map (eight items) names a doc, a registry, confirm and require tools, `pre_deploy_audit.py`, `run_pre_deploy_audit.bat`, `AGENTS.md` plus `claude_link/PROTOCOL.md`, and a ledger row in `messages.jsonl`. "How to confirm" in the same file names `confirm_qa_alignment.py`, receipt files under `C:\ATC\qa\receipts\`, and `require_qa_alignment.py`.

| Map item | Named artifact | In this repo |
|---|---|---|
| 1. Doc (canonical checklist) | Checklist prose | **Present** as `docs/atc/PRE_DEPLOY_QA_ALIGNMENT.md` (synced text). Canonical Windows path is not this tree. |
| 2. Registry | `REQUIRED_CHECKS.json` | **Absent** |
| 3. Confirm tool | `confirm_qa_alignment.py` | **Absent** |
| 4. Require tool | `require_qa_alignment.py` | **Absent** |
| 5. Pre-deploy audit | `pre_deploy_audit.py` | **Absent** |
| 6. Audit launcher | `run_pre_deploy_audit.bat` | **Absent** |
| 7. Agent protocol | `AGENTS.md` and `claude_link/PROTOCOL.md` | **Both absent** |
| 8. Ledger | `messages.jsonl` mandated registration row | **Absent.** Truncated snapshot row #3921 only. |
| Receipts (named with the confirm tool) | `receipts` directory and `QA_ALIGN_<purpose>_<stamp>.json` | **Absent** |

Confirmed missing, by repository listing: `confirm_qa_alignment.py`, `require_qa_alignment.py`, `pre_deploy_audit.py`, `REQUIRED_CHECKS.json`, a receipts directory, `AGENTS.md`, `claude_link/PROTOCOL.md`. Also missing, because the map names them: `run_pre_deploy_audit.bat` and `messages.jsonl`.

---

## Staged confirm checklist (this repo only)

Use this before claiming a documentation change in CADNET is done. Cite A1–A6 from `docs/atc/PRE_DEPLOY_QA_ALIGNMENT.md`. Verdicts below are for this gap note only. They are not a Windows confirm, and they are not a deploy receipt.

A documentary stamp in this file does not replace `C:\ATC\qa\receipts` on STALIE-MINI. A `code_finish` receipt does not satisfy `deploy`. This markdown creates neither.

| Check | Cite | What this repo can show | Verdict |
|---|---|---|---|
| A1 | `INVERT_SIGNALS` / `invert_signals` default **OFF** unless Farid explicitly approved ON for a named version/arm. Global ON is forbidden. The alignment doc revokes the old ship default of True. | Alignment text still says that. This note does not edit that file. No bot source and no `atc_state.json` are in the tree, so the live or code default cannot be measured here. | **not-verifiable** |
| A2 | Native signal side and submitted side match the universal direction contract. No silent invert at submission, Continue, or restore. Any flip path must be explicit in journals. | No submission path, Continue/restore code, or journals are in the tree. | **not-verifiable** |
| A3 | Direction-changing globals are visible in live state, gates, and dashboard and reviewed before deploy. Minimum set named in A3: `INVERT_SIGNALS` / `invert_signals`, `ATC_MASTER_FLIP` / `master_flip`, `ATC_FLIP_SUBMIT` / flip-submit scope, adaptive flip (AFLIP), contract-flip / XOR submission helpers. | No live state, gates, or dashboard are in the tree. | **not-verifiable** |
| A4 | Config, `atc_state.json`, Continue, and New Session restore must not turn a deliberately disabled flag back ON. | No config, state, or restore code are in the tree. | **not-verifiable** |
| A5 | `python C:\ATC\pre_deploy_audit.py <bot>` must PASS, including this list, and a fresh alignment receipt must exist. Sealed build identity must still match when those gates apply. | `pre_deploy_audit.py` is absent. No build-identity files. No receipts directory. A PASS cannot be recorded from this repo. | **fail** |
| A6 | A change for one arm (LAB/V3, CHALLENGER/V2, CHAMPION/V1, V4-CF12, shadow) must not silently alter another arm's direction defaults or invert flags. | This commit adds only this markdown file. No arm trees exist here to compare. | **not-verifiable** |

Passing this table, or merging this note, does not mean confirm-before-finish or confirm-before-deploy is sealed.

---

## Explicit non-goals

- Do not propose weakening A1. The mandated default remains OFF unless Farid has a recorded per-version GO. This note does not suggest otherwise.
- Do not set `ATC_QA_ALIGN_OVERRIDE`. The alignment doc reserves that switch for Farid's recorded GO. This stage does not use it and does not recommend it.
- Do not claim deploy receipt freshness. No `C:\ATC\qa\receipts` stamp was read or written. This file is not a `deploy` receipt and is not a `code_finish` receipt.

---

## Recommended next step (Windows box only)

On STALIE-MINI, wire `require_qa_alignment.py` so it runs fail-closed before APPLY: if a fresh deploy receipt is missing, the require tool exits 1 and APPLY does not proceed. Keep that wire next to the canonical checklist, `REQUIRED_CHECKS.json`, and `C:\ATC\qa\receipts` on that machine. This CADNET note does not do that wire.
