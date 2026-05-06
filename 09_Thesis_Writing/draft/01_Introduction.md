# Chapter 1: Introduction

## 1.1 Background

Convolutional Neural Networks (CNNs) have become the dominant approach for
computer vision tasks including image classification, object detection, and
semantic segmentation. However, the computational intensity of CNN inference
poses significant challenges for deployment on resource-constrained edge
devices. A single forward pass through even a modest network like LeNet-5
requires millions of multiply-accumulate (MAC) operations, making
general-purpose CPU execution prohibitively slow and power-inefficient for
real-time applications.

Hardware acceleration has emerged as the primary solution to this challenge.
Application-Specific Integrated Circuits (ASICs) and Field-Programmable Gate
Arrays (FPGAs) can achieve orders of magnitude better performance and energy
efficiency than CPUs by exploiting the inherent parallelism in CNN
computations. Systolic array architectures, in particular, have proven
highly effective for matrix multiplication—the core operation in both
fully-connected and convolutional layers—by organizing processing elements
in a regular grid with local data communication.

## 1.2 RISC-V and Custom Instruction Extensions

RISC-V is an open standard instruction set architecture (ISA) that has
gained significant traction in both academic and industrial settings since
its introduction at UC Berkeley in 2010. Unlike proprietary ISAs, RISC-V's
modular design explicitly reserves encoding space for custom instruction
extensions, enabling domain-specific acceleration without breaking
compatibility with the standard ecosystem.

The Nuclei Instruction Co-extension (NICE) interface, implemented in the
E203 Hummingbird v2 processor, provides a standardized mechanism for
integrating custom hardware accelerators directly into the processor
pipeline. Through NICE, custom instructions appear as native RISC-V
instructions to the programmer, with the processor automatically handling
operand fetch, hazard detection, and result writeback. This approach
eliminates the overhead of memory-mapped I/O or coprocessor communication
protocols, enabling fine-grained, low-latency acceleration.

## 1.3 Problem Statement

While RISC-V custom instruction extensions offer a promising path for CNN
acceleration, the practical challenges of integrating a hardware accelerator
with a RISC-V core and validating the complete system on an FPGA platform
remain significant. Key challenges include:

1. Correctly implementing the NICE interface protocol for custom instruction
   handshaking and data transfer.
2. Managing the FPGA build flow, including block RAM initialization,
   clock domain crossing, and timing closure.
3. Establishing a reliable debugging methodology using Integrated Logic
   Analyzer (ILA) probes for observing internal SoC signals.
4. Bridging the gap between RTL simulation and hardware behavior, where
   synthesis-specific issues, memory initialization formats, and macro
   visibility can cause divergent behavior.

## 1.4 Project Objectives

This project aims to design, implement, and validate a lightweight CNN
accelerator integrated with a RISC-V E203 processor through the NICE
interface, targeting FPGA prototype validation on the Davinci Pro A7-100T
development board.

The specific objectives are:

1. Design a 4×4 systolic PE array supporting INT8 quantized convolution,
   with six custom NICE instructions (CFG, CLEAR, WLOAD, DLOAD, COMP,
   RSTAT) for software control.
2. Integrate the accelerator with the E203 Hummingbird v2 SoC, including
   ITCM/DTCM memory, UART, and GPIO peripherals.
3. Establish a complete FPGA bring-up pipeline from RTL simulation through
   Vivado synthesis, place-and-route, and bitstream generation.
4. Validate the CPU boot chain by running a minimal bare-metal program
   (hello_e203) on the FPGA board with UART output verification.
5. Test the CNN accelerator custom instructions on the FPGA using custom
   NICE test programs, with ILA-based diagnostic evidence collection.

## 1.5 Thesis Structure

The remainder of this thesis is organized as follows. Chapter 2 provides
background on RISC-V architecture, the E203 processor, CNN fundamentals, and
FPGA prototyping methodology. Chapter 3 describes the system architecture,
NICE instruction design, PE array implementation, and SoC integration.
Chapter 4 presents the experimental results, including RTL simulation,
FPGA bitstream construction, hello_e203 board validation, CPU boot
debugging and root cause analysis, and NICE accelerator testing. Chapter 5
discusses the findings, limitations, and engineering lessons learned.
Chapter 6 concludes with a summary of contributions and directions for
future work.
