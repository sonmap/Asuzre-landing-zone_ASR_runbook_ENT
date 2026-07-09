# D40-access / dr-private-dns-records

DR센터 Access 영역이다.

기존 주센터 `40-access/private-dns-zones`, `private-endpoint`, `dns-record`, `firewall-rule`에 대응한다.

## 역할

- DR Private DNS Zone 또는 DR DNS Record 관리
- DR Private Endpoint 생성 기준 관리
- DR Firewall Rule / Route Rule 기준 관리
- Runbook 기반 DNS 전환 대상 관리

## DNS 전환 원칙

| 단계 | 설명 |
|---|---|
| 1 | ASR Recovery Plan 실행 |
| 2 | DB/WAS/WEB 상태 점검 |
| 3 | DR 서비스 Endpoint 확인 |
| 4 | Runbook `dr-dns-switch` 실행 |
| 5 | Private DNS A Record를 DR IP로 변경 |
| 6 | Inventory / CMDB 갱신 |

## 예시

| Record | 평상시 | DR 전환 후 |
|---|---|---|
| `sales.corp.internal` | 주센터 Web/LB IP | DR센터 Web/LB IP |
| `db-sales.corp.internal` | 주센터 DB IP | DR센터 DB IP |
