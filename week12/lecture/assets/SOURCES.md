# 12주차 자료·이미지 출처

작성·열람: 2026-11-14. 출처에서 확인한 과거 사례와 교수 작성 수업 예시를 구분했습니다. 공개 기업 사례를 현재 내부 플랫폼의 재현이라고 설명하지 않습니다. 장표 하단과 마지막 장표에서 원문으로 이동할 수 있습니다.

| 사용 | 원문 | 반영 |
|---|---|---|
| 15쪽 | [Netflix, 2016 · Experimentation Platform](https://netflixtechblog.com/its-all-a-bout-testing-the-netflix-experimentation-platform-4e1ca458c15) | 사용자 배정과 실제 변경 경험의 구분. 설명용 SVG 재구성 |
| 32–35쪽 | [Microsoft Research, 2020 · Diagnosing SRM](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/) | MSN 카드 변경 사례, 참여가 많은 사용자의 필터링 오류, SRM 원인 분류 |
| 9·20쪽 | [Microsoft · Pre-experiment Stage](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-pre-experiment-stage/) | 결과 확인 전 가설·지표·판정 기준 설계 |
| 45쪽 | [Dmitriev et al., KDD 2017 · Metric Interpretation Pitfalls](https://www.microsoft.com/en-us/research/wp-content/uploads/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf) | 지표·세그먼트 해석의 주의점 |
| 40쪽 | [Newcombe, 1998 · Interval Estimation for the Difference Between Independent Proportions](https://pubmed.ncbi.nlm.nih.gov/9595617/) | 두 독립 비율의 Newcombe–Wilson 95% 구간, 연속성 보정 없이 구현 |
| 43–44쪽 | [Johari et al. · Always Valid Inference](https://arxiv.org/abs/1512.04922) | 반복 확인과 순차 추론의 구분. 장표 막대 수치는 논문 실험이 아닌 코드의 귀무가설 시뮬레이션 |
| 57쪽 | [Kaufman, Pitchforth, Vermeer, 2017 · Booking.com](https://arxiv.org/abs/1710.08217) | 실패 결과 재사용·신뢰할 수 있는 실험 기반. 설명용 SVG 재구성 |
| 53쪽·실습 05 | [Ollama Chat API](https://docs.ollama.com/api/chat) | 실제 로컬 모델 호출·종료 이유·출력 토큰 |

## 포함된 외부 이미지

- `msn-srm.png`: [Microsoft 원본 이미지](https://www.microsoft.com/en-us/research/wp-content/uploads/2020/09/MSN_Car_SRM.png). MSN 카드 이미지 비교. 원문 맥락과 함께 제한적인 교육 설명에 사용.
- `srm-taxonomy.png`: [Microsoft 원본 도식](https://www.microsoft.com/en-us/research/wp-content/uploads/2020/09/SRM_Taxonomy-5f5faf80c8bd2.png). 34쪽은 상위 원인 범주를 읽는 용도이며 세부 문장은 웹의 그림 확대·원문 링크로 확인.
- 이미지의 저작권은 원 권리자에게 있습니다. 저장소 자체 코드의 라이선스가 이 이미지에 재부여되는 것은 아닙니다. 원본 파일은 보존하며 강의 화면에서는 CSS 흑백 필터를 사용합니다.

## 직접 만든 자료

- 나머지 아키텍처·흐름도·지표 그래프: `scripts/week12_content.py`의 SVG/HTML. 기업 사례의 개념도는 수업용 재구성이라고 표기했습니다.
- `lab-*.png`: 2026-11-14 실제 로컬 FastAPI 서비스·합성 분석 보고서의 브라우저 캡처. 실습용 `u-` ID만 사용했습니다.
- `week12/lab/data/*.csv`: 교수 작성 합성 데이터, 시드 12. 실제 고객 기록이나 LLM 출력에서 얻은 제품 성과가 아닙니다.
- `week12/lab/sample/ollama-responses.json`: 실제 `qwen2.5:1.5b-instruct` 로컬 응답. B의 `done_reason=length`를 포함해 성공하지 않은 출력도 원문으로 보존했습니다. 단일 실행의 지연을 모델 성능 벤치마크로 사용하지 않습니다.
- 폰트: Pretendard, 함께 보존한 `FONT-LICENSE.txt` 파일 적용.

## 디자인 참고

[Impeccable](https://github.com/pbakaus/impeccable), [Hallmark](https://github.com/Nutlope/hallmark)의 정보 위계·절제된 강조·반응형 원칙을 참고한 기존 11주차 디자인과 발표자 기능을 이어받았습니다. 이 자료를 해당 프로젝트의 자동 디자인 감사를 통과한 결과라고 주장하지 않습니다.
