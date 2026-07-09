variable "dns_resource_group_name" {
  type        = string
  description = "Resource Group for DR Private DNS"
}

variable "private_dns_zone_name" {
  type        = string
  description = "Private DNS zone name"
}

variable "create_private_dns_zone" {
  type        = bool
  default     = false
  description = "Create zone if true. Set false when zone already exists."
}

variable "a_records" {
  type = map(object({
    name    = string
    ttl     = number
    records = list(string)
  }))
  default = {}
}

variable "common_tags" {
  type    = map(string)
  default = {}
}
