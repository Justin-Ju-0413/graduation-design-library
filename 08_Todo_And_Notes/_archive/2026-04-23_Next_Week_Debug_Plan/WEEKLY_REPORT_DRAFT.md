# Weekly Report Draft

## This Week's Focus

This week focuses on keeping the verified RTL/full-SoC simulation baseline reproducible, while moving the main effort toward the Davinci Pro A7-100T soft-core debug path.

## Current Progress

- Windows has been organized as the final work center.
- The active GitHub baselines are fixed:
  - `riscv_cnn_accelerator`: `codex/a7-bringup-v2-main`
  - `e203_hbirdv2`: `codex/a7-bringup-v2-soc`
- Previous evidence already shows:
  - local RTL regression passed with `[TB_PASS]`
  - full-SoC regression passed with `expected_rstat = 19`

## Current Technical Focus

The current problem is no longer mainly about RTL function or full-SoC simulation. The key issue is the board-side soft-core debug path:

- `PTD04 + Vivado` is usable for FPGA programming.
- `OpenOCD + GDB` is not yet closed for CPU software debug.
- A new debug solution is likely needed.

## Next Actions

- Rerun `run_hw` and full-SoC regression on Ubuntu once SSH or local terminal access is available.
- Save new logs and screenshots into the Windows library.
- Compare independent soft-JTAG and BSCANE2-based debug paths.
- Try to collect UART, LED, or ILA evidence if board access is available.

## One-Minute Oral Update

This week my main goal is to keep the current simulation baseline stable and then focus on the board-side soft-core debug issue. The RTL regression and full-SoC regression already have verified evidence, including `[TB_PASS]` and `expected_rstat = 19`. The current blocker is not the accelerator RTL itself, but the CPU software debug path on the Davinci Pro A7-100T board. PTD04 can be used for FPGA programming, but the OpenOCD and GDB path is not closed yet. So next I will compare a dedicated OpenOCD-compatible soft-JTAG solution with a possible BSCANE2-based route, and try to collect basic UART, LED, or ILA evidence if board access is available.
