# 2026-04-23 Next Week Plan

## Main Goal

Keep the verified simulation baseline stable, then focus the next week on the Davinci Pro A7-100T soft-core debug path.

## Current Known Baseline

- `riscv_cnn_accelerator`
  - Branch: `codex/a7-bringup-v2-main`
  - Commit: `0030703a48380f69762306980022e082d0623052`
- `e203_hbirdv2`
  - Branch: `codex/a7-bringup-v2-soc`
  - Commit: `89bf700dc3cfe1a347e82160c66c812126fa88eb`
- Windows local repos are clean.
- Ubuntu SSH was not reachable during this setup pass, so the new rerun logs are marked as pending.

## Week Tasks

### Day 1: Reconfirm Simulation Baseline

Run on Ubuntu:

```bash
cd ~/Desktop/riscv_cnn_accelerator
./Project_Manager.sh run_hw
bash scripts/run_sdk_fullsoc_regression.sh
```

Expected results:

- `run_hw`: `[TB_PASS] mock NICE regression completed`
- full-SoC: `expected_rstat = 19`
- full-SoC: `[PHASE4_PASS] sdk build, image split, and full-SoC regression passed`

Store outputs:

- RTL screenshots/logs:
  - `04_Experiments/RTL_Simulation/2026-04-23_baseline_rerun`
- full-SoC screenshots/logs:
  - `04_Experiments/FullSoC_Simulation/2026-04-23_baseline_rerun`

### Day 2: Document Soft-Core Debug Blocker

Write down exactly what is working and not working:

- Working:
  - `PTD04 + Vivado` can be used for FPGA programming.
  - Route A board-side environment has been prepared.
- Not closed:
  - `OpenOCD + GDB`
  - `load ELF`
  - `break main`
  - stable CPU software debug

### Day 3: Evaluate Debug Options

Compare:

- Independent OpenOCD-compatible soft-JTAG adapter
- BSCANE2-based debug bridge

Recommended short-term direction:

- Try an independent OpenOCD-compatible debug adapter first.
- Keep BSCANE2 as a later integration route.

### Day 4: Minimal Board Observation

Do not force full GDB closure yet.

Try to collect:

- UART output
- LED stage marker
- ILA basic activity

If no evidence is available, record the missing part clearly instead of overstating progress.

### Day 5: Prepare Weekly Report

Update:

- Notion
- Windows library
- one-page weekly note
- next meeting talking points

## One-Sentence Weekly Goal

This week I will keep the RTL/full-SoC baseline reproducible, then focus on identifying and narrowing the board-side soft-core debug blocker on Davinci Pro A7-100T.
