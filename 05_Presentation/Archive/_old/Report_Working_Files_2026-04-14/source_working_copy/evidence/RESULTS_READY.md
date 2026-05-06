# Results Ready

This file records the strongest terminal evidence already available for the Tuesday report.

## Page 4: Local RTL Regression

Recommended screenshot target:

```text
./Project_Manager.sh run_hw
[normal_path] expected=320 err=0 got=320 err=0 => PASS
[negative_values] expected=4294967136 err=0 got=4294967136 err=0 => PASS
[invalid_index] expected=0 err=1 got=0 err=1 => PASS
[busy_blocks_new_req] expected=0 err=1 got=0 err=1 => PASS
[reset_clears_state] expected=0 err=1 got=0 err=1 => PASS
[TB_PASS] mock NICE regression completed
```

Suggested caption:

`Local RTL regression passed both functional and interface-safety cases, ending with [TB_PASS].`

## Page 5: Full-SoC Regression

Recommended screenshot target:

```text
bash scripts/run_sdk_fullsoc_regression.sh
EXPECTED_RSTAT=19
[stage] boot
[stage] main
CNN v1 Demo via NICE
[stage] accel cfg
[stage] start
[NICE_RSP] cycle=33007 rdat=19 err=0
[NICE_SUMMARY] request_seen=1 ready_low_seen=1 expected_rstat_seen=1 expected_rstat=19
[PHASE4_PASS] sdk build, image split, and full-SoC regression passed
```

Suggested caption:

`The software-driven full-SoC regression reached the expected NICE response rdat=19 and closed with [PHASE4_PASS].`

## Notes

- The full-SoC issue caused by missing `e203_fpga_mem_init.vh` on Ubuntu has been fixed in the Ubuntu workspace by updating `e203_hbirdv2/vsim/Makefile`.
- A non-fatal warning about ITCM image size may still appear during simulation. It does not block the `expected_rstat = 19` success condition.
