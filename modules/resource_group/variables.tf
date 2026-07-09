variable "resource_groups" {
  description = "Resource Groups to create"
  type = map(object({
    name     = string
    location = string
    tags     = optional(map(string), {})
  }))
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default     = {}
}
