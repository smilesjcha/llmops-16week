"""Update the standalone assignment while retaining its accessible memo editor."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'week12/assignment/index.html'
old = p.read_text()
css = old.split('<style>')[1].split('</style>')[0]
if 'pre.mission-code' not in css:
    css += '\npre.mission-code{white-space:pre-wrap;overflow-wrap:anywhere;padding:20px;background:var(--wash);font-size:15px}code{overflow-wrap:anywhere}\n'
js = old.split('<script>')[1].split('</script>')[0]
js = js.replace("'next','limits']", "'next','limits','plan']")
js = js.replace('llmops.w12.assignment.draft.v1', 'llmops.w12.langfuse-mission.draft.v2')
js = js.replace('week12-deployment-decision.html', 'week12-langfuse-mission.html')
js = js.replace("clone.querySelector('header').remove()", "clone.querySelector('header')?.remove()")
body = '''
<header><p class="eyebrow">LLMOPS / WEEK 12 / 9–12주차 통합 과제</p>
<h1>Langfuse로 확인하는<br>상담 AI 개선 미션</h1>
<p class="lead">질문 2개, 프롬프트 2개.<br>실제 응답과 평가 기록을 보고 다음 변경을 제안합니다.</p>
<p>모든 수강생이 로그인 없이 읽는 공개 안내입니다. 기존 11주차 Langfuse·Ollama 환경을 재사용합니다.</p>
<nav class="links"><a href="#task">미션</a><a href="#setup">실행 준비</a><a href="#submit">제출 안내</a><a href="#memo">작성 양식</a><a href="../lecture/#slide-64">강의 마지막 장</a></nav>
<div class="summary"><div><strong>60–90분</strong>설치 완료 후 예상 소요</div><div><strong>Notebook 1개</strong>코드 셀 8개 · 실제 요청 4건</div><div><strong>12월 4일 23:59</strong>금요일 · 한국시간 · LMS 최대 5회</div></div></header>
<main><section id="task"><h2>1. 미션 · 새 답변을 시험해도 될까?</h2>
<p><strong>교환 정책 질문과 실시간 재고 질문, 총 2개를 두 프롬프트로 실행하고 Langfuse의 Trace와 Scores를 근거로 개선안을 작성합니다.</strong> B가 더 좋아져야 하는 과제가 아닙니다. 잘못된 응답·평가자의 오판·지연을 발견하고 근거로 설명하는 것이 목표입니다.</p>
<ol><li><strong>실제 응답 4건</strong> — 같은 질문을 A baseline, B grounded에 각각 입력합니다. 모델·검색기는 같고 프롬프트만 다릅니다. 답변 생성 4회 + 모델 평가 4회, 총 8번의 Ollama 호출입니다.</li>
<li><strong>흐름과 평가 확인</strong> — 검색 근거 → 생성 입력·출력 → 코드 검사 → 모델 평가를 확인하고 개별 생성 시간·점수를 비교합니다.</li>
<li><strong>사람 검토와 판단</strong> — B의 재고 답변을 직접 읽고 사람 검토 점수와 이유를 기록합니다. 보류 또는 추가 검토 판단과 다음 변경 하나를 설명합니다.</li>
<li><strong>사용자 A/B 계획</strong> — 고정 배정을 확인하고 대상·지표와 분모·보호 기준·기간·중단 규칙을 설계합니다. 실제 사용자 모집이나 온라인 실험 수행은 요구하지 않습니다.</li></ol>
<div class="callout"><strong>판단 메모 1–2쪽(PDF 또는 HTML) + 근거 화면 2장</strong>을 제출합니다. 캡처는 메모 안이나 별도 파일로 넣어도 됩니다. 네 요청으로 일반 정확도·p95·사용자 개선을 입증했다고 쓰지 않습니다.</div>
<nav class="links"><a href="https://github.com/smilesjcha/llmops-16week/blob/main/week12/assignment/01_langfuse_mission.ipynb">과제 Notebook 열기</a><a href="https://github.com/smilesjcha/llmops-16week/blob/main/week12/assignment/README.md">GitHub 실행 안내</a></nav></section>
<section id="setup"><h2>2. VS Code 실행 순서</h2>
<p>Python 3.11의 기존 .venv 커널을 선택합니다. Docker Desktop과 Ollama를 실행하고 저장소 루트의 터미널에서 아래를 진행합니다. 기존 환경은 재사용합니다.</p>
<pre class="mission-code"><code>python -m pip install -r requirements/week12-langfuse.txt
python week11/lab/langfuse/init_env.py
ollama pull qwen2.5:1.5b-instruct
docker compose -f week11/lab/langfuse/compose.yaml up -d --wait --wait-timeout 300</code></pre>
<p><a href="http://localhost:3011">내 PC의 Langfuse</a>에서 <code>week11/lab/langfuse/.env</code>의 로그인 계정으로 접속합니다. 첫 설치의 다운로드 시간은 별도입니다. <a href="https://github.com/smilesjcha/llmops-16week/blob/main/week11/lab/langfuse/README.md">최초 설치·메모리 요구·문제 해결</a></p>
<div class="table-wrap"><table><thead><tr><th>코드 셀</th><th>실행</th><th>확인 결과</th></tr></thead><tbody>
<tr><td>1–2</td><td>연결·비교 조건</td><td>모델·세션 ID, 질문·응답 계약</td></tr>
<tr><td>3–4</td><td>A/B 실제 응답</td><td>질문 2개 × 버전 2개의 Trace 링크</td></tr>
<tr><td>5</td><td>서버 저장·비교표</td><td>요청별 부모 1개 + 하위 작업 4개, Scores·지연</td></tr>
<tr><td>6</td><td>사람 검토</td><td>REVIEW·COMMENT 직접 입력, human_review 저장</td></tr>
<tr><td>7</td><td>고정 배정·계획</td><td>같은 가상 ID에 같은 버전, 본인 계획 5항목</td></tr>
<tr><td>8</td><td>증거 저장</td><td>로컬 evidence.json·comparison.csv</td></tr>
</tbody></table></div><p class="small">코드 셀은 실행 횟수 [1], [2]가 아니라 코드 셀만 센 순서입니다. 별도 API 서버·Prometheus 설치는 추가로 요구하지 않습니다. 9주차의 요청·응답 계약은 Ollama HTTP 호출과 JSON 필드에서 확인합니다.</p></section>
<section id="screens"><h2>3. Langfuse에서 확인할 두 화면</h2>
<ol><li><strong>Trace 트리와 입출력</strong> — 셀 5의 B Q24a 링크 → <code>01-retrieval</code> Output → <code>02-ollama-answer</code> Input/Output. 근거 없는 재고 단정이나 기권 필드와 문장의 불일치를 확인합니다. 화면 1장 캡처.</li>
<li><strong>Scores와 비교 근거</strong> — 같은 요청의 Scores → 코드 검사·<code>llm_groundedness</code>·직접 작성한 <code>human_review</code>와 이유 비교. Scores 또는 A/B 비교표 화면 1장 캡처하고 메모에 평가 종류의 차이를 설명합니다.</li></ol>
<p>Trace는 요청 전체, Span/Observation은 내부 작업, Generation은 모델 호출 기록입니다. Score는 특정 기준의 평가값입니다. 코드 통과는 의미 정확도 100%가 아니며 작은 모델의 자기 평가도 독립된 정답이 아닙니다. <a href="https://langfuse.com/docs/observability/data-model">공식 개념</a> · <a href="https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk">Scores 기록 방식</a></p>
<p class="small">저장은 비동기이므로 셀 5·6의 재조회 후 새로고침합니다. w12-mission 세션으로 이번 실행을 찾습니다. 환경 이름 week11-local은 기존 환경 재사용에 따른 정상 표시입니다. localhost 링크는 교수 PC에서 열리지 않으므로 캡처를 제출하세요.</p></section>
<section id="criteria"><h2>4. 9–12주차 연결과 평가 기준</h2>
<div class="table-wrap"><table><thead><tr><th>기준</th><th>답안에 담을 내용</th><th>점수</th></tr></thead><tbody>
<tr><td>9·10주차 · 실행 근거</td><td>요청·응답 계약·Trace 단계·개별 생성 지연</td><td>30</td></tr>
<tr><td>11주차 · 품질 판단</td><td>A/B 원문과 코드·모델·사람 평가의 구체적 비교</td><td>30</td></tr>
<tr><td>12주차 · 실험 설계</td><td>고정 배정·지표·전체 진입자 분모·보호·기간·중단</td><td>25</td></tr>
<tr><td>결론과 전달</td><td>보류/검토 근거, 다음 변경 하나, 읽기 쉬운 메모·캡처</td><td>15</td></tr>
</tbody></table></div><p>실패를 발견하고 원인을 구분해도 좋은 수행입니다. 개별 요청 시간은 관찰 사실이고 사용자 효과는 아직 실행하지 않은 계획입니다. 생성형 AI의 도움을 받은 범위와 직접 검증한 부분도 한 줄로 남깁니다.</p></section>
<section id="submit"><h2>5. 제출 안내</h2>
<p><strong>2026년 12월 4일(금) 23:59, 한국시간(KST)</strong>까지 제출합니다. 11월 20일 수업 기준 2주이며 기존 11월 27일 안내를 대체합니다.</p>
<ul><li><strong>아주대AI대학원</strong>: <a href="https://eclass2.ajou.ac.kr/ultra/courses/_118756_1/assessment/Test/_2542055_1?gradeitemView=details">LMS 과제 바로가기</a> → 과제출제/제출 → ‘12주차 과제03 · Langfuse 상담 AI 개선 미션’. <strong>제출 시도 최대 5회</strong>, 마감 전 수정본 제출 가능.</li><li><strong>군산대·국립창원대 및 그 외 수강생</strong>: 같은 기한까지 공지된 교수 이메일로 개인 제출.</li></ul>
<p><strong>판단 메모 1–2쪽 PDF/HTML + 근거 화면 2장</strong>. HWP/HWPX 제외. Notebook·JSON은 선택 첨부입니다. 아래 저장/인쇄 기능은 파일을 만드는 기능이며 자동 제출하지 않습니다.</p>
<p>설치가 끝내 해결되지 않으면 오류·해결 시도와 <a href="https://smilesjcha.github.io/llmops-16week/week11/lab/sample/langfuse/">공개 실제 실행 예시</a>로 분석한 범위를 구분해 제출합니다. 예시를 본인의 실행으로 표시하지 않으며 예시 분석만으로 직접 실행 항목이 충족되지는 않습니다.</p>
<p class="small">API 키·.env·비밀번호·다른 사람의 정보는 제출물과 공개 GitHub에 올리지 않습니다.</p></section>
<section id="memo"><h2>Langfuse 미션 · 판단 메모</h2><p class="print-hint">각 항목은 2–4문장으로 간결하게 작성합니다. HTML 저장 또는 메모 인쇄/PDF 후 근거 화면 2장을 첨부하세요.</p>
<form id="memo-form"><label for="topic">제목</label><input id="topic" value="상담 AI 프롬프트 개선 검토" maxlength="120">
<label for="decision">1. 결론 · 보류 / 추가 검토와 이유</label><textarea id="decision" placeholder="무엇을 확인했고 어느 단계까지 진행할 수 있나요?"></textarea>
<label for="api">2. 실행 근거 · 요청과 Trace</label><textarea id="api" placeholder="질문·버전·Trace ID, 입력/출력 계약, 작업 단계와 생성 시간"></textarea>
<label for="evidence">3. 품질 비교 · 코드 / 모델 / 사람 평가</label><textarea id="evidence" placeholder="A/B의 구체적인 답변 차이, Scores와 직접 읽은 근거"></textarea>
<label for="next">4. 다음 변경 하나와 재검증</label><textarea id="next" placeholder="바꿀 것 하나와 같은 질문으로 다시 확인할 기준"></textarea>
<label for="plan">5. 사용자 A/B 실험 계획</label><textarea id="plan" placeholder="대상·배정 / 지표와 분모 / 보호 기준 / 기간·종료 / 해석 범위"></textarea>
<label for="limits">6. 확인 범위와 한계</label><textarea id="limits" placeholder="실제 수행·미실행 범위, 작은 문항 수·자기 평가의 한계, AI 활용 범위"></textarea></form>
<div class="links actions"><button class="primary" id="save-html">작성 메모 HTML 저장</button><button id="print-memo">메모 인쇄 / PDF</button></div><p id="saved" role="status">초안은 이 브라우저에만 저장됩니다. 자동 제출되지 않습니다.</p></section>
</main><footer>LLMOps 16주 과정 · 2026-11-20 개정 · 공개 안내 / 제출은 LMS 또는 이메일</footer>
'''
p.write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>12주차 과제 | Langfuse 상담 AI 개선 미션</title><style>'+css+'</style></head><body>'+body+'<script>'+js+'</script></body></html>')
print('Built standalone Langfuse mission and memo editor')
