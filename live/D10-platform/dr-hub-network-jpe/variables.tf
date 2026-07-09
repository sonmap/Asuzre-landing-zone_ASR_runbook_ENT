variable "location" {
  type        = string
  description = "Azure region for DR hub"
}

variable "resource_group_name" {
  type        = string
  description = "DR hub resource group name"
}

variable "vnet_name" {
  type        = string
  description = "DR hub VNet name"
}

variable "address_space" {
  type        = list(string)
  description = "DR hub VNet CIDR"
}

variable "dns_servers" {
  type    = list(string)
  default = []
}

variable "subnets" {
  type = map(object({
    name                              = string
    address_prefixes                  = list(string)
    create_nsg                        = optional(bool, true)
    associate_route_table             = optional(bool, false)
    private_endpoint_network_policies = optional(string)
  }))
}

variable "common_tags" {
  type    = map(string)
  default = {}
}
