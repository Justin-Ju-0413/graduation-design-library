# Final Defense Evidence Index

Every thesis/PPT claim below points to an existing evidence file.

| Claim | Result | Evidence path |
|---|---|---|
| RTL simulation | NICE unit behavior verified | `04_Experiments\RTL_Simulation\2026-04-23_baseline_rerun\rtl_sim_results.txt` (exists) |
| Full-SoC simulation | SDK/full-SoC baseline closed | `04_Experiments\FullSoC_Simulation\2026-04-23_baseline_rerun\fullsoc_sim_results.txt` (exists) |
| hello_e203 board | UART and ILA boot-chain evidence | `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\hello_e203_board_artifacts\ila_summary.txt` (exists) |
| hello_e203 UART | board program reached boot/uart ok/loop | `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\hello_e203_board_artifacts\uart_output.txt` (exists) |
| CNN v1 board | HW/SW/Expected match and speedup | `04_Experiments\Board_BringUp\2026-05-09_nice_rs2_fix_verification\uart_output.txt` (exists) |
| CNN ILA | post-fix board ILA capture | `04_Experiments\Board_BringUp\2026-05-09_nice_rs2_fix_verification\ila_capture.csv` (exists) |
| rs2 fix summary | decoder fix board verification | `04_Experiments\Board_BringUp\2026-05-09_nice_rs2_fix_verification\BOARD_VERIFICATION.md` (exists) |
| Baselines | active repo commit pair | `02_Source_Repos\CURRENT_BASELINES.md` (exists) |

## Core Reporting Line

`RTL -> full-SoC -> hello_e203 board -> CNN/NICE board -> rs2 bug fix case study`

## Notes

- Figures in the thesis and deck are redrawn summaries; raw CSV/log/screenshot evidence remains in `04_Experiments/`.
- Do not change numeric claims unless the corresponding evidence file is updated first.