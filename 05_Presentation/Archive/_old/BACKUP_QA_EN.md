# Backup Q and A

## Why E203 + NICE?

- E203 is lightweight and suitable for academic integration work.
- NICE provides a direct custom co-unit interface.
- It allows accelerator integration without first building a full external bus-based design.

## Why did the main result change from `320` to `19`?

- `RSTAT=320` is the historical software-driven closure result for the earlier dot-product validation path.
- `expected_rstat = 19` is the current minimal CNN v1 baseline on the active branch.
- They correspond to different validation checkpoints.

## Why is Route A prioritized over GDB-first debug?

- The current milestone is to prove that the board really runs the image.
- UART, LED, and ILA can close that proof chain faster.
- CPU single-step debug is still useful, but it is not the shortest path to the current milestone.

## What does `PTD04` support now?

- It has already been confirmed for FPGA programming through Vivado Hardware Manager.
- It does not yet provide a closed CPU software debug path for the current milestone.
- CPU debug remains a later research item together with `BSCANE2`.
