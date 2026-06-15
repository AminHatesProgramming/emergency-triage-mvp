param(
  [string]$Repo = "AminHatesProgramming/emergency-triage-mvp",
  [string]$Owner = "AminHatesProgramming",
  [string]$ProjectTitle = "Emergency Triage MVP - Agile Board",
  [string]$IssueSeed = "docs/artifacts/work-management-board.csv"
)

$ErrorActionPreference = "Stop"

function Require-Command($Name) {
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
    throw "Required command '$Name' was not found. Install GitHub CLI from https://cli.github.com/ and run: gh auth login"
  }
}

Require-Command gh

Write-Host "Checking GitHub authentication..."
gh auth status | Out-Host

if (-not (Test-Path -LiteralPath $IssueSeed)) {
  throw "Issue seed file not found: $IssueSeed"
}

$labels = @(
  @{ name = "status: done"; color = "17845B"; description = "Completed project-management item" },
  @{ name = "status: todo"; color = "B77A0B"; description = "Planned item for upcoming sprint" },
  @{ name = "sprint: 0"; color = "D6F5F5"; description = "Sprint 0" },
  @{ name = "sprint: 1"; color = "D6F5F5"; description = "Sprint 1" },
  @{ name = "sprint: 2"; color = "D6F5F5"; description = "Sprint 2" },
  @{ name = "sprint: 3"; color = "D6F5F5"; description = "Sprint 3" },
  @{ name = "sprint: 4"; color = "D6F5F5"; description = "Sprint 4" },
  @{ name = "sprint: 5"; color = "D6F5F5"; description = "Sprint 5" },
  @{ name = "area: model"; color = "575BC3"; description = "ML/model work" },
  @{ name = "area: product"; color = "087F8C"; description = "API/UI/product work" },
  @{ name = "area: pm"; color = "0B2545"; description = "Project management evidence" },
  @{ name = "area: docs"; color = "667781"; description = "Documentation and knowledge base" },
  @{ name = "area: feedback"; color = "C93535"; description = "Stakeholder feedback" }
)

Write-Host "Creating labels..."
foreach ($label in $labels) {
  gh label create $label.name --repo $Repo --color $label.color --description $label.description --force | Out-Null
}

$rows = Import-Csv -LiteralPath $IssueSeed
$createdIssues = @()

Write-Host "Creating GitHub issues from $IssueSeed..."
foreach ($row in $rows) {
  $title = if ($row.Title) { $row.Title } else { $row.Task }
  $statusLabel = if ($row.Status -eq "Done") { "status: done" } else { "status: todo" }
  $sprintNumber = ($row.Sprint -replace "[^0-9]", "")
  $sprintLabel = "sprint: $sprintNumber"
  $areaLabel = if ($title -match "model|Train|feature") {
    "area: model"
  } elseif ($title -match "UI|API|MVP|PWA") {
    "area: product"
  } elseif ($title -match "feedback|Stakeholder") {
    "area: feedback"
  } elseif ($title -match "document|Word|poster|Knowledge") {
    "area: docs"
  } else {
    "area: pm"
  }

  $body = @"
Owner: $($row.Owner)
Sprint: $($row.Sprint)
Status: $($row.Status)
Story Points: $($row.'Story Points')
Estimated Hours: $($row.'Estimated Hours')
Time Spent Hours: $($row.'Time Spent Hours')
Start Date: $($row.'Start Date')
Done Date: $($row.'Done Date')
Deliverable: $($row.Deliverable)
Evidence: $($row.Evidence)
Future Task: $($row.'Future Task')

Acceptance checklist:
- [ ] Owner is clear
- [ ] Deliverable is visible in repository or live tool
- [ ] Evidence link is available for final presentation
- [ ] Time tracking is recorded
- [ ] Review/status has been updated before final submission
"@

  $issueUrl = gh issue create `
    --repo $Repo `
    --title $title `
    --body $body `
    --label $statusLabel `
    --label $sprintLabel `
    --label $areaLabel

  $createdIssues += $issueUrl

  if ($row.Status -eq "Done") {
    gh issue close $issueUrl --repo $Repo --comment "Closed as completed based on sprint evidence in repository docs." | Out-Null
  }
}

Write-Host "Attempting to create GitHub Projects board..."
$projectUrl = $null
try {
  $projectJson = gh project create --owner $Owner --title $ProjectTitle --format json
  $project = $projectJson | ConvertFrom-Json
  $projectUrl = $project.url
  Write-Host "Project created: $projectUrl"

  foreach ($issueUrl in $createdIssues) {
    gh project item-add $project.number --owner $Owner --url $issueUrl | Out-Null
  }
} catch {
  Write-Warning "Issues were created, but GitHub Project creation/item-add failed. This often means gh auth needs the 'project' scope."
  Write-Warning "Run: gh auth refresh -s project"
  Write-Warning "Then rerun this script."
}

Write-Host ""
Write-Host "Work management setup complete."
Write-Host "Repo issues: https://github.com/$Repo/issues"
if ($projectUrl) {
  Write-Host "Project board: $projectUrl"
}
