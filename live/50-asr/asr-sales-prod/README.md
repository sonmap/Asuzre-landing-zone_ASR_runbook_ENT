# 50-asr / asr-sales-prod

주센터 Sales Prod VM을 ASR 보호 대상으로 등록하는 영역이다.

## 역할

- Source VM ID 관리
- Source VM ↔ DR Subnet Mapping 관리
- ASR Replication Policy 연결
- Cache Storage Account 기준 관리
- Protected Item 생성 기준 관리

## VM Mapping

| Source VM | Source Subnet | DR Subnet | Recovery Plan Group |
|---|---|---|---|
| `db01` | `snet-db` | `snet-db` | Group 1 |
| `was01` | `snet-was` | `snet-was` | Group 2 |
| `was02` | `snet-was` | `snet-was` | Group 2 |
| `web01` | `snet-web` | `snet-web` | Group 3 |
| `web02` | `snet-web` | `snet-web` | Group 3 |

## 주의

실제 ASR Terraform resource는 Source VM ID, Target VNet/Subnet ID, Vault Fabric/Container 값이 확정된 후 완성한다.
