# 毕业设计十天闭环任务书

## 一、课题名称

基于 RISC-V 自定义指令的轻量级 CNN 加速器设计与 FPGA 原型验证

## 二、当前基础

本课题已完成 RISC-V E203 SoC 与 CNN/NICE 加速器的基础集成，并形成了从 RTL 单元验证到 full-SoC 仿真的工程证据链。

当前已完成内容包括：

- CNN/NICE 加速器 RTL 基础设计与本地仿真验证。
- 自定义指令访问路径验证，包含 `CLEAR`、`WLOAD`、`DLOAD`、`COMP`、`RSTAT` 等指令流程。
- full-SoC SDK 仿真验证，当前基线结果为 `expected_rstat=19`。
- Davinci Pro A7-100T FPGA 板卡的 Vivado 构建、JTAG 识别、bitstream 下载流程。
- 板级时钟、复位、MMCM、ILA 调试链路验证。
- 当前 full SoC raw `sys_clk` ILA 诊断模式已能在板上观察 reset、PC activity 和总线活动。

当前有效代码基线：

- `riscv_cnn_accelerator`: `f75e04a6969ecbfd0fa2eb2b4055670a6785bc50`
- `e203_hbirdv2`: `3ea17fbbfba7f0ce600ea8c5500bdf7b7de418df`

## 三、十天总体目标

在十天内完成一个可用于毕业设计答辩的最小闭环成果，形成“设计、验证、板级运行、性能说明、论文与答辩材料”一致的证据链。

总体闭环目标为：

```text
hello_e203 板级运行证据
-> CNN/NICE 板级验证或 full-SoC 替代验证
-> 性能与准确率指标说明
-> 论文和答辩材料同步完成
```

优先目标是在 FPGA 板卡上完成 `hello_e203` 与 `cnn_accel_demo` 的运行验证，并通过 UART 或 ILA 采集运行证据。若板级 UART 或完整 CNN 板级运行仍受限，则以 full-SoC 仿真、板级 ILA 诊断和明确的问题定位作为答辩可解释的替代闭环。

## 四、具体任务安排

### 第 1 天：整理当前板级观测证据

任务：

- 固化 `soc_sysclk_ila` 当前板级 ILA 观测结果。
- 明确 PC、reset、UART、NICE、memory bus 等 probe 的实际含义。
- 形成下一步 CPU 启动诊断所需的 probe 列表。

输出：

- 当前板级证据说明文档。
- CPU 启动诊断信号列表。

验收标准：

- 能清楚说明当前板级 SoC 已经复位释放，并能观察到 CPU 侧活动。
- 不将 IFU PC activity 误表述为完整软件执行成功。

### 第 2 天：完成 CPU 启动诊断

任务：

- 构建 CPU boot diagnostic ILA。
- 观察 CPU 是否取指、是否停机、是否异常、是否仅 UART 无输出。
- 记录 reset、fetch、trap/halt、UART TX 等关键信号。

输出：

- CPU 启动诊断 bitstream。
- timing report。
- ILA capture CSV。
- CPU 当前状态判断。

验收标准：

- 能区分 CPU 未启动、取指异常、停机、复位问题或 UART 输出问题中的至少一种状态。

### 第 3 天：构建最小 `hello_e203` 程序

任务：

- 编写或整理最小 bare-metal `hello_e203` 程序。
- 生成 ELF、ITCM/DTCM preload 文件。
- 构建对应 FPGA bitstream。

输出：

- `hello_e203` 源码和 ELF。
- preload 文件。
- bitstream、`.ltx`、timing report。

验收标准：

- bitstream 构建成功。
- timing clean。
- 能确认 bitstream 使用的是目标 hello preload。

### 第 4 天：完成 `hello_e203` 板级验证

任务：

- 下载 hello bitstream 到 FPGA。
- 采集 UART 输出或无输出记录。
- 同步采集 ILA 证据。
- 判断 hello 是否成功运行。

输出：

- UART 截图或串口日志。
- ILA summary 和 CSV。
- hello 板级运行结论。

验收标准：

- 最优：UART 输出 hello 或阶段性启动信息。
- 最低可接受：ILA 能证明程序进入预期阶段，并说明 UART 未输出原因。

### 第 5 天：启动 CNN/NICE 板级验证

任务：

- 构建 `cnn_accel_demo` 板级镜像。
- 准备 NICE CSR、NICE handshake、memory bus、PC activity 等观测信号。
- 下载并采集第一组 CNN/NICE 板级证据。

输出：

- CNN demo bitstream。
- UART 或 ILA 运行证据。
- NICE 活动初步结论。

验收标准：

- 若 hello 已闭合，则进入 CNN/NICE 板级验证。
- 若 hello 未闭合，则形成明确 blocker 报告，不盲目切换到 CNN。

### 第 6 天：闭合 CNN/NICE 功能证据

任务：

- 尝试获取 CNN/NICE 板级运行结果。
- 对比软件期望结果和硬件加速结果。
- 若板级受阻，整理 full-SoC 仿真作为替代功能证据。

输出：

- CNN/NICE 功能验证记录。
- 板级证据或 full-SoC fallback 证据。

验收标准：

- 能证明 CNN/NICE 功能路径正确，或明确指出板级闭环受阻的具体环节。

### 第 7 天：整理性能指标

任务：

- 整理 CPU-only 与 accelerator 两种模式的 cycle/time 对比。
- 形成加速比表格。
- 判断是否能支撑“不低于 10 倍”的目标表述。

输出：

- 性能对比表。
- 指标来源说明。
- 答辩中的性能表述版本。

验收标准：

- 若达到 10 倍，给出证据来源。
- 若未达到或证据不足，给出诚实、可解释的阶段性结论。

### 第 8 天：整理准确率和模型范围

任务：

- 整理 INT8 量化、Python/C golden model、RTL、full-SoC 的一致性证据。
- 明确当前是否支持完整 MNIST/LeNet-5 准确率结论。
- 对原课题指标和当前完成证据进行对照。

输出：

- 准确率与模型范围说明。
- 课题要求 vs 当前证据对照表。

验收标准：

- 论文和答辩中不夸大 MNIST/LeNet-5 完整准确率。
- 能准确说明已验证的是完整应用、子集应用，还是 CNN kernel/NICE 功能路径。

### 第 9 天：同步论文材料

任务：

- 更新论文技术章节。
- 整理系统架构图、验证流程图、板级 bring-up 证据图、性能表和资源表。
- 建立结论与证据文件之间的映射。

输出：

- 论文主要章节草稿或章节笔记。
- 图表清单。
- 证据索引。

验收标准：

- 论文中的主要技术结论均能对应到代码、仿真、板级记录或报告。

### 第 10 天：完成答辩材料

任务：

- 更新最终答辩 PPT 主线。
- 编写讲稿和常见问题回答。
- 准备证据包。
- 形成最终风险与不足说明。

输出：

- 答辩 PPT 或 PPT 大纲。
- 讲稿。
- QA 文档。
- 证据包索引。

验收标准：

- 能完整讲清楚项目目标、设计方法、验证结果、板级进展、性能结论和不足。
- 答辩表述与实际证据一致。

## 五、最终交付物

十天结束时应形成以下交付物：

- 代码与工程：
  - 当前可复现代码基线。
  - FPGA bitstream 构建流程。
  - hello 或 CNN/NICE 板级验证工程。
- 实验与证据：
  - RTL/NICE 仿真结果。
  - full-SoC SDK 仿真结果。
  - FPGA 板级 JTAG/programming/ILA 证据。
  - hello 和 CNN/NICE 的板级或替代验证证据。
  - 性能、资源、准确率或模型范围说明。
- 文档与答辩：
  - 论文技术章节材料。
  - 最终 PPT。
  - 答辩讲稿。
  - 常见问题回答。
  - 证据索引。

## 六、风险与预案

### 风险 1：UART 无输出

预案：

- 使用 raw `sys_clk` ILA 继续观察 PC、reset、UART TX、GPIO、NICE handshake。
- 若 CPU 已运行但 UART 无输出，则将问题定位为 UART pinmux、波特率、板卡串口或软件初始化问题。

### 风险 2：CNN/NICE 无法在板上完整闭合

预案：

- 先保证 hello 程序闭合。
- 使用 full-SoC 仿真和 ILA NICE 活动作为功能替代证据。
- 答辩中明确区分“板级环境已闭合”和“完整 CNN 应用板级闭合”的完成边界。

### 风险 3：10 倍加速指标证据不足

预案：

- 使用同一工作负载的 CPU-only 和 accelerator cycle 进行对比。
- 若板级 cycle 不完整，则采用 full-SoC regression 或仿真 cycle 作为阶段性指标。
- 不无证据宣称最终性能指标，只给出当前可复现实验结论。

### 风险 4：MNIST/LeNet-5 准确率证据不足

预案：

- 明确当前验证范围是 INT8 kernel、CNN/NICE 数据路径、子集推理还是完整 MNIST。
- 若完整准确率无法闭合，则在论文中作为未完成指标或后续工作说明。

## 七、最终验收口径

本十天任务的验收目标不是盲目追求所有原始指标一次性完全达成，而是形成一个真实、可复现、可答辩的工程闭环。

最终验收分为三档：

### 最优闭环

- `hello_e203` 板上运行成功。
- `cnn_accel_demo` 板上运行成功。
- UART 和 ILA 证据完整。
- 性能和准确率指标有可复现实验支撑。

### 可答辩闭环

- 板上 raw-debug 能证明 SoC/CPU 运行状态。
- CNN/NICE 功能由 full-SoC 仿真和部分板级证据支撑。
- 性能、准确率和限制条件有清楚说明。
- 论文和答辩材料不夸大结果。

### 保底闭环

- 板级 blocker 被清楚定位。
- RTL、NICE、full-SoC 和板级调试链路证据完整。
- 能说明项目已完成的工程价值和后续改进路径。

## 八、汇报重点

向老师汇报时建议突出以下主线：

1. 本项目不是停留在单个 PE 或仿真模块，而是已经推进到 E203 SoC 和 FPGA 板级 bring-up。
2. 当前已证明 JTAG、programming、MMCM、reset、raw `sys_clk` ILA、full SoC raw-debug 观测链路可用。
3. 接下来十天的重点是从“能观测 SoC”推进到“能证明软件运行和 CNN/NICE 功能”。
4. 如果板级 UART 或 CNN 完整闭环受阻，将用可复现实验和明确问题定位形成可答辩闭环，避免无证据夸大。
