# D10-platform / dr-hub-network-jpe

DR센터 Japan East Hub Network 영역이다.

기존 주센터 `10-platform/hub-network`에 대응한다.

## DR Hub VNet

| 항목 | 값 |
|---|---|
| Region | Japan East |
| Resource Group | `rg-sl-dr-hub-jpe` |
| VNet | `vnet-sl-dr-hub-jpe` |
| CIDR | `10.110.0.0/16` |

## Subnet

| Subnet | CIDR | 용도 |
|---|---|---|
| `AzureFirewallSubnet` | `10.110.0.0/24` | DR Firewall |
| `snet-dns-shared` | `10.110.1.0/24` | DR DNS Resolver / Shared DNS |
| `snet-mgmt` | `10.110.2.0/24` | DR Management / Runbook Agent |

## 실행 예

```bash
./tools/tf_root.sh live/D10-platform/dr-hub-network-jpe plan
./tools/tf_root.sh live/D10-platform/dr-hub-network-jpe apply
```
