output "resource_group_names" {
  value = { for k, rg in azurerm_resource_group.this : k => rg.name }
}

output "resource_group_ids" {
  value = { for k, rg in azurerm_resource_group.this : k => rg.id }
}
