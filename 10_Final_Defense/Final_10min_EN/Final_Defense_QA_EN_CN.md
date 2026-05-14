# Final Defense QA Bank

These answers are written for oral defense: short, factual, and careful about limitations.

## Q1. Why did you use NICE custom instructions instead of memory-mapped registers?

**Answer:** NICE connects the accelerator directly to the processor instruction path. The CPU can control the accelerator using instructions, and pass values through registers. This avoids extra bus control logic for accelerator commands. For this small accelerator, it makes both the hardware and the software interface simpler.

**中文要点：** 因为 NICE 是指令级接口，控制路径短，软件直接发自定义指令，不需要做 MMIO 地址译码和总线仲裁。

## Q2. What further conclusion did you learn from the LeNet-5 debugging?

**Answer:** The main lesson is that accelerator correctness is not only about the hardware MAC result. The software schedule also matters. At first, ReLU was applied too early inside Conv2 for each input channel, causing information loss. After correction, ReLU was moved after all channels were added together, and the 10-image board demo reached 10/10.

**中文要点：** 进一步结论：硬件 MAC 对了还不够，软件调度和非线性位置也会影响网络正确性。Conv2 ReLU 必须在多通道累加之后做。

## Q3. What is the main contribution of the project?

**Answer:** The contribution is the complete prototype and evidence chain: a 4x4 INT8 CNN accelerator, a six-instruction NICE programming model, integration with E203, RTL and full-SoC simulation, FPGA bring-up, and board results showing matching hardware and software output plus 5.282x convolution speedup.

**中文要点：** 贡献不是单个模块，而是设计、集成、验证、上板、调试证据链完整闭环。

## Q4. Does 10/10 MNIST mean the model reaches 100% accuracy?

**Answer:** No. It means the recorded board demo correctly classified 10 sampled images. It shows that the full demo path works correctly, but it is not a full MNIST accuracy test. A larger test subset is future work.

**中文要点：** 一定要避免夸大。10/10 是演示样本正确，不代表完整数据集 100%。

## Q5. Why is the end-to-end LeNet-5 runtime still long?

**Answer:** Only the convolution path is accelerated in the current prototype. The fully connected layers still run in software and contain about 50,000 MAC operations per image at 16 MHz, so they take most of the total runtime.

**中文要点：** 当前只加速卷积，FC 层软件跑，而且 16 MHz 下 FC 计算量大，所以端到端慢。

## Q6. What was the hardest debugging issue?

**Answer:** The board appeared stuck near PC=0. The root causes were not one single RTL bug, but several integration issues: memory hex packing for ITCM and DTCM, macro visibility in Vivado synthesis, and correct ILA probe placement. Matching the simulation behavior with the board behavior was essential for fast debugging.

**中文要点：** 最难的是上板启动链路，不是 CNN 算法本身。要强调用 ILA 和仿真相关性定位问题。

## Q7. How do you know the accelerator result is correct?

**Answer:** Correctness was checked at several levels. RTL simulation verified known RSTAT results. Full-SoC simulation checked the CPU-to-accelerator connection. On FPGA, the UART log shows the hardware output exactly matches both the CPU reference and the expected values.

**中文要点：** 正确性来自多级验证：RTL、SoC、FPGA UART，硬件结果和软件参考及期望值一致。

## Q8. What does the rs2 bug tell us?

**Answer:** It shows that custom instruction integration can be affected by hidden processor assumptions. The E203 decoder treated rs2=x0 as no rs2 value needed, while the NICE instruction used rs2 as a vector index. The fix was to make NICE instructions always capture rs2 when required.

**中文要点：** rs2 bug 说明处理器原有译码假设和自定义指令语义可能冲突。这里 rs2 既是寄存器字段，又被用作向量索引。

## Q9. Why is the PE array only 4x4?

**Answer:** The project prioritizes a complete and easy-to-debug FPGA prototype. A 4x4 array is small enough to integrate with the E203 SoC and easy to test, while still showing real custom-instruction acceleration. Larger arrays are a natural future extension.

**中文要点：** 4x4 是工程取舍：小、可集成、可验证，先证明路径，再扩展规模。

## Q10. What would you improve first if you had more time?

**Answer:** The first priority would be to accelerate the fully connected layers or reduce their cost, because they take most of the current LeNet-5 runtime. After that, RSTAT readback should be optimized and a larger image subset should be tested.

**中文要点：** 优先 FC 层加速，因为它决定端到端时间；然后优化 RSTAT 和扩大测试集。

## Q11. What tools and platform did you use?

**Answer:** The project used Icarus Verilog for RTL simulation, the E203 full-SoC simulation flow, Xilinx Vivado 2023.2 for synthesis and implementation, and the Davinci Pro A7-100T board with UART and ILA evidence for FPGA validation.

**中文要点：** 工具链：Icarus Verilog、E203 SoC 仿真、Vivado 2023.2、Davinci Pro A7-100T、UART/ILA。

## Q12. Is your verification evidence sufficient without the Hummingbird Debugger?

**Answer:** Yes. The project does not depend on one specific debugger. I used RTL simulation, full-SoC simulation, UART logs, and ILA captures. This covers module behavior, SoC integration, FPGA boot, internal hardware activity, and application-level output.

**中文要点：** 是足够的。项目不是验证 debugger 本身，而是验证加速器路径。RTL、SoC 仿真、UART 和 ILA 已覆盖模块、集成、启动、内部信号和应用输出。

## Q13. Can ILA replace the Hummingbird Debugger in this project?

**Answer:** ILA cannot replace all interactive CPU debugging functions, such as single stepping or reading CPU registers directly. However, for this project, ILA was sufficient for signal-level FPGA debugging, including PC behavior, memory access, UART activity, NICE handshake, and accelerator state.

**中文要点：** ILA 不能完全替代单步调试和寄存器读取，但足够完成本项目需要的 FPGA 信号级调试。

## Q14. Why do you think this is not a shortcut or opportunistic development?

**Answer:** The work follows a standard FPGA prototype validation flow: RTL simulation, SoC simulation, FPGA bring-up, ILA observation, UART result checking, and performance/resource measurement. The claims are limited to what these results support.

**中文要点：** 这不是投机取巧，而是标准 FPGA 原型验证流程。结论也限定在已有证据范围内。

## Q15. Why did you not add more algorithm accuracy charts?

**Answer:** This is not mainly an algorithm training project. The main contribution is hardware integration and FPGA validation, so the most relevant evidence is architecture, instruction behavior, ILA traces, UART correctness, cycle comparison, and resource usage.

**中文要点：** 项目重点不是训练算法，而是硬件集成和 FPGA 验证，所以证据重点不是 loss/accuracy 曲线。

## Q16. What is the strongest evidence that the system really runs on FPGA?

**Answer:** The strongest evidence is the combination of UART output and ILA captures. UART shows software-visible results, while ILA confirms internal FPGA behavior such as PC execution, memory activity, and NICE-related signal activity.

**中文要点：** 最强证据是 UART 和 ILA 结合：UART 证明外部可见结果，ILA 证明 FPGA 内部运行状态。

## Q17. What does the verification chain prove?

**Answer:** It proves that the result is not from a single isolated demo. RTL simulation checks the accelerator logic, SoC simulation checks integration, hello_e203 checks boot, and CNN and LeNet tests check board-level functionality.

**中文要点：** 验证链证明结果不是孤立截图，而是从模块到系统再到板级逐层验证。

## Q18. What does the 5.282x speedup actually mean?

**Answer:** It means the tested convolution kernel ran 5.282 times faster on the accelerator than on the CPU reference. It is not the end-to-end LeNet-5 speedup.

**中文要点：** 5.282x 是卷积核测试加速比，不是完整 LeNet-5 端到端加速比。

## Q19. Why is the LeNet-5 demo still meaningful if it is slow?

**Answer:** The LeNet-5 demo is mainly an end-to-end correctness demonstration. It shows that the CNN firmware, NICE instruction path, accelerator, and UART output can work together on FPGA. Performance optimization is future work.

**中文要点：** LeNet-5 主要证明端到端功能正确，不是当前阶段的性能最优结果。

## Q20. Why do fully connected layers still run in software?

**Answer:** The current accelerator focuses on convolution, because convolution is the main target for the custom instruction path. Fully connected acceleration would require additional data movement and control design, so it is left as future work.

**中文要点：** 当前优先验证卷积加速路径，FC 加速需要额外数据搬运和控制设计，因此作为后续工作。

## Q21. What is the main limitation of using RSTAT for result readback?

**Answer:** RSTAT is simple and easy to verify, but when larger convolution workloads are split into many tiles, reading each result through a custom instruction can add overhead. A more efficient readback path would improve scalability.

**中文要点：** RSTAT 简单可验证，但多 tile 场景下逐个读回会增加开销，扩展性有限。

## Q22. Why did you choose INT8 data?

**Answer:** INT8 reduces storage and computation cost, which fits the goal of a lightweight FPGA prototype. It also matches common quantized CNN inference practice.

**中文要点：** INT8 降低存储和计算开销，符合轻量化 FPGA 原型目标，也符合量化 CNN 推理常见做法。

## Q23. Why does the design use no DSP blocks in the reported implementation?

**Answer:** The reported implementation maps the small INT8 MAC structure without using DSP blocks. This leaves DSP resources available for future scaling or more optimized arithmetic designs.

**中文要点：** 当前小规模 INT8 MAC 未使用 DSP，后续扩大阵列或优化乘法结构时仍有 DSP 余量。

## Q24. How do you know the NICE instructions are correctly connected to E203?

**Answer:** The connection is supported by full-SoC simulation and FPGA tests. The CPU executes custom instructions, the accelerator receives the command and operands, and UART output confirms that the returned results match the software reference.

**中文要点：** SoC 仿真和 FPGA 测试共同证明 NICE 连接正确，CPU 指令能到达加速器，结果能返回并匹配软件参考。

## Q25. What was the value of reproducing FPGA behavior in simulation?

**Answer:** It made debugging much faster. FPGA builds take much longer, while simulation can be repeated quickly. Reproducing the PC=0 issue in simulation helped identify memory initialization and macro-visibility problems.

**中文要点：** 仿真复现板级问题能大幅加快定位，尤其是 PC=0、存储器初始化和宏可见性问题。

## Q26. Why is the rs2 issue important?

**Answer:** It shows that custom instruction design must consider existing processor decode assumptions. In this case, rs2 was used as an index, but E203 treated rs2=x0 as unnecessary. Fixing this was essential for correct WLOAD and DLOAD behavior.

**中文要点：** rs2 问题说明自定义指令不能只看加速器，还要理解处理器译码假设。

## Q27. What would happen if the rs2 issue was not fixed?

**Answer:** Some vector-bank index values, especially index 0, could be missed or stale. Then WLOAD or DLOAD might load data into the wrong bank, causing incorrect accelerator results.

**中文要点：** 如果不修复，index 0 可能无法正确捕获，导致权重或输入加载错误，最终结果错误。

## Q28. Why is the 4x4 PE array still valuable if it is small?

**Answer:** The goal is not to build the largest accelerator, but to prove the complete custom-instruction acceleration path. A 4x4 array is small enough to integrate and debug, while still demonstrating real hardware acceleration.

**中文要点：** 4x4 的价值在于证明完整路径，而不是追求最大规模。

## Q29. What evidence supports resource feasibility?

**Answer:** Vivado utilization reports show that the complete E203 SoC with the CNN accelerator fits on the A7-100T device, with about 20.8% LUT, 10.1% FF, 26.3% BRAM, and 0% DSP usage.

**中文要点：** 资源报告证明完整 SoC 和加速器能放入 A7-100T，资源仍有余量。

## Q30. What evidence supports timing feasibility?

**Answer:** The implementation met timing requirements. The debug builds reported positive slack, with WNS above 12 ns, showing that the design can run at the target FPGA clock in the tested configuration.

**中文要点：** 时序报告显示 WNS 大于 12 ns，说明当前测试配置下时序可收敛。

## Q31. What is the next most convincing experiment to add?

**Answer:** The next most convincing experiment would be a larger MNIST subset test and more detailed cycle breakdown for convolution, data loading, COMP, and RSTAT. This would strengthen both correctness and performance analysis.

**中文要点：** 最值得补的是更大 MNIST 子集测试，以及卷积各阶段 cycle breakdown，用来增强正确性和性能分析。
