# 모델 적응과 서비스 기획

## 1. 모델 적응과
서비스 기획

WEEK 07 · 2026.10.16 · 온라인 실시간

선호 기준과 비교 평가 · 프로젝트 초안 0.1

차성재 · 무신사 Core AI PM × AI 대학원 겸임교수

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 2. 이번 주의 학습 목표

선택 · 오류 유형과 기술 대안의 연결

실험 · 선호 손실·reference·평가 집계 확인

기획 · 실행 근거와 요구사항·위험의 연결

강의 포인트: 6주차의 SFT·LoRA 원리를 실제 선택과 검증 계획으로 연결

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 3. 16주 로드맵 · 7주차



근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 4. 6–8주차 운영

주차 · 진행

06 · 10.09 · 한글날 · 수업·녹화영상·신규 과제 없음

07 · 10.16 · 실시간 온라인 · 초안 0.1·교수 피드백

08 · 10.23 · 시험·실시간 수업 없이 제출물 평가

강의 포인트: 수정본 0.2 마감: 10.22(목) 23:59 한국시간 · 6주차 내용은 7주차에 통합

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 5. 100분 수업 구성

시간 · 내용

00–10분 · 실패 유형·기술 선택

10–25분 · 학습 자료·분할·모델 적응 복습

25–45분 · 선호 기준·DPO·비교 평가

45–50분 · 휴식·커널 확인

50–80분 · Notebook 핵심 실험

80–100분 · 프로젝트 초안·설계 리뷰

강의 포인트: 전체 셀은 복습에서 확장 · 핵심 셀과 장표 연결은 63쪽

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 6. 정답과 선호의 차이

사실에 맞는 답변과 사용자가 원하는 답변

근거·형식·유용성을 나누어 보는 이유

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 7. 지식 오류와 행동 오류

지식·근거 오류 · 최신 문서 누락·잘못된 인용 · 검색·버전·접근 권한 점검

반복 행동 오류 · 출력 형식·설명 방식 불안정 · 프롬프트·검사·학습 후보 비교

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 8. 같은 근거와 다른 답변

근거가 같아도 설명 방식과 보류 기준은 달라짐

짧은 단정과 자세한 설명 모두 틀릴 수 있음

선택 이유를 명시한 뒤 개선할 행동을 정의

강의 포인트: 합성 문의 예시 · 사실 검토와 상대 선호를 구분

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 9. 오류 유형과 첫 비교 대상

문제 · 첫 비교 대상 · 추가 근거

최신 문서 누락 · 검색·문서 관리 · 버전·권한

JSON 형식 위반 · 프롬프트·출력 검사 · 같은 입력의 반복 실패

행동·형식의 반복 오류 · SFT·LoRA · 허가된 자료·보류 평가

답변 선호 불일치 · 기준·선호 최적화 · 선택 이유·라벨 편향

강의 포인트: JSON: JavaScript Object Notation · 데이터 교환 형식

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 10. 기술 선택의 검증 순서

오류 수집 · 입력·원문

기준선 · 최소 변경

후보 비교 · 같은 조건

채택 판단 · 품질·비용·복구

강의 포인트: 기술 이름보다 고칠 실패와 확인할 실험을 먼저 기록

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 11. 6주차 원리와 적용 조건

SFT · Supervised Fine-Tuning · 지도 미세조정

배경·수식·메모리는 6주차 76쪽 자료와 함께 복습

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 12. SFT의 예측과 업무 품질

예측 · 다음 토큰을 예측

손실 · 기대 답변과 차이 계산

검증 · 새 업무 입력에서 평가

강의 포인트: Hugging Face TRL 공식 도식 · 흑백 표시

logits는 확률 변환 전 점수다. 토큰 손실 감소와 새 사건에서의 업무 품질을 구분한다. 자세한 shift·마스킹 계산은 6주차 18–26쪽을 참고한다.

근거: https://huggingface.co/docs/trl/sft_trainer

## 13. 학습 자료의 준비

수집·허가 · 사용 범위

형식 검사 · 필드·출력

사건 분할 · 관련 표현 묶음

보류 평가 · 새 사건 검토

강의 포인트: 자동 형식 검사는 내용의 신뢰성과 사용 허가를 대신하지 않음

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 14. 자료 검사의 네 항목

검사 · 대상 · 실패 예시

필드 · 입력·답변·사건 ID · 빈 instruction

출력 · 구문·필수 키 · 잘못된 JSON

중복 · ID·내용·동일 사건 · 표현만 바꾼 복사

권한 · 사용·보존·삭제 · 고객 원문 무단 사용

강의 포인트: 수업 실습은 합성 자료 48건 · 실제 고객·학생 원문 미사용

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 15. 사건 단위 분할과 누출

문장별 · 사건 A 표현 1 · train 배치 · 표현 2는 test

사건별 · 사건 A의 모든 표현 · 같은 분할 · 사건 B로 평가

강의 포인트: train: 학습용 · test: 보류 평가용 · 같은 정보의 표현만 달라지는 누출 점검

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 16. 자료 오류와 누출의 확인

data = examples()

splits = split_groups(data, seed=42)

assert not leakage(splits)

splits["test"].append(splits["train"][0])

assert leakage(splits)

강의 포인트: Notebook 01 · 자료 추가 이후에도 누출 검사 반복

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 17. 분할 결과와 검사 범위

분할 · 사건 수 · 문장 수

train · 학습 · 16 · 32

dev · 설정 선택 · 4 · 8

test · 최종 보류 · 4 · 8

강의 포인트: 24사건 × 2표현 · seed=42 · 같은 분할 유지와 일반화 입증은 별개

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 18. LoRA의 고정 경로와 학습 경로

W · 기존 고정 가중치

A·B · 학습할 두 작은 행렬

차원 예시 · A: 2×8 · B: 12×2

강의 포인트: LoRA: Low-Rank Adaptation · Hu et al., Figure 1 · 흑백 발췌

원 논문 초기화 A 무작위/B=0과 이번 SVD 근사는 다른 계산이다. 12×8 차원은 수업용 예시이며 논문 실험 크기가 아니다.

근거: https://arxiv.org/abs/2106.09685, repo:course_labs/adaptation.py

## 19. rank별 파라미터와 비용



강의 포인트: 12×8 행렬 · 전체 96개와 r(12+8)개 · 실제 모델 메모리 실측 아님

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 20. 전체 미세조정·LoRA·QLoRA

전체 미세조정 · 모델 가중치까지 갱신

LoRA · 고정 Base와 Adapter

QLoRA · 4-bit 고정 Base와 Adapter

강의 포인트: QLoRA: Quantized Low-Rank Adaptation · Figure 1 · CC BY 4.0 · 흑백 발췌

도식 면적을 실측 메모리 비율로 해석하지 않는다. 저장 정밀도와 계산 정밀도, 고정 모델을 통과하는 gradient와 가중치 갱신을 구분한다.

근거: https://arxiv.org/abs/2305.14314, https://arxiv.org/abs/2106.09685

## 21. 학습 목적과 갱신 방법

구분 · 선택하는 내용 · 예시

학습 목적 · 어떤 신호로 학습할 것인가 · SFT·DPO

갱신 방법 · 어떤 파라미터를 바꿀 것인가 · 전체·LoRA

저장·자원 · 어떤 정밀도와 환경인가 · QLoRA·batch

강의 포인트: SFT·DPO에 LoRA를 결합할 수 있음 · 한 축의 선택을 다른 축의 대안으로 혼동하지 않음

근거: https://huggingface.co/docs/trl/sft_trainer, https://arxiv.org/abs/2106.09685, https://arxiv.org/abs/2305.14314, https://arxiv.org/abs/2305.18290

## 22. 수치 실험과 실제 모델 학습

이번 공통 실습 · 자료 누출·행렬 근사·선호 손실 · GPU·모델·API 키 없이 실행

실제 모델 검증 · 허가 자료·GPU·커널·버전 필요 · 동일 보류 입력의 품질·비용 측정

강의 포인트: SVD: Singular Value Decomposition · 특이값 분해 · 실제 LoRA 학습과 구분

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 23. 선호 데이터의 설계

같은 질문의 두 답변과 선택 이유

사용자에게 유용한 행동을 구체적인 기준으로 표현

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 24. 근거 없는 문의의 세 답변

A: 무조건 승인됩니다.

B: 확인할 근거가 없어 담당자 검토가 필요합니다.

C: 요청을 처리할 수 없습니다.

강의 포인트: 합성 예시 · B는 근거·다음 행동, C는 과도한 거절 여부를 검토

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 25. 선호쌍의 구성



강의 포인트: 같은 prompt 아래 두 답변 비교 · chosen은 명시한 기준에서 선택한 답변

prompt는 근거 문서가 없는 문의다. chosen은 사실의 절대 정답이라는 뜻이 아니다. 이 예시의 선택 기준은 근거 없는 단정 방지와 다음 행동 안내다.

근거: https://arxiv.org/abs/2305.18290, https://huggingface.co/docs/trl/dpo_trainer

## 26. 기대 답변과 상대 선호

SFT · 입력과 기대 답변 · 원하는 출력을 직접 제시

DPO · 질문과 두 답변의 선택 · 원하는 상대적 응답 행동 표현

강의 포인트: DPO: Direct Preference Optimization · 직접 선호 최적화

근거: https://huggingface.co/docs/trl/sft_trainer, https://arxiv.org/abs/2305.18290

## 27. 선호 데이터 한 건

prompt: 근거 문서가 없는 문의
chosen: 담당자 검토가 필요합니다.
rejected: 무조건 승인됩니다.
reason: 근거 없는 단정 방지

학습 입력과 검토 기록

같은 질문·같은 제공 문맥

reason은 라벨 검토용 기록

강의 포인트: prompt·chosen·rejected가 기본 형식 · reason을 모델 입력에 자동 포함하지 않음

근거: https://huggingface.co/docs/trl/dpo_trainer, repo:course_labs/adaptation.py

## 28. 무효 선호쌍의 탐지

invalid = [dict(prefs[0], chosen="같은 답변",

                rejected="같은 답변")]

issues = preference_audit(invalid)

assert any(x["kind"] == "identical_pair" for x in issues)

강의 포인트: Notebook 03 · 동일 답변과 필수 항목 누락 검사

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 29. 선택 기준의 구체화

차원 · 확인할 기준 · 남길 근거

근거 · 제공 문서와 주장 일치 · 원문 위치

유용성 · 다음 행동에 도움 · 구체적 안내

형식 · 필수 키·출력 계약 · 검사 결과

거절 · 필요한 보류와 과도한 거절 구분 · 선택 이유

강의 포인트: 좋아 보인다·더 자연스럽다 대신 비교 가능한 판단 기준 기록

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 30. 평가자 의견 불일치

기록 · 서로 다른 선택과 이유를 모두 보존

분리 · 근거 부족과 문체 선호를 구분

재검토 · 기준 수정·판단 보류·추가 라벨

강의 포인트: 불일치를 숨기거나 무조건 다수결로 정답화하지 않음

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 31. 길이와 답변 품질

길이가 긴 답변 · 상세해 보여 선택될 수 있음 · 근거 없는 내용도 길어질 수 있음

기준에 맞는 답변 · 필요한 내용과 근거 충족 · 길이와 별개로 유용성·거절 검토

강의 포인트: 문자 길이 차이는 검토 신호 · 자동 삭제나 정답 기준으로 사용하지 않음

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 32. 답변 순서와 평가자 가림

응답 수집 · 동일 입력

순서 배치 · A·B 위치 변경

기준 검토 · 모델명 가림

결과 복원 · 대응표로 집계

강의 포인트: 가림과 순서 변경은 편향을 줄이기 위한 절차 · 제거를 보장하지 않음

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 33. 선호 자료의 분할·보존

항목 · 확인할 내용

분할 · 같은 질문·사건의 쌍을 같은 분할에

기록 · 선택 이유·기준 버전·검토 이력

보류 평가 · 학습·기준 수정에 쓰지 않은 입력

권한 · 원문 사용 범위·삭제·보존 정책

강의 포인트: 평가 입력을 보고 라벨 기준과 설정을 반복 수정하면 독립성이 약해짐

근거: https://arxiv.org/abs/2305.18290, https://huggingface.co/docs/trl/dpo_trainer, repo:course_labs/adaptation.py

## 34. DPO의 계산과 학습

reference 대비 답변 선호의 변화

시퀀스 확률에서 손실과 갱신까지

근거: https://arxiv.org/abs/2305.18290, https://huggingface.co/docs/trl/dpo_trainer

## 35. 보상 모델 경로와 DPO 경로

RLHF 경로 · 보상 모델과 강화학습 단계

DPO 경로 · 선호 자료로 정책 직접 최적화

남는 작업 · 자료·편향·실제 업무 평가

강의 포인트: Rafailov et al., Figure 1, v3 p.2 · CC BY 4.0 · 흑백 발췌

원 논문의 RLHF 파이프라인과 DPO 대조다. DPO는 명시적인 보상 모델을 별도로 학습하지 않지만 비용이 0이거나 모든 업무에서 더 좋다는 뜻은 아니다.

근거: https://arxiv.org/abs/2305.18290

## 36. PPO 기반 RLHF와 DPO

항목 · PPO 기반 RLHF · 기본 DPO

학습 자료 · 선호로 보상 모델 학습 · 고정 선호쌍 사용

정책 갱신 · 샘플링·보상으로 최적화 · 상대 로그확률 손실

추가 관리 · 보상·정책·reference · policy·reference·라벨

강의 포인트: PPO: Proximal Policy Optimization · RLHF: Reinforcement Learning from Human Feedback

PPO는 근접 정책 최적화, RLHF는 인간 피드백 기반 강화학습이다. 다양한 변형이 있으므로 여기서는 원 논문의 기본 경로만 비교한다.

근거: https://arxiv.org/abs/2305.18290

## 37. Policy와 Reference의 비교



강의 포인트: policy: 학습 대상 · reference: 고정 비교 정책 · 같은 입력과 두 답변 사용

보통 SFT 모델에서 policy와 reference를 시작한다. reference의 가중치는 갱신하지 않는다. 구현에 따라 reference log probability를 사전 계산할 수 있으며 같은 토큰화·정의가 필요하다.

근거: https://arxiv.org/abs/2305.18290, repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 38. 시퀀스 로그확률

log P(답변 | 질문) = 토큰별 log p의 합

질문을 조건으로 답변 토큰의 확률을 누적

자연로그 · 확률 대신 음수 로그값 사용

강의 포인트: Judge 평가점수·문자 길이·단순 평균 점수를 수식에 넣지 않음

근거: https://arxiv.org/abs/2305.18290, repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 39. 토큰 확률의 작은 계산

항목 · 값 · 해석

조건부 확률 · 0.8, 0.5, 0.2 · 가상 답변 토큰 3개

시퀀스 확률 · 0.08 · 세 조건부 확률의 곱

로그확률 · −2.5257 · 세 자연로그의 합

강의 포인트: 실제 모델 실행값이 아닌 수식 확인 예시 · 답변 토큰만 계산

근거: repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb, repo:course_labs/preference_evaluation.py

## 40. 네 로그확률의 입력

모델 · chosen · rejected

policy · 학습 대상 · −2 · −5

reference · 고정 · −3 · −3

강의 포인트: 다른 답변 시퀀스도 존재할 수 있는 가상 로그확률 · Judge 점수 아님

근거: https://arxiv.org/abs/2305.18290, repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 41. Reference 대비 선호 Margin

m = (−2 − (−5)) − (−3 − (−3)) = 3

policy의 선호 차이에서 reference 차이를 차감

m이 커질수록 reference 대비 chosen의 상대 선호 증가

강의 포인트: Margin: 두 모델의 답변 선호 차이를 다시 비교한 값

근거: https://arxiv.org/abs/2305.18290, repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 42. DPO 손실의 안정적인 계산

policy = (-2., -5.)

reference = (-3., -3.)

loss = dpo_loss(*policy, *reference, beta=.1)

assert np.isclose(loss, np.logaddexp(0, -.1 * 3))

강의 포인트: Notebook 05 · −log sigmoid(βm) = logaddexp(0, −βm)

근거: https://arxiv.org/abs/2305.18290, repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 43. 세 조건의 손실 비교

조건 · margin · 손실 · β=0.1

기준선 · 0 · 0.6931

선호 방향 · 3 · 0.5544

반대 방향 · −3 · 0.8544

강의 포인트: 고정 수식 계산값 · 모델 정확도·평가 성과로 해석하지 않음

근거: repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 44. Margin과 DPO 손실



강의 포인트: β=0.1 · 가상 margin별 손실 · 큰 margin이 해당 선호쌍 손실을 감소

근거: https://arxiv.org/abs/2305.18290, repo:course_labs/adaptation.py

## 45. Beta의 수식 효과와 학습 설정

고정 Margin 실험 · 같은 m에서 β만 바꾼 손실 비교 · 수식 민감도를 관찰

실제 학습 설정 · reference와의 변화 제어에 관련 · 학습률·자료·갱신 횟수와 함께 검증

강의 포인트: β가 크면 항상 더 좋은 답변을 학습한다는 뜻은 아님

근거: https://arxiv.org/abs/2305.18290, https://huggingface.co/docs/trl/dpo_trainer

## 46. Beta별 손실 곡선



강의 포인트: β=0.1·0.5·1.0 · 고정 margin 수치 비교 · 실제 모델 성과·최적 β 추천 아님

근거: repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb, https://arxiv.org/abs/2305.18290

## 47. 질문 하나의 정책 실험

고정 답변 두 개 중 chosen의 선택 확률

θ 한 개와 Bernoulli policy만 갱신

reference는 0.5/0.5로 고정

강의 포인트: 전체 어휘·새 질문·텍스트 생성이 없는 장난감 정책

근거: repo:course_labs/adaptation.py, repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 48. 80회 갱신의 실행 예시

history = toy_preference_training(

    beta=.5, steps=80, lr=.3)

assert history[-1]["loss"] < history[0]["loss"]

print(history[0]); print(history[-1])

강의 포인트: Notebook 03·05 · 동일 β·학습률·갱신 횟수에서 관찰

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 49. 정책 실험의 손실 변화



강의 포인트: 질문 1개·답변 2개 · β=0.5 · lr=0.3 · θ 한 개의 수치 최적화

근거: repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 50. 선택 확률의 변화



강의 포인트: 같은 실험의 chosen 선택 확률 · 새 질문의 정확도·안전성 검증 아님

근거: repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 51. 확인한 결과와 남은 검증

이번 계산의 결과 · 해당 쌍의 손실·선택 확률 변화 · 수식·갱신 구현의 동작 확인

확인하지 못한 결과 · 새 질문의 사실성·유용성·안전성 · 실제 모델 품질·GPU 비용·일반화

강의 포인트: 한 쌍을 더 선호하게 된 결과와 업무 전체의 개선을 분리

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 52. DPO 실험의 재현 정보

항목 · 기록할 내용

자료 · 질문·쌍·선택 이유·분할·해시

모델 · policy·reference·revision·Tokenizer

학습 · β·학습률·길이·batch·step

평가 · 기준 버전·원문·실패·비용

강의 포인트: Tokenizer: 문자와 토큰 ID의 변환기 · 모델·데이터와 함께 버전 관리

근거: https://huggingface.co/docs/trl/dpo_trainer, repo:course_labs/adaptation.py

## 53. 비교 평가와 배포 판단

평균·승률 하나로 놓치는 회귀 오류

실제 입력의 실패 이유와 운영 비용을 함께 검토

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 54. 공정한 비교의 조건

고정 입력 · 문서·템플릿

응답 생성 · 설정·버전

가림 검토 · 같은 평가 기준

실패 기록 · 원문·비용·결정

강의 포인트: 개발용 입력과 최종 보류 입력을 분리 · 최고 사례만 선별하지 않음

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 55. 차원별 평가 기준

차원 · 확인 방법 · 실패 처리

근거 · 주장과 원문 위치 일치 · 근거 부족 시 보류

형식 · JSON 필수 키·구문 · 검사·재시도

유용성 · 다음 행동에 도움 · 안내 수정

거절 · 과도한 거절 여부 · 사유·사람 검토

강의 포인트: 같은 입력·문서·생성 조건에서 평가 · 실제 원문 검토를 플래그 검사로 대체하지 않음

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 56. 합성 평가 Fixture의 실행

fixtures = evaluation_fixtures()

summary = fixture_summary(fixtures)

assert summary["n"] == 12

print(summary["counts"])

강의 포인트: Notebook 05 · Fixture: 검증용 고정 입력 · 실제 모델·사람 평가 결과 아님

근거: repo:course_labs/preference_evaluation.py, repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 57. 12건의 수업용 규칙 집계

판정 · 건수 · 의미

candidate · 4 · 후보에 유리한 플래그

baseline · 4 · 기준선에 유리한 플래그

tie · 3 · 수업용 규칙상 동률

review · 1 · 필수 조건 미충족·검토

강의 포인트: 직접 작성한 0/1 조합과 수업용 규칙 · 실제 모델 승률·학생 성적 아님

근거: repo:course_labs/preference_evaluation.py, repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 58. 형식 개선과 근거 품질의 회귀



강의 포인트: 합성 플래그 12건 · 형식 9→11건, 근거 10→9건 · 실제 모델 품질 측정 아님

근거: repo:course_labs/preference_evaluation.py, repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 59. 회귀 사례의 검토 흐름

분리 · 차원별 결과에서 나빠진 항목 확인

원문 검토 · 동일 입력의 근거·답변을 다시 읽기

판단 · 기준 수정·자료 보완·채택 보류 기록

강의 포인트: 합성 예시의 근거 회귀 ID: SYN-03·SYN-12 · 실제 응답 검토는 별도 필요

근거: repo:course_labs/preference_evaluation.py, repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 60. 배포 후보의 검토 기준

검토 · 필요한 근거

품질 · 사전 합의한 조건과 회귀 사례

비용 · 시간·메모리·오류·처리량

재현 · Base·Adapter·입력·설정 버전

복구 · 이전 조합·중단 조건·담당

강의 포인트: 합성 fixture만으로 배포 승인 불가 · 실제 보류 입력에서 추가 검증

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 61. 정상·보류·실패의 사용자 흐름

정상 · 근거·형식 확인 · 답변과 출처 · 사용자 확인

보류 · 근거 부족·오류 · 사유·다음 행동 · 사람 검토

강의 포인트: 구현 시 과도한 거절·재시도 횟수·복구 경로를 함께 설계

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 62. 단계별 Notebook 실습

Python 3.11 · 기존 .venv · 공통 requirements

선택 핵심 셀부터 실행한 뒤 변수를 바꾸며 확장

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 63. 실습 파일과 장표 연결

파일 · 실행 내용 · 장표

01 · 데이터 · 분할·누출·Dataset Card · 13–17

02 · 행렬 · rank·오차·원본 고정 · 18–22

03 · 선호 · 선호쌍·DPO·단일 정책 · 27–52

04 · 기획 · 요구사항·HTML 초안 · 69, 71–79

05 · 워크숍 · 로그확률·평가 집계 · 38–60

강의 포인트: 전체 노트북은 복습에서 확장 · 100분 수업은 핵심 셀 선택

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 64. VS Code 실행 순서

루트 폴더 · llmops-16week 전체 열기

커널 선택 · Python 3.11 · .venv 환경

순서 실행 · 위에서 아래로 실행 후 한 변수 변경

강의 포인트: 기존 .venv 재생성 불필요 · 설치·Windows 안내는 lab/README.md

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 65. 실습 01 · 자료 누출의 확인

예상 · 같은 사건의
교차 여부

실행 · 문장·사건별
분할 비교

변경 · 누출 자료
추가

기록 · 검사 결과와
분할 기준

강의 포인트: 정상 48건 · train32/dev8/test8 · 완전 중복과 같은 사건의 표현 구분

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 66. 실습 02 · 원본과 근사 오차

result = rank_approximation(delta, 2)

adapted = W + result["update"]

assert np.array_equal(W, W_original)

print(result["factor_params"], result["relative_error"])

강의 포인트: Notebook 02의 W·delta 생성 이후 실행 · SVD 근사이며 LoRA 학습 아님

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 67. 실습 03 · 선호 손실의 변화

예상 · chosen 쪽 상대 로그확률 변화와 손실

실행 · 기준선·선호·반대 방향 비교

변경 · β만 바꾸고 가정과 한계 기록

강의 포인트: 한 질문 정책의 결과를 새 질문의 서비스 성과로 일반화하지 않음

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 68. 실습 05 · 차원별 회귀 검사

b = summary["rates"]["baseline"]

c = summary["rates"]["candidate"]

assert c["format"] > b["format"]

assert c["evidence"] < b["evidence"]

강의 포인트: Notebook 05 · 합성 입력에서 집계 해석 연습 · 실제 품질 평가는 별도

근거: repo:course_labs/preference_evaluation.py, repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb

## 69. 실습 04 · 기획서 HTML 생성

assert proposal_check(doc) == []

html = proposal_html(doc)

path = OUT / "proposal-draft.html"

path.write_text(html, encoding="utf-8")

강의 포인트: Notebook 04의 doc 작성 이후 실행 · 항목 유무 통과와 내용 검토 구분

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 70. 실행 산출물과 다음 확인

산출물 · 확인할 내용

Dataset Card·행렬 보고서 · 자료·분할·오차·수치 실험 범위

선호·워크숍 보고서 · 가정·조건·단일 정책·합성 평가

기획서 HTML·JSON · 문제·범위·평가·권한·복구

피드백 기록 · 현재 버전·질문·수정 이유

강의 포인트: output/validation/ 하위 로컬 출력 · 개인정보·학생 제출 원문 공개 GitHub 금지

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 71. 프로젝트 초안과 설계 리뷰

7주차 초안 0.1과 교수 피드백

8주차 수정본 0.2의 제출물 평가 · 중간고사 없음

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 72. 팀·개인 진행과 제출 일정

구분 · 기준

아주대AI대학원 · 2–4인 자율 팀 · LMS 제출

군산대·국립창원대 등 · 개인 진행 가능 · 공지 교수 이메일

7주차 · 10.16 · 초안 0.1·교수 피드백

마감 · 10.22(목) · 수정본 0.2 · 23:59 한국시간

평가 · 10.23(금) · 시험·실시간 수업 없이 제출물 평가

강의 포인트: 개별 예외는 교수 승인 확인 · 팀 신청 폼과 기획서 제출함은 별개

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 73. 제안서·요구사항·발표 자료

형식 · 독자가 확인할 내용

2Pager · 2쪽 요약 · 문제·제안·근거·검증 요청

PRD · 제품 요구사항 · 기능·완료 조건·실패·권한

로드맵 · 범위·일정·역할·완료 기준

PPT·시안·데모 · 핵심 구조와 실제 동작 범위

강의 포인트: PRD: Product Requirements Document · 같은 내용의 중복 문서 제출 불필요

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 74. 2Pager 첫 문단의 개선

과정 중심 초안 · 여러 AI 도구를 사용해 보았다. · 제작 과정만 있고 사용자·문제가 모호

제안 중심 초안 · 논증 글의 주장·근거 연결 피드백 제안 · 대상·현재 한계·최소 기능·검증을 먼저 제시

강의 포인트: 합성 작성 예시 · 도구 대화와 제작 과정은 필요한 경우 부록으로 이동

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 75. PRD의 요구사항과 검증 연결

요구사항 · 확인 방법 · 실패 처리

FR01 · 근거 위치 표시 · 고정 입력의 인용 위치 검토 · 근거 부족 시 보류

FR02 · 구조화 출력 · JSON 필드·구문 검사 · 재시도 후 검토

FR03 · 수정 제안 선택 · 채택·거절 동작 확인 · 원문 유지·되돌리기

강의 포인트: FR: Functional Requirement · 기능 요구사항 · 목표와 실제 성과 구분

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 76. 글쓰기 개선 서비스의 구조

원문 분리 · 서론·본론·결론

기준별 판단 · 주장·근거·유창성

근거 피드백 · 원문 위치·보류

사용자 수정 · 채택·재검토

강의 포인트: 구조·유창성·이해도는 별도 기준으로 검토 · 학생 성적 자동 결정 제외

서론은 아이디어 제안과 주장, 본론1·본론2는 각 주장과 근거 연결, 결론은 제언과 주장 요약을 각각 검토한다. 구조 검토와 유창성·이해도를 하나의 자동 점수로 섞지 않는다. 원문 인용과 판단 보류, 사용자 직접 수정 경로를 둔다.

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 77. 세 관점의 설계 리뷰

관점 · 질문 · 기획서의 근거

사업·대표 · 현재 대안보다 가치가 있는가 · 대상·문제·검증 계획

사용자 경험 · 실패·보류·수정이 이해되는가 · 흐름·시안·사용 범위

개발·평가 · 권한·비용·복구가 가능한가 · 자료·구현·평가·위험

강의 포인트: UX: User Experience · 사용자 경험 · 프로토타입은 운영 제품 검증과 구분

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 78. 교수 피드백과 수정 기록

feedback = {"version": "0.1", "question": doc["question"],

            "professor_feedback": "미수신",

            "decision": "미결정", "reason": "",

            "next_evidence": ""}

강의 포인트: Notebook 04 · 채택·보류·반박의 이유와 추가 근거를 수정본에 기록

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 79. 제출 전 확인

항목 · 확인

문제·범위 · 사용자·대안·최소 기능·제외 범위

검증·운영 · 보류 입력·기준·실패·권한·복구

문서 형식 · PPT·Word·PDF·HTML 가능 · HWP 제외

일정·경로 · 10.22(목) 23:59 · LMS 또는 공지 이메일

개인정보 · 명단·연락처·학생 제출 원문 공개 금지

강의 포인트: Prototype: 핵심 동작을 확인하는 시안 · 실제 LLM·고정 응답·수동 처리 범위 명시

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 80. 출처와 재현 경로

자료 · 원문·실행 위치

DPO 원 논문 · https://arxiv.org/abs/2305.18290

DPO 공식 문서 · https://huggingface.co/docs/trl/dpo_trainer

실습 Notebook · week07/lab/notebooks · 01–05

SFT·LoRA 배경 · week06 강의안 · 76쪽

강의 포인트: 외부 도식·계산 근거·이용 범위: lecture/assets/SOURCES.md

근거: https://arxiv.org/abs/2305.18290, https://huggingface.co/docs/trl/dpo_trainer, https://huggingface.co/docs/trl/sft_trainer, https://arxiv.org/abs/2106.09685, https://arxiv.org/abs/2305.14314, repo:week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb, repo:course_labs/preference_evaluation.py, repo:course_labs/adaptation.py