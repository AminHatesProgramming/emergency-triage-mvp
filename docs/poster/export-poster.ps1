$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$poster = Resolve-Path (Join-Path $PSScriptRoot "a0-poster.html")
$output = Join-Path $PSScriptRoot "emergency-triage-a0-poster.pdf"
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"

if (Test-Path $edge) {
  $browser = $edge
} elseif (Test-Path $chrome) {
  $browser = $chrome
} else {
  throw "Chrome or Edge was not found."
}

& $browser `
  --headless `
  --disable-gpu `
  --no-pdf-header-footer `
  --print-to-pdf="$output" `
  "file:///$($poster.Path.Replace('\','/'))"

Write-Output "Poster PDF exported to: $output"
