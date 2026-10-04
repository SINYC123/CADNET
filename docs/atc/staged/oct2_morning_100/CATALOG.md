# October 2 morning catalog — 100 staged cells

Draft only. `ARMED` is false. This file is the results table.

Time-bar legend: `HIT` is the one observed generator receipt. `SAME_CLOCK` reuses that entry clock and adds no dollar. `FAIL` is a reference book whose first journal fill is 11:09:03 ET. `BLOCKED` has no tape or no gate record.

Dollar legend: the three reference books are cited. Every other dollar cell is `BLOCKED`.

Missing codes:

| Code | File |
|---|---|
| TAPE_0830 | raw tick tape 2026-10-02 08:30-09:00 ET (not in oct2_pack; bars10s_2026-10-02.csv.gz was omitted from the pack and the October 2 simulation starts at 09:00) |
| BARS_EXIT | `C:\ATC\claude_harness\cf12_20261002\data\bars10s_2026-10-02.csv.gz` (sha256 e615fdcc3669651444e4274ec010a75bb2cd0a49ce288b18127457abb1447ea5), omitted from the pack |
| PEAK | journal exit rows have no peak / MFE field |
| SPY_LOG | no SPY refuse log; missing `C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V1.jsonl`, `C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V2.jsonl`, `C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V3.jsonl` |
| SIGNALS | `C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V1.jsonl`, `C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V2.jsonl`, `C:\ATC\claude_harness\exit_full_20261002\D_signals\signals_V3.jsonl` |

| id | kind | premarket | deadline | spy | notional | exit | by 9:35 | by 10:30 | dollars | missing |
|---|---|---|---|---|---:|---|---|---|---:|---|
| S001 | grid | absent | 935 | off_strong_own_rvol_trend | 50000 | as_traded_giveback | HIT | HIT | BLOCKED | BARS_EXIT |
| S002 | grid | absent | 935 | off_strong_own_rvol_trend | 50000 | keep_peak_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK |
| S003 | grid | absent | 935 | off_strong_own_rvol_trend | 50000 | trend_keep_peak_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK |
| S004 | grid | absent | 935 | off_strong_own_rvol_trend | 50000 | peak_lock_keep_80_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK |
| S005 | grid | absent | 1030 | off_strong_own_rvol_trend | 50000 | as_traded_giveback | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT |
| S006 | grid | absent | 1030 | off_strong_own_rvol_trend | 50000 | keep_peak_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK |
| S007 | grid | absent | 1030 | off_strong_own_rvol_trend | 50000 | trend_keep_peak_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK |
| S008 | grid | absent | 1030 | off_strong_own_rvol_trend | 50000 | peak_lock_keep_80_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK |
| S009 | grid | absent | force_hc_1030 | off_strong_own_rvol_trend | 50000 | as_traded_giveback | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+SIGNALS |
| S010 | grid | absent | force_hc_1030 | off_strong_own_rvol_trend | 50000 | keep_peak_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK+SIGNALS |
| S011 | grid | absent | force_hc_1030 | off_strong_own_rvol_trend | 50000 | trend_keep_peak_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK+SIGNALS |
| S012 | grid | absent | force_hc_1030 | off_strong_own_rvol_trend | 50000 | peak_lock_keep_80_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK+SIGNALS |
| S013 | grid | absent | 935 | off_strong_own_rvol_trend | 100000 | as_traded_giveback | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT |
| S014 | grid | absent | 935 | off_strong_own_rvol_trend | 100000 | keep_peak_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK |
| S015 | grid | absent | 935 | off_strong_own_rvol_trend | 100000 | trend_keep_peak_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK |
| S016 | grid | absent | 935 | off_strong_own_rvol_trend | 100000 | peak_lock_keep_80_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK |
| S017 | grid | absent | 1030 | off_strong_own_rvol_trend | 100000 | as_traded_giveback | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT |
| S018 | grid | absent | 1030 | off_strong_own_rvol_trend | 100000 | keep_peak_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK |
| S019 | grid | absent | 1030 | off_strong_own_rvol_trend | 100000 | trend_keep_peak_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK |
| S020 | grid | absent | 1030 | off_strong_own_rvol_trend | 100000 | peak_lock_keep_80_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK |
| S021 | grid | absent | force_hc_1030 | off_strong_own_rvol_trend | 100000 | as_traded_giveback | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+SIGNALS |
| S022 | grid | absent | force_hc_1030 | off_strong_own_rvol_trend | 100000 | keep_peak_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK+SIGNALS |
| S023 | grid | absent | force_hc_1030 | off_strong_own_rvol_trend | 100000 | trend_keep_peak_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK+SIGNALS |
| S024 | grid | absent | force_hc_1030 | off_strong_own_rvol_trend | 100000 | peak_lock_keep_80_look | SAME_CLOCK | SAME_CLOCK | BLOCKED | BARS_EXIT+PEAK+SIGNALS |
| S025 | grid | absent | 935 | on | 50000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S026 | grid | absent | 935 | on | 50000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S027 | grid | absent | 935 | on | 50000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S028 | grid | absent | 935 | on | 50000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S029 | grid | absent | 1030 | on | 50000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S030 | grid | absent | 1030 | on | 50000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S031 | grid | absent | 1030 | on | 50000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S032 | grid | absent | 1030 | on | 50000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S033 | grid | absent | force_hc_1030 | on | 50000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S034 | grid | absent | force_hc_1030 | on | 50000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S035 | grid | absent | force_hc_1030 | on | 50000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S036 | grid | absent | force_hc_1030 | on | 50000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S037 | grid | absent | 935 | on | 100000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S038 | grid | absent | 935 | on | 100000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S039 | grid | absent | 935 | on | 100000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S040 | grid | absent | 935 | on | 100000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S041 | grid | absent | 1030 | on | 100000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S042 | grid | absent | 1030 | on | 100000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S043 | grid | absent | 1030 | on | 100000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S044 | grid | absent | 1030 | on | 100000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S045 | grid | absent | force_hc_1030 | on | 100000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S046 | grid | absent | force_hc_1030 | on | 100000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S047 | grid | absent | force_hc_1030 | on | 100000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S048 | grid | absent | force_hc_1030 | on | 100000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | SPY_LOG |
| S049 | grid | present | 935 | off_strong_own_rvol_trend | 50000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S050 | grid | present | 935 | off_strong_own_rvol_trend | 50000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S051 | grid | present | 935 | off_strong_own_rvol_trend | 50000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S052 | grid | present | 935 | off_strong_own_rvol_trend | 50000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S053 | grid | present | 1030 | off_strong_own_rvol_trend | 50000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S054 | grid | present | 1030 | off_strong_own_rvol_trend | 50000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S055 | grid | present | 1030 | off_strong_own_rvol_trend | 50000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S056 | grid | present | 1030 | off_strong_own_rvol_trend | 50000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S057 | grid | present | force_hc_1030 | off_strong_own_rvol_trend | 50000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S058 | grid | present | force_hc_1030 | off_strong_own_rvol_trend | 50000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S059 | grid | present | force_hc_1030 | off_strong_own_rvol_trend | 50000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S060 | grid | present | force_hc_1030 | off_strong_own_rvol_trend | 50000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S061 | grid | present | 935 | off_strong_own_rvol_trend | 100000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S062 | grid | present | 935 | off_strong_own_rvol_trend | 100000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S063 | grid | present | 935 | off_strong_own_rvol_trend | 100000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S064 | grid | present | 935 | off_strong_own_rvol_trend | 100000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S065 | grid | present | 1030 | off_strong_own_rvol_trend | 100000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S066 | grid | present | 1030 | off_strong_own_rvol_trend | 100000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S067 | grid | present | 1030 | off_strong_own_rvol_trend | 100000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S068 | grid | present | 1030 | off_strong_own_rvol_trend | 100000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S069 | grid | present | force_hc_1030 | off_strong_own_rvol_trend | 100000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S070 | grid | present | force_hc_1030 | off_strong_own_rvol_trend | 100000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S071 | grid | present | force_hc_1030 | off_strong_own_rvol_trend | 100000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S072 | grid | present | force_hc_1030 | off_strong_own_rvol_trend | 100000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S073 | grid | present | 935 | on | 50000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S074 | grid | present | 935 | on | 50000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S075 | grid | present | 935 | on | 50000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S076 | grid | present | 935 | on | 50000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S077 | grid | present | 1030 | on | 50000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S078 | grid | present | 1030 | on | 50000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S079 | grid | present | 1030 | on | 50000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S080 | grid | present | 1030 | on | 50000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S081 | grid | present | force_hc_1030 | on | 50000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S082 | grid | present | force_hc_1030 | on | 50000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S083 | grid | present | force_hc_1030 | on | 50000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S084 | grid | present | force_hc_1030 | on | 50000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S085 | grid | present | 935 | on | 100000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S086 | grid | present | 935 | on | 100000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S087 | grid | present | 935 | on | 100000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S088 | grid | present | 935 | on | 100000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S089 | grid | present | 1030 | on | 100000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S090 | grid | present | 1030 | on | 100000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S091 | grid | present | 1030 | on | 100000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S092 | grid | present | 1030 | on | 100000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S093 | grid | present | force_hc_1030 | on | 100000 | as_traded_giveback | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S094 | grid | present | force_hc_1030 | on | 100000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S095 | grid | present | force_hc_1030 | on | 100000 | trend_keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S096 | grid | present | force_hc_1030 | on | 100000 | peak_lock_keep_80_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
| S097 | reference:journal | absent | as_traded | unrecorded | as_filled | as_traded_giveback | FAIL | FAIL | -2647.77 |  |
| S098 | reference:broker | absent | as_traded | unrecorded | as_filled | as_traded_giveback | FAIL | FAIL | -2208.95 |  |
| S099 | reference:scorer | absent | as_traded | unrecorded | as_filled | as_traded_giveback | FAIL | FAIL | -2041.95 |  |
| S100 | handoff | present | 935 | off_strong_own_rvol_trend | 100000 | keep_peak_look | BLOCKED | BLOCKED | BLOCKED | TAPE_0830 |
