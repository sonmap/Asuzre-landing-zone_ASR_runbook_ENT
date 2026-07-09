param(
  [string]$ResourceGroupName = "rg-sl-sales-prod-dr-jpe"
)

Write-Output "[DR-HEALTH-CHECK] Start"
Connect-AzAccount -Identity

$vms = Get-AzVM -ResourceGroupName $ResourceGroupName -Status
foreach ($vm in $vms) {
  $power = ($vm.Statuses | Where-Object { $_.Code -like "PowerState/*" }).DisplayStatus
  Write-Output "$($vm.Name) : $power"
}

Write-Output "[TODO] Add TCP port check for DB/WAS/WEB and application URL check."
Write-Output "[DR-HEALTH-CHECK] Completed"
