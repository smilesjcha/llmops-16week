# 모델 적응과 서비스 기획

## 1. 모델 적응과 서비스 기획

WEEK 07 · 2026.10.16 · 온라인 실시간

검색 이후의 기술 선택과 기획서 초안 0.1

차성재 · 무신사 Core AI PM × AI 대학원 겸임교수

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 2. 이번 주의 학습 목표

기술 선택 · 검색·프롬프트·학습의 개선 대상 구분

직접 실험 · 데이터 누출·행렬 구조·선호 손실 확인

기획서 리뷰 · 사용자·범위·평가·위험의 근거 연결

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 3. 16주 로드맵 · 7주차



근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 4. 6–8주차 운영

주차 · 진행

06 · 10.09 · 한글날 · 수업·녹화영상·신규 과제 없음

07 · 10.16 · 실시간 온라인 · 기획서 초안 0.1·피드백

08 · 10.23 · 시험·실시간 수업 없이 수정본 0.2 제출·평가

강의 포인트: 6주차 기술 내용은 이번 주에 연결 · 제출 시각은 소속별 공지

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 5. 100분 수업 구성

시간 · 내용

00–10분 · 운영·복습·기술 선택

10–30분 · SFT·데이터·LoRA

30–45분 · 선호 데이터·DPO·평가

45–50분 · 휴식·커널 준비

50–85분 · Notebook 실습 · 핵심 셀 우선

85–100분 · 기획서 초안·설계 리뷰

강의 포인트: 전체 노트북은 수업 후 확장 가능 · 강의 중 실습 경로는 별도 안내

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 6. 지난 실습의 확인 사항

검색 결과와 답변 품질의 분리

관련 문서가 있어도 날짜·권한·출처 확인 필요

검색 점수는 정답 확률이 아님

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 7. 검색 개선과 모델 적응

검색 개선 · 필요한 근거를 찾는 문제 · 자료·분할·순위·권한 검토

모델 적응 · 반복 출력·행동의 문제 · 학습 데이터·평가·버전 검토

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 8. 반복 실패의 예시

근거 문서는 정확하지만 출력 형식은 불안정

정책 내용 오류와 JSON 형식 오류의 분리

실패 유형을 먼저 확인한 뒤 변경 대상 선택

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 9. 기술 대안의 출발점

문제 · 우선 검토 · 추가 확인

출력 계약 위반 · 프롬프트·검증 · 반복 실패 유형

최신 문서 누락 · 검색·문서 관리 · 버전·권한

반복 행동 불안정 · SFT·LoRA · 학습 자료·평가

답변 선호 불일치 · 선호 기준·DPO · 라벨 편향·비용

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 10. 기술 선택의 근거

기술 이름보다 개선할 실패 유형

기준선과 대표 실패 사례의 기록

구현 비용과 남은 위험의 비교

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 11. 지도 미세조정

Supervised Fine-Tuning · SFT

입력과 기대 답변을 이용한 추가 학습

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 12. 모델 적응의 흐름

사전학습 · 범용 언어 패턴

SFT · 기대 답변 학습

선호 최적화 · 상대 선택 학습

평가·서빙 · 업무 조건 검증

강의 포인트: 프로젝트마다 모든 단계가 필요한 것은 아님

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 13. SFT의 학습 신호

입력에 이어 나올 답변 토큰의 예측

정답 예시의 형식·품질·사용 권한이 중요

학습 손실 감소만으로 서비스 품질 판단 불가

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 14. 외부 지식과 반복 행동

검색 증강 생성 · 외부 문서를 요청에 제공 · 변경·삭제·접근 제어 관리

지도 미세조정 · 반복 형식·행동을 학습 · 학습 자료·재평가·복구 관리

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 15. 학습 데이터 한 건

instruction: 문의 상태 정리
input: 합성 사례 DEMO-01
response:
  status: review
  source: DEMO-01

입력·기대 출력의 경계

실제 고객 정보가 아닌 합성 예시

출력 계약과 근거의 분리

강의 포인트: JSON 출력 실험 · 실제 업무 정책 아님

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 16. 데이터 준비의 순서

수집·허가 · 사용 범위 확인

형식 검증 · 필드·출력 계약

분할 · 사건 단위

검토 · 누출·편향 점검

강의 포인트: 형식 검증 통과와 내용 품질 검토의 분리

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 17. 데이터 품질의 네 검사

검사 · 확인 대상 · 실패 예시

필드 · 입력·답변·ID · 빈 instruction

출력 · JSON·필수 키 · answer만 존재

중복 · ID·내용·사건 · 같은 사례 복사

권한 · 사용 허가·보존 · 고객 원문 무단 사용

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 18. 문장 분할과 사건 분할

문장 단위 무작위 분할 · 표현만 다른 같은 사건 혼입 · 평가 결과 과대평가 위험

사건 단위 분할 · 동일 사건을 한 분할에 배치 · 새로운 사건 평가에 더 적합

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 19. 개발과 최종 평가

train · 모델 학습에 사용

dev · 설정·모델 선택에 사용

test · 최종 비교용으로 보류

강의 포인트: test 결과를 보고 설정을 반복 변경하면 독립 평가의 의미 약화

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 20. 합성 데이터의 분할 결과

분할 · 사건 수 · 문장 수

train · 16 · 32

dev · 4 · 8

test · 4 · 8

강의 포인트: Notebook 01 · 24사건 × 2표현 · seed=42 · 실제 고객 자료 아님

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 21. 손실 계산의 범위

입력까지 계산 · 질문·문서 토큰 포함 · 업무 목표와 손실 범위 확인

답변 중심 계산 · 답변 토큰에 학습 신호 · 템플릿·역할 경계 검증

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 22. 손실 마스킹 예시

token_ids = [10, 11, 12, 20, 21, 22]

labels = [-100, -100, -100, 20, 21, 22]

assert sum(x != -100 for x in labels) == 3

강의 포인트: 가상 토큰 ID · 실제 tokenizer나 trainer 실행이 아닌 경계 설명

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 23. 길이 제한과 문맥 손실

문자 수와 토큰 수의 차이

문서 끝의 예외·정답이 잘리는지 확인

모델별 토크나이저와 템플릿으로 재검증

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 24. LoRA와 학습 자원

Low-Rank Adaptation · 저차원 행렬을 이용한 모델 적응

기존 가중치 고정과 작은 변화량 학습

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 25. LoRA의 가중치 변화

W′ = W + (α/r) · BA

W: 고정 가중치 · BA: 학습할 변화량

r: rank · α: scaling 설정

강의 포인트: 일반 LoRA scaling 설명 · 구현별 다른 설정은 구분

근거: https://arxiv.org/abs/2106.09685

## 26. 행렬의 차원

B · 12 × 2

A · 2 × 8

BA · 12 × 8

W + BA · 동일 출력 차원

강의 포인트: Notebook 02 · 작은 행렬 구조 · 언어 모델 학습 아님

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 27. rank와 파라미터 수

rank · 전체 행렬 · 두 행렬 합계

1 · 96 · 20

2 · 96 · 40

4 · 96 · 80

8 · 96 · 160

강의 포인트: 12×8 행렬 · r(12+8) · 작은 예시에서 큰 rank는 절약되지 않음

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 28. rank별 파라미터 비교



강의 포인트: 12×8 합성 행렬 · 전체96개 vs r(12+8) · 실제 모델 메모리 측정 아님

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 29. 근사 오차와 서비스 품질

수학 실험의 결과 · 변화량 행렬 복원 오차 · rank 변화에 따른 구조 확인

실제 서비스의 결과 · 근거·유용성·형식·운영 비용 · 고정 업무 입력으로 별도 평가

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 30. rank별 행렬 근사 오차



강의 포인트: Notebook02 실행 결과 · 상대 Frobenius 오차 · 실제 LoRA 학습 결과 아님

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 31. 특이값 분해 실험의 범위

SVD · Singular Value Decomposition

이미 만든 행렬을 저차원으로 근사

실제 LoRA는 데이터·손실에 따라 A·B를 학습

강의 포인트: Notebook의 SVD 결과를 Adapter 학습 성공으로 표시하지 않음

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 32. 학습 방식의 비교

방식 · 학습 대상 · 운영 확인

전체 미세조정 · 다수 가중치 · 자원·저장·복구

LoRA · 저차원 행렬 · rank·대상 모듈

QLoRA · 양자화 Base + LoRA · 정밀도·지원 환경

강의 포인트: QLoRA · Quantized Low-Rank Adaptation · 양자화 기반 LoRA

근거: https://arxiv.org/abs/2106.09685, https://arxiv.org/abs/2305.14314

## 33. 메모리 추정의 구성

가중치 크기만으로 GPU 메모리 판단 불가

gradient·optimizer state·activation·버퍼 추가

동일 모델·길이·batch에서 최대 사용량 측정

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 34. Adapter 버전의 구성

Base · 모델·revision

Tokenizer · 템플릿·버전

Adapter · 설정·데이터

평가 기록 · 입력·결과·환경

강의 포인트: Adapter 파일만 남기면 재현·복구가 어려움

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 35. 학습 전 실행 조건

자료 · 사용 허가·분할·누출 점검

환경 · GPU·라이브러리·모델 접근

평가 · 동일 입력·실패 유형·중단 조건

강의 포인트: 이번 필수 실습은 모델 다운로드·GPU 학습 없이 진행

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 36. 선호 데이터와 DPO

Direct Preference Optimization · 직접 선호 최적화

같은 질문의 두 답변과 선택 기준

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 37. 기대 답변과 선호쌍

SFT · 입력 → 기대 답변 · 원하는 출력을 직접 제시

DPO · 질문 + chosen + rejected · 두 출력의 상대 선택 기준

근거: https://arxiv.org/abs/2305.18290

## 38. 선호쌍의 예시

질문: 근거 문서가 없는 문의

선택: 확인할 수 없어 담당자 검토가 필요합니다.

비선택: 무조건 승인됩니다.

강의 포인트: 합성 예시 · 선택 기준: 근거 없는 단정 방지

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 39. 선호 데이터의 검토

항목 · 질문

동일 입력 · 두 답변이 같은 질문에 대한 것인가

선택 이유 · 근거·유용성·형식 중 기준이 명시됐는가

차이 · 동일 답변·여러 품질 차이가 섞이지 않았는가

편향 · 길이·순서·라벨러 선호를 검토했는가

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 40. 길이와 품질

길이가 긴 답변 · 자세해 보여 선택될 수 있음 · 근거 없는 내용도 길어질 수 있음

업무 기준에 맞는 답변 · 필요한 내용과 근거 충족 · 길이와 별개로 기준별 검토

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 41. DPO의 입력

질문 · 같은 prompt

선호쌍 · chosen / rejected

reference · 고정 비교 정책

policy · 학습 대상 모델

강의 포인트: 선호쌍을 더 잘 구분하는 방향의 최적화 · 일반 정확성은 별도 평가

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 42. DPO의 비교량

m = policy 차이 − reference 차이

각 차이 = log P(chosen) − log P(rejected)

시퀀스 log probability · Judge 점수 아님

강의 포인트: 입력·토큰화·종료 조건을 같은 기준으로 계산

근거: https://arxiv.org/abs/2305.18290

## 43. DPO 손실의 방향

Loss = −log sigmoid(β · m)

m이 증가하면 해당 선호쌍의 손실 감소

β: reference 대비 변화의 제어와 관련된 설정

강의 포인트: 한 쌍의 손실 감소가 서비스 품질 향상 전체를 뜻하지 않음

근거: https://arxiv.org/abs/2305.18290

## 44. 손실의 수치 계산

loss0 = dpo_loss(-3, -3, -3, -3, .1)

good = dpo_loss(-2, -5, -3, -3, .1)

bad = dpo_loss(-5, -2, -3, -3, .1)

assert good < loss0 < bad

강의 포인트: Notebook 03 · logaddexp로 수치 안정성 확보

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 45. 고정 log probability의 비교

조건 · margin · 손실 · β=0.1

기준선 · 0 · 0.6931

선호 방향 · 3 · 0.5544

반대 방향 · −3 · 0.8544

강의 포인트: 수식 확인용 값 · 모델 평가 결과 아님

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 46. margin과 DPO 손실



강의 포인트: β=0.1 · 고정 log probability 수치 실험 · 업무 품질 측정 아님

근거: https://arxiv.org/abs/2305.18290, repo:course_labs/adaptation.py

## 47. 장난감 정책의 학습

질문 한 개 · 고정 답변 두 개

선택 확률을 결정하는 θ 하나만 갱신

새 질문의 일반화·정확성·안전성 미검증

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 48. DPO의 단순화와 남은 비용

PPO 기반 RLHF 경로 · 보상 모델·온라인 샘플링 등 필요 · 실행 구성과 자원 관리

DPO 경로 · 고정 선호쌍·reference로 학습 · 자료 라벨·편향·재평가는 여전히 필요

강의 포인트: RLHF · Reinforcement Learning from Human Feedback · 인간 피드백 기반 강화학습

근거: https://arxiv.org/abs/2305.18290

## 49. 비교 평가와 기술 선택

품질 · 운영 비용 · 실패 유형의 분리

기획서에 들어갈 검증 계획

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 50. 고정 입력의 비교표

항목 · 동일 조건 · 결과 기록

입력 · 평가셋·템플릿 · 응답 원문

품질 · 근거·형식·유용성 · 통과·실패 이유

설정 · 모델·Adapter·생성 · 버전·seed

운영 · 환경·반복 수 · 시간·비용·오류

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 51. 비교의 공정성

개발에 사용한 입력과 보류 입력의 분리

답변 순서 가림과 동일 기준의 사람 검토

최고 사례만 고르지 않은 실패 기록

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 52. 평가 기준의 구체화

차원 · 확인 방법

근거 · 인용한 문장이 주장과 일치하는가

형식 · 출력 계약과 필수 필드를 충족하는가

유용성 · 사용자의 다음 행동에 도움이 되는가

안전·거절 · 위험한 단정·과도한 거절이 있는가

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 53. 실험 결과와 의사결정

결과 기록 · 어떤 입력에서 무엇이 바뀌었는가 · 조건·수치·원문 보존

선택 이유 · 지금 어떤 대안을 채택할 것인가 · 비용·위험·다음 검증 포함

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 54. 모델 승격 전 검토

기준선 · 이전 버전과 같은 입력 비교

승격 · 사전 합의한 품질·비용 조건 확인

복구 · Base·Adapter·설정의 되돌리기 경로

강의 포인트: 승격 조건을 결과 확인 후 유리하게 변경하지 않음

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 55. 단계별 Notebook 실습

Python 3.11 · 기존 .venv

기본 실행은 API 키·Ollama·GPU 불필요

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 56. Notebook과 산출물

파일 · 실험 · 기록

01 · data_quality_split · 오염·누출·분할 · Dataset Card

02 · low_rank_adaptation · rank·오차·비용 · 행렬 실험표

03 · preference_dpo · 선호쌍·손실·정책 · 한계 포함 비교표

04 · project_proposal · 요구사항·위험·시안 · 초안 HTML·JSON

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 57. VS Code 환경 준비

python3.11 -m venv .venv

source .venv/bin/activate

python -m pip install -r requirements.txt

code .

강의 포인트: 기존 .venv가 있으면 재생성 불필요 · Windows는 .venv\Scripts\activate

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 58. VS Code 실행 경로

루트 폴더 · llmops-16week 전체 열기

Notebook 커널 · Python 3.11 · .venv 선택

셀 실행 · 위에서 아래로 · 한 변수 변경·기록

강의 포인트: 실행 위치: week07/lab/notebooks · 제출물은 공개 GitHub에 업로드 금지

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 59. 실습 01 · 누출 탐지

정상 48건 → 중복·깨진 JSON 주입

문장 단위 분할: 24사건 모두 교차

사건 단위 분할: 교차 사건 없음

강의 포인트: 핵심 셀: 문장 분할의 위험 → 사례 단위 분할 → 누출 탐지

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 60. 실습 01 · 검증 코드

data = examples()

splits = split_groups(data, seed=42)

assert not leakage(splits)

print({k: len(v) for k, v in splits.items()})

강의 포인트: 예상 문장 수: train32 · dev8 · test8

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 61. 실습 02 · rank의 비교

rank 1·2·4·8의 근사 오차

전체 96개와 두 행렬 파라미터 수 비교

원본 가중치 고정 여부를 assert로 확인

강의 포인트: 핵심 셀: rank 2 → 근사 오차 → rank 시각화 → 비용 계산

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 62. 실습 03 · 선호 손실

기준선·선호·반대 방향의 손실 비교

β만 변경한 민감도 실험

한 질문 정책의 학습과 한계 기록

강의 포인트: 핵심 셀: 기준선 → 선호 방향 → beta → 장난감 정책

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 63. 실습 03 · 반복 실험

for beta in [.1, .5, 1.]:

    history = toy_preference_training(beta=beta)

    print(beta, history[-1])

강의 포인트: 같은 학습률·80step · 실제 LLM 품질 비교가 아닌 장난감 정책

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 64. 실습 04 · 기획서 생성

문제·대안·범위·평가·복구의 문서화

항목 누락 검사와 내용 검토의 분리

HTML 시안 검토와 교수에게 확인할 질문

강의 포인트: output/validation/adaptation-labs/proposal-draft.html · 로컬 출력

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 65. 실습의 완료와 확장

오늘의 기본 완료 · 필수 셀 실행·가정과 한계 기록 · GPU 없는 공통 경로

선택 확장 · 기존 SFT/DPO 보존 실습 검토 · 별도 GPU 환경·의존성 검증 필요

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 66. 프로젝트 초안과 설계 리뷰

7주차 초안 0.1 → 교수 피드백 → 8주차 수정본 0.2

시험 없이 제출물 평가

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 67. 프로젝트 운영과 제출

구분 · 기준

아주대AI대학원 · 2–4인 자율 팀 · LMS 제출

군산대·국립창원대 등 · 개인 진행 가능 · 공지 교수 이메일

개별 예외 · 교수 승인 여부 별도 확인

10.16 · 7주차 · 초안 0.1·피드백 준비

10.23 · 8주차 · 수정본 0.2 온라인 제출·평가

강의 포인트: 팀 신청 폼은 기획서 제출함이 아님 · 정확한 시각은 소속별 공지

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 68. 기획서의 구성

2Pager · 문제·제안·근거

PRD · 요구사항·검증

로드맵 · 범위·일정·담당

선택 자료 · 시안·짧은 데모

강의 포인트: 형식 자유 · 동일 내용의 중복 문서 제출 불필요

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 69. 두괄식 2Pager

구간 · 핵심 정보

첫 문단 · 누구에게 무엇을 제안하는가

문제·근거 · 현재 대안의 한계와 관찰 증거

해결·범위 · 최소 기능과 이번에 하지 않을 일

검증·요청 · 성공 조건·주요 위험·확인할 질문

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 70. 제품 요구사항 문서

사용 흐름 · 입력·처리·출력·수정

요구사항 · 기능과 완료 조건의 연결

운영 · 권한·비용·실패·복구

강의 포인트: PRD · Product Requirements Document · 제품 요구사항 문서

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 71. 글쓰기 개선 서비스

원문 구조 · 서론·본론·결론

기준별 판단 · 주장·근거 연결

근거 피드백 · 원문 위치 제시

사용자 수정 · 보류·재검토

강의 포인트: 글쓰기의 유창성·이해도·구조를 하나의 점수로 섞지 않는 설계

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 72. 글쓰기 서비스의 평가

차원 · 확인 방법 · 실패 처리

구조 · 문단 역할·주장 구분 · 불명확 구간 보류

근거 · 원문 위치·주장 연결 · 근거 누락 표시

유창성 · 문장 연결·반복 · 수정 제안 선택

이해도 · 질문 의도·내용 이해 · 사용자 확인 요청

강의 포인트: 설명용 평가 설계 · 학생 성적 자동 결정 도구가 아님

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 73. Prototype과 제품

Prototype · 프로토타입 · 핵심 흐름을 확인하는 시안 · 합성 입력·실행 범위 명시

운영 제품 · 권한·실패·평가·보존 관리 · 시안만으로 준비 완료 판단 불가

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 74. 세 관점의 검토 질문

관점 · 질문

사업·대표 · 누구의 문제인가 · 대안보다 가치가 있는가

사용자 경험 · 실패·보류·수정 흐름이 이해되는가

개발·평가 · 권한·구현 범위·평가·복구가 가능한가

강의 포인트: UX · User Experience · 사용자 경험

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 75. 피드백과 수정 기록

질문 · 현재 버전과 한 가지 결정 제시

피드백 · 가정·누락·위험의 확인

수정 · 채택·보류·반박과 근거 기록

강의 포인트: 교수 피드백을 받은 뒤 변경 이유와 추가 증거를 수정본에 명시

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 76. 제출 전 점검

항목 · 확인

문제·범위 · 사용자·대안·최소 기능·제외 범위

자료·평가 · 사용 권한·고정 입력·비교·실패 기준

운영·일정 · 보류·복구·담당·완료 조건

문서 형식 · PPT·Word·PDF·HTML 가능 · HWP 제외

개인정보 · LMS·이메일 제출 · 공개 GitHub 금지

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py

## 77. 참고 자료와 재현 경로

LoRA · Hu et al. / QLoRA · Dettmers et al.

DPO · Rafailov et al. · 원 논문과 수치 실험 구분

repo: week07/lab/notebooks · 운영 커리큘럼

근거: https://arxiv.org/abs/2106.09685, https://arxiv.org/abs/2305.14314, https://arxiv.org/abs/2305.18290, repo:curriculum/2026-2/00_운영_커리큘럼.md, repo:course_labs/adaptation.py