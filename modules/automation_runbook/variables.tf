variable "automation_account_name" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "runbooks" {
  type = map(object({
    name         = string
    description  = string
    runbook_type = string
    script_path  = string
  }))
}
variable "tags" {
  type    = map(string)
  default = {}
}
