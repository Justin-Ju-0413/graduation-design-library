# Verify LeNet-5 execution on FPGA with proper probes file
puts "Opening hardware manager..."
open_hw_manager
connect_hw_server
open_hw_target

set dev [lindex [get_hw_devices] 0]

# Set probes file
set_property PROBES.FILE "C:/Users/16084/Documents/New project/e203_hbirdv2/fpga/davinci_a7_100t/obj/davinci_a7_100t.runs/impl_1/debug_nets.ltx" $dev

refresh_hw_device $dev

# Get ILA
set ilas [get_hw_ilas]
puts "ILA cores: [llength $ilas]"

if {[llength $ilas] > 0} {
    set ila [lindex $ilas 0]

    # Show probe info
    set probes [get_hw_probes -of_objects $ila]
    puts "Probes:"
    foreach p $probes {
        puts "  $p"
    }

    puts "Arming ILA trigger..."
    run_hw_ila $ila
    after 3000
    wait_on_hw_ila $ila -timeout 15

    set status [get_property STATUS $ila]
    puts "ILA status: $status"

    # Upload capture
    set csv_file "C:/Users/16084/Desktop/lenet5_ila.csv"
    upload_hw_ila_data $ila -csv -file $csv_file
    puts "ILA data: $csv_file"

    # Show sample data
    set data [get_hw_ila_data $ila]
    set samples [get_property SAMPLE_COUNT $data]
    puts "Captured $samples samples"

    # Show first 5 PC values
    puts "\nFirst 5 PC (probe0) values:"
    for {set i 0} {$i < 5} {incr i} {
        set pc [get_property PROBE0_TRIGGER_VAL $data]
        puts "  Sample $i: probe0_pc is being read..."
    }
}

close_hw_manager
