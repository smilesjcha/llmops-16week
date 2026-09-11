# Week 02 외부 시각자료 출처

확인일: 2026-09-11. 슬라이드의 사진·연구 도표는 아래 원자료를 사용한다. 수업용 도식과 로컬 실습 차트는 원자료 이미지와 구분한다. 슬라이드의 배경·주석은 흑백·파랑을 유지하고, 외부 증거 이미지의 색·축·범례는 원본대로 보존했다.

## 12장 · 글자가 바꾼 이미지 분류

- 저작자: Gabriel Goh et al., 2021, *Multimodal Neurons in Artificial Neural Networks*, Distill.
- [원문과 Reuse 안내](https://distill.pub/2021/multimodal-neurons/)
- 원본: [사과 사진](https://distill.pub/2021/multimodal-neurons/typographic/in-the-wild-2/apple-blank.jpg), [iPod 메모가 붙은 사과](https://distill.pub/2021/multimodal-neurons/typographic/in-the-wild-2/apple-ipod.jpg)
- [원본 분류 점수](https://raw.githubusercontent.com/distillpub/post--multimodal/master/static/typographic/in_the_wild_2.json)
- 라이선스: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), [동봉 전문](assets/external/distill-LICENSE.txt).
- 변경: 사진 원본 보존, 비율 유지 배치, 한글 설명 추가. 사진 내용을 생성하거나 편집하지 않았다.

같은 물체에 붙은 글자가 이미지 분류에 영향을 준 사례다. 사과 사진의 Granny Smith 85.61%, 메모 사진의 iPod 99.68%는 **해당 입력에 대한 zero-shot 분류 점수**다. 모델의 일반 정확도나 검증된 신뢰도로 해석하지 않는다. CLIP(Contrastive Language–Image Pre-training)의 이미지 분류 실험이며, 텍스트 대규모 언어 모델의 프롬프트 주입과 동일한 실험이라고 설명하지 않는다.

## 24장 · 예시를 입력으로 전달하는 구조

- 저작자: Sewon Min et al., 2022, *Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?*, EMNLP.
- [논문 페이지](https://aclanthology.org/2022.emnlp-main.759/) · [원본 PDF](https://aclanthology.org/2022.emnlp-main.759.pdf)
- 사용 부분: PDF 2쪽, Figure 2. 예시 세 개와 새 입력이 언어 모델에 함께 전달되는 구조.
- 라이선스: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [ACL 공식 저작권 안내](https://aclanthology.org/faq/copyright/).
- 변경: 원본 PDF 페이지를 렌더한 뒤 PowerPoint 사진 표시 영역으로 Figure 2를 확대. 도표 내용·색상·라벨 보존, 한글 해설 추가.

실습의 v3는 v2 규칙에 별도 예시 세 개를 더한다. 추론 시 입력에 예시를 포함하는 방식과 모델 가중치 학습을 구분한다. 논문의 특정 실험 관찰을 “잘못된 예시를 써도 괜찮다”는 실무 권고로 일반화하지 않는다.

## 25장 · 정보의 위치와 모델의 활용

- 저작자: Nelson F. Liu et al., 2024, *Lost in the Middle: How Language Models Use Long Contexts*, TACL.
- [논문 페이지](https://aclanthology.org/2024.tacl-1.9/) · [원본 PDF](https://aclanthology.org/2024.tacl-1.9.pdf)
- 사용 부분: PDF 2쪽, Figure 1. 정답을 포함한 문서의 위치와 질의응답 정확도 관계.
- 라이선스: PDF 첫 쪽의 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 표기. [ACL 공식 저작권 안내](https://aclanthology.org/faq/copyright/).
- 변경: 원본 PDF 페이지를 렌더한 뒤 Figure 1 영역 확대. 원본 축·범례·곡선·색상 보존, 한글 해설 추가.

그림은 20개 문서(약 4K 토큰)와 당시 GPT-3.5-Turbo-0613을 사용한 특정 질의응답 조건이다. 2023년 실험, 2024년 출판임을 구분한다. 현재 모든 모델에 같은 U자 형태가 나타난다고 주장하지 않는다. 수업에 연결하는 점은 프롬프트 비교 시 입력 내용뿐 아니라 입력 순서와 모델·생성 설정도 고정해야 한다는 것이다.

## 66장 · 생각의 경로와 후보 탐색

- 저작자: Shunyu Yao et al., 2023, *Tree of Thoughts: Deliberate Problem Solving with Large Language Models*, NeurIPS.
- [논문](https://arxiv.org/abs/2305.10601) · [공식 저장소](https://github.com/princeton-nlp/tree-of-thought-llm)
- [원본 도표](https://raw.githubusercontent.com/princeton-nlp/tree-of-thought-llm/master/pics/teaser.png)
- 라이선스: MIT, Copyright (c) 2023 Shunyu Yao. [동봉 전문](assets/external/tree-of-thoughts-LICENSE.txt).
- 변경: 원본 도표에서 Chain of Thought와 Tree of Thoughts 패널을 각각 확대 배치. 두 패널의 내용·색·화살표 보존, 한글 해설 추가. 전체 원본도 자산 폴더에 보존.

후보 생성·평가·선택·되돌아가기가 추가 호출과 연결되는 구조를 설명한다. 이번 실습의 v1·v2·v3 비교는 ToT 구현이 아니다. 원 논문의 과제별 성공률을 이번 실습의 보장 수치로 사용하지 않는다.

## 원본과 수업용 제작물의 구분

- 외부 원본 파일: [`assets/external`](assets/external/)
- 원본 크기와 표시 영역: [figures.json](assets/external/figures.json)
- 54장 실제 모델 차트: [로컬 실행 요약 데이터](assets/ollama-results-summary.json), [실습 검증 보고서](../LAB_TEST_REPORT.md). 외부 논문의 결과가 아니다.
- 나머지 처리 흐름·판단 트리·평가 행렬은 실습 코드와 합성 사례를 설명하는 편집 가능한 수업용 도식이다.
