# 论文图片手动生成指南

> **桌面路径**：`需手动生成的图片\`
> **替换目标**：`Graduation_Design_Library\thesis_latex\figures\`
> **关键要求**：文件名必须与现有文件**完全一致**（含大小写），直接覆盖即可，不需要修改 LaTeX 源码。

---

## 目录

- [一、Nanobanana AI 生成（3 张，必须替换）](#一nanobanana-ai-生成3-张必须替换)
  - [通用注意事项](#通用注意事项)
  - [Fig 3.1 — 系统架构框图](#fig-31--系统架构框图)
  - [Fig 3.3 — PE 微架构](#fig-33--pe-微架构处理单元内部结构)
  - [Fig 3.4 — PE 阵列](#fig-34--pe-阵列4×4-网格)
- [二、Vivado 原生截图（2 张，建议替换）](#二vivado-原生截图2-张建议替换)
  - [前置条件检查](#前置条件检查)
  - [详细操作步骤](#详细操作步骤)
  - [Fig 4.1 — ILA PC 追踪波形](#fig-41--ila-pc-追踪波形)
  - [Fig 4.2 — NICE 指令 ILA 波形](#fig-42--nice-指令-ila-波形)
- [三、生成后的验证与替换](#三生成后的验证与替换)
- [四、常见问题排查](#四常见问题排查)
- [优先级总览](#优先级总览)

---

## 一、Nanobanana AI 生成（3 张，必须替换）

这 3 张是目前论文中最影响质量的图。用以下英文提示词喂给 Nanobanana。

### 通用注意事项

1. **访问方式**：打开浏览器访问 [Nanobanana](https://nanobanana.com)，使用 Google 账号登录。
2. **模型选择**：选择最新的 **Nano Banana Pro** 或 **Nano Banana** 模型（Pro 效果更好，推荐优先尝试）。
3. **图片尺寸**：在生成设置中指定 **16:9 横版** 或 **1200×675** 左右的分辨率。论文中图片宽度约 12-14cm，太小的图放大后会模糊。
4. **导出格式**：生成后右键保存为 **PNG**，不要用 JPEG（JPEG 压缩会在论文打印时产生可见伪影）。
5. **风格一致性**：三张图尽量用同一次会话生成，Nanobanana 会保持风格连贯。
6. **迭代策略**：
   - 第一次生成后检查结构是否正确（连线、模块位置）
   - 如果结构不对，重新发送提示词（不要用"修改"指令，直接重新生成通常更准）
   - 如果结构对但风格不满意，可以追加 "Make the lines thinner and remove the gradient background" 之类的精修指令
   - 一般 2-3 次迭代可得到可用结果
7. **参考图**：`01_参考现有图\` 目录下有当前论文中使用的版本，可拖入 Nanobanana 作为风格/结构参考。

---

### Fig 3.1 — 系统架构框图

| 项目 | 内容 |
|------|------|
| **文件名** | `fig3_1_soc_architecture.png` |
| **参考图** | `01_参考现有图/fig3_1_soc_architecture.png` |
| **描述** | RISC-V SoC 整体架构，展示 CPU、CNN 加速器、存储器和外设之间的连接关系 |
| **论文位置** | 第三章 3.2 节，系统总体架构 |

**提示词**：

```
Technical block diagram of a RISC-V SoC with CNN accelerator for an academic paper. Show these components with clear rectangular blocks and arrows:

LEFT SIDE - Processor:
- "E203 RISC-V Core (RV32IMAC)" containing IFU, EXU with NICE interface, LSU/BIU

CENTER - Accelerator:
- "CNN Accelerator" containing "NICE Decoder + Control FSM" connected to "4×4 PE Array (INT8 MAC)"

RIGHT SIDE - Memory & Peripherals:
- "ITCM 64KB (64-bit)" at 0x8000_0000
- "DTCM 64KB (32-bit)" at 0x9000_0000
- "UART0" at 0x1001_3000
- "GPIO"

Bottom: "AHB Bus Fabric" connecting all components.

Style: Clean white background, black outlines, single blue accent (#2196F3) for the accelerator block. Arrow labels showing "NICE Request/Response" on the CPU-to-accelerator connection. No title text in the image. Academic paper figure, monochrome with one accent color.
```

**自检清单**（生成后逐项核对）：

- [ ] 三个区域（处理器 / 加速器 / 存储器+外设）左右排列清晰
- [ ] E203 的 NICE 接口明确标出
- [ ] CNN 加速器内部包含 NICE Decoder + Control FSM 和 4×4 PE Array
- [ ] AHB Bus Fabric 在底部连接所有模块
- [ ] CPU 到加速器之间有 "NICE Request/Response" 标注
- [ ] ITCM/DTCM 地址标注正确（0x8000_0000 / 0x9000_0000）
- [ ] 白色背景，无多余装饰元素

---

### Fig 3.3 — PE 微架构（处理单元内部结构）

| 项目 | 内容 |
|------|------|
| **文件名** | `fig3_3_pe_microarchitecture.png` |
| **参考图** | `01_参考现有图/fig3_3_pe_microarchitecture.png` |
| **描述** | 单个 PE 内部的数据通路，展示 INT8 乘法器和 INT32 累加器的连接 |
| **论文位置** | 第三章 3.3 节，PE 设计 |

**提示词**：

```
Microarchitecture diagram of a single processing element (PE) for a systolic array. Show:

INPUTS (left and top):
- "Weight W (INT8)" entering from top
- "Activation D (INT8)" entering from left

DATAPATH BLOCKS (connected by arrows):
- INT8 multiplier block: "8b × 8b → 16b"
- INT32 accumulator block with feedback loop (arrow looping back): "Σ (INT32)"
- Output at bottom: "Result (INT32)"

CONTROL SIGNALS (entering from side):
- "acc_clr" → accumulator clear
- "en" → enable/clock gate

Style: Hardware datapath diagram style. Rectangular blocks, sharp black lines on white background. Signal labels in small italic font. No color needed (monochrome is fine). Academic paper figure. No title.
```

**自检清单**（生成后逐项核对）：

- [ ] 两个输入端口（Weight 从上入，Activation 从左入）方向正确
- [ ] 乘法器标注 "8b × 8b → 16b"
- [ ] 累加器有回环箭头表示累加反馈
- [ ] acc_clr 和 en 两个控制信号均已标出
- [ ] 底部输出为 "Result (INT32)"
- [ ] 纯黑白，无线条颜色混杂

---

### Fig 3.4 — PE 阵列（4×4 网格）

| 项目 | 内容 |
|------|------|
| **文件名** | `fig3_4_pe_array.png` |
| **参考图** | `01_参考现有图/fig3_4_pe_array.png` |
| **描述** | 4×4 脉动阵列组织，展示权重和激活数据在 PE 间的流动方向 |
| **论文位置** | 第三章 3.3 节，PE 阵列架构 |

**提示词**：

```
4×4 systolic array organization diagram for an academic paper. Show:

GRID: 4 columns × 4 rows of identical PE (processing element) blocks. Each block labeled "PE".

DATA FLOW:
- Top: "W[0]" "W[1]" "W[2]" "W[3]" (weight inputs) entering each column from above, arrows flowing downward through each column
- Left: "D[0]" "D[1]" "D[2]" "D[3]" (activation inputs) entering each row from the left, arrows flowing rightward through each row

OUTPUT:
- At bottom of each column: arrows converging into a "Tree Adder" block
- Final output at bottom right: "Σ (INT32)"

Style: Clean academic diagram. White background, thin uniform black outlines. Each PE shown as a simple square with "PE" inside. Data flow arrows. No gradient fill, no shadow effects. No title.
```

**自检清单**（生成后逐项核对）：

- [ ] 4×4 网格完整（4 列 4 行，共 16 个 PE 块）
- [ ] 权重 W[0]-W[3] 从顶部向下流经各列
- [ ] 激活 D[0]-D[3] 从左侧向右流经各行
- [ ] 底部有 Tree Adder 汇聚求和
- [ ] 最终输出 Σ (INT32) 在右下角
- [ ] 每个 PE 块大小一致，排列整齐
- [ ] 箭头方向正确（数据流方向不应反向）

---

## 二、Vivado 原生截图（2 张，建议替换）

ILA 波形图用 Vivado 原生截图比 matplotlib 绘制的波形更权威，审稿人更认可。

### 前置条件检查

在开始前确认以下几点：

1. **Vivado 版本**：确认安装了 Vivado 2019.1 或更高版本（实际使用的是 2023.2：`D:\Xilinx\Vivado\2023.2\bin\vivado.bat`）。
2. **FPGA 板卡**：需要 DaVinci A7 100T 开发板（`xc7a100tfgg484-2`）。
3. **硬件连接**：FPGA 板通过 JTAG（Micro-USB 线）连接到电脑。

4. **两张图需要两个不同的 bitstream**（probe 定义不同）：

   | 图 | 使用 Bitstream | Probe 定义 |
   |----|---------------|-----------|
   | Fig 4.1 (PC 追踪) | `bootvec_sysclk_ila` | probe0=pc, probe5=uart |
   | Fig 4.2 (NICE 活动) | `cnn_sysclk_ila` | probe4=nice_csr, probe5=nice_hs |

5. **各 bitstream 完整路径**：

   **Fig 4.1 (PC 追踪)**：
   ```
   Bitstream:  C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\bootvec_sysclk_ila_artifacts\system.bit
   Probes:     C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\bootvec_sysclk_ila_artifacts\debug_nets.ltx
   ```

   **Fig 4.2 (NICE 活动)**：
   ```
   Bitstream:  C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\cnn_sysclk_ila_artifacts\system.bit
   Probes:     C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\cnn_sysclk_ila_artifacts\system.ltx
   ```

   > **注意**：两张图的 bitstream 不同，截完一张后需要 **重新 Program Device** 换另一个 bitstream，再截第二张。

> **如果板卡不在手边**：可以用 Vivado 打开之前保存的 ILA 数据文件（`.ila`），如果没有保存过，只能用现有的 matplotlib 截图替代。

### 详细操作步骤

#### 第一步：打开 Vivado 硬件管理器

1. 启动 **Vivado**。
2. 在欢迎界面点击 **Open Hardware Manager**（或在顶部菜单 `Flow → Open Hardware Manager`）。
3. 无需打开工程，Hardware Manager 可以独立运行。

#### 第二步：连接 FPGA 板

1. 在 Hardware Manager 窗口，点击绿色 **"Open target"** 链接（或 `Open target → Auto Connect`）。
2. Vivado 会自动扫描 JTAG 链，检测到 FPGA 芯片后显示在 Hardware 面板。
3. 如果报错 "No hardware target found"：
   - 检查 FPGA 板电源是否打开（板上的电源指示灯是否亮）
   - 检查 JTAG 线是否插好，Windows 设备管理器是否识别到 JTAG 设备
   - 尝试 `Open target → Open New Target` → 手动选择 JTAG 频率（降到 6MHz 试试）

#### 第三步：下载 Bitstream

1. 在 Hardware 面板中，右键点击 FPGA 芯片（如 `xc7a100t_0`）→ **Program Device**。
2. 在弹出对话框中，填入 bitstream 和 probes 文件的绝对路径：

   **Fig 4.1 (PC 追踪) 用 bootvec：**
   - **Bitstream file**：
     ```
     C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\bootvec_sysclk_ila_artifacts\system.bit
     ```
   - **Debug probes file**：
     ```
     C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\bootvec_sysclk_ila_artifacts\debug_nets.ltx
     ```

   **Fig 4.2 (NICE 活动) 用 cnn：**
   - **Bitstream file**：
     ```
     C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\cnn_sysclk_ila_artifacts\system.bit
     ```
   - **Debug probes file**：
     ```
     C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\cnn_sysclk_ila_artifacts\system.ltx
     ```

   > **重要**：截完 Fig 4.1 后，需要回到这一步，重新 Program Device，换成 cnn 的 bitstream + probes，再截 Fig 4.2。两个 bitstream 的 ILA probe 定义不同——bootvec 的 probe5 是 uart，cnn 的 probe5 才是 nice_hs。
3. 点击 **Program**，等待进度条完成（约 30 秒到 1 分钟）。
4. 下载成功后 FPGA 板上的 **DONE LED** 会亮起。

#### 第四步：配置 ILA 触发条件

1. 在 Hardware 面板展开 FPGA 芯片，找到 **hw_ila_1**（ILA 调试核）。
2. 点击 **hw_ila_1** 会在右侧打开 ILA Dashboard 窗口。
3. ILA Dashboard 包含三个子窗口：
   - **Trigger Setup** — 设置触发条件
   - **Waveform** — 显示捕获的波形
   - **Settings** — 捕获参数

4. ILA Dashboard 有两个标签页（在窗口左上方）：
   - **Trigger Setup** — 设置触发条件和触发位置
   - **Capture Setup** — 设置捕获方程（不需要动，本项目 ILA 不支持 BASIC capture mode 会报错，**忽略即可**）

5. 切换到 **Trigger Setup** 标签页（不是 Capture Setup），设置触发条件：

   - 对于 **Fig 4.1（PC 追踪）**：
     - 找到 probe0（`pc[31:0]`），右键 → **Compare Value** → 选 `==` → 填入 `80000000`
     - **触发位置**：在 Trigger Setup 窗口右侧找到 **Trigger Position** 输入框，填入 `0`（窗口起点），这样可以看到跳转前后的完整过程

   - 对于 **Fig 4.2（NICE 信号）**：
     - 找到 probe5（`nice_hs[3:0]`），右键 → **Compare Value** → 选 `==` → 填入 `1`
     - **触发位置**：填入 `512`（窗口中间），这样可以看到握手前后

   > **Trigger Position 在哪**：在 Trigger Setup 标签页内，通常位于触发条件表格的下方或右侧，是一个数字输入框。如果找不到，看看是否有 "Capture Mode" 区域，将模式设为 "BASIC"（如果可选），然后在旁边就能看到 Position 设置。

6. 如果弹窗报错 "Capture equation cannot be added because 'hw_ila_1' does not support BASIC capture mode"：
   - **忽略这个报错**，不需要设置捕获方程
   - 这个报错是因为点开 Capture Setup 标签页触发的，不去管它就行
   - 切回 Trigger Setup 标签页，设置触发条件 + 触发位置，然后直接 Run Trigger 即可

7. 在 **Settings** 窗口中确认捕获参数：
   - **Capture depth**：默认 1024，足够
   - **Data depth**：确认所有探针都已选中

#### 第五步：运行和捕获

1. 点击 ILA Dashboard 窗口左上角的 **▶ Run Trigger** 按钮（蓝色三角）。
2. ILA 状态变化：
   - `Idle` → `Waiting for Trigger`（等待触发条件满足）
   - 触发条件满足后 → `Uploading` → `Captured`
3. 绿色进度条走完表示捕获完成。
4. 如果长时间停在 "Waiting for Trigger"：
   - 检查触发条件是否合理（PC 真的会跳到 0x80000000 吗？nice_hs 真的会拉高吗？）
   - FPGA 是否已经正常运行（检查串口是否有输出）
   - 尝试把触发条件改为更宽松的值，或者改用 Immediate Trigger（不设条件，直接抓取当前波形）

#### 第六步：调整波形显示

1. **展开信号**：在 Waveform 窗口中，点击探针旁边的 `+` 展开总线信号，查看每个 bit。
2. **调整时间范围**：用鼠标滚轮缩放时间轴，或用工具栏的放大镜工具。
3. **调整信号顺序**：拖拽探针名可以重新排列显示顺序。
4. **设置基数**：右键探针 → **Radix** → 选择：
   - **Hexadecimal** — 地址/数据总线（推荐）
   - **Binary** — 控制信号
   - **Unsigned Decimal** — 计数值
5. **添加标记**：在波形上有意义的位置，右键 → **Add Marker**，给关键跳变点加标记。

#### 第七步：截图

1. 调整 ILA Waveform 窗口到合适大小，确保所有相关信号都可见。
2. **禁用深色主题**（如果使用）：`Tools → Settings → Display → Windows` 确保使用浅色主题，白底截图在论文中更干净。
3. 截图：
   - 用 Windows 自带截图工具（`Win + Shift + S`）精确截取波形区域
   - 或使用 Vivado 内置导出：Waveform 窗口 → `File → Export → Export Waveform` → 选择 PNG
   - **推荐用 Vivado 内置导出**，分辨率更高，不会有时钟截断问题
4. 保存截图到桌面 `需手动生成的图片\` 目录，直接命名为目标文件名。

---

### Fig 4.1 — ILA PC 追踪波形

| 项目 | 内容 |
|------|------|
| **文件名** | `fig_ila_pc_trace.png` |
| **参考图** | `02_Vivado截图/fig_ila_pc_trace.png` |
| **使用 Bitstream** | `bootvec_sysclk_ila`（不是 cnn 版本！） |
| **关键 Probe** | probe0 = `pc[31:0]` (32-bit) |
| **触发条件** | pc[31:0] == 0x80000000 |
| **触发位置** | 窗口起点（Position: 0） |
| **截取内容** | PC 从 MROM 地址空间 (0x0000_0000) 跳转到 ITCM (0x8000_0000) 的关键过程 |

**所有可用 Probe（bootvec_sysclk_ila）**：

| Probe | 信号名 | 宽度 | 含义 |
|-------|--------|------|------|
| probe0 | pc | 32 | IFU 取指 PC 地址 |
| probe1 | status | 4 | 系统状态标志 |
| probe2 | membus_live | 3 | 内存总线活跃标志 |
| probe3 | mem_addr | 32 | 内存地址总线 |
| probe4 | membus_counts | 32 | 内存总线访问计数 |
| probe5 | uart | 4 | UART TX/RX 状态 |
| probe6 | flags | 3 | 通用标志信号 |

**波形中应能看到**：
- PC 在 0x0000_0xxx 范围内递增（MROM 引导阶段）
- 一个明显的跳变到 0x8000_0000（跳入 ITCM，开始执行用户程序）
- 之后 PC 在 0x8000_xxxx 范围内变化（正常程序执行）

**操作提示**：
- PC 基数设为 **Hexadecimal**，否则地址不可读
- 触发后如果没抓到跳变，把 Trigger Position 改成 0（从窗口起点开始记录）
- 截完这张图后，需要换 `cnn_sysclk_ila` 的 bitstream 再截 Fig 4.2

---

### Fig 4.2 — NICE 指令 ILA 波形

| 项目 | 内容 |
|------|------|
| **文件名** | `fig_ila_nice_activity.png` |
| **参考图** | `02_Vivado截图/fig_ila_nice_activity.png` |
| **使用 Bitstream** | `cnn_sysclk_ila`（不是 bootvec 版本！） |
| **关键 Probe** | probe4 = `nice_csr[31:0]`, probe5 = `nice_hs[3:0]` |
| **触发条件** | nice_hs[3:0] == 1 |
| **触发位置** | 窗口中间（Position: 512） |
| **截取内容** | 展示一次 NICE 指令执行时 handshake 信号的完整时序 |

**所有可用 Probe（cnn_sysclk_ila）**：

| Probe | 信号名 | 宽度 | 含义 |
|-------|--------|------|------|
| probe0 | pc | 32 | IFU 取指 PC 地址 |
| probe1 | reset_uart | 4 | 复位和 UART 状态 |
| probe2 | liveness | 3 | 系统活跃标志 |
| probe3 | pc_activity | 32 | PC 活动监控 |
| **probe4** | **nice_csr** | 32 | **NICE CSR 数据** |
| **probe5** | **nice_hs** | 4 | **NICE 手握手信号** |
| probe6 | mem_status | 3 | 内存状态标志 |

**波形中应能看到**：
- nice_hs 从 0 → 1 → 0 的脉冲（握手信号）
- nice_csr 在握手期间的数据变化（NICE 指令的 CSR 操作）
- 握手前后相关信号的稳定/变化状态

**操作提示**：
- nice_hs 基数用 **Binary**（单 bit 信号），nice_csr 用 **Hexadecimal**
- 把 probe4 和 probe5 拖到相邻行，上下排列，方便观察时序关系
- 最好抓到一个完整的握手周期（请求→应答→释放）
- **截图前确认**：Program Device 时加载的是 `cnn_sysclk_ila_artifacts\system.bit` + `system.ltx`，不是 bootvec 的

---

## 三、生成后的验证与替换

### 验证步骤

1. **文件名校对**：
   ```
   fig3_1_soc_architecture.png   ← 注意下划线，不是连字符
   fig3_3_pe_microarchitecture.png
   fig3_4_pe_array.png
   fig_ila_pc_trace.png
   fig_ila_nice_activity.png
   ```

2. **图片质量检查**：
   - 每张 PNG 的尺寸应至少 1000px 宽，低于这个分辨率在论文 PDF 中会模糊
   - 文件大小一般在 50KB ~ 300KB 比较合理，太小说明分辨率不够，太大说明可以压缩
   - 打开图片放大到 100%，检查线条是否清晰无锯齿

3. **内容校对**：
   - 对照上面各图的自检清单逐项核对
   - 和 `01_参考现有图/` 或 `02_Vivado截图/` 中的参考图对比，确认关键元素不缺失

### 替换操作

1. 将 5 张 PNG 文件复制到论文 figures 目录：
   ```
   C:\Users\16084\Documents\Graduation_Design_Library\thesis_latex\figures\
   ```
2. 直接覆盖同名文件。
3. 覆盖前建议**备份原文件**（把旧文件重命名加 `_old` 后缀即可）。
4. 替换完成后通知我，我会重新编译论文 PDF 检查效果。

---

## 四、常见问题排查

### Nanobanana 相关

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| 生成的图缺少某些模块 | 提示词太长，模型遗漏 | 把提示词拆分——先要求生成主体结构，再追加指令补细节 |
| 架构图的连线混乱 | 模型对总线拓扑理解偏差 | 在提示词中明确指定 "use a simple shared bus topology, single horizontal bus at bottom" |
| 字体模糊或不可读 | 输出分辨率不够 | 在提示词末尾加 "High resolution, minimum 1200px wide, crisp text" |
| 颜色不对（太花哨） | 模型偏好多彩风格 | 强调 "monochrome with ONE blue accent only, no other colors" |
| PE 阵列中的 PE 大小不一 | 模型对网格排列不精确 | 追加 "All 16 PE blocks must be identical squares, evenly spaced in a perfect 4×4 grid" |

### Vivado 相关

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| "No hardware target found" | JTAG 驱动/连接问题 | 检查设备管理器 → 重新插拔 USB → 装 [Vivado 自带的 JTAG 驱动](https://docs.xilinx.com/r/en-US/ug973-vivado-release-notes-install-license/Install-Cable-Drivers) |
| Program 失败（红色报错） | Bitstream 和实际板卡不匹配 | 确认 bitstream 是为 DaVinci A7 100T 生成的，不是其他型号 |
| ILA 一直 Waiting for Trigger | 触发条件永远满足不了 | 改用 Immediate Trigger 先看有没有波形，如果波形全 0 说明 FPGA 程序没跑起来 |
| 波形中信号全为 0 或全为 X | FPGA 未正确运行 / debug nets 不匹配 | 重新生成 bitstream + debug_nets.ltx（`write_debug_probes` 要和 bitstream 同一次 run） |
| 截图后波形不清晰 | Vivado 窗口缩放太小 | 截前把 Waveform 窗口最大化，波形纵向拉开，字号调大到 12pt 以上 |
| 找不到 Hardware Manager | Vivado 版本太旧（<2018） | 旧版叫 "Vivado Lab Edition"，需单独安装 |

### 如果没有 FPGA 板

有两条替代路径：

1. **Vivado Simulator 仿真截图**（次选）：
   - 用 Vivado 自带的 xsim 跑后仿真（Post-Implementation Simulation）
   - 仿真波形窗口的截图也可以作为替代
   - 优点：不需要硬件；缺点：不如真实 ILA 波形权威

2. **保留现有 matplotlib 截图**（保底）：
   - `02_Vivado截图/` 中是当前使用的截图
   - 如果实在无法替换，这 2 张图维持现状也可接受

---

## 优先级总览

| 优先级 | 编号 | 图片 | 方式 | 估计时间 | 备注 |
|:------:|------|------|------|:--------:|------|
| 1 | Fig 3.1 | 系统架构框图 | Nanobanana | 5-10 min | AI 架构图，最影响论文观感 |
| 2 | Fig 3.3 | PE 微架构 | Nanobanana | 5-10 min | 硬件数据通路图 |
| 3 | Fig 3.4 | PE 阵列（4×4） | Nanobanana | 5-10 min | 脉动阵列拓扑图 |
| 4 | Fig 4.1 | ILA PC 追踪 | Vivado 截图 | 15-20 min | 需要 FPGA 板卡 |
| 5 | Fig 4.2 | ILA NICE 活动 | Vivado 截图 | 15-20 min | 需要 FPGA 板卡 |

> **建议顺序**：先把 3 张 Nanobanana 图搞定（不需要硬件，在家就能做），再集中处理 Vivado 截图（需要连接板卡，最好在实验室一次性搞定）。
