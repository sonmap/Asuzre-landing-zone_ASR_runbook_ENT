# Azure Landing Zone ASR Runbook ENT

기존 `azure-landing-zone_test04_ENT` 구조를 기반으로 **주센터(Korea Central) - DR센터(Japan East)** 구성을 확장한 ASR / Runbook / Inventory 중심 Terraform Lab 저장소입니다.

## 목표

- 주센터와 DR센터를 1차 구성 시 함께 준비
- 평상시 VM은 주센터에서 운영
- DR센터는 VNet/Subnet/Recovery Vault/Automation/Inventory 중심으로 사전 준비
- 장애 또는 DR Drill 발생 시 ASR Recovery Plan으로 DR센터에 VM 기동
- Runbook으로 DNS 전환, 상태 점검, Inventory/CMDB 갱신 자동화

## 기준 아키텍처

| 구분 | 주센터 | DR센터 |
|---|---|---|
| Region | Korea Central | Japan East |
| Hub VNet | `10.10.0.0/16` | `10.110.0.0/16` |
| Workload Spoke VNet | `10.20.0.0/16` | `10.120.0.0/16` |
| 주요 Subnet | web, was, db, pe, agent | web, was, db, pe, agent |
| VM 상태 | 평상시 기동 | 평상시 미기동, Failover 시 기동 |
| DR 방식 | ASR 보호 대상 | ASR Failover 대상 |

## 디렉터리 구조

```text
.
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DR_RUNBOOK.md
│   └── INVENTORY_DESIGN.md
├── live/
│   ├── 00-foundation/resource-groups/
│   ├── 10-platform/dr-hub-network-jpe/
│   ├── 20-workload/dr-sales-prod-spoke-jpe/
│   ├── 50-dr/recovery-vault-jpe/
│   ├── 50-dr/asr-sales-prod/
│   ├── 50-dr/recovery-plan-sales-prod/
│   └── 60-operations/automation-dr/
├── modules/
│   ├── resource_group/
│   ├── dr_network/
│   ├── recovery_services_vault/
│   ├── asr_policy/
│   └── automation_runbook/
├── runbooks/
│   ├── dr-precheck.ps1
│   ├── dr-dns-switch.ps1
│   ├── dr-health-check.ps1
│   └── dr-inventory-update.ps1
├── tools/
│   └── export_inventory.sh
└── backend.hcl.example
```

## 1차 적용 순서

```bash
# 1. Backend 설정
cp backend.hcl.example backend.hcl

# 2. DR Resource Group 생성
tools/tf_root.sh live/00-foundation/resource-groups plan
tools/tf_root.sh live/00-foundation/resource-groups apply

# 3. DR Hub Network 생성
tools/tf_root.sh live/10-platform/dr-hub-network-jpe plan
tools/tf_root.sh live/10-platform/dr-hub-network-jpe apply

# 4. DR Workload Spoke 생성
tools/tf_root.sh live/20-workload/dr-sales-prod-spoke-jpe plan
tools/tf_root.sh live/20-workload/dr-sales-prod-spoke-jpe apply

# 5. Recovery Services Vault 생성
tools/tf_root.sh live/50-dr/recovery-vault-jpe plan
tools/tf_root.sh live/50-dr/recovery-vault-jpe apply

# 6. Automation Account / Runbook 생성
tools/tf_root.sh live/60-operations/automation-dr plan
tools/tf_root.sh live/60-operations/automation-dr apply

# 7. ASR Policy / Recovery Plan 구성
tools/tf_root.sh live/50-dr/asr-sales-prod plan
tools/tf_root.sh live/50-dr/recovery-plan-sales-prod plan
```

## 설계 원칙

- DR센터 VM은 평상시 직접 생성하지 않고 ASR Failover 시점에 생성한다.
- DR VNet/Subnet/NSG/Route/DNS/Automation/Recovery Vault는 사전에 준비한다.
- DB는 ASR 단독 적용 전 정합성, RPO/RTO, DB Native Replication 필요 여부를 별도 검토한다.
- Runbook은 Recovery Plan의 Pre/Post Action으로 연결한다.
- Inventory는 Terraform output + Azure Resource Graph + Ansible/CMDB 연계 구조로 관리한다.

## 주의

이 저장소는 학습 및 사전 검증용 skeleton입니다. 실제 운영 반영 전에는 조직 보안정책, 네트워크 주소, 권한, Quota, 비용, 삭제방지, DR Drill 절차를 반드시 검증해야 합니다.
