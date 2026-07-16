$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$tools = Join-Path $root ".tools\submission-package-stage"

if (Test-Path -LiteralPath $tools) {
    $resolved = (Resolve-Path -LiteralPath $tools).Path
    if (-not $resolved.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to clean a path outside the workspace: $resolved"
    }
    Remove-Item -LiteralPath $resolved -Recurse -Force
}
New-Item -ItemType Directory -Path $tools -Force | Out-Null

$pmSource = Join-Path $root "project-management-final-package"
$pmZip = Join-Path $root "project-management-final-package.zip"
Compress-Archive -Path (Join-Path $pmSource "*") -DestinationPath $pmZip -CompressionLevel Optimal -Force

$deliverables = Join-Path $root "docs\deliverables"
$officialStage = Join-Path $tools "official"
New-Item -ItemType Directory -Path $officialStage -Force | Out-Null
$officialFiles = @(
    "ITPM_Final_Report_Emergency_Triage.docx",
    "Emdadyar_Final_Presentation_Runbook.docx",
    "ITPM_Project_Governance_and_Resource_Management.docx",
    "ITPM_Final_Announcement_Compliance_Matrix.docx",
    "ITPM_Project_Management_Evidence_Package.docx",
    "ITPM_Group_Project_Info_Emdadyar.docx",
    "Emdadyar_Mobile_App_For_Professor.docx",
    "Emdadyar_Market_Release_Package.zip",
    "README.md"
)
foreach ($name in $officialFiles) {
    Copy-Item -LiteralPath (Join-Path $deliverables $name) -Destination (Join-Path $officialStage $name) -Force
}
$officialZip = Join-Path $deliverables "ITPM_Official_Deliverables.zip"
Compress-Archive -Path (Join-Path $officialStage "*") -DestinationPath $officialZip -CompressionLevel Optimal -Force

$coreStage = Join-Path $tools "core"
New-Item -ItemType Directory -Path $coreStage -Force | Out-Null
$coreMappings = @{
    $officialZip = "ITPM_Official_Deliverables.zip"
    $pmZip = "project-management-final-package.zip"
    (Join-Path $root "poster-final-assets-fa.md") = "poster-final-assets-fa.md"
    (Join-Path $root "docs\final-submission-index.md") = "README-FIRST-final-submission-index.md"
    (Join-Path $root "data\feedback\triage-nurse-feedback-confirmed.csv") = "triage-nurse-feedback-confirmed.csv"
    (Join-Path $root "docs\triage-nurse-feedback-confirmation.md") = "triage-nurse-feedback-confirmation.md"
    (Join-Path $root "docs\stakeholder-outreach-log.md") = "stakeholder-outreach-log.md"
    (Join-Path $root "docs\model-release-scenario-audit-fa.md") = "model-release-scenario-audit-fa.md"
    (Join-Path $root "reports\model\release_validation_v7.json") = "release_validation_v7.json"
    (Join-Path $root "reports\model\browser_backend_differential_v7.json") = "browser_backend_differential_v7.json"
    (Join-Path $root "docs\market\Emdadyar_Android_Market_Release_1.0.0.zip") = "Emdadyar_Android_Market_Release_1.0.0.zip"
    (Join-Path $root "docs\artifacts\burndown-final.png") = "burndown-final.png"
    (Join-Path $root "docs\artifacts\velocity-final.png") = "velocity-final.png"
    (Join-Path $root "docs\artifacts\stakeholder-engagement.png") = "stakeholder-engagement.png"
    (Join-Path $root "docs\artifacts\emdadyar-pwa-qr.png") = "emdadyar-pwa-qr.png"
    (Join-Path $root "poster-assets\ui-empty-state.png") = "ui-empty-state.png"
    (Join-Path $root "poster-assets\ui-critical-scenario.png") = "ui-critical-scenario.png"
    (Join-Path $root "poster-assets\ui-partial-input.png") = "ui-partial-input.png"
    (Join-Path $root "poster-assets\ui-mobile-view.png") = "ui-mobile-view.png"
    (Join-Path $root "poster-assets\confusion-matrix.png") = "confusion-matrix.png"
    (Join-Path $root "poster-assets\roc-curve.png") = "roc-curve.png"
    (Join-Path $root "poster-assets\precision-recall-curve.png") = "precision-recall-curve.png"
    (Join-Path $root "poster-assets\feature-importance.png") = "feature-importance.png"
}
foreach ($source in $coreMappings.Keys) {
    if (-not (Test-Path -LiteralPath $source)) { throw "Missing package input: $source" }
    Copy-Item -LiteralPath $source -Destination (Join-Path $coreStage $coreMappings[$source]) -Force
}
$coreZip = Join-Path $root "Emdadyar_Submission_Core_Ready_For_Platform_Evidence.zip"
Compress-Archive -Path (Join-Path $coreStage "*") -DestinationPath $coreZip -CompressionLevel Optimal -Force

Get-FileHash -Algorithm SHA256 $pmZip, $officialZip, $coreZip | Select-Object Path, Hash
