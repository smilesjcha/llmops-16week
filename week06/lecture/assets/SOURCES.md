# SFT·LoRA·QLoRA 시각 자료 출처

확인일: 2026-10-17. 원 논문과 제작 주체의 공식 문서를 우선했다. 검색 결과의 재게시 이미지나 출처 불명 도식은 사용하지 않았다.

| 파일 | 제작자·원출처 | 강의에서 읽는 부분 |
|---|---|---|
| `sft-trainer.png` | [Hugging Face TRL SFT Trainer](https://huggingface.co/docs/trl/sft_trainer), [원본 이미지](https://huggingface.co/datasets/trl-lib/documentation-images/resolve/main/sft_figure.png) | 다음 토큰 예측, label shift, 교차 엔트로피 |
| `sft-assistant-mask.png` | 같은 공식 문서의 [원본 이미지](https://huggingface.co/datasets/trl-lib/documentation-images/resolve/main/train_on_assistant.png) | assistant 답변에 한정한 손실 마스킹 |
| `sft-completion-mask.png` | 같은 공식 문서의 [원본 이미지](https://huggingface.co/datasets/trl-lib/documentation-images/resolve/main/train_on_completion.png) | prompt/completion 경계와 label 선택 |
| `lora-paper-figure1.png` | Edward J. Hu 외, [LoRA 원 논문](https://arxiv.org/abs/2106.09685), Figure 1, v2 p.1 | 고정 W와 학습 A·B의 두 계산 경로 |
| `qlora-paper-figure1.png` | Tim Dettmers 외, [QLoRA 원 논문](https://arxiv.org/abs/2305.14314), Figure 1, v1 p.3 | 전체 미세조정·LoRA·QLoRA의 모델·Adapter·optimizer 상태 |

## 원본 보존과 인용

- TRL 이미지 파일은 원본 바이트를 유지한다. PPT에는 PowerPoint의 기본 `grayscl` 표시 효과를 적용하며, 이미지의 글자·연결·정보를 다시 그리지 않는다.
- 논문 도식은 해당 Figure 영역만 발췌해 300 dpi 흑백으로 렌더링했다. 도식의 크기를 실제 메모리 사용량 비율로 해석하지 않는다.
- QLoRA 논문은 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)이다. 발췌와 흑백 변환을 명시했다.
- LoRA 논문의 arXiv 표기는 비독점 배포 허가다. 이 허가를 재배포용 오픈 라이선스로 확대 해석하지 않는다. 본 강좌는 기법 설명·비교에 필요한 Figure 1을 출처와 해설을 붙인 교육용 인용으로 사용한다.
- TRL 문서 이미지도 출처를 붙인 교육용 인용이다. TRL 코드의 Apache-2.0을 별도 이미지의 포괄적 이용 허가로 간주하지 않는다. 외부 시각 자료는 본 저장소의 자체 제작물과 구분하며, 별도 재사용 시 원저작자의 조건을 확인한다.
- 각 장표의 발표자 노트에도 원문 URL을 기록했다. 강의용 수식·표·추가 해설은 편집 가능한 PowerPoint 객체다.

추가 검토 자료: [Hugging Face QLoRA 공식 해설](https://huggingface.co/blog/4bit-transformers-bitsandbytes), [PEFT LoRA 가이드](https://huggingface.co/docs/peft/developer_guides/lora). 본 수업의 설치·실행 조건은 저장소의 고정 환경이 우선하며, 외부 문서의 최신 설치 명령을 그대로 적용하지 않는다.

## 76쪽 확장본의 계산·도식

- 메모리·gradient accumulation·checkpointing 설명: [Transformers v4.46.3 공식 문서 원본](https://github.com/huggingface/transformers/blob/v4.46.3/docs/source/en/perf_train_gpu_one.md). 문서 개념을 참고하며 해당 버전을 공통 환경 설치값으로 지정한 것은 아니다.
- 다음 토큰 정렬표와 LoRA 두 경로는 위 공식 원리의 편집 가능한 수업용 도식이다. 원 논문 실험 수치와 구분한다.
- 새 손실·균등 양자화·7B 원시 저장량 차트는 `week06/lab/notebooks/01_loss_quantization.ipynb`의 계산에 기반한다. 실행 결과는 공개하지 않는 `output/validation/week06-concepts/concept-report.json`에 생성한다.
- 균등 양자화는 `[-1,1]`의 1,001개 값, 반올림, 평균제곱오차를 사용한 자체 수치 실험이다. NF4·실제 모델 정확도·GPU 메모리·속도 측정으로 해석하지 않는다.
- rank 오차 차트는 7주차 Notebook 02의 SVD 근사 결과다. 실제 LoRA Adapter 학습 결과가 아니다. 차트는 편집 가능한 PowerPoint 객체이며 표시 정밀도보다 높은 소수 6자리로 데이터를 보존한다.
