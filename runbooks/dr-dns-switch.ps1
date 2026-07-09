param(
  [string]$DnsResourceGroupName = "rg-sl-dr-hub-jpe",
  [string]$PrivateDnsZoneName = "corp.internal",
  [string]$RecordName = "sales",
  [string]$DrIpAddress = "10.120.0.10"
)

Write-Output "[DR-DNS-SWITCH] Start"
Connect-AzAccount -Identity

$zone = Get-AzPrivateDnsZone -ResourceGroupName $DnsResourceGroupName -Name $PrivateDnsZoneName -ErrorAction SilentlyContinue
if (-not $zone) {
  throw "Private DNS Zone not found: $PrivateDnsZoneName"
}

$record = Get-AzPrivateDnsRecordSet -ResourceGroupName $DnsResourceGroupName -ZoneName $PrivateDnsZoneName -Name $RecordName -RecordType A -ErrorAction SilentlyContinue
if ($record) {
  Remove-AzPrivateDnsRecordSet -ResourceGroupName $DnsResourceGroupName -ZoneName $PrivateDnsZoneName -Name $RecordName -RecordType A -Force
}

New-AzPrivateDnsRecordSet -ResourceGroupName $DnsResourceGroupName -ZoneName $PrivateDnsZoneName -Name $RecordName -RecordType A -Ttl 60 -PrivateDnsRecords (New-AzPrivateDnsRecordConfig -IPv4Address $DrIpAddress)

Write-Output "DNS switched: $RecordName.$PrivateDnsZoneName -> $DrIpAddress"
Write-Output "[DR-DNS-SWITCH] Completed"
