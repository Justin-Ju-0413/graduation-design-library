# Graduation Design Library Index

This folder is the navigation index for the Windows-side master library.

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

## Final Submission Baseline

- Use `..\14_final_submit\v2` as the authoritative final hand-in package.
- Complete archive tag: `fyp-final-v2-complete-archive-2026-05-14`.
- Key files:
  - Thesis DOCX: `..\14_final_submit\v2\thesis\FYP_Thesis_Final_v2_SUBMISSION_BASELINE.docx`
  - Thesis PDF reference: `..\14_final_submit\v2\thesis\main_final_SUBMISSION_REFERENCE.pdf`
  - Thesis LaTeX source archive: `..\14_final_submit\v2\thesis_latex_source`
  - Final defense PPT: `..\14_final_submit\v2\presentation\FYP_Final_Defense_English_Draft_REPORT_BASELINE.pptx`
  - Manifest: `..\14_final_submit\v2\BASELINE_MANIFEST.txt`

## Primary Entry Points

- Repo baseline and current commits:
  - `..\02_Source_Repos\CURRENT_BASELINES.md`
- Workspace policy:
  - `..\02_Source_Repos\WINDOWS_WORKSPACE_POLICY.md`
- Final submission package:
  - `..\14_final_submit\v2\README.md`
- Final defense preparation workspace:
  - `..\10_Final_Defense\README.md`
- Active thesis source:
  - `..\thesis_latex`
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
- `10_Final_Defense`
  - Final defense slides, scripts, QA, and evidence package
- `13_thesis_bak`
  - Historical thesis backup snapshot
- `14_final_submit`
  - Final submission packages and locked baselines
- `thesis_latex`
  - Active LaTeX thesis source tree
