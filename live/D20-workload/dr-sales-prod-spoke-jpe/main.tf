module "dr_sales_spoke" {
  source = "../../../modules/workload_spoke"

  name                    = var.vnet_name
  location                = var.location
  resource_group_name     = var.resource_group_name
  address_space           = var.address_space
  dns_servers             = var.dns_servers
  hub_vnet_id             = var.dr_hub_vnet_id
  hub_resource_group_name = var.dr_hub_resource_group_name
  hub_vnet_name           = var.dr_hub_vnet_name
  firewall_private_ip     = var.dr_firewall_private_ip
  subnets                 = var.subnets
  tags                    = var.common_tags
}
