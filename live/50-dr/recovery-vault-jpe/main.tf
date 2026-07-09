module "recovery_vault" {
  source = "../../../modules/recovery_services_vault"

  name                = var.vault_name
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = var.sku
  soft_delete_enabled = var.soft_delete_enabled
  tags                = var.common_tags
}
