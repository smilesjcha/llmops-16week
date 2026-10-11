# SFT · LoRA 참고 강의안

## 1. SFT · LoRA

2025년 6주차 강의자료 재구성

2026.10.09 한글날 · 정규 수업·영상·신규 과제 없음

차성재 · LLMOps 통합 강좌

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 2. 2026년 6주차 운영

한글날 휴일

이 자료는 향후 강의 재사용을 위한 참고안

현행 7주차 강의 내용·과제 일정과 별개

강의 포인트: 10월 9일 수업·녹화·신규 과제 없음

근거: repo:curriculum/2026-2/00_운영_커리큘럼.md

## 3. 학습 범위

데이터 · instruction·chat 형식, 분할, 누출 점검

학습 · SFT의 목적과 LoRA 설정의 역할

검증 · 동일 입력에서 Base와 Adapter 비교

강의 포인트: 2025년 6주차 SFT·LoRA 내용을 20장으로 재구성

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 4. 모델 적응의 위치

사전학습 · 범용 언어 패턴

지도 미세조정 · 입력과 기대 답변

선호 최적화 · 선택 기준

서빙·평가 · 운영 조건 검증

강의 포인트: 각 단계의 데이터와 판단 기준을 구분

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 5. 적응 방법의 선택

상황 · 우선 검토 · 확인할 한계

지식 최신성 · 검색·근거 연결 · 자료의 버전·권한

출력 형식 · 프롬프트·검증 · 대표 입력의 일관성

반복 행동·문체 · SFT·Adapter · 학습 데이터·평가 비용

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 6. SFT의 학습 신호

사용자 입력과 기대 답변의 쌍

모델은 다음 토큰을 예측하도록 학습

입력의 정답까지 무작정 외우게 하지 않도록 손실 범위 점검

강의 포인트: SFT: Supervised Fine-Tuning · 지도 미세조정

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 7. 학습 데이터 한 건

{"instruction":"환불 기간 안내",
 "input":"9월 주문, 반품 승인",
 "response":"승인일 기준 안내 문서를 확인하세요."}

업무 지식은 예시로만

실제 고객 정보 대신 합성 사례

문서 버전·근거는 별도 관리

강의 포인트: 설명용 합성 자료 · 실제 정책 아님

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 8. 템플릿 일관성

학습 · instruction·input·response 경계 고정

추론 · 동일한 역할·종료 토큰 적용

비교 · Base와 Adapter에 같은 입력 적용

강의 포인트: 학습·평가·서빙에서 형식 불일치 방지

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 9. 손실 마스킹

입력까지 학습 · 질문 형식이 손실에 포함 · 답변 성능 평가가 흐려질 수 있음

답변 구간 중심 · 기대 답변 토큰만 손실 계산 · 설계한 템플릿과 마스킹 확인

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 10. 데이터 분할과 누출

검사 · 위험 · 최소 확인

문장 중복 · 검증 결과 과대평가 · 해시·유사 문장 점검

동일 사건 · 표현만 다른 사례의 누출 · 사건 단위 분할

시간 역전 · 미래 정보로 과거 평가 · 기준일 기록

길이 분포 · 잘림과 형식 붕괴 · 토큰 길이 요약

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 11. LoRA와 자원 선택

전체 가중치 대신 작은 Adapter 학습

품질·메모리·운영 복잡도의 교환

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 12. LoRA의 핵심

기존 가중치는 고정, 변화량만 학습

낮은 rank의 두 행렬로 업데이트 표현

rank가 커질수록 학습 파라미터와 자원 증가

강의 포인트: 성능 향상은 데이터·평가 조건에 따라 별도 확인

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 13. Adapter 적용 흐름

Base 모델 고정 · 기존 가중치 유지

대상 모듈 선택 · 모델 구조 확인

LoRA 학습 · 작은 변화량 갱신

Adapter 보존 · Base와 함께 버전 기록

강의 포인트: 추론 시 Base와 Adapter의 조합·버전 기록

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 14. 미세조정 방식 비교

방식 · 학습 대상 · 실무 확인

전체 미세조정 · 모델 가중치 다수 · 자원·저장 비용

LoRA · 저차원 Adapter · rank·alpha·대상 모듈

QLoRA · 양자화 Base + Adapter · 지원 환경·정밀도·속도

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 15. LoRA 설정 예시

r = 8
lora_alpha = 16
target_modules = ["q_proj", "v_proj"]
seed = 42

설정값의 역할

rank·alpha: 변화량의 크기

target_modules: 적용 대상

seed: 재현 조건

강의 포인트: 2025 보존 실습의 예시 · 모델 구조에 맞게 대상 모듈 확인

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 16. 재현성 기록

데이터 · 스키마·분할·해시·사용 허가

실험 · 모델·토크나이저·설정·seed

산출물 · Adapter·로그·평가표·실패 사례

강의 포인트: 기록이 없으면 Base와 Adapter의 변화 원인을 분리하기 어려움

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 17. Base와 Adapter 평가

검사 · 동일 조건 · 기록

대표 입력 · 프롬프트·온도·길이 · 응답 원문

형식 준수 · 출력 스키마·금지 항목 · 통과·실패 사유

근거 정확성 · 참조 자료·기준일 · 오류 유형

운영 비용 · 환경·반복 횟수 · 시간·메모리

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 18. 실패 유형

학습 손실 감소만으로 사용 품질을 판단할 수 없음

과적합·형식 붕괴·근거 없는 답변을 따로 분류

검증 입력을 바꾸지 않은 재실험은 독립 검증이 아님

강의 포인트: 정량 결과와 수작업 검토의 기록을 함께 보존

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 19. 참고 실습의 산출물

설정 파일 + Adapter + 비교표

학습 실행은 GPU·모델 다운로드·의존성 확인 후 선택

본 참고안은 기존 2025 실습 파일을 수정하거나 재실행하지 않음

강의 포인트: AS-IS 보존 자료의 실행 전 환경 검증 필요

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb

## 20. 근거 자료

2025년 6주차 SFT·LoRA 보존본

통합 강의안 · 원본 슬라이드 콘티 · 실습 notebook

2026년 2학기 일정은 별도 운영 커리큘럼 기준

근거: repo:AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md, repo:AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md, repo:AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb, repo:curriculum/2026-2/00_운영_커리큘럼.md