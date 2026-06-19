$ErrorActionPreference = "Stop"

$root = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$python = "C:\Users\Webhouse\Desktop\quera\qenv\Scripts\python.exe"
$port = if ($env:PORT) { $env:PORT } elseif ($env:TRIAGE_PORT) { $env:TRIAGE_PORT } else { "8000" }
$env:TRIAGE_HOST = "0.0.0.0"
$env:TRIAGE_PORT = $port

Write-Host "Starting Emergency Triage web app on all network interfaces..." -ForegroundColor Cyan
Write-Host "Local URL:   http://127.0.0.1:$port/" -ForegroundColor Green

$ips = Get-NetIPAddress -AddressFamily IPv4 |
  Where-Object {
    $_.IPAddress -notlike "127.*" -and
    $_.IPAddress -notlike "169.254.*" -and
    $_.PrefixOrigin -ne "WellKnown"
  } |
  Select-Object -ExpandProperty IPAddress -Unique

foreach ($ip in $ips) {
  Write-Host "Phone URL:   http://$ip`:$port/" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Keep this window open while testing on your phone." -ForegroundColor Cyan
Write-Host "For PWA installation on Android, HTTPS is required on most browsers; use a tunnel or cloud deploy for final testing." -ForegroundColor DarkYellow

Set-Location -LiteralPath $root
& $python -m uvicorn backend.main:app --host 0.0.0.0 --port $port --log-level info
