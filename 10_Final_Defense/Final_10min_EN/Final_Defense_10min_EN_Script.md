# Final Defense 10-Minute English Script

Suggested pacing: 18 slides, about 12:20-12:40 total with normal explanation pauses, leaving a short buffer within a 13-minute defense. English is the main speaking script.

## Slide 1. RISC-V Custom Instruction Based Lightweight CNN Accelerator FPGA Prototype Validation

Suggested time: 0:10-0:15

Good morning, everyone. My project is RISC-V Custom-Instruction CNN Accelerator on FPGA.

## Slide 2. Presentation Outline

Suggested time: 0:30

I will present this project in three main parts. First, I will explain the motivation and project scope, so the target of the work is clear. Then I will introduce the system architecture and accelerator design. Finally, I will show the verification evidence and board results, including the CNN correctness test, the LeNet-5 sampled demo, the resource summary, and the limitations.

## Slide 3. Motivation and Objective

Suggested time: 0:08

I will first introduce the motivation of this project and define its scope.

## Slide 4. Problem and Design Goal

Suggested time: 0:50

The problem I focus on is CNN convolution on a small embedded CPU. Convolution has many repeated multiply-accumulate operations, so running it only in software is not efficient, especially for edge devices with limited resources. RISC-V is useful here because it allows custom instructions. In this project, I use the NICE interface to connect a lightweight CNN accelerator to the E203 core. The goal is not to build a large ASIC-style accelerator, but to build a compact FPGA prototype and prove it step by step: first in RTL simulation, then in full SoC simulation, and finally on the FPGA board.

## Slide 5. Project Scope and Deliverables

Suggested time: 0:50

This slide defines the scope I actually implemented. The project includes a 4 by 4 INT8 systolic PE array, six custom NICE instructions, integration with the Hummingbird E203 SoC, and validation on the Davinci Pro A7-100T FPGA board. The final deliverable is a repeatable FPGA prototype with evidence from RTL simulation, full-SoC simulation, and board testing. In the LeNet-5 demo, the convolution layers use NICE acceleration, while the rest of the program runs on E203 software.

## Slide 6. System Architecture

Suggested time: 0:55

At the system level, the accelerator is connected to the E203 instruction path through NICE. This is different from a memory-mapped peripheral. The SoC includes the E203 RV32IMAC core, ITCM, DTCM, UART0, GPIO, and the CNN accelerator. Software sends operands through custom instructions, and the result returns through the processor register path. So from the software point of view, the accelerator is controlled like part of the instruction execution flow, not like a separate device with an address range. This keeps the control path simple and matches the custom-instruction goal of the project.

## Slide 7. Accelerator Microarchitecture

Suggested time: 0:55

The accelerator core is a 4 by 4 PE array, so there are sixteen processing elements. Each PE performs signed INT8 multiplication and accumulates into an INT32 value. Weights are loaded by columns, and activation values are loaded by rows, which matches the packing of four INT8 values into one 32-bit operand. After the data is loaded, the computation produces partial sums, and a tree adder generates the final output. I chose this structure because it is small enough for the FPGA prototype, but it still demonstrates clear parallel acceleration compared with running the convolution completely on the CPU.

## Slide 8. Verification Evidence and Results

Suggested time: 0:08

Next, I will show the verification evidence and the measured board results.

## Slide 9. Why These Design Choices?

Suggested time: 0:55

These choices were made mainly for a lightweight FPGA prototype. A 4 by 4 PE array gives some parallelism but still fits easily on the A7-100T device, so it is suitable for a graduation project prototype. INT8 data is commonly used in small edge inference and also lets four 8-bit values fit into one 32-bit NICE operand, which reduces the number of load instructions. The output-stationary dataflow keeps partial sums local in the PEs and avoids unnecessary movement for this small convolution case. Using NICE avoids adding a memory-mapped bus interface and keeps the accelerator controlled directly by instructions.

## Slide 10. Implementation Flow

Suggested time: 0:45

The implementation was checked step by step instead of only testing the final board result. First, RTL tests were used to verify PE loading, COMP, and RSTAT behavior, because these are the basic operations of the accelerator. Then full-SoC simulation checked that the E203 core and the NICE accelerator worked together through the intended instruction path. After that, Vivado 2023.2 was used to build the FPGA prototype for the Davinci Pro A7-100T board. The final validation used UART output for software-visible results and ILA observation for signal-level context.

## Slide 11. FPGA Prototype Validation

Suggested time: 0:45

Before testing the accelerator result, I first confirmed that the FPGA prototype could boot and run firmware. The hello_e203 program printed boot, uart ok, and loop through UART. The ILA capture also showed that the CPU was executing in the ITCM code region. This result is basic, but it is important because if this part does not work, the accelerator result would not be meaningful. It proves that the CPU, memory initialization, clock, reset, and UART path were working together on the real FPGA board.

## Slide 12. NICE Instruction Path Evidence

Suggested time: 0:45

This slide explains how firmware reaches the accelerator. The program issues CLEAR, WLOAD, DLOAD, COMP, and RSTAT as NICE custom instructions. These instructions cover clearing the accelerator state, loading weights and input data, starting computation, and reading back the result. So the accelerator is not only an isolated RTL module; it is called by software through the E203 instruction path, performs the computation, and returns a value that the CPU can read. This is the main connection between the hardware design and the board-level software result.

## Slide 13. NICE Instruction Path Evidence: ILA Capture

Suggested time: 0:35

This page provides the ILA evidence for the same execution path. I do not need to explain every signal in the waveform, because the purpose here is not a waveform tutorial. The important point is that the board run was active and the processor was executing the expected firmware region. Together with the UART output, this supports that the result came from the actual FPGA execution flow, not only from a separate simulation or a software-only test.

## Slide 14. Board Result: CNN Correctness and Speedup

Suggested time: 0:55

This is the main reduced-CNN board result. The test is a 3 by 3 INT8 convolution over a 4 by 4 input. The software reference, the hardware accelerator output, and the expected output all match: 12, 23, 0, and 19. This confirms that the accelerator computes the same result as the reference for this test case. The cycle count also shows the performance difference. The CPU version takes 1,516 cycles, while the accelerator takes 287 cycles. So the measured convolution-only speedup is 5.282 times. I describe it as convolution-only because the measurement is for this kernel, not for the whole neural network.

## Slide 15. Board Result: LeNet-5 Inference

Suggested time: 0:45

To test a more complete workload, I also ran a LeNet-5 inference program on the FPGA. In this demo, NICE accelerates the convolution layers, while pooling and fully connected layers still run in software on E203. This means the demo checks system integration, not full hardware acceleration of every layer. The UART transcript records that all 10 sampled MNIST images were classified correctly. This should be understood as a sampled board demo, not as a full MNIST benchmark, but it still shows that the firmware, accelerator calls, and final classification flow can run together on the FPGA.

## Slide 16. Performance and Resource Summary

Suggested time: 0:45

This slide summarizes performance, resource usage, and timing evidence. The measured convolution-only speedup is 5.282 times, meeting the target of at least 5 times. The resource usage also fits comfortably on the A7-100T FPGA: LUT is 20.8 percent, FF is 10.1 percent, BRAM is 26.3 percent, and DSP is 0 percent. On the right, I added the routed Vivado timing evidence: the cnn_sysclk_ila build reports WNS of 12.472 ns, WHS of 0.057 ns, and zero failing endpoints. So this implementation is not only functionally correct, but also timing-clean in the tested FPGA configuration.

## Slide 17. Limitations and Future Work

Suggested time: 0:45

There are still several limitations. The SoC currently runs at 16 MHz, so a higher frequency would require timing re-validation. The 10 out of 10 MNIST result is only a sampled demo, so broader testing is still needed before making a stronger accuracy claim. Also, only Conv1 and Conv2 use NICE; pooling and fully connected layers remain on the software side, which limits the end-to-end speed. Future work can include a larger MNIST subset, FC acceleration, RSTAT optimization to reduce readback overhead, and more formal checks for the NICE interface.

## Slide 18. Brief Summary

Suggested time: 0:35-0:45

To summarize, this project integrates a lightweight INT8 CNN accelerator with the E203 RISC-V core through NICE custom instructions. The prototype was validated from RTL simulation to FPGA board execution, using UART output and ILA captures as evidence. The board results show correct reduced-CNN output, 5.282 times convolution-only speedup, and a 10 out of 10 sampled LeNet-5 demo. The main value of the project is that it connects the accelerator design with a working RISC-V SoC and real FPGA evidence. Thank you for listening. I am happy to take questions.
