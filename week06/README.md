# Week 06 · SFT·LoRA·QLoRA 시각 보충 강의안

2026년 2학기 6주차인 **10월 9일은 한글날 휴일**이며 당시 수업·녹화영상·신규 과제는 없다. 6주차 기술 내용은 10월 16일 7주차 통합 강의에서 이어서 진행했다. 아래 자료는 이 내용을 복습하기 위한 **32장 시각 보충 강의안**이다.

- [학생용 PDF · 32쪽](../output/pdf/06_week6_sft_lora_reference.pdf)
- [발표용 PPT · 32장](lecture/06_week6_sft_lora_reference.pptx)
- [장표별 설명과 근거](lecture/lecture-notes.md)
- [외부 도식 출처·인용 안내](lecture/assets/SOURCES.md)
- [6–7주차 통합 녹화 영상](../week07/resources/README.md)

## 자료의 범위

- [선택 실습 안내](lab/README.md): 실행 검증한 데이터·분할·행렬 Notebook은 7주차 기준본을 참조
- [7주차 정규 강의·실습·초안 제출](../week07/README.md)

- 학습 데이터 형식·분할·누출, 손실 마스킹
- SFT와 LoRA/QLoRA의 적용 판단
- 설정, 재현성, Base/Adapter 평가 계획
- 2025 보존 실습의 설정 예시. 현재 기기에서 GPU 학습을 재실행했다는 뜻은 아니다.

실습에 나온 환불 안내는 **합성 예시**이며 실제 정책이나 고객 정보를 뜻하지 않는다. 모델·라이브러리 버전과 하드웨어 호환성은 재사용 시 다시 검증해야 한다. 2025년 보존 notebook은 수정하지 않았다.

## 재사용 절차

1. 2026년 운영안과 소속별 아주대·군산대·국립창원대 공지를 확인한다. 현행 6주차를 정규 강의로 표시하지 않는다.
2. `scripts/week06_deck_content.mjs`에서 6주차 내용을 새 학기 일정·학습성과에 맞게 수정한다.
3. `scripts/presentation_design.mjs`에서 색·서체·레이아웃 의도와 리듬을 확인한다.
4. `scripts/build_course_deck.mjs 6`으로 다시 빌드하고 모든 슬라이드를 PDF로 렌더링해 검수한다.

구체적인 설계·검증 원칙은 [PPT 제작 가이드](../scripts/presentation-production.md)를 따른다.

## 출처

- `AS-IS 2025 2nd semester/01_AS-IS_주차별_통합_강의안.md`의 6주차 SFT/LoRA 요약
- `AS-IS 2025 2nd semester/02_AS-IS_주차별_강의_디자인_콘티.md`의 6주차 실제 장표 흐름
- `AS-IS 2025 2nd semester/practice/week06/06_lora_sft.ipynb`의 보존 실습
- `curriculum/2026-2/00_운영_커리큘럼.md`의 현행 휴일 운영
