variable "vnet_name" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "address_space" { type = list(string) }
variable "dns_servers" {
  type    = list(string)
  default = []
}
variable "remote_vnet_id" {
  type    = string
  default = null
}
variable "subnets" {
  type = map(object({
    name             = string
    address_prefixes = list(string)
    create_nsg       = optional(bool, true)
  }))
}
variable "tags" {
  type    = map(string)
  default = {}
}
