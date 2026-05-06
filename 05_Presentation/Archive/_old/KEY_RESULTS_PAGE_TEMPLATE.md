# Key Results Page Template

Use this file after you finish tonight's experiments.

## Recommended Page Title

`Key Experimental Results`

## Best Layout

- Left side: one screenshot for `run_sdk_fullsoc_regression.sh`
- Right side: one screenshot for Vivado programming or bitstream success
- Bottom row: one optional screenshot for UART or ILA

## Must-Have Evidence Priority

1. full-SoC regression success
2. `expected_rstat = 19`
3. bitstream rebuild success
4. FPGA programming success

## Strong Extra Evidence

1. UART milestones
2. ILA waveform
3. LED observation

## Suggested Caption Style

- `Local RTL simulation passed`
- `Full-SoC regression reached expected_rstat = 19`
- `A7-100T Route A bitstream rebuilt successfully`
- `PTD04 + Vivado programmed the FPGA successfully`
- `UART milestones observed on the board`
- `ILA captured CPU and NICE runtime activity`

## Suggested Conclusion Line

- These results show that the active baseline is reproducible in simulation and already reaches the FPGA programming stage, while the remaining work is the final Route A runtime evidence chain.
