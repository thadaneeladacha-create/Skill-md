param(
    [Parameter(Mandatory=$true)][string]$MdPath,
    [Parameter(Mandatory=$true)][string]$PdfPath,
    [Parameter(Mandatory=$true)][string]$TitleText
)

# Same as md-to-pdf.ps1 but also embeds local images referenced via ![alt](relative/path.png)
# and skips ```mermaid``` code fences (Word can't render them). Use this for full how-to/hand-off
# guides that have screenshots (e.g. Projects/SPC/How to/*.md) when the Remark column of the
# weekly Excel needs to link the full guide instead of the plain daily-log PDF.

$ErrorActionPreference = "Stop"

$mdDir = Split-Path -Parent $MdPath
$lines = Get-Content -Path $MdPath -Encoding UTF8

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Add()

$sel = $word.Selection
$sel.Font.Name = "Tahoma"
$sel.Font.Size = 10

$sel.Style = "Title"
$sel.TypeText($TitleText)
$sel.TypeParagraph()
$sel.Style = "Normal"
$sel.Font.Name = "Tahoma"
$sel.Font.Size = 10

$inMermaid = $false

foreach ($raw in $lines) {
    $line = $raw.TrimEnd()

    if ($line -match '^\s*```mermaid') { $inMermaid = $true; continue }
    if ($inMermaid) {
        if ($line -match '^\s*```') { $inMermaid = $false }
        continue
    }
    if ($line -match '^\s*```') { continue }

    if ($line -match '^\s*$') {
        $sel.TypeParagraph()
        continue
    }
    if ($line -match '^---+\s*$') { continue }
    if ($line -match '^\s*🏠') { continue }

    if ($line -match '^\s*!\[([^\]]*)\]\(([^\)]+)\)') {
        $imgRel = $Matches[2]
        $imgPath = Join-Path $mdDir $imgRel
        if (Test-Path $imgPath) {
            $sel.InlineShapes.AddPicture($imgPath) | Out-Null
            $sel.TypeParagraph()
        }
        continue
    }

    $clean = $line -replace '\*\*', '' -replace '`', ''
    $clean = $clean -replace '\[\[([^\]]+)\]\]', '$1'
    $clean = $clean -replace '\[([^\]]+)\]\(([^\)]+)\)', '$1 ($2)'

    if ($clean -match '^####\s+(.*)') {
        $sel.Style = "Heading 4"; $sel.Font.Name = "Tahoma"; $sel.TypeText($Matches[1]); $sel.TypeParagraph()
    }
    elseif ($clean -match '^###\s+(.*)') {
        $sel.Style = "Heading 3"; $sel.Font.Name = "Tahoma"; $sel.TypeText($Matches[1]); $sel.TypeParagraph()
    }
    elseif ($clean -match '^##\s+(.*)') {
        $sel.Style = "Heading 2"; $sel.Font.Name = "Tahoma"; $sel.TypeText($Matches[1]); $sel.TypeParagraph()
    }
    elseif ($clean -match '^#\s+(.*)') {
        $sel.Style = "Heading 1"; $sel.Font.Name = "Tahoma"; $sel.TypeText($Matches[1]); $sel.TypeParagraph()
    }
    elseif ($clean -match '^\s*-\s*\[x\]\s*(.*)') {
        $sel.Style = "Normal"; $sel.Font.Name = "Tahoma"; $sel.Font.Size = 10
        $sel.TypeText("[Done] " + $Matches[1]); $sel.TypeParagraph()
    }
    elseif ($clean -match '^\s*-\s*\[\s\]\s*(.*)') {
        $sel.Style = "Normal"; $sel.Font.Name = "Tahoma"; $sel.Font.Size = 10
        $sel.TypeText("[Open] " + $Matches[1]); $sel.TypeParagraph()
    }
    elseif ($clean -match '^\s*[-*]\s+(.*)') {
        $sel.Style = "List Bullet"; $sel.Font.Name = "Tahoma"; $sel.Font.Size = 10
        $sel.TypeText($Matches[1]); $sel.TypeParagraph()
    }
    elseif ($clean -match '^\s*\d+\.\s+(.*)') {
        $sel.Style = "List Number"; $sel.Font.Name = "Tahoma"; $sel.Font.Size = 10
        $sel.TypeText($Matches[1]); $sel.TypeParagraph()
    }
    elseif ($clean -match '^\|') {
        $sel.Style = "Normal"; $sel.Font.Name = "Consolas"; $sel.Font.Size = 8
        $sel.TypeText($clean); $sel.TypeParagraph()
        $sel.Font.Name = "Tahoma"; $sel.Font.Size = 10
    }
    else {
        $sel.Style = "Normal"; $sel.Font.Name = "Tahoma"; $sel.Font.Size = 10
        $sel.TypeText($clean); $sel.TypeParagraph()
    }
}

$wdExportFormatPDF = 17
$doc.ExportAsFixedFormat($PdfPath, $wdExportFormatPDF)

$doc.Close($false)
$word.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()

Write-Output "PDF created: $PdfPath"
