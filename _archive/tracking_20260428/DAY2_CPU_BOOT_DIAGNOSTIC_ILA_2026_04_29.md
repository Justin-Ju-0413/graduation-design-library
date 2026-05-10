# Day 2 CPU Boot Diagnostic ILA

Date: 2026-04-29

## Purpose

Day 2 adds `soc_bootdiag_sysclk_ila` as a full-SoC diagnostic build. The SoC still runs from MMCM-generated `clk_16M`; ILA/debug hub runs from raw `sys_clk`. CPU boot state is reduced into counters and sticky flags in the CPU clock domain, then synchronized into the raw debug clock domain.

## Build Result

Command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\Invoke-Vivado-Fpga.ps1 -BuildMode soc_bootdiag_sysclk_ila -Action bit
```

Result:

```text
write_bitstream completed successfully
WNS=13.337 ns
WHS=0.039 ns
TNS failing endpoints=0
THS failing endpoints=0
```

Artifacts:

- `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_bootdiag_sysclk_ila_artifacts\`

## Board Capture Result

Program/capture command used the archived bitstream and `.ltx` from `soc_bootdiag_sysclk_ila_artifacts`.

Result:

```text
PROGRAM_PASS=soc_bootdiag_sysclk_ila_system.bit
HW_ILAS=hw_ila_1
ILA_CAPTURE_STATUS=CAPTURED
Samples=1024
```

Capture archive:

- `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_bootdiag_sysclk_ila_ila_capture\ila_summary.txt`
- `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_bootdiag_sysclk_ila_ila_capture\ila_capture.csv`

## Probe Decode

```text
probe0_pc: observed 00000000 and 00000002
probe1_reset_uart: d
  sys_rst_n=1, mmcm_locked=1, reset_periph=0, uart_txd=1
probe2_liveness: 0
  ifu_req_seen=0, ifu_rsp_seen=0, trap_or_halt=0
probe3_pc_activity: 000f79d9 -> 000f7a05
probe4_nice_csr: 00000000
  ifu_req_count=0, ifu_rsp_count=0
probe5_nice_hs: 4
  uart_tx_edge_seen=0, uart_txd_sync=1, gpio17_oe=0, gpio17_oval=0
probe6_mem_status: 4
  reset_released_seen=1, core_cgstop_seen=0, dbg_halt_seen=0
```

## Decision

The board is not reset-blocked: `sys_rst_n=1`, `mmcm_locked=1`, `reset_periph=0`, and `reset_released_seen=1`.

No debug halt or core clock stop was observed. UART TX stayed idle high and no UART TX edge was captured. The IFU inspect PC activity counter continued increasing, but the direct IFU-to-ITCM request/response counters stayed at zero in this capture.

This points away from board clock/reset/JTAG/ILA failure. Day 3 should proceed to a minimal `hello_e203` image with explicit software stage markers, and if UART remains silent the first branch should be boot address / preload / UART initialization rather than MMCM or debug-hub bring-up.

Note: `probe_commit_trap` is still not a real exposed trap signal in the current path, so the Day 2 trap conclusion is limited to no debug halt and no sticky `trap_or_halt` assertion in this diagnostic build.

## Next Action

Start Day 3:

- create or locate minimal `hello_e203`
- generate ELF and ITCM/DTCM preload artifacts
- build a raw `sys_clk` ILA hello bitstream
- capture UART and ILA evidence from the same programmed design
