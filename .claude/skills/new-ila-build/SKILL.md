---
name: new-ila-build
description: Use when the user needs to add a new ILA diagnostic FPGA build mode. This skill handles creating the system.v top file, XDC constraints, updating Invoke-Vivado-Fpga.ps1, and building/flashing/capturing. Trigger phrases: "add ILA build mode", "new diagnostic ILA", "create new probe", "new sysclk ila variant", "add boot diagnostic probes".
version: 1.0.0
---

# New ILA Diagnostic Build Mode

This skill automates adding a new ILA-based FPGA diagnostic build mode to the E203 FPGA bring-up flow.

## Overview

Every time we need new ILA probes for debugging, we follow the same pattern:
1. Create `*_system.v` top-level wrapper with CDC logic and probe assignments
2. Create `*.xdc` timing constraints
3. Register the build mode in `Invoke-Vivado-Fpga.ps1`
4. Build bitstream, program board, capture ILA

## File Paths

- SoC repo: `C:\Users\16084\Documents\New project\e203_hbirdv2`
- Main repo: `C:\Users\16084\Documents\New project\riscv_cnn_accelerator`
- Board src: `{SoC}/fpga/davinci_a7_100t/src/`
- Board script: `{SoC}/fpga/davinci_a7_100t/script/`
- Vivado script: `{Main}/scripts/Invoke-Vivado-Fpga.ps1`
- Install RTL: `{SoC}/fpga/install/rtl/`
- Evidence root: `C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check`

## Procedure

### Step 1: Create the system.v top-level file

Copy the closest existing variant (e.g., `hello_sysclk_ila_system.v` or `soc_bootdiag_sysclk_ila_system.v`) to a new name.

The file must contain:
- MMCM instantiation (50 MHz sys_clk -> 16 MHz clk_16M)
- `reset_sys` instantiation
- `e203_soc_top` DUT with all probe wires connected
- CDC logic: 16 MHz domain registers (`*_cpu`) -> two-flop sync to 50 MHz domain (`*_meta` -> `*_sync`)
- 7-probe ILA (`ila_runtime`) clocked on `sys_clk_raw`
- Probe width limits: probe0=32, probe1=4, probe2=3, probe3=32, probe4=32, probe5=4, probe6=3

Key decisions when creating a new variant:
- `bootrom_n_i_ival`: `1'b0` for mask-ROM boot, `1'b1` for QSPI flash boot
- Which probe signals to expose (PC, IFU, UART, NICE, memory bus, traps, etc.)
- Whether to use `E203_FORCE_BOOTROM_BOOT` define

### Step 2: Create the .xdc timing constraints file

Copy from closest existing `.xdc`. Must include at minimum:
```tcl
set_property PACKAGE_PIN ... [get_ports sys_clk]
set_property PACKAGE_PIN ... [get_ports sys_rst_n]
# ... all pin constraints from board
set_false_path -from [get_clocks clk_16M_mmcm] -to [get_clocks sys_clk_pin]
```

### Step 3: Register in Invoke-Vivado-Fpga.ps1

Three changes needed in the script:

**a)** Add to `[ValidateSet(...)]` on line 4:
```powershell
[ValidateSet("soc", ..., "new_mode_name")]
```

**b)** Add to `$topNames` hash (around line 46):
```powershell
new_mode_name = "new_mode_system.v"
```

**c)** Add EXTRA_XDCS block (after line 108):
```powershell
if ($BuildMode -eq "new_mode_name") {
    $extraXdc = Join-Path $boardDir "script\new_mode_name.xdc"
    if (-not (Test-Path $extraXdc)) {
        throw "New mode XDC not found: $extraXdc"
    }
    $env:EXTRA_XDCS = (& $normalize $extraXdc)
}
```

### Step 4: Build, program, and capture

Standard build and capture commands reference:
```
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\Invoke-Vivado-Fpga.ps1 -BuildMode {mode} -Action bit
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\Invoke-Vivado-Fpga.ps1 -BuildMode {mode} -Action setup
```

For capture, use the Vivado Tcl script:
```
vivado -mode batch -source scripts/capture_vivado_ila.tcl
```

### Step 5: Archive evidence

Create subdirectories under the evidence root:
- `{mode}_artifacts/` - bitstream, .ltx, timing summary, route status
- `{mode}_ila_capture/` - ILA summary, CSV

### Step 6: Write day summary note

Create day note at:
`08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan\DAY{N}_{DESCRIPTION}_{date}.md`

### Step 7: Commit to both repos

```bash
cd "C:\Users\16084\Documents\New project\e203_hbirdv2"
git add -A && git commit -m "fpga: add {mode} build mode"
cd "C:\Users\16084\Documents\New project\riscv_cnn_accelerator"
git add -A && git commit -m "fpga: add {mode} build mode"
```

## ILA Probe Mapping Reference

Current probe assignments across modes:

| Probe | Width | Typical Signal |
|-------|-------|---------------|
| probe0 | 32 | PC value (pc_sync) |
| probe1 | 4 | {sys_rst_n, mmcm_locked_sync, reset_periph_sync, uart_txd_sync} |
| probe2 | 3 | Liveness: IFU/Trap/Halt flags |
| probe3 | 32 | PC change counter |
| probe4 | 32 | IFU req/rsp counts or NICE CSR |
| probe5 | 4 | UART TX / GPIO or NICE handshake |
| probe6 | 3 | Reset release, cgstop, dbg_halt |

## Common CDC Pattern

```verilog
// 16 MHz domain
always @(posedge clk_16M) begin
  if (reset_periph) begin
    signal_cpu <= 0;
  end else begin
    signal_cpu <= source_signal;
    // optional: count edges, set sticky flags
  end
end

// 50 MHz domain (ILA clock)
always @(posedge sys_clk_raw or negedge sys_rst_n) begin
  if (!sys_rst_n) begin
    signal_meta <= 0;
    signal_sync <= 0;
  end else begin
    signal_meta <= signal_cpu;
    signal_sync <= signal_meta;
  end
end
```

## Current Build Modes

- `soc` - default SoC, no special ILA probes, QSPI boot
- `hello_sysclk_ila` - hello_e203 with mask-ROM boot, PC/IFU/UART probes
- `soc_bootdiag_sysclk_ila` - CPU boot diagnostic, QSPI boot, full IFU probes
- `soc_sysclk_ila` - Full SoC raw debug, QSPI boot, NICE+memory probes
- `heartbeat_mmcm_sysclk_ila` - Minimal no-SoC MMCM/ILA sanity check
- `heartbeat_mmcm_dualclk` - Dual-clock MMCM test
- `heartbeat_mmcm_ledonly` - LED-only MMCM test
- `heartbeat_direct` - Direct clock LED heartbeat
- `heartbeat` - Basic heartbeat
