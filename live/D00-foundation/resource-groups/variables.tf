variable "resource_groups" {
  type = map(object({
    name     = string
    location = string
    tags     = optional(map(string), {})
  }))
}

variable "common_tags" {
  type    = map(string)
  default = {}
}
