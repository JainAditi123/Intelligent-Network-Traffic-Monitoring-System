# make_submission_zip.ps1
# Creates DDoS_Monitoring_Final.zip on the Desktop,
# preserving subfolder structure and excluding venv/ and __pycache__/

$source  = $PSScriptRoot                                   # project root
$dest    = Join-Path (Split-Path $source -Parent) "DDoS_Monitoring_Final.zip"

# Remove old ZIP if it exists
if (Test-Path $dest) { Remove-Item $dest -Force }

Add-Type -Assembly System.IO.Compression.FileSystem

$zip = [System.IO.Compression.ZipFile]::Open(
    $dest,
    [System.IO.Compression.ZipArchiveMode]::Create
)

$files = Get-ChildItem -Path $source -Recurse -File |
    Where-Object {
        $_.FullName -notmatch '\\venv\\'          -and
        $_.FullName -notmatch '\\__pycache__\\'   -and
        $_.Name    -ne 'make_submission_zip.ps1'
    }

foreach ($file in $files) {
    # Relative path inside the zip, rooted at DDoS_Monitoring/
    $relative = "DDoS_Monitoring\" + $file.FullName.Substring($source.Length + 1)
    Write-Host "  Adding: $relative"
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
        $zip, $file.FullName, $relative,
        [System.IO.Compression.CompressionLevel]::Optimal
    ) | Out-Null
}

$zip.Dispose()

$sizeMB = [math]::Round((Get-Item $dest).Length / 1MB, 2)
Write-Host ""
Write-Host "ZIP created : $dest"
Write-Host "Size        : $sizeMB MB"
