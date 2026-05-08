# Graduation Design Project - FPGA Bring-Up

## Repos
- Main: `C:\Users\16084\Documents\New project\riscv_cnn_accelerator` (branch `codex/a7-bringup-v2-main`)
- SoC: `C:\Users\16084\Documents\New project\e203_hbirdv2` (branch `codex/a7-bringup-v2-soc`)

## Key Paths
- Board src: `{SoC}/fpga/davinci_a7_100t/src/`
- Board script: `{SoC}/fpga/davinci_a7_100t/script/`
- Vivado: `D:\Xilinx\Vivado\2023.2\bin\vivado.bat`
- FPGA part: `xc7a100tfgg484-2`
- Evidence: `04_Experiments/Board_BringUp/2026-04-28_board_connection_check/`
- Plans: `08_Todo_And_Notes/2026-04-28_To_Final_Defense_Plan/`

## Active Plan Files
- Master: `MASTER_PLAN.md`
- Ten-Day: `TEN_DAY_CLOSURE_TASK_BOOK_2026_04_29.md`
- Five-Day: `FIVE_DAY_BOARD_BRINGUP_PLAN_2026_04_29.md`
- Weekly: `WEEKLY_CHECKLIST.md`

## Build Commands
```powershell
# Build bitstream
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Invoke-Vivado-Fpga.ps1 -BuildMode {mode} -Action bit

# Current modes: soc, soc_sysclk_ila, soc_bootdiag_sysclk_ila, hello_sysclk_ila, heartbeat, heartbeat_direct, heartbeat_mmcm_ledonly, heartbeat_mmcm_dualclk, heartbeat_mmcm_sysclk_ila

# Build hello_e203 image
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Build-HelloE203.ps1
```

## Thesis Build Pipeline (论文编译流水线)

论文源码在 `thesis_latex/`，修改 `.tex` 文件后运行编译脚本。

### 快速命令
```bash
cd thesis_latex

# 只编译 PDF
bash build.sh pdf

# 只生成 DOCX (Pandoc + 后处理)
bash build.sh docx

# 全部 (PDF + DOCX)
bash build.sh all
```

### 流水线步骤

```
修改 chapters/*.tex
       │
       ▼
  XeLaTeX + Biber ──→ main_final.pdf       (71页, 43引用)
       │
       ▼
  Pandoc LaTeX→DOCX ──→ .build/_pandoc_raw.docx   (嵌入图片, IEEE引用, Heading样式)
       │
       ▼
  python post_process_final.py ──→ FYP_FINAL.docx  (强制TNR字体, 1.5行距, 边距)
```

### 关键工具路径
- Pandoc: `/c/Users/16084/AppData/Local/Pandoc/pandoc`
- Python: `/c/Users/16084/AppData/Local/Programs/Python/Python313/python`
- 参考模板: `thesis_latex/.build/pandoc-reference.docx`
- 后处理脚本: `thesis_latex/.build/post_process_final.py`
- IEEE CSL: `thesis_latex/ieee.csl`
- 施工脚本: `thesis_latex/build.sh`

### 修改论文的正确方式
1. 编辑 `chapters/*.tex` (LaTeX 源文件)
2. 运行 `bash build.sh all`
3. 检查 `main_final.pdf` 和 `FYP_FINAL.docx`
4. 不要在 DOCX 里直接改内容 —— 一切以 `.tex` 为准

### DOCX 后处理保证
- 所有 run 字体 = Times New Roman
- H1=16pt Bold, H2=14pt Bold, H3=13pt Bold
- 正文 12pt, 参考文献 12pt
- 行距 1.5
- 页边距 上下 1.5in / 左右 1.0in
- Declaration/Abstract 官方文本

## Current Status (2026-05-08)

**论文**: PDF 74页 (3.5MB), DOCX 3.9MB, 44引用, 编译通过
**数据修复 (2026-05-08)**: 全部图表数据已替换为真实来源，零合成数据
**Figure 4.1** (hello_e203 ILA): 真实 CSV 数据 — hello_e203_board_artifacts PC/Status/MemAddr probe
**Figure 4.2** (CNN program entry): 真实 CSV 数据 — cnn_sysclk_ila PC/DataPtr/MemStatus probe; NICE CSR/HS 窗口缺失已如实标注
**Figure 4.4/4.5** (资源): 真实 Vivado utilization_placed.rpt 数据 — LUT 20.8%, FF 10.1%, BRAM 26.3%

### 图片产物管理

**Single Source of Truth**: `thesis_latex/figures/MANIFEST.md`

所有图片的元数据（Figure 编号、LaTeX label、Caption、来源脚本、生成命令、文件大小）统一在 MANIFEST.md 中维护。修改图片后必须同步更新 MANIFEST.md。

**编译注意事项**:
- 编译前关闭 WPS/PDF阅读器, 否则 xelatex 文件锁定失败
- 不要加 `\usepackage{microtype}` (MiKTeX 未安装会挂起)
- XeLaTeX 绝对路径: `/c/Users/16084/AppData/Local/Programs/MiKTeX/miktex/bin/x64/xelatex`

**FPGA 上板**: Day 1-4 DONE, Day 5+ TODO

## Skills Available
- `/new-ila-build` - Add a new ILA diagnostic FPGA build mode
- `/day-closeout` - Update daily status across tracking files
- `/board-evidence-archive` - Archive board run artifacts
