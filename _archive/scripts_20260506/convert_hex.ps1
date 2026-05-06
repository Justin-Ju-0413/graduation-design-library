$src = "C:\Users\16084\DOCUME~1\NEWPRO~1\riscv_cnn_accelerator\sw\lenet5_demo\lenet5.verilog"
$lines = Get-Content $src
Write-Host "Total lines: $($lines.Count)"
Write-Host "Has ITCM (@8000): $(($lines | Where-Object { $_ -match '^@8000' }).Count)"
Write-Host "Has DTCM (@9000): $(($lines | Where-Object { $_ -match '^@9000' }).Count)"

# Find ITCM section - byte-level hex needs conversion to 64-bit words
$itcm_data = @()
$in_itcm = $false
foreach ($line in $lines) {
    if ($line -match '^@80000000') { $in_itcm = $true; continue }
    if ($line -match '^@') { $in_itcm = $false; continue }
    if ($in_itcm) {
        $bytes = $line.Trim() -split '\s+'
        foreach ($b in $bytes) {
            if ($b.Length -eq 2) {
                $itcm_data += [Convert]::ToByte($b, 16)
            }
        }
    }
}
Write-Host "ITCM data bytes: $($itcm_data.Count)"

# Convert bytes to 64-bit little-endian words (for 64-bit ITCM BRAM)
$itcm_words_8b = @()  # 8-byte words
for ($i = 0; $i -lt $itcm_data.Count; $i += 8) {
    $word = 0UL
    for ($j = 0; $j -lt 8; $j++) {
        if ($i + $j -lt $itcm_data.Count) {
            $word = $word -bor ([UInt64]$itcm_data[$i + $j] -shl ($j * 8))
        }
    }
    $itcm_words_8b += $word
}
Write-Host "ITCM 64-bit words: $($itcm_words_8b.Count)"

# Write hex file for Vivado $readmemh (64-bit words, one per line)
$out_itcm = "C:\Users\16084\DOCUME~1\NEWPRO~1\riscv_cnn_accelerator\sw\lenet5_demo\lenet5.itcm.verilog"
$itcm_words_8b | ForEach-Object { "{0:X16}" -f $_ } | Out-File $out_itcm -Encoding ASCII
Write-Host "ITCM hex saved: $out_itcm ($((Get-Item $out_itcm).Length) bytes)"

# Show first few words
Write-Host "`nFirst 3 ITCM 64-bit words:"
Get-Content $out_itcm -TotalCount 3 | ForEach-Object { Write-Host "  $_" }
