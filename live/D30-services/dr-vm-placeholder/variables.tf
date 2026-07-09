variable "dr_vm_mapping" {
  description = "Source VM to DR subnet mapping. This root does not create DR VMs. ASR creates VMs during failover."
  type = map(object({
    source_vm_name   = string
    role             = string
    source_subnet    = string
    target_subnet    = string
    recovery_group   = number
    create_by        = string
  }))
}
