# Tuesday Report Slides

## Page 1: Project Goal And Report Scope

Title:

`RISC-V CNN Accelerator Progress Report`

Bullets:

- Project: lightweight CNN accelerator based on Hummingbird E203
- Goal: integrate the accelerator through NICE and push the flow from RTL verification to FPGA board validation
- This report focuses on the last four weeks of progress
- Current active baseline: `codex/a7-bringup-v2-main` + `codex/a7-bringup-v2-soc`

Conclusion:

- This report summarizes the recent progress on the active A7-100T Route A line.

## Page 2: System Architecture

Title:

`System Architecture`

Bullets:

- E203 works as the host CPU
- NICE is used as the custom accelerator interface
- A 4x4 INT8 PE array is used as the CNN compute engine
- Firmware, SDK app, and full-SoC simulation form the software verification path
- The current FPGA target is A7-100T

Conclusion:

- The project is a complete CPU-to-accelerator-to-board validation flow.

## Page 3: Four-Week Timeline

Title:

`Progress Over The Last Four Weeks`

Bullets:

- Week 1: confirmed the integration and simulation baseline
- Week 2: closed the software-driven full-SoC path
- Week 3: consolidated pre-board verification and documentation
- Week 4: moved into A7-100T bring-up, including Vivado setup, FPGA download, and Route A observation preparation

Conclusion:

- The last four weeks moved the project from reproducible simulation closure toward real board-side bring-up.

## Page 4: Closed Technical Work

Title:

`Closed Technical Work`

Bullets:

- The E203-to-CNN NICE integration is formally locked
- The command path `CLEAR/WLOAD/DLOAD/COMP/RSTAT` is stable
- Interface safety checks were completed for invalid command, reset, busy blocking, and repeated `RSTAT`
- The software-driven full-SoC flow is already reproducible through the SDK path

Evidence line:

- Evidence: `./Project_Manager.sh run_hw` and `bash scripts/run_sdk_fullsoc_regression.sh` have passed in the current baseline

Conclusion:

- The RTL and SoC simulation baseline is already closed and reproducible.

## Page 5: Reproducible Result Baseline

Title:

`Reproducible Result Baseline`

Bullets:

- Historical software-driven SoC closure reached `RSTAT=320`
- The current minimal CNN v1 baseline reaches `expected_rstat = 19`
- The current active branch pair is `codex/a7-bringup-v2-main` and `codex/a7-bringup-v2-soc`
- The active baseline can be rerun from the current script entry points

Suggested table:

| Flow | Entry | Expected result |
|------|-------|-----------------|
| Local RTL baseline | `./Project_Manager.sh run_hw` | pass |
| Full-SoC regression | `bash scripts/run_sdk_fullsoc_regression.sh` | `expected_rstat = 19` |
| Current board prep status | environment and shell prepared | in progress |

Conclusion:

- The current baseline is measurable and reproducible, not only descriptive.

## Page 6: Board Bring-Up Status

Title:

`Board Bring-Up Status`

Bullets:

- The active FPGA target is `davinci_a7_100t`
- The board-side development environment has already been prepared to the bring-up stage
- `PTD04 + Vivado` has already been confirmed for FPGA programming
- The A7-100T Route A bitstream has already been rebuilt
- UART, LED, and ILA observation paths have been added into the current shell

Conclusion:

- The board build and FPGA download path is prepared, but runtime closure is still ongoing.

## Page 7: Current Blockers

Title:

`Current Blockers`

Bullets:

- The UART COM port still needs to be locked on Windows
- The current bottleneck is soft-core debug on the Davinci Pro A7-100T board
- `PTD04` is currently usable for FPGA programming, but not yet for CPU software debug
- `OpenOCD + GDB load ELF + break main` is still unresolved in the current setup
- A new debug solution is still needed, such as a dedicated soft-JTAG adapter or a later `BSCANE2` bridge

Conclusion:

- The current blocker is board-side soft-core debugging, not RTL or full-SoC simulation.

## Page 8: Next-Step Plan

Title:

`Next-Step Plan`

Bullets:

- Keep the current simulation baseline stable as the reference line
- Continue Route A observation through UART, LED, and ILA
- Evaluate a new CPU debug solution for the Davinci Pro A7-100T board
- Keep `PTD04 + BSCANE2` as a later research direction
- Close the board-side runtime evidence chain step by step

Conclusion:

- The next step is to move from board preparation into board-side runtime and debug closure.
