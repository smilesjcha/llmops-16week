# 4·5주차 검증 기록

검증 환경: macOS arm64 / CPython 3.11.14 / 저장소 루트 requirements.

- 기본 notebook8개를 각각 새 커널에서 전체 실행: 오류0건.
- 각 notebook34셀, 코드12셀. 전체272셀·코드96셀.
- 검색·원문 위치·중복 제거·날짜·권한·보류·지표·API 오류·재현성 테스트.
- 자동 테스트 11개 통과. 핵심 Python 파일 Ruff 검사 통과.
- 로컬 웹 화면 검색·16질의 평가 실행, 실제 캡처를 PPT에 반영.
- 기본 응답은 원문 발췌. 실제 LLM 생성·Pinecone·GPU 성능을 검증한 것으로 해석하지 않는다.
- 선택 Ollama 호출은 기본 스위치 OFF로 전체 실행 검증. 실제 모델 네트워크 실행은 별도 준비가 필요하다.
- 16질의 평가는 질의별로 지정된 역할·날짜를 고정한다. 화면의 역할·날짜는 개별 검색에 적용된다.

재검증: `python -m pytest -q course_labs/tests`, `python scripts/verify_retrieval_notebooks.py`.
실행 출력·임시 캡처·검수 자료는 `output/validation/`에 보관하며 공개 Git에서 제외한다.
