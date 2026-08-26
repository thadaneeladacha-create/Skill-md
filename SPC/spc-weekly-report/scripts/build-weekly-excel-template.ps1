<#
Reference template for building the weekly Excel report to match the exact visual style of
X:\QM\IMS\Thada\Report\Week6\ThadaN.090077.xlsx (confirmed via Excel COM inspection 2026-08-21,
colors decoded with [System.Drawing.ColorTranslator]::FromOle — do NOT eyeball colors, always
decode them this way since Excel's .Interior.Color / .Font.Color use OLE BGR-packed ints).

This is a REFERENCE/STARTING POINT, not a blind fire-and-forget script — always adapt the $data
array to the actual week's daily logs before running, and re-verify column widths/row count
against the current WeekN-1 file in case the format evolves.

Confirmed style spec (Week6, 2026-08-21):
  - Font: Calibri throughout (11pt body, 14pt bold title)
  - NAVY  #002060 - title text, header row fill, "holiday" row fill (with white bold text)
  - CORAL #F23A73 - "Update: <date>" badge fill (row 1, col H), white bold text, centered
  - GOLD  #FFE699 - Status column fill when status = "In-progress"
  - GREEN #A9D08E - Status column fill when status = "Completed"
  - Header row (row 3): white bold text on NAVY fill, centered H+V
  - Data rows: centered H+V for all columns EXCEPT Summary (col E) which is left-H / top-V
  - Summary column (E) body text font color = NAVY (not black)
  - WW column (col A) is MERGED across all data rows of the week, single "WWxx" value, centered
  - No explicit cell borders — relies on Excel's default gridlines (DisplayGridlines = True)
  - Remark column (col J): hyperlink per row, address = relative filename only (same folder as
    the .xlsx), textToDisplay = "For more detail please follow link :" (verbatim every time)
#>

param(
    [Parameter(Mandatory=$true)][string]$OutputPath,   # e.g. X:\QM\IMS\Thada\Report\WeekN\ThadaN.090077.xlsx
    [Parameter(Mandatory=$true)][string]$WeekTitle,     # e.g. "Training Report - Week 7 (WW34)"
    [Parameter(Mandatory=$true)][string]$UpdateBadge,   # e.g. "Update: 21 Aug 2026"
    [Parameter(Mandatory=$true)][string]$WWLabel,       # e.g. "WW34" (merged into col A)
    [Parameter(Mandatory=$true)][array]$Rows            # array of hashtables, see $data example below
)
<#
Each element of $Rows: @{ Day="Mon"; Date="08/17/2026"; Activity="..."; Summary="bullet text with `n";
                          Instructor="Self"; Method="..."; Tasks="..."; Status="Completed"|"In-progress"|"";
                          Remark="filename.pdf" (relative, blank string = no hyperlink) }
Build Summary bullets with: "$([char]8226) point one$([char]10)$([char]8226) point two"
For a holiday/no-activity day, set Day/Date but leave Activity/Summary/etc blank AND set
Status = "" — then after the loop, manually fill that row navy/white per the Week6 pattern
(see SKILL.md section 3 for the exact holiday-row snippet).
#>

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$wb = $excel.Workbooks.Add()
$ws = $wb.Sheets(1)
$ws.Name = "Thada"

$NAVY  = [System.Drawing.ColorTranslator]::ToOle([System.Drawing.Color]::FromArgb(0,32,96))
$CORAL = [System.Drawing.ColorTranslator]::ToOle([System.Drawing.Color]::FromArgb(242,58,115))
$GOLD  = [System.Drawing.ColorTranslator]::ToOle([System.Drawing.Color]::FromArgb(255,230,153))
$GREEN = [System.Drawing.ColorTranslator]::ToOle([System.Drawing.Color]::FromArgb(169,208,142))
$WHITE = [System.Drawing.ColorTranslator]::ToOle([System.Drawing.Color]::White)

$xlCenter = -4108
$xlLeft   = 1
$xlTop    = -4160

# Row 1: Title + Update badge
$ws.Cells.Item(1,1).Value2 = $WeekTitle
$ws.Cells.Item(1,1).Font.Name = "Calibri"
$ws.Cells.Item(1,1).Font.Bold = $true
$ws.Cells.Item(1,1).Font.Size = 14
$ws.Cells.Item(1,1).Font.Color = $NAVY

$ws.Cells.Item(1,8).Value2 = $UpdateBadge
$ws.Cells.Item(1,8).Font.Name = "Calibri"
$ws.Cells.Item(1,8).Font.Bold = $true
$ws.Cells.Item(1,8).Font.Color = $WHITE
$ws.Cells.Item(1,8).Interior.Color = $CORAL
$ws.Cells.Item(1,8).HorizontalAlignment = $xlCenter

# Row 3: Header
$headers = @("WW","Day","Date","Activity","Summary","Instructor","Training Method","Assigned tasks","Status of Assigned Tasks","Remark")
for ($c=1; $c -le 10; $c++) {
  $cell = $ws.Cells.Item(3,$c)
  $cell.Value2 = $headers[$c-1]
  $cell.Font.Name = "Calibri"; $cell.Font.Bold = $true; $cell.Font.Size = 11
  $cell.Font.Color = $WHITE
  $cell.Interior.Color = $NAVY
  $cell.HorizontalAlignment = $xlCenter
  $cell.VerticalAlignment = $xlCenter
}

$r = 4
foreach ($row in $Rows) {
  $ws.Cells.Item($r,2).Value2 = $row.Day
  $ws.Cells.Item($r,3).Value2 = $row.Date
  $ws.Cells.Item($r,4).Value2 = $row.Activity
  $ws.Cells.Item($r,5).Value2 = $row.Summary
  $ws.Cells.Item($r,6).Value2 = $row.Instructor
  $ws.Cells.Item($r,7).Value2 = $row.Method
  $ws.Cells.Item($r,8).Value2 = $row.Tasks
  $ws.Cells.Item($r,9).Value2 = $row.Status

  $rng = $ws.Range("A$r`:J$r")
  $rng.Font.Name = "Calibri"; $rng.Font.Size = 11
  $rng.HorizontalAlignment = $xlCenter
  $rng.VerticalAlignment = $xlCenter
  $rng.WrapText = $true

  $sCell = $ws.Cells.Item($r,5)
  $sCell.HorizontalAlignment = $xlLeft
  $sCell.VerticalAlignment = $xlTop
  $sCell.Font.Color = $NAVY

  $statusCell = $ws.Cells.Item($r,9)
  if ($row.Status -eq "Completed") { $statusCell.Interior.Color = $GREEN }
  elseif ($row.Status -eq "In-progress") { $statusCell.Interior.Color = $GOLD }

  if ($row.Remark) {
    $ws.Hyperlinks.Add($ws.Cells.Item($r,10), $row.Remark, "", "", "For more detail please follow link :") | Out-Null
  }

  $r++
}
$lastRow = $r - 1

# Merge WW column across all data rows
$ws.Range("A4:A$lastRow").Merge()
$ws.Cells.Item(4,1).Value2 = $WWLabel
$ws.Cells.Item(4,1).Font.Name = "Calibri"
$ws.Cells.Item(4,1).Font.Size = 11
$ws.Cells.Item(4,1).HorizontalAlignment = $xlCenter
$ws.Cells.Item(4,1).VerticalAlignment = $xlCenter

# Column widths (write each individually — do NOT loop over a mixed-type array, see COM gotcha in SKILL.md)
$ws.Columns.Item(1).ColumnWidth = 8
$ws.Columns.Item(2).ColumnWidth = 6
$ws.Columns.Item(3).ColumnWidth = 10
$ws.Columns.Item(4).ColumnWidth = 34
$ws.Columns.Item(5).ColumnWidth = 60
$ws.Columns.Item(6).ColumnWidth = 30
$ws.Columns.Item(7).ColumnWidth = 25.71
$ws.Columns.Item(8).ColumnWidth = 30
$ws.Columns.Item(9).ColumnWidth = 22
$ws.Columns.Item(10).ColumnWidth = 31.71

$ws.Rows.Item(1).RowHeight = 18.75
$ws.Rows.Item(2).RowHeight = 15
$ws.Rows.Item(3).RowHeight = 15
# Row heights 4..lastRow: set per-row based on Summary text length, ~60-90pt is typical — adjust manually after reviewing wrap

$ws.PageSetup.Orientation = 1
$ws.PageSetup.FitToPagesWide = 1
$ws.PageSetup.FitToPagesTall = 1

if (Test-Path $OutputPath) { Remove-Item $OutputPath -Force }
$wb.SaveAs($OutputPath)
$wb.Close($false)
$excel.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ws) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($wb) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
[GC]::Collect()
[GC]::WaitForPendingFinalizers()
Write-Output "DONE: $OutputPath"
