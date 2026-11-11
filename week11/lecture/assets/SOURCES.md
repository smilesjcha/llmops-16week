# 출처와 라이선스

확인일: 2026-11-11. 논문 결과와 수업 실측을 구분합니다.

| 자료 | 원문 / 위치 | 사용 방식 |
|---|---|---|
| ARES framework | https://arxiv.org/html/2311.09476v2 / Figure 1 | 원본 PNG, 회색조 CSS 표시 |
| ARES NQ context relevance | https://arxiv.org/html/2311.09476v2 / Figure 2 | 원본 성능 그래프. 평가 프롬프트가 아님 |
| Ragas | https://arxiv.org/html/2309.15217v2 | 평가 차원의 개념 요약 |
| Lost in the Middle | https://arxiv.org/abs/2307.03172 | 위치 조건을 설명한 자체 도식. 성능 곡선 복제 아님 |
| LLM-as-a-Judge | https://arxiv.org/abs/2306.05685 | 위치·장황함 등 편향 설명 |
| TfidfVectorizer | https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html | 고정 1.7 계열 API 설명 |
| nDCG | https://scikit-learn.org/1.7/modules/generated/sklearn.metrics.ndcg_score.html | 독립 계산 교차 검증 |
| Data leakage | https://scikit-learn.org/1.7/common_pitfalls.html#data-leakage | 설정 선택과 평가 분리 |

## 외부 이미지

- ares-framework.png: 원문 Figure1 / 원본 이미지 경로 https://arxiv.org/html/2311.09476v2/Tables/Headline_Figure_V1.png
- ares-context-results.png: 원문 Figure2 / 원본 이미지 경로 https://arxiv.org/html/2311.09476v2/Tables/NQ_ContextRelevance.png
- 저자: Jon Saad-Falcon, Omar Khattab, Christopher Potts, Matei Zaharia.
- 논문 v2 라이선스: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- 원본 파일의 픽셀은 수정하지 않았습니다. HTML과 인쇄 PDF에서 강의 팔레트에 맞춰 CSS grayscale을 적용했습니다. 밝기가 비슷한 범례는 원문과 함께 확인합니다. 저자나 기관의 보증·제휴를 의미하지 않습니다.
- 원본 연구의 평가 환경과 모델에 한정된 그래프이며 현재 최신 모델 순위나 수업 실측이 아닙니다.

## 직접 생성한 시각 자료

- lab-report.png, lab-report-metrics.png, lab-report-filters.png, lab-error-detail.png:
  scripts/capture_week11_lab.mjs가 실제 sample/report.html을 열어 캡처한 화면입니다.
- 슬라이드 차트: sample/results.json 또는 고정 dev의 evaluation.py 실행 결과에서 계산합니다.
- 흐름·구조·분리·문맥 위치 도식: 수업 설명용 자체 제작. 실측 수치인 것처럼 표시하지 않습니다.
- 평가자 혼동 행렬: judging.py의 교수 작성 fixture. 실제 LLM benchmark 아님.

## 글꼴

Pretendard 1.3.9, SIL Open Font License 1.1. 원본:
https://github.com/orioncactus/pretendard
배포된 Regular/Bold WOFF2를 HTML에 내장했습니다. FONT-LICENSE.txt 포함.

## 디자인 하네스

- [Impeccable](https://github.com/pbakaus/impeccable), 참조 commit ebe9c265f416f7f9b83ed424ed5b9bd0d2684536.
- [Hallmark](https://github.com/Nutlope/hallmark), 참조 commit 407fa689f4a276f2fd389208d271d0fef08f5058.

공식 SKILL.md와 craft/quality 지침을 읽고 활용했습니다. 기존 강의의 블랙·화이트·블루, 한 화면의 핵심 메시지, 자료 중심의 구조, 상태·접근성·반응형 검수를 적용했습니다. 웹 마케팅용 섹션 수·CTA·사진 요구는 수업용 페이지와 인쇄에 그대로 적용하지 않았습니다. 하네스 자체를 저장소나 사용자 전역에 설치하지 않았습니다.

## 개정판의 운영 도구·아키텍처 참고

- [Langfuse 관찰·추적](https://langfuse.com/docs/observability/overview): trace, 중첩 observations, 입력·출력·지연 탐색.
- [Langfuse 평가](https://langfuse.com/docs/evaluation/overview): 운영 trace와 오프라인 dataset·experiment의 연결.
- [LangSmith 평가 개념](https://docs.langchain.com/langsmith/evaluation-concepts): dataset example, experiment, evaluator, 운영 피드백.
- [MLflow 평가 구성](https://mlflow.org/docs/latest/genai/eval-monitor/): dataset, predict function, scorers.
- [MLflow 평가 개발 흐름](https://mlflow.org/docs/latest/genai/datasets/end-to-end-workflow/): trace·참고 기준·데이터·실험의 연결.
- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/): trace와 span의 관계.
- [Ollama Chat API](https://docs.ollama.com/api/chat), [구조화 출력](https://docs.ollama.com/capabilities/structured-outputs): 실제 요청·출력 계약·토큰·지연.
- [Qwen2.5 1.5B Instruct](https://ollama.com/library/qwen2.5:1.5b-instruct): 수업 기본 로컬 모델.

확인일: 2026-11-11. 아키텍처·평가 흐름은 위 문서를 바탕으로 작성한 수업용 재구성입니다. 특정 산업의 단일 강제 표준으로 소개하지 않습니다.

### 제품 화면

`langfuse-trace.png`: [공식 문서 원본 이미지](https://langfuse.com/images/docs/tracing-overview.png). Langfuse UI의 기능 설명을 위한 교육용 인용이며 재사용 가능한 별도 공개 라이선스를 주장하지 않습니다. 원본 픽셀은 유지했고 CSS로 회색조·작업 영역 확대를 적용했습니다. 원문 링크를 병기하며 수업 계정 화면이나 자체 성능 측정값으로 소개하지 않습니다.

LangSmith 사례는 공식 문서의 기능 관계를 재구성한 편집 가능한 SVG입니다. 제품 화면을 모사한 그림은 아닙니다.

### 실제 로컬 호출

`week11/lab/sample/ollama/`는 `ollama_lab.py`의 실제 생성·평가 결과입니다. 모델 digest, 프롬프트, 데이터·코드 해시, 원응답, 토큰·지연을 기록합니다. 선택된 합성 시연 사례이므로 미공개 test 벤치마크나 실제 서비스 정확도를 뜻하지 않습니다.
