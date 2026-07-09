module "dr_sales_spoke" {
  source = "../../../modules/dr_network"

  vnet_name           = var.vnet_name
  location            = var.location
  resource_group_name = var.resource_group_name
  address_space       = var.address_space
  dns_servers         = var.dns_servers
  subnets             = var.subnets
  remote_vnet_id      = var.dr_hub_vnet_id
  tags                = var.common_tags
}
