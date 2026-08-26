param(
    [Parameter(Mandatory=$true)][string]$MdPath,
    [Parameter(Mandatory=$true)][string]$PdfPath,
    [Parameter(Mandatory=$true)][string]$TitleText
)

$ErrorActionPreference = "Stop"

$lines = Get-Content -Path $MdPath -Encoding UTF8

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Add()

$sel = $word.Selection
$sel.Font.Name = "Tahoma"
$sel.Font.Size = 10

# Title
$sel.Style = "Title"
$sel.TypeText($TitleText)
$sel.TypeParagraph()
$sel.Style = "Normal"
$sel.Font.Name = "Tahoma"
$sel.Font.Size = 10

foreach ($raw in $lines) {
    $line = $raw.TrimEnd()

    # skip backlink line, horizontal rules, and empty checkbox artifacts
    if ($line -match '^\s*$') {
        $sel.TypeParagraph()
        continue
    }
    if ($line -match '^---+\s*$') { continue }
    if ($line -match '^\s*🏠') { continue }

    # strip markdown emphasis markers but keep text
    $clean = $line -replace '\*\*', '' -replace '`', ''
    # convert wikilinks [[x]] -> x
    $clean = $clean -replace '\[\[([^\]]+)\]\]', '$1'
    # convert markdown links [text](url) -> text (url)
    $clean = $clean -replace '\[([^\]]+)\]\(([^\)]+)\)', '$1 ($2)'

    if ($clean -match '^####\s+(.*)') {
        $sel.Style = "Heading 4"
        $sel.Font.Name = "Tahoma"
        $sel.TypeText($Matches[1])
        $sel.TypeParagraph()
    }
    elseif ($clean -match '^###\s+(.*)') {
        $sel.Style = "Heading 3"
        $sel.Font.Name = "Tahoma"
        $sel.TypeText($Matches[1])
        $sel.TypeParagraph()
    }
    elseif ($clean -match '^##\s+(.*)') {
        $sel.Style = "Heading 2"
        $sel.Font.Name = "Tahoma"
        $sel.TypeText($Matches[1])
        $sel.TypeParagraph()
    }
    elseif ($clean -match '^#\s+(.*)') {
        $sel.Style = "Heading 1"
        $sel.Font.Name = "Tahoma"
        $sel.TypeText($Matches[1])
        $sel.TypeParagraph()
    }
    elseif ($clean -match '^\s*-\s*\[x\]\s*(.*)') {
        $sel.Style = "Normal"
        $sel.Font.Name = "Tahoma"
        $sel.Font.Size = 10
        $sel.TypeText("[Done] " + $Matches[1])
        $sel.TypeParagraph()
    }
    elseif ($clean -match '^\s*-\s*\[\s\]\s*(.*)') {
        $sel.Style = "Normal"
        $sel.Font.Name = "Tahoma"
        $sel.Font.Size = 10
        $sel.TypeText("[Open] " + $Matches[1])
        $sel.TypeParagraph()
    }
    elseif ($clean -match '^\s*[-*]\s+(.*)') {
        $sel.Style = "List Bullet"
        $sel.Font.Name = "Tahoma"
        $sel.Font.Size = 10
        $sel.TypeText($Matches[1])
        $sel.TypeParagraph()
    }
    elseif ($clean -match '^\s*\d+\.\s+(.*)') {
        $sel.Style = "List Number"
        $sel.Font.Name = "Tahoma"
        $sel.Font.Size = 10
        $sel.TypeText($Matches[1])
        $sel.TypeParagraph()
    }
    elseif ($clean -match '^\|') {
        # simple table row rendering as monospace-ish plain text
        $sel.Style = "Normal"
        $sel.Font.Name = "Consolas"
        $sel.Font.Size = 8
        $sel.TypeText($clean)
        $sel.TypeParagraph()
        $sel.Font.Name = "Tahoma"
        $sel.Font.Size = 10
    }
    else {
        $sel.Style = "Normal"
        $sel.Font.Name = "Tahoma"
        $sel.Font.Size = 10
        $sel.TypeText($clean)
        $sel.TypeParagraph()
    }
}

# Export as PDF
$wdExportFormatPDF = 17
$doc.ExportAsFixedFormat($PdfPath, $wdExportFormatPDF)

$doc.Close($false)
$word.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()

Write-Output "PDF created: $PdfPath"
