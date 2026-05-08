# Figure Manifest — 产物清单（Single Source of Truth）

> 所有图片数据均来自真实实验。无合成数据。  
> 修改图片后必须更新此文件。

## Chapter 3 — Methodology

### Fig 3.1 — SoC Architecture
| 字段 | 值 |
|------|-----|
| **文件** | `fig3_1_soc_architecture.png` |
| **LaTeX label** | `fig:3_1` |
| **来源** | 用户手绘 (dark-mode), SVG: `3.1.svg` |
| **类型** | 手动制图 |
| **大小** | 124 KB |

### Fig 3.2 — Instruction Format
| 字段 | 值 |
|------|-----|
| **文件** | `fig3_2_instruction_format.png` |
| **LaTeX label** | `fig:3_2` |
| **来源** | `.build/fix_figures.py` → `gen_fig3_2()` (硬编码位域布局) |
| **类型** | 自动生成 |
| **大小** | 50 KB |

### Fig 3.2b — Instruction Table
| 字段 | 值 |
|------|-----|
| **文件** | `fig3_2b_instruction_table.png` |
| **LaTeX label** | `fig:3_2b` |
| **来源** | 用户手绘 |
| **类型** | 手动制图 |
| **大小** | 60 KB |

### Fig 3.3 — PE Microarchitecture
| 字段 | 值 |
|------|-----|
| **文件** | `fig3_3_pe_microarchitecture.png` |
| **LaTeX label** | `fig:3_3` |
| **来源** | 用户手绘 (dark-mode), SVG: `3.3.svg` |
| **类型** | 手动制图 |
| **大小** | 70 KB |

### Fig 3.4 — PE Array
| 字段 | 值 |
|------|-----|
| **文件** | `fig3_4_pe_array.png` |
| **LaTeX label** | `fig:3_4` |
| **来源** | `.build/gen_block_diagrams.py` |
| **类型** | 自动生成 |
| **大小** | 70 KB |

### Fig 3.5 — Packed Data Format
| 字段 | 值 |
|------|-----|
| **文件** | `fig3_5_packed_format.png` |
| **LaTeX label** | `fig:3_5` |
| **来源** | 用户手绘 (dark-mode) |
| **类型** | 手动制图 |
| **大小** | 891 KB |

### Fig 3.6 — Build Pipeline
| 字段 | 值 |
|------|-----|
| **文件** | `fig3_6_build_pipeline.png` |
| **LaTeX label** | `fig:3_6` |
| **来源** | Vivado 截图 |
| **类型** | 截图 |
| **大小** | 1.1 MB |

### Fig 3.7 — Verification Chain
| 字段 | 值 |
|------|-----|
| **文件** | `fig3_7_verification_chain.png` |
| **LaTeX label** | `fig:3_7` |
| **来源** | 截图 |
| **类型** | 截图 |
| **大小** | 878 KB |

---

## Chapter 4 — Results

### FPGA Board Photo (unnumbered)
| 字段 | 值 |
|------|-----|
| **文件** | `fig_fpga_board.jpg` |
| **LaTeX label** | `fig:fpga_board` |
| **来源** | 照片 |
| **类型** | 照片 |
| **大小** | 327 KB |

### Fig 4.1 — hello_e203 ILA PC Trace
| 字段 | 值 |
|------|-----|
| **文件** | `fig4_1_ila_pc_trace.png` |
| **LaTeX label** | `fig:4_1` |
| **数据源** | `04_Experiments/.../hello_e203_board_artifacts/ila_capture.csv` |
| **来源** | `.build/fix_figures.py` → `gen_ila_pc_trace()` |
| **Probes** | probe0_pc (6 unique ITCM addresses), probe1_status (0xc/0xd), probe3_mem_addr (GPIOA 0x10012008) |
| **真实性** | 100% 真实 Vivado ILA CSV 数据 |
| **最近修改** | 2026-05-08 — 全部替换为真实 CSV 数据 |

### Fig 4.2 — CNN Program CPU Activity
| 字段 | 值 |
|------|-----|
| **文件** | `fig4_2_ila_nice_activity.png` |
| **LaTeX label** | `fig:4_2` |
| **数据源** | `04_Experiments/.../cnn_sysclk_ila_ila_capture/ila_capture.csv` |
| **来源** | `.build/fix_figures.py` → `gen_ila_nice_activity()` |
| **Probes** | probe0_pc (6 unique CNN code addresses), probe3_pc_activity (memory ref counter), probe6_mem_status (bus active) |
| **已知局限** | NICE CSR 全程为 0，HS 全程为 4（ILA 未抓到 NICE 指令窗口）。Caption 如实说明。 |
| **真实性** | 100% 真实 Vivado ILA CSV 数据 |
| **最近修改** | 2026-05-08 — 全部替换为真实 CSV 数据 |

### UART Output (unnumbered)
| 字段 | 值 |
|------|-----|
| **文件** | `fig_uart_output.png` |
| **LaTeX label** | `fig:uart_output` |
| **来源** | PuTTY 截图 |
| **类型** | 截图 |
| **大小** | 43 KB |

### Fig 4.3 — Speedup Bar Chart
| 字段 | 值 |
|------|-----|
| **文件** | `fig4_3_speedup_bar.png` |
| **LaTeX label** | `fig:4_3` |
| **数据源** | 实验测量：CPU 1516 cycles, NICE 287 cycles, speedup 5.28x |
| **来源** | `.build/fix_figures.py` → `gen_speedup()` |
| **真实性** | 真实实验 cycle count |

### Fig 4.4 — Resource Pie Chart
| 字段 | 值 |
|------|-----|
| **文件** | `fig4_4_resource_pie.png` |
| **LaTeX label** | `fig:4_4` |
| **数据源** | Vivado `system_utilization_placed.rpt` (cnn_sysclk_ila, post-placement) |
| **数值** | LUTs: 13,209/63,400 (20.8%), Regs: 12,752/126,800 (10.1%), BRAM: 35.5/135 tiles (26.3%) |
| **来源** | `.build/fix_figures.py` → `gen_resource_pie()` |
| **真实性** | 100% Vivado 报告数据 |

### Fig 4.5 — Utilization Bar Chart
| 字段 | 值 |
|------|-----|
| **文件** | `fig4_5_utilization.png` |
| **LaTeX label** | `fig:4_5` |
| **数据源** | 同上 Vivado `system_utilization_placed.rpt` |
| **来源** | `.build/fix_figures.py` → `gen_utilization()` |
| **真实性** | 100% Vivado 报告数据 |

### Fig 4.6 — Timing Closure
| 字段 | 值 |
|------|-----|
| **文件** | `fig4_6_timing.png` |
| **LaTeX label** | `fig:4_6` |
| **数据源** | Vivado timing summary (各 build 的 WNS/WHS) |
| **来源** | `.build/fix_figures.py` → `gen_timing()` |
| **真实性** | 匹配 Table 4.3 真实时序数据 |

---

## 产物统计

| 类型 | 数量 | 说明 |
|------|------|------|
| 手动制图 | 4 | Fig 3.1, 3.2b, 3.3, 3.5 |
| 真实 ILA CSV | 2 | Fig 4.1, 4.2 |
| 真实 Vivado 数据 | 3 | Fig 4.4, 4.5, 4.6 |
| 真实实验数据 | 1 | Fig 4.3 |
| 位域布局 | 1 | Fig 3.2 |
| 截图 | 3 | Fig 3.6, 3.7, UART |
| 照片 | 1 | FPGA Board |
| **合计** | **16** | **100% 真实数据，无合成数据** |

## 生成命令

```bash
cd thesis_latex
python .build/fix_figures.py          # 全部 7 张自动生成图
python .build/gen_block_diagrams.py   # Fig 3.4
bash build.sh all                     # PDF + DOCX
```

## 修改规则

- 手动制图 → 改 SVG/PPT 源 → 重新导出 PNG → 更新本文件
- ILA CSV 数据 → 重新上板抓取 → 覆盖 CSV → `python .build/fix_figures.py` → 更新本文件
- Vivado 资源数据 → 重新跑 Vivado → 更新 RPT 路径 → `python .build/fix_figures.py` → 更新本文件
- **禁止：** 直接修改 PNG/JPG、手动编辑 CSV 数据、使用合成/随机数据
