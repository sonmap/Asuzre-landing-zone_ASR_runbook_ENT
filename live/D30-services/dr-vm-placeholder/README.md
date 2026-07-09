# D30-services / dr-vm-placeholder

DR센터 Service Placeholder 영역이다.

기존 주센터 `30-services/vm-sales-prod`와 대응되지만, ASR 기반 DR 설계에서는 DR VM을 Terraform으로 상시 생성하지 않는다.

## 역할

- DR VM Naming Rule 관리
- ASR Failover 시 생성될 VM 역할 정의
- Source VM ↔ Target Subnet Mapping 문서화
- Failover 후 Inventory 비교 기준 관리
- 필요 시 DR 관리용 Agent/Jump VM만 제한적으로 생성

## 기본 원칙

| 항목 | 원칙 |
|---|---|
| Web/WAS/DB VM | 평상시 미생성 |
| Failover 시점 | ASR가 DR VNet/Subnet에 VM 생성 |
| Terraform 역할 | Placeholder / Mapping / Output 기준 관리 |
| 예외 | Agent VM, Bastion, Jump VM 등 관리 자원은 사전 생성 가능 |

## VM Mapping 예시

| Source VM | Role | DR Subnet | Failover Target |
|---|---|---|---|
| `web01` | web | `snet-web` | Japan East |
| `web02` | web | `snet-web` | Japan East |
| `was01` | was | `snet-was` | Japan East |
| `was02` | was | `snet-was` | Japan East |
| `db01` | db | `snet-db` | Japan East |
