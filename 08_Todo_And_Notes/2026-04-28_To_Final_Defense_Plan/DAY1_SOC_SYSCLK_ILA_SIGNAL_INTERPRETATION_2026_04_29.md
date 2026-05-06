# Day 1 Signal Interpretation: `soc_sysclk_ila`

## Summary

Day 1 closes the interpretation of the current full-SoC raw `sys_clk` ILA evidence.

The `soc_sysclk_ila` capture is valid board evidence: the full SoC is programmed, reset is released, raw `sys_clk` ILA upload works, and CPU-side activity is visible. The sampled `probe0_pc` should be treated as IFU fetch-PC state, not as commit-PC or software-completion proof.

## Capture Summary

Evidence path:

- `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_sysclk_ila_ila_capture\ila_summary.txt`
- `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_sysclk_ila_ila_capture\ila_capture.csv`

Observed values:

| Probe | Meaning in this build | Observed value |
| --- | --- | --- |
| `probe0_pc` | synchronized IFU inspect PC sample | `00000000`, `00000002` |
| `probe1_reset_uart` | `{sys_rst_n, mmcm_locked, reset_periph, uart_txd}` | `d` |
| `probe2_liveness` | `{pc_change_edge, trap_sync, cgstop_or_halt}` | `0`, `4` |
| `probe3_pc_activity` | PC-change counter sampled in raw `sys_clk` domain | `000ed645 -> 000ed671` |
| `probe4_nice_csr` | sampled NICE CSR addr/wdata mux | `00000000` |
| `probe5_nice_hs` | NICE handshake summary | `4` |
| `probe6_mem_status` | memory command/ready/event summary | `1`, `3`, `5` |

Interpretation:

- `probe1_reset_uart=d` means `sys_rst_n=1`, `mmcm_locked=1`, `reset_periph=0`, and UART TX sampled high.
- `probe3_pc_activity` increments and `probe2_liveness` shows PC-change events, so the IFU-side PC logic is active after reset release.
- `probe0_pc` only exposing `00000000` and `00000002` is not enough to conclude the architectural program counter is progressing through the intended software image.
- `probe5_nice_hs=4` and `probe6_mem_status` activity show live bus/NICE-related signal changes, but they need a CPU boot-focused capture before drawing software-level conclusions.

## `probe_pc` Wiring Conclusion

Trace:

```text
soc_sysclk_ila_system.probe_pc
  -> e203_soc_top.probe_pc
  -> e203_subsys_top.probe_pc
  -> e203_subsys_main.probe_pc
  -> e203_cpu.inspect_pc
  -> e203_core.inspect_pc
  -> e203_ifu.inspect_pc
  -> e203_ifu_ifetch.inspect_pc
  -> pc_r
```

Relevant RTL facts:

- `e203_subsys_main.v`: `assign probe_pc = inspect_pc`
- `e203_ifu_ifetch.v`: `pc_r` is updated by `pc_dfflr` when `pc_ena = ifu_req_hsked | pipe_flush_hsked`
- `e203_ifu_ifetch.v`: `assign inspect_pc = pc_r`
- `e203_ifu_ifetch.v`: `assign ifu_req_pc = pc_nxt`

Conclusion:

- `probe_pc` is a real core-origin signal, not a top-level placeholder.
- It is the IFU inspect PC (`pc_r`), which tracks fetch/flush-side PC state.
- It is not a commit-stage PC and does not by itself prove instruction retirement, trap-free execution, UART software progress, or correct boot image execution.
- For board bring-up, `probe3_pc_activity` and explicit fetch/ITCM counters are stronger liveness indicators than a single asynchronously sampled `probe0_pc` value.

## Day 2 Diagnostic Probe List

The next diagnostic build should keep raw `sys_clk` ILA and replace ambiguous software-level interpretation with activity counters and sticky flags.

Recommended probes:

| Probe | Content |
| --- | --- |
| `probe0` | IFU inspect PC sample or lower PC bits plus reset-stage bits |
| `probe1` | `{sys_rst_n, mmcm_locked, reset_periph, uart_txd}` |
| `probe2` | sticky `{pc_changed, ifu_req_seen, ifu_rsp_seen, trap_or_halt}` summary |
| `probe3` | PC-change counter |
| `probe4` | IFU request/response counter or `{ifu_req_count, ifu_rsp_count}` reduced value |
| `probe5` | UART TX edge counter or sampled UART state plus GPIOA[17] output-enable |
| `probe6` | halt/cgstop/trap/reset-release counter summary |

Priority signals to expose from RTL:

- `ifu_req_valid`, `ifu_req_ready`, `ifu_rsp_valid`, `ifu_rsp_ready`
- `ifu2itcm_icb_cmd_valid`, `ifu2itcm_icb_cmd_ready`, `ifu2itcm_icb_rsp_valid`, `ifu2itcm_icb_rsp_ready`
- `reset_periph`, `mmcm_locked`, `sys_rst_n`
- `uart_txd`, `gpioA_o_oe[17]`, `gpioA_o_oval[17]`
- `core_cgstop`, `dbg_halt_r`
- a real trap/exception indicator if available; current `probe_commit_trap` is tied to `1'b0` in `e203_subsys_main`

## Decision

Day 1 is complete. The next task is Day 2: build a CPU boot diagnostic ILA that observes fetch/ITCM activity, UART TX activity, reset release, and halt/cgstop/trap state through counters and sticky flags.

