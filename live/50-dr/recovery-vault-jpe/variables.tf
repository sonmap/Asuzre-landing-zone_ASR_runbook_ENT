variable "vault_name" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "sku" {
  type    = string
  default = "Standard"
}
variable "soft_delete_enabled" {
  type    = bool
  default = true
}
variable "common_tags" {
  type    = map(string)
  default = {}
}
