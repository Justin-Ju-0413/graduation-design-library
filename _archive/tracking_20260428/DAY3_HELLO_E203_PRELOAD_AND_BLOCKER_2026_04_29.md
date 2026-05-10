# Day 3 hello_e203 Preload And Blocker Note

Date: 2026-04-29

## Purpose

Day 3 started the minimal `hello_e203` board image. The goal was to prove software execution with a small ITCM-resident program before returning to CNN/NICE.

## Implemented

- Added a freestanding `hello_e203` image:
  - `_start` linked at `0x80000000`
  - GPIOA bit 0 LED/stage marker
  - GPIOA IOF bits 16/17 configured for UART0 RX/TX
  - UART0 initialized for the 16 MHz SoC clock
  - staged strings: `hello_e203: boot`, `hello_e203: uart ok`, `hello_e203: loop`
- Added `Build-HelloE203.ps1` to build ELF/verilog/ITCM/DTCM preload files using the Vitis RISC-V GCC toolchain.
- Added `hello_sysclk_ila` build mode.
- Added `hello_sysclk_ila_system.v`, based on the raw `sys_clk` ILA diagnostic top.
- Added `E203_FORCE_BOOTROM_BOOT` for hello install RTL so `pc_rtvec` is forced to `0x00001000`; the mask ROM then jumps to ITCM `0x80000000`.

## Build Result

Command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\Build-HelloE203.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\Invoke-Vivado-Fpga.ps1 -BuildMode hello_sysclk_ila -Action bit
```

Result:

```text
hello_e203 _start: 0x80000000
hello_sysclk_ila build: write_bitstream completed successfully
hello_sysclk_ila timing: WNS=14.204 ns, WHS=0.060 ns, no failing endpoints
hello_sysclk_ila program/capture: PROGRAM_PASS, ILA_CAPTURE_STATUS=CAPTURED
```

Artifacts:

- `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\hello_sysclk_ila_artifacts\`
- `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\hello_sysclk_ila_ila_capture\`

## Capture Decode

```text
probe0_pc: observed 00000000 and 00000002
probe1_reset_uart: d
  sys_rst_n=1, mmcm_locked=1, reset_periph=0, uart_txd=1
probe2_liveness: 0
  ifu_req_seen=0, ifu_rsp_seen=0, trap_or_halt=0
probe3_pc_activity: 000e5182 -> 000e51ae
probe4_nice_csr: 00000000
  ifu_req_count=0, ifu_rsp_count=0
probe5_nice_hs: 4
  uart_tx_edge_seen=0, uart_txd_sync=1, gpio17_oe=0, gpio17_oval=0
probe6_mem_status: 4
  reset_released_seen=1, core_cgstop_seen=0, dbg_halt_seen=0
```

## Decision

`hello_e203` is not closed yet. The image and bitstream are reproducible and timing-clean, and raw `sys_clk` ILA upload remains reliable, but the board capture does not show UART/GPIO stage activity or direct IFU-to-ITCM handshakes.

The first failed hypothesis was that the ELF entry was not at `0x80000000`; this was fixed. The second failed hypothesis was bootrom pad deglitch timing; `E203_FORCE_BOOTROM_BOOT` now forces `pc_rtvec=0x00001000`, but the board capture still did not show hello execution.

## Next Action

Add a narrower boot-vector diagnostic that exposes or summarizes:

- `pc_rtvec`
- IFU request PC/address before ITCM decode
- MROM request/response count
- ITCM request/response count
- first observed fetch address region
- optional direct software stage register written by `hello_e203`

Do not move to CNN/NICE board validation until this boot/preload branch is explained.
