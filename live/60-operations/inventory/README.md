# 60-operations / inventory

DR Inventory / CMDB 갱신 영역이다.

## 역할

- Azure Resource Graph 기반 전체 자원 조회
- 주센터/DR센터 Resource 비교
- ASR Protected Item 상태 조회
- Failover 후 DR VM/NIC/IP 정보 Export
- CMDB/ITSM 연계용 JSON 생성

## 출력 예시

```text
inventory/output/
  primary-krc.json
  dr-jpe-design.json
  dr-jpe-runtime.json
  asr-protected-items.json
  failover-result-YYYYMMDD-HHMM.json
```

## 실행 예

```bash
./tools/export_inventory.sh
```
