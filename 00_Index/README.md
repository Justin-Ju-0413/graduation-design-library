# Graduation Design Library

This folder is the Windows-side master library for the graduation project.

## Current Rule

- Windows is the only long-term document and presentation center.
- `C:\Users\16084\Documents\New project` is the code workspace.
- Ubuntu is used for development, simulation, and board-side execution only.
- The active baseline is:
  - `riscv_cnn_accelerator`: `codex/a7-bringup-v2-main`
  - `e203_hbirdv2`: `codex/a7-bringup-v2-soc`
- Latest board-build commit pair:
  - `riscv_cnn_accelerator`: `f75e04a6969ecbfd0fa2eb2b4055670a6785bc50`
  - `e203_hbirdv2`: `3ea17fbbfba7f0ce600ea8c5500bdf7b7de418df`

## Primary Entry Points

- Current active task book:
  - `..\08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan\TEN_DAY_CLOSURE_TASK_BOOK_2026_04_29.md`
- Teacher-facing ten-day task book:
  - `..\08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan\TEACHER_TASK_BOOK_10_DAY_CLOSURE_2026_04_29.md`
- Five-day board bring-up subplan:
  - `..\08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan\FIVE_DAY_BOARD_BRINGUP_PLAN_2026_04_29.md`
- Repo baseline and current commits:
  - `..\02_Source_Repos\CURRENT_BASELINES.md`
- Workspace policy:
  - `..\02_Source_Repos\WINDOWS_WORKSPACE_POLICY.md`
- Roadmap to final defense:
  - `..\08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan\MASTER_PLAN.md`
- Final presentation files:
  - `..\05_Presentation\README.txt`
- Thesis process Word documents:
  - `..\03_Documents\Thesis_Materials\README.md`

## Current Strong Evidence

- Local RTL regression:
  - `[TB_PASS] mock NICE regression completed`
- Full-SoC regression:
  - `expected_rstat = 19`
  - `[PHASE4_PASS] sdk build, image split, and full-SoC regression passed`
- Davinci A7 board connection:
  - `CHECK_PASS: xc7a100t_0 detected`
  - `PROGRAM_PASS: ...\system.bit`
  - `heartbeat_direct` ILA capture passed with incrementing `probe0_counter`
  - `heartbeat_mmcm_dualclk` timing met after CDC false path, but ILA upload still failed
  - `heartbeat_mmcm_sysclk_ila` raw `sys_clk` ILA capture passed while observing MMCM/reset/`clk_16M`
  - `soc_sysclk_ila` full SoC raw `sys_clk` ILA capture passed with reset released and PC/activity/bus probes visible

## Folder Map

- `01_Project_Overview`
  - Short summaries and architecture snapshots
- `02_Source_Repos`
  - GitHub baselines, repo status, and workspace rules
- `03_Documents`
  - Project docs, weekly reports, and thesis materials
- `04_Experiments`
  - RTL simulation, full-SoC simulation, board bring-up, and logs
- `05_Presentation`
  - Final deck, scripts, explanations, QA, screenshots, and archived versions
- `06_References`
  - Papers, manuals, datasheets, and tool references
- `07_Backups`
  - Older working copies and exported snapshots
- `08_Todo_And_Notes`
  - Open issues and next steps
  - `2026-04-28_To_Final_Defense_Plan`
    - master roadmap from current progress to final defense
- `09_Thesis_Writing`
  - Thesis outline, chapter notes, references, figures, and drafts
- `10_Final_Defense`
  - Final defense slides, scripts, QA, and evidence package
