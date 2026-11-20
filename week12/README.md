# 12주차 · 온라인 실험과 A/B 테스트

사용자 배정 → API·이벤트 → 데이터 검증 → 효과·위험 분석 → 배포 판단을 연결하는 **100분 수업**입니다. 웹 강의안과 학생용 PDF는 같은 64장입니다.

| 자료 | 바로 보기 |
|---|---|
| HTML 강의안 · 발표자 모드 | [강의안 열기](https://smilesjcha.github.io/llmops-16week/week12/lecture/) |
| 학생용 PDF · 64쪽 | [PDF 열기·저장](https://smilesjcha.github.io/llmops-16week/output/pdf/12_week12_online_experiments.pdf) |
| 실습 Notebook 5개 | [VS Code 준비·실행 순서](lab/README.md) · [셀별 확인 결과](lab/WALKTHROUGH.md) |
| 실습 분석 보고서 | [세 가지 결과 비교](https://smilesjcha.github.io/llmops-16week/week12/lab/sample/report.html) |
| **9–12주차 통합 과제** | **[공개 과제 안내·작성 양식](https://smilesjcha.github.io/llmops-16week/week12/assignment/)** |
| 교수용 설명 노트 | [64쪽 핵심 메시지·코드 셀별 안내](https://smilesjcha.github.io/llmops-16week/week12/lecture/instructor/) |

과제는 **Langfuse 상담 AI 개선 미션**입니다. [전용 Notebook 1개](https://github.com/smilesjcha/llmops-16week/blob/main/week12/assignment/01_langfuse_mission.ipynb)에서 질문 2개 × 프롬프트 2개를 실제로 실행하고 Trace·Scores·지연을 비교한 뒤 사용자 A/B 계획을 작성합니다. 설치 후 60–90분, **판단 메모 1–2쪽 PDF/HTML + 화면 2장**을 제출합니다. **2026년 12월 4일(금) 23:59 KST**, 아주대AI대학원은 LMS에 **최대 5회** 제출 가능하며 마지막 제출물을 평가합니다. 그 외 수강생은 같은 기한까지 공지된 교수 이메일로 개인 제출합니다. [실행·평가 기준](https://github.com/smilesjcha/llmops-16week/blob/main/week12/assignment/README.md)

## 10·11·12주차의 구분

10주차는 요청·장애·복구, 11주차는 같은 질문의 답변 품질, 12주차는 무작위 배정 사용자의 결과를 다룹니다. **11주차 A/B/C 평가와 12주차 사용자 A/B 실험은 다른 비교입니다.** [장표별 중복 점검·개선 내용](lecture/WEEKS_10_12_COMPARISON.md) · [38개 코드 셀별 실행·교수 설명](lab/WALKTHROUGH.md)

## 수업 흐름

| 구간 | 장표 | 활동 |
|---|---|---|
| 0–15분 | 1–21 발췌 | 가설·배정·지표 → 01번 핵심 8분 |
| 15–35분 | 22–30 | 배정·실제 제공·피드백 연결 → 02번 12분 |
| 35–50분 | 31–38 | 누락·SRM·분모 → 03번 9분 |
| 50–75분 | 39–51 | 차이·신뢰구간·운영 기준 → 04번 핵심 12분 |
| 75–90분 | 52–58 | 실험 적용 범위·측정 조건·실제 출력 구분 → 05번 발췌 6분 |
| 90–100분 | 59–64 | 배포 토론·9–12주차 과제 |

04번 표본 계획·반복 확인은 교수 시연/복습으로 활용합니다. 모델 다운로드는 수업 전에 마칩니다. 64장을 모두 같은 속도로 읽지 않고 코드 결과와 연결해 진행합니다.

## 사례와 근거

- Microsoft MSN: 사용자가 많이 참여한 B에서 필터링 오류로 발생한 표본 비율 불일치(SRM).
- Netflix: 실험에 배정된 사용자와 실제 변경을 경험한 사용자의 차이.
- Booking.com: 성공·실패 결과를 남기는 실험 문화와 분석 신뢰성.
- 수업 서비스: 실제 FastAPI·SQLite·중복 방지·피드백·중단 스위치.
- 실제 모델: `qwen2.5:1.5b-instruct`를 Ollama로 호출한 A/B 원문. B의 출력 잘림도 그대로 보존했습니다.
- 성과 분석: 교수 작성 **합성 사용자 2400명**의 세 가지 시나리오. 실제 고객·제품·모델 성과라고 해석하지 않습니다.

[전체 출처와 이미지 사용 기록](lecture/assets/SOURCES.md) · [검증 범위](VALIDATION.md)
