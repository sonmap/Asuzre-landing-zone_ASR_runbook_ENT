#!/usr/bin/env python3
"""
Numbered Excel -> Terraform tfvars generator.

Excel sheet names are aligned with Terraform live roots:
- 00_Foundation_RG              -> live/00-foundation/resource-groups/terraform.tfvars
- 10_Platform_Hub_Network       -> live/10-platform/hub-network/terraform.tfvars
- 10_Platform_Azure_Firewall    -> live/10-platform/azure-firewall/terraform.tfvars
- 20_Workload_Spoke             -> live/20-workload/<workload>-<env>-spoke/terraform.tfvars
- 30_Service_VM                 -> live/30-services/vm-<workload>-<env>/terraform.tfvars
- 30_Service_AKS                -> live/30-services/aks-<workload>-<env>/terraform.tfvars
- 40_Access_Private_DNS         -> live/40-access/private-dns-zones/terraform.tfvars
- D00_Foundation_RG             -> live/D00-foundation/resource-groups/terraform.tfvars
- D10_Platform_DR_Hub           -> live/D10-platform/dr-hub-network-jpe/terraform.tfvars
- D20_Workload_DR_Spoke         -> live/D20-workload/dr-sales-prod-spoke-jpe/terraform.tfvars
- D30_Service_DR_VM_Map         -> live/D30-services/dr-vm-placeholder/terraform.tfvars
- D40_Access_DR_DNS             -> live/D40-access/dr-private-dns-records/terraform.tfvars
- 50_ASR_Vault                  -> live/50-asr/recovery-vault-jpe/terraform.tfvars
- 50_ASR_RecoveryPlan           -> live/50-asr/recovery-plan-sales-prod/terraform.tfvars
- 60_Operations_Runbook         -> live/60-operations/automation-dr/terraform.tfvars
- 60_Operations_Inventory       -> live/60-operations/inventory/terraform.tfvars
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import openpyxl
except ImportError as exc:
    raise SystemExit("openpyxl is required. Install with: pip install openpyxl") from exc


def rows_as_dicts(wb, sheet_name: str) -> List[Dict[str, Any]]:
    if sheet_name not in wb.sheetnames:
        return []
    ws = wb[sheet_name]
    headers: Optional[List[str]] = None
    rows: List[Dict[str, Any]] = []
    for row in ws.iter_rows(values_only=True):
        values = list(row)
        if not any(v is not None for v in values):
            continue
        if headers is None:
            headers = [str(v).strip() if v is not None else f"col_{i}" for i, v in enumerate(values)]
            continue
        item: Dict[str, Any] = {}
        for i in range(min(len(headers), len(values))):
            if headers[i] and values[i] not in (None, ""):
                item[headers[i]] = values[i]
        if item:
            rows.append(item)
    return rows


def value(row: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    idx = {str(k).strip().lower().replace(" ", "").replace("_", "").replace("-", ""): k for k in row.keys()}
    for key in keys:
        nk = key.strip().lower().replace(" ", "").replace("_", "").replace("-", "")
        real = idx.get(nk)
        if real is not None and row[real] not in (None, ""):
            return row[real]
    return default


def as_bool(raw: Any, default: bool = False) -> bool:
    if raw in (None, ""):
        return default
    return str(raw).strip().lower() in {"y", "yes", "true", "1", "사용", "예", "enabled", "enable"}


def slug(raw: Any, fallback: str = "item") -> str:
    text = str(raw or "").strip().lower()
    text = re.sub(r"[^a-z0-9가-힣]+", "-", text).strip("-")
    mapping = {"영업": "sales", "영업지원": "sales", "공통": "shared", "관리": "mgmt"}
    text = mapping.get(text, text)
    text = re.sub(r"[^a-z0-9-]+", "", text).strip("-")
    return text or fallback


def hcl_string(text: str) -> str:
    return json.dumps(str(text), ensure_ascii=False)


def hcl_key(key: Any) -> str:
    text = str(key)
    return text if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", text) else hcl_string(text)


def to_hcl(obj: Any, indent: int = 0) -> str:
    pad = " " * indent
    child = " " * (indent + 2)
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float)):
        return str(obj)
    if obj is None:
        return "null"
    if isinstance(obj, str):
        return hcl_string(obj)
    if isinstance(obj, list):
        if not obj:
            return "[]"
        return "[\n" + ",\n".join(f"{child}{to_hcl(v, indent + 2)}" for v in obj) + f"\n{pad}]"
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        lines = ["{"]
        for key in sorted(obj.keys()):
            lines.append(f"{child}{hcl_key(key)} = {to_hcl(obj[key], indent + 2)}")
        lines.append(f"{pad}}}")
        return "\n".join(lines)
    return hcl_string(str(obj))


def write_tfvars(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{key} = {to_hcl(data[key])}" for key in sorted(data.keys())]
    path.write_text("\n\n".join(lines) + "\n", encoding="utf-8")
    print(f"created: {path}")


def tags(args, workload: str, env: str = "platform") -> Dict[str, str]:
    return {
        "project": args.project,
        "env": env,
        "workload": workload,
        "managed_by": "terraform",
    }


def id_for_vnet(subscription_id: str, rg: str, vnet: str) -> str:
    return f"/subscriptions/{subscription_id}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworks/{vnet}"


def id_for_subnet(subscription_id: str, rg: str, vnet: str, subnet: str) -> str:
    return f"{id_for_vnet(subscription_id, rg, vnet)}/subnets/{subnet}"


def build_resource_groups(args, rows: List[Dict[str, Any]], location: str, default_rows: List[Dict[str, str]]) -> Dict[str, Any]:
    if not rows:
        rows = default_rows
    groups = {}
    for row in rows:
        key = slug(value(row, "key", "id", "구분", default=value(row, "name", default="rg"))).replace("-", "_")
        name = str(value(row, "name", "ResourceGroup", "resource_group_name", default="rg-replace"))
        workload = str(value(row, "workload", "업무", default="foundation"))
        env = str(value(row, "env", "Environment", default="platform"))
        groups[key] = {
            "name": name,
            "location": str(value(row, "location", "region", default=location)),
            "tags": tags(args, workload, env),
        }
    return {"tenant_id": args.tenant_id, "subscription_id": args.subscription_id, "location": location, "common_tags": tags(args, "foundation"), "resource_groups": groups}


def build_hub_network(args, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    subnets = {}
    for row in rows:
        key = slug(value(row, "key", "SubnetKey", default=value(row, "SubnetName", default="subnet"))).replace("-", "_")
        name = str(value(row, "SubnetName", "name", default="snet-replace"))
        subnets[key] = {
            "name": name,
            "address_prefixes": [str(value(row, "CIDR", "address_prefix", default="10.39.0.0/24"))],
            "create_nsg": as_bool(value(row, "create_nsg", "NSG", default=False), False),
        }
        if as_bool(value(row, "delegate_dns_resolver", default=False), False):
            subnets[key]["delegate_dns_resolver"] = True
    if not subnets:
        subnets = {
            "gateway": {"name": "GatewaySubnet", "address_prefixes": ["10.39.0.0/27"], "create_nsg": False},
            "firewall": {"name": "AzureFirewallSubnet", "address_prefixes": ["10.39.0.64/26"], "create_nsg": False},
            "dns_in": {"name": "snet-dns-inbound", "address_prefixes": ["10.39.1.0/28"], "create_nsg": False, "delegate_dns_resolver": True},
            "dns_out": {"name": "snet-dns-outbound", "address_prefixes": ["10.39.1.16/28"], "create_nsg": False, "delegate_dns_resolver": True},
            "bastion": {"name": "AzureBastionSubnet", "address_prefixes": ["10.39.2.0/26"], "create_nsg": False},
            "pe": {"name": "snet-shared-pe", "address_prefixes": ["10.39.3.0/24"], "create_nsg": True},
        }
    return {
        "tenant_id": args.tenant_id,
        "subscription_id": args.subscription_id,
        "location": args.location,
        "resource_group_name": args.hub_resource_group_name,
        "hub_name": args.hub_vnet_name,
        "address_space": [args.hub_vnet_cidr],
        "dns_servers": [],
        "enable_private_dns_resolver": True,
        "dns_inbound_subnet_key": "dns_in",
        "dns_outbound_subnet_key": "dns_out",
        "subnets": subnets,
        "common_tags": tags(args, "platform"),
    }


def build_firewall(args, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    row = rows[0] if rows else {}
    enabled = as_bool(value(row, "enabled", "사용여부", "create_azure_firewall", default=False), False)
    fw_name = str(value(row, "firewall_name", "name", default="fw-sl-hub-krc"))
    return {
        "tenant_id": args.tenant_id,
        "subscription_id": args.subscription_id,
        "location": args.location,
        "resource_group_name": str(value(row, "resource_group_name", default=args.hub_resource_group_name)),
        "create_azure_firewall": enabled,
        "firewall_name": fw_name if enabled else None,
        "firewall_subnet_id": id_for_subnet(args.subscription_id, args.hub_resource_group_name, args.hub_vnet_name, "AzureFirewallSubnet") if enabled else None,
        "public_ip_name": str(value(row, "public_ip_name", default=f"pip-{fw_name}")) if enabled else None,
        "sku_tier": str(value(row, "sku_tier", default="Standard")),
        "common_tags": tags(args, "network"),
    }


def subnet_map(rows: List[Dict[str, Any]], defaults: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    if not rows:
        return defaults
    result = {}
    for row in rows:
        key = slug(value(row, "key", "role", default=value(row, "SubnetName", default="subnet"))).replace("-", "_")
        name = str(value(row, "SubnetName", "name", default="snet-replace"))
        item = {
            "name": name,
            "address_prefixes": [str(value(row, "CIDR", "address_prefix", default="10.0.0.0/24"))],
            "create_nsg": as_bool(value(row, "create_nsg", "NSG", default=True), True),
            "associate_route_table": as_bool(value(row, "associate_route_table", "RouteTable", default=True), True),
        }
        if "pe" in name.lower():
            item["private_endpoint_network_policies"] = "Disabled"
        result[key] = item
    return result


def build_workload_spokes(args, rows: List[Dict[str, Any]]) -> List[tuple[Path, Dict[str, Any]]]:
    if not rows:
        rows = [{"업무": "sales", "Environment": "dev", "ResourceGroup": "rg-sl-sales-dev-krc", "VNet": "vnet-sl-sales-dev-krc", "CIDR": "10.40.0.0/20"}]
    outputs = []
    for row in rows:
        workload = slug(value(row, "workload", "업무", default="sales"))
        env = str(value(row, "Environment", "env", default="dev")).lower()
        rg = str(value(row, "ResourceGroup", "resource_group_name", default=f"rg-sl-{workload}-{env}-krc"))
        vnet = str(value(row, "VNet", "vnet_name", default=f"vnet-sl-{workload}-{env}-krc"))
        cidr = str(value(row, "CIDR", "address_space", default="10.40.0.0/20"))
        defaults = {
            "web": {"name": "snet-web", "address_prefixes": ["10.40.0.0/24"], "create_nsg": True, "associate_route_table": True},
            "was": {"name": "snet-was", "address_prefixes": ["10.40.1.0/24"], "create_nsg": True, "associate_route_table": True},
            "db": {"name": "snet-db", "address_prefixes": ["10.40.2.0/24"], "create_nsg": True, "associate_route_table": True},
            "pe": {"name": "snet-pe", "address_prefixes": ["10.40.3.0/24"], "create_nsg": True, "associate_route_table": True, "private_endpoint_network_policies": "Disabled"},
        }
        data = {
            "tenant_id": args.tenant_id,
            "subscription_id": args.subscription_id,
            "location": args.location,
            "resource_group_name": rg,
            "spoke_name": vnet,
            "address_space": [cidr],
            "dns_servers": [args.hub_dns_inbound_ip],
            "hub_vnet_id": id_for_vnet(args.subscription_id, args.hub_resource_group_name, args.hub_vnet_name),
            "hub_resource_group_name": args.hub_resource_group_name,
            "hub_vnet_name": args.hub_vnet_name,
            "firewall_private_ip": None if args.firewall_private_ip.lower() == "none" else args.firewall_private_ip,
            "subnets": defaults,
            "common_tags": tags(args, workload, env),
        }
        outputs.append((Path("20-workload") / f"{workload}-{env}-spoke" / "terraform.tfvars", data))
    return outputs


def build_vm_groups(args, rows: List[Dict[str, Any]]) -> List[tuple[Path, Dict[str, Any]]]:
    groups: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        name = str(value(row, "VM Name", "VM명", "name", default="")).strip()
        if not name:
            continue
        workload = slug(value(row, "workload", "업무", default="sales"))
        env = str(value(row, "Environment", "env", default="dev")).lower()
        key = f"{workload}-{env}"
        group = groups.setdefault(key, {
            "tenant_id": args.tenant_id,
            "subscription_id": args.subscription_id,
            "location": args.location,
            "resource_group_name": str(value(row, "ResourceGroup", default=f"rg-sl-{workload}-{env}-krc")),
            "vnet_resource_group_name": str(value(row, "ResourceGroup", default=f"rg-sl-{workload}-{env}-krc")),
            "vnet_name": str(value(row, "VNet", default=f"vnet-sl-{workload}-{env}-krc")),
            "admin_username": "azureuser",
            "ssh_public_key": args.ssh_public_key,
            "os_disk_storage_type": "Premium_LRS",
            "image_publisher": "RedHat",
            "image_offer": "RHEL",
            "image_sku": "9-lvm-gen2",
            "image_version": "latest",
            "web_vms": {}, "was_vms": {}, "db_vms": {}, "agent_vms": {},
            "common_tags": tags(args, workload, env),
        })
        role = slug(value(row, "role", "역할", default="agent"))
        bucket = "web_vms" if "web" in role else "was_vms" if "was" in role or "app" in role else "db_vms" if "db" in role else "agent_vms"
        group[bucket][slug(name)] = {
            "name": name,
            "subnet_name": str(value(row, "Subnet", "subnet", default=f"snet-{role}")),
            "private_ip_address": str(value(row, "Private IP", "private_ip", default="")),
            "vm_size": str(value(row, "Size", "vm_size", default="Standard_D2s_v3")),
            "os_disk_size_gb": int(value(row, "Disk GB", "os_disk_size_gb", default=128)),
            "role": role,
            "itsm_ticket": str(value(row, "RequestID", default="CSR-REPLACE")),
            "data_disks": {},
        }
    return [(Path("30-services") / f"vm-{key}" / "terraform.tfvars", data) for key, data in groups.items()]


def build_private_dns(args, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    zones = [str(value(r, "zone", "ZoneName", default="")).strip() for r in rows]
    zones = [z for z in zones if z]
    if not zones:
        zones = ["privatelink.openai.azure.com", "privatelink.search.windows.net", "privatelink.blob.core.windows.net", "privatelink.vaultcore.azure.net"]
    links = {}
    for z in zones:
        key = slug(z.split(".")[1] if "." in z else z)
        links[f"hub-{key}"] = {"zone_name": z, "name": f"lnk-hub-{key}", "virtual_network_id": id_for_vnet(args.subscription_id, args.hub_resource_group_name, args.hub_vnet_name), "registration_enabled": False}
    return {"tenant_id": args.tenant_id, "subscription_id": args.subscription_id, "resource_group_name": args.hub_resource_group_name, "zones": zones, "virtual_network_links": links, "common_tags": tags(args, "access")}


def build_dr_vm_mapping(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        rows = [
            {"source_vm_name": "db01", "role": "db", "source_subnet": "snet-db", "target_subnet": "snet-db", "recovery_group": 1},
            {"source_vm_name": "was01", "role": "was", "source_subnet": "snet-was", "target_subnet": "snet-was", "recovery_group": 2},
            {"source_vm_name": "web01", "role": "web", "source_subnet": "snet-web", "target_subnet": "snet-web", "recovery_group": 3},
        ]
    mapping = {}
    for row in rows:
        name = str(value(row, "source_vm_name", "SourceVM", "VM Name", default="vm"))
        mapping[slug(name).replace("-", "_")] = {
            "source_vm_name": name,
            "role": str(value(row, "role", "역할", default="app")),
            "source_subnet": str(value(row, "source_subnet", "SourceSubnet", default="snet-app")),
            "target_subnet": str(value(row, "target_subnet", "TargetSubnet", default="snet-app")),
            "recovery_group": int(value(row, "recovery_group", "RecoveryGroup", default=2)),
            "create_by": "ASR Failover",
        }
    return {"dr_vm_mapping": mapping}


def build_dr_dns(args, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    records = {}
    for row in rows:
        name = str(value(row, "name", "RecordName", default="")).strip()
        ip = str(value(row, "ip", "IPAddress", default="")).strip()
        if name and ip:
            records[name] = {"name": name, "ttl": int(value(row, "ttl", default=60)), "records": [ip]}
    return {"dns_resource_group_name": args.dr_hub_rg, "private_dns_zone_name": args.private_dns_zone_name, "create_private_dns_zone": False, "a_records": records, "common_tags": tags(args, "dr-access", "dr")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel", required=True)
    parser.add_argument("--out", default="live")
    parser.add_argument("--tenant-id", required=True)
    parser.add_argument("--subscription-id", required=True)
    parser.add_argument("--project", default="azure-landing-zone-asr-runbook-ent")
    parser.add_argument("--location", default="koreacentral")
    parser.add_argument("--dr-location", default="japaneast")
    parser.add_argument("--hub-resource-group-name", default="rg-sl-hub-krc")
    parser.add_argument("--hub-vnet-name", default="vnet-sl-hub-krc")
    parser.add_argument("--hub-vnet-cidr", default="10.39.0.0/20")
    parser.add_argument("--hub-dns-inbound-ip", default="10.39.1.4")
    parser.add_argument("--firewall-private-ip", default="none")
    parser.add_argument("--ssh-public-key", default="ssh-rsa REPLACE_ME")
    parser.add_argument("--dr-hub-rg", default="rg-sl-dr-hub-jpe")
    parser.add_argument("--dr-workload-rg", default="rg-sl-sales-prod-dr-jpe")
    parser.add_argument("--dr-asr-rg", default="rg-sl-dr-asr-jpe")
    parser.add_argument("--dr-automation-rg", default="rg-sl-dr-automation-jpe")
    parser.add_argument("--dr-inventory-rg", default="rg-sl-dr-inventory-jpe")
    parser.add_argument("--dr-hub-vnet-name", default="vnet-sl-dr-hub-jpe")
    parser.add_argument("--dr-hub-cidr", default="10.110.0.0/16")
    parser.add_argument("--dr-workload-vnet-name", default="vnet-sl-sales-prod-dr-jpe")
    parser.add_argument("--dr-workload-cidr", default="10.120.0.0/16")
    parser.add_argument("--private-dns-zone-name", default="corp.internal")
    parser.add_argument("--recovery-vault-name", default="rsv-sl-asr-jpe")
    parser.add_argument("--automation-account-name", default="aa-sl-dr-runbook-jpe")
    args = parser.parse_args()

    wb = openpyxl.load_workbook(args.excel, data_only=True)
    out = Path(args.out)

    write_tfvars(out / "00-foundation/resource-groups/terraform.tfvars", build_resource_groups(args, rows_as_dicts(wb, "00_Foundation_RG"), args.location, [{"key": "hub", "name": args.hub_resource_group_name, "workload": "platform"}]))
    write_tfvars(out / "10-platform/hub-network/terraform.tfvars", build_hub_network(args, rows_as_dicts(wb, "10_Platform_Hub_Network")))
    write_tfvars(out / "10-platform/azure-firewall/terraform.tfvars", build_firewall(args, rows_as_dicts(wb, "10_Platform_Azure_Firewall")))

    for relpath, data in build_workload_spokes(args, rows_as_dicts(wb, "20_Workload_Spoke")):
        write_tfvars(out / relpath, data)
    for relpath, data in build_vm_groups(args, rows_as_dicts(wb, "30_Service_VM")):
        write_tfvars(out / relpath, data)

    write_tfvars(out / "40-access/private-dns-zones/terraform.tfvars", build_private_dns(args, rows_as_dicts(wb, "40_Access_Private_DNS")))

    write_tfvars(out / "D00-foundation/resource-groups/terraform.tfvars", build_resource_groups(args, rows_as_dicts(wb, "D00_Foundation_RG"), args.dr_location, [
        {"key": "dr_hub", "name": args.dr_hub_rg, "workload": "platform", "env": "dr"},
        {"key": "dr_sales_prod", "name": args.dr_workload_rg, "workload": "sales", "env": "dr"},
        {"key": "dr_asr", "name": args.dr_asr_rg, "workload": "asr", "env": "dr"},
        {"key": "dr_automation", "name": args.dr_automation_rg, "workload": "automation", "env": "dr"},
    ]))

    d10_defaults = {
        "firewall": {"name": "AzureFirewallSubnet", "address_prefixes": ["10.110.0.0/24"], "create_nsg": False, "associate_route_table": False},
        "dns_shared": {"name": "snet-dns-shared", "address_prefixes": ["10.110.1.0/24"], "create_nsg": True, "associate_route_table": False},
        "mgmt": {"name": "snet-mgmt", "address_prefixes": ["10.110.2.0/24"], "create_nsg": True, "associate_route_table": False},
    }
    write_tfvars(out / "D10-platform/dr-hub-network-jpe/terraform.tfvars", {
        "location": args.dr_location, "resource_group_name": args.dr_hub_rg, "vnet_name": args.dr_hub_vnet_name, "address_space": [args.dr_hub_cidr], "dns_servers": [], "common_tags": tags(args, "dr-platform", "dr"), "subnets": subnet_map(rows_as_dicts(wb, "D10_Platform_DR_Hub"), d10_defaults)
    })

    d20_defaults = {
        "web": {"name": "snet-web", "address_prefixes": ["10.120.0.0/24"], "create_nsg": True, "associate_route_table": True},
        "was": {"name": "snet-was", "address_prefixes": ["10.120.1.0/24"], "create_nsg": True, "associate_route_table": True},
        "db": {"name": "snet-db", "address_prefixes": ["10.120.2.0/24"], "create_nsg": True, "associate_route_table": True},
        "pe": {"name": "snet-pe", "address_prefixes": ["10.120.3.0/24"], "create_nsg": True, "associate_route_table": True, "private_endpoint_network_policies": "Disabled"},
        "agent": {"name": "snet-agent", "address_prefixes": ["10.120.4.0/24"], "create_nsg": True, "associate_route_table": True},
    }
    write_tfvars(out / "D20-workload/dr-sales-prod-spoke-jpe/terraform.tfvars", {
        "location": args.dr_location, "resource_group_name": args.dr_workload_rg, "vnet_name": args.dr_workload_vnet_name, "address_space": [args.dr_workload_cidr], "dns_servers": [], "dr_hub_vnet_id": id_for_vnet(args.subscription_id, args.dr_hub_rg, args.dr_hub_vnet_name), "dr_hub_resource_group_name": args.dr_hub_rg, "dr_hub_vnet_name": args.dr_hub_vnet_name, "dr_firewall_private_ip": None, "common_tags": tags(args, "dr-sales", "dr"), "subnets": subnet_map(rows_as_dicts(wb, "D20_Workload_DR_Spoke"), d20_defaults)
    })
    write_tfvars(out / "D30-services/dr-vm-placeholder/terraform.tfvars", build_dr_vm_mapping(rows_as_dicts(wb, "D30_Service_DR_VM_Map")))
    write_tfvars(out / "D40-access/dr-private-dns-records/terraform.tfvars", build_dr_dns(args, rows_as_dicts(wb, "D40_Access_DR_DNS")))
    write_tfvars(out / "50-asr/recovery-vault-jpe/terraform.tfvars", {"location": args.dr_location, "resource_group_name": args.dr_asr_rg, "vault_name": args.recovery_vault_name, "sku": "Standard", "soft_delete_enabled": True, "common_tags": tags(args, "asr", "dr")})
    write_tfvars(out / "50-asr/recovery-plan-sales-prod/terraform.tfvars", {"recovery_plan_name": "rp-sales-prod-dr", "vault_name": args.recovery_vault_name, "resource_group_name": args.dr_asr_rg, "groups": {"group1_db": ["db01"], "group2_was": ["was01", "was02"], "group3_web": ["web01", "web02"]}})
    write_tfvars(out / "60-operations/automation-dr/terraform.tfvars", {"location": args.dr_location, "resource_group_name": args.dr_automation_rg, "automation_account_name": args.automation_account_name, "common_tags": tags(args, "automation", "dr")})
    write_tfvars(out / "60-operations/inventory/terraform.tfvars", {"location": args.dr_location, "resource_group_name": args.dr_inventory_rg, "inventory_name": "dr-inventory", "common_tags": tags(args, "inventory", "dr")})

    print("completed: numbered Excel terraform.tfvars generation")


if __name__ == "__main__":
    main()
