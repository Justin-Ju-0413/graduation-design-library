# FYP Report Execution Plan — 基于 RISC-V 自定义指令的 CNN 加速器 FPGA 原型验证

## 关键约束

| 要求 | 状态 |
|------|------|
| ≥40页 (不含附录) | ⚠️ 硬性要求 |
| 查重 <24% | ⚠️ 关键 |
| Oral Presentation | 5月1-17日 |
| Demonstration (可展示诊断过程) | 进行中 |

## 论文结构 (对标 Report Rubric)

### 第一章 Introduction (~5页)
- 1.1 CNN推理加速背景
- 1.2 RISC-V自定义指令优势
- 1.3 课题目标：设计NICE CNN加速器并在FPGA原型验证
- 1.4 论文结构

### 第二章 Background (~8页)
- 2.1 RISC-V ISA与自定义指令扩展机制
- 2.2 E203蜂鸟处理器架构 (2-stage pipeline, NICE接口)
- 2.3 CNN基础 (卷积、矩阵乘法、量化INT8)
- 2.4 FPGA原型验证方法论 (ILA、JTAG、bring-up流程)

### 第三章 Methodology (~10页)
- 3.1 系统架构总览 (RISC-V SoC + CNN Accelerator)
- 3.2 NICE自定义指令设计 (CLEAR/WLOAD/DLOAD/COMP/RSTAT/CGF)
- 3.3 PE阵列设计 (4×4 systolic array)
- 3.4 SoC集成 (E203 + NICE + ITCM/DTCM + UART + GPIO)
- 3.5 FPGA板级bring-up方法 (Davinci Pro A7-100T, Vivado, ILA)

### 第四章 Results (~12页)
- 4.1 RTL仿真验证 (iverilog, full-SoC RSTAT=19)
- 4.2 FPGA bitstream构建 (timing closure, WNS/WHS)
- 4.3 hello_e203板级验证 (UART三阶段输出, ILA PC追踪)
- 4.4 CPU启动调试与根因分析 (四个根因：sirv_gnrl_dffs #1延迟、ITCM/DTCM 64/32-bit格式、pc_rtvec全局可见性)
- 4.5 NICE CNN加速器板级测试 (ILA确认NICE指令执行、RSTAT结果)

### 第五章 Discussion (~3页)
- 5.1 板级验证的挑战与解决
- 5.2 当前限制 (UART在CNN程序中的问题, RSTAT结果分析)
- 5.3 与课题目标的对比

### 第六章 Conclusion (~2页)
- 6.1 主要贡献
- 6.2 未来工作 (完整CNN应用、性能优化、MNIST准确率)

## 已有证据包

| 章节 | 证据 | 路径 |
|------|------|------|
| 4.3 | hello_e203 UART输出 | hello_e203_board_artifacts/uart_output.txt |
| 4.3 | hello_e203 ILA CSV | bootvec_sysclk_ila_ila_capture/ila_capture.csv |
| 4.4 | 根因分析文档 | DAY4_BOOT_DEBUG_FULL_ANALYSIS_2026_04_29.md |
| 4.4 | 仿真trace | Ubuntu sim outputs |
| 4.5 | NICE ILA捕获 | bootvec_sysclk_ila_ila_capture/ |
| 3.3 | RTL源码 | e203_hbirdv2, riscv_cnn_accelerator repos |
| 4.1 | 全SoC仿真基线 | RSTAT=19 regression |

## 执行优先级

### 今天紧急
1. ✅ **写Abstract** (6要素: 背景/问题/动机/方法/结果/结论)
2. ⬜ **写Introduction + Background草稿** (可基于已有README/文档)
3. ⬜ **整理Results章节** (已有全部实验数据, 只需组织)

### 明天
4. ⬜ 完成Methodology (基于RTL代码和设计文档)
5. ⬜ 完成Discussion + Conclusion

### 后天
6. ⬜ 格式排版 (页码、目录、图表标注)
7. ⬜ 查重检查
8. ⬜ PPT初稿
