# INVERT_SIGNALS ORIGIN RECEIPT — 2026-10-02

**Ask:** Why did `INVERT_SIGNALS` end up ON by default / programmed that way instead of OFF as wanted?

**Scope:** Read-only trace (bak timestamps, code comments, state restore, ledger/state files). No git on PATH; no `git.exe` found. Did **not** change INV again.

**Live note (already done earlier today):** V3 LAB `:5052` hot-set INV OFF and persisted — `C:\ATC\LAB\atc_state.json` now `invert_signals: false` (ledger #3920). CHALLENGER / root state still had `true` at probe time.

---

## Executive answer

`INVERT_SIGNALS` was deliberately flipped to **code default True on 2026-04-28** after `bt_invert_validation.py` showed INV=ON beating INV=OFF on a 90-day 1-sec tick BT (+$227,250 vs +$102,442). Original hook landed **2026-04-27** as a test for “signals systematically wrong-side from bar-close slippage,” initially intended OFF (stale hook comment still says “Restart resets to False”). It stayed global ON because: (1) code default True, (2) Continue persists/restores `invert_signals` from `atc_state`, (3) `default+` / `default` profile resets **force True**, (4) no `ATC_INVERT` env authority / no per-version gate on this flag (unlike later `ATC_V3_INVERT_ALL`, which defaults OFF).

---

## Timeline (evidence-backed)

| When (ET) | What | Evidence |
|-----------|------|----------|
| ≤ 2026-04-25 | No `INVERT_SIGNALS` symbol in bot | `atc_bot_v5_pre_phase4_backup.py` (2026-04-25 23:09), `atc_bot_v5 4_20 Bad.py`, earlier Apr baks — `has_INV False` |
| 2026-04-27 | SIGNAL INVERTER hook added | Comment block in bot: “SIGNAL INVERTER (2026-04-27)”; hook at signal path. Early intent text (May-1 bak): *test hypothesis that signals are systematically wrong direction due to bar-close timing slippage. Set True to flip every BUY↔SELL.* Hook comment: *Restart resets to False* (original default OFF). |
| 2026-04-27 ~12:22 | State bak **before** invert persistence | `atc_state.json.bak_pre_crypto_etf` — **`invert_signals` NOTFOUND** |
| 2026-04-28 ~17:25–17:29 | Validation BT run + results | `run_bt_invert.bat` (17:25), `bt_invert_validation_results.txt` (17:29, UTF-16 from PowerShell Tee), `bt_1sec_20260428_172929.json` with `"invert_signals": true` |
| 2026-04-28 (same day, after BT) | **DEFAULT FLIPPED True** in code | Comment at `atc_bot_v5.py` ~L2771–2779 documents exact BT numbers; `INVERT_SIGNALS = True` |
| 2026-04-30 | Persist INV across Continue | Save path comment “2026-04-30: Persist runtime overrides… INV state”; key `invert_signals` in state |
| 2026-05-06+ | State backups carry `invert_signals: true` | `atc_state.backup.20260506_pre_v9_expansion.json` and later baks |
| 2026-05-10 | Lane-scope (MR+VWAP then later VWC split) | FIX-V13-MRVWAP comments; INV no longer full-blanket, but **flag default remains True** |
| 2026-06-23+ | VWC direction owned by `VWT_LIVE_MODE`, not blanket INV | Comments / `_MRVWAP_INVERT_LANES` trimmed |
| 2026-07-31 / ongoing | `default+` / `default` **force** `INVERT_SIGNALS = True` | `_apply_default_plus_profile` ~L36557; evidence reset ~L36828 |
| 2026-10-02 | LAB INV killed OFF (this session); CHALLENGER still ON in state | `LAB\atc_state.json` = false; `CHALLENGER\atc_state.json` = true; root `atc_state.json` = true at probe |

---

## 1. When first enabled

- **Feature/hook first enabled:** **2026-04-27** (SIGNAL INVERTER).
- **Default programmed ON:** **2026-04-28**, explicitly after `bt_invert_validation.py` results.

---

## 2. By whom / what

- **No git blame available** (no `git` / `git.exe` on STALIE-MINI PATH).
- Surviving artifacts name the *mechanism*, not a person:
  - `bt_invert_validation.py` — INV-mode 90d BT harness (docstring: hypothesis “flipping every BUY↔SELL… positive expectancy”).
  - `run_bt_invert.bat` — “Tests if INVERT_SIGNALS should ship as default”.
  - In-bot comment block citing that BT by filename and exact P/L.
- **Attribution:** session engineering work dated 2026-04-27/28 baked into `atc_bot_v5.py` + BT scripts. No ledger row / session note found that names Claude vs Codex vs human as the author of the default flip. Treat as **code-authored decision from that BT session**, not a later accidental toggle.

---

## 3. Original intent

Yes — **legacy mean-reversion / wrong-side hypothesis flip**:

1. Apr 27 intent (May-1 bak wording): signals may be systematically wrong-side from **bar-close timing slippage** → flip BUY↔SELL at source to test.
2. Current wording (~L2766): “legacy MR reversion-lane inverter”; VWC not controlled here (owns direction via `VWT_LIVE_MODE`); true trend lanes stay raw.
3. Runtime: `'invert on'` / `'invert off'`.
4. Separate later path: `ATC_V3_INVERT_ALL` (default **OFF**, launcher opt-in) — different from global `INVERT_SIGNALS`.

---

## 4. Why never defaulted OFF / never gated per-version

| Factor | Detail |
|--------|--------|
| **Code default** | `INVERT_SIGNALS = True` at ~L2779 with comment: *Restart restores this default (= MR INV ON)*. |
| **BT justification locked in** | Comment cites A OFF +$102,442/90d vs B ON +$227,250/90d (+$124,808 lift). Bat file framed as “should ship as default”. |
| **Profile stomps** | `default+` and `default`/`restore defaults` set `globals()['INVERT_SIGNALS'] = True` every time. |
| **Session restore** | Continue restores `saved['invert_signals']` when present (~L14479–14484). Save defaults `get('INVERT_SIGNALS', True)` (~L13180). So ON tends to self-perpetuate once saved. |
| **No env override for this flag** | `ATC_INVERT*` count = 0. Contrast: `ATC_V3_INVERT_ALL` exists and defaults OFF. |
| **Not per-version** | Module-level global in shared bot. Lane-scope was added (which *lanes* INV applies to), but not V1/V2/V3 / LAB vs CHALLENGER defaults. Each arm’s `atc_state.json` can diverge after runtime toggle, but fresh code default + DEFAULT+ still point ON. |
| **Stale comment debt** | Hook still says “Restart resets to False” in one place while code default is True — shows original OFF intent never fully cleaned up after the Apr 28 flip. |

---

## BT numbers that flipped the default (from `bt_invert_validation_results.txt`)

Decoded UTF-16 (PowerShell Tee):

- `A_baseline_INV_OFF` → **+$102,442** (112.3 t/d, 82.7% WR)
- `B_INV_ON_default_cascade` → **+$227,250** (117.1 t/d, 84.3% WR)
- C/D (INV ON + gate bypass variants) matched B at +$227,250

Range loaded: 2025-12-08 → 2026-04-17, 90 days, 51 symbols, 1-sec ratchet BT.

Caveat written into the bot comment at ship time: *BT-vs-live gap is 50x+; absolute live numbers will be much smaller. Live monitoring required.*

---

## Code vs restored session state (what actually keeps it ON)

1. **Primary:** **code default True** (~L2779). Fresh process → ON before any state load.
2. **Secondary:** **Continue restore** can keep an operator OFF/ON across restart if `invert_signals` is in `atc_state` and restore path runs.
3. **Tertiary:** **`default+` / `default`** re-force True even if you toggled OFF in-session.
4. **Today’s LAB:** runtime + persist set **false** in `LAB\atc_state.json`. That does **not** change the code default; a Fresh start that ignores saved INV or a DEFAULT+ still returns ON unless code default is changed.

Probe snapshot 2026-10-02 ~12:52 ET:

- `C:\ATC\LAB\atc_state.json` → `invert_signals: false`
- `C:\ATC\CHALLENGER\atc_state.json` → `true`
- `C:\ATC\atc_state.json` (root) → `true`

---

## Specific “commit/config/session” answer

- **No git commit ID** (git unavailable).
- **Config that turned it ON:** in-source assignment `INVERT_SIGNALS = True` with dated comment **2026-04-28 DEFAULT FLIPPED True after bt_invert_validation.py**.
- **Session/artifact that justified it:** `run_bt_invert.bat` + `bt_invert_validation.py` run producing `bt_invert_validation_results.txt` at **2026-04-28 17:29 ET**.
- **Reasoning for leaving global ON:** BT showed large positive lift; ship-as-default decision baked into comments + DEFAULT+; later work narrowed *which lanes* INV touches but never reversed the default to OFF or made it per-version.

---

## Files consulted

- `C:\ATC\atc_bot_v5.py` (L2765–2779, L13176–13180, L14479–14484, L36557, L36828, L38175–38188, L41887+)
- `C:\ATC\atc_bot_v5.py.pre_tailfix` (May-1 bak — clearer Apr-27 intent wording)
- `C:\ATC\bt_invert_validation.py`, `run_bt_invert.bat`, `bt_invert_validation_results.txt`
- State: `atc_state.json`, `LAB\atc_state.json`, `CHALLENGER\atc_state.json`, `atc_state.json.bak_pre_crypto_etf`, `atc_state.backup.20260506_pre_v9_expansion.json`
- Apr baks without INV: `atc_bot_v5_pre_phase4_backup.py` et al.

---

*Receipt written 2026-10-02 by Grok Bot executor. INV not modified by this dig.*
