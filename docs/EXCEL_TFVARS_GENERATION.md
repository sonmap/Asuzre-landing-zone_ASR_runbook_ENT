# Excel 기반 전체 terraform.tfvars 생성 기준

## 1. 목표

모든 Terraform root의 실제 `terraform.tfvars`는 사람이 직접 작성하지 않고 Excel 설계서에서 생성한다.

대상은 주센터 기존 영역과 DR/ASR 신규 영역 전체다.

```text
주센터: 00 / 10 / 20 / 30 / 40
DR센터: D00 / D10 / D20 / D30 / D40
ASR:    50-asr
운영:   60-operations
```

## 2. 스크립트 역할

| 스크립트 | 생성 대상 |
|---|---|
| `tools/excel_to_tfvars.py` | 기존 주센터 `00~40` |
| `tools/excel_to_tfvars_dr.py` | DR/ASR/운영 `D00~D40`, `50-asr`, `60-operations` |
| `tools/generate_all_tfvars.sh` | 위 두 스크립트를 순서대로 실행 |

## 3. 실행 방법

```bash
export TENANT_ID="<TENANT_ID>"
export SUBSCRIPTION_ID="<SUBSCRIPTION_ID>"
export LOCATION="koreacentral"
export DR_LOCATION="japaneast"

bash tools/generate_all_tfvars.sh azure_landingzone_terraform_module_design.xlsx
```

실행 후 `live/**/terraform.tfvars`가 생성된다.

## 4. DR 전용 Excel 시트

DR/ASR 영역을 Excel에서 관리하려면 아래 시트를 추가한다.

| 시트명 | 생성 대상 | 설명 |
|---|---|---|
| `D00_DR_Foundation` | `live/D00-foundation/resource-groups/terraform.tfvars` | DR Resource Group |
| `D10_DR_Network` | `live/D10-platform/dr-hub-network-jpe/terraform.tfvars` | DR Hub VNet/Subnet |
| `D20_DR_Workload` | `live/D20-workload/dr-sales-prod-spoke-jpe/terraform.tfvars` | DR Spoke VNet/Subnet |
| `D30_DR_VM_Mapping` | `live/D30-services/dr-vm-placeholder/terraform.tfvars` | Source VM ↔ DR Subnet Mapping |
| `D40_DR_Access` | `live/D40-access/dr-private-dns-records/terraform.tfvars` | DR DNS Record |

`50-asr/recovery-vault-jpe`와 `60-operations/automation-dr`는 CLI 기본값으로 생성되며, 필요 시 스크립트 인자로 변경한다.

## 5. D10_DR_Network 시트 예시

| key | SubnetName | CIDR | create_nsg | associate_route_table |
|---|---|---|---|---|
| firewall | AzureFirewallSubnet | 10.110.0.0/24 | false | false |
| dns_shared | snet-dns-shared | 10.110.1.0/24 | true | false |
| mgmt | snet-mgmt | 10.110.2.0/24 | true | false |

## 6. D20_DR_Workload 시트 예시

| key | SubnetName | CIDR | create_nsg | associate_route_table |
|---|---|---|---|---|
| web | snet-web | 10.120.0.0/24 | true | true |
| was | snet-was | 10.120.1.0/24 | true | true |
| db | snet-db | 10.120.2.0/24 | true | true |
| pe | snet-pe | 10.120.3.0/24 | true | true |
| agent | snet-agent | 10.120.4.0/24 | true | true |

## 7. D30_DR_VM_Mapping 시트 예시

| source_vm_name | role | source_subnet | target_subnet | recovery_group |
|---|---|---|---|---|
| db01 | db | snet-db | snet-db | 1 |
| was01 | was | snet-was | snet-was | 2 |
| was02 | was | snet-was | snet-was | 2 |
| web01 | web | snet-web | snet-web | 3 |
| web02 | web | snet-web | snet-web | 3 |

## 8. D40_DR_Access 시트 예시

| name | ip | ttl |
|---|---|---|
| sales | 10.120.0.10 | 60 |
| db-sales | 10.120.2.10 | 60 |

운영 전환 DNS는 보통 Runbook으로 수행하므로, 평상시에는 해당 시트를 비워 둘 수 있다.

## 9. Git 관리 기준

`terraform.tfvars`는 실제 환경값이 들어가므로 Git에 올리지 않는다.

```gitignore
terraform.tfvars
*.auto.tfvars
backend.hcl
```

Git에는 스크립트, Terraform root, 문서, 필요 시 `terraform.tfvars.example`만 저장한다.

## 10. 배포 흐름

```bash
# 1. Excel에서 전체 tfvars 생성
bash tools/generate_all_tfvars.sh azure_landingzone_terraform_module_design.xlsx

# 2. DR Resource Group
./tools/tf_root.sh live/D00-foundation/resource-groups plan

# 3. DR Hub
./tools/tf_root.sh live/D10-platform/dr-hub-network-jpe plan

# 4. DR Spoke
./tools/tf_root.sh live/D20-workload/dr-sales-prod-spoke-jpe plan

# 5. ASR Vault
./tools/tf_root.sh live/50-asr/recovery-vault-jpe plan
```
