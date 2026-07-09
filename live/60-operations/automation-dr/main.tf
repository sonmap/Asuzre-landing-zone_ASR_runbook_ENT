module "automation_dr" {
  source = "../../../modules/automation_runbook"

  automation_account_name = var.automation_account_name
  location                = var.location
  resource_group_name     = var.resource_group_name
  runbooks                = var.runbooks
  tags                    = var.common_tags
}
