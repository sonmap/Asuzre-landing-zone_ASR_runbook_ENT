param(
  [string]$ResourceGroupName = "rg-sl-sales-prod-dr-jpe",
  [string]$VaultResourceGroupName = "rg-sl-dr-asr-jpe",
  [string]$VaultName = "rsv-sl-asr-jpe"
)

Write-Output "[DR-PRECHECK] Start"
Connect-AzAccount -Identity
Get-AzResourceGroup -Name $ResourceGroupName -ErrorAction Stop | Out-Null
Get-AzRecoveryServicesVault -ResourceGroupName $VaultResourceGroupName -Name $VaultName -ErrorAction Stop | Out-Null
Write-Output "[DR-PRECHECK] Completed"
