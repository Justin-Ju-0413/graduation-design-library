open_hw_manager
connect_hw_server
open_hw_target
set dev [lindex [get_hw_devices] 0]
set_property PROBES.FILE "C:/Users/16084/Documents/New project/e203_hbirdv2/fpga/davinci_a7_100t/obj/davinci_a7_100t.runs/impl_1/debug_nets.ltx" $dev
refresh_hw_device $dev
set ila [lindex [get_hw_ilas] 0]
run_hw_ila $ila
after 5000
wait_on_hw_ila $ila
set data [get_hw_ila_data $ila]
write_hw_ila_data -csv_file "C:/Users/16084/Desktop/lenet5_ila.csv" $data
puts "ILA CSV written"
close_hw_manager
