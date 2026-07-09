# Repository Redesign: 기존 Landing Zone + D-prefix DR 확장

본 저장소는 `azure-landing-zone_test04_ENT`를 원본으로 복사한 뒤 DR/ASR 영역을 추가한다.

## 번호 체계

| 구분 | Prefix | 역할 |
|---|---:|---|
| 주센터 Foundation | `00` | 기존 Resource Group |
| 주센터 Platform | `10` | 기존 Hub Network / Platform |
| 주센터 Workload | `20` | 기존 업무 Spoke |
| 주센터 Service | `30` | 기존 VM / AKS / LB |
| 주센터 Access | `40` | 기존 DNS / PE / Rule |
| DR Foundation | `D00` | DR Resource Group |
| DR Platform | `D10` | DR Hub Network |
| DR Workload | `D20` | DR 업무 Spoke |
| DR Service Placeholder | `D30` | ASR Failover 대상 Placeholder |
| DR Access | `D40` | DR DNS / PE / Rule |
| ASR Control | `50-asr` | Vault / Policy / Recovery Plan |
| Operations | `60-operations` | Runbook / Inventory / Monitor |

## 원칙

- 기존 `00~40`은 주센터 영역으로 유지한다.
- DR 영역은 `D00~D40`으로 분리한다.
- ASR와 Recovery Plan은 `50-asr`에서 관리한다.
- Runbook, Inventory, Monitor는 `60-operations`에서 관리한다.
- DR VM은 평상시 Terraform으로 생성하지 않고 ASR Failover 시 생성한다.
