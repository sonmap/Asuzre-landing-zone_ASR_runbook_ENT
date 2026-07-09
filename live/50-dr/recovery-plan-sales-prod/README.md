# Recovery Plan Sales Prod Skeleton

이 영역은 ASR Recovery Plan의 구조를 문서화하고, 실제 Runbook 연결 전 설계값을 관리하기 위한 skeleton입니다.

## Recovery Plan Group

| Group | 대상 | Action |
|---|---|---|
| Pre Action | 전체 | `dr-precheck` |
| Group 1 | DB VM | `db01` Failover |
| Post Group 1 | DB | DB Health Check |
| Group 2 | WAS VM | `was01`, `was02` Failover |
| Post Group 2 | WAS | WAS Service Check |
| Group 3 | WEB VM | `web01`, `web02` Failover |
| Final Action | DNS / Inventory | DNS Switch, Inventory Update |

## 수동 검증 항목

- Recovery Services Vault에 VM Protected Item이 등록되어 있는지 확인
- Test Failover용 Isolated VNet 준비 여부 확인
- Runbook Managed Identity 권한 확인
- DNS 전환 전 서비스 Health Check 수행
- Test Failover 후 Cleanup Test Failover 수행

## CLI 확인 예시

```bash
az backup vault list -o table
az resource list -g rg-sl-dr-asr-jpe -o table
az automation runbook list -g rg-sl-dr-automation-jpe --automation-account-name aa-sl-dr-runbook-jpe -o table
```
