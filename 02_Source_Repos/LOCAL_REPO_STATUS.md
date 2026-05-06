# Local Repo Status

This file explains how local repo content and Windows library content are separated.

## Current Repo State

### riscv_cnn_accelerator

- Branch:
  - `codex/a7-bringup-v2-main`
- Remote tracking:
  - `origin/codex/a7-bringup-v2-main`
- Current commit:
  - `5a76bc7a489759cf650fc050af6d2ca97acbd551`
- Working tree state:
  - clean after pushing `soc_bootdiag_sysclk_ila` build mode

### e203_hbirdv2

- Branch:
  - `codex/a7-bringup-v2-soc`
- Remote tracking:
  - `origin/codex/a7-bringup-v2-soc`
- Current commit:
  - `3e2f14d4f312903bb1e248ba724403ef8f73ccad`
- Working tree state:
  - clean after pushing full SoC CPU boot diagnostic ILA

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
