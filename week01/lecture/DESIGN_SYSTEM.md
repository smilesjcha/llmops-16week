# Week 01 Visual System — BLACK / PAPER / SIGNAL

이 문서는 특정 브랜드의 logo나 UI를 복제하지 않고, 한국 패션 editorial에서 느껴지는 강한 흑백 대비·큰 typography·절제된 signal color를 강의용으로 번역한 기준이다.

## 시각 원칙

1. 한 장에는 한 문장만 주장한다.
2. 이미지는 장식이 아니라 사례·증거·맥락일 때만 쓴다.
3. 흰 배경과 검은 배경을 section 단위로 교대해 호흡을 만든다.
4. 둥근 card dashboard 대신 선, 면, 숫자, 간격으로 위계를 만든다.
5. AI를 뜻하는 보라색 gradient, glow, chat bubble, brain/circuit cliché를 쓰지 않는다.
6. 영어 label은 짧고 좁게, 한국어 주장은 크고 단단하게 쓴다.

## 색상

| Token | Hex | 역할 |
|---|---|---|
| `INK` | `#090909` | 기본 검정, dark section |
| `PAPER` | `#F4F2EC` | 따뜻한 off-white, light section |
| `WHITE` | `#FFFFFF` | 최대 대비 highlight |
| `GRAPHITE` | `#2C2C2C` | dark divider |
| `ASH` | `#979797` | secondary text |
| `SIGNAL` | `#FF5A36` | 핵심 전환·경고·현재 위치 |

`SIGNAL`은 한 화면 면적의 10% 이하로 쓴다. 상태 색상이 필요한 경우에도 새 색을 늘리기보다 `INK / ASH / SIGNAL`의 명도와 패턴으로 구분한다.

## Typography

- 한국어: `Apple SD Gothic Neo`
- 숫자·영문 label: `Helvetica Neue`
- 표지: 64–88 pt, ExtraBold, 자간 타이트
- 본문 제목: 36–48 pt, Bold
- 강조 숫자: 64–120 pt, Bold
- 본문: 18–24 pt
- 작은 label: 11–14 pt, uppercase, tracking 확장
- 16 pt보다 작은 본문은 사용하지 않는다.

## Layout

- Canvas: 16:9, 1280 × 720
- 기본 margin: 좌우 64 px, 상하 48 px
- 12-column grid, gutter 20 px
- 상단: section / slide number
- 하단: 과정명과 출처 표시는 최소화하고 발표자 notes를 우선 사용
- 핵심 수치와 문장은 grid 경계를 의도적으로 넘겨 scale을 만든다.

## 반복 요소

- `W01 / LLMOPS` micro-label
- 우측 상단 두 자리 slide number
- 1 px hairline divider
- `SIGNAL` 세로 bar 또는 작은 square
- section break의 giant index (`01`, `02`, `03`, `04`)

## 모션·전환

- 기본 전환 없음
- live demo 직전과 직후에만 black → paper contrast를 사용
- 순서를 가르치는 그림은 한 장에 모두 표시하되 현재 단계만 `SIGNAL`로 강조

## 접근성·배포

- 모든 텍스트와 도형은 PowerPoint에서 편집 가능하게 유지한다.
- 텍스트 대비는 dark/light 배경 모두 충분히 확보한다.
- 의미 있는 screenshot에는 대체 텍스트를 지정한다.
- 공개본에는 개인 연락처, 현직 회사·팀명, 내부 사례·지표를 넣지 않는다.
