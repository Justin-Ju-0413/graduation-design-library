# 毕设论文配图 — 终极AI生成提示词 + 手绘教程

---

## 通用规格要求 (每次生成都要遵守)

```
- 风格: 学术论文黑白/浅色为主，柔和不刺眼
- 字体: 统一无衬线字体(如Arial)，最小字号相当于打印10pt
- 分辨率: 至少1200px宽
- 线条: 统一1.5pt粗边框，连线1pt
- 背景: 纯白 #FFFFFF
- 禁止: Comic Sans、渐变填充、3D阴影效果、emoji
- 所有模块用圆角矩形 (border-radius ~6px)
- 标题在正上方居中，加粗
```

---

## Figure 2.1: 系统架构图

### 手绘教程

```
准备一张A4纸横放。从左到右画三列，底部画一条长横条。

1. 画布尺寸: 宽12cm × 高8cm

2. 左列 (蓝色区域, x=0.5, y=2.5, 宽3cm, 高3cm):
   - 大框: 浅蓝 #E3F2FD, 深灰边框
   - 标题(居中): "E203 RISC-V Core (RV32IMAC)" 加粗
   - 副标题(标题下方小字): "2-stage pipeline, Machine Mode" 灰色斜体
   - 子框1(上半): "IFU (Instruction Fetch)" 浅蓝 #BBDEFB
   - 子框2(下半): "EXU (Execute + NICE)" 浅蓝 #BBDEFB

3. 中列 (绿色区域, x=4.0, y=2.5, 宽2.5cm, 高3cm):
   - 大框: 浅绿 #E8F5E9
   - 标题: "CNN Accelerator" 加粗
   - 副标题: "NICE Interface" 灰色斜体
   - 子框1(上半): "NICE Decoder + Control FSM" 绿色 #C8E6C9
   - 子框2(下半): "4×4 PE Array (INT8 MAC)" 绿色 #C8E6C9

4. 左上→中: 画一条橙色 DOUBLE-HEADED 箭头 (<---->)
   因为NICE接口是双向的(请求+响应)
   标签: "NICE Req / Rsp" 橙色 #E65100

5. 右上列 (紫色区域, x=7.0, 上部):
   - 大框: 浅紫 #F3E5F5
   - 标题: "Memory"
   - 两个子框并排:
     a. "ITCM 64KB (64-bit)"  + 下方小字 "@ 0x8000_0000"
     b. "DTCM 64KB" + 下方小字 "@ 0x9000_0000"
   - 内存上面不画箭头指向CPU，只画两条独立的向下箭头到总线

6. 右下列 (灰色区域, x=7.0, 下部):
   - 大框: 浅灰 #ECEFF1
   - 标题: "Peripherals"
   - "UART0 @ 0x1001_3000"
   - "GPIO"

7. 底部 (x=0.5, y=0.3, 宽8.5cm, 高0.35cm):
   - 深灰长条 #90A4AE
   - 标签: "AHB Bus Fabric" 白色字加粗

8. 总线上的设备 (y=0.7, 在总线条上方):
   - "CLINT @ 0x0200_0000" (位置x=1.0)
   - "PLIC @ 0x0C00_0000" (位置x=2.6)
   - "Boot ROM (MROM) @ 0x0000_0000" (位置x=4.2)
   - 注意: 只有一个Boot ROM，不要在其他地方重复

9. 垂直连线:
   - CPU → 总线: 从CPU框底部(2.0, 2.5)垂直向下到总线(2.0, 0.65)
     ⚠️ 必须绕过CLINT(在x=1.0~2.3位置), 所以这条线在x=2.0
   - 加速器 → 总线: (5.25, 2.5) → (5.25, 0.65)
     ⚠️ 必须绕过PLIC(x=2.6~3.9)和Boot ROM(x=4.2~6.0), 所以线在x=5.25
   - 内存ITCM → 总线: (7.9, 上方) → (7.9, 0.65)
   - 内存DTCM → 总线: (7.9, 中部) → (7.9, 0.65)
   - UART/GPIO → 总线: (7.9, 下部) → (7.9, 0.65)
   - 每一个总线设备 → 总线: 短垂直箭头

🔴 红线检查:
  □ CPU→总线的垂直线是否穿过了任何外设模块? 不能穿过
  □ 加速器→总线的线是否穿过了PLIC或Boot ROM? 不能穿过
  □ ITCM和DTCM是分别独立连到总线吗? 不是串联
  □ Boot ROM只有一个吗? 是的，只在总线上方
  □ NICE箭头是双向的吗? 是↔不是→
  □ 所有地址标注都正确吗? ITCM=0x8000_0000, DTCM=0x9000_0000,
    UART=0x1001_3000, CLINT=0x0200_0000, PLIC=0x0C00_0000, MROM=0x0000_0000
```

### AI提示词

```
DRAW AN ACADEMIC SYSTEM ARCHITECTURE BLOCK DIAGRAM.

CRITICAL CONSTRAINTS — Violating any of these means the image is REJECTED:

CONSTRAINT 1: ITCM and DTCM are PARALLEL blocks side by side inside the Memory box. Each has its OWN separate vertical line down to the AHB Bus. They are NOT connected to each other in series.

CONSTRAINT 2: There is exactly ONE "Boot ROM (MROM)" block, placed on the AHB bus area at the bottom. Do NOT draw a second Boot ROM anywhere else.

CONSTRAINT 3: The arrow between E203 Core and CNN Accelerator must be a DOUBLE-HEADED ARROW (bidirectional ↔), colored orange, labeled "NICE Req / Rsp".

CONSTRAINT 4: Vertical connection lines from CPU and Accelerator to the AHB Bus must route AROUND the peripheral blocks (CLINT, PLIC, Boot ROM). Lines must NOT pass through any block.

LAYOUT SPECIFICATION:

Canvas: 9:5.5 aspect ratio, white background.

LEFT SECTION (x: 5%-35%, light blue #E3F2FD):
  Large rounded rectangle containing:
  - Title centered at top: "E203 RISC-V Core (RV32IMAC)" [bold, 11pt]
  - Subtitle: "2-stage pipeline, Machine Mode" [italic, gray, 7pt]
  - Upper sub-block: "IFU (Instruction Fetch)" [light blue #BBDEFB, 7pt]
  - Lower sub-block: "EXU (Execute + NICE)" [light blue #BBDEFB, 7pt]

MIDDLE SECTION (x: 40%-65%, light green #E8F5E9):
  Large rounded rectangle containing:
  - Title: "CNN Accelerator" [bold, 11pt]
  - Subtitle: "NICE Interface" [italic, gray, 7pt]
  - Sub-block 1: "NICE Decoder + Control FSM" [#C8E6C9, 7pt]
  - Sub-block 2: "4×4 PE Array (INT8 MAC)" [#C8E6C9, 7pt]

BETWEEN LEFT AND MIDDLE:
  Orange double-headed arrow (↔) connecting the two sections.
  Label above the arrow: "NICE Req / Rsp" [orange #E65100, 7pt]

RIGHT-TOP SECTION (x: 70%-90%, upper half, light purple #F3E5F5):
  Rounded rectangle containing:
  - Title: "Memory"
  - Two sub-blocks SIDE BY SIDE (same row):
    Left sub-block: "ITCM 64KB (64-bit)" with small text "0x8000_0000"
    Right sub-block: "DTCM 64KB" with small text "0x9000_0000"
  - Each sub-block has its OWN SEPARATE arrow down to the bus. NOT connected in series.

RIGHT-BOTTOM SECTION (x: 70%-90%, lower half, light gray #ECEFF1):
  Rounded rectangle containing:
  - Title: "Peripherals"
  - "UART0 @ 0x1001_3000" [7pt]
  - "GPIO" [6pt]
  - Arrow from this block down to bus

BOTTOM BAR (full width, y: 90%-95%, dark gray #90A4AE):
  Wide rectangle with white text "AHB Bus Fabric" [bold, 8pt]

ABOVE THE BUS BAR (y: 82%-90%):
  Three small blocks in a row:
  - "CLINT @ 0x0200_0000" [left position, 6pt]
  - "PLIC @ 0x0C00_0000" [center-left position, 6pt]
  - "Boot ROM (MROM) @ 0x0000_0000" [center-right position, 6pt]
  Each has a short vertical arrow down to the bus bar.

VERTICAL CONNECTIONS:
  - From CPU block bottom center → straight down to bus. Path: x≈20%, avoid CLINT block.
  - From Accelerator bottom center → straight down to bus. Path: x≈52%, avoid PLIC and Boot ROM blocks.
  - From ITCM sub-block bottom → straight down to bus.
  - From DTCM sub-block bottom → straight down to bus.
  - From Peripherals block bottom → straight down to bus.
  Lines must NOT intersect or pass through any colored blocks.

TITLE at top: "E203 SoC with NICE CNN Accelerator — System Architecture" [bold, 12pt]

COLOR PALETTE: Soft pastels only. #E3F2FD (CPU blue), #E8F5E9 (Accel green), #F3E5F5 (Memory purple), #ECEFF1 (IO gray), #90A4AE (Bus gray), #E65100 (NICE orange). Black text (#263238). Dark gray borders (#37474F, 1.2pt).

FONTS: Sans-serif. All labels readable. No text smaller than 6pt equivalent. No Comic Sans.

DO NOT INCLUDE: gradients, 3D shadows, emoji, multiple Boot ROMs, serial ITCM→DTCM connections, one-way NICE arrows, lines through blocks.
```

---

## Figure 2.3: PE微架构图

### 手绘教程

```
从上到下垂直画4个模块，中间用箭头连接。

1. 顶部输入 "W (INT8, 8-bit signed weight)" 
   箭头↓指向下方乘法器

2. 左侧输入 "D (INT8, 8-bit signed activation)"
   箭头→指向乘法器左侧

3. 乘法器框 (浅蓝 #E3F2FD, 宽4cm):
   "INT8 Multiplier"
   "W[7:0] × D[7:0] → P[15:0]"
   箭头↓指向下方ReLU

4. ReLU框 (浅粉 #FFEBEE, 宽4cm):
   "ReLU (optional)"
   "if en_relu && result < 0 then 0"
   箭头↓指向下方累加器

5. 累加器框 (浅黄 #FFF8E1, 宽4cm):
   "INT32 Accumulator"
   "acc ← acc + P (signed)"
   "(reset on acc_clr)"
   ⚠️ 在累加器框的右侧画一个小环形箭头 ↻
   标注 "accumulate" 
   这个环表示累加器自身反馈：新值 = 旧值 + 输入
   不要从ReLU拉线到累加器作为反馈！
   箭头↓指向下方输出

6. 底部输出: "Result (INT32)"

7. 左侧控制信号:
   - "acc_clr" (红色) → 指向累加器
   - "en" (灰色) → 指向累加器

🔴 红线检查:
  □ accumulate是不是画成了累加器自身的环形箭头? 不是从ReLU连过来的!
  □ ReLU在乘法器和累加器之间吗? 是的
  □ 数据流是: W,D → 乘法器 → ReLU → 累加器 → Result 吗?
  □ 所有模块之间都有清晰间隔，没有文字重叠?
```

### AI提示词

```
DRAW A PROCESSING ELEMENT (PE) MICROARCHITECTURE DIAGRAM FOR A CNN ACCELERATOR.

CRITICAL CONSTRAINT — THIS IS THE MOST COMMON MISTAKE:
The "accumulate" feedback is an INTERNAL loop of the Accumulator. 
It is NOT a wire from ReLU to Accumulator. 
The accumulate represents: acc_new = acc_old + input.
DRAW IT AS A SMALL CIRCULAR ARROW ↻ INSIDE OR NEXT TO THE ACCUMULATOR BOX.
DO NOT draw a curved arrow from ReLU going into the Accumulator.

VERTICAL DATA FLOW (top to bottom):

Step 1 — INPUTS:
  - From TOP: label "W (INT8, 8-bit signed weight)" with downward arrow ↓
  - From LEFT: label "D (INT8, 8-bit signed activation)" with rightward arrow →

Step 2 — MULTIPLIER (light blue #E3F2FD box, centered):
  Title: "INT8 Multiplier" [bold]
  Formula: "W[7:0] × D[7:0] → P[15:0]"
  Downward arrow ↓ from multiplier output

Step 3 — ReLU (light pink #FFEBEE box, centered, BELOW multiplier):
  Title: "ReLU (optional)"
  Text: "if en_relu && result < 0 then 0"
  Downward arrow ↓ from ReLU output

Step 4 — ACCUMULATOR (light yellow #FFF8E1 box, centered, BELOW ReLU):
  Title: "INT32 Accumulator" [bold]
  Text: "acc ← acc + P (signed)"
  Small text below: "(reset on acc_clr)"
  
  ON THE RIGHT SIDE of this box, draw a SMALL CIRCULAR ARROW (↻, loopback icon).
  Label near it: "accumulate" [orange #E65100, 7pt]
  This loop means: output feeds back to input internally.

  Downward arrow ↓ from accumulator output

Step 5 — OUTPUT:
  Label: "Result (INT32)" [bold, centered below accumulator]

CONTROL SIGNALS (from LEFT side):
  - "acc_clr" [red #C62828] → arrow pointing to Accumulator left side
  - "en" [gray #546E7A] → arrow pointing to Accumulator left side

TITLE: "Processing Element (PE) Microarchitecture" [bold, centered at top]

SPACING: All 4 boxes (Multiplier, ReLU, Accumulator) must have CLEAR gaps between them. No text overlap. Each box approximately 4cm wide.

COLORS: Multiplier #E3F2FD, ReLU #FFEBEE, Accumulator #FFF8E1, accumulate loop #E65100, control signals #C62828 and #546E7A, data arrows #37474F.

DO NOT INCLUDE: curved feedback arrow from ReLU to Accumulator, text inside other text, overlapping labels.
```

---

## Figure 2.4: PE阵列图

### 手绘教程

```
画一个4行×4列的PE网格。

1. 画16个PE方块，排列成4行4列
   每个方块标签: "PE 0,0", "PE 0,1", ... "PE 3,3"
   (行号,列号)
   交替使用浅绿#E8F5E9和白色

2. 顶部: W[0],W[1],W[2],W[3] 四个输入
   每个W[i]箭头↓进入第i列顶部PE

3. 左侧: D[0],D[1],D[2],D[3] 四个输入
   每个D[i]箭头→进入第i行左侧PE

4. PE之间的连线:
   - 水平方向: 每行PE之间用实线→连接(从左到右)
   - 垂直方向: 每列PE之间用虚线--↓连接(从上到下)
   
5. 最右边一列PE(PE[0,3]到PE[3,3])向右的箭头
   没有继续连接的PE — 这些箭头应该终止或指向输出
    
6. 最下边一行PE(PE[3,0]到PE[3,3])向下的箭头
   指向Tree Adder

7. Tree Adder:
   位置在PE阵列下方偏右
   标注: "Tree Adder (4-input)" — ⚠️是4-input不是16-input
   因为数据在垂直方向已经累加(Output-Stationary)
   只有最下一行的4个PE输出需要最终求和
   
   如果不采用Output-Stationary数据流而是所有PE同时输出:
   则标注 "Tree Adder (16-input)" 并且必须从ALL 16个PE拉线到Adder

8. 输出: Tree Adder → "Result (INT32)"

🔴 红线检查:
  □ Tree Adder标注和实际连线数一致吗? 4-input = 4条线 / 16-input = 16条线
  □ 每个PE都有标签吗? PE R,C格式
  □ W从上方输入，D从左侧输入吗?
  □ 没有悬空的未连接箭头吗?
```

### AI提示词

```
DRAW A 4×4 SYSTOLIC PE ARRAY WITH OUTPUT-STATIONARY DATAFLOW.

CRITICAL CONSTRAINT:
The Tree Adder label MUST match the actual number of input connections.
- If only the BOTTOM ROW (4 PEs) connects to the adder → label "Tree Adder (4-input)"
- If ALL 16 PEs connect to the adder → label "Tree Adder (16-input)" AND draw all 16 connections
CHOOSE ONE and be consistent. For Output-Stationary dataflow, use 4-input.

LAYOUT:

4×4 GRID of PE blocks (4 rows labeled 0-3, 4 columns labeled 0-3).
Each PE is a rounded rectangle with text "PE R,C" (e.g., "PE 0,0", "PE 1,2").
Alternating fill colors: #E8F5E9 (light green) and white.
Grid spacing: equal gaps between all PEs.

DATA INPUTS:
  TOP of grid: W[0], W[1], W[2], W[3] — one above each column
  Each W[i] has downward arrow into the top PE of column i

  LEFT of grid: D[0], D[1], D[2], D[3] — one beside each row
  Each D[i] has rightward arrow into the leftmost PE of row i

INTER-PE CONNECTIONS:
  HORIZONTAL: Solid arrows → from each PE to the PE on its right (same row, next column)
  VERTICAL: Dashed arrows --> from each PE to the PE below it (same column, next row)

OUTPUT CONNECTIONS:
  From the BOTTOM of each PE in the LAST ROW (row 3), draw downward arrows.
  All 4 arrows connect to a single "Tree Adder" block positioned below-right of the grid.
  
  Label the adder: "Tree Adder (4-input)" [if only bottom row connects]
  
  From Tree Adder output, downward arrow to: "Result (INT32)"

DANGLING ARROWS:
  - PEs in the rightmost column (col 3) have rightward arrows that terminate. These are fine.
  - PEs in the bottom row have downward arrows going to the Tree Adder. All connected.

TITLE: "4×4 Systolic Processing Element Array" [bold]
SUBTITLE: "Output-Stationary Dataflow" [gray, smaller]

LABELS: All PE labels readable. W/D indices clear. Tree Adder label consistent with actual connections.

DO NOT INCLUDE: dangling unlabeled arrows, 16-input label with only 4 connections, missing PE labels.
```

---

## Figure 2.5: 数据打包格式

### 手绘教程

```
画一条水平长条代表32位寄存器，分成4个8bit段。

1. 长条 [31:0]，4个等宽段:
   [31:24] | [23:16] | [15:8] | [7:0]
   
2. 每段内文字:
   "Value[3]\nINT8" | "Value[2]\nINT8" | "Value[1]\nINT8" | "Value[0]\nINT8"

3. 每段下方: "Byte 3" | "Byte 2" | "Byte 1" | "Byte 0"

4. 示例行(下方):
   "Example: rs1 = 0x12_34_AB_CD"
   下面画4个小箭头:
   0x12 ↑ Value[3],  0x34 ↑ Value[2],  0xAB ↑ Value[1],  0xCD ↑ Value[0]

5. 图左侧: 垂直文字/箭头 "WLOAD / DLOAD packs 4×INT8 → 32-bit register"

🔴 红线检查:
  □ 所有bit范围标注一致吗? 全部[31:24][23:16][15:8][7:0]
  □ 没有混用31和24这种不一致的情况
  □ 4个段等宽
```

### AI提示词

```
DRAW A DATA FORMAT DIAGRAM: 4 INT8 VALUES PACKED INTO ONE 32-BIT REGISTER.

CRITICAL: Bit range labels must be CONSISTENT throughout. Use ONLY this format:
[31:24], [23:16], [15:8], [7:0]. Do NOT mix different styles like "0, 8, 16, 31".

LAYOUT:

HORIZONTAL BAR representing a 32-bit register.
Divided into 4 EQUAL-WIDTH segments, each 8 bits wide.

Each segment (left to right, MSB to LSB):

| Segment 3 [31:24]       | Segment 2 [23:16]       | Segment 1 [15:8]        | Segment 0 [7:0]         |
| "Value[3] (INT8)"       | "Value[2] (INT8)"       | "Value[1] (INT8)"       | "Value[0] (INT8)"       |
| "Byte 3"                | "Byte 2"                | "Byte 1"                | "Byte 0"                |

Segment colors: light blue, light green, light yellow, light red (left to right).
Dark borders between segments.

BELOW THE BAR, an example row in a light yellow box:
"Example: rs1 = 0x12_34_AB_CD"
With mapping text below:
"Value[3]=0x12    Value[2]=0x34    Value[1]=0xAB    Value[0]=0xCD"

LEFT SIDE of the diagram, a vertical annotation:
Arrow with text "WLOAD / DLOAD packs 4×INT8 → 32-bit register" [blue, 8pt]

TITLE: "Packed INT8 Data Format for WLOAD and DLOAD Instructions" [bold, 11pt]

DO NOT INCLUDE: inconsistent bit labels (no mixing [31:24] with "24"), overlapping tick marks, 31 as a boundary value.

BIT LABELS FORMAT: Every segment shows its bit range in the SAME format: [MSB:LSB].
Bit 31 is the leftmost (most significant), bit 0 is the rightmost (least significant).
```

---

## 生成后检查清单

用下面这个命令逐一检查每张图:
```
node vision.js <图片> "逐一检查：1.文字重叠 2.连线错误 3.标签准确性 4.多余/缺失元素"
```

### 通过标准:
- Fig 2.1: ITCM/DTCM并联✓ 只有一个BootROM✓ NICE双向箭头✓ 线不穿模块✓
- Fig 2.3: accumulate是环形反馈✓ ReLU在乘法和累加之间✓ 无文字重叠✓
- Fig 2.4: Tree Adder标注与连线数一致✓ 每个PE有标签✓ W从上方D从左侧✓
- Fig 2.5: bit范围标注全部一致✓ 4段等宽✓ 示例正确✓
