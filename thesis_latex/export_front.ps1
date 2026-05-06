$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open('C:\Users\16084\Documents\Graduation_Design_Library\FYP_Thesis_Final.docx')
$doc.ExportAsFixedFormat('C:\Users\16084\Documents\Graduation_Design_Library\thesis_latex\front_matter.pdf', 17, $false, 0, 1, 3, $false, $false, $false, $false, $false)
$doc.Close()
$word.Quit()
Write-Host 'Front matter PDF exported (pages 1-3)'
