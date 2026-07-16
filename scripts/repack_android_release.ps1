param(
    [string]$JavaHome = "F:\neo4j\distributions\java\zulu17.50.19-ca-jdk17.0.11",
    [string]$AndroidSdk = "C:\Users\Webhouse\AppData\Local\Android\Sdk"
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$dist = Join-Path $root "dist"
$androidApp = Join-Path $root "android-app"
$release = Join-Path $root "docs\market\release"
$work = Join-Path $root ".tools\android-release-repack"

if (-not (Test-Path -LiteralPath (Join-Path $dist "index.html"))) {
    throw "dist/index.html is missing. Run scripts/build_pages.py first."
}

if (Test-Path -LiteralPath $work) {
    $resolvedWork = (Resolve-Path -LiteralPath $work).Path
    if (-not $resolvedWork.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to clean a path outside the workspace: $resolvedWork"
    }
    Remove-Item -LiteralPath $resolvedWork -Recurse -Force
}

$keystoreFile = Join-Path $androidApp "keystore.properties"
if (-not (Test-Path -LiteralPath $keystoreFile)) {
    throw "android-app/keystore.properties is required for release signing."
}
$keystore = ConvertFrom-StringData (Get-Content -LiteralPath $keystoreFile -Raw -Encoding UTF8)

$buildTools = Join-Path $AndroidSdk "build-tools\36.0.0"
$zipalign = Join-Path $buildTools "zipalign.exe"
$apksigner = Join-Path $buildTools "apksigner.bat"
$jar = Join-Path $JavaHome "bin\jar.exe"
$jarsigner = Join-Path $JavaHome "bin\jarsigner.exe"
@($zipalign, $apksigner, $jar, $jarsigner, $keystore.storeFile) | ForEach-Object {
    if (-not (Test-Path -LiteralPath $_)) { throw "Required tool or key not found: $_" }
}

$sourceApk = Join-Path $androidApp "app\build\outputs\apk\release\app-release.apk"
$sourceAab = Join-Path $androidApp "app\build\outputs\bundle\release\app-release.aab"
@($sourceApk, $sourceAab) | ForEach-Object {
    if (-not (Test-Path -LiteralPath $_)) { throw "Base release artifact not found: $_" }
}

$apkStage = Join-Path $work "apk-stage\assets\www"
$aabStage = Join-Path $work "aab-stage\base\assets\www"
New-Item -ItemType Directory -Path $apkStage, $aabStage, $release -Force | Out-Null
Copy-Item -Path (Join-Path $dist "*") -Destination $apkStage -Recurse -Force
Copy-Item -Path (Join-Path $dist "*") -Destination $aabStage -Recurse -Force

$updatedApk = Join-Path $work "updated-unsigned.apk"
$alignedApk = Join-Path $work "updated-aligned.apk"
$signedApk = Join-Path $work "Emdadyar-1.0.0-release.apk"
$updatedAab = Join-Path $work "updated-unsigned.aab"
$signedAab = Join-Path $work "Emdadyar-1.0.0-release.aab"
Copy-Item -LiteralPath $sourceApk -Destination $updatedApk -Force
Copy-Item -LiteralPath $sourceAab -Destination $updatedAab -Force

& $jar uf $updatedApk -C (Join-Path $work "apk-stage") .
if ($LASTEXITCODE -ne 0) { throw "Unable to update APK web assets." }
& $zipalign -f -p 4 $updatedApk $alignedApk
if ($LASTEXITCODE -ne 0) { throw "zipalign failed." }
& $apksigner sign `
    --ks $keystore.storeFile `
    --ks-key-alias $keystore.keyAlias `
    --ks-pass "pass:$($keystore.storePassword)" `
    --key-pass "pass:$($keystore.keyPassword)" `
    --v1-signing-enabled true `
    --v2-signing-enabled true `
    --v3-signing-enabled true `
    --out $signedApk `
    $alignedApk
if ($LASTEXITCODE -ne 0) { throw "APK signing failed." }
& $zipalign -c -p 4 $signedApk
if ($LASTEXITCODE -ne 0) { throw "Signed APK alignment verification failed." }
& $apksigner verify --verbose --print-certs $signedApk
if ($LASTEXITCODE -ne 0) { throw "Signed APK verification failed." }

& $jar uf $updatedAab -C (Join-Path $work "aab-stage") .
if ($LASTEXITCODE -ne 0) { throw "Unable to update AAB web assets." }
& $jarsigner `
    -keystore $keystore.storeFile `
    -storepass $keystore.storePassword `
    -keypass $keystore.keyPassword `
    -signedjar $signedAab `
    $updatedAab `
    $keystore.keyAlias
if ($LASTEXITCODE -ne 0) { throw "AAB signing failed." }
& $jarsigner -verify -verbose -certs $signedAab
if ($LASTEXITCODE -ne 0) { throw "Signed AAB verification failed." }

Copy-Item -LiteralPath $signedApk -Destination (Join-Path $release "Emdadyar-1.0.0-release.apk") -Force
Copy-Item -LiteralPath $signedAab -Destination (Join-Path $release "Emdadyar-1.0.0-release.aab") -Force

Get-FileHash -Algorithm SHA256 $signedApk, $signedAab | Select-Object Path, Hash
