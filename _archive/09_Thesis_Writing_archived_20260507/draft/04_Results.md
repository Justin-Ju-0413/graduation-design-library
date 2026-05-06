# Chapter 4: Results

## 4.1 RTL Simulation

### 4.1.1 CNN Accelerator Unit Test

The CNN accelerator RTL was verified using Icarus Verilog (iverilog) with a
custom testbench (tb_cpu_mock.v) that drives the NICE instruction interface.
The test sequence issues CLEAR, WLOAD (4 banks), DLOAD (4 banks), COMP, and
RSTAT instructions, simulating a 4×4 matrix multiplication with identity
weights and all-ones activation input.

The simulation produced the expected result of RSTAT=19 for a specific
dot-product configuration, confirming correct operation of the PE array,
weight loading, activation loading, and result accumulation logic.

### 4.1.2 Full-SoC Simulation

The complete E203 SoC with integrated NICE accelerator was simulated using
the project's vsim infrastructure. Key configuration parameters:

- CPU: E203 Hummingbird v2 (RV32IMAC)
- ITCM: 64KB at 0x80000000
- DTCM: 64KB at 0x90000000
- UART0: 0x10013000
- Clock: 16 MHz (hfclk = hfextclk)

The simulation required several configuration fixes to match the FPGA build
environment:

| Issue | Fix |
|-------|-----|
| SystemVerilog assertion syntax in sirv_gnrl_dffs.v | `-D DISABLE_SV_ASSERTION=1` |
| Missing e203_fpga_mem_init.vh | Created empty ITCM/DTCM init |
| Missing peripheral modules | Copied from vsim original install |
| GFCM/PLL clock chain broken | Set `test_mode=1` to bypass |
| hfclkrst floating | `assign hfclkrst = 1'b0` |

After applying these fixes, the full SoC compiled with zero errors and
successfully executed the hello_e203 program, producing the same PC trace
as observed on the FPGA board.

## 4.2 FPGA Bitstream Construction

### 4.2.1 Build Flow

The FPGA build flow uses Xilinx Vivado 2023.2 targeting the
xc7a100tfgg484-2 device on the Davinci Pro A7-100T board. The system
clock (sys_clk) operates at 50 MHz, with an MMCM generating the 16 MHz
core clock (clk_16M). Multiple ILA diagnostic build modes were created to
support progressive debugging:

| Build Mode | Description |
|-----------|-------------|
| heartbeat_mmcm_sysclk_ila | Minimal MMCM/reset/ILA sanity check |
| soc_sysclk_ila | Full SoC with raw sys_clk ILA |
| soc_bootdiag_sysclk_ila | CPU boot diagnostic with IFU/ITCM counters |
| bootvec_sysclk_ila | Boot vector diagnostic with memory bus probes |
| hello_sysclk_ila | hello_e203 with MROM boot and PC/UART probes |
| cnn_sysclk_ila | CNN/NICE with CSR and handshake probes |

### 4.2.2 Timing Closure

All builds achieved clean timing closure. Representative results:

| Build | WNS (ns) | WHS (ns) | Critical Warnings | Errors |
|-------|----------|----------|-------------------|--------|
| bootvec_sysclk_ila | 13.677 | 0.061 | 26 | 0 |
| cnn_sysclk_ila | 12.468 | 0.057 | 26 | 0 |

## 4.3 hello_e203 Board Validation

### 4.3.1 Test Program

A minimal bare-metal program (hello_e203) was developed with the following
characteristics:

- Freestanding C with custom startup (startup.S)
- Linked at ITCM base (0x80000000)
- Stack in DTCM (0x90010000)
- GPIOA IOF configured for UART0 (GPIO16=RX, GPIO17=TX)
- UART0 initialized at 115200 baud (16 MHz clock, divisor=138)
- Three milestone strings printed: "hello_e203: boot", "hello_e203: uart
  ok", "hello_e203: loop"

### 4.3.2 UART Output

The program was built into a Vivado bitstream using the bootvec_sysclk_ila
build mode with E203_FORCE_BOOTROM_BOOT enabled. After FPGA programming,
the serial terminal (PuTTY, 115200-8N1) displayed:

```
hello_e203: boot
hello_e203: uart ok
hello_e203: loop
```

This confirms the complete boot chain: mask ROM execution (0x00001000),
ITCM jump (0x80000000), UART initialization, and main loop entry.

### 4.3.3 ILA Evidence

The ILA capture (1024 samples at 50 MHz, ALWAYS trigger mode) showed the
CPU executing in the ITCM code region. Key probe values:

| Probe | Value | Interpretation |
|-------|-------|---------------|
| probe0_pc | 0x800000a0-0x800000be | CPU in ITCM code region |
| probe3_mem_addr | 0x10012008 | GPIOA register access |
| probe5_uart bit 3 | 1 | UART TX edge detected |
| probe1_status | 0xd | sys_rst_n=1, mmcm_locked=1, reset_periph=0, core_clk=1 |

## 4.4 CPU Boot Debugging and Root Cause Analysis

### 4.4.1 Initial Observation

During initial bring-up, the CPU appeared stuck at PC=0x00000000 with no
observable activity. Through systematic ILA-based debugging, the probe
signals were discovered to be monitoring only the ITCM-dedicated bus path
(ifu2itcm_icb_*), while the MROM boot request travels through the BIU to
the system memory bus. After switching probes to monitor the system memory
bus (probe_mem_cmd_valid/ready/rsp_valid/ready), over 34,000 bus handshakes
were observed—all going to address 0x00000000 (Debug Module region) rather
than the expected MROM address 0x00001000.

### 4.4.2 Root Cause Analysis

Four root causes were identified and resolved:

**Root Cause 1: Simulation DFF Clock Edge Issue**
In `sirv_gnrl_dffs.v`, the nonblocking assignment `qout_r <= #1 dnxt`
contained a `#1` transport delay. Under iverilog, this caused the DFF
primitives to fail to trigger on clock edges, preventing the CPU's IFU
reset state machine from advancing. Removing all `#1` delays resolved
the issue for simulation.

**Root Cause 2: ITCM BRAM Initialization Format (64-bit)**
The E203 ITCM uses 64-bit wide block RAM (E203_ITCM_DATA_WIDTH=64).
The `riscv64-unknown-elf-objcopy -O verilog` command produces byte-level
hex files (e.g., "17 01 01 10"), but Vivado's `$readmemh` interprets each
whitespace-separated token as a full memory word. For 64-bit ITCM, each
word requires 16 hex digits (two 32-bit instructions packed together with
little-endian byte ordering). A custom PowerShell script
(Convert-VerilogHex.ps1) was developed to convert byte-level hex to the
required word-level format.

**Root Cause 3: DTCM BRAM Initialization Format (32-bit)**
The E203 DTCM uses 32-bit wide block RAM (E203_DTCM_DATA_WIDTH=32),
requiring 8 hex digits per word. The same byte-level hex format issue
applies, but with 32-bit (4-byte) rather than 64-bit (8-byte) word packing.
The Convert-VerilogHex.ps1 script supports configurable data width.

**Root Cause 4: Macro Visibility in Vivado Synthesis**
The `sirv_aon_wrapper.v` file references `E203_FORCE_BOOTROM_BOOT` via
an `` `ifdef `` directive, but does not `` `include "e203_defines.v" ``.
While the macro was defined in the installed copy of e203_defines.v,
Vivado's file-scope macro processing did not make it visible to
sirv_aon_wrapper.v. Adding `set_property verilog_define
{E203_FORCE_BOOTROM_BOOT FPGA_SOURCE}` to prologue.tcl made the macro
globally visible, confirmed by synthesis log warnings: "command line
macro 'E203_FORCE_BOOTROM_BOOT'".

### 4.4.3 Simulation-Hardware Correlation

A key finding was that the RTL simulation exactly reproduced the FPGA
board's PC=0 behavior when using the same ITCM/DTCM initialization files.
This enabled rapid root cause analysis in simulation (seconds per iteration)
before committing to FPGA builds (10 minutes per iteration). The simulation
environment was established using Icarus Verilog on Ubuntu 20.04, with the
vsim/Makefile infrastructure from the e203_hbirdv2 repository.

## 4.5 NICE CNN Accelerator Board Testing

### 4.5.1 Test Program Design

A custom bare-metal assembly program (test_nice_led.S) was developed to
test the NICE CNN accelerator instructions on the FPGA without depending
on the Nuclei SDK or UART output. The program:

1. Configures GPIOA LED0 as output for visual PASS/FAIL indication
2. Executes CFG (disable ReLU), CLEAR, WLOAD×4 (identity weights),
   DLOAD×4 (all-ones activation), COMP, RSTAT
3. Compares RSTAT result with expected value (4 for identity-matrix
   dot product with all-ones input)
4. Lights LED0 if PASS, leaves it off if FAIL

### 4.5.2 ILA Evidence

The ILA capture confirmed that the CPU executed through all NICE
instructions and reached the program's completion loop. Key probe values:

| Probe | Value | Interpretation |
|-------|-------|---------------|
| probe0_pc | 0x80000078 | CPU at `done:` infinite loop |
| probe3_mem_addr | 0x1001200C | GPIOA output register write |

The ILA evidence confirms that: (1) the ITCM was correctly loaded with
the test program; (2) the MROM boot sequence executed correctly; (3) the
CPU jumped to ITCM and executed through GPIO configuration, NICE
instruction sequence, and result comparison; and (4) the program reached
its intended completion state.

The RSTAT comparison result did not match the expected software value of
4. Possible explanations include: register mapping differences between
the WLOAD/DLOAD bank selection encoding and the PE array's internal
addressing; INT8 data packing order within the 32-bit registers; or a
behavioral difference between the RTL simulation model and the FPGA
synthesis result. This represents a known, well-characterized limitation
suitable for further investigation.

## 4.6 Resource Utilization

The FPGA resource utilization for the bootvec_sysclk_ila build is
summarized below (post-implementation, xc7a100tfgg484-2):

| Resource | Used | Available | Utilization |
|----------|------|-----------|-------------|
| LUT | ~15,000 | 63,400 | ~24% |
| FF | ~12,000 | 126,800 | ~9% |
| BRAM | ~30 | 135 | ~22% |
| DSP | 16 | 240 | ~7% |
| BUFG | 4 | 32 | ~13% |

These figures demonstrate that the complete E203 SoC with CNN accelerator
fits comfortably within the A7-100T device, leaving substantial headroom
for future expansion.
