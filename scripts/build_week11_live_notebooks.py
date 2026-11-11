"""Build real Ollama notebooks without rewriting the six offline notebooks."""
from pathlib import Path
import nbformat as n

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'week11/lab/notebooks'
SETUP='''from pathlib import Path
import sys, json
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "week11/lab/ollama_lab.py").exists())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
assert sys.version_info[:2] == (3, 11), "저장소 .venv의 Python 3.11 커널을 선택하세요."
import pandas as pd
from IPython.display import display
from week11.lab.ollama_lab import OllamaClient, generate_one, judge_answer, save_run, now, PROMPTS, experiment_manifest
from week11.lab.evaluation import load_data
client = OllamaClient()  # 기본 qwen2.5:1.5b-instruct / 외부 API 키 불필요
print(client.probe())
docs, questions = load_data()
by_id = {q["id"]: q for q in questions}
'''

def build(name,title,intro,steps):
    setup = SETUP
    if name.startswith('07'):
        setup = setup.replace('generate_one, judge_answer,', 'generate_one,')
    else:
        setup = setup.replace('import sys, json', 'import sys').replace('now, PROMPTS,', 'now,')
    cells=[n.v4.new_markdown_cell(f'''# {title}

{intro}

**준비:** Ollama 앱 실행 → 별도 터미널에서 `ollama pull qwen2.5:1.5b-instruct` → 이 파일의 Python 3.11 커널 선택.
기존 `requirements/week11-offline.txt`만으로 실행됩니다. Ollama Python SDK나 클라우드 계정은 필요 없습니다.
모델 다운로드는 최초 한 번만 필요합니다. 앱이 없거나 모델이 없으면 준비 방법을 표시하고 중단하며, 가짜 응답으로 대체하지 않습니다.

첫 호출은 모델 로딩 때문에 느릴 수 있습니다. 출력 최대 192토큰, 문맥 2,048토큰, temperature=0, 모델 유지 10분입니다.
Qwen2.5 Instruct는 추론 전용 모델이 아니며, thinking 지원 모델로 바꾸면 `think=False`를 보냅니다.
**속도와 문장은 기기·모델 버전에 따라 달라집니다. 특정 문장 또는 의미 판정의 일치를 성공 조건으로 삼지 않습니다.**

[전체 실습 순서](../WALKTHROUGH.md) / [실제 호출 구현](../ollama_lab.py)
'''),n.v4.new_code_cell(setup)]
    for i,(title,why,code,check) in enumerate(steps,1):
        cells.extend([n.v4.new_markdown_cell(f'## {i}. {title}\n\n{why}'),n.v4.new_code_cell(code),n.v4.new_markdown_cell('**확인 결과**\n\n'+check)])
    cells.append(n.v4.new_markdown_cell('''## 다음 실험

질문·프롬프트·모델 중 하나만 바꾸고 응답, 근거, 지연을 비교합니다. 이 사례는 개발용 시연 질문이며 미공개 test 벤치마크가 아닙니다.
생성 결과와 자체 평가가 모두 좋아도 사람의 의미 검토가 필요합니다. 실제 사용자 정보나 API 키를 입력·공개하지 않습니다.

연결 실패: Ollama 앱/`ollama serve`. 모델 없음: `ollama list` 후 pull. 긴 대기: 최초 로드 시간과 생성 시간을 분리해 확인.
변수가 섞이면 **Restart Kernel → Run All**. 출력은 Git 제외 `week11/lab/reports/`에만 저장합니다.
'''))
    nb=n.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python 3.11 (llmops)','language':'python','name':'python3'}})
    for i,c in enumerate(nb.cells):c['id']=f'{name[:2]}-cell-{i:02d}'
    n.write(nb,OUT/name)

build('07_ollama_rag_generation.ipynb','07 실제 Ollama RAG 응답 비교',
'가상 정책을 실제로 검색하고, 로컬 instruct 모델이 답변을 생성합니다. RAG는 Retrieval-Augmented Generation(검색 증강 생성)입니다. 질문·검색 근거·모델 응답·기계적 검사를 분리해서 관찰합니다.',[
('기준 프롬프트의 실제 응답','Q01a 반품 기간 질문으로 검색부터 생성까지 한 요청을 실행합니다.',
'''baseline = generate_one(client, by_id["Q01a"], prompt_version="baseline")
display(pd.DataFrame(baseline["ranked"])[["id", "title", "score"]])
print(json.dumps(baseline["answer"], ensure_ascii=False, indent=2))
print("응답(ms):", baseline["generation"]["latency_ms"], "로드(ms):", baseline["generation"]["load_ms"])''',
'실제 모델의 answer·citations·abstain이 나옵니다. 정답 문장(reference)이나 gold_ids는 생성 입력에 전달하지 않습니다.'),
('근거 제한 프롬프트의 비교','같은 질문·검색기·모델에서 시스템 프롬프트만 변경합니다.',
'''grounded = generate_one(client, by_id["Q01a"], prompt_version="grounded")
for row in [baseline, grounded]:
    print(row["prompt_version"], row["answer"])
    print(row["checks"])
print(PROMPTS["grounded"])''',
'두 응답이 같아도 정상입니다. 개선을 미리 가정하지 않습니다. 인용 ID가 검색 문서 안에 있는지와 답변 의미가 맞는지는 다른 검사입니다.'),
('복수 근거와 답변 불가 질문','문서 두 개가 필요한 교환 질문과, 문서에 없는 현재 재고 질문을 실행합니다.',
'''multi = generate_one(client, by_id["Q03a"])
unanswerable = generate_one(client, by_id["Q24a"])
for row in [multi, unanswerable]:
    print(row["question_id"], row["question"])
    print(row["answer"])
    print(row["checks"])''',
'Q03a는 기간·비용과 D03/D04 인용을 확인합니다. Q24a는 기권이 바람직합니다. 모델이 추측하면 실제 실패 사례로 기록합니다.'),
('검사와 사람 판단의 분리','검사 결과를 정답률로 이름 붙이지 않습니다.',
'''rows = [baseline, grounded, multi, unanswerable]
display(pd.DataFrame([{"id":r["question_id"],"prompt":r["prompt_version"],**r["checks"]} for r in rows]))
display(pd.DataFrame([{"id":r["question_id"],"reference":r["reference"],"actual":r["answer"]["answer"]} for r in rows]))''',
'실제 답변을 참고 기준과 읽어 비교합니다. 정상 문서 ID를 인용해도 숫자·조건·부정 표현이 틀릴 수 있습니다.'),
('토큰과 지연의 실제 측정','모델 최초 로드와 응답 생성 시간을 구분합니다.',
'''display(pd.DataFrame([{"id":r["question_id"],"prompt":r["prompt_version"],**{k:r["generation"][k] for k in ["latency_ms","load_ms","input_tokens","output_tokens","tokens_per_second"]}} for r in rows]))''',
'모든 값은 Ollama 응답과 실제 경과 시간에서 가져옵니다. 한 번의 작은 표본으로 모델 속도 순위를 정하지 않습니다.'),
('로컬 보고서 저장','실제 응답·검색 근거·검사를 HTML과 JSONL로 남깁니다.',
'''result = {"created_at":now(),"provenance":"real local Ollama calls; teaching cases", **experiment_manifest(client),"rows":rows}
report = save_run(result, ROOT/"week11/lab/reports")
print(report)
print("macOS: open week11/lab/reports/ollama-report.html")''',
'ollama-report.html에서 각 요청의 검색 근거·검사·실행 기록을 펼칩니다. 4개 실제 응답이 보입니다. 공개 페이지에 자동 업로드되지 않습니다.')])

build('08_ollama_judge_and_traces.ipynb','08 실제 LLM 평가와 실행 추적',
'작은 로컬 LLM이 실제 답변을 평가합니다. 사람이 정의한 판정과 비교하고, 검색·생성·평가를 하나의 요청 기록으로 연결합니다. 07번을 미리 실행하지 않아도 됩니다.',[
('평가자의 실제 판정','05번에서 사용한 작성 예시를 이번에는 실제 모델에 전달합니다.',
'''from week11.lab.judging import FIXTURES
cases = [f for f in FIXTURES if f["id"] in ["J01","J02","J03","J05"]]
judgments=[]
for case in cases:
    judged=judge_answer(client,"근거가 답변의 주장을 뒷받침하는가?",case["evidence"],case["answer"])
    judgments.append({"id":case["id"],"expected":case["gold"],"actual":judged["parsed"]["verdict"],"reason":judged["parsed"]["reason"],"latency_ms":judged["latency_ms"]})
display(pd.DataFrame(judgments))''',
'표의 actual과 reason은 실제 모델 출력입니다. 05번에 저장된 judge 열을 재사용하지 않습니다. 불일치가 생기면 근거와 판정 기준을 다시 읽습니다.'),
('일치율과 불일치 원인','판정 형식이 맞아도 평가자가 틀릴 수 있습니다.',
'''frame=pd.DataFrame(judgments)
print("선택 예시 일치:",int((frame.expected==frame.actual).sum()),"/",len(frame))
display(frame[frame.expected!=frame.actual])''',
'4건의 시연 계산이며 일반화된 모델 성능이 아닙니다. 작은 모델과 자기 평가의 한계를 사례로 설명합니다.'),
('생성 응답의 실제 평가','Q03a를 새로 생성한 뒤 동일한 근거로 의미 평가를 요청합니다.',
'''row=generate_one(client,by_id["Q03a"])
row["judge"]=judge_answer(client,row["question"],[d["text"] for d in row["ranked"]],row["answer"]["answer"])
row["spans"].append({"name":"llm_judge","parent_id":row["trace_id"],"duration_ms":row["judge"]["latency_ms"],"result":row["judge"]["parsed"]})
print(row["answer"])
print(row["judge"]["parsed"])
print(row["checks"])''',
'생성·코드 검사·LLM 판정을 따로 읽습니다. 같은 모델의 자기 평가는 독립 검증이 아니며 사람 검토를 대체하지 않습니다.'),
('요청과 단계별 기록','trace는 전체 요청, span은 요청 안의 개별 작업입니다.',
'''print("trace_id:",row["trace_id"])
display(pd.DataFrame(row["spans"]))
print("모델:",client.info["model"],"digest:",client.info["digest"])
print("프롬프트 해시:",row["generation"]["prompt_sha256"])''',
'동일 trace_id 아래 retrieval·generation·code_checks·llm_judge가 연결됩니다. 이 파일의 JSON은 교육용 로컬 추적 형식이며 OpenTelemetry 전송 형식 자체는 아닙니다.'),
('Langfuse·LangSmith와의 연결','플랫폼은 이 기록을 팀이 검색·비교·검토할 수 있게 관리합니다.',
'''display(pd.DataFrame([
 {"실습 기록":"trace_id + spans","Langfuse":"Trace / observations","LangSmith":"Run trace / child runs"},
 {"실습 기록":"question + reference","Langfuse":"Dataset item","LangSmith":"Dataset example"},
 {"실습 기록":"prompt_version + model","Langfuse":"Experiment","LangSmith":"Experiment"},
 {"실습 기록":"checks + judge + 사람 검토","Langfuse":"Scores / annotation","LangSmith":"Feedback / annotation queue"},
]))''',
'클라우드나 자체 호스팅 전송은 수행하지 않습니다. 플랫폼 도입은 선택이지만 입력·출력·버전·지연·평가 근거의 기록은 필요합니다. 실제 계정 연동은 공식 SDK 안내를 따릅니다.'),
('검토 가능한 결과 저장','질문 하나의 근거와 평가 판정을 함께 보관합니다.',
'''result={"created_at":now(),"provenance":"real local Ollama generation and judge; not a benchmark",**experiment_manifest(client),"rows":[row],"judge_calibration":judgments}
report=save_run(result,ROOT/"week11/lab/reports/judge")
print(report)
print("macOS: open week11/lab/reports/judge/ollama-report.html")''',
'judge 폴더에 평가자 판정과 요청 추적을 담은 HTML·JSON·JSONL이 생성됩니다. API 키 없이 로컬에서 끝납니다.')])
print('Built 07 and 08 live notebooks')
