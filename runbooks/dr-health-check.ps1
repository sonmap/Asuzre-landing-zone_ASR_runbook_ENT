param([string]$ResourceGroupName = "rg-sl-sales-prod-dr-jpe")
Write-Output "[DR-HEALTH-CHECK] Start"
Connect-AzAccount -Identity
Get-AzVM -ResourceGroupName $ResourceGroupName -Status | Select-Object Name, PowerState
Write-Output "[DR-HEALTH-CHECK] Completed"
