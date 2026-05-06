# Quick check: is FPGA alive? Read ILA probes
puts "Opening hardware manager..."
open_hw_manager
connect_hw_server
open_hw_target
refresh_hw_device [lindex [get_hw_devices] 0]

puts "Getting ILA cores..."
set ilas [get_hw_ilas]
puts "ILA cores found: [llength $ilas]"

if {[llength $ilas] > 0} {
    set ila [lindex $ilas 0]
    puts "Triggering ILA capture..."
    run_hw_ila $ila
    after 2000
    wait_on_hw_ila $ila -timeout 10

    # Upload capture data
    set csv_file "C:/Users/16084/Desktop/lenet5_ila.csv"
    puts "Uploading ILA data to $csv_file..."
    upload_hw_ila_data $ila -csv -file $csv_file
    puts "Done! Check $csv_file"
}

close_hw_manager
puts "All done."
