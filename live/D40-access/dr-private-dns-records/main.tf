resource "azurerm_private_dns_zone" "this" {
  count               = var.create_private_dns_zone ? 1 : 0
  name                = var.private_dns_zone_name
  resource_group_name = var.dns_resource_group_name
  tags                = var.common_tags
}

locals {
  zone_name = var.private_dns_zone_name
}

resource "azurerm_private_dns_a_record" "records" {
  for_each = var.a_records

  name                = each.value.name
  zone_name           = local.zone_name
  resource_group_name = var.dns_resource_group_name
  ttl                 = each.value.ttl
  records             = each.value.records

  depends_on = [azurerm_private_dns_zone.this]
}
