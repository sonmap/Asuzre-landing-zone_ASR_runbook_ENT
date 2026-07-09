# 50-asr / recovery-vault-jpe

ASR 신규 제어 영역이다.

기존 Landing Zone 번호 체계와 분리하여 `50-asr`에서 관리한다.

## 역할

- Recovery Services Vault 생성
- ASR Replication Policy 연결 기준 관리
- Protected Item 등록 전 Vault 기준값 제공

## 위치

| 항목 | 값 |
|---|---|
| Region | Japan East |
| Resource Group | `rg-sl-dr-asr-jpe` |
| Vault | `rsv-sl-asr-jpe` |

## 실행 예

```bash
./tools/tf_root.sh live/50-asr/recovery-vault-jpe plan
./tools/tf_root.sh live/50-asr/recovery-vault-jpe apply
```
