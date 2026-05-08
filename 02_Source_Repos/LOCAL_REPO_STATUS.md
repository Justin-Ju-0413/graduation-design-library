# Local Repo Status

This file explains how local repo content and Windows library content are separated.

## Current Repo State

### riscv_cnn_accelerator

- Branch:
  - `codex/a7-bringup-v2-main`
- Remote tracking:
  - `origin/codex/a7-bringup-v2-main`
- Current commit:
  - `ba847db4ecc6d696e55a5576e3e17164ac83cb97`
- Working tree state:
  - current baseline records the NICE rs2 software hardening commit

### e203_hbirdv2

- Branch:
  - `codex/a7-bringup-v2-soc`
- Remote tracking:
  - `origin/codex/a7-bringup-v2-soc`
- Current commit:
  - `1d609725740752b4d4de79a903574b94564538d1`
- Working tree state:
  - current baseline records the NICE rs2 decoder fix commit

## Latest Board Verification

- Date: `2026-05-09`
- Evidence folder:
  - `..\04_Experiments\Board_BringUp\2026-05-09_nice_rs2_fix_verification\`
- Result:
  - `cnn_sysclk_ila` board programming passed.
  - ILA capture completed.
  - UART reported SW/HW/Expected outputs all matching and `CNN v1 DEMO PASSED`.

## What Should Stay In Git Repos

- source code
- repo-owned project documents
- simulation and integration scripts that belong to development
- codebase-level technical docs

## What Should Stay Only In The Windows Library

- final PPT files
- report speaking scripts
- detailed explanation notes for presentation
- QA sheets for rehearsal
- report-ready screenshots
- archived intermediate slide materials

## Practical Rule

If a file exists mainly for reporting, rehearsal, or presentation delivery, it should live in `Graduation_Design_Library`, not inside the repo working tree.
