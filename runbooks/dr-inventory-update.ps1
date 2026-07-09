param([string]$ResourceGroupName = "rg-sl-sales-prod-dr-jpe")
Write-Output "[DR-INVENTORY-UPDATE] Start"
Connect-AzAccount -Identity
Get-AzResource -ResourceGroupName $ResourceGroupName | ConvertTo-Json -Depth 10
Write-Output "[DR-INVENTORY-UPDATE] Completed"
