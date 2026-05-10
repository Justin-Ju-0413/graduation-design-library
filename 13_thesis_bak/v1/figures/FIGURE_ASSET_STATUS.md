# Figure Asset Status

All thesis figures are maintained as report-ready English assets. Raw evidence remains in `04_Experiments/` and is indexed in `10_Final_Defense/Evidence_Package/EVIDENCE_INDEX.md`.

| Figure | Use | Current treatment | Evidence/source |
|---|---|---|---|
| Fig 3.1 SoC architecture | Thesis + PPT | Redrawn academic block diagram | `thesis_latex/.build/gen_block_diagrams.py` |
| Fig 3.2 instruction format | Thesis | Redrawn bit-field diagram | `thesis_latex/.build/fix_figures.py` |
| Fig 3.2b instruction table | Thesis + PPT | Redrawn readable table | `thesis_latex/.build/fix_figures.py` |
| Fig 3.3 PE microarchitecture | Thesis | Redrawn academic block diagram | `thesis_latex/.build/gen_block_diagrams.py` |
| Fig 3.4 PE array | Thesis + PPT | Redrawn academic block diagram | `thesis_latex/.build/gen_block_diagrams.py` |
| Fig 3.5 packed format | Thesis | Existing readable figure retained | Manual asset |
| Fig 3.6 build pipeline | Thesis + PPT | Redrawn pipeline | `thesis_latex/.build/fix_figures.py` |
| Fig 3.7 verification chain | Thesis + PPT | Redrawn evidence chain | `thesis_latex/.build/fix_figures.py` |
| Fig 4.1 hello ILA | Thesis + PPT | CSV-redrawn evidence chart | `04_Experiments/.../hello_e203_board_artifacts/ila_capture.csv` |
| Fig 4.2 CNN ILA | Thesis | CSV-redrawn evidence chart | `04_Experiments/.../2026-05-09_nice_rs2_fix_verification/ila_capture.csv` |
| UART output | Thesis + PPT | Redrawn terminal summary | `04_Experiments/.../2026-05-09_nice_rs2_fix_verification/uart_output.txt` |
| Fig 4.3 speedup | Thesis + PPT | Redrawn measured bar chart | `uart_output.txt`: 1516 vs 287 cycles |
| Fig 4.4 resource fit | Thesis | Redrawn used/headroom capacity chart | recorded Vivado utilization values |
| Fig 4.5 utilization | Thesis | Redrawn horizontal utilization chart | recorded Vivado utilization values |
| Fig 4.6 timing | Thesis | Redrawn timing chart | recorded Vivado timing values |
| FPGA board photo | Thesis | Original photo retained | `fig4_1_fpga_board.jpg` |

## Regeneration

```powershell
cd C:\Users\16084\Documents\Graduation_Design_Library\thesis_latex
& C:\Users\16084\AppData\Local\Programs\Python\Python313\python.exe .build\gen_block_diagrams.py
& C:\Users\16084\AppData\Local\Programs\Python\Python313\python.exe .build\fix_figures.py
```
