# Final Defense English Script With Chinese Explanation

Use the English paragraph as the speaking script. The Chinese explanation gives the same point in defense-oriented language.

## Slide 1. RISC-V Custom-Instruction CNN Accelerator

**English script**

Good morning, professors and classmates. This work presents a RISC-V custom-instruction CNN accelerator. The goal is not only to design a small CNN computing block, but also to connect it to a real RISC-V E203 soft-core and test the complete path on FPGA. The presentation covers the motivation, system design, instruction interface, verification flow, board results, and main limitations.

**中文解释**

本项目不是单独完成一个 RTL 计算模块，而是将 CNN 加速器接入 E203 RISC-V 软核，并在 FPGA 上完成从软件调用到硬件结果的验证闭环。

## Slide 2. Presentation Outline

**English script**

This presentation is organized in four parts. The first part introduces the motivation and design objective. The second part explains the system architecture and the custom instruction interface. The third part describes the accelerator microarchitecture and verification strategy. The final part presents the FPGA validation results, limitations, and future work.

**中文解释**

汇报结构包括项目动机、系统与指令接口设计、加速器与验证方法、FPGA 结果以及后续改进方向。

## Slide 3. Problem and Design Goal

**English script**

The motivation comes from running AI on edge devices. CNN convolution contains many repeated MAC operations, meaning multiply and accumulate. These operations are slow on a small embedded processor. RISC-V is suitable for this topic because its open instruction set allows custom instructions. The design objective is to build a small accelerator that the CPU can control directly through custom instructions, and to prove it with a repeatable FPGA prototype.

**中文解释**

选择 RISC-V 自定义指令的原因是边缘端 CNN 卷积计算量较大，而 RISC-V 开放指令集支持面向特定任务的扩展。

## Slide 4. System Architecture

**English script**

At the system level, the host processor is the E203 Hummingbird v2 core. The SoC includes ITCM, DTCM, UART, GPIO, and the CNN accelerator. A key design decision is to connect the accelerator through the NICE custom-instruction interface. Compared with a memory-mapped peripheral, NICE avoids extra bus control logic for accelerator commands. The software sends input values through rs1 and rs2, and reads the result through a CPU register.

**中文解释**

讲结构时强调：不是 MMIO 外设，而是 NICE 协处理器路径。数据通过寄存器操作数传递，结果回写寄存器，这样控制路径短，软件调用也清楚。

## Slide 5. Custom Instruction Interface

**English script**

The software interface is built from six custom instructions. CLEAR resets the internal state. WLOAD loads packed weights, and DLOAD loads packed activation values. Each 32-bit input contains four signed INT8 values. COMP starts the multiply-accumulate calculation, and RSTAT reads the final INT32 result. CFG is used for options such as ReLU. This instruction set is small, but it is enough for the convolution operation used in the demo.

**中文解释**

六条自定义指令构成软件控制模型：CLEAR 清除状态，WLOAD 和 DLOAD 加载权重与输入，COMP 启动计算，RSTAT 读取结果，CFG 配置 ReLU 等选项。

## Slide 6. Accelerator Microarchitecture

**English script**

Inside the accelerator, the computing engine is a 4 by 4 PE array. Each PE multiplies one signed 8-bit weight and one signed 8-bit activation value, and adds the result into a 32-bit register. The design keeps partial sums inside the PEs; this is called output-stationary dataflow. The weights are sent by columns, and the activation values are sent by rows. The array is intentionally small, so it can fit together with the E203 SoC on the Artix-7 FPGA.

**中文解释**

硬件计算核心是 4x4 PE 阵列，共 16 个处理单元。每个 PE 执行 INT8 乘法和 INT32 累加，规模较小但足以验证自定义指令加速卷积路径。

## Slide 7. Verification Strategy

**English script**

The verification strategy is one of the important parts of this project. The validation does not rely on only one final board demo. Instead, it uses a step-by-step evidence chain. First, the accelerator RTL was tested with a simple NICE-like test interface. Second, the complete E203 SoC was simulated with the accelerator. Third, the hello_e203 program tested the boot path on the FPGA. Finally, the CNN demo tested the NICE instruction path and accelerator output on the board.

**中文解释**

这里强调工程可信度：不是只放一个结果截图，而是 RTL 仿真、SoC 仿真、hello_e203 板级启动、CNN 板级回归逐层闭环。

## Slide 8. Evidence Map

**English script**

Before moving into the board screenshots, this slide summarizes how the claims are supported. The SoC integration claim is supported by the architecture and full-SoC simulation. The boot claim is supported by hello_e203 UART output and the ILA PC trace. The NICE path claim is supported by custom-instruction tests and ILA captures. The convolution correctness and speedup claims are supported by the CNN UART output and the cycle comparison. Resource feasibility is supported by the Vivado utilization report.

**中文解释**

本页将核心结论与证据一一对应，避免只展示结果截图。证据来源包括 SoC 仿真、ILA、UART、cycle 对比和 Vivado 报告。

## Slide 9. Implementation Flow

**English script**

This slide shows the implementation flow. The hardware RTL, bare-metal firmware, E203 SoC integration, Vivado implementation, and FPGA board validation were treated as one connected process. This is important because a custom-instruction accelerator is not useful as an isolated module. It must be callable from software, connected through the processor interface, implemented on the FPGA, and checked with board-level output.

**中文解释**

本页把重点从调试细节转向完整实现流程：RTL、固件、SoC 集成、Vivado 实现和 FPGA 验证共同构成原型闭环。

## Slide 10. FPGA Prototype Validation

**English script**

After the design was implemented on FPGA, the first validation target was the E203 boot path. The hello_e203 program printed boot, uart ok, and loop through UART. The ILA capture also showed that the CPU reached the ITCM code region and that UART activity was present. This confirms that the processor, memory initialization, clocking, reset, and UART path were working together on the board.

**中文解释**

本页聚焦板级原型是否真正启动，而不是展开调试细节。UART 和 ILA 共同证明 E203 系统在 FPGA 上能够运行。

## Slide 11. NICE Instruction Path Evidence

**English script**

This slide focuses on the CPU-to-accelerator execution path. The firmware controls the accelerator through the six NICE instructions: CLEAR, WLOAD, DLOAD, COMP, and RSTAT. ILA gives signal-level context that the board is executing in the expected firmware region, while UART gives the final software-visible output comparison. Together, they show that the accelerator is integrated into the processor-controlled execution flow.

**中文解释**

本页重心放在 NICE 指令路径是否连通：软件发指令、加速器执行、结果由 UART 对比确认。

## Slide 12. Correctness Evidence Breakdown

**English script**

This slide breaks down the UART evidence into a simple comparison. The software reference, hardware accelerator output, and expected output are all 12, 23, 0, and 19. This supports the correctness claim for the reduced convolution test. The same run reports 1,516 CPU cycles and 287 accelerator cycles, so the measured speedup is 5.282 times. This speedup is for the convolution kernel only, not for the complete LeNet-5 inference.

**中文解释**

本页把 CNN UART 截图转成表格证据，强调 SW/HW/Expected 三者一致；同时限定 5.282x 是 convolution-only speedup。

## Slide 13. Board Result: CNN Board Test

**English script**

The first CNN board result is a reduced convolution test. It uses a 3 by 3 INT8 convolution on a 4 by 4 input. The UART log shows that the software reference, the hardware accelerator output, and the expected output all match: 12, 23, 0, and 19. For this convolution kernel, the CPU reference took 1,516 cycles, while the accelerator took 287 cycles. This gives a measured speedup of 5.282 times.

**中文解释**

这是最重要的数据页之一。要准确说：3x3 INT8 卷积，4x4 输入，输出 12/23/0/19，CPU 1516 cycles，加速器 287 cycles，5.282x。

## Slide 14. Board Result: LeNet-5 Inference

**English script**

To go beyond a small convolution kernel, a LeNet-5 inference program was also deployed. The convolution layers use the NICE accelerator path, while the fully connected layers still run in software. During testing, the Conv2 ReLU position was corrected, so ReLU is applied after all input channels are added together. The UART divisor was also corrected for 115200 baud. The recorded UART output shows that all 10 sampled MNIST images were classified correctly. This is not a full MNIST accuracy test, but it shows that the end-to-end FPGA demo works correctly.

**中文解释**

LeNet-5 结果表示 10 张采样 MNIST 图像均分类正确，并不等同于完整 MNIST 测试集准确率。测试过程中还修正了 Conv2 ReLU 位置和 UART divisor；卷积层使用 NICE 加速，全连接层仍由软件执行。

## Slide 15. Performance and Resource Summary

**English script**

The measured convolution speedup is 5.282 times, which meets the project target of at least 5 times for convolution. The FPGA design also met timing requirements. In the debug builds, WNS, or worst negative slack, stayed above 12 nanoseconds. Resource usage is also low enough for this board: about 20.8 percent LUT, 10.1 percent flip-flop, 26.3 percent BRAM, and no DSP blocks in the reported design. This means the complete E203 SoC with the CNN accelerator fits comfortably on the A7-100T device.

**中文解释**

性能与资源结果显示，卷积加速比为 5.282x，达到至少 5x 的目标；设计满足时序要求，资源利用率约为 LUT 20.8%、FF 10.1%、BRAM 26.3%、DSP 0%，A7-100T 仍有资源余量。

## Slide 16. Limitations and Future Work

**English script**

There are also clear limitations. The current accelerator is small, and reading results through RSTAT adds overhead when larger convolutions are split into tiles. In the LeNet-5 demo, the fully connected layers still run in software and take most of the end-to-end runtime, which is about two to five minutes per image in the current design. Future work will focus on improving the readback path, accelerating the fully connected layers, testing a larger MNIST subset, and exploring a larger or pipelined PE array. Overall, this project demonstrates a complete and testable FPGA prototype of a RISC-V custom-instruction CNN accelerator.

**中文解释**

最后要主动承认限制：不是完美高性能芯片，而是完整可验证原型。当前端到端约 2-5 分钟每张图，主要被软件 FC 层限制。未来工作包括 RSTAT 优化、FC 层加速、更大测试集、更大/流水 PE 阵列。
