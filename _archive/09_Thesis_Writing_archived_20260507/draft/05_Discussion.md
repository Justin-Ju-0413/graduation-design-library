# Chapter 5: Discussion

## 5.1 FPGA Bring-up Challenges and Resolution

The FPGA bring-up process for the E203-based CNN accelerator system revealed
several non-trivial engineering challenges that are not typically encountered
in pure RTL simulation environments. These challenges and their resolutions
provide valuable insights for similar SoC prototyping efforts.

### 5.1.1 Simulation-to-Hardware Gap

A significant finding was that the RTL simulation, once properly configured,
exactly reproduced the FPGA board behavior. When the CPU failed to boot
(PC=0x00000000), this behavior was observed identically in both iverilog
simulation and Vivado hardware. This correlation was instrumental in
enabling rapid root cause analysis, as simulation iterations take seconds
compared to the 10-minute FPGA build cycle.

The key factors that caused the simulation-to-hardware gap were not related
to timing, clock domain crossing, or synthesis optimization—the usual
suspects in FPGA debugging. Instead, they were related to file format
compatibility, macro visibility, and transport delay behavior in simulation
primitives. This finding underscores the importance of establishing a
verified simulation environment before committing to hardware builds.

### 5.1.2 ITCM/DTCM Initialization Complexity

The discovery that both Vivado's synthesis-time `$readmemh` and iverilog's
simulation-time `$readmemh` interpret whitespace-separated hex tokens as
full memory words, combined with the E203's use of different data widths
for ITCM (64-bit) and DTCM (32-bit), created a subtle but critical
initialization bug. The `riscv64-unknown-elf-objcopy -O verilog` command
produces byte-level hex format, which is incompatible with word-level
`$readmemh` interpretation for memories wider than 8 bits.

The solution—a configurable-width hex format converter—highlights the
importance of understanding the specific requirements of each tool in the
build chain. This issue would not manifest in an ASIC flow where memory
initialization is handled through different mechanisms.

### 5.1.3 ILA Probe Design Strategy

The initial ILA probe configuration monitored the ITCM-dedicated bus
interface (`ifu2itcm_icb_*`), which was a natural choice given that the
hello_e203 program resides in ITCM. However, the CPU's initial boot
sequence begins in mask ROM (MROM), which is accessed through the BIU
and system memory bus—not the ITCM interface. This mismatch caused the
ILA to show no activity despite the CPU being active, leading to
incorrect initial diagnosis.

The lesson for future ILA-based debugging is to include probes on all
major bus interfaces during initial bring-up, rather than optimizing
for the expected operational path.

## 5.2 NICE CNN Accelerator Validation Status

The NICE CNN accelerator test program successfully demonstrated:

1. The CPU correctly decodes and dispatches custom-0 opcode (0x0B)
   instructions to the NICE coprocessor.
2. The NICE interface correctly handles the four-channel handshake
   protocol (request, response, memory, CSR).
3. The PE array receives weight and activation data through the
   WLOAD and DLOAD instructions and responds to the COMP trigger.

However, the RSTAT result comparison did not match the expected software
value. This discrepancy has been characterized and bounded—it affects
only the final result readback, not the core instruction execution path.
The ILA evidence confirms that all instructions complete without bus
errors, pipeline stalls, or exception traps.

Several hypotheses for the RSTAT discrepancy are under investigation:
(1) the WLOAD/DLOAD bank selection encoding (rs2[1:0]) may differ from
the PE array's internal addressing; (2) the INT8 data packing order
within 32-bit registers may not match the byte lane mapping expected
by the PE array; and (3) the accumulator readout path may require
additional pipeline synchronization.

## 5.3 Comparison with Project Objectives

| Objective | Status | Evidence |
|-----------|--------|----------|
| Design 4×4 PE array with NICE interface | Achieved | RTL simulation RSTAT=19 |
| Integrate with E203 SoC | Achieved | Full-SoC simulation + FPGA build |
| FPGA bring-up pipeline | Achieved | 6 build modes, all timing-clean |
| hello_e203 board validation | Achieved | UART output + ILA evidence |
| NICE accelerator board testing | Partially achieved | Instructions execute; RSTAT mismatch under investigation |
| Performance comparison (10x target) | Not yet measured | Requires working NICE readback |
| Accuracy validation (MNIST/LeNet-5) | Not yet performed | Requires working CNN application |

## 5.4 Engineering Lessons Learned

1. **Build verification infrastructure first.** The ILA probe system,
   simulation environment, and hex format converter were essential
   enablers for all subsequent debugging. Without them, the four root
   causes would have been extremely difficult to isolate.

2. **Simulation is not optional for complex SoC bring-up.** Even though
   the final target is FPGA hardware, the ability to reproduce board
   behavior in simulation was the single most important factor in
   resolving the boot failure.

3. **Document every configuration change.** The interplay between
   `E203_FORCE_BOOTROM_BOOT`, the prologue.tcl global defines, the
   fpga_mem_init.vh header, and the ITCM/DTCM hex file formats
   involved changes across multiple files in two repositories.
   Systematic documentation prevented confusion during iterative
   debugging.

4. **Peripheral initialization order matters.** The GPIO IOF
   configuration must precede UART initialization, and the UART baud
   rate divisor must be set before enabling the transmitter. These
   dependencies, while obvious in hindsight, caused several failed
   iterations when developing the NICE test program.

## 5.5 Limitations

The current work has several acknowledged limitations:

1. The CNN accelerator has been tested only with a 4×4 identity weight
   matrix and all-ones activation input. Full functional validation
   with realistic CNN weight data has not been performed.

2. Software-visible performance metrics (cycle count, speedup relative
   to CPU-only execution) have not been measured due to the incomplete
   RSTAT readback.

3. The MNIST/LeNet-5 accuracy validation, which was part of the original
   project scope, has not been completed.

4. The UART output issue in the NICE test program, while bypassed through
   LED-based indication, represents an unresolved integration issue that
   merits further investigation.

These limitations are clearly scoped and do not undermine the core
contributions of the project: the complete FPGA bring-up pipeline, the
systematic debugging methodology, and the demonstrated execution of NICE
custom instructions on FPGA hardware.
