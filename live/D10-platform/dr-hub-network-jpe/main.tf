module "dr_hub" {
  source = "../../../modules/workload_spoke"

  name                    = var.vnet_name
  location                = var.location
  resource_group_name     = var.resource_group_name
  address_space           = var.address_space
  dns_servers             = var.dns_servers
  hub_vnet_id             = null
  hub_resource_group_name = null
  hub_vnet_name           = null
  firewall_private_ip     = null
  subnets                 = var.subnets
  tags                    = var.common_tags
}
