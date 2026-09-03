# Week 01 Visual System — BLACK / WHITE / NAVY / BLUE

이 문서는 79장으로 구성한 Week 01 강의안의 시각 구현 기준이다. 특정 브랜드의 로고나 UI를 복제하지 않고, 한국 패션 에디토리얼의 강한 흑백 대비·날카로운 그리드·절제된 파란색을 기술 강의에 맞게 번역한다. 전체 16주 공통 제작 원칙은 [PPT 제작 가이드](PPT_PRODUCTION_GUIDELINE.md)를 따른다.

## 시각 원칙

1. 한 장에는 `개념·비교·근거·실행·판정` 가운데 하나의 역할만 둔다.
2. 이미지는 장식이 아니라 사례·증거·맥락일 때만 사용한다.
3. 흰색·밝은 회색과 검정·네이비 배경을 구간에 맞게 교대해 호흡을 만든다.
4. 둥근 카드형 대시보드 대신 선, 면, 숫자, 간격, 활자로 위계를 만든다.
5. 같은 레이아웃 실루엣을 세 장 연속 사용하지 않는다.
6. 파랑은 위치나 순서가 아니라 현재 변수·운영 증거·판정 상태처럼 의미가 있을 때만 사용한다.

## 색상

| Token | Hex | 역할 |
|---|---|---|
| `BLACK` | `#050505` | 표지, 강한 구분 장표 |
| `INK` | `#191919` | 제목, 본문, 기본 도식 |
| `WHITE` | `#FFFFFF` | 기본 배경, 어두운 면의 본문 |
| `PAPER` | `#F7F8FA` | 밝은 보조 면과 화면 호흡 |
| `NAVY` | `#0B1F3A` | 구분 장표와 구조 강조 |
| `BLUE` | `#2563EB` | 현재 변수, 운영 증거, 판정 상태 |
| `BLUE_SOFT` | `#E0F0FE` | 약한 비교 면과 annotation |
| `GRAY` | `#667085` | 보조 본문 |
| `HAIRLINE` | `#D0D5DD` | 구분선 |

- 주황·빨강·노랑·초록·보라·시안은 장식 색으로 사용하지 않는다.
- gradient, glow, glassmorphism, 다색 module coding을 사용하지 않는다.
- 실제 제품 화면과 screenshot은 원래 색을 유지하며 색상 overlay를 씌우지 않는다.
- 같은 위계의 항목은 같은 색과 무게를 유지한다.
- 마지막 항목·오른쪽 열·마지막 슬라이드라는 이유만으로 파랑을 적용하지 않는다.

## Typography

- 한국어: `AppleGothic` 또는 최종 변환 환경에서 확인된 일반 고딕체
- 숫자·영문: `Helvetica Neue`
- 코드: `Menlo`

| 요소 | 최소 | 권장 |
|---|---:|---:|
| 표지 제목 | 54pt | 58–64pt |
| Section 제목 | 44pt | 46–50pt |
| 일반 제목 | 38pt | 40–44pt |
| 중간 제목·핵심 수치 | 24pt | 26–32pt |
| 본문 | 18pt | 20–24pt |
| 표 Cell | 17pt | 18–20pt |
| Code | 16pt | 17–19pt |
| Micro label·footer | **14pt** | 14–16pt |

- 화면에 보이는 모든 텍스트의 절대 최소 크기는 14pt다.
- `shrinkText`로 overflow를 숨기지 않는다. 문장 축약, 정보 통합, 장표 분할, 레이아웃 변경 순서로 해결한다.
- 제목은 2–8단어의 한 줄 명사형을 기본값으로 한다.
- 표지 제목·장표 제목·부제에는 `합니다`, `됩니다`, `있습니다`, `~다` 같은 문장형 종결어미와 마침표를 쓰지 않는다.
- 표지 부제는 설명 문장 대신 `기술 · 과업 · 산출물` 키워드 조합으로 구성한다.

## Layout

- Canvas: 16:9, 1280 × 720
- 안전 여백: 좌우 64px, 상단 40px, 하단 42px
- 기본 구조: 12-column grid, column gap 24px, section gap 32px
- 모서리: 0–4px
- 기본 정렬: 제목·본문·하단선의 왼쪽 기준선 통일

79장 전체에서 다음 실루엣을 내용에 맞게 교차 사용한다.

1. 최소 표지와 dark section divider
2. 대형 명제와 단일 수식
3. 좌우 분류 비교와 matrix
4. 세로형 `01–05` 단계 목록
5. Timeline, ladder, cost staircase
6. 폐루프 lifecycle과 swimlane
7. Trace anatomy와 schema specimen
8. 실제 UI 확대와 번호 annotation
9. Terminal command와 expected signal
10. Failure–recovery map과 application checkpoint

단계명은 2–6어절, 설명은 두 줄 이하로 제한한다. 시간·의존 관계가 실제로 있을 때만 화살표를 사용한다. 긴 단계명은 가로 한 줄로 이어 붙이지 않고 번호와 개행으로 읽기 순서를 만든다.

## 반복 요소

- `W01 / LLMOPS` micro label
- 우측 상단 두 자리 slide number
- 1px hairline divider
- 의미 기반 blue rule 또는 작은 square
- section break의 giant index

반복 요소도 14pt 최소 크기와 의미 기반 강조 원칙을 따른다. 장표 번호나 마지막 위치에는 자동 강조를 적용하지 않는다.

## 접근성·배포

- 모든 텍스트와 도형은 PowerPoint에서 편집 가능하게 유지한다.
- dark/light 배경 모두 충분한 텍스트 대비를 확보한다.
- 의미 있는 screenshot에는 대체 텍스트를 지정한다.
- 모든 장표의 발표자 노트에 `[Sources] ... [/Sources]` 블록을 둔다.
- 공개본에는 개인 연락처, 현직 회사·팀명, 내부 사례·지표, API key, 로컬 절대경로를 넣지 않는다.
- 최종본은 79장을 모두 렌더해 overflow, 겹침, 제목 개행, 14pt 미만 텍스트, 금지 색상, 동일 레이아웃 3장 연속 여부를 확인한다.
