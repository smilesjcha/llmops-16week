"""Portable public casebook generated only from the synthetic real-run snapshot."""
import html
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
OUT=ROOT/'week11/lab/sample/langfuse'
r=json.loads((OUT/'results.json').read_text())
esc=lambda x: html.escape(str(x))
labels={'baseline':'A · 기준선','candidate':'B · 근거 제한','guarded':'C · 기능 정책'}
summary=[]
for key in labels:
    d=r['guarded_decision'] if key=='guarded' else r['decision']
    m=d['summary']['baseline' if key=='baseline' else 'candidate']
    summary.append(f'<tr><th>{labels[key]}</th><td>{m["structural_pass_rate"]:.0%}</td><td>{m["false_accepts"]}건</td><td>{"비교 기준" if key=="baseline" else d["decision"]}</td></tr>')
case_rows=[]
from week11.lab.release_lab import regression_cases
for q in sorted(regression_cases(),key=lambda q: q['id']!='Q24a'):
    lines=[]
    for key,label in labels.items():
        o=next(x['output'] for x in r[key]['rows'] if x['question_id']==q['id'])
        lines.append(f'<tr><th>{label}</th><td>{esc(o["answer"]["answer"])}<small>인용: {esc(o["answer"]["citations"])}</small></td><td>{esc(o["answer"]["abstain"])}</td><td>{esc(o["judge"]["verdict"])}<small>{esc(o["judge"]["reason"])}</small></td></tr>')
    case_rows.append(f'<section><h2>{q["id"]} · {esc(q["query"])}</h2><p>참고 기준: {esc(q["reference"])}</p><div class="scroll"><table><thead><tr><th>버전</th><th>실제 서비스 응답</th><th>기권</th><th>실제 모델 평가</th></tr></thead><tbody>{"".join(lines)}</tbody></table></div></section>')
style=''':root{--focus:#1954cb}*{box-sizing:border-box}html,body{overflow-x:clip}:focus-visible{outline:3px solid var(--focus);outline-offset:4px}body{margin:0;background:#fff;color:#121923;font:18px/1.7 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:64px 32px}header{border-bottom:2px solid #111;padding-bottom:32px}h1{font-size:44px;line-height:1.25;max-width:900px}h2{font-size:26px;line-height:1.4;margin-top:0}p{max-width:1000px}a{color:#1756b7;text-underline-offset:4px}section{padding:42px 0;border-bottom:1px solid #c9d2df}table{border-collapse:collapse;width:100%;font-size:16px;text-align:left}th,td{padding:16px 12px;border-bottom:1px solid #d5dce6;vertical-align:top}thead{background:#eef3fa}th:first-child{min-width:120px}td small{display:block;color:#536174;margin-top:10px}.scroll{overflow:auto}section table{min-width:820px}section td:nth-child(2){width:46%}section td:nth-child(4){width:30%}.note{border-top:1px solid #c9d2df;padding:8px 20px;background:#f2f5fa}footer{padding:28px 0;color:#536174;font-size:15px}@media(max-width:700px){main{padding:28px 20px}h1{font-size:32px}h2{font-size:23px}body{font-size:17px}}'''
(OUT/'index.html').write_text(f'''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>11주차 실제 Langfuse 실험 비교</title><style>{style}</style><main><header><h1>새 상담 AI의 배포 판단</h1><p>같은 질문 4개, 같은 로컬 모델, 세 가지 변경. Langfuse Docker 서버에서 실행·저장을 확인한 합성 수업 사례입니다.</p><p><a href="../../../lecture/">강의안</a> · <a href="https://github.com/smilesjcha/llmops-16week/blob/main/week11/lab/langfuse/README.md">Docker·VS Code 실습 안내</a> · <a href="../../demo/">화면별 시연 안내</a> · <a href="results.json">실제 기록 JSON</a></p></header><section><h2>계약 검사와 배포 전 판단</h2><table><thead><tr><th>버전</th><th>인용·기권 검사</th><th>답변 불가 수락</th><th>결론</th></tr></thead><tbody>{''.join(summary)}</tbody></table><p class="note">계약 검사 통과율은 답변 의미 정확도가 아닙니다. REVIEW도 자동 배포가 아니며, 조건 누락과 평가자의 오판을 사람이 검토해야 합니다.</p><p>C는 UI 메뉴·API 라우트로 전달된 실시간 조회 요청을 기능 정책으로 처리합니다. 이 경로는 모델 호출·모델 평가가 없으며 <code>not_run</code>으로 표시합니다. 나머지 정상 질문은 실제 Ollama를 호출합니다.</p></section>{''.join(case_rows)}<footer>2026-11-11 검증 / Langfuse 4.78.0 / Python SDK 5.2.0 / qwen2.5:1.5b-instruct<br>선택된 합성 회귀 사례이며 일반적인 모델 성능 벤치마크가 아닙니다. 로컬 실행에서는 답변·판정·지연이 달라질 수 있습니다. 실제 Langfuse 화면은 본인 PC의 localhost:3011에서 확인합니다.</footer></main></html>''',encoding='utf-8')
print('Built real Langfuse casebook')
