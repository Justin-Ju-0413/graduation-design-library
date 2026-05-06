# Program FPGA with LeNet-5 bitstream
set bitfile "C:/Users/16084/Documents/New project/e203_hbirdv2/fpga/davinci_a7_100t/obj/system.bit"

puts "Connecting to hardware server..."
open_hw
connect_hw_server

puts "Opening target..."
open_hw_target

set devices [get_hw_devices]
puts "Found devices: $devices"

current_hw_device [lindex $devices 0]

puts "Programming device with $bitfile..."
set_property PROGRAM.FILE $bitfile [current_hw_device]
program_hw_devices [current_hw_device]

puts "Program complete!"
close_hw
