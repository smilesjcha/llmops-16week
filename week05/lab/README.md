# Week 05 · 검색 비교와 개선 실습

환경·커널·오류 해결은 [공통 준비 안내](../../week04/lab/README.md)를 따른다. 같은 루트 `.venv`를 사용한다.

| 순서 | Notebook | 직접 구현·비교 |
|---|---|---|
| 01 | [통계 기반 검색](notebooks/01_lexical_search.ipynb) | 토큰화, TF·DF·IDF, 코사인, BM25 빈도 포화·길이 보정 |
| 02 | [순위 결합·재정렬](notebooks/02_fusion_reranking.ipynb) | RRF 수동 계산, 점수 합산의 함정, 후보 수, 규칙 재정렬·중복 제거 |
| 03 | [검색 실험](notebooks/03_search_experiments.ipynb) | 개발 질의, 한 변수 비교, 테스트 고정, 실패 사례, 실제 검색 시간 |
| 04 | [서비스·프로젝트](notebooks/04_service_project.ipynb) | API 검증, 잘못된 입력, 글쓰기 평가 기준, 요구사항·로드맵 연결 |

4개 notebook × 34셀, 각 코드 셀의 값과 데이터를 직접 바꾸는 10개 확장 실험을 포함한다.
01–03 기본 실험을 수업에서 진행하고 추가 실험·프로젝트 적용은 자율 실습으로 이어간다.

```bash
python -m uvicorn week05.lab.search05.main:app --host 127.0.0.1 --port 8005
python -m pytest -q course_labs/tests
```

`http://127.0.0.1:8005`에서 BM25 / TF-IDF / RRF를 비교한다.
동의어 확장·규칙 재정렬은 한 번에 하나씩 변경한다. 규칙 재정렬은 학습된 cross-encoder가 아니다.
16질의 평가는 사례별 역할·날짜를 고정한다. 날짜·역할 설정을 바꾼 실험은 개별 검색에서 확인한다.
Recall/MRR은 정답 문서 회수·순위 지표이며 답변 정확도·서비스 성공률이 아니다.
기본 corpus가 작으므로 질의 세트에서 1.0을 얻어도 실서비스 일반화 성능을 주장할 수 없다.

개발용 질의로 설정을 선택한 뒤 테스트 질의는 마지막에 한 번 평가한다.
테스트 결과를 보고 설정을 다시 바꾸었다면 그 질의는 더 이상 미사용 테스트셋이 아니다.

전체 notebook 실행 검증(교수자·개발자용):

```bash
python scripts/verify_retrieval_notebooks.py
```

출력은 Git에서 제외된 `output/validation/`에 저장된다. 학생의 개인정보·실제 고객 데이터는 공개 저장소에 넣지 않는다.
