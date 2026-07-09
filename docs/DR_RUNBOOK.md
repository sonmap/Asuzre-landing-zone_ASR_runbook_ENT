# DR Runbook 설계

## 1. Runbook 역할

Runbook은 ASR Recovery Plan의 Pre/Post Action으로 연결하여 DR 절차를 자동화한다.

| Runbook | 실행 시점 | 역할 |
|---|---|---|
| `dr-precheck.ps1` | Recovery Plan 실행 전 | ASR Health, DR VNet/Subnet, Quota, DNS 상태 확인 |
| `dr-health-check.ps1` | VM Group 기동 후 | DB/WAS/WEB 서비스 상태 확인 |
| `dr-dns-switch.ps1` | 서비스 정상 확인 후 | Private DNS 또는 서비스 DNS를 DR IP로 전환 |
| `dr-inventory-update.ps1` | DR 절차 종료 전 | Azure Resource Graph 기반 Inventory/CMDB 갱신 |

## 2. Recovery Plan 권장 순서

| Group | 대상 | Action |
|---|---|---|
| Pre Action | 전체 | `dr-precheck.ps1` |
| Group 1 | DB | DB VM Failover |
| Post Group 1 | DB | DB Listener/Port/Process 확인 |
| Group 2 | WAS | WAS VM Failover |
| Post Group 2 | WAS | WAS 서비스 시작 및 DB 연결 확인 |
| Group 3 | WEB | WEB VM Failover |
| Post Group 3 | WEB | Web URL, Backend Health 확인 |
| Final Action | DNS/Inventory | DNS 전환, Inventory 갱신, 알림 발송 |

## 3. 권한

Automation Account Managed Identity에는 최소한 아래 권한이 필요하다.

| 대상 | 권한 |
|---|---|
| Recovery Services Vault | Site Recovery Contributor |
| DR Resource Group | Contributor 또는 제한된 Custom Role |
| Private DNS Zone | Private DNS Zone Contributor |
| Log Analytics / Monitor | Monitoring Reader |
| Resource Graph 조회 | Reader |

## 4. 운영 시나리오

### Test Failover

- 운영 서비스 영향 없이 DR Drill 수행
- Test Network를 별도 구성
- Test Failover 후 반드시 Cleanup Test Failover 수행

### Planned Failover

- 주센터가 살아 있고 계획된 전환이 가능한 경우 사용
- 데이터 손실 최소화 가능

### Unplanned Failover

- 실제 장애 발생 시 사용
- 최신 Recovery Point 기준으로 DR VM 기동

## 5. 주의사항

- DNS 전환 전 DR Web/WAS/DB 상태 확인이 선행되어야 한다.
- DB 정합성 검증 전 외부 트래픽을 열지 않는다.
- Runbook 실패 시 Manual Action 절차를 반드시 준비한다.
