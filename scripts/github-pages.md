# GitHub Pages 배포

- 저장소: `smilesjcha/llmops-16week` (Public)
- 게시 방식: Deploy from a branch → `main` → `/ (root)`
- `.nojekyll`: 기존 HTML·CSS·JavaScript를 정적 파일 그대로 게시
- 사이트 루트: 11주차 강의안으로 이동

## 학생 공유 주소

- [11주차 HTML 강의안](https://smilesjcha.github.io/llmops-16week/week11/lecture/)
- [11주차 실습 평가 보고서](https://smilesjcha.github.io/llmops-16week/week11/lab/sample/report.html)
- [11주차 실제 Ollama 실행 보고서](https://smilesjcha.github.io/llmops-16week/week11/lab/sample/ollama/ollama-report.html)
- [11주차 PDF](https://smilesjcha.github.io/llmops-16week/output/pdf/11_week11_offline_evaluation.pdf)
- [실습 코드·VS Code 안내](https://github.com/smilesjcha/llmops-16week/tree/main/week11/lab)
- [Notebook 01–10 실행 순서·확인 결과](https://github.com/smilesjcha/llmops-16week/blob/main/week11/lab/WALKTHROUGH.md)

- [Langfuse 실제 A/B/C 비교 결과](https://smilesjcha.github.io/llmops-16week/week11/lab/sample/langfuse/)
- [09·10번 Docker 준비·100분 시간표](https://github.com/smilesjcha/llmops-16week/blob/main/week11/lab/langfuse/README.md)

## 수정본 반영

생성 원본 `scripts/week11_refinement.py`와 `week11/lecture/deck.css`, `deck.js`를 수정하고 `python scripts/build_week11_html.py`로 강의안 HTML을 생성합니다. `node scripts/verify_week11_browser.mjs`는 화면과 조작을 검사하고 PDF를 갱신합니다. 생성물까지 `main`에 push하면 GitHub가 다시 배포합니다. 저장소 Actions의 **pages build and deployment**가 성공한 뒤 학생용 주소를 확인합니다. 보고서는 `week11/lab/sample/`에 반영한 공개 합성 수업 예제만 공유합니다. 학생의 로컬 결과 `week11/lab/reports/`는 Git 제외 상태를 유지합니다.

배포 범위는 공개 저장소의 커밋된 파일입니다. 로컬 `.venv`·환경변수 파일·개인정보·학생 제출물을 커밋하지 않습니다.

설정 확인과 최신 배포 상태:

```sh
gh api repos/smilesjcha/llmops-16week/pages
gh api repos/smilesjcha/llmops-16week/pages/builds/latest
```

인증 없는 새 Chrome 세션에서 HTTP 상태, 원본 파일 일치, 슬라이드 이동·지표 조작·이미지 확대, 보고서 필터·상세 조회를 확인합니다.

공식 문서: [브랜치 기반 게시 설정](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

- 화면별 시연 안내: https://smilesjcha.github.io/llmops-16week/week11/lab/demo/
