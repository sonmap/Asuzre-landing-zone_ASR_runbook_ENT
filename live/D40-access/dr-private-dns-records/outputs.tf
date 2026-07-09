output "private_dns_zone_name" {
  value = var.private_dns_zone_name
}

output "a_record_names" {
  value = { for k, v in azurerm_private_dns_a_record.records : k => v.fqdn }
}
