# 论文 AI 图片生成提示词

> 使用 Nanobanana 或其他 AI 图片生成工具
> 生成后保存到：`Graduation_Design_Library\thesis_latex\figures\` 覆盖同名文件

---

## 图 1：系统架构框图 (fig3_1_soc_architecture.png)

```
A clean academic block diagram of a RISC-V SoC with CNN accelerator. White background, thin black rectangular borders, single accent color #2196F3 for the accelerator block.

LAYOUT (left to right):

LEFT COLUMN - "E203 RISC-V Core (RV32IMAC)":
- A large rounded rectangle containing two internal blocks stacked vertically:
  - "IFU (Instruction Fetch)"
  - "EXU (Execute + NICE Interface)"
- Below: "LSU / BIU (Load/Store + Bus)"

CENTER COLUMN - "CNN Accelerator":
- A large blue-accented (#E8F5E9 fill) rounded rectangle containing:
  - "NICE Decoder + Control FSM"
  - "4×4 PE Array (INT8 MAC, Output-Stationary)"

RIGHT COLUMN - Memory & Peripherals:
- Two vertically stacked blocks:
  - "ITCM 64KB (0x8000_0000, 64-bit width)"
  - "DTCM 64KB (0x9000_0000, 32-bit width)"
- Below, two small blocks side by side:
  - "UART0 (0x1001_3000)"  "GPIO"

BOTTOM: A wide horizontal bar labeled "AHB Bus Fabric" connecting all columns.

Also show small blocks connected to the bus bar:
- "CLINT (0x0200_0000)"  "PLIC (0x0C00_0000)"  "Boot ROM (MROM, 0x0000_0000)"

ARROWS:
- A thick orange arrow labeled "NICE Request / Response" connecting EXU to CNN Accelerator
- Thin downward arrows from each block to the AHB Bus
- Small arrow from Boot ROM to ITCM labeled "Reset vector → 0x80000000"

STYLE: Academic paper figure. No title. Clean, minimal, well-spaced.
```

---

## 图 2：PE 微架构 (fig3_3_pe_microarchitecture.png)

```
A hardware datapath diagram of a single processing element (PE). White background, black lines, clean academic style.

SHOW THESE ELEMENTS connected by arrows flowing top-to-bottom and left-to-right:

INPUTS:
- "W (INT8)" entering from top-left, labeled in blue
- "D (INT8)" entering from left side, labeled in green

MAIN BLOCKS (connected by arrows):
1. "8b × 8b Signed Multiplier" (rectangle, light blue fill #E3F2FD)
   → produces "P (INT16)"
2. "INT32 Accumulator" (rectangle, light orange fill #FFF3E0)
   → equation inside: "acc ← acc + sign_extend(P)"
   → feedback loop arrow curving from output back to input, labeled "accumulate"
3. "ReLU" (small diamond shape)
   → "if acc < 0 → output 0, else → output acc"

CONTROL INPUTS (entering from right side, thin arrows):
- "acc_clr" → clears accumulator (connected to Accumulator block)
- "en" → clock enable

OUTPUT:
- "Result (INT32)" at bottom

STYLE: Classic hardware datapath. Rectangular blocks for computation, diamond for ReLU mux. Signal names in small italic. No title.
```

---

## 图 3：PE 阵列 (fig3_4_pe_array.png)

```
A 4×4 systolic array grid diagram. Academic paper style, white background.

GRID: 4 columns × 4 rows of identical squares. Each square contains "PE" in the center. The squares are connected in a regular grid pattern.

ABOVE EACH COLUMN (top to bottom arrows):
- Small labels: "W[0]"  "W[1]"  "W[2]"  "W[3]"
- Vertical dashed arrows showing weight flow from top through each column of PEs

LEFT OF EACH ROW (left to right arrows):
- Small labels: "D[0]"  "D[1]"  "D[2]"  "D[3]"
- Horizontal dashed arrows showing activation flow from left through each row of PEs

BELOW THE GRID:
- Four vertical arrows from the bottom of each column converging into a single horizontal line
- The horizontal line connects to a rectangle labeled "Tree Adder (16-input)"
- Arrow down from the adder to "Result (INT32)"

STYLE: Clean black outlines, no fill in the PE squares. Thin arrows. The tree adder rectangle uses a light yellow fill (#FFF9C4). No title.
```

---

## 图 4：FPGA 构建流水线 (fig3_6_build_pipeline.png)

```
A pipeline/flow diagram showing the FPGA build process. Academic style, white background.

TWO PARALLEL TRACKS (labeled):

LEFT TRACK - "Software Track" (blue theme #E3F2FD):
Three connected blocks (top to bottom):
1. "C/C++ Source (.c, .S)"
2. "ELF Binary (.elf)"  ← label "RISC-V GCC"  
3. "Verilog Hex (.verilog)" ← label "objcopy"

RIGHT TRACK - "Hardware Track" (orange theme #FFF3E0):
Three connected blocks (top to bottom):
1. "RTL Source (.v, .sv)"
2. "Gate Netlist (.edf)" ← label "Vivado Synthesis"
3. "Routed Design (.dcp)" ← label "Vivado Implementation"

BOTH TRACKS MERGE into:
A large block labeled "Bitstream (.bit) + Debug Probes (.ltx)"

BELOW the merge block, a final block:
"FPGA Board (Davinci Pro A7-100T)" with sub-labels "JTAG Programming" "ILA Capture" "UART Output"

A curved feedback arrow from the bottom looping back to the top-left, labeled "Debug Iteration"

STYLE: Flowing from top to bottom. Clean rounded rectangles. The merge point shown clearly. No title.
```

---

## 图 5：验证流程 (fig_verification_chain.png)

```
A horizontal multi-stage verification flow diagram for an academic paper.

FOUR STAGES, left to right, connected by arrows:

Stage 1: "RTL Simulation" (light blue #E3F2FD)
  - "Icarus Verilog (iverilog)"
  - "CNN Accelerator Unit Test"
  - "RSTAT = 19 (PASS)"

Stage 2: "Full SoC Simulation" (medium blue #BBDEFB)
  - "E203 + NICE + ITCM/DTCM"
  - "hello_e203 Program"
  - "PC Trace Verified"

Stage 3: "FPGA Bitstream" (darker blue #90CAF9)
  - "Vivado 2023.2"
  - "7 Build Configurations"
  - "WNS > 13ns, All Met"

Stage 4: "Board Validation" (dark blue #42A5F5)
  - "Davinci Pro A7-100T"
  - "ILA + UART Verification"
  - "LeNet-5 MNIST Demo"

A RED curved feedback arrow from Stage 4 looping back to Stage 1, labeled "Debug Loop (Root Cause Analysis)"

STYLE: Horizontal flow. Each stage is a distinct block. Clean white background. No title.
```

---

## 不需要 AI 生成的图（matplotlib 已画好）

以下图是数据驱动的柱状图/波形图/饼图，matplotlib 画的效果没问题，**不需要重做**：

- `fig3_2_instruction_format.png` — 指令格式（已用 matplotlib 画好）
- `fig3_5_packed_format.png` — 数据打包格式（已用 matplotlib 画好）
- `fig4_3_speedup_bar.png` → `fig_speedup_bar.png` — 加速比柱状图
- `fig4_4_utilization.png` → `fig_utilization.png` — 资源利用率柱状图
- `fig4_5_timing.png` → `fig_timing.png` — 时序收敛柱状图
- `fig4_6_resource_pie.png` → `fig_resource_pie.png` — 资源饼图
- `fig4_1_ila_pc.png` → `fig_ila_pc_trace.png` — ILA 波形 (matplotlib)
- `fig4_2_ila_nice.png` → `fig_ila_nice_activity.png` — ILA 波形 (matplotlib)

---

## 替换方法

1. AI 生成图片后，保存 PNG 到桌面
2. 重命名为对应的文件名（如 `fig3_1_soc_architecture.png`）
3. 复制到：`C:\Users\16084\Documents\Graduation_Design_Library\thesis_latex\figures\`
4. 覆盖同名文件
5. 告诉我，我会重新编译论文
