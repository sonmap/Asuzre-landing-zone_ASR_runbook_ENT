# Repository Redesign: 기존 Landing Zone + D-prefix DR 확장

## 1. 재정의 목적

초기 skeleton은 DR 영역을 `50-dr`, `60-operations` 중심으로 만들었으나, 운영 관점에서는 기존 Landing Zone 구조를 먼저 복사하고, DR 영역을 동일한 계층으로 분리하는 편이 명확하다.

따라서 본 저장소의 표준 구조는 다음과 같이 재정의한다.

- 기존 주센터 영역: `00`, `10`, `20`, `30`, `40`
- DR센터 영역: `D00`, `D10`, `D20`, `D30`, `D40`
- ASR 신규 제어 영역: `50-asr`
- Runbook / Inventory / Monitor 운영 영역: `60-operations`

## 2. 번호 체계

| 기존 영역 | 역할 | DR 대응 영역 | 설명 |
|---|---|---|---|
| `00-foundation` | 주센터 Resource Group | `D00-foundation` | DR Resource Group |
| `10-platform` | 주센터 Hub/Platform | `D10-platform` | DR Hub/Platform |
| `20-workload` | 주센터 업무 Spoke | `D20-workload` | DR 업무 Spoke |
| `30-services` | 주센터 VM/AKS/LB | `D30-services` | DR 서비스 Placeholder |
| `40-access` | 주센터 DNS/PE/Rule | `D40-access` | DR DNS/PE/Rule |
| 신규 | ASR Control | `50-asr` | Vault, Policy, Recovery Plan |
| 신규 | 운영 자동화 | `60-operations` | Runbook, Inventory, Monitor |

## 3. 구성 원칙

### 3.1 기존 환경 유지

`azure-landing-zone_test04_ENT`의 기존 구조는 주센터 기준으로 유지한다.

```text
live/00-foundation/
live/10-platform/
live/20-workload/
live/30-services/
live/40-access/
```

### 3.2 DR 영역은 D-prefix로 분리

DR센터는 주센터와 동일한 계층을 갖지만 이름 충돌을 방지하기 위해 `D` prefix를 붙인다.

```text
live/D00-foundation/
live/D10-platform/
live/D20-workload/
live/D30-services/
live/D40-access/
```

### 3.3 ASR과 Runbook은 신규 운영 기능

ASR은 단순 DR 네트워크 자원이 아니라 복제/기동 제어 영역이므로 별도 `50-asr`로 둔다.
Runbook, Inventory, Monitor는 운영 자동화 성격이므로 `60-operations`로 둔다.

```text
live/50-asr/
live/60-operations/
```

## 4. DR 네트워크 표준

| 구분 | 주센터 | DR센터 |
|---|---|---|
| Hub VNet | `10.10.0.0/16` | `10.110.0.0/16` |
| Workload VNet | `10.20.0.0/16` | `10.120.0.0/16` |
| Web Subnet | `10.20.0.0/24` | `10.120.0.0/24` |
| WAS Subnet | `10.20.1.0/24` | `10.120.1.0/24` |
| DB Subnet | `10.20.2.0/24` | `10.120.2.0/24` |
| PE Subnet | `10.20.3.0/24` | `10.120.3.0/24` |
| Agent Subnet | `10.20.4.0/24` | `10.120.4.0/24` |

## 5. 배포 순서

```text
기존 주센터:
00 -> 10 -> 20 -> 30 -> 40

DR 기반:
D00 -> D10 -> D20 -> D40

ASR/운영:
50-asr/recovery-vault-jpe
60-operations/automation-dr
50-asr/asr-sales-prod
50-asr/recovery-plan-sales-prod
60-operations/inventory
```

## 6. D30의 의미

`D30-services`는 평상시 VM을 생성하기 위한 영역이 아니다.

ASR 방식에서는 DR VM이 평상시 미기동이며, Failover 시점에 Recovery Services Vault/ASR가 DR VNet/Subnet에 VM을 생성한다.

따라서 `D30-services`는 아래 용도로 사용한다.

- DR 서비스 Placeholder 문서화
- DR VM naming rule 관리
- DR subnet mapping 관리
- Failover 후 Inventory 비교 기준 관리
- 필요 시 Agent VM 또는 Bastion/Jump VM 같은 상시 운영 DR 관리 자원만 제한적으로 생성

## 7. 정리 대상

초기 skeleton에서 사용한 아래 경로는 신규 표준에서는 정리 대상이다.

```text
live/50-dr/
```

신규 표준 경로는 다음이다.

```text
live/50-asr/
```
