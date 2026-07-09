variable "location" {
  type        = string
  description = "Azure region for DR spoke"
}

variable "resource_group_name" {
  type        = string
  description = "DR workload resource group name"
}

variable "vnet_name" {
  type        = string
  description = "DR workload spoke VNet name"
}

variable "address_space" {
  type        = list(string)
  description = "DR workload spoke CIDR"
}

variable "dns_servers" {
  type    = list(string)
  default = []
}

variable "dr_hub_vnet_id" {
  type        = string
  description = "DR Hub VNet ID from D10 output"
}

variable "dr_hub_resource_group_name" {
  type        = string
  description = "DR Hub Resource Group name"
}

variable "dr_hub_vnet_name" {
  type        = string
  description = "DR Hub VNet name"
}

variable "dr_firewall_private_ip" {
  type        = string
  default     = null
  description = "Optional DR firewall private IP for default route"
}

variable "subnets" {
  type = map(object({
    name                              = string
    address_prefixes                  = list(string)
    create_nsg                        = optional(bool, true)
    associate_route_table             = optional(bool, true)
    private_endpoint_network_policies = optional(string)
  }))
}

variable "common_tags" {
  type    = map(string)
  default = {}
}
