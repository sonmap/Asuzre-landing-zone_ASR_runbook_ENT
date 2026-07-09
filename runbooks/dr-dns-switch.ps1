param(
  [string]$DnsResourceGroupName = "rg-sl-dr-hub-jpe",
  [string]$PrivateDnsZoneName = "corp.internal",
  [string]$RecordName = "sales",
  [string]$DrIpAddress = "10.120.0.10"
)

Write-Output "[DR-DNS-SWITCH] Start"
Connect-AzAccount -Identity
Write-Output "Switch $RecordName.$PrivateDnsZoneName to $DrIpAddress"
Write-Output "[TODO] Add Private DNS record update logic after actual DNS zone is confirmed."
