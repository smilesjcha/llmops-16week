# Week 01 검증 보고서

검증 기준일: 2026-09-04
검증 환경: macOS 26.6.2 arm64 · CPython 3.11.14 · `pytest 8.4.1`

## 결론

현재 `01_week1_llmops_kickoff.pptx`는 79장 구조, 79개 speaker notes와 79개 `[Sources]` block, 최소 14pt 가시 텍스트, 명사형·고유 제목, 41개 layout type, 검정·흰색·네이비·파랑 중심 색상, slide canvas overflow 0건을 확인했다. `TRACE/01` 로컬 API test는 4/4 통과했고, guided notebook 6개 code cell도 임시 trace store를 연결한 live server에서 오류 없이 실행했다.

최종 PPTX 이후 생성된 `final-render-v4`의 79개 PNG와 79장 전체 contact sheet, 교정 대상 장표의 full-size render를 함께 육안 검수했다.

## 현재 자동 검증 결과

| 영역 | 결과 | 확인 내용 |
|---|---|---|
| PowerPoint 구조 | PASS | final PPTX 79 slides |
| Speaker notes | PASS | 79 notes, 79 `[Sources]` open/close block, source 없는 slide 0건 |
| 가시 텍스트 크기 | PASS | builder instrument 기준 최소 14pt; 모든 visible text가 공통 text helper를 통과 |
| 제목 assertion | PASS | 제목 누락 0건, 중복 0건, 문장형 종결 패턴 0건 |
| Layout assertion | PASS | 41개 layout type, 동일 layout 3회 연속 0건 |
| 색상 정책 | PASS | black/white/navy/blue와 neutral grayscale만 사용; blue tint `#A9C6F8` 포함, 금지 orange `#FF5A36` 0건 |
| PowerPoint overflow | PASS | `slides_test.py`: overflow 0건 |
| PowerPoint portability | PASS | slide·notes XML의 `/Users/...` 절대 경로 0건 |
| 최종 render coverage | PASS | `final-render-v4`: 79 PNG, final PPTX 이후 생성 |
| API tests | PASS | `week01/lab/tests`: 4/4 통과 |
| Python format·lint | PASS | Ruff check·format check 통과, Python·notebook 7개 파일 format 일치 |
| Course material structure | PASS | 보존 notebook 16개·제작 notebook 1개, structural error 0건 |
| Dependency integrity | PASS | `uv pip check --python .venv/bin/python`: 123 packages compatible |
| 장별 육안 검수 | PASS | 79장 contact sheet 전수 검수 후 교정 장표 full-size 재검수 |
| Guided notebook 실행 | PASS | live server 기준 6 code cell, notebook error output 0건 |
| 실서비스 smoke | PASS | `/health`, `/`, `/api/v1/generate`, `/api/v1/traces`, `/api/v1/stats`, `/metrics` 확인; 선택 Ollama 경로의 503 복구 메시지 확인 |

## PowerPoint QA 근거

- Final deck: `week01/lecture/01_week1_llmops_kickoff.pptx`
- Builder·audit·manifest·render: `week01/lecture/build/v2/` 로컬 생성 임시 영역(git 제외)

Builder는 export 전에 다음을 강제한다.

- 정확히 79 slides
- visible text 14pt 미만 금지
- title 누락·중복·문장형 종결 금지
- notes 또는 source 누락 금지
- 동일 layout 3회 연속 금지

## 검증 명령

```bash
# Builder audit와 manifest
jq . week01/lecture/build/v2/build-audit.json
jq 'length' week01/lecture/build/v2/slide-manifest.json

# Final PPTX overflow
python "$PRESENTATIONS_SKILL_DIR/container_tools/slides_test.py" \
  week01/lecture/01_week1_llmops_kickoff.pptx

# TRACE/01 API tests
cd <repository-root>
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q -p no:cacheprovider week01/lab/tests
.venv/bin/ruff check week01/lab
.venv/bin/ruff format --check week01/lab
.venv/bin/python scripts/check_course_materials.py
uv pip check --python .venv/bin/python

# Guided notebook — port 8000 live server와 임시 trace store 사용
.venv/bin/jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.timeout=180 \
  --output-dir /tmp/trace01-notebook-qa \
  --output executed.ipynb \
  week01/lab/week01_trace01_lab.ipynb
```

최종 render 생성 명령은 다음과 같다.

```bash
python "$PRESENTATIONS_SKILL_DIR/container_tools/render_slides.py" \
  week01/lecture/01_week1_llmops_kickoff.pptx \
  --output_dir week01/lecture/build/v2/final-render-v4
```

## 개발환경 기준

- Python support range: `>=3.11,<3.12`
- Canonical classroom build: CPython `3.11.14`
- 기본 실습은 model download와 외부 credential 없이 동작하는 demo provider 사용
- `content_fingerprint`는 익명화가 아니라 동일 입력 비교용 식별자이므로 개인정보·기밀 원문을 실습 입력으로 사용하지 않음
- `token_estimate`는 tokenizer-backed billing value가 아닌 교육용 추정치

## 알려진 AS-IS 경고

보존 원본인 `practice/week02/02_advanced_reasoning.ipynb`의 code cell 20에는 닫히지 않은 문자열 1건이 있다. AS-IS 원본 상태를 숨기지 않기 위해 자동 수정하지 않는다.

## 수동 검증 경계

- Ollama model pull과 실제 sampling 비교
- OpenAI, Pinecone, Langfuse credential을 사용하는 외부 호출
- Hugging Face model 다운로드와 1-step SFT/DPO
- Linux/CUDA의 QLoRA와 `bitsandbytes` backend
- 실제 강의장 네트워크에서의 다중 사용자 부하 시험
