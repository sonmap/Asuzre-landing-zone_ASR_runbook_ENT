resource "azurerm_automation_account" "this" {
  name                = var.automation_account_name
  location            = var.location
  resource_group_name = var.resource_group_name
  sku_name            = "Basic"
  tags                = var.tags

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_automation_runbook" "this" {
  for_each = var.runbooks

  name                    = each.value.name
  location                = var.location
  resource_group_name     = var.resource_group_name
  automation_account_name = azurerm_automation_account.this.name
  log_verbose             = true
  log_progress            = true
  description             = each.value.description
  runbook_type            = each.value.runbook_type
  content                 = file(each.value.script_path)
  tags                    = var.tags
}
