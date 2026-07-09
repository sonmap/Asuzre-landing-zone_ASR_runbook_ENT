# 주센터-DR센터 ASR Runbook 아키텍처

## 1. 개요

본 설계는 기존 Azure Landing Zone 구조를 확장하여 Korea Central 주센터와 Japan East DR센터를 구성하는 방안이다.

핵심은 다음과 같다.

- 주센터는 평상시 서비스 운영 영역이다.
- DR센터는 VNet/Subnet/Recovery Vault/Automation/Inventory를 사전 구성한다.
- VM은 ASR Replication으로 보호하고, DR 발생 시 Japan East에 생성한다.
- Recovery Plan은 DB → WAS → WEB 순서로 기동한다.
- Runbook은 Precheck, DNS 전환, 상태 점검, Inventory 갱신에 사용한다.

## 2. 네트워크 구조

| 영역 | 주센터 | DR센터 |
|---|---|---|
| Hub VNet | `vnet-sl-hub-krc`, `10.10.0.0/16` | `vnet-sl-dr-hub-jpe`, `10.110.0.0/16` |
| Workload VNet | `vnet-sl-sales-prod-krc`, `10.20.0.0/16` | `vnet-sl-sales-prod-dr-jpe`, `10.120.0.0/16` |
| Firewall Subnet | `10.10.0.0/24` | `10.110.0.0/24` |
| DNS Shared Subnet | `10.10.1.0/24` | `10.110.1.0/24` |
| Management Subnet | `10.10.2.0/24` | `10.110.2.0/24` |
| Web Subnet | `10.20.0.0/24` | `10.120.0.0/24` |
| WAS Subnet | `10.20.1.0/24` | `10.120.1.0/24` |
| DB Subnet | `10.20.2.0/24` | `10.120.2.0/24` |
| Private Endpoint Subnet | `10.20.3.0/24` | `10.120.3.0/24` |
| Agent Subnet | `10.20.4.0/24` | `10.120.4.0/24` |

## 3. DR 이벤트 흐름

```text
1. 평상시 주센터 VNet에서 서비스 운영
2. ASR Replication 유지
3. 장애 감지 또는 DR Drill 요청
4. Recovery Plan 실행
5. DB → WAS → WEB 순서로 DR센터 VM 기동
6. Runbook으로 상태 점검
7. DNS 전환
8. Inventory / CMDB 갱신
9. 서비스 복구 완료
```

## 4. Terraform Root 구성

| Root | 목적 |
|---|---|
| `live/00-foundation/resource-groups` | DR용 Resource Group 생성 |
| `live/10-platform/dr-hub-network-jpe` | Japan East DR Hub VNet 구성 |
| `live/20-workload/dr-sales-prod-spoke-jpe` | Japan East DR 업무 Spoke VNet 구성 |
| `live/50-dr/recovery-vault-jpe` | Recovery Services Vault 구성 |
| `live/50-dr/asr-sales-prod` | ASR 복제 정책 및 VM 보호 설정 skeleton |
| `live/50-dr/recovery-plan-sales-prod` | Recovery Plan skeleton |
| `live/60-operations/automation-dr` | Automation Account와 Runbook 구성 |

## 5. 운영 판단 포인트

- Web/WAS VM은 ASR 보호 대상으로 적합하다.
- DB VM은 ASR만으로 충분한지 RPO/RTO와 정합성 검토가 필요하다.
- AKS는 ASR 대상이 아니라 DR 리전에 Terraform/GitOps로 재배포하는 것이 적합하다.
- Private Endpoint, DNS, Firewall, Route Table은 ASR 대상이 아니므로 DR 리전에 별도 구성한다.
