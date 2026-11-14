"""Portable HTML decision report with the original units' reproducible analysis."""
import json
from pathlib import Path
from .analysis import analyze, peeking_demo
from .simulate import SCENARIOS, load_units


def render_report(reports):
    data = json.dumps(reports, ensure_ascii=False).replace("<", "\\u003c")
    return '''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>12주차 · 온라인 실험 판단 보고서</title>
<style>:root{--ink:#15191f;--blue:#1954cb;--navy:#0b203a;--rule:#c7d0dc;--wash:#edf3fc}*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font:18px/1.65 system-ui,sans-serif;word-break:keep-all}main{max-width:1120px;margin:auto;padding:40px 24px}a{color:var(--blue)}h1{font-size:40px;line-height:1.2}h2{font-size:24px;margin-top:36px}.eyebrow{font-size:14px;letter-spacing:.1em}.notice{padding:16px 20px;background:var(--wash)}label{display:block;font-weight:700;margin-top:24px}select,button{font:inherit;padding:12px;border:1px solid var(--rule);background:#fff;color:var(--ink);max-width:100%}header{padding:0 0 24px;border-bottom:1px solid var(--rule)}.decision{padding:24px 0;border-bottom:1px solid var(--rule);display:grid;grid-template-columns:220px 1fr;gap:24px}.status{font-size:44px;font-weight:700;color:var(--blue)}table{border-collapse:collapse;width:100%;margin:24px 0}th,td{border-bottom:1px solid var(--rule);padding:12px;text-align:left}th{background:var(--wash)}.scroll{overflow:auto}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}.stats>div{border-top:2px solid var(--ink);padding:16px 0}.stats strong{display:block;font-size:30px}svg{width:100%;max-height:210px}.small{font-size:15px;color:#515e70}#reasons{margin:0}footer{border-top:1px solid var(--rule);margin-top:40px;padding-top:20px}button{cursor:pointer}:focus-visible{outline:3px solid var(--blue);outline-offset:3px}@media(max-width:680px){h1{font-size:30px}.decision,.stats{grid-template-columns:1fr}.status{font-size:36px}th,td{font-size:15px;padding:10px}}@media print{select,button{display:none}main{padding:0}h1{font-size:28px}.decision{break-inside:avoid}.scroll{overflow:visible}}</style>
<main><header><p class="eyebrow">WEEK 12 / EXPERIMENT REVIEW</p><h1>좋아진 답변, 배포 가능한 변경?</h1><p>사용자 배정 → 데이터 신뢰성 → 해결 확인율 → 운영 기준 → 판단</p></header>
<p class="notice"><strong>교수 작성 합성 데이터</strong> · 가상의 14일 종료 스냅샷. 실제 고객·기업·모델 성과가 아닙니다. 이 보고서는 코드 실행 결과를 읽는 수업용 사례입니다.</p>
<label for="scenario">살펴볼 사례</label><select id="scenario"></select><section class="decision" aria-live="polite"><div><div id="decision" class="status"></div><p id="meaning"></p></div><div><strong>판단 근거</strong><ul id="reasons"></ul></div></section>
<div class="stats"><div>사용자 수<strong id="users"></strong></div><div>해결 확인율 차이<strong id="lift"></strong></div><div>SRM p-value<strong id="srm"></strong></div></div>
<h2>버전별 결과</h2><div class="scroll"><table><thead><tr><th>지표</th><th>A 기준선</th><th>B 후보</th><th>사전 기준</th></tr></thead><tbody id="rows"></tbody></table></div>
<h2>불확실성과 해석</h2><div id="interval"></div><p id="interval-text"></p><p class="small">95% Newcombe–Wilson 신뢰구간, 독립 사용자·고정 종료 시점의 이진 지표. 매일 반복해 ‘유의하면 종료’하는 규칙에는 사용하지 않습니다. 이 수업의 지연·오류 상한은 운영 절대 기준이며 통계적 비열등성 검정이 아닙니다.</p>
<h2>분모와 관찰 창</h2><p>분모는 실험 진입 사용자 전체의 첫 요청입니다. 30분 내 해결됐다고 확인한 사용자만 분자입니다. 피드백 미응답은 ‘해결 확인 없음’이며 실제로 해결 실패했다고 단정하지 않습니다. 오류 사용자도 분모에 남깁니다.</p>
<h2>검토 기록</h2><ol><li>배정·이벤트·버전이 믿을 만한가?</li><li>성공 지표와 운영 지표가 같은 방향인가?</li><li>배포를 보류한다면 무엇을 바꿔 다시 평가할 것인가?</li></ol>
<button id="download">현재 결과 JSON 저장</button> <button onclick="window.print()">현재 사례 인쇄 / PDF</button>
<footer><a href="https://smilesjcha.github.io/llmops-16week/week12/lecture/">웹 강의안</a> · <a href="https://smilesjcha.github.io/llmops-16week/week12/assignment/">9–12주차 통합 과제</a> · <a href="https://github.com/smilesjcha/llmops-16week/tree/main/week12/lab/notebooks">Notebook 실습</a><p class="small">INVALID: 해석 중단 / WAIT: 계획 미충족 / HOLD: 운영 기준 위반 / INCONCLUSIVE: 효과 근거 부족 / REVIEW: 사람 검토 대기. 자동 배포 없음.</p></footer></main>
<script>const data='''+data+''';const $=s=>document.querySelector(s),pct=v=>v===null?'—':(100*v).toFixed(1)+'%',num=v=>v===null?'—':v.toFixed(0);for(const [k,v]of Object.entries(data)){const o=document.createElement('option');o.value=k;o.textContent=v.label;$('#scenario').append(o);}$('#scenario').value=data.slow?'slow':Object.keys(data)[0];function render(){const r=data[$('#scenario').value].report,a=r.arms.A,b=r.arms.B,c=r.contract,e=r.effect;$('#decision').textContent=r.decision;$('#meaning').textContent=({INVALID:'데이터 진단 우선',WAIT:'표본·기간 확보',HOLD:'배포 보류',INCONCLUSIVE:'효과 근거 부족',REVIEW:'사람 검토 대기'})[r.decision];$('#reasons').replaceChildren(...r.reasons.map(t=>{const li=document.createElement('li');li.textContent=t;return li;}));$('#users').textContent=a&&b?(a.n+b.n).toLocaleString():'—';$('#lift').textContent=e?(100*e.difference).toFixed(1)+'%p':'해석 중단';$('#srm').textContent=r.srm?.p_value===null||!r.srm?'—':r.srm.p_value.toExponential(3);const rows=a&&b?[['진입 사용자',a.n,b.n,'각 '+c.min_per_arm+'명 이상'],['해결 확인율',pct(a.rate),pct(b.rate),'차이 '+(100*c.practical_lift)+'%p 이상 + 구간 하한 > 0'],['피드백 수집률',pct(a.feedback_rate),pct(b.feedback_rate),'선택 편향 함께 검토'],['오류율',pct(a.error_rate),pct(b.error_rate),'각 '+pct(c.max_error_rate)+' 이하'],['p95 응답 시간',num(a.p95_ms)+'ms',num(b.p95_ms)+'ms','각 '+c.max_p95_ms+'ms 이하']]:[];$('#rows').replaceChildren(...rows.map(row=>{const tr=document.createElement('tr');row.forEach(x=>{const td=document.createElement('td');td.textContent=x;tr.append(td);});return tr;}));$('#interval').replaceChildren();if(e){const lo=Math.min(-.02,e.low-.02),hi=Math.max(.12,e.high+.02),x=v=>70+(v-lo)/(hi-lo)*860;$('#interval').innerHTML=`<svg viewBox="0 0 1000 170" role="img" aria-label="95% 신뢰구간"><line x1="70" y1="80" x2="930" y2="80" stroke="#c7d0dc"/><line x1="${x(0)}" y1="30" x2="${x(0)}" y2="120" stroke="#515e70" stroke-dasharray="5 5"/><line x1="${x(e.low)}" y1="80" x2="${x(e.high)}" y2="80" stroke="#1954cb" stroke-width="8"/><circle cx="${x(e.difference)}" cy="80" r="9" fill="#0b203a"/><text x="${x(0)}" y="150" font-size="23" text-anchor="middle">0%p</text><text x="${x(e.low)}" y="46" font-size="23" text-anchor="middle">${(100*e.low).toFixed(1)}%p</text><text x="${x(e.high)}" y="46" font-size="23" text-anchor="middle">${(100*e.high).toFixed(1)}%p</text></svg>`;$('#interval-text').textContent=`B − A: ${(100*e.difference).toFixed(2)}%p, 95% 구간 [${(100*e.low).toFixed(2)}, ${(100*e.high).toFixed(2)}]%p. ${r.decision==='HOLD'?'효과가 양수여도 운영 기준 위반을 덮을 수 없습니다.':'이 결과와 지연·오류·사례를 함께 검토합니다.'}`;}else{$('#interval-text').textContent='신뢰성 검사를 통과하기 전에는 효과의 크기나 승자를 해석하지 않습니다.';}}$('#scenario').onchange=render;$('#download').onclick=()=>{const b=new Blob([JSON.stringify(data[$('#scenario').value],null,2)],{type:'application/json'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='week12-'+$('#scenario').value+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);};render();</script></html>'''


def build_reports(out=None):
    out = Path(out or Path(__file__).with_name("reports"))
    out.mkdir(parents=True, exist_ok=True)
    reports = {name: {"label": label, "report": analyze(load_units(name))} for name, label in SCENARIOS.items()}
    (out/"results.json").write_text(json.dumps(reports, ensure_ascii=False, indent=2))
    (out/"report.html").write_text(render_report(reports))
    (out/"peeking.json").write_text(json.dumps(peeking_demo(), indent=2))
    return reports


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = build_reports(args.out)
    print(json.dumps({k: v["report"]["decision"] for k, v in result.items()}))
