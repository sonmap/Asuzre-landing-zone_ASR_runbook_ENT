param(
  [string]$ResourceGroupName = "rg-sl-sales-prod-dr-jpe",
  [string]$VaultResourceGroupName = "rg-sl-dr-asr-jpe",
  [string]$VaultName = "rsv-sl-asr-jpe"
)

Write-Output "[DR-PRECHECK] Start"
Write-Output "Target Resource Group: $ResourceGroupName"
Write-Output "Recovery Vault: $VaultName"

try {
  Connect-AzAccount -Identity
  Write-Output "Managed Identity login succeeded."
}
catch {
  throw "Managed Identity login failed: $_"
}

$rg = Get-AzResourceGroup -Name $ResourceGroupName -ErrorAction SilentlyContinue
if (-not $rg) {
  throw "Target Resource Group not found: $ResourceGroupName"
}

$vault = Get-AzRecoveryServicesVault -ResourceGroupName $VaultResourceGroupName -Name $VaultName -ErrorAction SilentlyContinue
if (-not $vault) {
  throw "Recovery Services Vault not found: $VaultName"
}

Write-Output "[OK] Resource Group and Recovery Vault exist."
Write-Output "[TODO] Add quota, subnet, ASR replication health, DNS pre-check."
Write-Output "[DR-PRECHECK] Completed"
