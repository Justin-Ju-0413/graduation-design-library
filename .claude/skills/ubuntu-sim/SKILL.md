---
name: ubuntu-sim
description: Compile and run iverilog simulation on Ubuntu VM (192.168.10.128). Use when user says "run simulation", "compile sim", "仿真", "跑仿真", or needs to test RTL changes on Ubuntu.
version: 1.0.0
---

# Ubuntu iverilog Simulation

Compiles RTL from `~/Desktop/e203_hbirdv2/vsim/install/rtl/` and runs simulation.

## Prerequisites
- Ubuntu VM running at 192.168.10.128 (user: gstar, key: ~/.ssh/id_ed25519_ubuntu)
- SSH config has `Host ubuntu` entry
- RTL modified at vsim/install/rtl/

## Quick Compile & Run

```bash
# Testbench goes to vsim/install/tb/
# Compile with:
ssh -q ubuntu "cd ~/Desktop/e203_hbirdv2/vsim/install && \
  iverilog -Wall -g2005-sv -D DISABLE_SV_ASSERTION=1 -D FPGA_SOURCE -D E203_FORCE_BOOTROM_BOOT \
  -I rtl/core -I rtl/perips -I rtl/perips/apb_i2c -I rtl/soc -I rtl/subsys \
  -I rtl/mems -I rtl/debug -I rtl/fab -I rtl/general \
  -s {TOP_MODULE} -o ../sim_out \
  \$(find rtl -name '*.v' | sort) tb/{TB_FILE}.v 2>&1 | grep -c error"

# If 0 errors, run:
ssh -q ubuntu "cd ~/Desktop/e203_hbirdv2/vsim && timeout 20 vvp sim_out 2>&1"
```

## File Transfer
```bash
# SCP a file to Ubuntu:
scp -q {local_path} ubuntu:{remote_path}

# Common destinations:
# Testbench: ubuntu:~/Desktop/e203_hbirdv2/vsim/install/tb/
# RTL core: ubuntu:~/Desktop/e203_hbirdv2/vsim/install/rtl/core/
```

## Key Simulation Fixes Applied
These fixes are in vsim/install/rtl/ and MUST be preserved:
- `subsys/e203_subsys_top.v`: `assign hfclkrst = 1'b0;`
- `subsys/e203_subsys_main.v`: PLL wires assigned (pllbypass=1, pll_ASLEEP=0, etc.)
- `soc/e203_soc_top.v`: `test_mode = 1'b1`
- `core/e203_cpu.v`: `assign clk_aon = clk;` (may conflict - verify)
- `core/e203_fpga_mem_init.vh`: Empty ITCM/DTCM init
- Perips files from vsim/original copied: sirv_ResetCatchAndSync*.v, sirv_jtaggpioport.v
- `general/sirv_sram_icb_ctrl.v`: Restored from source
