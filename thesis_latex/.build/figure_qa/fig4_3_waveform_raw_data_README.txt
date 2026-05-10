Figure 4.3 waveform raw data

Source file:
  04_Experiments\Board_BringUp\2026-05-09_nice_rs2_fix_verification\ila_capture.csv

Copied to:
  thesis_latex\.build\figure_qa\fig4_3_waveform_raw_data.csv

Capture metadata:
  samples: 1024
  trigger index: 512
  ILA clock: 50 MHz

Columns:
  probe0_pc[31:0]          CPU program counter
  probe1_reset_uart[3:0]   reset/UART-related status probe
  probe2_liveness[2:0]     liveness/fetch activity indicator
  probe3_pc_activity[31:0] memory-reference activity probe
  probe4_nice_csr[31:0]    NICE CSR/status probe
  probe5_nice_hs[3:0]      NICE handshake probe
  probe6_mem_status[2:0]   memory/bus status probe

Recommended waveform presentation:
  Use a single shared x-axis in samples or time.
  Stack probes vertically like a Vivado ILA waveform.
  Mark trigger index 512 with a vertical cursor.
  Use hexadecimal radix for 32-bit buses and binary/hex for small status buses.
