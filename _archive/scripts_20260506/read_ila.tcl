# Read ILA capture data to verify LeNet-5 execution
puts "Opening hardware manager..."
open_hw_manager
connect_hw_server -allow_unsupported
open_hw_target

set devices [get_hw_devices]
current_hw_device [lindex $devices 0]
refresh_hw_device [current_hw_device]

puts "Getting ILA cores..."
set ilas [get_hw_ilas]
puts "ILA cores: $ilas"

if {[llength $ilas] > 0} {
    set ila [lindex $ilas 0]
    puts "Reading ILA data from $ila..."

    # Trigger and capture
    run_hw_ila $ila
    wait_on_hw_ila $ila

    # Read capture data
    set data [get_hw_ila_data $ila]
    puts "ILA data captured successfully"

    # Also get probes info
    set probes [get_hw_probes -of_objects $ila]
    puts "Probes: $probes"

    # Display first few samples of probe0 (PC)
    puts "\nDisplaying capture data..."
    display_hw_ila_data $data
}

# Try to upload capture data to CSV
set csv_file "C:/Users/16084/Desktop/lenet5_ila_capture.csv"
upload_hw_ila_data $ila -csv -file $csv_file
puts "ILA data uploaded to $csv_file"

close_hw_manager
