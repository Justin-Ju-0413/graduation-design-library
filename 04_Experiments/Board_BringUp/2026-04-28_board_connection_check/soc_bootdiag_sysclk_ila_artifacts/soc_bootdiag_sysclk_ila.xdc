set_false_path -from [get_clocks clk_16M_mmcm] -to [get_clocks sys_clk_pin]

# The APB advanced timer samples its low-speed clock input as data. In this
# diagnostic build lfextclk is intentionally tied to the same 16 MHz board clock
# used by the SoC, so these clock-as-data synchronizer endpoints are not a real
# synchronous data path.
set_false_path -to [get_pins -hierarchical -quiet -filter {NAME =~ *r_ls_clk_sync_reg*/D}]
