# Week 07 검증 기록

검증일: 2026-10-11. 공통 Python 3.11.14 / NumPy 1.26.4 환경.

| 검증 | 결과 |
|---|---|
| 공통 모듈·1–3주차 회귀 테스트 | 96개 통과 |
| 7주차 Notebook 독립 커널 실행 | 4개 / 코드 53셀 통과 |
| `pip check` | 의존성 충돌 없음 |
| PPT 내용·출처 검사 | 77장, 누락 경고 없음 |
| PPT 최종화 검사 | 감사 경고 없음 |
| PDF 페이지·텍스트 경계 검사 | 77쪽, 빈 페이지·페이지 밖 텍스트·대체 문자 없음 |
| PDF 렌더링 육안 검토 | 전체 장표의 렌더링 확인, 발견된 잘림·겹침 없음 |

## 재현 명령

저장소 루트에서 기존 `.venv`를 활성화한 뒤 실행한다.

```bash
PYTHONPATH=week03/lab python -m pytest -q course_labs/tests week01/lab/tests week02/lab/tests week03/lab/tests
python -m pip check
python scripts/verify_adaptation_notebooks.py
node scripts/validate_course_decks.mjs
```

PDF 검사에는 별도의 제작 환경에 `pdfplumber`, Pillow, Poppler가 필요하다. 수강생 공통 실습 환경에는 추가 설치할 필요가 없다. `scripts/qa_week07_pdf.py`의 자동 검사는 실제 도형 겹침의 부재를 보증하지 않으므로 렌더링 검토를 함께 진행한다.

## 검증하지 않은 범위

- 실제 언어 모델 SFT·LoRA·DPO 학습, GPU 메모리와 학습 속도
- 보존된 2025년 GPU 실습의 모든 모델·패키지 조합
- 학생 제출물의 내용 정확성·성적 및 팀 배정 완료 여부

공통 Notebook의 SVD·장난감 선호 정책은 개념 실험이다. 실제 LLM 품질 향상이나 서비스 운영 준비 완료를 입증하는 결과로 사용하지 않는다.
