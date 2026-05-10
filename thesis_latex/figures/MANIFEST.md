# Thesis Figure Manifest

This file is the figure asset source of truth. Report figures are regenerated
from scripts and recorded project evidence; raw screenshots, UART logs, ILA CSV
captures, and Vivado reports remain in the evidence package.

## Regeneration

```powershell
cd C:\Users\16084\Documents\Graduation_Design_Library\thesis_latex
& C:\Users\16084\AppData\Local\Programs\Python\Python313\python.exe .build\gen_block_diagrams.py
& C:\Users\16084\AppData\Local\Programs\Python\Python313\python.exe .build\fix_figures.py
```

QA outputs:

- `thesis_latex/.build/figure_qa/all_figures_contact_sheet.png`
- `thesis_latex/.build/figure_qa/figure_data_provenance.json`

## Chapter 3 Figures

| Figure | File | LaTeX label | Source | Evidence boundary |
|---|---|---|---|---|
| Fig 3.1 SoC architecture | `fig3_1_soc_architecture.png` | `fig:3_1` | `.build/gen_block_diagrams.py` | Academic redraw of project architecture; not a measurement chart. |
| Fig 3.2 instruction format | `fig3_2_instruction_format.png` | `fig:3_2` | `.build/fix_figures.py` | Encodes the implemented custom0/NICE field interpretation. |
| Fig 3.2b instruction table | `fig3_2b_instruction_table.png` | `fig:3_2b` | `.build/fix_figures.py` | Instruction encodings are documented constants, not sampled data. |
| Fig 3.3 PE microarchitecture | `fig3_3_pe_microarchitecture.png` | `fig:3_3` | `.build/gen_block_diagrams.py` | Academic redraw of RTL datapath intent. |
| Fig 3.4 PE array | `fig3_4_pe_array.png` | `fig:3_4` | `.build/gen_block_diagrams.py` | Academic redraw of implemented 4x4 PE dataflow. |
| Fig 3.5 packed format | `fig3_5_packed_format.png` | `fig:3_5` | `.build/fix_figures.py` | Bit-packing diagram for WLOAD/DLOAD operands. |
| Fig 3.6 build pipeline | `fig3_6_build_pipeline.png` | `fig:3_6` | `.build/fix_figures.py` | Redrawn workflow; raw build logs remain in `04_Experiments/`. |
| Fig 3.7 verification chain | `fig3_7_verification_chain.png` | `fig:3_7` | `.build/fix_figures.py` | Redrawn evidence chain from RTL to board regression. |

## Chapter 4 Figures

| Figure | File | LaTeX label | Source | Evidence boundary |
|---|---|---|---|---|
| FPGA board photo | `fig4_1_fpga_board.jpg` | `fig:fpga_board` | Original photo | Visual hardware context only. |
| Fig 4.1 hello ILA | `fig4_2_ila_pc_trace.png` | `fig:4_1` | `.build/fix_figures.py` | Redrawn from `04_Experiments/Board_BringUp/2026-04-28_board_connection_check/hello_e203_board_artifacts/ila_capture.csv`. |
| Fig 4.2 CNN ILA | `fig4_3_ila_nice_activity.png` | `fig:4_2` | `.build/fix_figures.py` | Redrawn from `04_Experiments/Board_BringUp/2026-05-09_nice_rs2_fix_verification/ila_capture.csv`; sampled NICE window is stable idle, with pass/fail from UART. |
| Fig 4.4 CNN v1 UART | `fig4_4_uart_cnn_v1.png` | `fig:uart_output` | `.build/fix_figures.py` | Rendered from `04_Experiments/Board_BringUp/2026-05-09_nice_rs2_fix_verification/uart_output.txt`; proves CNN v1 reduced-convolution HW/SW/expected agreement and 5.282x speedup. |
| Fig 4.5 LeNet-5 UART | `fig4_5_uart_lenet5.png` | `fig:4_7` | `.build/fix_figures.py` | Rendered from the recorded LeNet-5 v8 board result: 10 MNIST test images classified correctly (10/10 = 100%). |
| Fig 4.6 speedup | `fig4_6_speedup_bar.png` | `fig:4_3` | `.build/fix_figures.py` | Uses UART cycle counts: CPU 1516 cycles, NICE 287 cycles, speedup 5.282x. |
| Fig 4.7 resource fit | `fig4_7_resource_pie.png` | `fig:4_4` | `.build/fix_figures.py` | Shows per-resource used/headroom bars using recorded Vivado utilization values. |
| Fig 4.8 utilization | `fig4_8_utilization_bar.png` | `fig:4_5` | `.build/fix_figures.py` | Shows the same recorded Vivado utilization percentages on a single percentage scale with a 30% reference. |
| Fig 4.9 timing | `fig4_9_timing.png` | `fig:4_6` | `.build/fix_figures.py` | Uses recorded timing values from Vivado reports/summaries; Table 4.3 must match the values in `figure_data_provenance.json`. |

## Data Values

Measured UART result:

| Metric | Value |
|---|---:|
| CPU reference cycles | 1516 |
| NICE accelerator cycles | 287 |
| Speedup | 5.282x |
| SW output | `12 23 0 19` |
| HW output | `12 23 0 19` |
| Expected output | `12 23 0 19` |

LeNet-5 UART result:

| Metric | Value |
|---|---:|
| Correct MNIST samples | 10 / 10 |
| Accuracy | 100% |
| Expected labels | `7 2 1 0 4 1 4 9 5 9` |
| Predicted labels | `7 2 1 0 4 1 4 9 5 9` |

Resource values:

| Resource | Used | Available | Utilization |
|---|---:|---:|---:|
| LUT | 13,188 | 63,400 | 20.8% |
| LUTRAM | 219 | 19,000 | 1.2% |
| FF | 12,752 | 126,800 | 10.1% |
| BRAM | 35.5 | 135 | 26.3% |
| DSP | 0 | 240 | 0.0% |
| BUFG | 5 | 32 | 15.6% |

Timing values:

| Build | WNS (ns) | WHS (ns) |
|---|---:|---:|
| heartbeat_mmcm_sysclk_ila | 13.887 | 0.058 |
| soc_sysclk_ila | 13.515 | 0.058 |
| soc_bootdiag_sysclk_ila | 13.337 | 0.039 |
| bootvec_sysclk_ila | 13.677 | 0.061 |
| hello_sysclk_ila | 14.204 | 0.060 |
| cnn_sysclk_ila | 12.472 | 0.057 |

## Rules

- Do not manually edit generated PNGs.
- Do not hand-edit ILA CSV, UART log, or Vivado report values.
- If evidence changes, update the source evidence path or constants in the
  generation scripts, regenerate figures, and re-run visual/PDF QA.
