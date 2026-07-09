output "dr_vm_mapping" {
  value = local.dr_vm_mapping
}

output "recovery_plan_groups" {
  value = {
    group1_db  = [for k, v in local.dr_vm_mapping : v.source_vm_name if v.recovery_group == 1]
    group2_was = [for k, v in local.dr_vm_mapping : v.source_vm_name if v.recovery_group == 2]
    group3_web = [for k, v in local.dr_vm_mapping : v.source_vm_name if v.recovery_group == 3]
  }
}
