variable "location" {
  type        = string
  description = "Recovery Services Vault region"
}

variable "resource_group_name" {
  type        = string
  description = "Recovery Services Vault resource group"
}

variable "vault_name" {
  type        = string
  description = "Recovery Services Vault name"
}

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
