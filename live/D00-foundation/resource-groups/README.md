# D00-foundation / resource-groups

DR센터 Foundation 영역이다.

기존 주센터 `00-foundation/resource-groups`와 대응되며, Japan East DR 구성을 위한 Resource Group을 생성한다.

## 역할

| Resource Group | 용도 |
|---|---|
| `rg-sl-dr-hub-jpe` | DR Hub Network |
| `rg-sl-sales-prod-dr-jpe` | DR Sales Workload |
| `rg-sl-dr-asr-jpe` | ASR Recovery Services Vault |
| `rg-sl-dr-automation-jpe` | Automation Account / Runbook |
| `rg-sl-dr-inventory-jpe` | Inventory / CMDB export |

## 실행 예

```bash
./tools/tf_root.sh live/D00-foundation/resource-groups plan
./tools/tf_root.sh live/D00-foundation/resource-groups apply
```
