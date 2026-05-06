# Usage Guide

This guide defines how to use the Windows library as the only long-term work center.

## Work Separation

- Code workspace:
  - `C:\Users\16084\Documents\New project`
- Master library:
  - `C:\Users\16084\Documents\Graduation_Design_Library`
- Ubuntu:
  - run simulations, board-side tests, and toolchain tasks
  - copy final evidence back to the Windows library

## Repo Rule

- Only treat these as the active baselines:
  - `riscv_cnn_accelerator`: `codex/a7-bringup-v2-main`
  - `e203_hbirdv2`: `codex/a7-bringup-v2-soc`
- Do not use `main`, `master`, `bringup_v1`, or `cnn_bringup_v1` as the current work baseline.

## Presentation Rule

- Use final report materials only from `05_Presentation`.
- Use these files by default:
  - `Final\Tuesday_4Week_Report_Final_CN_Fixed.pptx`
  - `Scripts\Tuesday_4Week_Report_Per_Page_Bilingual_Script_Final.docx`
  - `Explanations\Tuesday_4Week_Report_Detailed_Explanation_CN.docx`
  - `QA\Tuesday_4Week_Report_QA_Bilingual_Practical.docx`
- Treat everything under `05_Presentation\Archive` as reference only.

## Thesis Rule

- Use `09_Thesis_Writing` as the only thesis writing center.
- Keep chapter notes, thesis figures, reference plans, and drafts there.
- Build thesis claims from existing evidence in `04_Experiments` and `05_Presentation`.
- Do not overstate board-level progress: soft-core software debug is still the current blocker.

## Final Defense Rule

- Use `10_Final_Defense` as the only final defense preparation center.
- Keep final slides, scripts, QA, and defense evidence there.
- The defense story must match the thesis story and the current GitHub baseline.

## Evidence Rule

- Put final evidence screenshots into `05_Presentation\Screenshots`.
- Put raw logs and additional experiment records into `04_Experiments`.
- Keep only the strongest, report-ready figures in the main presentation folders.

## Final Roadmap Rule

- Use `08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan` as the master roadmap from the current engineering state to final defense.
- Development, thesis writing, and final defense must follow the same evidence chain:
  - `RTL_PASS -> full-SoC PASS -> hello_e203 board run -> cnn_accel_demo board evidence -> final defense`
- If board evidence is missing, record the exact blocker instead of writing it as completed.

## Maintenance Rule

- Keep helper scripts under `C:\Users\16084\Documents\New project\$archive\tools`.
- Do not store final slide decks or final scripts inside the repo working tree.
- If material is useful but no longer current, move it to `Archive` instead of deleting it.
