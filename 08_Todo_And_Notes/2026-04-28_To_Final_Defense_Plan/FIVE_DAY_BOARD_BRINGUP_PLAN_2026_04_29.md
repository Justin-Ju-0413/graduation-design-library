# Five-Day Board Bring-up Execution Plan

This is the active local project-management plan for the next engineering cycle.
All following board bring-up work should start from this file unless the priority is explicitly changed.

## Current Baseline

- Date started: 2026-04-29
- Main repo:
  - `riscv_cnn_accelerator`
  - branch `codex/a7-bringup-v2-main`
  - commit `5a76bc7a489759cf650fc050af6d2ca97acbd551`
- SoC repo:
  - `e203_hbirdv2`
  - branch `codex/a7-bringup-v2-soc`
  - commit `3e2f14d4f312903bb1e248ba724403ef8f73ccad`
- Starting evidence:
  - `heartbeat_mmcm_sysclk_ila` raw `sys_clk` ILA capture passed.
  - `soc_sysclk_ila` full SoC raw `sys_clk` ILA capture passed.
  - Full SoC reset is released on board.
  - PC/activity/bus probes are visible through ILA.

## Main Chain

`soc_sysclk_ila evidence -> CPU boot diagnosis -> hello_e203 -> UART/ILA closure -> CNN/NICE preparation`

## Daily Tracking Format

Use this block for each day. Update only the current day when work is completed or blocked.

```text
Status: TODO / IN_PROGRESS / DONE / BLOCKED
Date:
Main output:
Evidence path:
Decision:
Next action:
```

## Operating Rules

- Work follows this plan by default.
- If a day finishes early, continue with the first unfinished task from the next day.
- If a blocker appears, record the blocker, evidence, and next hypothesis before switching paths.
- Board evidence is archived under:
  - `04_Experiments\Board_BringUp\2026-04-28_board_connection_check`
- Repo baselines are recorded in:
  - `02_Source_Repos\CURRENT_BASELINES.md`
  - `02_Source_Repos\LOCAL_REPO_STATUS.md`

## Day 1: Freeze Full SoC Observation And Clarify PC/UART Signals

```text
Status: DONE
Date: 2026-04-29
Main output: `soc_sysclk_ila` signal interpretation and `probe_pc` wiring conclusion
Evidence path: `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_sysclk_ila_ila_capture`; `DAY1_SOC_SYSCLK_ILA_SIGNAL_INTERPRETATION_2026_04_29.md`
Decision: `probe_pc` is IFU inspect PC (`e203_ifu_ifetch.pc_r`), not commit PC; use activity counters and fetch/ITCM handshakes for Day 2.
Next action: Build CPU boot diagnostic ILA with fetch/ITCM counters, UART TX edge counter, reset release, halt/cgstop, and real trap/status signals.
```

Goal:

- Convert the successful `soc_sysclk_ila` capture into a clear CPU-state interpretation.

Tasks:

- Review `soc_sysclk_ila` CSV and summarize PC, PC activity, reset, UART TX, NICE, and memory bus fields.
- Trace `probe_pc` in RTL and decide whether it is a reliable architectural PC signal.
- Identify whether the current evidence points to boot image, PC probe wiring, halt/trap, UART pinmux, or software initialization.
- Define the next diagnostic probe set for CPU boot.

Outputs:

- `soc_sysclk_ila` probe explanation table.
- PC probe wiring conclusion.
- Next diagnostic probe list.

Success criteria:

- The meaning of `probe0_pc=00000000/00000002` is explained or marked as unreliable with evidence.
- The next debug direction is narrowed to a concrete cause group.

Failure branch:

- If `probe_pc` cannot be traced clearly, prioritize adding unambiguous activity counters over interpreting sampled PC values.

## Day 2: Build CPU Boot Diagnostic ILA

```text
Status: DONE
Date: 2026-04-29
Main output: `soc_bootdiag_sysclk_ila` build, timing-clean bitstream, board program, and ILA capture
Evidence path: `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_bootdiag_sysclk_ila_artifacts`; `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_bootdiag_sysclk_ila_ila_capture`; `DAY2_CPU_BOOT_DIAGNOSTIC_ILA_2026_04_29.md`
Decision: Reset is released, MMCM is locked, raw `sys_clk` ILA upload is captured, no cgstop/debug halt is observed, UART TX stays idle high, direct IFU-to-ITCM counters are zero, and PC activity continues. Proceed to `hello_e203` with boot/preload/UART as the first diagnosis branch if output is silent.
Next action: Build minimal `hello_e203` image with explicit stage markers and raw `sys_clk` ILA observation.
```

Goal:

- Determine whether the CPU fetches instructions, traps, halts, stays in reset, or runs without UART output.

Tasks:

- Add or adjust raw `sys_clk` ILA probes for CPU boot diagnosis:
  - fetch or ITCM request/response activity counter
  - PC-change counter
  - trap/halt/cgstop sticky flags
  - reset release counter
  - UART TX edge counter
- Build the diagnostic bitstream.
- Confirm timing is clean.
- Program the board and capture ILA CSV.

Outputs:

- CPU boot diagnostic bitstream artifacts.
- ILA summary and CSV.
- One-line CPU state judgment.

Success criteria:

- ILA upload remains `CAPTURED`.
- The evidence distinguishes at least one of: reset blocked, no fetch, active fetch, trap, halt/cgstop, or UART-only failure.

Failure branch:

- If timing fails, fix only mode-specific diagnostic CDC or known clock-as-data paths.
- If ILA upload fails, rerun `heartbeat_mmcm_sysclk_ila` as sanity check before changing CPU logic.

## Day 3: Build Minimal `hello_e203` Board Image

```text
Status: DONE
Date: 2026-04-29/30
Main output: `hello_e203` image, `hello_sysclk_ila` timing-clean bitstream, board program/capture, and blocker note
Evidence path: `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\hello_sysclk_ila_artifacts`; `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\hello_sysclk_ila_ila_capture`; `DAY3_HELLO_E203_PRELOAD_AND_BLOCKER_2026_04_29.md`
Decision: Hello image generation and bitstream build are closed, but board execution is not proven; UART/GPIO17 stays idle and IFU-to-ITCM counters remain zero even after fixing ELF entry and forcing bootrom reset vector.
Next action: Add boot-vector/IFU-address/MROM-vs-ITCM diagnostic before moving to CNN/NICE.
```

Goal:

- Prepare a minimal board program that can prove software execution through UART and ILA.

Tasks:

- Create or locate a minimal `hello_e203` bare-metal app.
- Ensure the program emits staged evidence:
  - early boot stage marker
  - UART hello string
  - loop heartbeat or GPIO/stage update
- Generate ELF, ITCM/DTCM image, and Verilog preload files.
- Build a hello bitstream using raw `sys_clk` ILA observation.
- Verify the bitstream uses the intended preload image.

Outputs:

- hello ELF and preload image paths.
- hello bitstream artifacts.
- timing report.
- preload-to-bitstream mapping note.

Success criteria:

- Bitstream builds successfully and timing is clean.
- ILA can observe reset release and program-stage or PC/activity changes.

Failure branch:

- If image generation is unclear, stop and document the exact image/preload flow before changing hardware.

## Day 4: Validate `hello_e203` On Board

```text
Status: TODO
Date: 2026-05-02
Main output:
Evidence path:
Decision:
Next action:
```

Goal:

- Close the minimal board runtime loop.

Tasks:

- Program the hello bitstream.
- Capture UART output or screenshot.
- Capture ILA CSV in the same run.
- Record LED or stage behavior if available.
- Classify the result.

Outputs:

- `hello_e203_board_artifacts`
- `hello_e203_ila_capture`
- UART screenshot or no-output record.
- Board runtime conclusion.

Success criteria:

- Best case: UART prints hello or staged boot text.
- Minimum acceptable case: ILA proves the program reaches a known stage and explains why UART is not visible.

Failure branch:

- If UART is silent but PC/activity continues, focus on UART pinmux, GPIOA[17], baud rate, and software initialization.
- If PC/activity stops, focus on boot address, ITCM preload, reset, halt, or trap.

## Day 5: Start CNN/NICE Board Validation Or Close Hello Blocker

```text
Status: TODO
Date: 2026-05-03
Main output:
Evidence path:
Decision:
Next action:
```

Goal:

- Move from hello evidence to CNN/NICE evidence, or produce a precise blocker report if hello is not closed.

Tasks if hello is successful:

- Build `cnn_accel_demo` board image.
- Prepare raw `sys_clk` ILA probes for NICE CSR, NICE request/response, memory bus, and cycle/activity summary.
- Generate CNN bitstream.
- Program and capture first CNN/NICE board evidence.

Tasks if hello is still blocked:

- Do not switch to CNN.
- Write a blocker report with command history, evidence paths, failed hypothesis, and next hypothesis.
- Update project status and baseline docs.

Outputs:

- Success path:
  - CNN/NICE first board artifacts and capture.
  - UART or ILA result summary.
- Blocked path:
  - hello bring-up blocker report.
  - next action list.

Success criteria:

- If hello is closed, CNN/NICE board validation has a first capture.
- If hello is blocked, the blocker is specific enough to continue without rediscovery.

## Daily Closeout Checklist

At the end of every day, archive or update:

- command used
- bitstream and `.ltx`
- timing summary
- route status if available
- ILA summary
- ILA CSV
- UART screenshot or no-output note
- one-line conclusion
- next action
