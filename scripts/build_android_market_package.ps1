$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$market = Join-Path $root "docs\market"
$stage = Join-Path $root ".tools\android-market-package"
$zip = Join-Path $market "Emdadyar_Android_Market_Release_1.0.0.zip"
$deliverable = Join-Path $root "docs\deliverables\Emdadyar_Market_Release_Package.zip"

if (Test-Path -LiteralPath $stage) {
    $resolvedStage = (Resolve-Path -LiteralPath $stage).Path
    if (-not $resolvedStage.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to clean a path outside the workspace: $resolvedStage"
    }
    Remove-Item -LiteralPath $resolvedStage -Recurse -Force
}
New-Item -ItemType Directory -Path $stage -Force | Out-Null

$documents = @(
    "README.md",
    "android-build-guide.md",
    "android-market-listing-fa.md",
    "android-release-checklist.md",
    "build-verification-fa.md",
    "device-test-checklist-fa.md",
    "release-notes-fa.md",
    "store-data-safety-fa.md"
)

foreach ($name in $documents) {
    $source = Join-Path $market $name
    if (-not (Test-Path -LiteralPath $source)) { throw "Missing market document: $source" }
    Copy-Item -LiteralPath $source -Destination (Join-Path $stage $name) -Force
}

Copy-Item -LiteralPath (Join-Path $root "frontend\privacy.html") -Destination (Join-Path $stage "privacy.html") -Force

Copy-Item -LiteralPath (Join-Path $market "release") -Destination (Join-Path $stage "release") -Recurse -Force
Copy-Item -LiteralPath (Join-Path $market "screenshots") -Destination (Join-Path $stage "screenshots") -Recurse -Force

Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $zip -CompressionLevel Optimal -Force
Copy-Item -LiteralPath $zip -Destination $deliverable -Force

$hash = Get-FileHash -LiteralPath $zip -Algorithm SHA256
$hashLine = "$($hash.Hash)  $([System.IO.Path]::GetFileName($zip))`n"
$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Join-Path $market "Emdadyar_Android_Market_Release_1.0.0.zip.sha256.txt"), $hashLine, $utf8)

Get-Item -LiteralPath $zip, $deliverable | Select-Object FullName, Length
$hash | Select-Object Path, Hash
