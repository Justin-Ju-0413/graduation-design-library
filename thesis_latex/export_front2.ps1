$docPath = 'C:\Users\16084\Documents\Graduation_Design_Library\FYP_Thesis_Final.docx'
$pdfPath = 'C:\Users\16084\Documents\Graduation_Design_Library\thesis_latex\front_matter.pdf'

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open($docPath)

# wdExportAllDocument = 0, wdExportFromTo = 3
# wdFormatPDF = 17
$range = $doc.Range(0, $doc.GoTo(8, 1, 3).End)
$range.ExportAsFixedFormat($pdfPath, 17, $false, 0, $false, $false, 0, $false, $false, $false, $false, $false)

$doc.Close()
$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
Write-Host "Front matter exported"
