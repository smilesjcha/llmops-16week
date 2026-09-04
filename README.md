# Large Language Model Operations (LLMOps) · 16주 과정

현행 LLMOps 수업의 강의안·실습·프로젝트 운영 문서와 2025년 2학기 보존본을 함께 관리하는 저장소다. 2025년 공개 Notion 커리큘럼, 실제 PPTX/PDF와 기존 실습 repository는 `AS-IS` 자료로 보존하고, 현행 학기 설계는 별도 문서에서 관리한다.

## 현행 학기 운영

- [2026년 2학기 운영 커리큘럼](curriculum/2026-2/00_운영_커리큘럼.md)
- [기말 프로젝트 기획서 가이드](curriculum/2026-2/01_기말프로젝트_기획서_가이드.md)
- [제출용 기획서 템플릿](curriculum/2026-2/02_기말프로젝트_기획서_템플릿.md)
- [16주 과정 로드맵](curriculum/2026-2/web/course-roadmap.html)
- [2페이지 프로젝트 제안서](curriculum/2026-2/web/project-proposal-2pager.html)
- [제품 요구사항 문서](curriculum/2026-2/web/project-prd.html)
- 수업 운영: 16주 전체 대면 수업 없이 온라인으로 진행하며, 정규 수업은 실시간 강의를 원칙으로 운영
- 8주차: 중간고사와 실시간 강의 없이 기말 프로젝트 기획서 0.1을 온라인으로 제출·평가
- 16주차: 서비스 구현·평가·시연·포트폴리오 발표를 실시간 온라인으로 진행
- 대상: 특정 대학에 한정하지 않는 대학생·대학원생 대상 통합 강좌
- 교수: 차성재 · 무신사 Core AI PM × AI 대학원 겸임교수
  - AI: Artificial Intelligence · PM: Product Manager

매주의 실행 증거와 의사결정 기록을 기획서에 누적하고, 교수 설계 리뷰 이후 수정 이력을 기말 프로젝트 포트폴리오로 연결한다. 모든 수업은 온라인으로 운영하며, 9월 25일 추석과 10월 9일 한글날 주차만 정규 실시간 온라인 강의 대신 녹화 강의영상을 업로드한다. 두 주차는 휴강이 아니다. 8주차는 실시간 수업 없이 온라인 제출물만으로 평가하고, 16주차 프로젝트 발표는 실시간 온라인으로 진행한다. 배점·영상 시청·제출 일정은 해당 학기 학습관리시스템(Learning Management System, LMS) 공지를 따른다.

## 학생용 주차별 강의안

학생이 매주 확인할 강의안의 기준 위치는 [`output/pdf/`](output/pdf/README.md)다. 이전 학기 자료가 있는 `AS-IS 2025 2nd semester`가 아니라, `main` 브랜치의 주차별 PDF를 사용한다.

현재 저장소는 **Public**으로 운영한다. 강의 기록은 교수자 공개 정보와 개인정보 비식별 처리를 마친 복습본만 연결하며, 수강생 등 제3자의 이름·얼굴·프로필·소속·비공개 대화는 공개하지 않는다.

- 오늘 수업: [01주차 PDF · LLM 서비스 운영의 기본](output/pdf/01_week1_llmops_kickoff.pdf)
- 1주차 복습: [강의영상·음성·채팅 기록](week01/resources/README.md)
- 확인 경로: `llmops-16week` → `output` → `pdf` → 해당 주차 PDF
- 발표용 PowerPoint와 실습 코드: 각 `weekNN` 폴더
- 수정본 확인: 수업 직전 `main` 브랜치 새로고침

## 2025년 2학기 AS-IS 보존본

- 01–16주차 통합 강의안과 핵심 커리큘럼
- 실제 slide range 기반 강의 디자인 storyboard
- 1,002장 슬라이드의 검색용 텍스트 원문
- 기존 notebook 16개와 지원 data/code/artifact
- PPTX/PDF 파일명·크기·SHA-256 인벤토리

## 시작하기

[AS-IS 2025년 2학기 안내](AS-IS%202025%202nd%20semester/README.md)에서 문서와 실습자료를 확인한다.

새로 설계한 첫 수업은 [Week 01 패키지](week01/README.md)에서 바로 시작할 수 있다.

- 80장 강의용 [PowerPoint](week01/lecture/01_week1_llmops_kickoff.pptx), [인쇄용 PDF](output/pdf/01_week1_llmops_kickoff.pdf)와 상세 강의안
- 60–80장 제작 범위와 렌더 QA를 정의한 [PPT 제작 가이드](week01/lecture/PPT_PRODUCTION_GUIDELINE.md)
- black / white / navy / blue 기반 강의 디자인 시스템
- 교수 공개 프로필을 반영한 간결한 자기소개
- offline-first FastAPI 서비스 `TRACE/01`
- Google Drive 비식별 강의영상·음성과 GitHub·Drive 비식별 채팅 복습 자료
- 실행·trace·비교·개선 흐름을 따라가는 실습 notebook
- CPython 3.11.14 공통 환경과 충돌 주차별 dependency profile
- VS Code 작업·실행·테스트·디버깅 구성

강의용 PPT는 명사형 제목, visible text 14pt 이상, 의미 기반 파란색 강조를 공통 정책으로 사용한다. 주황색과 위치 기반 강조를 배제하고, 동일 레이아웃이 세 장 연속 이어지지 않도록 구성한다.

```text
llmops-16week/
├── README.md
├── curriculum/                      # 현행 학기 운영·프로젝트 문서
├── requirements/                    # 16주 공통·주차별 Python profile
├── output/pdf/                     # 검증을 마친 인쇄·배포용 PDF
├── scripts/                         # 자료 구조·notebook 검사 도구
├── week01/                          # 신규 1주차 강의·TRACE/01 실습·복습 기록
└── AS-IS 2025 2nd semester/
    ├── 00_AS-IS_핵심_커리큘럼.md
    ├── 01_AS-IS_주차별_통합_강의안.md
    ├── 02_AS-IS_주차별_강의_디자인_콘티.md
    ├── 03_AS-IS_슬라이드_텍스트_원문.md
    ├── 04_AS-IS_원본_자료_인벤토리.md
    └── practice/
```

## 실습 코드

실습 원본은 2025년 2학기 공개 실습 저장소의 `main@554898da07d58b191066a94f37f0a9502138fe94` 스냅샷을 `AS-IS` 보존본으로 가져왔다.

- notebook 16개
- 원본 Git blob 78/78 일치
- 모든 notebook이 nbformat 4 JSON으로 유효
- 저장된 오류 output 3건은 AS-IS 상태로 유지
- OpenAI, Langfuse, Pinecone, 학습/서버 실행은 자동 수행하지 않음

자세한 실행 위치와 의존성은 [practice README](AS-IS%202025%202nd%20semester/practice/README.md)를 따른다.

## 2026 운영 환경

- canonical interpreter: CPython 3.11.14 (`>=3.11,<3.12`)
- 기본 설치: `uv pip install -r requirements.txt`
- macOS arm64 완전 고정 설치: `uv pip install -r requirements/locks/course-base-py311-macos-arm64.txt`
- 검색 증강 생성(Retrieval-Augmented Generation, RAG)·미세조정·에이전트·관찰 가능성: [주차별 profile 안내](requirements/README.md)
- 검증 결과: [Week 01 QA 보고서](week01/TEST_REPORT.md)

## 큰 원본 파일

로컬 PPTX/PDF는 약 882 MiB이며 15주차 PPTX는 GitHub의 일반 100 MiB 파일 한도를 넘는다. Git LFS를 구성하기 전에는 Git 추적에서 제외한다.

- [2025년 2학기 AS-IS 원본 강의자료 — Google Drive 보기 전용](https://drive.google.com/drive/folders/1CCnXmqZoDwGPQrr68T41ydbyaxB4wnCF?usp=sharing)
- 파일명, 크기와 SHA-256은 [원본 자료 인벤토리](AS-IS%202025%202nd%20semester/04_AS-IS_원본_자료_인벤토리.md)에서 확인한다.

## 라이선스·개인정보

- 기존 실습 저장소에는 `LICENSE`가 없다. 별도 재배포 권한을 가정하지 않는다.
- 학생 개인 정보가 포함된 Notion 페이지는 수집·복제하지 않았다.
- 실제 응용 프로그래밍 인터페이스(Application Programming Interface, API) 키는 포함하지 않는다.
