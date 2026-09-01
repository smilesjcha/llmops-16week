# 원본 및 가져오기 기록

이 디렉터리는 아주대학교 AI대학원 2025년 2학기 LLMOps 실습 저장소를 실행 결과까지 포함한 **AS-IS 스냅샷**으로 보존한다.

## 원본

- 저장소: <https://github.com/smilesjcha/ajou-llmops-2025-2nd-semester>
- 소유자: `smilesjcha`
- 기준 브랜치: `main`
- 기준 커밋: `554898da07d58b191066a94f37f0a9502138fe94`
- 기준 커밋 시각: `2025-12-01T18:56:54+09:00`
- 가져온 날짜: `2026-09-01` (Asia/Seoul)

원격 브랜치는 `main`과 `update/week1` 두 개다. 조사 시점의 `update/week1` 끝 커밋은 `90d24bc0843d1ab4f7e9cb9368a21da4eeb5735d`이며, 기준 커밋과 비교하면 실습 노트북·코드·데이터는 동일하고 원본 `README.md`만 다르다. 태그는 없다.

## 가져온 범위

다음 파일은 기준 커밋의 Git blob과 byte-for-byte 동일하게 복사했다.

- 루트 환경 파일: `.env.sample`, `.gitignore`, `poetry.lock`, `pyproject.toml`, `requirements-week01.txt`, `requirements.txt`
- Python 패키지 자리표시자: `src/`
- 강의 실습 자산: `week01/`–`week07/`, `week09/`–`week14/`
- 노트북 안에 저장된 출력, Week05 BM25 pickle, Week06 LoRA adapter와 `checkpoint-5`, CSV/JSON/JSONL 로그 및 결과

원본에 `week08/`, `week15/`, `week16/` 디렉터리나 노트북은 없다. 8주차와 16주차는 시험, 15주차는 Capstone 설계 워크숍으로 원본 강의계획서에 기재되어 있다.

## 제외한 항목

- Git 메타데이터: `.git/`
- 도구별 작업 설정: `.claude/`, `.mcp.json`, `CLAUDE.md`
- macOS 메타데이터: 모든 `.DS_Store`

이 디렉터리의 `README.md`와 `SOURCE.md`는 가져오기·실행 안내를 위해 새로 작성한 문서이므로 원본 Git blob 비교 대상이 아니다. 원본의 짧은 강의계획은 상위 디렉터리의 통합 강의 문서와 이 `README.md`의 주차별 표로 보존한다.

## 무결성

- 원본에서 선택한 파일: 78개
- 복사된 원본 파일: 78개
- Jupyter Notebook: 16개
- 복사된 78개 파일을 `git hash-object`로 원본 `main@554898d`의 blob ID와 대조했으며, 78개 모두 일치했다.
- 노트북은 실행하거나 출력 정리, 셀 재저장, 메타데이터 정규화를 하지 않았다.

## 라이선스

조사한 원본 커밋에는 `LICENSE`, `LICENSE.md`, `COPYING` 등 별도 라이선스 파일이 없다. 따라서 이 스냅샷만으로 제3자의 재사용·재배포 권한을 추정해서는 안 된다. 저장소 소유자의 자료 보존·이관 목적 외 사용에는 별도 권리 확인이 필요하다.
