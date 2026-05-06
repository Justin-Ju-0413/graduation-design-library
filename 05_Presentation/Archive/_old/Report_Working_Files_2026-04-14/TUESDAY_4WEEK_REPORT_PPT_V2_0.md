# Tuesday Four-Week Report PPT Guide

> **Version**: V2.0 | **Updated**: 2026-04-13 | **Owner**: Justin JU

## Purpose

This document is the practical guide for preparing the Tuesday report about
the last four weeks of work. It is not a full defense deck. It is a short,
evidence-driven progress report for an advisor or lab meeting.

## Core Message

Use one sentence to anchor the whole talk:

> The project has already closed the RTL, SoC, SDK, and FPGA download
> baseline, and the current work is focused on closing the final A7-100T
> Route A board evidence chain.

## Time Budget

- Total deck: 8 to 10 slides
- Total speaking time: about 8 minutes
- Recommended pace: about 45 to 60 seconds per slide

## Slide Plan

### Slide 1: Title, Goal, And Scope

Answer this question:

> What project am I reporting, and what part of it is covered in this report?

Include:

- project title
- one-sentence project goal
- this report only covers the last four weeks
- current active baseline is `codex/a7-bringup-v2-*`

Page conclusion:

- This report focuses on the last four weeks of progress on the active A7-100T Route A line.

### Slide 2: System Architecture

Answer this question:

> What system am I actually building?

Include:

- E203 CPU
- NICE interface
- CNN accelerator
- firmware and SDK verification path
- FPGA board target

Use:

- one architecture diagram if possible

Page conclusion:

- The project is a full chain from custom instruction integration to board validation, not only an isolated accelerator module.

### Slide 3: Four-Week Timeline

Answer this question:

> What did I move forward in the last four weeks?

Break the four weeks into four lines:

- Week 1: integration and simulation baseline confirmation
- Week 2: software-driven full-SoC path closure
- Week 3: pre-board verification and documentation consolidation
- Week 4: A7-100T Route A, Vivado programming, UART/LED/ILA observability

Use:

- a simple timeline or 4-row table

Page conclusion:

- The last four weeks moved the project from reproducible simulation closure toward real board evidence collection.

### Slide 4: Closed Technical Work

Answer this question:

> What has already been solved and verified?

Include:

- RTL/NICE integration locked
- interface safety closed
- SDK full-SoC software path closed
- reproducible command chain available

Use evidence:

- `./Project_Manager.sh run_hw`
- `bash scripts/run_sdk_fullsoc_regression.sh`
- `bash scripts/run_preboard_verification.sh`

Page conclusion:

- The software and simulation baseline is already reproducible and no longer the main project risk.

### Slide 5: Reproducible Result Baseline

Answer this question:

> What concrete technical results can I reproduce now?

Include:

- historical SoC closure result: `RSTAT=320`
- current minimal CNN v1 baseline: `expected_rstat = 19`
- current branch pair
- current reproduction entry scripts

Use:

- one small table with command and expected result

Page conclusion:

- The current active baseline is measurable and reproducible, not only descriptive.

### Slide 6: FPGA And Board Progress

Answer this question:

> What has already been completed on the FPGA side?

Include:

- A7-100T as the active target
- Route A as the active strategy
- `PTD04 + Vivado` programming succeeded
- bitstream rebuild succeeded
- UART, LED, and ILA have been wired for runtime evidence

Page conclusion:

- The board build and download path is already closed; the remaining work is runtime evidence capture.

### Slide 7: Current Blockers

Answer this question:

> What is still missing before I can claim board-side closure?

Include:

- UART COM port still needs to be locked
- UART milestones still need to be archived
- LED stage observation still needs to be archived
- ILA CPU/NICE activity still needs to be archived
- CPU debug via `PTD04` is not the current gate

Page conclusion:

- The blocker is no longer integration or build failure; it is the final Route A evidence chain.

### Slide 8: Next Step

Answer this question:

> What will I do immediately after this report?

Include:

- capture UART milestones
- observe LED stage transition
- capture ILA activity
- archive board evidence
- keep `BSCANE2` as a later track

Page conclusion:

- The next step is to close board evidence, not to redesign the architecture.

### Optional Slide 9: Backup

Prepare backup answers for:

- why E203 + NICE
- why the current result changed from `320` to `19`
- why Route A is prioritized over GDB-first debug
- what `PTD04` currently supports and does not support

## What To Say On Each Slide

Keep the oral explanation in the same three-step structure:

1. what the goal was
2. what was done
3. what evidence proves the current result

Do not say:

- which files were edited
- every small branch-management detail
- unrelated historical experiments

Do say:

- what problem was solved
- how it was verified
- what conclusion can now be claimed

## Evidence Checklist

Before Tuesday, make sure each core slide has at least one concrete proof item:

- branch or baseline name
- pass command
- result value
- bitstream rebuild success
- `PTD04 + Vivado` programming success
- open board evidence list

## Self-Check Before The Report

- Slide 1 can explain the project and this report scope in 30 seconds
- Slide 2 can explain the system without requiring code-level background
- Slide 3 clearly covers the last four weeks, not the full project lifetime
- Slides 4 to 6 each include at least one concrete evidence item
- Slide 7 clearly separates closed work from open work
- Slide 8 gives a concrete next-step plan for the next week
- The whole talk fits within about 8 minutes

## Source Documents To Reuse

- `docs/CURRENT_STATE.md`
- `docs/PHASE_HISTORY.md`
- `docs/PROGRESS.md`
- `docs/DAVINCI_A7_100T_BRINGUP_V2_0.md`
- `docs/PRESENTATION_OUTLINE_V2_0.md`
