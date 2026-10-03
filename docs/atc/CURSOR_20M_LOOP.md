# Cursor 20-minute ATC ledger loop

Armed 2026-10-02 17:55 ET by the Cursor cloud orchestrator. **Stopped 2026-10-02 20:21 ET** at Farid's request. Do not re-arm `atc-ledger-20m` unless asked.

## Every tick

1. Re-read `docs/atc/CURSOR_CLOUD_LEDGER.md`, `LEDGER_SNAPSHOT_20261002.md`, `OPEN_ACTION_PLAN_20261002.md`, and `BOT_BAKEOFF_SCOREBOARD.md`.
2. Diff `git log` on `main` and this branch since the previous tick. Treat a new snapshot or new `CC-` row as a work change.
3. List open stage-only work. Skip anything that needs Farid GO or a secret, and skip anything a cloud agent already has in review (open draft PR or running agent) unless the ledger shows that work changed again.
4. Spin up one cloud agent per independent thread. Scale to workload: zero agents when nothing new is actionable. Each agent writes only its own file under `docs/atc/staged/<YYYYMMDD>/` and opens a **draft** PR against `main` for review.
5. Append one `CC-` row to `CURSOR_CLOUD_LEDGER.md` with: what was read, what changed, which agents were staged (or why none), and what stayed blocked. Commit and push that ledger update.

## Hard limits

- Stage for review. Do not APPLY, reseal, restart paper, promote CF12, arm Push-to-Fleet, fire a bake-off bot, or loosen a gate.
- Do not overwrite `PRE_DEPLOY_QA_ALIGNMENT.md`.
- Do not invent live port, PID, or fill measurements. This VM does not have `C:\ATC`.
- Do not assign Windows ledger ids. Use `CC-` ids in `CURSOR_CLOUD_LEDGER.md`.

## Timer

Name: `atc-ledger-20m`  
Interval: 20 minutes (`delaySeconds` 1200), recurring.  
Status: **stopped** 2026-10-02 20:21 ET. Subscription `sub_4b43ffb2-7ede-4d10-9125-727ded454baf` closed. Last delivery was 7 at 20:02 ET (CC-0011).
