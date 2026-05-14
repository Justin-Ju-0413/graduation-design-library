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
- Use `00_Index\DESIGN_ITERATION_HISTORY.md` for design evolution traceability.
- Use `00_Index\VERSION_MANAGEMENT.md` before creating a new final baseline.

## Presentation Rule

- Use `14_final_submit\v2\presentation` for the locked final defense baseline.
- Use `10_Final_Defense` for editable defense preparation materials.
- Treat `05_Presentation\Archive` as reference only.

## Thesis Rule

- Use `14_final_submit\v2\thesis` for the locked thesis submission baseline.
- Use `thesis_latex` for the active LaTeX source tree.
- Use `14_final_submit\v2\thesis_latex_source` as the archived source snapshot matching the final v2 package.
- Build thesis claims from evidence in `04_Experiments` and final deliverables in `14_final_submit\v2`.

## Final Defense Rule

- Use `10_Final_Defense` as the only final defense preparation center.
- Keep final slides, scripts, QA, and defense evidence there.
- The defense story must match the thesis story and the current GitHub baseline.

## Evidence Rule

- Put final evidence screenshots into `05_Presentation\Screenshots`.
- Put raw logs and additional experiment records into `04_Experiments`.
- Keep only the strongest, report-ready figures in the main presentation folders.

## Final Roadmap Rule

- Treat `08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan` as a historical closure roadmap.
- Current development, thesis writing, and final defense traceability must follow the same evidence chain:
  - `RTL_PASS -> full-SoC PASS -> hello_e203 board run -> cnn_accel_demo board evidence -> final defense`
- If board evidence is missing, record the exact blocker instead of writing it as completed.

## Maintenance Rule

- Keep repository maintenance helpers under `scripts` or `tools`.
- Store locked final deliverables only under `14_final_submit\v2`.
- If material is useful but no longer current, move it to `Archive` instead of deleting it.

## GitHub Upload Rule

- Run `powershell -ExecutionPolicy Bypass -File scripts/check_github_upload.ps1` before pushing.
- Final deliverables in `14_final_submit\v2` are intentionally tracked even though large document formats are ignored elsewhere.
- Do not rely on ordinary `git add .` for ignored file types; use the upload check script and explicit `git add -f` only for deliberate final artifacts.
