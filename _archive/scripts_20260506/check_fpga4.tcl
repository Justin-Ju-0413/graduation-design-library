# Final ILA capture for LeNet-5 verification
open_hw_manager
connect_hw_server
open_hw_target

set dev [lindex [get_hw_devices] 0]
set_property PROBES.FILE "C:/Users/16084/Documents/New project/e203_hbirdv2/fpga/davinci_a7_100t/obj/davinci_a7_100t.runs/impl_1/debug_nets.ltx" $dev
refresh_hw_device $dev

set ila [lindex [get_hw_ilas] 0]

puts "Arming ILA trigger..."
run_hw_ila $ila
after 5000
wait_on_hw_ila $ila

# Upload to CSV
set csv_file "C:/Users/16084/Desktop/lenet5_ila.csv"
puts "Uploading ILA data..."
upload_hw_ila_data $ila -csv -file $csv_file
puts "ILA data saved: $csv_file"

close_hw_manager
puts "Done!"
