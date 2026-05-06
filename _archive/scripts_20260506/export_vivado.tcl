# Vivado batch script: export device view and reports
set dcp_path "C:/Users/16084/Documents/New project/e203_hbirdv2/fpga/davinci_a7_100t/obj/davinci_a7_100t.runs/impl_1/system_routed.dcp"
set out_dir "C:/Users/16084/Documents/Graduation_Design_Library/09_Thesis_Writing/Figures"

open_checkpoint $dcp_path

# Export device view (floorplan)
write_device_image -format png -file $out_dir/fig_device_view.png

# Export utilization report
report_utilization -file $out_dir/utilization_report.txt

# Export timing summary
report_timing_summary -file $out_dir/timing_summary.txt

puts "Export complete!"
