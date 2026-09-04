# Week 01 검증 보고서

검증 기준일: 2026-09-04
대상: Week 01 강의 자료와 TRACE/01 실습 환경

## 상태 요약

현재 표준 경로의 80장 PowerPoint, 80쪽 인쇄용 PDF, 전체 렌더, 실제 화면 캡처, 실습 서비스, 노트북과 16주 의존성 프로필의 검증이 완료되었다. Qwen3 4B Instruct 로컬 호출까지 실제로 실행했으며, 외부 자격 증명·학생별 장비 차이·교실 부하 시험은 아래 수동 검증 경계에 별도 표기했다.

## 확정된 프레젠테이션 검증 결과

현재 최종화가 완료된 검증 대상은 다음 파일이다. `build/v2`는 재생성 과정에서만 사용하는 로컬 검증 영역으로 Git에서 제외되며, GitHub에서 배포하는 파일은 표준 경로의 PowerPoint, 인쇄용 PDF와 이 보고서다.

- 배포 PowerPoint: week01/lecture/01_week1_llmops_kickoff.pptx
- 인쇄·배포 PDF: output/pdf/01_week1_llmops_kickoff.pdf
- 로컬 생성 산출물(git 제외): week01/lecture/build/v2/output-v3r22/01_week1_llmops_kickoff_v3r22.pptx
- 로컬 검증 영수증(git 제외): week01/lecture/build/v2/staging-v12/01_week1_llmops_kickoff_v3r22.validation.json
- PowerPoint SHA-256: 77e27156b94e21d457511da7e1eff799bf9274455f15c362bd8ebba666b9be26
- PDF SHA-256: 9e7f32f2390a642b564f25d94db6fe5f77341c0d870718856f4cc278b21d70c4

| 영역 | 결과 | 확인 내용 |
|---|---|---|
| PowerPoint 패키지 구조 | PASS | 80 slides, 구조 finding 0건 |
| 슬라이드 크기 | PASS | 13.3333 × 7.5 inch, 16:9 |
| 레이아웃 기하 검사 | PASS | finding 0건, warning 0건 |
| 글꼴 정책 | PASS | AppleGothic·Menlo만 관찰, 1,722개 텍스트 구간 검사 |
| 첫 번째 당사자 가져오기 | PASS | Artifact Tool import 성공, 80 slides 재확인 |
| 네이티브 표 산술 검사 | PASS | 대상 네이티브 표 0개, finding·warning 0건 |
| 네이티브 차트 제목 검사 | PASS | 대상 네이티브 차트 0개, finding 0건 |
| 빌더 장수 정책 | PASS | build-audit.json 기준 정확히 80장 |
| 빌더 최소 글자 크기 정책 | PASS | build-audit.json 기준 가시 텍스트 최소 14pt |
| 레이아웃 다양성 | PASS | build-audit.json 기준 51개 layout type |
| 색상 정책 | PASS | 검정·흰색·네이비·파랑·중립 회색, 금지 주황색 #FF5A36 |
| 학교 비종속성 | PASS | 배포 PowerPoint 화면·발표자 노트와 PDF 추출 텍스트에서 특정 대학명·학교별 교과목 코드 0건 |
| 인쇄용 PDF | PASS | 80쪽, 960.009 × 540pt 가로 페이지, 빈 페이지 0건, 전체 렌더·모판 검수 |
| PDF 글꼴 | PASS | 한글·영문 글꼴 임베딩, 텍스트 추출과 핵심 운영 문구 확인 |

### 검증 범위 해석

- 패키지 구조 검사는 PowerPoint 파일 내부 관계와 슬라이드 수를 확인한다. 문장의 사실성이나 강의 내용의 정확성을 대신하지 않는다.
- 글꼴 정책 검사는 지정 글꼴 사용 여부를 확인한다. 네이티브 PowerPoint 애플리케이션에서의 편집·애니메이션·발표 모드는 별도 수동 확인 영역이다.
- 최소 14pt는 빌더 계측 정책으로 확인했고, 최종 80장 PNG 렌더와 몽타주를 별도로 육안 검수했다.
- 레이아웃 51개는 매니페스트에 기록된 고유 유형 수다. 각 장표의 미적 품질은 전체 몽타주와 핵심 장표 확대 검수로 보완했다.

## 콘텐츠 동기화 확인

- slide-manifest.json과 강의안은 정확히 80개 제목·순번으로 구성.
- 섹션 범위: 1–7, 8–17, 18–32, 33–45, 46–57, 58–65, 66–79, 80.
- 수강 대상 표기: 특정 대학에 한정하지 않는 대학생·대학원생 대상 통합 LLMOps 강좌.
- 자기소개 표기: 무신사 Core AI PM × AI 대학원 겸임교수.
- 학교 비종속성: 표지·공통 푸터·자기소개·발표자 노트·실습 화면에서 특정 대학명과 학교별 교과목 코드 0건.
- 전체 운영: 16주 전체 대면 수업 없이 온라인으로 진행하며, 정규 주차는 실시간 강의를 원칙으로 운영.
- 평가 운영: 중간고사와 실시간 수업 없이 8주차에 기말 프로젝트 기획서 0.1을 온라인으로 제출·평가.
- 제출 묶음: 16주 과정 로드맵, 2페이지 제안서, 제품 요구사항 문서(Product Requirements Document, PRD) HTML과 PowerPoint 요약.
- 기획 고도화 흐름: 초안 0.1 → 교수 설계 리뷰 → 학생 결정 → 수정안 0.2 → 포트폴리오 반영.
- 공휴일 운영: 9월 25일 추석과 10월 9일 한글날은 휴강이 아니며, 정규 실시간 온라인 강의 대신 녹화 강의영상으로 대체.
- 최종 발표: 16주차 기말 프로젝트 발표와 질의응답을 실시간 온라인으로 진행.
- 초반 현재 위치 모듈: 2번 현재 1주차, 3번 16주 일정, 4번 포트폴리오 로드맵, 5번 제출 패키지, 6번 교수 설계 리뷰, 7번 공휴일 주차의 녹화 강의.
- 52번 장표: 중앙 원·대각선 연결선이 아닌 4행 상충 관계 비교표.
- 표현 감사: 사용자 피드백에서 지적된 번역투·추상 표현의 배포 자료 잔존 0건.
- 16번 장표: 02 항목을 2행으로 정리하고 가변 행 높이와 구분선 사이 12px 이상 안전 간격 확보.
- 18번 장표: `모델 성능과 서비스 신뢰성의 간극`으로 제목·부제·교수자 노트 동기화.
- 71·72·74·76번 장표: 각각 실제 Visual Studio Code, 실제 OpenAPI 문서, 실제 Demo 실행 화면, 실제 Qwen3 Instruct 실행 결과·추적 화면 캡처.

## 최종 산출물·실습 통합 검증

| 영역 | 결과 | 확인 내용 |
|---|---|---|
| 표준 경로 반영 | PASS | finalizer 산출물과 표준 PowerPoint의 SHA-256 일치 |
| 전체 렌더 | PASS | `final-render-v25` PNG 80개, 렌더 오류 0건 |
| 오버플로 | PASS | `slides_test.py` 결과 잘림·오버플로 0건 |
| 전체 육안 검수 | PASS | 80장 전수, 변경 장표 원본 1600 × 900 확대, 선·면·텍스트 충돌 0건 |
| 16·18번 확대 검수 | PASS | 16번 행·구분선 분리, 18번 제목·부제·구분선 간격 정상 |
| 55·69번 확대 검수 | PASS | `시간 초과` 복합어 분리와 단독 단어 줄바꿈 해소, API·RAG 풀어쓰기 정상 |
| 52번 확대 검수 | PASS | 4행 비교표, 중앙 원·방사형 선·대각선 연결 0건, 영단어 중간 개행 0건 |
| 실제 캡처 검수 | PASS | 71·72·74·76번 실제 Visual Studio Code·OpenAPI·Demo·Qwen3 Instruct 실행 결과, 민감정보 노출 0건 |
| 응용 프로그래밍 인터페이스 테스트 | PASS | pytest 8건 통과, 실패 0건 |
| Python 정적 검사 | PASS | Ruff check·format check 통과 |
| 의존성 무결성 | PASS | 현재 123개 패키지 호환, 13개 공통·주차별 프로필 해석 충돌 0건 |
| 강의 자료 구조 검사 | PASS | 보존 노트북 16개·작성 노트북 1개, 구조 오류 0건 |
| 실서비스 스모크 검사 | PASS | 건강 상태·현재 설정·Qwen3 Instruct 생성·실행 추적·통계·메트릭 경로 정상 응답 |
| 가이드 노트북 실행 | PASS | 코드 셀 6개 실행, 오류 출력 0건 |

## Qwen3 4B 응답 시간 설정 검증

수업 기본 모델은 `qwen3:4b`가 아니라 `qwen3:4b-instruct`로 고정했다. 현재 Ollama 태그에서 `qwen3:4b`는 Thinking 계열 모델과 같은 식별자를 가리키므로 `think: false`만으로 기대한 속도 개선이 재현되지 않을 수 있다. `--hidethinking`은 사고 과정 표시를 숨기는 옵션이며 생성 연산을 줄이는 설정으로 사용하지 않는다.

| 항목 | 확정값·결과 |
|---|---|
| 모델 | `qwen3:4b-instruct` |
| Thinking 요청값 | `false` — Ollama `/api/chat` 요청의 최상위 필드 |
| 컨텍스트·출력 상한 | `num_ctx=2048`, `num_predict=128` |
| 반복 호출 | `keep_alive=30m`, `seed=42` |
| 실제 로컬 실행 | HTTP 200, `finish_reason=stop`, 출력 토큰 66 |
| 현재 장비 실행 예시 | 전체 1,527.38ms, 모델 적재 16.34ms, 생성 919.74ms |
| 적재 상태 | `ollama ps` 기준 100% GPU, context 2048, 30분 유지 |

응답 시간은 장비·동시 실행·첫 호출 여부에 따라 달라진다. 첫 호출과 두 번째 호출을 분리하고, 사용자 화면과 `/api/v1/traces`에서 모델 적재 시간과 생성 시간을 함께 확인한다. 설정 근거는 [Ollama Thinking 문서](https://docs.ollama.com/capabilities/thinking), [Chat API](https://docs.ollama.com/api/chat), [FAQ](https://docs.ollama.com/faq), [Qwen3 태그](https://ollama.com/library/qwen3/tags)다.

## HTML 문서 검증

| 영역 | 결과 | 확인 내용 |
|---|---|---|
| 내부 링크·문서 구조 | PASS | 세 HTML, 공통 CSS·JavaScript, 로컬 링크, 고유 식별자와 제목 구조 정상 |
| 통합 강좌 표기 | PASS | 세 HTML의 메타·헤더·푸터에서 특정 대학명 0건, 대학생·대학원생 대상 통합 강좌로 통일 |
| 현재 주차 상호작용 | PASS | `?week=4`, `?week=8`, `?week=16`, 주차 버튼, 잘못된 주차값 보정, 두 위치의 현재 주차 표시 동기화 |
| 반응형 화면 | PASS | 1,440px 데스크톱과 390px 모바일에서 문서 가로 넘침 0건 |
| 2페이지 인쇄 | PASS | 2페이지 제안서를 A4 PDF로 출력했을 때 정확히 2쪽, 결론·출처 잘림 0건 |
| 색상 정책 | PASS | 검정·흰색·네이비·파랑·중립 회색만 사용, 주황색·그라데이션·그림자 0건 |

## 권장 검증 명령

환경 변수 PRESENTATIONS_SKILL_DIR에는 Presentations skill의 절대 경로를 지정한다.

~~~bash
# 배포 파일 지문
shasum -a 256 week01/lecture/01_week1_llmops_kickoff.pptx
shasum -a 256 output/pdf/01_week1_llmops_kickoff.pdf

# 인쇄용 PDF 페이지·크기 확인
pdfinfo output/pdf/01_week1_llmops_kickoff.pdf

# PowerPoint 구조·오버플로 재검사
python "$PRESENTATIONS_SKILL_DIR/container_tools/slides_test.py" \
  week01/lecture/01_week1_llmops_kickoff.pptx

# 전체 렌더
python "$PRESENTATIONS_SKILL_DIR/container_tools/render_slides.py" \
  week01/lecture/01_week1_llmops_kickoff.pptx \
  --output_dir week01/lecture/build/v2/final-render-v25

# HTML 문서
python -m http.server 4173 --directory curriculum/2026-2/web

# TRACE/01 실습 코드
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q -p no:cacheprovider week01/lab/tests
.venv/bin/ruff check week01/lab
.venv/bin/ruff format --check week01/lab
.venv/bin/python scripts/check_course_materials.py
uv pip check --python .venv/bin/python
~~~

## 개발환경 기준

- Python 지원 범위: 3.11 이상 3.12 미만.
- 강의 표준 버전: CPython 3.11.14.
- 기본 실습: 외부 자격 증명과 모델 다운로드 없이 동작하는 결정론적 데모 제공자.
- 선택 실습: 로컬 모델 실행 도구 Ollama.
- 콘텐츠 지문(content fingerprint): 익명화 수단이 아니라 동일 입력 비교용 식별자. 개인정보나 기밀 원문을 입력하지 않는다.
- 토큰 추정치(token estimate): 모델 토크나이저 또는 공급자 과금 사용량이 아닌 교육용 추정치.

## 알려진 AS-IS 경고

보존 원본인 practice/week02/02_advanced_reasoning.ipynb의 code cell 20에는 닫히지 않은 문자열 1건이 있다. 원본 보존 범위이므로 Week 01 변경에 포함하지 않는다.

## 수동 검증 경계

- 학생별 운영체제·메모리·가속기에서의 Ollama 설치, 모델 다운로드와 응답 시간 비교.
- OpenAI, Pinecone, Langfuse 자격 증명을 사용하는 외부 호출.
- Hugging Face 모델 다운로드와 단일 단계 지도 미세조정·직접 선호 최적화.
- Linux·CUDA 환경의 양자화 저랭크 적응(Quantized Low-Rank Adaptation, QLoRA)과 bitsandbytes 백엔드.
- 실제 강의장 네트워크의 다중 사용자 부하 시험.
