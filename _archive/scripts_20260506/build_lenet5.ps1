$gcc = "D:\Xilinx\Vitis\2023.2\gnu\riscv\nt\riscv64-unknown-elf\bin\riscv64-unknown-elf-gcc.exe"
$objcopy = "D:\Xilinx\Vitis\2023.2\gnu\riscv\nt\riscv64-unknown-elf\bin\riscv64-unknown-elf-objcopy.exe"
$repo = "C:\Users\16084\Documents\New project\riscv_cnn_accelerator"
$sw = "$repo\sw\lenet5_demo"

Write-Host "Compiling LeNet-5 for RISC-V E203..."
Write-Host "GCC: $gcc"
Write-Host "Source: $sw"

$args = @(
    "-march=rv32imac",
    "-mabi=ilp32",
    "-O2",
    "-nostdlib",
    "-T", "$sw\linker.ld",
    "$sw\startup.S",
    "$sw\main.c",
    "-o", "$sw\lenet5.elf"
)

& $gcc $args 2>&1 | ForEach-Object { Write-Host $_ }

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== Compile OK ==="
    $elf = Get-Item "$sw\lenet5.elf"
    Write-Host "ELF: $($elf.Length) bytes"

    # Generate Verilog hex
    Write-Host "`nGenerating Verilog hex..."
    & $objcopy -O verilog "$sw\lenet5.elf" "$sw\lenet5.verilog" 2>&1
    if ($LASTEXITCODE -eq 0) {
        $hex = Get-Item "$sw\lenet5.verilog"
        Write-Host "Verilog hex: $($hex.Length) bytes"

        # Show first few lines
        Write-Host "`nFirst 5 lines:"
        Get-Content "$sw\lenet5.verilog" -TotalCount 5 | ForEach-Object { Write-Host $_ }
    }
} else {
    Write-Host "`n=== Compile FAILED (exit code $LASTEXITCODE) ==="
}
