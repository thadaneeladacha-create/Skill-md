param(
    [Parameter(Mandatory=$true)][string]$PdfPath,
    [Parameter(Mandatory=$true)][string]$OutDir,
    [Parameter(Mandatory=$true)][int]$StartPage,
    [Parameter(Mandatory=$true)][int]$EndPage
)

Add-Type -AssemblyName System.Runtime.WindowsRuntime

$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetGenericArguments().Count -eq 1
})[0]

function Await($WinRtTask, $ResultType) {
    $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
    $task = $asTask.Invoke($null, @($WinRtTask))
    $task.Wait() | Out-Null
    return $task.Result
}

function AwaitAction($WinRtAction) {
    $asTaskAction = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
        $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and -not $_.IsGenericMethod
    })[0]
    $task = $asTaskAction.Invoke($null, @($WinRtAction))
    $task.Wait() | Out-Null
}

[void][Windows.Data.Pdf.PdfDocument,Windows.Data.Pdf,ContentType=WindowsRuntime]
[void][Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
[void][Windows.Storage.Streams.RandomAccessStreamReference,Windows.Storage.Streams,ContentType=WindowsRuntime]

$storageFileType = [Windows.Storage.StorageFile]
$getFileTask = $storageFileType::GetFileFromPathAsync($PdfPath)
$file = Await $getFileTask ([Windows.Storage.StorageFile])

$pdfDocType = [Windows.Data.Pdf.PdfDocument]
$loadTask = $pdfDocType::LoadFromFileAsync($file)
$pdfDoc = Await $loadTask ([Windows.Data.Pdf.PdfDocument])

Write-Output "PageCount: $($pdfDoc.PageCount)"

if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }

$last = [Math]::Min($EndPage, $pdfDoc.PageCount)
for ($i = $StartPage; $i -le $last; $i++) {
    $page = $pdfDoc.GetPage($i - 1)
    $outFile = Join-Path $OutDir ("page-{0:D3}.png" -f $i)
    if (-not (Test-Path $outFile)) { New-Item -ItemType File -Path $outFile -Force | Out-Null }
    $file2 = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($outFile)) ([Windows.Storage.StorageFile])
    $streamTask = $file2.OpenAsync([Windows.Storage.FileAccessMode]::ReadWrite)
    $stream = Await $streamTask ([Windows.Storage.Streams.IRandomAccessStream])
    $renderOptions = New-Object Windows.Data.Pdf.PdfPageRenderOptions
    $renderOptions.DestinationWidth = [uint32]1600
    $renderTask = $page.RenderToStreamAsync($stream, $renderOptions)
    AwaitAction $renderTask
    $stream.FlushAsync() | Out-Null
    $stream.Dispose()
    $page.Dispose()
    Write-Output "Rendered page $i -> $outFile"
}
