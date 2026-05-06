# Graduation Design Project - FPGA Bring-Up

## Repos
- Main: `C:\Users\16084\Documents\New project\riscv_cnn_accelerator` (branch `codex/a7-bringup-v2-main`)
- SoC: `C:\Users\16084\Documents\New project\e203_hbirdv2` (branch `codex/a7-bringup-v2-soc`)

## Key Paths
- Board src: `{SoC}/fpga/davinci_a7_100t/src/`
- Board script: `{SoC}/fpga/davinci_a7_100t/script/`
- Vivado: `D:\Xilinx\Vivado\2023.2\bin\vivado.bat`
- FPGA part: `xc7a100tfgg484-2`
- Evidence: `04_Experiments/Board_BringUp/2026-04-28_board_connection_check/`
- Plans: `08_Todo_And_Notes/2026-04-28_To_Final_Defense_Plan/`

## Active Plan Files
- Master: `MASTER_PLAN.md`
- Ten-Day: `TEN_DAY_CLOSURE_TASK_BOOK_2026_04_29.md`
- Five-Day: `FIVE_DAY_BOARD_BRINGUP_PLAN_2026_04_29.md`
- Weekly: `WEEKLY_CHECKLIST.md`

## Build Commands
```powershell
# Build bitstream
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Invoke-Vivado-Fpga.ps1 -BuildMode {mode} -Action bit

# Current modes: soc, soc_sysclk_ila, soc_bootdiag_sysclk_ila, hello_sysclk_ila, heartbeat, heartbeat_direct, heartbeat_mmcm_ledonly, heartbeat_mmcm_dualclk, heartbeat_mmcm_sysclk_ila

# Build hello_e203 image
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Build-HelloE203.ps1
```

## Current Status (2026-04-29)
- Day 1 DONE: `soc_sysclk_ila` interpretation, `probe_pc` = IFU inspect PC
- Day 2 DONE: CPU boot diagnostic ILA, no cgstop/halt, UART idle, IFU-to-ITCM zero
- Day 3 BLOCKED: `hello_e203` bitstream OK, but board PC=0x00000000, IFU counters zero
- Next: Add boot-vector/IFU-address/MROM-vs-ITCM diagnostic

## Skills Available
- `/new-ila-build` - Add a new ILA diagnostic FPGA build mode
- `/day-closeout` - Update daily status across tracking files
- `/board-evidence-archive` - Archive board run artifacts
