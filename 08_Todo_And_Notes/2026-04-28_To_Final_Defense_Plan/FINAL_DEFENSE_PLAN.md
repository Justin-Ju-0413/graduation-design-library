# Final Defense Plan

## Goal

Prepare a final defense package that matches the thesis and engineering evidence.

## Slide Structure

1. Title and project goal
2. Background and motivation
3. Overall system architecture
4. NICE custom instruction interface
5. CNN accelerator RTL design
6. Verification chain
7. hello_e203 board bring-up evidence
8. CNN board result
9. Performance and FPGA fit
10. NICE rs2 bug case study
11. Contribution summary and future work

## Main Message

The project has completed a reproducible evidence chain from RTL/NICE verification through full-SoC simulation, hello_e203 board validation, CNN/NICE board execution, and a board-regressed rs2 decoder fix.

## Evidence Package

- Branch and commit table
- RTL `[TB_PASS]` screenshot
- full-SoC `expected_rstat=19` screenshot
- Vivado `xc7a100t_0` detection screenshot
- `system.bit` generation record
- UART hello evidence
- CNN UART result evidence
- ILA PC and NICE handshake evidence
- NICE rs2 fix board-regression evidence

## QA Preparation

Prepare answers for:

- Why use RISC-V and NICE?
- What does the accelerator compute?
- How was RTL verified?
- What does full-SoC simulation prove?
- How does the program enter the bitstream?
- What was the NICE rs2 decoder bug and why did it matter?
- What is the difference between PTD04 programming and CPU debugging?
- Why is the full LeNet-5 runtime still slow despite convolution speedup?

## Rehearsal Plan

- 8 to 12 minute full version
- 3 minute short version
- 1 minute current status answer
- 30 second blocker answer
