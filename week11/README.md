# 11주차: LLM 서비스의 품질 검증

2026년 11월 13일 실시간 온라인 수업. **52쪽 HTML 프레젠테이션**, 인쇄 PDF, 단계별 Notebook 8개로 검색 평가·실제 Ollama 생성·LLM 평가·실행 추적을 다룹니다.

- [HTML 강의안 바로 보기 · 52쪽](https://smilesjcha.github.io/llmops-16week/week11/lecture/): 로그인·다운로드 없이 브라우저에서 열기
- [학생용 PDF / 52쪽](../output/pdf/11_week11_offline_evaluation.pdf)
- [실습 코드와 VS Code 실행 순서](lab/README.md)
- [실습 평가 보고서 바로 보기](https://smilesjcha.github.io/llmops-16week/week11/lab/sample/report.html): 필터·질문 검색·근거 탐색이 가능한 실행 예제
- [실제 Ollama 실행 보고서](https://smilesjcha.github.io/llmops-16week/week11/lab/sample/ollama/ollama-report.html)
- [Notebook별 실행 순서·확인 결과](lab/WALKTHROUGH.md)
- [Langfuse·LangSmith의 역할과 도입 기준](lab/PLATFORMS.md)
- [100분 교수 진행안](lecture/TEACHING_GUIDE.md)
- [장표별 설명 노트](lecture/lecture-notes.md)
- [출처·이미지·라이선스](lecture/assets/SOURCES.md)
- [설계·검수 기준](lecture/DESIGN.md)
- [실행 검증 결과](VALIDATION.md)

위의 **바로 보기** 링크는 GitHub Pages에서 실행됩니다. Chrome·Edge 등에서 바로 열고 주소를 학생들에게 공유하면 됩니다. `main`의 수정본은 Pages 배포가 완료되면 같은 주소에 반영됩니다.

오프라인 이용도 가능합니다. [강의안 원본](lecture/index.html)이나 [보고서 원본](lab/sample/report.html)의 **Download raw file**로 저장한 뒤 브라우저로 여세요. 글꼴·그림·스크립트가 내장된 단일 파일입니다. 공개 보고서는 수업용 합성 자료이며 학생 제출물이 아닙니다. 직접 실행한 결과는 로컬 `week11/lab/reports/report.html`에서 확인합니다.

## 이번 주에 만드는 결과

1. 질문·필수 근거·답변 가능 여부·의도 그룹을 갖춘 평가 데이터
2. 단어/문자 TF-IDF와 문서 버전 필터의 비교
3. Hit·Recall·MRR·nDCG와 기권 정책의 차이
4. 실패 유형·말투별 분석과 질문별 근거 확인
5. 답변 평가 기준, 평가자 불일치와 위치 편향 분석
6. 그룹 bootstrap, 학습용 검증 조건, 재현 가능한 HTML 보고서
7. 실제 로컬 LLM의 프롬프트별 답변·인용·기권 비교
8. 실제 LLM 평가, 요청별 실행 추적과 플랫폼 기능의 연결

공통 실습은 실제 TF-IDF 검색을 실행합니다. **가상 정책 22개·교수 작성 합성 질문 48개**를 사용하며 실제 기업 정책·학생 정보는 포함하지 않습니다. 01–06은 외부 모델 호출 없이 계산 원리를 확인합니다. 07–08은 로컬 Ollama에 실제 요청을 보내 답변 생성과 모델 평가를 실행합니다. 05번의 작성 예시와 08번의 실제 판정을 구분하며, Langfuse·LangSmith 계정으로 데이터는 전송하지 않습니다.

실제 실행에서 후보의 Recall@3는 56.25%에서 81.25%로 높아졌지만, 기권을 반영한 필수 근거 확보율은 56.25%에서 50%로 낮아졌습니다. 답변 불가 수락률도 12.5%로 교육용 기준 10%를 넘어서 **HOLD**입니다. HOLD는 실행 오류가 아니라 평가의 결론입니다. 세 지표의 분모와 범위가 다르므로 한 점수로 합쳐 해석하지 않습니다.

## HTML 프레젠테이션 조작

- 이전/다음 버튼, 방향키, PageUp/PageDown, Home/End
- 페이지 번호 입력과 URL hash로 위치 유지
- 목차로 바로 이동, N으로 설명 노트, O로 목차
- 그림 확대와 Escape로 닫기
- 16쪽에서 검색 개수 k를 바꿔 지표 계산
- 인쇄 / PDF 버튼: 전체 52쪽 출력, 노트·조작 버튼 제외

JS를 꺼도 전체 장표는 문서 순서대로 읽을 수 있습니다. 휴대폰에서는 내용을 세로로 배치하며 차트 수치는 표로 제공합니다. 발표에는 데스크톱 브라우저를 권장합니다.

별도 신규 과제 마감·배점을 이 자료에서 추가하지 않습니다. 수업 활동과 프로젝트 평가 기록으로 활용하고 제출은 소속별 최신 공지를 따릅니다.
