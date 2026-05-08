# Current Baselines

This file records the only active GitHub and local repo baselines for the graduation project.

## Active Repositories

### 1. riscv_cnn_accelerator

- Local path:
  - `C:\Users\16084\Documents\New project\riscv_cnn_accelerator`
- GitHub:
  - `https://github.com/Justin-Ju-0413/riscv_cnn_accelerator.git`
- Active branch:
  - `codex/a7-bringup-v2-main`
- Remote tracking:
  - `origin/codex/a7-bringup-v2-main`
- Current commit:
  - `ba847db4ecc6d696e55a5576e3e17164ac83cb97`

### 2. e203_hbirdv2

- Local path:
  - `C:\Users\16084\Documents\New project\e203_hbirdv2`
- GitHub:
  - `https://github.com/Justin-Ju-0413/e203_hbirdv2.git`
- Active branch:
  - `codex/a7-bringup-v2-soc`
- Remote tracking:
  - `origin/codex/a7-bringup-v2-soc`
- Current commit:
  - `1d609725740752b4d4de79a903574b94564538d1`

## Historical Branches

These are preserved only as historical references and not as the current baseline:

- `bringup_v1`
- `cnn_bringup_v1`
- `main`
- `master`

## Reporting Line

The current project status should always be described using the active baselines above:

- local RTL regression closed
- software-driven full-SoC regression closed
- hello_e203 board validation closed with UART and ILA evidence
- CNN/NICE board demo closed for the recorded CNN v1 test
- **NICE rs2 index capture bug fixed and board-verified (2026-05-09)**: E203 decode RTL fix + software defense + CNN v1 board regression

## Latest Board-Build Commit Pair

- Date:
  - `2026-04-28`
- `riscv_cnn_accelerator`:
  - `b414e36399ba6d301497a9f03341bd7c880ed779`
  - `fpga: prepare windows davinci bitstream flow`
- `e203_hbirdv2`:
  - `afbf0c4d4ac282166b5be710b9e42d2f672c6e44`
  - `fpga: stabilize davinci source management`
- Evidence:
  - `..\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\BOARD_RUNTIME_EVIDENCE_2026_04_28.md`

## Latest ILA Debug Commit Pair

This commit pair records ILA capture support and the ILA sample-clock change.

- `riscv_cnn_accelerator`:
  - `c3698c2418b3aa8be4aa7c8f36f4a385d89deaa5`
  - `fpga: add vivado ila capture helper`
- `e203_hbirdv2`:
  - `c7337216cf3297c6c1818a8f0b6f90ac6c8a42d8`
  - `fpga: clock ila from stable davinci clock`

## Latest Heartbeat Debug Commit Pair

This commit pair records the minimal Davinci A7 heartbeat debug flow used to isolate board clock/JTAG/ILA behavior from the E203 CPU design.

- Date:
  - `2026-04-28`
- `riscv_cnn_accelerator`:
  - `2028fee0a2d98063a987a04df808877a8aa2fe48`
  - `fpga: add davinci heartbeat build modes`
- `e203_hbirdv2`:
  - `bf87a17b923faed0df640b8271631fc145b6b01b`
  - `fpga: add davinci heartbeat debug tops`
- Evidence:
  - `..\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\heartbeat_direct_ila_capture\ila_summary.txt`
  - `..\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\heartbeat_direct_artifacts\`

## Latest MMCM/Reset Debug Commit Pair

This commit pair records MMCM/reset-chain heartbeat diagnostics.

- Date:
  - `2026-04-28`
- `riscv_cnn_accelerator`:
  - `7b30969020caa6eefb9a631ba3989c0ba57797b7`
  - `fpga: add mmcm heartbeat build modes`
- `e203_hbirdv2`:
  - `f6610c9cd87c3d4c6961c86269c13b061bb949ed`
  - `fpga: add davinci mmcm heartbeat diagnostics`
- Evidence:
  - `..\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\heartbeat_mmcm_ledonly_artifacts\`
  - `..\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\heartbeat_mmcm_dualclk_artifacts\`
  - `..\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\heartbeat_mmcm_dualclk_ila_capture\ila_summary.txt`

## Latest Full SoC Raw-Debug Commit Pair

This commit pair records the full SoC diagnostic build where CPU/SoC logic runs on `clk_16M` and ILA/debug hub runs on raw `sys_clk`.

- Date:
  - `2026-04-28`
- `riscv_cnn_accelerator`:
  - `f75e04a6969ecbfd0fa2eb2b4055670a6785bc50`
  - `fpga: add full soc sysclk ila build mode`
- `e203_hbirdv2`:
  - `3ea17fbbfba7f0ce600ea8c5500bdf7b7de418df`
  - `fpga: add full soc raw sysclk ila diagnostic`
- Evidence:
  - `..\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_sysclk_ila_artifacts\`
  - `..\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_sysclk_ila_ila_capture\ila_summary.txt`
  - `..\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_sysclk_ila_ila_capture\ila_capture.csv`

## Latest Hello E203 Board Validation Commit Pair

This commit pair records the Day 3-4 hello_e203 board validation, three root cause fixes,
and the bootvec ILA diagnostic build mode.

- Date:
  - `2026-04-30`
- `riscv_cnn_accelerator`:
  - `d817dc0`
  - `fpga: add cnn_sysclk_ila build mode for CNN/NICE validation`
- `e203_hbirdv2`:
  - `c20ce47`
  - `fpga: add cnn_sysclk_ila build mode for CNN/NICE validation`
- Evidence:
  - `..\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\hello_e203_board_artifacts\`
- Root causes fixed:
  1. sirv_gnrl_dffs.v #1 delay (simulation only, iverilog event scheduling)
  2. ITCM hex byte vs 64-bit BRAM format (sim + board, Vivado $readmemh)
  3. DTCM hex byte vs 32-bit BRAM format (sim + board)
  4. E203_FORCE_BOOTROM_BOOT not globally visible (board, Vivado verilog_define)

## Latest CPU Boot Diagnostic Commit Pair

This commit pair records the Day 2 diagnostic build where full SoC runs on `clk_16M`, ILA/debug hub runs on raw `sys_clk`, and CPU boot state is exposed through PC activity, IFU/ITCM handshake counters, UART edge state, reset release, cgstop, and debug halt probes.

- Date:
  - `2026-04-29`
- `riscv_cnn_accelerator`:
  - `5a76bc7a489759cf650fc050af6d2ca97acbd551`
  - `fpga: add soc boot diagnostic ila mode`
- `e203_hbirdv2`:
  - `3e2f14d4f312903bb1e248ba724403ef8f73ccad`
  - `fpga: add full soc boot diagnostic ila`
- Evidence:
  - `..\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_bootdiag_sysclk_ila_artifacts\`
  - `..\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_bootdiag_sysclk_ila_ila_capture\ila_summary.txt`
  - `..\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_bootdiag_sysclk_ila_ila_capture\ila_capture.csv`
  - `..\08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan\DAY2_CPU_BOOT_DIAGNOSTIC_ILA_2026_04_29.md`

## Latest NICE rs2 Index Capture Fix (2026-05-09)

This commit pair fixes a hardware bug where the E203 IFU skipped capturing
the rs2 register index for NICE instructions when the index value was 0.
The NICE rs2 field encodes the accelerator vector index (0-3), not a GPR
number. When index=0, the rs2 field is 5'b00000, which the decoder
misinterpreted as "rs2=x0 -> no rs2 needed". This caused ir_rs2idx_ena=0
in the IFU, which retained a stale index from the previous instruction.

The fix moves the rv32_rs2_x0 gating outside the nice_op ternary so NICE
instructions always capture rs2 when nice_need_rs2=1.

- Date:
  - `2026-05-09`
- `riscv_cnn_accelerator`:
  - `ba847db4ecc6d696e55a5576e3e17164ac83cb97`
  - `sw: harden NICE rs2 register constraint against x0 allocation`
- `e203_hbirdv2`:
  - `1d609725740752b4d4de79a903574b94564538d1`
  - `fix: force rs2 index capture for NICE instructions regardless of x0`
- Files changed:
  - `e203_hbirdv2/rtl/e203/core/e203_exu_decode.v` (RTL fix)
  - `riscv_cnn_accelerator/sw/inc/custom_insn.h` (software defense)
- Verification completed:
  - FPGA `cnn_sysclk_ila` bitstream rebuild passed timing
  - Board programming passed on Davinci Pro A7-100T
  - ILA capture completed with stable NICE handshake idle state
  - UART reported SW/HW/Expected outputs all matching and `CNN v1 DEMO PASSED`
- Evidence:
  - `..\04_Experiments\Board_BringUp\2026-05-09_nice_rs2_fix_verification\BOARD_VERIFICATION.md`
  - `..\04_Experiments\Board_BringUp\2026-05-09_nice_rs2_fix_verification\ila_summary.txt`
  - `..\04_Experiments\Board_BringUp\2026-05-09_nice_rs2_fix_verification\uart_output.txt`
