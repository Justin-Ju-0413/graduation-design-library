# Vivado batch: export reports only (device image not supported in batch)
set dcp_path "C:/Users/16084/Documents/New project/e203_hbirdv2/fpga/davinci_a7_100t/obj/davinci_a7_100t.runs/impl_1/system_routed.dcp"
set out_dir "C:/Users/16084/Documents/Graduation_Design_Library/09_Thesis_Writing/Figures"

open_checkpoint $dcp_path

# Export utilization report
report_utilization -file $out_dir/utilization_vivado.txt
puts "Utilization report exported."

# Export timing summary
report_timing_summary -file $out_dir/timing_vivado.txt
puts "Timing report exported."

# Export clock utilization
report_clock_utilization -file $out_dir/clock_utilization.txt
puts "Clock report exported."

puts "All exports complete!"
