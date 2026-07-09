# D20-workload / dr-sales-prod-spoke-jpe

DR센터 Japan East 업무 Spoke Network 영역이다.

기존 주센터 `20-workload/sales-prod-spoke`에 대응한다.

## DR Workload Spoke VNet

| 항목 | 값 |
|---|---|
| Region | Japan East |
| Resource Group | `rg-sl-sales-prod-dr-jpe` |
| VNet | `vnet-sl-sales-prod-dr-jpe` |
| CIDR | `10.120.0.0/16` |

## Subnet Mapping

| 주센터 Subnet | DR Subnet | 설명 |
|---|---|---|
| `snet-web` `10.20.0.0/24` | `snet-web` `10.120.0.0/24` | Web VM Failover 대상 |
| `snet-was` `10.20.1.0/24` | `snet-was` `10.120.1.0/24` | WAS VM Failover 대상 |
| `snet-db` `10.20.2.0/24` | `snet-db` `10.120.2.0/24` | DB VM Failover 대상 |
| `snet-pe` `10.20.3.0/24` | `snet-pe` `10.120.3.0/24` | Private Endpoint 대상 |
| `snet-agent` `10.20.4.0/24` | `snet-agent` `10.120.4.0/24` | Agent / 관리 대상 |

## 실행 예

```bash
./tools/tf_root.sh live/D20-workload/dr-sales-prod-spoke-jpe plan
./tools/tf_root.sh live/D20-workload/dr-sales-prod-spoke-jpe apply
```
