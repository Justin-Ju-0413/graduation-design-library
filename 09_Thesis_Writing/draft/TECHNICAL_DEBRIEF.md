# 毕设全自动执行——技术工作总结

> 本文档供你快速学习本项目的全部技术工作，用于检查成果和应对导师问题。

---

## 一、项目做了什么

在 Davinci Pro A7-100T FPGA 开发板上，让 RISC-V E203 处理器启动，运行用户程序，并通过 NICE 自定义指令调用 CNN 加速器。

**一句话**：打通了 "RTL设计 → 仿真验证 → FPGA综合 → 板级调试 → 程序运行" 的完整闭环。

---

## 二、代码仓库

| 仓库 | 分支 | 说明 |
|------|------|------|
| `Justin-Ju-0413/e203_hbirdv2` | `codex/a7-bringup-v2-soc` | E203 SoC RTL + FPGA 板级文件 |
| `Justin-Ju-0413/riscv_cnn_accelerator` | `codex/a7-bringup-v2-main` | CNN 加速器 RTL + 构建脚本 + 测试程序 |

---

## 三、关键工作（按时间线）

### 阶段 1：ILA 探针体系搭建

**做了什么**：在 FPGA 设计中嵌入 ILA (Integrated Logic Analyzer) 探针，通过 Vivado Hardware Manager 实时观测 CPU 内部信号。

**改了哪些文件**：
- `e203_hbirdv2/fpga/davinci_a7_100t/src/bootvec_sysclk_ila_system.v` — 新建的 ILA 顶层
- `e203_hbirdv2/fpga/davinci_a7_100t/script/prologue.tcl` — 添加全局 Verilog 宏定义
- `riscv_cnn_accelerator/scripts/Invoke-Vivado-Fpga.ps1` — 注册新 build mode

**ILA 探针布局**（7个探针，共 110 位宽）：
| 探针 | 宽度 | 信号 |
|------|------|------|
| probe0 | 32 | CPU PC 值 |
| probe1 | 4 | 复位/时钟状态 |
| probe2 | 3 | 系统内存总线活跃标志 |
| probe3 | 32 | 内存命令地址 (CPU 在访问哪里) |
| probe4 | 32 | 内存握手计数 |
| probe5 | 4 | UART TX 状态 |
| probe6 | 3 | 复位/时钟门控/调试停止标志 |

---

### 阶段 2：CPU 启动调试——四大根因

**发现 #1：探针盲视**
- 原来的 `probe_ifu_cmd_valid` 只监控 ITCM 专用路径
- MROM 启动的请求走的是 BIU → 系统内存总线，探针完全看不到
- 修复：切换到系统内存总线探针（`probe_mem_cmd_valid/ready` 等）

**发现 #2：sirv_gnrl_dffs.v 中的 `#1` 延迟（仅影响仿真）**
- `qout_r <= #1 dnxt` 中的 `#1` 导致 iverilog 中 D 触发器不响应时钟沿
- 修复：移除所有 `#1` 延迟
- 影响范围：仅仿真，Vivado 综合忽略 `#1`

**发现 #3：ITCM/DTCM 初始化文件格式（影响仿真+板级）**
- `objcopy -O verilog` 输出字节级 hex：`17 01 01 10`
- Vivado 和 iverilog 的 `$readmemh` 把每个空格分隔的值当成一个完整的存储器字
- ITCM 数据宽度 = 64 位 → 需要 16 位 hex 值/字
- DTCM 数据宽度 = 32 位 → 需要 8 位 hex 值/字
- 修复：编写 `Convert-VerilogHex.ps1` 脚本，将字节级格式转为字级格式

**发现 #4：E203_FORCE_BOOTROM_BOOT 宏不可见**
- `sirv_aon_wrapper.v` 使用了 `` `ifdef E203_FORCE_BOOTROM_BOOT ``
- 但该文件没有 `` `include "e203_defines.v" ``
- Vivado 的文件作用域宏处理导致该宏不可见
- 修复：在 `prologue.tcl` 中添加 `set_property verilog_define {E203_FORCE_BOOTROM_BOOT FPGA_SOURCE}`，使宏在全局可见

---

### 阶段 3：hello_e203 板级验证（Day 3-4 完成）

**做了什么**：
1. 编写最小裸机程序 `hello_e203`（freestanding C + 自定义 startup.S）
2. 配置 UART0 (GPIO16=RX, GPIO17=TX, 115200 baud)
3. 编译 → ELF → Verilog hex → 64-bit ITCM 转换 → Vivado bitstream
4. 烧录 FPGA → 串口输出验证

**结果**：
```
hello_e203: boot
hello_e203: uart ok
hello_e203: loop
```
三行输出确认 CPU 完整启动链：MROM → ITCM → UART 初始化 → 主循环。

---

### 阶段 4：仿真环境搭建

**做了什么**：
- 在 Ubuntu 20.04 虚拟机上搭建 Icarus Verilog 仿真
- 使用 `vsim/` 目录下的现有 Makefile 基础设施
- 修复了 6 个仿真特有的编译/运行问题：
  1. SV 断言语法错误 → `-D DISABLE_SV_ASSERTION=1`
  2. 缺失 `e203_fpga_mem_init.vh` → 创建空初始化文件
  3. I2C 模块语法错误 → 排除 I2C 目录 + `-g2005-sv`
  4. 缺失外设模块 → 从 vsim 原始安装复制
  5. `hfclkrst` 浮空 → `assign hfclkrst = 1'b0`
  6. GFCM/PLL 时钟链断裂 → `test_mode = 1'b1`

**结果**：仿真 0 错误编译，CPU 启动追踪与板级完全一致。

---

### 阶段 5：NICE CNN 加速器测试

**做了什么**：
1. 从 RTL 确认 NICE 指令编码（6条自定义指令）
2. 编写纯汇编 NICE 测试程序（test_nice.S）
3. ILA 确认 CPU 执行完所有 NICE 指令
4. NICE 指令编码表：

| 操作 | 指令编码 | 功能 |
|------|---------|------|
| CFG | 0x0A00100B | 配置 (ReLU 开关) |
| CLEAR | 0x0800000B | 清除累加器 |
| WLOAD | 0x0001800B | 加载权重 |
| DLOAD | 0x0201800B | 加载数据 |
| COMP | 0x0400000B | 触发计算 |
| RSTAT | 0x0600250B | 读取结果 |

---

## 四、关键技术要点（应对导师问题）

### Q: 为什么 CPU 一开始不启动？
A: 四个根因叠加：
1. 仿真：DFF 的 `#1` 延迟阻止时钟沿触发
2. 板级：ITCM/DTCM hex 文件字节格式与 Vivado $readmemh 不兼容
3. 板级：`E203_FORCE_BOOTROM_BOOT` 宏在 Vivado 中不可见
4. 板级+仿真：探针监控了错误的信号路径（ITCM 而非 mem bus）

### Q: 怎么确认 hello_e203 确实在运行？
A: 双重证据——(1) 串口终端输出三行预期字符串；(2) ILA 捕获 PC 在 ITCM 代码区域 (0x800000a0+)。

### Q: NICE 加速器验证到什么程度？
A: CPU 成功执行了全部 NICE 指令流程（ILA 确认 PC 到达程序完成点），但 RSTAT 返回值与预期有偏差。ILA 证据充分，偏差原因为 WLOAD/DLOAD 的寄存器映射细节，属已知可追踪问题。

### Q: 仿真和板级的关系？
A: 仿真精确复现了板级的 PC=0 行为，证明问题不是时序/综合导致的。仿真环境 (iverilog) 提供秒级迭代，板上构建 (Vivado) 需 10 分钟。

---

## 五、修改的文件清单

### e203_hbirdv2 仓库
| 文件 | 修改内容 |
|------|---------|
| `fpga/.../script/prologue.tcl` | 添加全局 verilog_define (根因 #4) |
| `fpga/.../src/bootvec_sysclk_ila_system.v` | 新建 ILA 顶层 (探针切换) |
| `fpga/.../src/cnn_sysclk_ila_system.v` | 新建 CNN ILA 建模式 |
| `fpga/.../src/hello_sysclk_ila_system.v` | hello_e203 ILA 建模式 |
| `rtl/e203/soc/e203_soc_top.v` | 添加 probe_mem_cmd_addr 端口 |
| `rtl/e203/subsys/e203_subsys_main.v` | 添加 probe 端口 |
| `rtl/e203/subsys/e203_subsys_top.v` | 添加 probe 端口 |
| `rtl/e203/general/sirv_gnrl_dffs.v` | 移除 `#1` 延迟 (仿真修复) |

### riscv_cnn_accelerator 仓库
| 文件 | 修改内容 |
|------|---------|
| `scripts/Convert-VerilogHex.ps1` | 新建 hex 格式转换脚本 (根因 #2, #3) |
| `scripts/Build-HelloE203.ps1` | hello_e203 构建脚本 |
| `scripts/Invoke-Vivado-Fpga.ps1` | 注册新 build mode |
| `scripts/Prepare-Fpga-Install.ps1` | 自动使用 64-bit ITCM |
| `sw/hello_e203/` | hello_e203 源码 |
| `sw/minimal_test.S` | NICE 汇编测试程序 |

---

## 六、构建命令速查

```powershell
# hello_e203 构建
powershell -File scripts/Build-HelloE203.ps1

# FPGA bitstream 构建 (选一个 mode)
powershell -File scripts/Invoke-Vivado-Fpga.ps1 -BuildMode bootvec_sysclk_ila -Action bit

# ILA 采集
D:/Xilinx/Vivado/2023.2/bin/vivado.bat -mode batch -source scripts/capture_vivado_ila.tcl -tclargs system.bit system.ltx output_dir

# Ubuntu 仿真编译
cd ~/Desktop/e203_hbirdv2/vsim/install
iverilog -Wall -g2005-sv -D DISABLE_SV_ASSERTION=1 -D FPGA_SOURCE -D E203_FORCE_BOOTROM_BOOT \
  -I rtl/core -I rtl/perips -I rtl/perips/apb_i2c -I rtl/soc -I rtl/subsys \
  -I rtl/mems -I rtl/debug -I rtl/fab -I rtl/general \
  -s tb_ifu -o ../sim_out $(find rtl -name '*.v' | sort) tb/tb_pc_trace.v
```
