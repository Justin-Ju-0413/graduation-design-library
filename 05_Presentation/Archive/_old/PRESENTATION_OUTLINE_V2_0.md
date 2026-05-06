# Presentation Outline

> **Version**: V2.0 | **Updated**: 2026-04-13 | **Owner**: Justin JU

## Purpose

This is the default outline for turning the current project state into a
weekly report, defense PPT, or thesis-progress presentation.

## Slide 1: Project Title And Goal

- Topic: lightweight CNN accelerator based on RISC-V E203
- Goal: integrate a CNN accelerator through NICE and push it from RTL verification to FPGA board bring-up
- Current focus: A7-100T Route A functional validation

## Slide 2: System Architecture

- E203 core as the host CPU
- NICE as the custom accelerator interface
- 4x4 INT8 PE array as the compute engine
- firmware, SDK app, and full-SoC simulation as the software path

## Slide 3: What I Implemented

- Completed the formal E203 to CNN NICE integration
- Corrected the E203 NICE custom instruction interpretation
- Built the software-driven verification path through the SDK
- Added board-oriented Route A instrumentation for UART, LED, and ILA

## Slide 4: Phase-Based Progress

- Phase 1: SoC minimum closure
- Phase 2: interface safety closure
- Phase 3: software path closure
- Phase 4: recovery and engineering cleanup
- Phase 5: board bring-up preparation and A7-100T Route A shift

## Slide 5: Reproducible Technical Baseline

- Local accelerator flow can be rerun with project manager commands
- Full-SoC regression can be rerun from the SDK path
- Current minimal CNN v1 baseline reaches `expected_rstat = 19`
- Pre-board verification sweep is available as the current software gate

## Slide 6: FPGA And Board Progress

- Vivado is confirmed in the active environment
- `PTD04 + Vivado` can program the A7-100T board
- Route A bitstream rebuild is already closed
- UART, LED, and ILA observability have been wired into the active shell

## Slide 7: Current Results And Evidence

- Historical software-driven closure: `RSTAT=320`
- Current minimal CNN v1 full-SoC result: `expected_rstat = 19`
- FPGA programming path: closed
- Final board runtime evidence: still being collected

## Slide 8: Current Blockers

- UART COM port still needs to be locked
- UART milestone logs are not yet archived
- LED runtime observation is not yet archived
- ILA capture of CPU and NICE activity is not yet archived
- CPU debug through `PTD04` is still a later path, not the current gate

## Slide 9: Next Step Plan

- capture UART milestones on real hardware
- record LED stage behavior
- arm and capture ILA evidence
- close the Route A board evidence chain
- keep `BSCANE2` and CPU debug as follow-up work, not as the current blocker

## Slide 10: One-Sentence Conclusion

- The project has already closed the RTL, SoC, SDK, and FPGA programming baseline; the remaining work is the final board-side evidence chain for A7-100T Route A.
