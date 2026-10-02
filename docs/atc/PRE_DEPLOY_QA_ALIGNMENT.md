# Mandated Pre-Deployment QA Alignment List

**Status:** MANDATORY as of 2026-10-02T12:53:42-04:00
**Canonical path:** `C:\ATC\qa\PRE_DEPLOY_QA_ALIGNMENT.md`
**Registry:** `C:\ATC\qa\REQUIRED_CHECKS.json`
**Enforcer:** `C:\ATC\qa\require_qa_alignment.py` (also hooked from `pre_deploy_audit.py`)

This list is not advisory. Claude, Codex/ChatGPT, and Grok must confirm every item
before finishing programming work, and confirm again before any deploy / APPLY /
launcher start that touches bot code, arm env, release contract, or live state.

Confirmation is a stamped receipt under `C:\ATC\qa\receipts\`. Without a fresh
receipt, `pre_deploy_audit.py` and `require_qa_alignment.py` FAIL CLOSED.

---

## Alignment checks (minimum)

### A1. INVERT_SIGNALS default OFF
- `INVERT_SIGNALS` / `invert_signals` must default **OFF** unless Farid explicitly
  approved ON for a named version/arm (V1 / V2 / V3 / V4-CF12 / shadow lane).
- Per-version approval must be recorded (ledger id + receipt). Global ON is forbidden.
- Historical note: `pre_deploy_audit.py` previously expected `INVERT_SIGNALS=True`
  from the 2026-04-28 BT invert validation. That ship default is **revoked**. OFF is
  the mandated default unless a fresh per-version GO says otherwise.

### A2. Reversion-at-submission matches the universal contract
- Native signal side and submitted side must match the universal direction contract.
- Sides must **not** silently invert at submission, Continue, or restore.
- If a flip/XOR path exists (AFLIP, master flip, contract flip), it must be explicit
  in journals (`entry_was_flipped`, native side, final side) and visible in state.

### A3. Direction-changing globals are visible and reviewed
- Any global flag that changes trade direction must appear in live state / gates /
  dashboard and be reviewed before deploy. Minimum set:
  - `INVERT_SIGNALS` / `invert_signals`
  - `ATC_MASTER_FLIP` / `master_flip`
  - `ATC_FLIP_SUBMIT` / flip-submit scope
  - Adaptive flip (AFLIP) arming and scope
  - Contract flip lanes / XOR submission helpers
- Hidden or env-only direction flips without state visibility = FAIL.

### A4. Persistence must not resurrect a disabled flag
- Config / `atc_state.json` / Continue / New Session restore must **not** turn a
  flag back ON after it was deliberately disabled for that arm.
- After disabling INV (or any direction flag), verify: live gates API, on-disk state,
  and post-Continue intent all agree OFF (unless per-version GO).

### A5. Pre-deploy audit + build identity still pass
- `python C:\ATC\pre_deploy_audit.py <bot>` must PASS (now includes this list).
- Sealed / build-guard paths must still match reviewed identity when those gates apply.
- No deploy while audit FAIL or alignment receipt missing/stale.

### A6. No silent lane/version bleed
- A change intended for one arm (LAB/V3, CHALLENGER/V2, CHAMPION/V1, V4-CF12, shadow)
  must not silently alter another arm's direction defaults or invert flags.

---

## When confirmation is required

| Moment | Purpose token | Freshness |
|---|---|---|
| Before finishing any programming / patch / staged edit | `code_finish` | <= 4 hours |
| Before any deploy, APPLY, bot start, reseal, or launcher that ships code/state | `deploy` | <= 1 hour |

Both moments require a **new** receipt. A code_finish receipt does not satisfy deploy.

---

## How to confirm

```bat
py -3 C:\ATC\qa\confirm_qa_alignment.py --purpose code_finish --agent grok --note "why"
py -3 C:\ATC\qa\confirm_qa_alignment.py --purpose deploy --agent grok --note "why"
```

Or fail-closed check only:

```bat
py -3 C:\ATC\qa\require_qa_alignment.py --purpose deploy
```

Receipts land in `C:\ATC\qa\receipts\QA_ALIGN_<purpose>_<stamp>.json`.

---

## Enforcement map

1. **Doc (this file)** - canonical checklist.
2. **Registry** - `REQUIRED_CHECKS.json` marks this list mandated.
3. **Confirm tool** - writes checklist-hash receipt.
4. **Require tool** - exits 1 without fresh receipt.
5. **`pre_deploy_audit.py`** - hard FAIL if deploy receipt missing; INV default must be False.
6. **`run_pre_deploy_audit.bat`** - runs require(deploy) then audit.
7. **`AGENTS.md` + `claude_link/PROTOCOL.md`** - agents must confirm before finish and before deploy.
8. **Ledger** - mandated registration row in `messages.jsonl`.

Emergency override (explicit, loud, logged): set `ATC_QA_ALIGN_OVERRIDE=1` only with
Farid's recorded GO. Override still prints WARN; it does not erase the list.
