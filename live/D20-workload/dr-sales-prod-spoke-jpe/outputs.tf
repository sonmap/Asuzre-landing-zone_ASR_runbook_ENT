output "dr_spoke_vnet_id" {
  value = module.dr_sales_spoke.vnet_id
}

output "dr_spoke_vnet_name" {
  value = module.dr_sales_spoke.vnet_name
}

output "dr_spoke_subnet_ids" {
  value = module.dr_sales_spoke.subnet_ids
}

output "asr_target_subnet_mapping" {
  value = {
    web   = module.dr_sales_spoke.subnet_ids["web"]
    was   = module.dr_sales_spoke.subnet_ids["was"]
    db    = module.dr_sales_spoke.subnet_ids["db"]
    pe    = module.dr_sales_spoke.subnet_ids["pe"]
    agent = module.dr_sales_spoke.subnet_ids["agent"]
  }
}
