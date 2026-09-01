# LLMOps 16-Week Course Archive

2025년 2학기 `AI융합실전프로젝트10(LLMOps)`의 기존 자료를 근거 중심으로 정리한 저장소다. 공개 Notion 커리큘럼, 실제 PPTX/PDF, 기존 실습 repository를 대조해 AS-IS 기준 문서와 주차별 실습 코드를 보존한다.

## 현재 구성

- 핵심 16주 커리큘럼
- 01–16주차 통합 강의안(08주차 중간고사, 16주차 팀별 프로젝트 결과 발표 포함)
- 실제 slide range 기반 강의 디자인 storyboard
- 1,002장 슬라이드의 검색용 텍스트 원문
- 기존 notebook 16개와 지원 data/code/artifact
- PPTX/PDF 파일명·크기·SHA-256 인벤토리

## 시작하기

[AS-IS 2025년 2학기 안내](AS-IS%202025%202nd%20semester/README.md)에서 문서와 실습자료를 확인한다.

```text
llmops-16week/
├── README.md
├── scripts/                         # PPTX text·asset manifest 재생성 도구
└── AS-IS 2025 2nd semester/
    ├── 00_AS-IS_핵심_커리큘럼.md
    ├── 01_AS-IS_주차별_통합_강의안.md
    ├── 02_AS-IS_주차별_강의_디자인_콘티.md
    ├── 03_AS-IS_슬라이드_텍스트_원문.md
    ├── 04_AS-IS_원본_자료_인벤토리.md
    └── practice/
```

## 실습 코드

실습 원본은 [smilesjcha/ajou-llmops-2025-2nd-semester](https://github.com/smilesjcha/ajou-llmops-2025-2nd-semester)의 `main@554898da07d58b191066a94f37f0a9502138fe94`에서 가져왔다.

- notebook 16개
- 원본 Git blob 78/78 일치
- 모든 notebook이 nbformat 4 JSON으로 유효
- 저장된 오류 output 3건은 AS-IS 상태로 유지
- OpenAI, Langfuse, Pinecone, 학습/서버 실행은 자동 수행하지 않음

자세한 실행 위치와 의존성은 [practice README](AS-IS%202025%202nd%20semester/practice/README.md)를 따른다.

## 큰 원본 파일

로컬 PPTX/PDF는 약 882 MiB이며 15주차 PPTX는 GitHub의 일반 100 MiB 파일 한도를 넘는다. Git LFS를 구성하기 전에는 Git 추적에서 제외한다. 무결성 정보는 [원본 자료 인벤토리](AS-IS%202025%202nd%20semester/04_AS-IS_원본_자료_인벤토리.md)에 있다.

## 라이선스·개인정보

- 기존 실습 저장소에는 `LICENSE`가 없다. 별도 재배포 권한을 가정하지 않는다.
- 학생 개인 정보가 포함된 Notion 페이지는 수집·복제하지 않았다.
- 실제 API key는 포함하지 않는다.
