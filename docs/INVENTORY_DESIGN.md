# Inventory / CMDB 설계

## 1. Inventory 목적

DR 구성에서는 설계값과 실제 운영 상태를 구분해서 관리해야 한다.

| 구분 | 생성 시점 | 내용 |
|---|---|---|
| Design Inventory | Terraform plan/apply 후 | VNet/Subnet/VM/ASR 설계값 |
| Runtime Inventory | 주기적 또는 DR 직후 | 실제 Azure Resource Graph 조회 결과 |
| ASR Inventory | ASR 보호 설정 후 | Protected Item, Replication Health, Recovery Plan |
| Failover Inventory | Failover 후 | DR VM ID, NIC, Private IP, Boot 상태 |
| Ansible Inventory | VM 기동 후 | Hostname, Private IP, Role, User |

## 2. Azure Resource Graph 예시

```bash
az graph query -q "Resources | project resourceGroup, name, type, location, id | order by resourceGroup asc, name asc" -o json
```

## 3. DR VM 조회 예시

```bash
az graph query -q "Resources | where resourceGroup =~ 'rg-sl-sales-prod-dr-jpe' | project name, type, location, id, tags" -o json
```

## 4. 출력 파일 구조

```text
inventory/output/
  primary-krc.json
  dr-jpe-design.json
  dr-jpe-runtime.json
  asr-protected-items.json
  failover-result-YYYYMMDD-HHMM.json
  ansible-dr.ini
```

## 5. CMDB 연계 방향

1. Terraform output 수집
2. Azure Resource Graph로 실제 자원 조회
3. ASR 상태 조회
4. JSON 표준 포맷 생성
5. ITSM/CMDB API 또는 수동 업로드 파일로 전달

## 6. 필수 태그

| Tag | 설명 |
|---|---|
| `env` | prod/dev/dr |
| `region_role` | primary/dr |
| `workload` | sales/policy/digital 등 |
| `role` | web/was/db/agent |
| `dr_protected` | true/false |
| `asr_policy` | ASR 정책명 |
| `itsm_ticket` | 변경 요청 번호 |
