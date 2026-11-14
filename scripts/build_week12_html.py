"""Build the authored Week 12 deck, previews and lecturer handbook."""
import ast
import base64
import html
import json
import math
from pathlib import Path

from week12_content import SOURCES, slides

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'week12/lecture'
H = html.escape
FIELDS = [('message','핵심 메시지'),('talk','설명 예시'),('point','화면 짚기'),('question','확인 질문'),('answer','기대 답변'),('caution','오해 방지'),('bridge','다음 연결')]
fonts = ''.join('@font-face{font-family:"Course Pretendard";font-weight:'+str(w)+';font-style:normal;font-display:swap;src:url(data:font/woff2;base64,'+base64.b64encode((P/'assets'/name).read_bytes()).decode()+') format("woff2");}' for w,name in [(400,'Pretendard-Regular.woff2'),(700,'Pretendard-Bold.woff2')])
css = (P/'deck.css').read_text()+fonts
# Keep the established Week 11 presenter controls verbatim; no execution of its builder.
tree = ast.parse((ROOT/'scripts/build_week11_html.py').read_text())
controls = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='controls' for t in n.targets))
controls = controls.replace('11주차','12주차').replace('예: 기권, Langfuse, 실습','예: 배정, SRM, 과제')
# The initial illustration remains readable with JavaScript disabled.
n=1200;z=1.959963984540054
def wilson(p):
    d=1+z*z/n;c=(p+z*z/(2*n))/d;r=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-r,c+r
la,ua=wilson(.55);lb,ub=wilson(.64)
lo=.09-math.hypot(.64-lb,ua-.55);hi=.09+math.hypot(ub-.64,.55-la)
def x(p):return 180+(p+.05)/.30*950
initial=f'<svg class="chart ci-chart" viewBox="0 0 1220 240" role="img" aria-label="각 버전 1200명일 때 차이 9%p와 95% 구간"><line x1="180" y1="165" x2="1130" y2="165" stroke="var(--rule)"/><line x1="{x(0)}" y1="30" x2="{x(0)}" y2="180" stroke="var(--muted)" stroke-dasharray="6 6"/><line x1="{x(lo)}" y1="90" x2="{x(hi)}" y2="90" stroke="var(--blue)" stroke-width="7"/><circle cx="{x(.09)}" cy="90" r="12" fill="var(--ink)"/>'+''.join(f'<text x="{x(p)}" y="205" text-anchor="middle">{round(p*100)}%p</text>'for p in [-.05,0,.05,.10,.15,.20,.25])+f'<text x="{x(lo)}" y="60" text-anchor="middle">{lo*100:.1f}</text><text x="{x(hi)}" y="60" text-anchor="middle">{hi*100:.1f}</text></svg>'
slides[39]['body']=slides[39]['body'].replace('<div id="sample-chart"></div>','<div id="sample-chart">'+initial+'</div>').replace('<p id="sample-result" class="statement"></p>',f'<p id="sample-result" class="statement">각 1200명 · 차이 +9.0%p · 95% 구간 [{lo*100:.1f}, {hi*100:.1f}]%p</p>')
sections=[]
for s in slides:
    i=s['page']; title_tag='h1' if i==1 else 'h2'
    source='<span>교수 작성 설명 · 수업용 실습</span>'
    if s['source']:
        label,url=SOURCES[s['source']]
        source=f'<a href="{url}" target="_blank" rel="noopener">{H(label)}</a>'
    note='\n\n'.join(label+'\n'+s[key] for key,label in FIELDS)
    sections.append(f'<section class="slide {"dark" if s["dark"] else ""}" id="slide-{i}" data-kind="{s["kind"]}" data-chapter="{H(s["chapter"])}" aria-label="{i}페이지 {H(s["title"].replace("<br>"," "))}"><header><{title_tag}>{s["title"]}</{title_tag}><p class="subtitle">{s["sub"]}</p></header><div class="body">{s["body"]}</div><footer><span class="source">{source}</span><span class="pageno">{s["chapter"]} / {i:02}</span></footer><aside class="presenter-note">{H(note)}</aside></section>')
head='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
(P/'index.html').write_text(head+'<meta name="description" content="LLMOps 12주차 온라인 실험과 A/B 테스트. 100분 수업, 64장, 단계별 실습과 9–12주차 통합 과제."><title>12주차 | 온라인 실험과 A/B 테스트</title><style>'+css+'</style></head><body><main class="deck-shell">'+''.join(sections)+'</main>'+controls+'<script>'+(P/'deck.js').read_text()+'</script></body></html>')
(P/'preview.html').write_text(head.replace('<html lang="ko">','<html lang="ko" class="js presentation-mode">')+'<meta name="robots" content="noindex"><title>12주차 장표 미리보기</title><style>'+css+(P/'preview.css').read_text()+'</style></head><body><main id="preview-root" inert></main><script>'+(P/'preview.js').read_text()+'</script></body></html>')
manifest=[{k:v for k,v in s.items() if k!='body'} for s in slides]
(P/'slide-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(P/'teaching-notes.json').write_text(json.dumps([{**{k:s[k] for k,_ in FIELDS},'page':s['page'],'title':s['title'].replace('<br>',' ')} for s in slides],ensure_ascii=False,indent=2)+'\n')
(P/'lecture-notes.md').write_text('# 12주차 페이지별 설명 노트\n\n'+ '\n\n'.join(f'## {s["page"]:02}. {s["title"].replace("<br>"," ")}\n\n'+'\n\n'.join(f'### {label}\n\n{s[key]}' for key,label in FIELDS) for s in slides)+'\n')

out=P/'instructor';out.mkdir(exist_ok=True)
(out/'handbook.css').write_text((ROOT/'week11/lecture/instructor/handbook.css').read_text())
parts=[head+'<title>12주차 강의 준비 | 장표·실습 설명</title><link rel="stylesheet" href="handbook.css"></head><body><header class="masthead"><a href="../">12주차 강의안</a><a href="../../assignment/">공개 과제 안내</a></header><main><header class="intro"><h1>온라인 실험과 배포 판단</h1><p class="lead">64장 · 100분 · 5개 Notebook</p><p>실행 성공보다 판단의 근거가 목표입니다. 설명 노트는 발표자 모드에서도 현재 장표와 함께 바뀝니다.</p></header><nav class="local-nav"><a href="#weeks">10·11·12주차 차이</a><a href="#runbook">수업 진행</a><a href="#overview">페이지별 핵심</a><a href="#cells">셀별 안내</a></nav>',
 '<section id="runbook"><h2>100분 진행</h2><p>0–15분 설계·01번 → 15–35분 API·02번 → 35–50분 데이터 신뢰성·03번 → 50–75분 효과·04번 → 75–90분 실제 모델·05번 발췌 → 90–100분 토론·과제.</p><p>장표 21·30·38·50·55에서 해당 Notebook으로 전환합니다. 04번 셀 7–8은 교수 시연/복습, 05번은 모델을 미리 준비합니다. 실행 중에는 다음 설명을 진행하고, 모델 설치는 수업 전에 완료합니다.</p><p>기존 실행에서 실제 Ollama B 출력은 길이 상한에 걸렸습니다. 자신의 실행에서도 원문과 종료 이유를 확인하고, 잘림이 있으면 오프라인 재검증 사례로 설명합니다. 온라인 성과는 별도의 합성 데이터이며 실제 모델의 효과가 아닙니다.</p><p>화면 공유는 강의안 창만 선택합니다. 발표자 모드 버튼으로 연 별도 창에서 현재·다음 장표와 노트를 확인합니다. 노트 글씨와 영역 비율을 조절할 수 있고 설정이 유지됩니다.</p></section><section id="overview"><h2>페이지별 핵심 메시지</h2>']
comparison='<section id="weeks"><h2>10·11·12주차의 서로 다른 검증</h2><div class="table-scroll"><table><thead><tr><th>주차</th><th>단위</th><th>검증 질문</th><th>남길 증거</th></tr></thead><tbody><tr><td>10 운영</td><td>요청·작업 구간</td><td>정상 처리·장애 진단·복구가 가능한가?</td><td>로그·Trace·지표·복구 확인</td></tr><tr><td>11 품질</td><td>고정 질문의 답변</td><td>근거·정확성·기권 기준을 만족하는가?</td><td>문항별 실패·A/B/C 회귀 평가</td></tr><tr><td>12 실험</td><td>배정 사용자</td><td>사용자 결과를 개선하는가?</td><td>배정·누락·효과 구간·위험</td></tr></tbody></table></div><p><strong>11주차 A/B/C는 같은 질문을 여러 버전으로 실행한 비교, 12주차 A/B는 사용자 집단 간 결과를 비교하는 설계입니다.</strong> 이번 주는 API·도구 정의를 다시 길게 설명하지 않고, 배정·분모·관찰 창·불확실성·실험 오염에 집중합니다.</p><p><a href="https://github.com/smilesjcha/llmops-16week/blob/main/week12/lecture/WEEKS_10_12_COMPARISON.md">원본 장표별 중복 점검과 수정 내용</a> · <a href="#book-01">01번</a> · <a href="#book-02">02번</a> · <a href="#book-03">03번</a> · <a href="#book-04">04번</a> · <a href="#book-05">05번</a></p></section>'
parts.insert(1,comparison)
chapter=None
for s in slides:
    if s['chapter']!=chapter:
        if chapter is not None:parts.append('</tbody></table></div>')
        chapter=s['chapter'];parts.append(f'<h3>{H(chapter)}</h3><div class="table-scroll"><table><thead><tr><th>쪽</th><th>장표</th><th>전달할 한 문장</th></tr></thead><tbody>')
    parts.append(f'<tr><td>{s["page"]}</td><td><a href="#page-{s["page"]}">{s["title"].replace("<br>"," ")}</a></td><td>{H(s["message"])}</td></tr>')
parts.append('</tbody></table></div></section><section id="page-notes"><h2>페이지별 설명 노트</h2>')
for s in slides:
    parts.append(f'<article id="page-{s["page"]}"><h3>{s["page"]:02}. {s["title"].replace("<br>"," ")}</h3><a href="../index.html#slide-{s["page"]}">이 장표 열기</a>'+''.join(f'<section class="note-block"><h4>{label}</h4><p>{H(s[key])}</p></section>' for key,label in FIELDS)+'</article>')
parts.append('</section><section id="cells"><h2>실습 셀별 진행</h2><p>번호는 Markdown 셀을 제외한 코드 셀 순서입니다. 모든 Notebook의 첫 코드 셀은 경로와 Python 커널 확인입니다. Notebook 상단의 실행 지도와 함께 사용합니다.</p>')
guide=json.loads((ROOT/'week12/lab/notebook-guide.json').read_text())
cell_notes=json.loads((ROOT/'week12/lab/cell-teaching-guide.json').read_text())
book_notes=json.loads((ROOT/'week12/lab/instructor-notes.json').read_text())['books']
for book in guide:
    key=book['file'][:2];details=book_notes[key]
    parts.append(f'<article id="book-{key}"><h3>{H(book["title"])}</h3><p>{H(details["summary"])}</p><p><strong>재실행:</strong> {H(details["rerun"])}</p><p>{book["minutes"]}분 · 코드 셀 {book["code_cells"]}개 · <a href="https://github.com/smilesjcha/llmops-16week/blob/main/week12/lab/notebooks/{book["file"]}">Notebook 열기</a></p>')
    for cell in [c for c in cell_notes if c['book']==key]:
        parts.append(f'<section class="note-block" id="book-{key}-cell-{cell["code_cell"]}"><h4>코드 셀 {cell["code_cell"]} · {H(cell["title"])}</h4><p>전체 {cell["position"]}번째 셀 · <code>{H(cell["first_line"])}</code></p><p><strong>확인 결과:</strong> {H(cell["expected"])}</p><p><strong>화면 짚기:</strong> {H(cell["point"])}</p><p><strong>학생에게 설명:</strong> {H(cell["talk"])}</p><p><strong>확인 질문:</strong> {H(cell["question"])}</p></section>')
    parts.append('</article>')
parts.append('</section></main></body></html>');(out/'index.html').write_text(''.join(parts))
print(f'Built {len(slides)} slides, preview, notes and instructor handbook')
