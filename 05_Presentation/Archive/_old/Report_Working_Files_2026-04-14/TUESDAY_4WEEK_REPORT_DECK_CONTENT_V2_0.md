# Tuesday Four-Week Report Deck Content

> **Version**: V2.0 | **Updated**: 2026-04-14 | **Owner**: Justin JU

## Purpose

This document contains ready-to-paste English slide content for the Tuesday
four-week progress report. It is designed to fit the existing weekly-report
PPT template with minimal rewriting.

## Page 1: Title, Goal, And Scope

### Suggested title

`RISC-V CNN Accelerator Progress Report`

### Suggested bullets

- Project: lightweight CNN accelerator based on Hummingbird E203
- Goal: integrate the accelerator through NICE and push the flow from RTL verification to FPGA board validation
- This report focuses on the last four weeks of progress
- Current active baseline: `codex/a7-bringup-v2-main` + `codex/a7-bringup-v2-soc`

### Suggested conclusion line

- This report summarizes the recent progress on the active A7-100T Route A line.

### Speaker notes

- The project is no longer only about accelerator RTL.
- The current work covers the full path from custom instruction integration to board-side validation.
- This report only focuses on the most recent four weeks, not the full project history.

## Page 2: System Architecture

### Suggested title

`System Architecture`

### Suggested bullets

- E203 works as the host CPU
- NICE is used as the custom accelerator interface
- A 4x4 INT8 PE array is used as the CNN compute engine
- Firmware, SDK app, and full-SoC simulation form the software verification path
- The current FPGA target is A7-100T

### Suggested conclusion line

- The project is a complete CPU-to-accelerator-to-board validation flow.

### Speaker notes

- Emphasize that the accelerator is not an isolated RTL block.
- It is attached to the official E203 SoC path through NICE.
- The verification path already includes both software and hardware views.

## Page 3: Four-Week Timeline

### Suggested title

`Progress Over The Last Four Weeks`

### Suggested bullets

- Week 1: confirmed the integration and simulation baseline
- Week 2: closed the software-driven full-SoC path
- Week 3: consolidated pre-board verification and documentation
- Week 4: moved into A7-100T bring-up, including Vivado setup, FPGA download, and Route A observation preparation

### Suggested conclusion line

- The last four weeks moved the project from reproducible simulation closure toward real board-side bring-up.

### Speaker notes

- Keep this page short and chronological.
- Do not list every micro-task.
- Use it to give the audience a quick mental map before the technical pages.

## Page 4: Closed Technical Work

### Suggested title

`Closed Technical Work`

### Suggested bullets

- The E203-to-CNN NICE integration is formally locked
- The command path `CLEAR/WLOAD/DLOAD/COMP/RSTAT` is stable
- Interface safety checks were completed for invalid command, reset, busy blocking, and repeated `RSTAT`
- The software-driven full-SoC flow is already reproducible through the SDK path

### Suggested evidence line

- Evidence: `./Project_Manager.sh run_hw` and `bash scripts/run_sdk_fullsoc_regression.sh` have passed in the current baseline.

### Suggested conclusion line

- The RTL and SoC simulation baseline is already closed and reproducible.

### Speaker notes

- This page is where you establish that the project is technically real and already validated.
- Focus on closed work, not open problems.

## Page 5: Reproducible Result Baseline

### Suggested title

`Reproducible Result Baseline`

### Suggested bullets

- Historical software-driven SoC closure reached `RSTAT=320`
- The current minimal CNN v1 baseline reaches `expected_rstat = 19`
- The current active branch pair is `codex/a7-bringup-v2-main` and `codex/a7-bringup-v2-soc`
- The active baseline can be rerun from the current script entry points

### Suggested small table

| Flow | Entry | Expected result |
|------|-------|-----------------|
| Local RTL baseline | `./Project_Manager.sh run_hw` | pass |
| Full-SoC regression | `bash scripts/run_sdk_fullsoc_regression.sh` | `expected_rstat = 19` |
| Current board prep status | environment and shell prepared | in progress |

### Suggested conclusion line

- The current baseline is measurable and reproducible, not only descriptive.

### Speaker notes

- If asked why the result is now `19`, explain that this is the current minimal CNN v1 baseline, while `320` is the historical dot-product closure reference.

## Page 6: Board Bring-Up Status

### Suggested title

`Board Bring-Up Status`

### Suggested bullets

- The active FPGA target is `davinci_a7_100t`
- The board-side development environment has already been prepared to the bring-up stage
- `PTD04 + Vivado` has already been confirmed for FPGA programming
- The A7-100T Route A bitstream has already been rebuilt
- UART, LED, and ILA observation paths have been added into the current shell

### Suggested conclusion line

- The board build and FPGA download path is prepared, but runtime closure is still ongoing.

### Speaker notes

- This page should make it clear that the project is no longer blocked by synthesis or download.
- The remaining problem is runtime evidence capture on the real board.

## Page 7: Current Blockers

### Suggested title

`Current Blockers`

### Suggested bullets

- The UART COM port still needs to be locked on Windows
- The current bottleneck is soft-core debug on the Davinci Pro A7-100T board
- `PTD04` is currently usable for FPGA programming, but not yet for CPU software debug
- `OpenOCD + GDB load ELF + break main` is still unresolved in the current setup
- A new debug solution is still needed, such as a dedicated soft-JTAG adapter or a later `BSCANE2` bridge

### Suggested conclusion line

- The current blocker is board-side soft-core debugging, not RTL or full-SoC simulation.

### Speaker notes

- This page is important because it shows the project is in the final validation stage.
- Avoid making the blockers sound like major design failures.

## Page 8: Next-Step Plan

### Suggested title

`Next-Step Plan`

### Suggested bullets

- Keep the current simulation baseline stable as the reference line
- Continue Route A observation through UART, LED, and ILA
- Evaluate a new CPU debug solution for the Davinci Pro A7-100T board
- Keep `PTD04 + BSCANE2` as a later research direction
- Close the board-side runtime evidence chain step by step

### Suggested conclusion line

- The next step is to move from board preparation into board-side runtime and debug closure.

### Speaker notes

- End with a confident and bounded plan.
- The message should be: the architecture is stable, and the next work is focused closure.

## Backup Page: Suggested Q And A

### Why E203 + NICE?

- E203 is lightweight and open enough for academic integration work.
- NICE provides a direct custom co-unit path without building a full external bus-based accelerator first.
- It is a good balance between architecture clarity and implementation cost.

### Why did the result change from `320` to `19`?

- `RSTAT=320` is the historical software-driven closure result for the earlier dot-product validation path.
- `expected_rstat = 19` is the current minimal CNN v1 baseline for the active branch.
- They are different checkpoints for different validation targets.

### Why is Route A prioritized over GDB-first debug?

- The current goal is to prove that the board really runs the image.
- UART, LED, and ILA can close that proof chain faster than CPU single-step debug.
- CPU debug is still valuable, but the current blocker shows that a new debug solution is still needed later.

### What does `PTD04` support now?

- It has already been confirmed for FPGA programming through Vivado Hardware Manager.
- It does not yet provide a closed CPU software debug path for the current milestone.
- CPU debug remains a later research item together with `BSCANE2` or a separate OpenOCD-compatible soft-JTAG adapter.

## Tonight Checklist

- Fill the old weekly-report PPT template with the 8 pages above
- Add one architecture figure on Page 2
- Add one 4-week timeline figure or table on Page 3
- Add one result table on Page 5
- Add one board-progress screenshot or photo if available on Page 6
- Rehearse once to keep the talk within 8 minutes
