# STAGE ONLY — Cycle 1 INV OFF-default audit (Cursor baseline)

**STAGE ONLY.** No APPLY. No live INV toggle. No paper promote.

| Field | Value |
|---|---|
| Date | 2026-10-02 |
| Agent | Cursor |
| Purpose token | `code_finish` (documentary stamp only) |
| Equivalent asks | Ledger #3922 (Claude) and #3923 (Codex) |
| Mode | Observation only. No bot fired. |

`confirm_qa_alignment.py` is **not in this repo**. The purpose token above is a documentary stamp inside this file. It is not a receipt produced by `C:\ATC\qa\confirm_qa_alignment.py`, and it is not a file under `C:\ATC\qa\receipts\`.

This checkout does not contain `C:\ATC`. Nothing below is a live probe. Ports, PIDs, file hashes, and live gate JSON are not invented. Where a synced doc quotes a port or a gate field, that quote is labeled as documentary text from that file.

## Sources (only these)

| File on `main` | Role in this audit |
|---|---|
| `docs/atc/PRE_DEPLOY_QA_ALIGNMENT.md` | Mandated checks A1–A6 |
| `docs/atc/INVERT_SIGNALS_ORIGIN_20261002.md` | Why the code default is True, and the three mechanisms that keep it ON |
| `docs/atc/LEDGER_SNAPSHOT_20261002.md` | Rows **#3920** and **#3929** only |
| `docs/atc/OPEN_ACTION_PLAN_20261002.md` | Item 4 as it still reads on `main` |

Rubric self-score is omitted. Scoring stays with the orchestrator.

## What A1 requires

A1 in `PRE_DEPLOY_QA_ALIGNMENT.md` (mandatory as of 2026-10-02T12:53:42-04:00):

- `INVERT_SIGNALS` / `invert_signals` defaults **OFF** unless Farid explicitly approved ON for a **named** version/arm (V1 / V2 / V3 / V4-CF12 / shadow lane).
- Per-version approval must be recorded (ledger id + receipt). Global ON is forbidden.
- The historical `pre_deploy_audit.py` expectation of `INVERT_SIGNALS=True` from the 2026-04-28 BT invert validation is **revoked**.

These four files contain no named per-version Farid GO that approves ON for any arm. #3929 says "No approve-ON given" for the V2 kill.

## Action plan on `main` vs #3929

`OPEN_ACTION_PLAN_20261002.md` on `main` (header ~12:53 ET, "Updated: 2026-10-02 12:55 ET") still lists item 4 as **OPEN**:

> V2 CHALLENGER INVERT_SIGNALS still ON. Blocker: flag true in `C:\ATC\CHALLENGER\atc_state.json`; V3 LAB already OFF (#3920). Next: hot POST `/api/gates` inv=false on V2 :5051, or Farid explicit approve-ON.

That next-step is older than the ledger row below. The `:5051` token is text inside the action plan. This audit did not open a port.

**#3929** in the ledger snapshot (generated 2026-10-02T13:00:09.088895-04:00), author grok, 2026-10-02T12:57:48-04:00. The snapshot body is truncated at 286 characters and ends mid-token. Exact visible text:

> V2 CHALLENGER (:5051) INVERT_SIGNALS killed OFF mid-session (Farid plan step 1 / default-OFF). No approve-ON given. BEFORE: file invert_signals=True. AFTER: live gate_status.invert_signals=False; CHALLENGER atc_state.json invert_signals=Fal

What that visible text supports: a mid-session kill to OFF, no approve-ON, file was True before, and a live `gate_status.invert_signals` value of False is asserted in the sentence. The on-disk "after" phrase is cut off at `invert_signals=Fal`. This audit does not complete that token and does not reconstruct a gate JSON document.

**Latest evidence is #3929.** V2 INV is OFF on that row. This audit does not recommend turning INV back ON. The action plan's alternative ("Farid explicit approve-ON") is not a recommendation of this file.

Task context, not a file on this branch: a later orchestrator commit that is **not on `main` yet** marks item 4 DONE-SNAPSHOT because #3929 killed V2 INV OFF at 12:57 ET. This stage does not edit `OPEN_ACTION_PLAN_20261002.md`. The disagreement is recorded here so a reviewer can see that `main`'s action-plan sentence is stale relative to #3929, which is already inside the synced ledger snapshot.

## Origin mechanisms (why OFF is not what the code does)

`INVERT_SIGNALS_ORIGIN_20261002.md` is a read-only receipt. It says the dig did not change INV. Line numbers below are the origin doc's citations of `C:\ATC\atc_bot_v5.py`. That bot is not in this repo, so the line numbers are unreverified here.

Three mechanisms the origin doc names:

1. **Code default True at the Apr 28 BT.** Hook added 2026-04-27 with an OFF intent (a hook comment still says "Restart resets to False"). On 2026-04-28, after `bt_invert_validation.py`, the code default became `INVERT_SIGNALS = True` (~L2779). The in-bot comment cites A OFF +$102,442/90d vs B ON +$227,250/90d. The comment says restart restores that default (MR INV ON). A1 revokes that ship default.
2. **`default+` / `default` force True.** `_apply_default_plus_profile` ~L36557 and the evidence reset ~L36828 set `globals()['INVERT_SIGNALS'] = True` on every profile reset.
3. **Continue restore.** Continue restores `saved['invert_signals']` when present (~L14479–14484). The save path defaults `get('INVERT_SIGNALS', True)` (~L13180), so a missing key persists as ON and ON self-perpetuates once saved.

Related facts from the same origin doc, still documentary:

- No `ATC_INVERT` env authority (count 0). `ATC_V3_INVERT_ALL` is a different flag and defaults OFF.
- The flag is a module-level global in the shared bot. Lane scope limits which lanes INV touches. It does not give V1/V2/V3/LAB/CHALLENGER separate code defaults.
- Probe written as 2026-10-02 ~12:52 ET, which is **before** #3929: `C:\ATC\LAB\atc_state.json` → `invert_signals: false`; `C:\ATC\CHALLENGER\atc_state.json` → `true`; root `C:\ATC\atc_state.json` → `true`. The origin doc states that the LAB persist does not change the code default. A fresh start that ignores saved INV, or a `default+`, still returns ON until the code default changes.

## Per-arm table

| Arm | What the synced docs actually prove | Unknown because `C:\ATC` is not in this repo |
|---|---|---|
| **V1 CHAMPION** | A1 and A6 name CHAMPION/V1. ON would require a named per-version Farid GO (ledger id + receipt). No such GO is in these four files. The origin doc's code default is a shared module-level `INVERT_SIGNALS = True`, so it is not a V1-only default. At the ~12:52 ET probe the origin doc records root `C:\ATC\atc_state.json` `invert_signals: true`. That doc does not identify the root file as the V1 CHAMPION state. #3920's snapshot body is empty. #3929 is about V2. | V1 state path, whether the root file is V1, live `invert_signals`, any change after 12:52 ET, build identity, and any GO that exists only on disk under `C:\ATC`. No port, PID, hash, or live gate JSON is asserted for V1 by this audit. |
| **V2 CHALLENGER** | Origin ~12:52 ET: `C:\ATC\CHALLENGER\atc_state.json` `invert_signals: true`. Action plan item 4 on `main` still says OPEN / still ON (text frozen at 12:55 ET) and names a hot-toggle on `:5051` as a next step. #3929 at 12:57:48 ET is later and is the latest evidence: killed OFF mid-session, no approve-ON, file was True before, `gate_status.invert_signals=False` appears in the truncated sentence, on-disk tail cut off at `invert_signals=Fal`. A1 is satisfied by staying OFF. The origin mechanisms (code default True, `default+` force True, Continue restore) are still described as in force; #3929 does not say those code paths changed. | The unread tail of #3929, any state after 12:57:48 ET, a fresh read of the live gate, the file hash of `CHALLENGER\atc_state.json`, and whether `default+` or Continue has run since the kill. This audit does not re-open `:5051`. |
| **V3 LAB** | Origin live note: V3 LAB hot-set INV OFF and persisted; `C:\ATC\LAB\atc_state.json` `invert_signals: false`; the note cites ledger #3920 and names `:5052` in that sentence. Action plan item 4's blocker text also says "V3 LAB already OFF (#3920)". Snapshot row #3920 itself is only `[grok] 2026-10-02T12:48:24.192140-04:00` plus an empty body, so the OFF claim is carried by the origin doc and the action plan, not by the snapshot sentence. Origin: that persist leaves the code default True, and `default+` or a fresh start that ignores saved INV returns ON. No per-version approve-ON for V3 is in these files. OFF matches A1. | The #3920 message body (absent from this snapshot; the full `messages.jsonl` row is on `C:\ATC`), live gate value after the ~12:52 probe, and whether a later Continue or `default+` put the flag back ON. This audit does not re-open `:5052`. |
| **V4-CF12** | A1 and A6 name V4-CF12 as an arm that needs its own GO before ON. The origin doc, #3920, and #3929 do not mention V4-CF12 `invert_signals`. Action-plan rows about the V4-CF12 paper loop, Tradier VA4414585, and combined-board registration do not state an invert flag. | Whether V4-CF12 loads `INVERT_SIGNALS` at all, which state file it would use, and any live gate. No invert port, PID, hash, or gate JSON is taken from the paper-loop notes. |
| **shadow** | A1 and A6 name the shadow lane. The origin doc, item 4, #3920, and #3929 do not record shadow `invert_signals`. | Shadow invert default, shadow state file, and any live gate. No shadow PID or slot id is imported into this audit. |

Shared conclusion across arms: runtime OFF on V3 (origin + action-plan citation of #3920) and on V2 (#3929) is evidence about saved/live flags at those timestamps. It is not evidence that the code default, the profile reset, or Continue-restore agree with A1. V1, V4-CF12, and shadow remain unproven on invert state inside this repo.

## Staged OFF-default proposal (written plan, not applied)

Goal: make the three origin mechanisms agree with A1. Default OFF unless a named per-version Farid GO (ledger id + receipt) exists for that arm. Global ON stays forbidden.

**No code is applied.** `atc_bot_v5.py` is not in this repo. The sketch uses the origin doc's line citations as the future APPLY sites on `C:\ATC`. This pull request does not contain a bot diff.

### 1. Code default (Apr 28 BT site)

Site the origin doc names: `INVERT_SIGNALS = True` at ~L2779, with the BT comment at ~L2771–2779.

Plan:

- Set the module assignment to `False` so a fresh process is OFF before any state load.
- Keep the 2026-04-28 BT numbers in the comment (A OFF +$102,442 vs B ON +$227,250) and add that A1 revoked that ship default on 2026-10-02.
- Make the Apr 27 hook comment agree with the assignment. The origin doc records a stale "Restart resets to False" comment beside a True assignment. After the change, restart-to-False is the real default, and the comment should say that.

### 2. Profile reset (`default+` / `default` force True)

Sites the origin doc names: `_apply_default_plus_profile` ~L36557 and the evidence / restore-defaults reset ~L36828, both forcing `globals()['INVERT_SIGNALS'] = True`.

Plan:

- Those assignments become `False`.
- A profile reset must not stomp a deliberate OFF back to ON (A4).
- The only True write is a named per-version Farid GO already recorded for that arm (ledger id + receipt). One global True write remains forbidden (A1, A6).

### 3. Continue restore

Sites the origin doc names: restore of `saved['invert_signals']` when present (~L14479–14484); save default `get('INVERT_SIGNALS', True)` (~L13180).

Plan:

- Missing-key save default becomes `False`.
- If the saved value is true, restore True only when that same arm has a named per-version Farid GO on record. Otherwise leave the flag OFF and journal that a saved true was not restored (A4: persistence must not resurrect a disabled flag).
- A2 still requires that a flip, when one is actually in force, be explicit in journals (`entry_was_flipped`, native side, final side). This plan does not add a silent XOR.

### 4. Visibility and arm scope (A3, A6)

- Do not add a hidden env-only flip. The origin doc already records `ATC_INVERT*` count = 0. A new env, if one is ever added on `C:\ATC`, has to show up in live state / gates and default OFF.
- `ATC_V3_INVERT_ALL` stays a separate flag. The origin doc says it already defaults OFF. It is not a substitute for changing `INVERT_SIGNALS`.
- Profile reset and Continue must write the arm whose state file is being restored. A V3 OFF persist must not be the thing that sets V2, and a shared `default+` must not turn every arm ON.

### Explicit non-actions in this proposal

- No edit to a bot in this pull request.
- No APPLY, no launcher start, no reseal.
- No live INV toggle, including no re-toggle of V2 or V3.
- No paper promote.
- No recommendation to turn INV back ON.

```text
NOT APPLIED — plan sketch only — bot source is not in this repo

~L2779   INVERT_SIGNALS = False
         # was True after bt_invert_validation.py on 2026-04-28
         # A1 (2026-10-02) revokes that ship default
         # BT history stays in the comment:
         #   A OFF +$102,442 / 90d ; B ON +$227,250 / 90d

~L36557  globals()['INVERT_SIGNALS'] = False   # default+ ; was True
~L36828  globals()['INVERT_SIGNALS'] = False   # default / restore defaults ; was True
         # True only if this arm has a named Farid GO (ledger id + receipt)

~L13180  get('INVERT_SIGNALS', False)          # save default ; was True

~L14479–14484  Continue:
         if saved invert_signals is true AND this arm has a named Farid GO:
             restore True
         else:
             leave False and journal the suppressed restore
```

## code_finish receipt (documentary)

```text
timestamp: 2026-10-02T17:59:31-04:00
agent: cursor
purpose: code_finish
path: docs/atc/staged/20261002/cursor_cycle1_inv_off_default.md
```

`confirm_qa_alignment.py` is not in this repo. This block does not satisfy a deploy receipt. `PRE_DEPLOY_QA_ALIGNMENT.md` requires a separate `deploy` receipt (freshness <= 1 hour) before any deploy, APPLY, bot start, reseal, or launcher. A `code_finish` stamp does not meet that bar, and this stamp was not written by the enforcer.

| Check | Result | Note from the synced docs only |
|---|---|---|
| A1 | fail | Mandate is OFF unless a named per-version GO. Origin still documents code default True. No approve-ON is recorded. Runtime OFF on V2 (#3929) and V3 (origin + action plan citing #3920) does not change the code default. |
| A2 | not-in-repo | Native side vs submitted side, and `entry_was_flipped` journals, live on `C:\ATC`. These files do not include them. |
| A3 | not-in-repo | The minimum visible set is `INVERT_SIGNALS`, `ATC_MASTER_FLIP`, `ATC_FLIP_SUBMIT`, AFLIP, and contract-flip lanes. #3929 mentions one `gate_status.invert_signals` value in truncated prose. That is not a review of the set, and this agent did not read a live gate. |
| A4 | fail | Origin documents Continue restore plus `default+` / `default` forcing True, which can resurrect ON after a deliberate OFF. Live three-way agreement (gates, on-disk, post-Continue) is not in this repo; the resurrect paths themselves are. |
| A5 | not-in-repo | `pre_deploy_audit.py`, build-guard identity, and `C:\ATC\qa\receipts\` are not in this repo. `confirm_qa_alignment.py` is not in this repo. |
| A6 | fail | Origin: module-level global, not per-version; fresh code default and `default+` still point ON for every arm that runs that bot. The ~12:52 probe shows LAB false while CHALLENGER and root were true, so that one persist did not rewrite the other two files. Whether any later edit bled is not in this repo. |

Checklist result is the documentary judgment of this stage. It is not a PASS from `require_qa_alignment.py`.

## What this stage concluded

1. A1's mandated default is OFF. The origin doc shows the code still defaults ON because of the 2026-04-28 BT, and two other mechanisms (`default+` force True, Continue restore with a True save default) put ON back.
2. On `main`, action-plan item 4 still says V2 is OPEN and ON. #3929 at 12:57 ET is the latest evidence and records the V2 kill OFF with no approve-ON. Leave V2 OFF. Do not turn INV back ON.
3. V3 LAB OFF is attested by the origin doc and the action plan via #3920, while the snapshot row #3920 has an empty body. That OFF is a persisted flag, not a code-default change.
4. V1 CHAMPION, V4-CF12, and shadow have no `invert_signals` proof in the files this audit was allowed to use.
5. The repair is a written plan against the three origin sites. It is not an applied patch. Bot source is not in this repo.
