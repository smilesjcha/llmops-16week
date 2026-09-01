# AS-IS 2025년 2학기 자료 안내

이 폴더는 `AI융합실전프로젝트10(LLMOps)` 2025년 2학기 강의의 커리큘럼, 강의 콘티, 실제 슬라이드 텍스트, PPTX/PDF 원본 인벤토리, 실습 코드를 한곳에 보존한다.

## 먼저 읽을 문서

1. [핵심 커리큘럼](00_AS-IS_핵심_커리큘럼.md)
2. [주차별 통합 강의안](01_AS-IS_주차별_통합_강의안.md)
3. [주차별 강의 디자인 콘티](02_AS-IS_주차별_강의_디자인_콘티.md)
4. [슬라이드 텍스트 원문](03_AS-IS_슬라이드_텍스트_원문.md)
5. [PPTX/PDF 원본 자료 인벤토리](04_AS-IS_원본_자료_인벤토리.md)
6. [기존 실습 코드 안내](practice/README.md)
7. [실습 코드 출처·무결성](practice/SOURCE.md)

## 자료 범위

- 공개 Notion: 커리큘럼과 01–14주차 중 공개된 주차별·하위 콘티
- PPTX/PDF: 01–07, 09–15주차 14쌍, 총 1,002장
- notebook: 01–07, 09–14주차 16개
- 08주차: 중간고사. 별도 PPTX/PDF·notebook 없음
- 15주차: Capstone PPTX/PDF는 있으나 별도 Notion 주차 페이지와 notebook은 없음
- 16주차: 기말고사·팀별 프로젝트 결과 발표. 별도 PPTX/PDF·notebook 없음

## 폴더 구조

```text
AS-IS 2025 2nd semester/
├── 00_AS-IS_핵심_커리큘럼.md
├── 01_AS-IS_주차별_통합_강의안.md
├── 02_AS-IS_주차별_강의_디자인_콘티.md
├── 03_AS-IS_슬라이드_텍스트_원문.md
├── 04_AS-IS_원본_자료_인벤토리.md
├── [AI_PR_PR_10] ... .pptx/.pdf
└── practice/
    ├── README.md
    ├── SOURCE.md
    ├── week01/ ... week14/
    └── 실행 환경 파일
```

## 출처

- [공개 Notion 메인](https://synonymous-faucet-52e.notion.site/AI-10-LLMOps-260a18c366b180deb569f134e48e7bff)
- [Notion 주차별 커리큘럼](https://synonymous-faucet-52e.notion.site/260a18c366b180d78d81d435d43a8043)
- [기존 실습 저장소](https://github.com/smilesjcha/ajou-llmops-2025-2nd-semester), `main@554898da07d58b191066a94f37f0a9502138fe94`

## 보존 원칙

- 실제 PPTX/PDF를 AS-IS 판정의 1차 기준으로 삼는다.
- Notion에 여러 초안이 있으면 문서에 선택 우선순위를 명시하고 대안 이력을 삭제하지 않는다.
- notebook의 기존 output, adapter, checkpoint, log를 원본 그대로 보존한다.
- 외부 API·Pinecone·학습·서버 실행은 비용이나 외부 변경이 가능해 이관 과정에서 실행하지 않는다.
- 학생 이름·학번·이메일이 포함된 프로젝트 관리 페이지와 개인 이력서 리뷰는 이관하지 않는다.
- 실제 secret은 없으며 `.env.sample`만 보존한다.

## GitHub 업로드 주의

PPTX/PDF 원본은 약 882 MiB이고 15주차 PPTX 하나가 100 MiB를 넘는다. 현재는 로컬에 보존하되 루트 `.gitignore`로 제외한다. 원본을 GitHub에도 올리려면 Git LFS와 자료 배포 권한을 먼저 구성해야 한다. MD와 `practice/`는 일반 Git으로 관리할 수 있다.

원본 실습 저장소에는 `LICENSE`가 없다. 따라서 이 폴더의 소스 보존은 별도 재배포 라이선스를 부여하지 않는다.
