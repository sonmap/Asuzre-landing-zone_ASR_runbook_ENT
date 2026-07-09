param(
  [string]$ResourceGroupName = "rg-sl-sales-prod-dr-jpe"
)

Write-Output "[DR-INVENTORY-UPDATE] Start"
Connect-AzAccount -Identity

$resources = Get-AzResource -ResourceGroupName $ResourceGroupName | Select-Object Name, ResourceType, Location, ResourceId, Tags
$inventory = $resources | ConvertTo-Json -Depth 10

Write-Output $inventory
Write-Output "[TODO] Send inventory JSON to Storage Account, Log Analytics, ITSM or CMDB API."
Write-Output "[DR-INVENTORY-UPDATE] Completed"
