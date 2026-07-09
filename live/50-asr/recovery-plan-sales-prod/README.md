# 50-asr / recovery-plan-sales-prod

ASR Recovery Plan 정의 영역이다.

## Recovery Plan 순서

| 순서 | Group | 대상 | Action |
|---:|---|---|---|
| 0 | Pre Action | 전체 | `dr-precheck` Runbook |
| 1 | Group 1 | DB | `db01` Failover |
| 2 | Post Group 1 | DB | DB 상태 점검 |
| 3 | Group 2 | WAS | `was01`, `was02` Failover |
| 4 | Post Group 2 | WAS | WAS 상태 점검 |
| 5 | Group 3 | WEB | `web01`, `web02` Failover |
| 6 | Post Group 3 | WEB | WEB 상태 점검 |
| 7 | Final Action | DNS / Inventory | DNS 전환, Inventory 갱신 |

## 연결 Runbook

| Runbook | 목적 |
|---|---|
| `dr-precheck` | DR 전 사전 확인 |
| `dr-health-check` | VM/서비스 상태 점검 |
| `dr-dns-switch` | Private DNS 전환 |
| `dr-inventory-update` | Inventory / CMDB 갱신 |
