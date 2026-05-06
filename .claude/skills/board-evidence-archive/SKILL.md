---
name: board-evidence-archive
description: Use when a board run (bitstream build, FPGA program, ILA capture) completes and evidence needs to be archived. Also use when recording board-level results with evidence paths. Trigger phrases: "archive evidence", "archive board run", "归档证据", "save ILA capture", "record board result", "archive artifacts".
version: 1.0.0
---

# Board Evidence Archive

Archives board-level FPGA artifacts after each run into the proper evidence directory structure.

## Evidence Root

`C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check`

## Directory Structure

Each build mode gets two subdirectories under the evidence root:

```
{mode}_artifacts/
  - system.bit           (bitstream)
  - system.ltx           (ILA probe file for Vivado hardware manager)
  - timing_summary.txt   (timing report: WNS, WHS, failing endpoints)
  - route_status.txt     (route status output)
  - build_log.txt        (relevant build log excerpts)

{mode}_ila_capture/
  - ila_summary.txt      (human-readable ILA summary)
  - ila_capture.csv      (CSV export of ILA waveform data)
  - conclusion.txt       (one-line conclusion from the capture)
```

## Archiving Procedure

### After bitstream build
1. Copy `system.bit` from `{SoC}/fpga/davinci_a7_100t/build/` to `{mode}_artifacts/`
2. Copy `system.ltx` from build dir to `{mode}_artifacts/`
3. Extract timing summary (WNS, WHS, failing endpoints) from Vivado log
4. Note route status (routed, unrouted, timing failures)

### After ILA capture
1. Save CSV from Vivado ILA dashboard to `{mode}_ila_capture/ila_capture.csv`
2. Write `ila_summary.txt` with:
   - Capture status (CAPTURED / IDLE / etc.)
   - Window size and trigger condition
   - Each probe's observed values (min, max, notable patterns)
   - Key signal interpretation
3. Write `conclusion.txt` with one-line decision and next action

## ILA Summary Template

```text
ILA Capture: {build_mode}
Date: {date}
Status: CAPTURED / IDLE / FAILED
Samples: 1024
Clock: sys_clk_raw (50 MHz) / clk_16M (16 MHz)

probe0_pc: {observed values}
probe1_reset_uart: {observed values and bit meanings}
  sys_rst_n={}, mmcm_locked={}, reset_periph={}, uart_txd={}
probe2_liveness: {observed values and bit meanings}
probe3_pc_activity: {observed values, delta}
probe4_nice_csr: {observed values and bit meanings}
probe5_nice_hs: {observed values and bit meanings}
probe6_mem_status: {observed values and bit meanings}

Conclusion: {one-line interpretation}
Next action: {concrete next step}
```

## Evidence Archiving Rules

1. Every board run must archive: command, bitstream, .ltx, timing report, ILA summary, CSV, UART note, conclusion
2. Never overwrite previous captures - use new directories or versioned filenames
3. Bitstream and .ltx must be from the same build (matching timestamps)
4. CSV must include the full ILA capture window, not a subset
5. If UART has no output, explicitly record "no UART output" - never omit

## Additional Artifacts (if applicable)

- UART log or screenshot -> `{mode}_ila_capture/uart_log.txt`
- LED status notes -> `{mode}_ila_capture/led_status.txt`
- Preload verification -> `{mode}_artifacts/preload_check.txt`
- Extra XDC content -> `{mode}_artifacts/extra.xdc`
