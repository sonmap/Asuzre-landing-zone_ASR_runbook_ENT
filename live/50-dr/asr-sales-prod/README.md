# ASR Sales Prod Skeleton

이 root는 `sales-prod` 업무 VM을 ASR 보호 대상으로 등록하기 위한 skeleton 영역입니다.

## 현재 상태

- Recovery Services Vault는 `live/50-dr/recovery-vault-jpe`에서 생성한다.
- DR VNet/Subnet은 `live/20-workload/dr-sales-prod-spoke-jpe`에서 생성한다.
- 실제 ASR 보호 설정은 Source VM ID, Source/Target Region, Fabric, Protection Container, Cache Storage Account, Target Subnet ID가 확정된 후 적용한다.

## 1차 설계 변수

| 변수 | 설명 |
|---|---|
| `source_resource_group_name` | Korea Central 운영 VM Resource Group |
| `source_vm_ids` | ASR 보호 대상 VM ID 목록 |
| `target_resource_group_id` | Japan East Failover 대상 RG ID |
| `target_vnet_id` | DR Spoke VNet ID |
| `target_subnet_mapping` | web/was/db/agent subnet mapping |
| `recovery_vault_name` | Recovery Services Vault 이름 |
| `replication_policy_name` | ASR Replication Policy 이름 |

## 권장 적용 흐름

```bash
# 1. 운영 VM ID 확인
az vm list -g <PRIMARY_VM_RG> --query "[].{name:name,id:id}" -o table

# 2. DR VNet/Subnet ID 확인
terraform -chdir=../../20-workload/dr-sales-prod-spoke-jpe output subnet_ids

# 3. ASR 보호 설정 적용
# 실제 환경값 확정 후 main.tf를 완성한다.
```

## 주의

ASR Terraform resource는 환경 의존성이 크므로, 초기 skeleton에서는 의도적으로 변수/설계 구조 중심으로 둔다. 실제 적용 시 `azurerm_site_recovery_*` 리소스와 Azure Portal/CLI 검증을 병행한다.
