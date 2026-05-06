# Thesis Figures Inventory

Generated: 2026-05-04
Scope: All files under `04_Experiments/` and `05_Presentation/` that can serve as thesis figures or data sources.

---

## 1. Screenshots (PNG) -- Thesis-Ready

| # | File | Description | Thesis Chapter | Needs Processing |
|---|------|-------------|----------------|-----------------|
| 1 | `05_Presentation/Screenshots/2026-04-14_fullsoc_rstat19_phase4pass.png` | Full SoC simulation pass (iverilog rstat19 phase 4) | Ch.4 RTL Simulation | No |
| 2 | `05_Presentation/Screenshots/2026-04-14_local_rtl_tb_pass.png` | Local RTL testbench pass | Ch.4 RTL Simulation | No |
| 3 | `05_Presentation/Assets/cityu_logo.png` | CityU logo | Cover/Title page | No |

## 2. ILA Capture CSV Data -- Needs Charting

Each CSV contains 1024-sample waveform data from Vivado ILA. Must be converted to waveform plots or tables.

| # | File | Design Mode | Probes | Thesis Chapter | Needs Processing |
|---|------|------------|--------|----------------|-----------------|
| 1 | `Board_BringUp/.../bootvec_sysclk_ila_ila_capture/ila_capture.csv` | bootvec_sysclk_ila | pc, status, membus_live, mem_addr, membus_counts, uart, flags | Ch.5 Boot Vector Debug | CSV -> waveform plot |
| 2 | `Board_BringUp/.../cnn_sysclk_ila_ila_capture/ila_capture.csv` | cnn_sysclk_ila | pc, reset_uart, liveness, pc_activity, nice_csr, nice_hs, mem_status | Ch.6 CNN/NICE Validation | CSV -> waveform plot |
| 3 | `Board_BringUp/.../heartbeat_direct_ila_capture/ila_capture.csv` | heartbeat_direct | counter, reset, inputs, zero, zero, jtag, status | Ch.5 Clock/Reset Debug | CSV -> waveform plot |
| 4 | `Board_BringUp/.../heartbeat_mmcm_sysclk_ila_ila_capture/ila_capture.csv` | heartbeat_mmcm_sysclk_ila | sysclk_counter, reset, inputs, clk16_edges, zero, jtag, status | Ch.5 MMCM/Reset Debug | CSV -> waveform plot |
| 5 | `Board_BringUp/.../hello_e203_board_artifacts/ila_capture.csv` | bootvec_sysclk_ila (hello_e203 run) | pc, status, membus_live, mem_addr, membus_counts, uart, flags | Ch.5 hello_e203 Validation | CSV -> waveform plot |
| 6 | `Board_BringUp/.../hello_sysclk_ila_ila_capture/ila_capture.csv` | hello_sysclk_ila | pc, reset_uart, liveness, pc_activity, nice_csr, nice_hs, mem_status | Ch.5 hello_e203 Attempt | CSV -> waveform plot |
| 7 | `Board_BringUp/.../ila_capture/ila_capture.csv` | Original (MMCM-clocked, corrupted) | csr_flags, mem_bus, nice_csr_addr, nice_csr_wdata, nice_hs, pc, status | Ch.5 Initial Debug | CSV (illustrates corruption) |
| 8 | `Board_BringUp/.../soc_bootdiag_sysclk_ila_ila_capture/ila_capture.csv` | soc_bootdiag_sysclk_ila | pc, reset_uart, liveness, pc_activity, nice_csr, nice_hs, mem_status | Ch.5 Boot Diagnostic | CSV -> waveform plot |
| 9 | `Board_BringUp/.../soc_sysclk_ila_ila_capture/ila_capture.csv` | soc_sysclk_ila | pc, reset_uart, liveness, pc_activity, nice_csr, nice_hs, mem_status | Ch.5 SoC ILA Diagnostic | CSV -> waveform plot |

## 3. UART Output (TXT) -- Thesis-Ready

| # | File | Content | Thesis Chapter | Needs Processing |
|---|------|---------|----------------|-----------------|
| 1 | `Board_BringUp/.../hello_e203_board_artifacts/uart_output.txt` | `hello_e203: boot` / `uart ok` / `loop` | Ch.5 hello_e203 Validation | No (direct text) |

## 4. Conclusion / Closure Summaries (TXT/MD) -- Source for Results Tables

| # | File | Content | Thesis Chapter | Needs Processing |
|---|------|---------|----------------|-----------------|
| 1 | `Board_BringUp/.../hello_e203_board_artifacts/conclusion.txt` | 4 root causes, PC/GPIOA/UART evidence | Ch.5 Closure Summary | Extract key rows |
| 2 | `Board_BringUp/.../DAY3_4_HELLO_E203_CLOSURE_SUMMARY.md` | Full Day 3-4 closure: root cause table, UART evidence, ILA probe table | Ch.5 | Extract root cause table |
| 3 | `Board_BringUp/.../BOARD_RUNTIME_EVIDENCE_2026_04_28.md` | Chronological evidence log from Day 1 through Day 4 | Ch.5 (chronological reference) | Extract key milestones |
| 4 | `Board_BringUp/.../STATUS.md` | Complete status log with all debug iterations | Ch.5 (appendix or reference) | Extract key milestones |

## 5. Timing Summary Reports (.rpt) -- Data Source for Tables

Each `.rpt` contains Vivado timing summary. Extract WNS, WHS, and constraint status.

| # | File | Build Mode | Thesis Chapter | Needs Processing |
|---|------|-----------|---------------|-----------------|
| 1 | `Board_BringUp/.../heartbeat_direct_artifacts/heartbeat_direct_timing_summary_routed.rpt` | heartbeat_direct | Ch.4 Timing Closure | Extract WNS/WHS |
| 2 | `Board_BringUp/.../heartbeat_mmcm_dualclk_artifacts/heartbeat_mmcm_dualclk_timing_summary_routed.rpt` | heartbeat_mmcm_dualclk | Ch.4 Timing Closure | Extract WNS/WHS |
| 3 | `Board_BringUp/.../heartbeat_mmcm_ledonly_artifacts/heartbeat_mmcm_ledonly_timing_summary_routed.rpt` | heartbeat_mmcm_ledonly | Ch.4 Timing Closure | Extract WNS/WHS |
| 4 | `Board_BringUp/.../heartbeat_mmcm_sysclk_ila_artifacts/heartbeat_mmcm_sysclk_ila_timing_summary_routed.rpt` | heartbeat_mmcm_sysclk_ila | Ch.4 Timing Closure | Extract WNS/WHS |
| 5 | `Board_BringUp/.../hello_sysclk_ila_artifacts/hello_sysclk_ila_timing_summary_routed.rpt` | hello_sysclk_ila | Ch.4 Timing Closure | Extract WNS/WHS |
| 6 | `Board_BringUp/.../soc_bootdiag_sysclk_ila_artifacts/soc_bootdiag_sysclk_ila_timing_summary_routed.rpt` | soc_bootdiag_sysclk_ila | Ch.4 Timing Closure | Extract WNS/WHS |
| 7 | `Board_BringUp/.../soc_sysclk_ila_artifacts/soc_sysclk_ila_timing_summary_routed.rpt` | soc_sysclk_ila | Ch.4 Timing Closure | Extract WNS/WHS |

**Quick-reference WNS/WHS extracted from reports & summaries:**

| Build Mode | WNS | WHS |
|-----------|-----|-----|
| bootvec_sysclk_ila | 13.677 ns | 0.061 ns |
| soc_sysclk_ila | 13.515 ns | 0.058 ns |
| soc_bootdiag_sysclk_ila | 13.337 ns | 0.039 ns |
| hello_sysclk_ila | 14.204 ns | 0.060 ns |
| heartbeat_mmcm_sysclk_ila | 13.887 ns | -- |
| heartbeat_mmcm_dualclk | 27.913 ns | -- |
| heartbeat_mmcm_ledonly | 60.386 ns | -- |
| heartbeat_direct | Positive (exact value in .rpt) | -- |

## 6. Route Status Reports (.rpt) -- Data for Utilization Tables

| # | File | Thesis Chapter | Needs Processing |
|---|------|---------------|-----------------|
| 1 | `Board_BringUp/.../heartbeat_direct_artifacts/heartbeat_direct_route_status.rpt` | Ch.4 Utilization | Extract LUT/FF/BRAM |
| 2 | `Board_BringUp/.../heartbeat_mmcm_dualclk_artifacts/heartbeat_mmcm_dualclk_route_status.rpt` | Ch.4 Utilization | Extract LUT/FF/BRAM |
| 3 | `Board_BringUp/.../heartbeat_mmcm_ledonly_artifacts/heartbeat_mmcm_ledonly_route_status.rpt` | Ch.4 Utilization | Extract LUT/FF/BRAM |
| 4 | `Board_BringUp/.../heartbeat_mmcm_sysclk_ila_artifacts/heartbeat_mmcm_sysclk_ila_route_status.rpt` | Ch.4 Utilization | Extract LUT/FF/BRAM |
| 5 | `Board_BringUp/.../hello_sysclk_ila_artifacts/hello_sysclk_ila_route_status.rpt` | Ch.4 Utilization | Extract LUT/FF/BRAM |
| 6 | `Board_BringUp/.../soc_bootdiag_sysclk_ila_artifacts/soc_bootdiag_sysclk_ila_route_status.rpt` | Ch.4 Utilization | Extract LUT/FF/BRAM |
| 7 | `Board_BringUp/.../soc_sysclk_ila_artifacts/soc_sysclk_ila_route_status.rpt` | Ch.4 Utilization | Extract LUT/FF/BRAM |

## 7. Build Summary Files (TXT) -- Data for Build Flow

| # | File | Thesis Chapter | Needs Processing |
|---|------|---------------|-----------------|
| 1 | `Board_BringUp/.../hello_sysclk_ila_artifacts/build_summary.txt` | Ch.4 Build Flow | No (text) |
| 2 | `Board_BringUp/.../soc_bootdiag_sysclk_ila_artifacts/build_summary.txt` | Ch.4 Build Flow | No (text) |

## 8. Software Build Artifacts -- hello_e203 Toolchain Output

| # | File | Description | Thesis Chapter | Needs Processing |
|---|------|-------------|----------------|-----------------|
| 1 | `Board_BringUp/.../hello_sysclk_ila_artifacts/hello_e203.elf` | ELF binary | Ch.4 SW Build | Binary, extract _start address |
| 2 | `Board_BringUp/.../hello_sysclk_ila_artifacts/hello_e203.dump` | Disassembly dump | Ch.4 SW Build | Extract entry point |
| 3 | `Board_BringUp/.../hello_sysclk_ila_artifacts/hello_e203.map` | Linker map | Ch.4 SW Build | Extract memory layout |
| 4 | `Board_BringUp/.../hello_sysclk_ila_artifacts/hello_e203.verilog` | Verilog hex dump | Ch.4 SW Build | No |
| 5 | `Board_BringUp/.../hello_sysclk_ila_artifacts/hello_e203.itcm.verilog` | ITCM init hex | Ch.4 Memory Init | No |
| 6 | `Board_BringUp/.../hello_sysclk_ila_artifacts/hello_e203.dtcm.verilog` | DTCM init hex | Ch.4 Memory Init | No |

## 9. XDC Constraint Files -- Source for Constraint Strategy

| # | File | Thesis Chapter | Needs Processing |
|---|------|---------------|-----------------|
| 1 | `Board_BringUp/.../hello_sysclk_ila_artifacts/hello_sysclk_ila.xdc` | Ch.4 Timing Constraints | No (direct text) |
| 2 | `Board_BringUp/.../soc_bootdiag_sysclk_ila_artifacts/soc_bootdiag_sysclk_ila.xdc` | Ch.4 Timing Constraints | No (direct text) |

## 10. ILA Summary Files (TXT) -- Probe Configuration Reference

These show which probes were configured, their widths, and capture status.

| # | File | Build Mode | Chapter | Notes |
|---|------|-----------|---------|-------|
| 1 | `bootvec_sysclk_ila_ila_capture/ila_summary.txt` | bootvec_sysclk_ila | Ch.5 | 7 probes, CAPTURED |
| 2 | `cnn_sysclk_ila_ila_capture/ila_summary.txt` | cnn_sysclk_ila | Ch.6 | 7 probes, CAPTURED |
| 3 | `heartbeat_direct_ila_capture/ila_summary.txt` | heartbeat_direct | Ch.5 | 7 probes, CAPTURED |
| 4 | `heartbeat_ila_capture/ila_summary.txt` | heartbeat (original) | Ch.5 | ILA UPLOAD_FAILED |
| 5 | `heartbeat_mmcm_dualclk_ila_capture/ila_summary.txt` | heartbeat_mmcm_dualclk | Ch.5 | ILA UPLOAD_FAILED |
| 6 | `heartbeat_mmcm_sysclk_ila_ila_capture/ila_summary.txt` | heartbeat_mmcm_sysclk_ila | Ch.5 | 7 probes, CAPTURED |
| 7 | `hello_e203_board_artifacts/ila_summary.txt` | bootvec_sysclk_ila | Ch.5 | 7 probes, CAPTURED |
| 8 | `hello_sysclk_ila_ila_capture/ila_summary.txt` | hello_sysclk_ila | Ch.5 | 7 probes, CAPTURED |
| 9 | `ila_capture/ila_summary.txt` | Original SoC | Ch.5 | ILA UPLOAD_FAILED (corrupted) |
| 10 | `soc_bootdiag_sysclk_ila_ila_capture/ila_summary.txt` | soc_bootdiag_sysclk_ila | Ch.5 | 7 probes, CAPTURED |
| 11 | `soc_sysclk_ila_ila_capture/ila_summary.txt` | soc_sysclk_ila | Ch.5 | 7 probes, CAPTURED |

## 11. Analysis Scripts (Python)

| # | File | Thesis Chapter | Needs Processing |
|---|------|---------------|-----------------|
| 1 | `Board_BringUp/.../hello_sysclk_ila_ila_capture/analyze_hello_sysclk_ila.py` | Ch.5 | Script (not figure) |
| 2 | `Board_BringUp/.../soc_bootdiag_sysclk_ila_ila_capture/analyze_soc_bootdiag.py` | Ch.5 | Script (not figure) |

## 12. Presentation Files (PPTX/DOCX) -- Existing Figures Source

These may contain block diagrams, architecture drawings, or results tables reusable in the thesis.

| # | File | Type | Notes |
|---|------|------|-------|
| 1 | `05_Presentation/Archive/.../Tuesday_4Week_Report_2026-04-14.pptx` | PPTX | 4-week report slides (may have system diagram) |
| 2 | `05_Presentation/Archive/.../Tuesday_4Week_Report_2026-04-14_CityU_Final_With_Notes.pptx` | PPTX | Final version with speaker notes |
| 3 | `05_Presentation/Archive/.../Tuesday_4Week_Report_2026-04-14_CityU_Styled.pptx` | PPTX | CityU-styled version |
| 4 | `05_Presentation/Archive/Slides/Tuesday_4Week_Report_2026-04-14_CityU_Humanized.pptx` | PPTX | Humanized version |
| 5 | `05_Presentation/Archive/Tuesday_4Week_Report_Final.pptx` | PPTX | Final version |
| 6 | `05_Presentation/Final/Tuesday_4Week_Report_Final_CN_Fixed.pptx` | PPTX | Chinese-fixed final |
| 7 | `05_Presentation/Archive/Tuesday_4Week_Report_Bilingual_Script.docx` | DOCX | Bilingual script |
| 8 | `05_Presentation/Archive/Tuesday_4Week_Report_Explanation.docx` | DOCX | Explanation doc |
| 9 | `05_Presentation/Archive/Tuesday_4Week_Report_Explanation_CN.docx` | DOCX | Chinese explanation |
| 10 | `05_Presentation/QA/Tuesday_4Week_Report_QA_Bilingual_Practical.docx` | DOCX | QA doc |

## 13. Bitstream & Probes Files (Binary -- Not Directly Usable)

These are listed for completeness but are binary FPGA files, not thesis figures.

- `*_artifacts/*.bit` (bitstream) -- 8 files across all build modes
- `*_artifacts/*.ltx` (debug probes) -- 8 files across all build modes

## 14. Build Logs (Runme Logs)

Implementation logs from Vivado -- may contain utilization/timing data as secondary source.

- `heartbeat_direct_artifacts/heartbeat_direct_impl_runme.log`
- `heartbeat_mmcm_dualclk_artifacts/heartbeat_mmcm_dualclk_impl_runme.log`
- `heartbeat_mmcm_ledonly_artifacts/heartbeat_mmcm_ledonly_impl_runme.log`
- `heartbeat_mmcm_sysclk_ila_artifacts/heartbeat_mmcm_sysclk_ila_impl_runme.log`
- `hello_sysclk_ila_artifacts/hello_sysclk_ila_impl_runme.log`
- `soc_bootdiag_sysclk_ila_artifacts/soc_bootdiag_sysclk_ila_impl_runme.log`
- `soc_sysclk_ila_artifacts/soc_sysclk_ila_impl_runme.log`

## 15. Simulation Evidence (RTL / FullSoC)

| # | File | Thesis Chapter | Notes |
|---|------|---------------|-------|
| 1 | `04_Experiments/RTL_Simulation/2026-04-23_baseline_rerun/README.md` | Ch.4 | Placeholder -- no actual sim artifacts captured |
| 2 | `04_Experiments/FullSoC_Simulation/2026-04-23_baseline_rerun/README.md` | Ch.4 | Placeholder -- no actual sim artifacts captured |

Note: RTL simulation evidence (iverilog waveforms, VCD dumps) is not stored under the Library archive. Simulation is run on Ubuntu VM (`ubuntu-sim` skill). Screenshots of simulation passes are in `05_Presentation/Screenshots/`.

---

## Summary by Thesis Chapter

### Ch.2 Background
- No direct evidence files (architecture diagrams may exist in repo source code)

### Ch.3 System Architecture
- No direct evidence files. Architecture block diagrams may exist in:
  - Presentation PPTX slides (Ch.3 should be drawn from design source)
  - RTL source code comments
  - `08_Todo_And_Notes/` planning documents

### Ch.4 Implementation (RTL Design, Build Flow, Timing Closure)
- **3 screenshots**: 2 sim passes, 1 logo
- **7 timing reports** (.rpt) -- WNS range: 13.3 - 60.4 ns
- **7 route status reports** (.rpt) -- resource utilization data
- **7 build logs** -- implementation log
- **2 build summaries** (TXT)
- **2 XDC constraint files**
- **6 software build artifacts** (ELF, dump, map, verilog hex)
- **2 simulation README placeholders** (actual sim artifacts elsewhere)

### Ch.5 FPGA Bring-up and Validation
- **9 ILA capture CSVs** -- most critical data, need waveform charting
- **11 ILA summary TXT** -- probe configurations and capture status
- **1 UART output TXT** -- thesis-ready text
- **1 closure conclusion TXT**
- **3 evidence MD documents** (chronological debug journey)
- **2 Python analysis scripts**
- **1 timing summary TXT** (quick-reference WNS)

### Ch.6 CNN Accelerator Validation
- **1 ILA capture CSV** (`cnn_sysclk_ila`) with NICE handshake probes
- **1 ILA summary TXT**

### Ch.7 Conclusion / Defense Presentation
- **10+ PPTX/DOCX presentation files**
- Various QA and script docs

## Critical Gaps

1. **No PNG screenshots of ILA waveforms.** All ILA probe data exists as raw CSV, requiring Vivado or Python-based waveform plotting to convert for thesis use.
2. **No FPGA board photos.** Consider taking a photo of the Davinci Pro A7-100T board with LED evidence visible.
3. **No resource utilization summary table.** Need to extract LUT/FF/BRAM/DSP from each `route_status.rpt` and compile.
4. **No architecture block diagram.** The system-level diagram (CPU + CNN accelerator + bus fabric) needs to be drawn from the RTL source.
5. **No simulation waveform screenshots** stored in the Library. The two existing PNGs are terminal-output pass/fail screenshots, not waveform views.

---

*All paths above are relative to `C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\` for experiment files, or `05_Presentation\` for presentation files, unless otherwise noted.*
