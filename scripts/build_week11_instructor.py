"""Build a static, searchable lecturer handbook from authored page/cell notes."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'week11/lecture/instructor'
OUT.mkdir(exist_ok=True)
notes = json.loads((OUT.parent/'teaching-notes.json').read_text())
cells = json.loads((ROOT/'week11/lab/instructor-notes.json').read_text())
manifest = json.loads((OUT.parent/'slide-manifest.json').read_text())
steps = json.loads((ROOT/'week11/lab/notebook-steps.json').read_text())
assert len(notes) == 64 and len(cells) == 18
for i, note in enumerate(notes, 1):
    assert note['page'] == i and note['title'] == manifest[i-1]['title'].replace('<br>', ' ')
for book in ('09', '10'):
    assert [c['cell'] for c in cells if c['notebook'] == book] == list(range(1, 10))
H = html.escape
chapters = [
    ('수업 안내',1,6,'서비스의 어느 단계를 관찰하고, 무엇으로 변경을 판단할 것인가'),
    ('평가 기준',7,12,'사용자 성공 조건을 근거·문서 버전·평가 데이터로 정의'),
    ('검색 비교',13,20,'같은 질문과 한 요소 변경으로 검색 지표의 의미 확인'),
    ('실패 분석',21,27,'검색 성공·답변 가능·기권을 구분해 다음 실험 선택'),
    ('실제 LLM 응답',28,32,'실제 입력·출력과 기권·인용 상태를 함께 확인'),
    ('답변 평가',33,38,'코드·모델·사람의 역할 분리와 평가자 오류 검토'),
    ('LLMOps 도구',39,42,'제품 이름보다 요청 추적·실험 비교·검토 기능 이해'),
    ('Langfuse 실습',43,54,'09 요청 추적 → 10 A/B/C 실험 → 보류 또는 추가 검토'),
    ('배포 판단',55,64,'자동 조건의 결과·한계·다음 조치를 근거와 함께 기록'),
]


def table(headers, rows, cls=''):
    return '<div class="table-scroll"><table class="'+cls+'"><thead><tr>'+''.join('<th scope="col">'+H(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'


def block(label, value, cls=''):
    return f'<section class="note-block {cls}"><h4>{H(label)}</h4><p>{H(value)}</p></section>'

parts = ['''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="11주차 교수용 강의 준비: 64쪽 핵심 메시지·설명 예시·확인 질문, 09·10번 Notebook 18개 코드 셀의 시연과 수업 안내.">
<title>11주차 강의 준비 | 64쪽 요약 · 09·10 셀별 설명</title><link rel="stylesheet" href="handbook.css"></head><body>
<a class="skip" href="#overview">본문으로 이동</a><header class="masthead"><a href="../index.html">11주차 강의안</a><span>교수용 준비 자료 · 64쪽 / 코드 셀 18개</span></header>
<main><header class="intro"><h1>11주차 강의 준비</h1><p class="lead">실패를 추적하고, 같은 질문으로 변경을 비교한 뒤,<br>배포 전 판단의 근거를 설명하는 수업.</p>
<p>장표에는 핵심을, 설명 노트에는 이유와 사례를 담았습니다. 먼저 목차별 한 문장으로 흐름을 파악하고, 필요한 페이지 또는 코드 셀을 펼쳐 설명 예시와 확인 질문을 읽으세요.</p>
<div class="start-links"><a href="#overview">64쪽 한눈에 보기</a><a href="#notebook-09">09번 셀별 설명</a><a href="#notebook-10">10번 셀별 설명</a></div></header>
<nav class="local-nav" aria-label="강의 준비 목차"><a href="#runbook">100분 진행</a><a href="#concepts">개념과 비교 기준</a><a href="#overview">페이지별 핵심</a><a href="#page-notes">페이지별 설명</a><a href="#cells">셀별 설명</a></nav>
<section id="runbook"><h2>100분 진행과 시간 배분</h2><p>64쪽을 같은 속도로 읽지 않습니다. 검색 계산 심화는 복습으로 두고, <strong>09번 20분·10번 25분</strong>을 확보합니다. 모델·Docker 이미지는 수업 전에 준비합니다.</p>''']
parts.append(table(['시간','장표','교수 진행','학생의 확인 결과'],[
    ['0–10분','1–6, 43 예고','상담 AI 변경의 성공 조건·실패 사례 예상','요청 성공과 답변 품질의 차이'],
    ['10–25분','7–27 발췌','7·8·10·11·15·16·21·23·25·26 중심. 나머지는 복습 연결','검색됨과 답변 가능함의 차이'],
    ['25–40분','28–42 발췌','29·30·31·33·36·39·42 중심. 07·08은 실행 결과 설명','형식 검사와 의미 판정의 역할'],
    ['40–60분','43–48 / 09번','코드 셀 1–5 우선. 6은 경계 비교, 7은 한 사례 직접 검토, 8–9는 저장·정리','실제 입력·출력·Scores를 읽고 원인 설명'],
    ['60–85분','49–54 / 10번','1–3 준비 → 4·5·6 A/B/C → 7 비교 → 8·9 검증·저장','HOLD/REVIEW의 조건과 실제 근거'],
    ['85–100분','55–64 발췌','55·57·58·62·63 중심. 56은 선택 심화, 59–61은 결과 확인','판단 한 문장 + 증거 하나 + 다음 조치'],
]))
parts.append('''<div class="aside-note"><strong>시간이 밀릴 때</strong><p>09번 최소 SDK 셀 2는 교수 시연으로 짧게 읽고 전체 요청 셀 3–5에 집중합니다. 10번은 모델 실행 중 판단 기준을 설명하고 A/B/C 비교 시간을 유지합니다. 설치·연결 문제는 별도 복구하고 <a href="../../lab/sample/langfuse/">검증된 실행 예시</a>로 분석 활동에 먼저 참여합니다. 예시와 학생의 실제 실행 결과는 구분합니다.</p></div>
<p><a href="../../lab/langfuse/README.md">Docker·모델 준비</a> · <a href="../../lab/demo/#notebooks">실행 순서·화면 클릭 안내</a> · <a href="../../lab/WALKTHROUGH.md">전체 Notebook 실행 안내</a></p>
<h3>학생용 화면과 발표자 노트의 분리</h3><ol><li><a href="../index.html" target="_blank" rel="noopener">강의안</a> 하단의 <strong>발표자 모드</strong>를 눌러 교수용 창을 엽니다.</li><li>교수용 창에 ‘강의 창과 동기화 중’이 보이면 공유하지 않는 모니터나 별도 창에 둡니다.</li><li>원래 강의 창에서 <strong>P / 전체 화면</strong>을 누르고, 온라인 수업에서는 <strong>강의 창만 공유</strong>합니다.</li><li>어느 창에서 넘겨도 현재 장표와 노트가 함께 바뀝니다. 교수용 창의 번호·목차·도식 단계 버튼도 사용할 수 있습니다.</li></ol><p class="fine">전체 데스크톱을 공유하면 노트 창도 보일 수 있습니다. 발표자 모드에서는 강의 화면의 노트를 잠그며 N도 별도 창으로 연결됩니다. 팝업이 차단되면 허용 후 다시 누르세요. 발표자 모드를 종료한 일반 보기에서는 기존 N 노트가 화면에 표시됩니다.</p></section>
<section id="concepts"><h2>먼저 설명할 개념</h2><p>“상담 요청 한 건을 처리하는 기록”으로 시작하면 용어를 연결하기 쉽습니다. LLMOps는 Large Language Model Operations, 대규모 언어 모델 기반 서비스의 개발·평가·배포·운영을 다루는 활동입니다.</p>''')
parts.append(table(['용어','학생에게 할 설명','이번 실습에서 확인할 곳'],[
 ['Trace · 요청 전체 기록','상담 요청 한 건에서 일어난 작업을 연결해 보는 전체 기록','09 코드 셀 3의 Q03a 요청 링크'],
 ['Span · 작업 구간','검색·검사처럼 시작과 끝을 가진 작업 하나. 부모·자식 관계로 연결','Tree의 루트와 하위 작업'],
 ['Observation · 관찰 기록','Langfuse가 기록하는 작업 단위. span·retriever·generation 등 유형을 구분','01-retrieval, 02-ollama-answer 등'],
 ['Generation · 모델 호출 기록','답변 생성뿐 아니라 모델을 이용한 평가 호출도 generation','02-ollama-answer와 04-ollama-judge'],
 ['Scores · 평가 결과','실행에 붙이는 코드·모델·사람의 평가 결과. 이름·타입·기준·이유를 함께 읽기','루트 Scores의 코드 검사와 llm_groundedness'],
 ['Dataset · 평가 데이터셋','다시 실행할 질문과 기대 행동을 버전으로 고정한 목록','10 코드 셀 3: 정상 3개 + 경계 1개'],
 ['Experiment · 비교 실험','고정 데이터에 특정 모델·프롬프트·서비스 설정을 실행한 결과 묶음','10 코드 셀 4–6의 A/B/C'],
 ['RAG · Retrieval-Augmented Generation','검색 증강 생성. 자료를 찾고 그 근거와 질문을 모델에 전달','retrieval Output → answer Input'],
 ['SDK · Software Development Kit','기록 전송을 코드에서 쉽게 호출하는 개발 도구 모음','lf.start_as_current_observation, lf.create_score'],
]))
parts.append('''<p class="fine">개념 출처: <a href="https://opentelemetry.io/docs/concepts/signals/traces/">OpenTelemetry의 Trace·Span</a>, <a href="https://langfuse.com/docs/observability/overview">Langfuse Observability</a>, <a href="https://langfuse.com/docs/evaluation/core-concepts">평가와 Scores</a>. 구체적인 작업 수와 점수 이름은 이 수업의 구현입니다.</p>
<figure class="trace-example"><figcaption>09번 전체 요청: 한 Trace 안의 실제 작업</figcaption><pre>rag-Q03a-grounded                 요청 전체를 묶는 부모 작업
├─ 01-retrieval                   문서 검색 · retriever
├─ 02-ollama-answer               답변 생성 · generation
├─ 03-code-checks                 인용·기권 검사 · evaluator
└─ 04-ollama-judge                모델 평가 · generation

Scores: 위 실행을 평가한 결과. 작업 트리의 단계와는 별도.</pre></figure>
<h3>Scores를 읽는 순서</h3><p>먼저 검사 이름과 적용 대상을 읽고, 통과 여부와 판단 이유를 봅니다. 마지막에 실제 답변과 근거를 대조합니다. <strong>점수 1은 그 검사 통과이지 답변 정확도 100%가 아닙니다.</strong></p>''')
parts.append(table(['이름','무엇을 검사하는가','주의할 점'],[
 ['citations_in_context','인용 ID가 검색 문서 안에 존재하는가','문서 내용이 주장을 뒷받침하는지까지 보장하지 않음'],
 ['decision_matches_reference','기권 여부가 평가 기준의 답변 가능 여부와 맞는가','정답 라벨은 평가에 사용. 생성·C 정책 분기의 입력으로 쓰지 않음'],
 ['required_evidence_cited','답변 가능한 질문에서 필수 문서 ID를 모두 인용했는가','답변 불가 질문은 적용하지 않음(None). 누락 점수를 0점으로 해석하지 않음'],
 ['llm_groundedness','모델이 답변과 근거를 대조한 범주형 판정','같은 작은 모델의 자기 평가. 오판 가능'],
 ['human_review','실제로 읽은 사람이 남긴 판단과 이유','09 셀 7에서 직접 입력해야 생성. None은 미실행'],
 ['structural_pass','적용되는 인용·기권 계약 검사가 모두 통과했는가','10번의 회귀 문항 4개에 대한 검사. 의미 정확도가 아님'],
 ['false_accept','답변 불가 질문을 정상 답변으로 수락했는가','재고 질문 1개만 해당. 정상 3개에는 미적용'],
 ['generation_ms','클라이언트가 관측한 답변 생성 호출 시간','정책으로 모델 미호출이면 0. 모델 성능 향상과 구분'],
]))
parts.append('''<h3>A/B/C: 변경한 요소와 확인할 가설</h3>''')
parts.append(table(['버전','변경','학생에게 던질 가설','실행 범위'],[
 ['A · 기준선','기본 프롬프트','근거가 없는 재고 질문에도 단정해서 답할까?','네 질문 모두 실제 생성·모델 평가'],
 ['B · 프롬프트','같은 모델·데이터, 근거 중심 지시','지시를 바꾸면 문장·인용·기권 상태가 함께 개선될까?','네 질문 모두 실제 생성·모델 평가'],
 ['C · 기능 정책','B + requested_capability의 지원 여부 확인','없는 기능을 명시적으로 제한하면 실패를 막으면서 정상 질문을 유지할까?','정상 3개 실제 모델. 재고 1개는 정책 응답'],
]))
parts.append('''<p>이 비교는 고정 질문의 오프라인 실험입니다. 온라인 사용자 A/B 테스트가 아닙니다. C는 <code>policy_qa</code>와 <code>live_inventory</code>라는 명시된 요청 기능을 확인합니다. 자유 문장의 의도 분류나 실시간 재고 API는 구현하지 않았습니다.</p>
<h3>HOLD와 REVIEW: 자동 판정의 다음 행동</h3>''')
parts.append(table(['결과','정확한 의미','교수 설명 예시','다음 행동'],[
 ['HOLD · 보류','필수 조건 실패, 서로 다른 데이터, 누락·실패한 실행 등','“지시를 고쳤지만 재고를 알 수 없는 요청을 수락했습니다. 이 변경은 보류합니다.”','실패 checks와 원본 trace 확인 → 원인 수정 → 같은 데이터 재평가'],
 ['REVIEW · 검토 대기','자동 조건은 통과했으며 사람 검토로 이동','“C는 네 사례의 계약 검사를 통과했습니다. 실제 내용과 추가 경계 사례를 확인하겠습니다.”','의미 품질·위험·범위 검토 → 별도 승인 판단'],
]))
parts.append('''<p><strong>둘 다 자동 배포 승인이 아닙니다.</strong> 이 이름과 기준은 <a href="https://github.com/smilesjcha/llmops-16week/blob/main/week11/lab/release_lab.py">수업의 release_decision 함수</a>가 정의한 정책이며 Langfuse의 내장 승인 상태가 아닙니다.</p>
<ol class="policy"><li>같은 데이터셋의 네 질문이 빠짐없이 정상 실행됐는지 확인</li><li>답변 불가 수락 0건, 적용되는 계약 검사 통과율 100%</li><li>기준선 대비 계약 검사 통과율 저하 없음</li><li>단일 생성 호출의 최대 시간 3000ms 이하</li><li>모든 조건을 통과하면 REVIEW, 그렇지 않으면 HOLD</li></ol>
<p>3000ms는 결과를 보기 전에 정한 수업용 예산입니다. 실제 제품에서는 요구사항에 맞춰 정합니다. 여기서 최대 시간은 네 요청 중 최댓값이며 p95라고 부르지 않습니다.</p>
<div class="aside-note"><strong>이름이 비슷한 두 REVIEW</strong><p>09 코드 셀 7의 <code>REVIEW</code>는 사람이 입력하는 평가 변수(<code>supported</code>·<code>unsupported</code>·<code>needs_review</code>)입니다. 10 코드 셀 7의 <code>"REVIEW"</code>는 자동 조건을 통과한 뒤의 검토 대기 상태입니다.</p></div>
<h3>예상과 다른 결과가 나왔을 때</h3><p>공개 예시에서는 A·B의 계약 통과율이 75%, C가 100%였고 B는 HOLD, C는 REVIEW였습니다. 학생 실행에서는 답변·판정·지연이 달라질 수 있습니다. 좋은 결과가 나올 때까지 다시 돌리는 대신 <strong>현재 결과 → 실패 조건 → 원본 답변 → 다음 변경</strong> 순서로 설명합니다.</p>
</section><section id="overview"><h2>목차별 핵심과 64쪽 요약</h2><p>페이지 제목은 실제 장표와 일치합니다. ‘설명’은 아래의 수업 노트를 열고, ‘장표’는 해당 발표 페이지를 새 탭에서 엽니다.</p>''')
parts.append(table(['목차','페이지','이 구간에서 전달할 메시지'],[[H(c),f'<a href="#summary-{a}">{a:02d}–{b:02d}</a>',H(m)] for c,a,b,m in chapters]))
for name,start,end,message in chapters:
    parts.append(f'<section class="chapter-summary" id="summary-{start}"><h3>{start:02d}–{end:02d} · {H(name)}</h3><p>{H(message)}</p>')
    parts.append(table(['페이지 / 제목','핵심 한 문장','열기'],[[f'<span class="page-number">{n["page"]:02d}</span> {H(n["title"])}',H(n['message']),f'<a href="#page-{n["page"]}">설명</a> · <a href="../index.html#slide-{n["page"]}" target="_blank" rel="noopener">장표<span class="sr-only"> {n["page"]} 새 탭</span></a>'] for n in notes[start-1:end]],'summary-table'))
    parts.append('</section>')
parts.append('''</section><section id="page-notes"><h2>페이지별 교수 설명 노트</h2><p>설명 예시는 실제 수업에서 말할 수 있는 문장입니다. 그대로 읽기보다 자신의 사례와 학생의 반응에 맞게 조정하세요. ‘복습’·‘심화’ 페이지는 시간에 따라 짧게 연결합니다.</p>
<div class="tools js-only"><label for="search">노트 검색<input id="search" type="search" placeholder="예: 재고, HOLD, 09"></label><label for="priority">진행 구분<select id="priority"><option value="">전체</option><option value="핵심">핵심</option><option value="짧게">짧게</option><option value="복습">복습</option><option value="심화">심화</option></select></label><button id="expand">표시된 노트 펼치기</button><button id="collapse">모두 접기</button><button id="print">인쇄</button></div><p id="search-status" class="js-only" role="status" aria-live="polite"></p>''')
for name,start,end,message in chapters:
    parts.append(f'<section class="page-group"><h3>{start:02d}–{end:02d} · {H(name)}</h3>')
    for n in notes[start-1:end]:
        parts.append(f'<details class="page-note" id="page-{n["page"]}" data-priority="{H(n["priority"])}"><summary><span class="page-number">{n["page"]:02d}</span><span>{H(n["title"])}</span><small>{H(n["priority"])}</small></summary><div class="detail-body"><p class="takeaway">{H(n["message"])}</p>')
        for key,label in [('talk','설명 예시'),('point','화면에서 짚을 근거'),('question','학생 확인 질문'),('answer','기대 답변'),('caution','오해 방지'),('bridge','다음 내용 연결')]:
            parts.append(block(label,n[key]))
        parts.append(f'<p class="detail-links"><a href="../index.html#slide-{n["page"]}" target="_blank" rel="noopener">{n["page"]:02d}쪽 장표 열기</a> · <a href="#summary-{start}">이 구간 요약</a></p></div></details>')
    parts.append('</section>')
parts.append('''</section><section id="cells"><h2>09·10번 셀별 수업 안내</h2><p>아래 번호는 <strong>위에서부터 코드 셀만 세는 순서</strong>입니다. VS Code 왼쪽의 실행 횟수 <code>[숫자]</code>나 설명 제목의 단계 번호와 다릅니다. 각 파일의 첫 셀부터 한 개씩 실행합니다.</p>''')
for book in ('09','10'):
    group=[c for c in cells if c['notebook']==book]
    parts.append(f'<section id="notebook-{book}"><h3>{H(steps[book]["title"])}</h3><p><a href="https://github.com/smilesjcha/llmops-16week/blob/main/week11/lab/notebooks/{steps[book]["filename"]}">GitHub Notebook</a> · <a href="../../lab/demo/#notebooks">화면 클릭 안내</a></p>')
    parts.append(table(['코드 셀','학습 목적','관련 장표'],[[f'<a href="#cell-{book}-{c["cell"]}">{c["cell"]}. {H(c["title"])}</a>',H(c['intent']),', '.join(str(p) for p in c['slides'])] for c in group]))
    for c in group:
        parts.append(f'<details class="cell-note" id="cell-{book}-{c["cell"]}"><summary><span class="page-number">{book} / {c["cell"]}</span><span>{H(c["title"])}</span></summary><div class="detail-body"><p class="takeaway">{H(c["intent"])}</p>')
        for key,label in [('talk','학생에게 할 설명'),('screen','Langfuse·VS Code에서 누를 곳'),('result','확인할 결과'),('question','학생 확인 질문'),('answer','기대 답변'),('caution','오해·문제 해결')]:
            if key == 'screen' and ' → ' in c[key]:
                parts.append('<section class="note-block"><h4>'+H(label)+'</h4><ol>'+''.join('<li>'+H(step)+'</li>' for step in c[key].split(' → '))+'</ol></section>')
            else:
                parts.append(block(label,c[key]))
        parts.append('<p class="detail-links">연결 장표: '+', '.join(f'<a href="../index.html#slide-{p}" target="_blank" rel="noopener">{p:02d}쪽</a>' for p in c['slides'])+'</p></div></details>')
    parts.append('</section>')
parts.append('''</section><section id="closing"><h2>수업 마무리의 확인 질문</h2><ol><li>요청 트리에서 답변 생성과 모델 평가를 구분할 수 있는가?</li><li>코드 검사가 통과했어도 답변이 틀릴 수 있는 이유를 실제 근거로 설명할 수 있는가?</li><li>B와 C에서 바꾼 요소를 구분하고 HOLD 또는 REVIEW의 이유를 말할 수 있는가?</li><li>자기 프로젝트에 추가할 정상 질문과 경계 질문을 하나씩 정의할 수 있는가?</li></ol><p>학생에게 마지막으로 받을 답변은 <strong>판단 한 문장 · 근거 하나 · 다음 실험 하나</strong>입니다. 추가 과제나 제출 기한을 새로 부여하는 안내는 아닙니다.</p></section>
<footer><p><a href="../index.html">HTML 강의안</a> · <a href="../../lab/demo/">실습 시연 안내</a> · <a href="../lecture-notes.md">페이지별 원문 노트</a> · <a href="https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk">Langfuse SDK 실험 공식 문서</a></p><p>가상 쇼핑 정책 기반 수업 자료. 실제 기업 정책·학생 정보 없음. 실행 결과는 코드와 해당 실행의 범위에서 해석합니다.</p></footer></main><script src="handbook.js"></script></body></html>''')
(OUT/'index.html').write_text('\n'.join(parts),encoding='utf-8')
md=['# 11주차 강의 준비: 목차와 페이지별 핵심\n', '[검색·펼치기·셀별 설명이 있는 HTML 안내](https://smilesjcha.github.io/llmops-16week/week11/lecture/instructor/)\n']
for name,a,b,message in chapters:
    md += [f'## {a:02d}–{b:02d}. {name}\n',message+'\n','| 페이지 | 제목 | 핵심 메시지 |','|---|---|---|']
    md += [f'| {n["page"]:02d} | {n["title"]} | {n["message"]} |' for n in notes[a-1:b]]
    md.append('')
for book in ('09','10'):
    md += [f'## {book}번 코드 셀별 학습 목적\n','| 코드 셀 | 단계 | 학습 목적 |','|---|---|---|']
    md += [f'| {c["cell"]} | {c["title"]} | {c["intent"]} |' for c in cells if c['notebook']==book]
    md.append('')
(OUT.parent/'INSTRUCTOR_OVERVIEW.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(f'Built lecturer handbook: {len(notes)} pages, {len(cells)} code-cell guides')
