resource "azurerm_virtual_network" "this" {
  name                = var.vnet_name
  location            = var.location
  resource_group_name = var.resource_group_name
  address_space       = var.address_space
  dns_servers         = var.dns_servers
  tags                = var.tags
}

resource "azurerm_subnet" "this" {
  for_each = var.subnets

  name                 = each.value.name
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = each.value.address_prefixes
}

resource "azurerm_network_security_group" "this" {
  for_each = { for k, s in var.subnets : k => s if try(s.create_nsg, true) }

  name                = "nsg-${each.value.name}"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

resource "azurerm_subnet_network_security_group_association" "this" {
  for_each = azurerm_network_security_group.this

  subnet_id                 = azurerm_subnet.this[each.key].id
  network_security_group_id = each.value.id
}

resource "azurerm_virtual_network_peering" "to_remote" {
  count = var.remote_vnet_id == null ? 0 : 1

  name                         = "peer-${var.vnet_name}-to-remote"
  resource_group_name          = var.resource_group_name
  virtual_network_name         = azurerm_virtual_network.this.name
  remote_virtual_network_id    = var.remote_vnet_id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
}
