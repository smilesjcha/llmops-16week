# 7주차 확장 강의안 · 출처와 수치 해석

확인일: 2026-10-17. 80쪽 강의안의 외부 도식은 원 논문과 공식 문서를 사용한다. 출처 URL은 해당 장표의 발표자 노트에도 기록한다.

## 외부 도식

| 도식 | 원출처 | 발췌·이용 안내 |
|---|---|---|
| SFT 토큰 예측 | [Hugging Face TRL](https://huggingface.co/docs/trl/sft_trainer) | 6주차 원본 PNG 재사용, PPT의 기본 흑백 표시 효과 |
| LoRA Figure 1 | [Hu et al., 2021](https://arxiv.org/abs/2106.09685) | 6주차의 Figure 발췌 재사용, 교육용 인용 |
| QLoRA Figure 1 | [Dettmers et al., 2023](https://arxiv.org/abs/2305.14314) | 6주차 발췌 재사용, CC BY 4.0, 흑백 변환 명시 |
| DPO Figure 1 | [Rafailov et al., v3 p.2](https://arxiv.org/abs/2305.18290v3) | `dpo-paper-figure1.png`, Figure 영역만 300 dpi 흑백 발췌, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

DPO 원본은 [논문 PDF](https://arxiv.org/pdf/2305.18290v3)이며 보상 모델·강화학습 경로와 DPO 경로의 비교에 사용한다. 한국어 설명과 수치 예시는 원본 Figure와 구분한다. 도식 면적이나 단순한 단계 수를 실측 비용 비율로 해석하지 않는다.

6주차 이미지의 원본 URL·개별 이용 범위는 [6주차 출처 안내](../../../week06/lecture/assets/SOURCES.md)를 참조한다. TRL 코드 라이선스를 별도 이미지 전체의 포괄적 재사용 허가로 간주하지 않는다.

## 계산과 자체 도식

- DPO의 기본 수식·정의: [원 논문](https://arxiv.org/abs/2305.18290), [TRL DPO Trainer](https://huggingface.co/docs/trl/dpo_trainer). 설치·하드웨어 호환성은 공통 고정 환경과 별도로 확인한다.
- 선호쌍·policy/reference 비교는 위 원리에 기반한 편집 가능한 수업 도식이다. 숫자 −2·−5·−3·−3은 가상의 시퀀스 로그확률이며 Judge 점수가 아니다.
- 새 β·단일 정책·합성 평가 차트는 `05_dpo_evaluation_workshop.ipynb`의 `output/validation/week07-workshop/workshop-report.json`을 사용한다. 단일 정책은 질문 하나·고정 답변 두 개이며 실제 언어 모델을 학습하지 않는다.
- 평가 fixture는 `course_labs/preference_evaluation.py`에 직접 작성한 12건의 플래그 조합이다. 사람 평가·모델 출력·학생 성적이 아니다. candidate 4, baseline 4, tie 3, review 1이라는 규칙 결과를 실제 모델 승률로 해석하지 않는다.
- 후보의 형식 플래그 9→11건과 근거 플래그 10→9건은 차원별 회귀를 설명하기 위한 합성 입력이다. 배포 결정을 내리려면 실제 보류 입력·응답 원문·운영 비용의 검증이 추가로 필요하다.
- 원시 로그확률은 답변 토큰의 자연로그 합으로 계산한다. 단순 길이 평균이나 Judge 점수를 기본 DPO 수식에 섞지 않는다. β는 같은 margin의 수식 효과와 실제 학습 설정의 역할을 구분한다.

기획서의 목표·예시 요구사항은 제안값이며 실제 성과가 아니다. 학생·고객 원문, 명단·메일·연락처는 포함하지 않는다.
