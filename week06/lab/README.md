# 6주차 · 손실·마스킹·양자화 수치 실습

2026년 10월 9일은 수업·녹화영상·신규 과제가 없는 휴일이다. 여기의 실습 안내는 제출 과제가 아닌 선택 참고다. SFT/LoRA 기술 내용은 7주차 수업에서 연결한다.

- [6주차 수치 실습 Notebook · 29셀 / 코드 14셀](notebooks/01_loss_quantization.ipynb)
- [공통 환경·VS Code 안내](../../week07/lab/README.md)
- [학습 데이터·분할 Notebook](../../week07/lab/notebooks/01_data_quality_split.ipynb)
- [LoRA 행렬 구조 Notebook](../../week07/lab/notebooks/02_low_rank_adaptation.ipynb)
- [2025년 SFT/LoRA 보존 실습](../../AS-IS%202025%202nd%20semester/practice/week06/06_lora_sft.ipynb)

## VS Code 실행 순서

1. 저장소 루트를 열고 기존 `.venv`를 활성화한다. 없는 경우 위 공통 환경 안내를 따른다.
2. `week06/lab/notebooks/01_loss_quantization.ipynb`를 열고 **Select Kernel → Python Environments → .venv (Python 3.11)**을 선택한다.
3. **Run All**로 위에서 아래로 실행한다. NumPy 1.26.4와 기존 Jupyter 환경을 사용하며 패키지를 추가하지 않는다.
4. 7주차 Notebook 01의 데이터 누출, 02의 rank 비교 실험을 이어서 확인한다.

Windows 환경 활성화는 `.venv\Scripts\activate`, macOS/Linux는 `source .venv/bin/activate`다.

| 실험 | 바꿀 변수 | 확인할 결과 |
|---|---|---|
| 교차 엔트로피 | 정답 확률 | 확률이 낮을 때 손실 증가 |
| 마스킹과 Shift | 답변 시작 위치 | 학습 정답 20·21·22와 대응 위치 |
| 길이 제한 | 3·4·6 | 남는 답변 정답 0·1·3개 |
| LoRA 초기화 | A·B·배율 | 초기 BA=0, 원본 W 고정 |
| 균등 양자화 | 2·3·4·8-bit | 복원값과 평균제곱오차 |
| 가중치 저장량 | 16·8·4-bit | 7B의 원시 저장량 14·7·3.5 GB |

결과는 Git 추적에서 제외된 `output/validation/week06-concepts/concept-report.json`에 저장한다. 예상값을 적고 실행한 뒤 한 변수씩 변경한다. 수치의 단위·가정·확인하지 못한 점도 기록한다.

## 실행 검증과 범위

```bash
python scripts/verify_week06_notebook.py
```

새 커널에서 14개 코드 셀을 실행한다. 개념 계산과 7주차 공통 Notebook은 모델 다운로드·GPU·API 키가 필요 없다. 실제 SFT·LoRA·QLoRA 모델 학습은 실행하지 않으며, 균등 양자화는 NF4 구현이 아니다. NumPy 배열을 실제 2-bit/4-bit 저장 형식으로 패킹하지도 않는다. 가중치 원시 bit 계산과 실제 VRAM 사용량을 구분한다.

보존 실습은 별도 GPU 환경에서 선택 검증한다. 데이터·분할·행렬 코드는 중복 복제하지 않고 7주차 기준본을 참조한다. 이번 복습은 휴일의 새 과제나 제출 요구가 아니다.
