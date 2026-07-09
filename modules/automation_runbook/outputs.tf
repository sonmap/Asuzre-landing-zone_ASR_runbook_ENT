output "automation_account_id" {
  value = azurerm_automation_account.this.id
}

output "automation_account_principal_id" {
  value = azurerm_automation_account.this.identity[0].principal_id
}

output "runbook_names" {
  value = { for k, r in azurerm_automation_runbook.this : k => r.name }
}
