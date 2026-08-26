<div align="center">

# Code-Wiki

### 코딩 에이전트를 위한 지속 가능한 프로젝트 메모리

세션이 바뀌어도 승인된 의도를 보존하고, 요구사항에서 코드로 바로 이동하며, 구현을 프로젝트 계약에 맞게 유지합니다.

[![Version](https://img.shields.io/badge/version-0.3.0-2563EB)](../.codex-plugin/plugin.json)
[![Codex Plugin](https://img.shields.io/badge/Codex-plugin-111827)](#codex)
[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code-plugin-D97757)](#claude-code)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../LICENSE)

🇺🇸 [English](../README.md) | 🇰🇷 **한국어**

[설치](#설치) · [작동 방식](#code-wiki의-작동-방식) · [일상적인-사용](#일상적인-사용) · [wiki-구조](#wiki-구조) · [기여](#기여)

</div>

> Code-Wiki는 코딩 에이전트에 **저장소 로컬 기반의 지속 가능한 프로젝트 메모리**를 제공합니다. 하나의 저장소에서 Codex와 Claude Code 플러그인을 함께 배포하며, 두 플러그인은 동일한 7개 스킬을 설치합니다.

| 승인된 의도 | 검증된 구현 | 지속 가능한 탐색 |
| --- | --- | --- |
| Specs는 프로젝트가 **어떻게 동작해야 하는지** 보존합니다. | 소스 검사는 프로젝트가 **현재 어떻게 동작하는지** 확인합니다. | Reference는 각 요구사항 도메인을 현재 코드와 테스트에 연결합니다. |

Code-Wiki는 코드의 변화가 프로젝트 의미를 조용히 덮어쓰지 못하게 하고, 구현이 승인된 명세에 계속 부합하도록 돕습니다.

## 사전 준비

다음 지원 환경 중 하나를 선택하세요.

- `codex plugin` 명령을 사용할 수 있는 Codex
- 플러그인 마켓플레이스를 지원하는 Claude Code
- 독립적인 `SKILL.md` 디렉터리를 불러올 수 있는 호환 에이전트

대상 프로젝트는 로컬 저장소여야 합니다. Code-Wiki는 검사한 소스 리비전을 기록하고 이를 기준으로 오래된 Reference 커버리지를 감지하므로 Git 사용을 강력히 권장합니다. Python 3는 번들된 Wiki 검증기를 직접 실행할 때만 필요합니다.

## 설치

공개 마켓플레이스를 등록한 다음 플러그인을 설치합니다.

### Codex

```bash
codex plugin marketplace add codewiki-labs/codewiki
codex plugin add code-wiki@code-wiki
```

마켓플레이스와 플러그인이 표시되는지 확인합니다.

```bash
codex plugin marketplace list
codex plugin list
```

### Claude Code

터미널에서 다음 명령을 실행합니다.

```bash
claude plugin marketplace add codewiki-labs/codewiki
claude plugin install code-wiki@code-wiki
```

Claude Code 세션 안에서는 `/plugin`이 같은 마켓플레이스·설치 흐름을 대화형으로 엽니다.

셸에서 설치 상태를 확인합니다.

```bash
claude plugin details code-wiki
```

상세 정보에 아래에 설명된 7개 스킬이 모두 표시되어야 합니다.

## 최초 설정

새로 설치한 스킬을 불러오도록 Codex를 재시작하거나 Claude Code에서 `/reload-plugins`를 실행하세요. 그다음 대상 저장소를 열고 새 세션에서 다음과 같이 요청합니다.

```text
이 저장소를 위한 Code-Wiki 프로젝트 메모리를 만들어줘.
```

에이전트는 다음 순서로 작업합니다.

1. 현재 체크아웃의 소스, 설정, 라우트, 스키마, 런타임 구성과 핵심 테스트를 검사합니다.
2. 중요한 기능 표면을 인벤토리로 만들고 도메인 분류 체계를 제안합니다.
3. 임시 `wiki/` 트리를 쓰지 않은 상태에서 행동을 충분히 설명하는 Specs를 검토용으로 제시합니다.
4. 정식 생성, Specs, 분류 체계를 포함하는 한 번의 승인을 기다립니다.
5. 승인된 Specs를 기록하고 소스에 근거한 Reference를 `wiki/` 아래에 생성합니다.
6. 도메인 짝, 커버리지 근거, 관심사 적용 여부와 타입이 있는 링크를 검증합니다.

사용자는 Specs와 분류 체계를 승인하며, 구현 탐색용 Reference까지 검토할 필요는 없습니다. 제안 검토 중 체크아웃이 바뀌면 에이전트는 Wiki를 쓰기 전에 소스 변경 여부를 다시 확인합니다.

## Code-Wiki가 필요한 이유

에이전트는 새 세션마다 프로젝트의 목적, 제약, 요구사항과 코드 경로를 다시 추론하는 경우가 많습니다. 소스를 읽으면 현재 존재하는 동작은 복원할 수 있지만, 사용자가 왜 그 동작을 선택했는지, 어떤 제약을 계속 지켜야 하는지, 프로젝트가 어디로 가야 하는지는 안정적으로 복원하기 어렵습니다.

Code-Wiki는 이 누락된 맥락을 프로젝트 메모리로 다룹니다.

- 프로젝트가 존재하는 이유
- 제품 우선순위와 전체 방향
- 지속해야 하는 요구사항과 비목표
- 도메인이 소유하는 아키텍처, 보안, 신뢰 경계 불변조건
- 중요한 판단 근거
- Acceptance Criteria
- 각 요구사항 도메인에서 구현으로 가는 탐색 경로

Code-Wiki는 과거 대화 전체가 아니라 **현재 유효한 의도**를 저장합니다. 자세한 변경 이력은 Git이 담당합니다.

최초 생성에서는 분류 체계를 확정하기 전에 비정규 **Feature Surface Inventory**도 만듭니다. 모든 중요 기능은 하나의 주 도메인에 배정하거나 소스 근거와 함께 명시적으로 제외해야 합니다. 승인 후 이 소스 기반 상태는 `reference/coverage.json`에 저장됩니다. **coverage gate**는 중요 기능이 누락되거나, 설명이 얕거나, 근거가 모호한 제안을 차단합니다.

Code-Wiki는 **Spec만 승인하는 방식**을 사용합니다. 사용자는 행동을 충분히 설명하는 Specs와 분류 체계를 승인하고, 에이전트는 소스에 근거한 Reference를 생성하고 유지합니다. 별도의 **authority-leakage gate**는 권한, 계산, 가격 우선순위, 불변조건, 수명주기 보장, 실패 정책, 보존이나 감사 의미가 Reference에만 존재하는 것을 거부합니다.

## Code-Wiki의 작동 방식

```text
사용자가 승인한 의도           현재 체크아웃
          │                         │
          ▼                         ▼
        Specs ── 적합성 검사 ──> 소스 코드
          │                         │
          └──── 요구사항 ID ───────┤
                                    ▼
                              Reference 지도
```

Specs는 프로젝트가 어떻게 동작해야 하는지 답합니다. 소스 코드와 관찰된 런타임 상태는 현재 어떻게 동작하는지 답합니다. Reference는 해당 구현을 빠르게 찾게 하지만 어느 권한도 덮어쓰지 않습니다. 이 분리는 우연한 구현 세부사항을 영구 요구사항으로 만들지 않으면서도 에이전트가 맥락을 빠르게 복원하게 합니다.

## 권한 모델

Code-Wiki는 질문 종류에 따라 서로 다른 권한을 사용합니다.

| 질문 | 권한 | 충돌할 때 |
| --- | --- | --- |
| 어떻게 동작해야 하는가? | 사용자가 승인한 Specs | 코드를 Spec에 맞게 수정합니다. |
| 현재 어떻게 동작하는가? | 소스 코드와 관찰된 런타임 상태 | 활성 구현을 검사합니다. |
| 구현이 어디에 있는가? | Reference | 검증된 코드에서 Reference를 갱신합니다. |

Specs는 규범적이고 Reference는 설명적입니다.

```text
Spec != Code
→ Code 수정

Reference != Code
→ Reference 수정
```

Reference는 탐색 계층이지 소스 검사를 대체하지 않습니다. 코드 변경은 Reference를 갱신할 수 있지만 승인된 Specs를 조용히 다시 쓰지는 못합니다.

## Wiki 구조

```text
wiki/
├── index.md
├── specs/
│   ├── index.md
│   ├── project.md
│   ├── policies/               # 승인된 도메인 횡단 정책만
│   │   ├── architecture.md
│   │   └── security.md
│   └── domains/
│       └── <domain>.md
└── reference/
    ├── index.md
    ├── overview.md
    ├── coverage.json
    ├── views/                  # 적용 가능한 소스 기반 관점
    │   ├── architecture.md
    │   └── security.md
    ├── data-flow.md
    ├── data-models.md
    ├── api-surface.md
    ├── configuration.md
    ├── dependencies.md
    ├── commands.md
    ├── testing.md
    ├── gotchas.md
    ├── glossary.md
    └── domains/
        └── <domain>.md
```

`wiki/index.md`는 권한과 탐색 라우터입니다. `wiki/specs/index.md`는 도메인 레지스트리이며, `wiki/specs/project.md`는 모든 프로젝트 세션에서 읽는 짧은 전역 메모리입니다.

### Specs

Specs는 승인된 의미를 보존하고 Reference 없이도 올바른 동작을 판단할 수 있게 합니다.

- 프로젝트 목적, 우선순위, 전역 의도, 제약과 비목표
- 안정적인 요구사항 ID(`-Rddd`)와 Acceptance Criterion ID(`-ACddd`)만 사용하는 간결한 3단계 제목
- 도메인 Intent, 행위자 권한, 계산과 정책, 불변조건, 수명주기와 실패 결과, 보존과 감사 의미, Constraints, Rationale
- 실제로 여러 도메인에 걸치는 규칙만 두는 `specs/policies/`의 승인된 정책
- 계산에 유용한 직접 계산 예시를 포함한 테스트 가능한 Acceptance Criteria
- 재귀적인 `Required Context` 링크와 비재귀적인 `See Also` 링크

정규 Specs에는 현재 승인된 요구사항만 들어갑니다. 최초 생성 중에는 완전한 Spec 제안이 승인 흐름 안에 머무르며, 승인 전에 `wiki/` 아래에 Spec, Reference, 빈 골격이나 영구 초안을 만들지 않습니다. 보안은 필수 도메인이 아니라 관심사입니다. 인증, 인가, 소유권, 노출, 시크릿, 민감 데이터와 신뢰 경계는 이를 소유하는 도메인 Specs에 둡니다. 빈 전역 정책 자리표시자는 만들지 않습니다.

### Reference

에이전트용 Reference는 승인된 도메인을 현재 구현에 연결합니다.

- 중요 기능 커버리지와 종단 간 추적
- 진입점과 소스 경로
- 주요 심볼, 라우트, 작업과 데이터 모델
- 안정적인 요구사항 ID에서 인가·불변조건 강제로 이어지는 `Spec Basis` 링크
- 적용 가능한 수명주기, 실패, 사용량, 비용, 감사, 공급자, 보존, 취소와 삭제 구현
- 코드 근거가 있는 계약 산출물과 변경 전 점검 사항
- 테스트와 검증 위치
- 향후 소스 검사를 빠르게 만드는 구현 세부사항

모든 Spec에는 대응하는 Reference가 있습니다. project는 overview와, 두 index는 서로, policy는 같은 이름의 view와 짝을 이룹니다. Spec과 Reference의 도메인 트리는 동일한 상대 경로 파일 집합을 가져야 하며 Reference 전용 도메인 파일은 유효하지 않습니다. 하나의 논리 도메인은 여러 패키지, 서비스, 프런트엔드 영역과 테스트를 가리킬 수 있습니다. commands, configuration, testing, dependencies, glossary 같은 운영 페이지와 도메인 횡단 Reference view에는 그 외의 Spec이 필요하지 않습니다.

Policy와 view의 짝은 의도적으로 비대칭입니다. `specs/policies/<concern>.md`는 항상 `reference/views/<concern>.md`를 요구하지만, `coverage.json`에 기록되고 지속 의도를 새로 만들지 않는 소스 기반 view는 policy 없이 존재할 수 있습니다. manifest는 모든 기능 배정과 보안·아키텍처 적용 여부를 기록합니다. 근거가 있는 `not_applicable`은 검사 범위에서 중요한 프로젝트 고유 관심사가 발견되지 않았다는 뜻이므로 빈 policy나 view가 필요하지 않습니다.

Deep Reference는 계속 설명적입니다. 관찰된 동작을 승인된 의도로 승격하지 않고 코드에 근거한 구현 증거를 기록합니다. 생성과 감사 스킬은 페이지 길이·도메인 수·파일 수가 아니라 중요 기능 커버리지, 완전한 추적, `Spec Basis`, 정확한 근거로 깊이를 판단합니다.

## 기본 워크플로

프로젝트 관련 작업에서 플러그인은 다음 검색·변경 절차를 따릅니다.

1. `wiki/index.md`와 간결한 `wiki/specs/project.md`를 불러옵니다.
2. 도메인 레지스트리에서 직접 관련된 Specs를 찾습니다.
3. 선택한 Spec과 재귀적인 `Required Context` 전체를 읽습니다. `See Also`는 직접 관련될 때만 한 단계로 따라갑니다.
4. `reference/coverage.json`에서 기능·관심사 적용 여부를 확인하고 필요한 대응 도메인과 manifest에 기록된 view를 읽습니다.
5. Reference에서 소스 코드로 이동해 현재 동작을 검증합니다.
6. 요청이 지속 의도를 바꾸는지 판단합니다.
7. 필요하면 정확한 Spec 변경안을 작성하고 사용자 승인을 받습니다.
8. 정규 Specs를 갱신하고 구현한 뒤 Acceptance Criteria를 검증합니다.
9. 검증된 구현 구조가 바뀌면 Reference, 커버리지 근거와 관련 view를 갱신합니다.

사용자에게는 **Spec 적합성 매트릭스**로 완료 결과를 보고합니다: `요구사항 ID → 검증 결과 → 통과 또는 불일치`. 요청하면 소스와 Reference 근거도 제시할 수 있지만, 사용자가 구현 적합성을 판단하기 위해 Reference를 읽을 필요는 없습니다.

항상 읽는 것은 라우터와 프로젝트 메모리뿐입니다. 정책, 도메인, 커버리지, view와 운영 Reference 페이지는 작업에 필요할 때만 불러옵니다.

정확한 요구사항을 제시하면서 구현을 요청하면 해당 내용의 승인으로 간주합니다. 모호하거나 충돌하는 지속 요청은 구현 전에 Spec 변경안을 제시해야 합니다. 일회성 디버깅 명령, 임시 테스트 지시, 단기 우회책과 구현 계획은 프로젝트 메모리가 아닙니다.

## 일상적인 사용

초기 Wiki가 존재하면 프로젝트 맥락이 필요한 일반 저장소 요청에서 bootstrap 스킬이 자동으로 동작합니다. 매번 Code-Wiki를 직접 지칭할 필요는 없습니다.

### 프로젝트에 질문하기

```text
공개 검색 권한은 어떻게 결정돼?
```

에이전트는 전역 프로젝트 의도를 복원하고, 필요한 최소 Spec 문맥을 읽은 다음, 대응 Reference에서 현재 소스로 이동해 검증된 구현 근거로 답합니다.

### 기존 동작 변경하기

```text
문서 내보내기에서 원래 파일명을 보존하도록 바꿔줘.
```

지속적인 동작 변경이면 에이전트가 영향을 받는 요구사항을 찾습니다. 요청이 충분히 정확하면 그 내용 자체를 승인으로 간주하고, 그렇지 않으면 정규 Specs나 구현을 수정하기 전에 정확한 Spec 변경안을 제안합니다. 완료 결과는 안정적인 요구사항 ID와 Acceptance Criterion ID를 기준으로 보고합니다.

### Spec과 코드의 불일치 수정하기

```text
승인된 업로드 Spec은 200 MB인데 검증기가 100 MB를 강제해. 고쳐줘.
```

승인된 Spec이 권한을 유지하므로 구현을 수정하고 검증합니다. 구현은 맞지만 Reference가 오래된 코드를 가리키면 Reference만 갱신합니다.

### 프로젝트 메모리 갱신 또는 감사하기

```text
이 구현 변경 후 Code-Wiki Reference를 갱신해줘.
```

```text
오래된 경로, 누락된 기능 커버리지, authority leakage가 있는지 Code-Wiki를 감사해줘.
```

Reference 갱신은 승인 없이 검증된 구현 사실을 반영합니다. 감사는 먼저 발견 사항을 보고하며 승인된 Specs를 조용히 다시 쓰지 않습니다. 200줄보다 긴 Wiki 페이지는 압축 검토 후보로 보고하지만, 크기만으로 승인된 의미를 삭제할 권한은 생기지 않습니다.

### 생성된 Wiki 직접 검증하기

Code-Wiki 체크아웃이나 설치된 플러그인 루트에서 실행합니다.

```bash
python3 scripts/validate_generated_wiki.py \
  --repo-root /absolute/path/to/project \
  --wiki-root /absolute/path/to/project/wiki
```

종료 코드 `0`은 구조·의미 검사를 통과했다는 뜻입니다. 0이 아닌 종료 코드는 짝, manifest, 근거, 링크 또는 최신성 오류를 구체적으로 출력합니다. Git 저장소의 `source_revision`은 변경 불가능한 전체 커밋 ID여야 합니다. 이후 Wiki만 바꾼 커밋은 유효하지만 Wiki 외의 커밋된 변경은 커버리지를 오래된 상태로 만들며, 커밋하지 않은 소스는 기록된 스냅샷 밖의 상태라는 경고를 발생시킵니다. 이 검증기는 소스 검사와 프로젝트 테스트를 보완하지만 대체하지 않습니다.

## Superpowers와 함께 사용하기

Code-Wiki와 Superpowers는 서로 다른 책임을 담당합니다.

- **Code-Wiki:** 지속 가능한 WHAT, WHY, WHERE — 프로젝트 메모리, 승인된 Specs, 코드 탐색
- **Superpowers:** HOW — 브레인스토밍, 계획, TDD, 실행, 리뷰, 검증 워크플로

Code-Wiki는 Superpowers를 대체하거나 일회성 구현 계획을 영구 저장하지 않습니다. Superpowers를 사용할 수 없으면 스킬은 `회상 → 검사 → 승인 → 구현 → 검증 → 갱신`의 가벼운 흐름만 제공합니다.

## 스킬

| 스킬 | 사용 시점 |
| --- | --- |
| `using-code-wiki` | 프로젝트 작업을 시작하고, 메모리와 권한 규칙을 복원하며, 작업을 적절한 스킬로 전달합니다. |
| `creating-code-wiki` | Wiki를 처음 만들거나 크게 재생성합니다. |
| `reading-code-wiki` | 전역 의도와 필요한 최소 요구사항 도메인 문맥을 복원합니다. |
| `exploring-code-with-wiki` | Reference를 따라 소스를 검사하고 현재 코드와 승인된 Specs를 비교합니다. |
| `updating-code-wiki` | 승인된 Spec 변경을 적용하거나 설명적인 Reference를 갱신합니다. |
| `auditing-code-wiki` | 권한, 승인, 도메인 짝, 최신성과 에이전트 유용성을 검사합니다. |
| `writing-code-wiki-skills` | 이 패키지의 스킬 경계, 문서, 메타데이터와 테스트를 유지합니다. |

일반 저장소 작업에서는 사용자가 “Code-Wiki를 사용해”라고 직접 말할 필요가 없습니다. bootstrap 스킬이 저장소 맥락이 필요할 때 프로젝트 메모리를 확인합니다.

## 예제

생성, 검색, 불일치, 승인, 갱신과 감사 시나리오는 [기본 워크플로 예제](../examples/basic-workflow.md)를 참고하세요.

## 독립형 스킬 설치

플러그인 설치는 검증기와 패키지 메타데이터를 함께 제공하므로 권장 방식입니다. 호환 에이전트나 스킬 전용 설치에서는 저장소를 복제하고 모든 스킬 디렉터리를 복사하세요.

```bash
git clone https://github.com/codewiki-labs/codewiki.git
cd codewiki

# Codex: 현재 사용자에게 설치
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/* "${CODEX_HOME:-$HOME/.codex}/skills/"

# Claude Code: 현재 사용자에게 설치
mkdir -p "$HOME/.claude/skills"
cp -R skills/* "$HOME/.claude/skills/"

# Claude Code: 특정 프로젝트에만 설치
mkdir -p /path/to/project/.claude/skills
cp -R skills/* /path/to/project/.claude/skills/
```

`using-code-wiki`가 지원 동작으로 라우팅할 수 있도록 7개 스킬을 모두 설치하세요. 라우터만 복사하면 불완전한 설치가 됩니다. `cp`는 같은 이름의 기존 디렉터리를 병합하거나 파일을 덮어쓸 수 있으므로 수동 설치를 업그레이드하기 전에 로컬 수정 사항을 확인하세요.

스킬 전용 설치는 번들된 검증기를 복사하지 않습니다. `scripts/validate_generated_wiki.py`를 실행하려면 복제한 체크아웃을 유지하거나 전체 플러그인 payload를 설치하세요.

## 플러그인 관리

### 업데이트

Codex:

```bash
codex plugin marketplace upgrade code-wiki
codex plugin add code-wiki@code-wiki
```

Claude Code:

```bash
claude plugin marketplace update code-wiki
claude plugin update code-wiki
```

수동 설치에서는 체크아웃을 pull한 다음 해당 복사 명령을 다시 실행합니다. Codex를 재시작하거나 Claude Code에서 `/reload-plugins`를 실행한 뒤 새 세션을 시작해 현재 스킬 지침을 다시 불러오세요.

### 삭제

Codex:

```bash
codex plugin remove code-wiki@code-wiki
codex plugin marketplace remove code-wiki
```

Claude Code:

```bash
claude plugin uninstall code-wiki
claude plugin marketplace remove code-wiki
```

플러그인을 삭제해도 프로젝트의 `wiki/` 디렉터리는 삭제되지 않습니다.

### 문제 해결

Codex:

```bash
codex plugin marketplace list
codex plugin list
codex plugin list --available --json
```

Claude Code:

```bash
claude plugin list
claude plugin details code-wiki
```

플러그인이 설치됐지만 스킬이 보이지 않으면 플러그인과 마켓플레이스 manifest가 버전 `0.3.0`을 가리키는지 확인하고, 마켓플레이스를 갱신한 뒤 플러그인을 다시 설치하고 새 세션을 시작하세요. 독립형 설치에서는 호스트의 스킬 디렉터리에 7개 `skills/<name>/SKILL.md` 파일이 모두 존재하는지 확인하세요. 스킬 전용 설치에는 `scripts/validate_generated_wiki.py`가 포함되지 않습니다.

## 기여

스킬 경계, 계약 기대사항과 로컬 검증 방법은 [CONTRIBUTING.md](../CONTRIBUTING.md)를 참고하세요.

## 라이선스

MIT. [LICENSE](../LICENSE)를 참고하세요.
