# Day 4: E203 Boot Failure — Full Debug Analysis

Date: 2026-04-29

---

## 1. 问题现象

E203 CPU 在 FPGA 板卡和仿真中均表现为 **PC=0，不执行任何指令**。

板级 ILA 采集：PC=0x00000000/0x00000002，系统内存总线 34,000+ 次握手全部去往地址 0x0。

仿真：完全相同的 PC=0 行为。

---

## 2. 板级调试发现

### 2.1 探针路径错误 (关键发现 #1)

`probe_ifu_cmd_valid` 连接的是 `ifu2itcm_icb_cmd_valid`（IFU→ITCM 专用路径），而 MROM 启动请求走 **BIU→系统内存总线**。原来的 ILA 探针对启动流程完全盲视。

### 2.2 切换到系统内存总线探针

添加 `probe_mem_cmd_addr` 并修改 `bootvec_sysclk_ila_system.v` 的探针分配：

| 探针 | 变更 |
|------|------|
| probe3 (32-bit) | 从 pc_change_count 改为 `mem_cmd_addr` — 显示 CPU 实际请求的地址 |
| probe2 (3-bit) | 从 IFU ITCM liveness 改为 系统内存总线 liveness |
| probe4 (32-bit) | 从 IFU 计数改为 系统内存总线 handshake 计数 |

结果：**34,000+ 次握手，全部去往 0x00000000**（Debug Module 区域），从未访问 MROM (0x00001000)。

### 2.3 pc_rtvec 问题 (关键发现 #2)

`sirv_aon_wrapper.v` 没有 `include "e203_defines.v"`。即使在安装目录中定义了 `E203_FORCE_BOOTROM_BOOT`，Vivado 综合时该宏可能不可见。

修复：在 `prologue.tcl` 中添加全局 verilog_define，Synthesis log 确认为 "command line macro"。

### 2.4 板级现状

修复后板级 ILA 仍显示 PC=0。但由于使用 ALWAYS 触发模式，20us 捕获窗口只能看到稳态（可能是正确的 MROM→ITCM 启动后 trap 到 0x0 的死循环），无法确认启动序列是否正确。

---

## 3. 仿真环境搭建

### 3.1 基础设施

- **环境**: Ubuntu 20.04 VM (VMware, IP 192.168.10.128)
- **仿真器**: Icarus Verilog 12.0 (iverilog + vvp)
- **RTL 源**: `~/Desktop/e203_hbirdv2/vsim/install/rtl/` (从源 rtl/e203/ 复制)

### 3.2 编译修复链

| # | 问题 | 修复 | 文件 |
|---|------|------|------|
| 1 | `sirv_gnrl_dffs.v` SV 断言语法错误 | `-D DISABLE_SV_ASSERTION=1` | 编译参数 |
| 2 | `e203_fpga_mem_init.vh` 缺失 | 创建空 ITCM/DTCM 初始化文件 | vsim/install/rtl/core/ |
| 3 | I2C 模块语法错误 | `-D DISABLE_SV_ASSERTION=1` 无效 → 排除 I2C 目录 + 添加 `-g2005-sv` | 编译参数 |
| 4 | Periph 模块缺失 (sirv_ResetCatchAndSync 等) | 从 `vsim/install/rtl/perips/` 复制 | rtl/perips/ |
| 5 | **`hfclkrst` 浮空 — 无时钟生成** | `assign hfclkrst = 1'b0` | subsys/e203_subsys_top.v |
| 6 | **PLL 控制线浮空 — GFCM 不工作** | 赋值默认值 (pllbypass=1, pll_ASLEEP=0 等) | subsys/e203_subsys_main.v |
| 7 | **`test_mode=0` → GFCM 时钟链断裂** | `test_mode = 1'b1` (绕过 GFCM/PLL) | soc/e203_soc_top.v |
| 8 | `clk_aon` 循环依赖 (clk_ctrl↔reset_ctrl) | test_mode=1 打破循环 (clk_ctrl 直接从 rst_n 获得复位) | core/e203_cpu.v |

### 3.3 最终编译命令

```bash
cd ~/Desktop/e203_hbirdv2/vsim/install
iverilog -Wall -g2005-sv \
  -D DISABLE_SV_ASSERTION=1 -D FPGA_SOURCE -D E203_FORCE_BOOTROM_BOOT \
  -I rtl/core -I rtl/perips -I rtl/perips/apb_i2c -I rtl/soc -I rtl/subsys \
  -I rtl/mems -I rtl/debug -I rtl/fab -I rtl/general \
  -s tb_ifu -o ../sim_out \
  $(find rtl -name '*.v' | sort) tb/tb_ifu_final.v
```

**0 错误编译通过。**

---

## 4. IFU 内部探针

### 4.1 探头设计

在 `e203_ifu_ifetch.v` 中添加 `output [7:0] probe_ifu_state`，位分配：

| 位 | 信号 | 含义 |
|----|------|------|
| [7] | 0 (填充) | — |
| [6] | clk | IFU 模块的时钟输入 |
| [5] | rst_n | IFU 模块的复位输入 |
| [4] | reset_flag_r | DFFRS 输出 (复位标志) |
| [3] | ifu_reset_req | 复位请求标志 (= reset_req_r) |
| [2] | ifu_req_valid | IFU 请求有效 |
| [1] | ifu_req_hsked | IFU 请求握手完成 |
| [0] | ifu_req_valid_pre | IFU 请求有效预条件 |

### 4.2 层级传播

端口通过 6 层 RTL 层级传播：
```
e203_ifu_ifetch.v → e203_ifu.v → e203_core.v → e203_cpu.v → e203_cpu_top.v → e203_subsys_main.v → e203_subsys_top.v → e203_soc_top.v
```

每层使用 sed 命令统一添加。

---

## 5. 仿真结果分析

### 5.1 复位时序

在 test_mode=1 下，复位是直通的（无 PMU 延迟）：

```
T=0ns:       外部 rst_n=0, IFU rst_n=0
T=5us:       外部 rst_n=1, IFU rst_n=1 (即刻释放)
T=100us:     ext_rst=1, IFU probe = 0x70
T=200us:     ext_rst=1, IFU probe = 0x70 (无变化)
```

### 5.2 IFU 探针值解读

`ifu_raw = 0x70 = 0111_0000`：

| 位 | 值 | 含义 |
|----|-----|------|
| [6] clk | 1 (posedge) / 0 (negedge) | **时钟正常翻转** |
| [5] rst_n | 1 恒定 | **复位已释放** |
| [4] flag_r | 1 恒定 | **DFFRS 输出不翻转** |
| [3] reset_req | 0 恒定 | **未产生复位请求** |
| [2] req_v | 0 | IFU 不发送请求 |
| [1] hsked | 0 | 无握手完成 |
| [0] v_pre | 0 | 请求预条件为假 |

### 5.3 双沿采样验证

| 时钟沿 | IFU probe | clk bit[6] |
|--------|-----------|------------|
| posedge | 0x70 | **1** |
| negedge | 0x30 | **0** |

**确认 IFU clk 在翻转。** rst_n bit[5] 在两个沿都是 1（稳定）。

### 5.4 核心矛盾

- IFU clk 翻转 ✓
- IFU rst_n 已释放 ✓
- **DFFRS 不响应** (`flag_r` 卡在 1) ✗
- **所有 IFU 寄存器卡在复位值** ✗

`sirv_gnrl_dffrs` 单测通过（独立编译运行，flag_r 正确翻转为 0），但在完整 SoC 中不工作。

### 5.5 待验证假设

Probe 端口在层级传播中可能在某层接错了信号，导致：
- 读到的 `clk` 和 `rst_n` 不是实际输入到 DFFRS 的信号
- 真正的 `clk` 未到达 IFU 内部

**验证方法**: 直接在 `sirv_gnrl_dffrs` 实例端口上监控，或在 e203_ifu_ifetch.v 内部添加 `always @(posedge clk)` 进程确认时钟是否触发。

---

## 6. GitHub 仓库对比

### 6.1 分支

- `e203_hbirdv2`: `cnn_bringup_v1` (旧) vs `codex/a7-bringup-v2-soc` (当前)
- `riscv_cnn_accelerator`: `bringup_v1` (旧) vs `codex/a7-bringup-v2-main` (当前)

### 6.2 差异

核心 RTL (`e203_subsys_top.v`, `e203_subsys_main.v`, `e203_soc_top.v`, `e203_cpu.v`) 在两个分支中**基本相同**。

唯一差异：
1. V2 分支添加了 probe 调试信号 (probe_ifu_cmd_valid 等)
2. V2 分支添加了 `e203_fpga_mem_init.vh` include (ITCM/DTCM 内存初始化)
3. `hfclkrst`、PLL 线、`test_mode` 在两个分支中一致

**结论**: 当前 `codex/a7-bringup-v2-*` 分支的 RTL 改动不是引入启动失败的原因。

---

## 7. 参考资料扫描

### 7.1 BaiduNetdiskDownload

三个目录全部扫描——**无 RISC-V/E203/蜂鸟 材料**：
- A 盘：仅 FPGA 出厂测试 + 快速入门 PDF
- B 盘：仅 VS2015/WDK 等 Windows 工具
- PPT 课件：23 个 FPGA 基础教程 (LED/UART/HDMI/DDR3)

### 7.2 本地项目

- `C:\Users\16084\Documents\riscv_cnn_accelerator` — codex/a7-bringup-v2-main 分支，带 `hw/sim/Makefile` (CNN accelerator NICE 级仿真)
- `C:\Users\16084\Documents\New project\riscv_cnn_accelerator` — 同一分支，带 Vivado 脚本
- `C:\Users\16084\Documents\New project\e203_hbirdv2` — codex/a7-bringup-v2-soc 分支

---

## 8. 修复汇总

### 8.1 已应用到 vsim/install/ 的仿真修复

| 文件 | 修复 | 原因 |
|------|------|------|
| subsys/e203_subsys_top.v | `assign hfclkrst = 1'b0` | hfclkrst 浮空 → HCLKGEN 不产生时钟 |
| subsys/e203_subsys_main.v | PLL 线赋值 | pllbypass/pll_ASLEEP 等浮空 → GFCM 断裂 |
| soc/e203_soc_top.v | test_mode = 1'b1 | 绕过 GFCM/PLL 时钟链 |
| core/e203_fpga_mem_init.vh | 空 ITCM/DTCM | 避免 $readmemh 文件缺失 |
| perips/ | sirv_ResetCatchAndSync*.v 等 | 缺失模块补全 |
| general/sirv_sram_icb_ctrl.v | 恢复原文件 | 误删除 |

### 8.2 已应用到板级的修复

| 文件 | 修复 | 原因 |
|------|------|------|
| prologue.tcl | `set_property verilog_define {E203_FORCE_BOOTROM_BOOT FPGA_SOURCE}` | pc_rtvec 全局可见 |
| bootvec_sysclk_ila_system.v | 探针切换为系统内存总线监控 | 原来监控 ITCM 路径 (错的) |
| e203_soc_top/subsys_top/subsys_main.v | probe_mem_cmd_addr 端口 | 暴露内存命令地址 |

---

## 9. 下步计划

### 短期（验证探针连接正确性）

直接在 IFU 实例的 `clk` 和 `rst_n` 引脚上加 `$display` 监控，确认信号是否真的到达 DFFRS。

### 中期（如果 DFFRS 确实不触发）

- 检查 `e203_clk_ctrl` 生成的 `clk_core_ifu` 是否正确传递到 `e203_ifu.clk`
- 可能在 e203_cpu.v 的 `assign clk_aon = clk` 行有冲突（e203_clk_ctrl 也有 `assign clk_aon = clk`）
- 尝试用仿真 force 机制直接驱动 reset_flag_r

### 长期

- 找一份已知能正常仿真启动的 E203 参考工程对比
- 检查 Nuclei 官方是否有 E203 FPGA 仿真 testbench
