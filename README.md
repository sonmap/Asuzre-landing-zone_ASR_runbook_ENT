# Azure Landing Zone ASR Runbook ENT

이 저장소는 기존 `sonmap/azure-landing-zone_test04_ENT` 구조를 기반으로 복사/확장하는 것을 전제로 한다.

핵심 원칙은 다음과 같다.

- 기존 Landing Zone 구조는 최대한 유지한다.
- 주센터 영역은 기존 번호 체계 `00`, `10`, `20`, `30`, `40`을 그대로 사용한다.
- DR센터 영역은 동일한 구조를 `D00`, `D10`, `D20`, `D30`, `D40`으로 분리한다.
- ASR, Recovery Plan, Runbook, Inventory 같은 신규 DR 제어 영역은 `50`, `60`으로 별도 네이밍한다.
- DR센터 VM은 평상시 직접 생성하지 않고, ASR Failover 시 DR VNet/Subnet에 생성하는 구조를 기본으로 한다.

## 1. 네이밍 기준

| 구분 | Prefix | 의미 |
|---|---:|---|
| 주센터 Foundation | `00` | 기존 Resource Group, 공통 기반 |
| 주센터 Platform | `10` | 기존 Hub Network, Firewall, DNS |
| 주센터 Workload | `20` | 기존 업무 Spoke Landing Zone |
| 주센터 Service | `30` | 기존 VM, AKS, LB, AppGW 등 서비스 |
| 주센터 Access | `40` | 기존 Private DNS, Private Endpoint, Firewall Rule |
| DR Foundation | `D00` | DR Resource Group, DR 공통 기반 |
| DR Platform | `D10` | DR Hub Network, DR DNS, DR Mgmt |
| DR Workload | `D20` | DR 업무 Spoke VNet/Subnet |
| DR Service Placeholder | `D30` | DR 서비스 Placeholder. VM은 ASR Failover 시 생성 |
| DR Access | `D40` | DR Private DNS, DR DNS Record, DR Private Endpoint |
| ASR Control | `50` | Recovery Services Vault, ASR Policy, Recovery Plan |
| Operations | `60` | Automation Account, Runbook, Inventory, Monitor |

## 2. 기준 아키텍처

| 구분 | 주센터 | DR센터 |
|---|---|---|
| Region | Korea Central | Japan East |
| Hub VNet | `10.10.0.0/16` | `10.110.0.0/16` |
| Workload Spoke VNet | `10.20.0.0/16` | `10.120.0.0/16` |
| VM 상태 | 평상시 기동 | 평상시 미기동, ASR Failover 시 기동 |
| DR 방식 | ASR 보호 대상 | ASR Failover 대상 |
| Runbook | 운영 자동화 호출 원천 | DNS 전환, 상태 점검, Inventory 갱신 |

## 3. 권장 디렉터리 구조

```text
.
├── docs/
│   ├── ARCHITECTURE.md
│   ├── REPOSITORY_REDESIGN.md
│   ├── DR_RUNBOOK.md
│   └── INVENTORY_DESIGN.md
│
├── live/
│   ├── 00-foundation/                 # 기존 주센터 Foundation 복사 유지
│   │   └── resource-groups/
│   ├── 10-platform/                   # 기존 주센터 Platform 복사 유지
│   │   └── hub-network/
│   ├── 20-workload/                   # 기존 주센터 Workload 복사 유지
│   │   └── sales-prod-spoke/
│   ├── 30-services/                   # 기존 주센터 Service 복사 유지
│   │   └── vm-sales-prod/
│   ├── 40-access/                     # 기존 주센터 Access 복사 유지
│   │   └── private-dns-zones/
│   │
│   ├── D00-foundation/                # DR Foundation
│   │   └── resource-groups/
│   ├── D10-platform/                  # DR Hub Network
│   │   └── dr-hub-network-jpe/
│   ├── D20-workload/                  # DR Workload Spoke
│   │   └── dr-sales-prod-spoke-jpe/
│   ├── D30-services/                  # DR Service Placeholder
│   │   └── dr-vm-placeholder/
│   ├── D40-access/                    # DR Access / DNS
│   │   └── dr-private-dns-records/
│   │
│   ├── 50-asr/                        # 신규 ASR Control 영역
│   │   ├── recovery-vault-jpe/
│   │   ├── asr-sales-prod/
│   │   └── recovery-plan-sales-prod/
│   └── 60-operations/                 # 신규 Runbook / Inventory / Monitor 영역
│       ├── automation-dr/
│       └── inventory/
│
├── modules/
│   ├── resource_group/
│   ├── dr_network/
│   ├── recovery_services_vault/
│   └── automation_runbook/
│
├── runbooks/
│   ├── dr-precheck.ps1
│   ├── dr-health-check.ps1
│   ├── dr-dns-switch.ps1
│   └── dr-inventory-update.ps1
│
├── tools/
│   ├── tf_root.sh
│   └── export_inventory.sh
└── backend.hcl.example
```

## 4. 기존 저장소 복사 기준

대상 저장소는 기존 `azure-landing-zone_test04_ENT`를 먼저 복사한 뒤 DR 영역을 추가하는 방식이 맞다.

```bash
git clone https://github.com/sonmap/azure-landing-zone_test04_ENT.git Asuzre-landing-zone_ASR_runbook_ENT
cd Asuzre-landing-zone_ASR_runbook_ENT

# remote 변경
git remote remove origin
git remote add origin https://github.com/sonmap/Asuzre-landing-zone_ASR_runbook_ENT.git
```

이후 기존 영역은 유지하고 DR 영역을 추가한다.

```bash
mkdir -p live/D00-foundation/resource-groups
mkdir -p live/D10-platform/dr-hub-network-jpe
mkdir -p live/D20-workload/dr-sales-prod-spoke-jpe
mkdir -p live/D30-services/dr-vm-placeholder
mkdir -p live/D40-access/dr-private-dns-records
mkdir -p live/50-asr/recovery-vault-jpe
mkdir -p live/50-asr/asr-sales-prod
mkdir -p live/50-asr/recovery-plan-sales-prod
mkdir -p live/60-operations/automation-dr
mkdir -p live/60-operations/inventory
```

## 5. 배포 순서

```bash
# 주센터 기존 기반
./tools/tf_root.sh live/00-foundation/resource-groups plan
./tools/tf_root.sh live/10-platform/hub-network plan
./tools/tf_root.sh live/20-workload/sales-prod-spoke plan
./tools/tf_root.sh live/30-services/vm-sales-prod plan
./tools/tf_root.sh live/40-access/private-dns-zones plan

# DR 기반
./tools/tf_root.sh live/D00-foundation/resource-groups plan
./tools/tf_root.sh live/D10-platform/dr-hub-network-jpe plan
./tools/tf_root.sh live/D20-workload/dr-sales-prod-spoke-jpe plan
./tools/tf_root.sh live/D40-access/dr-private-dns-records plan

# 신규 ASR / Runbook / Inventory
./tools/tf_root.sh live/50-asr/recovery-vault-jpe plan
./tools/tf_root.sh live/60-operations/automation-dr plan
./tools/tf_root.sh live/50-asr/asr-sales-prod plan
./tools/tf_root.sh live/50-asr/recovery-plan-sales-prod plan
./tools/tf_root.sh live/60-operations/inventory plan
```

## 6. 설계 원칙

- 기존 주센터 구조는 손대지 않는다.
- DR 영역은 `D` prefix로 분리하여 기존 영역과 혼동하지 않게 한다.
- ASR/Runbook/Inventory는 DR 전용 신규 운영 기능이므로 `50-asr`, `60-operations`로 별도 관리한다.
- DR VNet/Subnet은 사전 생성한다.
- DR VM은 Terraform으로 상시 생성하지 않는다. ASR Failover 시 생성한다.
- DB는 ASR만 적용하기 전 정합성, RPO/RTO, DB Native Replication 필요 여부를 별도 검토한다.

## 7. 현재 저장소 상태

현재 저장소에는 초기 skeleton이 들어가 있으며, 다음 단계는 기존 `azure-landing-zone_test04_ENT`의 `live/00~40`, `modules`, `tools`, `docs`를 복사한 뒤 `D00~D40`, `50-asr`, `60-operations` 구조로 재배치하는 것이다.
