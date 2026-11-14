# 12주차 검증 기록

검증일: 2026-11-14. macOS arm64, Python 3.11.14, 로컬 Ollama, Chrome headless에서 확인했습니다.

| 범위 | 결과 |
|---|---|
| API·분석 자동 테스트 | **24 passed**. 고정 배정, 설정 버전, SRM/SciPy 대조, 구간 대칭·경계, 데이터 누락·모순, 중간 종료, 반복 확인, 중복 요청·409·422·503, 피드백, 복구, 혼합 provider, 처리 중 지표·제어 상태 |
| Notebook | **5개 / 114셀 / 코드 셀 38개**, 각각 새 커널에서 순서대로 실행. 오류 0. 공개 Notebook에는 실행 결과·로컬 경로 미포함 |
| 실제 모델 | Ollama `qwen2.5:1.5b-instruct` A/B 호출 성공. 원문·토큰·실행 시간·종료 이유 기록. B의 `length` 종료는 품질 재검증 사례로 명시 |
| 의존성 | 기존 고정 profile 재사용, `pip check` 통과. 학생용·선택 개발용 profile resolver 확인 |
| 소스 정적 검사 | 실습 Python 모듈 `ruff --select F` 통과 |
| HTML 장표 | 64장 모두 경계·하단 넘침 검사 통과. JavaScript 오류 0. 키보드·목차·그림 확대·노트·표본 수 조작 확인 |
| 반응형 | 390 / 768 / 1024px에서 64장 가로 넘침 0. 무JavaScript에서도 64장 내용 유지 |
| 발표자 모드 | HTTP와 로컬 파일 양쪽에서 64장 양방향 동기화, 현재·다음 미리보기, 학생 창 노트 숨김, 전체화면, 창 격리, 재연결, 글씨 크기, 드래그 비율·키보드·저장·복원 확인 |
| 학생 PDF | **64페이지**, 모든 페이지 제목이 HTML manifest와 일치. 노트·버튼 제외. 64쪽 렌더와 전체 contact sheet, 주요 도식·숫자·화면 상세 확인 |
| 과제·보고서 | 초안 저장·복원, 작성 메모만 HTML 저장·재열기, 입력 escape, 3개 시나리오 전환, 원본 JSON 다운로드, 작성 메모의 한 페이지 PDF 인쇄 확인, 모바일 넘침 0 |
| 공개 자료 범위 | 합성 CSV·실습 ID·교수의 정책 예시만 포함. 실제 서비스 DB·학생 작성 결과·검증 출력은 Git 제외 |

## 확인된 계산

- A 1196명 / B 1204명, 정상 SRM p = 0.870282772.
- 해결 확인율 A 55.0167%, B 64.0365%; B − A **+9.0198%p**.
- Newcombe–Wilson 95% 구간 **[5.0951, 12.9059]%p**.
- `healthy`: B p95 1147ms → REVIEW.
- `slow`: B p95 2868ms > 1800ms → HOLD.
- `srm`: B 602명 누락, p ≈ 1.38×10⁻⁴⁴ → INVALID, 효과 계산 중지.
- 반복 확인 시뮬레이션: 시드 12, 500회. 최종 한 번 3.6%, 14번 중 한 번이라도 17.6%. 이 시뮬레이션의 값이며 일반 상수 아님.

## 검증의 경계

실제 고객 A/B 실험, 운영 플랫폼 부하·인증·장애 복구, Windows/Linux 실기 검증, 장기 효과·순차 검정은 이 기록의 범위가 아닙니다. 로컬 서버는 수업용이며 API 인증을 구성하지 않았습니다. 웹 응답 성공을 노출 대리 지표로 쓰므로 실제 제품에서는 클라이언트 렌더 이벤트를 추가해야 합니다.

합성 성과와 실제 Ollama 출력은 별개입니다. 현재 작은 모델의 B 답변을 온라인 고객 실험에 바로 투입해도 된다는 결론을 내리지 않습니다.

## 재검증

```bash
python -m pip install -r requirements/week12-dev.txt
python -m pytest week12/lab/tests -q
python scripts/verify_week12_notebooks.py
node scripts/verify_week12_browser.mjs
node scripts/verify_week12_presenter.mjs
node scripts/verify_week12_materials.mjs
```

Node 검증은 `scripts/node_modules`의 Playwright와 Chrome을 사용합니다. 공개 학생 자료는 이 제작 도구 설치 없이 열립니다. 상세 영수증·스크린샷·실행 결과는 로컬 `output/validation/week12*`에 보존하며 공개 저장소에는 포함하지 않습니다.
