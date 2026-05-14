# Final Defense 15-Minute English Script

Suggested pacing: 16 slides, about 50-60 seconds per slide. Speak slightly faster on slides 1-2 and 16, and leave more time for slides 7-12.

## Slide 1. RISC-V Custom-Instruction CNN Accelerator

Good morning, professors and classmates. This work presents a RISC-V custom-instruction CNN accelerator. The goal is not only to design a small CNN computing block, but also to connect it to a real RISC-V E203 soft-core and test the complete path on FPGA. The presentation covers the motivation, system design, instruction interface, verification flow, board results, and main limitations.

## Slide 2. Presentation Outline

This presentation is organized in four parts. The first part introduces the motivation and design objective. The second part explains the system architecture and the custom instruction interface. The third part describes the accelerator microarchitecture and verification strategy. The final part presents the FPGA validation results, limitations, and future work.

## Slide 3. Problem and Design Goal

The motivation comes from running AI on edge devices. CNN convolution contains many repeated MAC operations, meaning multiply and accumulate. These operations are slow on a small embedded processor. RISC-V is suitable for this topic because its open instruction set allows custom instructions. The design objective is to build a small accelerator that the CPU can control directly through custom instructions, and to prove it with a repeatable FPGA prototype.

## Slide 4. System Architecture

At the system level, the host processor is the E203 Hummingbird v2 core. The SoC includes ITCM, DTCM, UART, GPIO, and the CNN accelerator. A key design decision is to connect the accelerator through the NICE custom-instruction interface. Compared with a memory-mapped peripheral, NICE avoids extra bus control logic for accelerator commands. The software sends input values through rs1 and rs2, and reads the result through a CPU register.

## Slide 5. Custom Instruction Interface

The software interface is built from six custom instructions. CLEAR resets the internal state. WLOAD loads packed weights, and DLOAD loads packed activation values. Each 32-bit input contains four signed INT8 values. COMP starts the multiply-accumulate calculation, and RSTAT reads the final INT32 result. CFG is used for options such as ReLU. This instruction set is small, but it is enough for the convolution operation used in the demo.

## Slide 6. Accelerator Microarchitecture

Inside the accelerator, the computing engine is a 4 by 4 PE array. Each PE multiplies one signed 8-bit weight and one signed 8-bit activation value, and adds the result into a 32-bit register. The design keeps partial sums inside the PEs; this is called output-stationary dataflow. The weights are sent by columns, and the activation values are sent by rows. The array is intentionally small, so it can fit together with the E203 SoC on the Artix-7 FPGA.

## Slide 7. Verification Strategy

The verification strategy is one of the important parts of this project. The validation does not rely on only one final board demo. Instead, it uses a step-by-step evidence chain. First, the accelerator RTL was tested with a simple NICE-like test interface. Second, the complete E203 SoC was simulated with the accelerator. Third, the hello_e203 program tested the boot path on the FPGA. Finally, the CNN demo tested the NICE instruction path and accelerator output on the board.

## Slide 8. Evidence Map

Before moving into the board screenshots, this slide summarizes how the claims are supported. The SoC integration claim is supported by the architecture and full-SoC simulation. The boot claim is supported by hello_e203 UART output and the ILA PC trace. The NICE path claim is supported by custom-instruction tests and ILA captures. The convolution correctness and speedup claims are supported by the CNN UART output and the cycle comparison. Resource feasibility is supported by the Vivado utilization report.

## Slide 9. Implementation Flow

This slide shows the implementation flow. The hardware RTL, bare-metal firmware, E203 SoC integration, Vivado implementation, and FPGA board validation were treated as one connected process. This is important because a custom-instruction accelerator is not useful as an isolated module. It must be callable from software, connected through the processor interface, implemented on the FPGA, and checked with board-level output.

## Slide 10. FPGA Prototype Validation

After the design was implemented on FPGA, the first validation target was the E203 boot path. The hello_e203 program printed boot, uart ok, and loop through UART. The ILA capture also showed that the CPU reached the ITCM code region and that UART activity was present. This confirms that the processor, memory initialization, clocking, reset, and UART path were working together on the board.

## Slide 11. NICE Instruction Path Evidence

This slide focuses on the CPU-to-accelerator execution path. The firmware controls the accelerator through the six NICE instructions: CLEAR, WLOAD, DLOAD, COMP, and RSTAT. ILA gives signal-level context that the board is executing in the expected firmware region, while UART gives the final software-visible output comparison. Together, they show that the accelerator is integrated into the processor-controlled execution flow.

## Slide 12. Correctness Evidence Breakdown

This slide breaks down the UART evidence into a simple comparison. The software reference, hardware accelerator output, and expected output are all 12, 23, 0, and 19. This supports the correctness claim for the reduced convolution test. The same run reports 1,516 CPU cycles and 287 accelerator cycles, so the measured speedup is 5.282 times. This speedup is for the convolution kernel only, not for the complete LeNet-5 inference.

## Slide 13. Board Result: CNN Board Test

The first CNN board result is a reduced convolution test. It uses a 3 by 3 INT8 convolution on a 4 by 4 input. The UART log shows that the software reference, the hardware accelerator output, and the expected output all match: 12, 23, 0, and 19. For this convolution kernel, the CPU reference took 1,516 cycles, while the accelerator took 287 cycles. This gives a measured speedup of 5.282 times.

## Slide 14. Board Result: LeNet-5 Inference

To go beyond a small convolution kernel, a LeNet-5 inference program was also deployed. The convolution layers use the NICE accelerator path, while the fully connected layers still run in software. During testing, the Conv2 ReLU position was corrected, so ReLU is applied after all input channels are added together. The UART divisor was also corrected for 115200 baud. The recorded UART output shows that all 10 sampled MNIST images were classified correctly. This is not a full MNIST accuracy test, but it shows that the end-to-end FPGA demo works correctly.

## Slide 15. Performance and Resource Summary

The measured convolution speedup is 5.282 times, which meets the project target of at least 5 times for convolution. The FPGA design also met timing requirements. In the debug builds, WNS, or worst negative slack, stayed above 12 nanoseconds. Resource usage is also low enough for this board: about 20.8 percent LUT, 10.1 percent flip-flop, 26.3 percent BRAM, and no DSP blocks in the reported design. This means the complete E203 SoC with the CNN accelerator fits comfortably on the A7-100T device.

## Slide 16. Limitations and Future Work

There are also clear limitations. The current accelerator is small, and reading results through RSTAT adds overhead when larger convolutions are split into tiles. In the LeNet-5 demo, the fully connected layers still run in software and take most of the end-to-end runtime, which is about two to five minutes per image in the current design. Future work will focus on improving the readback path, accelerating the fully connected layers, testing a larger MNIST subset, and exploring a larger or pipelined PE array. Overall, this project demonstrates a complete and testable FPGA prototype of a RISC-V custom-instruction CNN accelerator.
