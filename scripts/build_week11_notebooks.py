"""Generate independent notebooks; explanations, experiments and clean outputs."""
from pathlib import Path
import nbformat as nbf
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "week11/lab/notebooks"
SETUP = """from pathlib import Path
import sys, json
ROOT = next((p for p in [Path.cwd(), *Path.cwd().parents] if (p / "week11/lab/evaluation.py").exists()), None)
if ROOT is None:
    raise RuntimeError("저장소 안에서 Notebook을 실행하세요.")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if sys.version_info[:2] != (3, 11):
    raise RuntimeError("저장소 .venv의 Python 3.11 커널을 선택하세요.")
import pandas as pd
from IPython.display import display
from week11.lab.evaluation import *
docs, questions = load_data()
dev = [q for q in questions if q["split"] == "dev"]
test = [q for q in questions if q["split"] == "test"]
print("환경 준비 완료", sys.version.split()[0], "문서",len(docs),"질문",len(questions))
"""

def build(name, title, purpose, steps, extension):
    code_text = "\n".join(step[2] for step in steps)
    names = ["load_data"] + [name for name in ["validate_data", "Config", "Retriever", "evaluate", "summarize", "ranking_metrics", "select_on_dev", "run_experiment"] if re.search(r"\b"+name+r"\b", code_text)]
    setup = SETUP.replace("from week11.lab.evaluation import *", "from week11.lab.evaluation import " + ", ".join(names))
    if "json." not in code_text:
        setup = setup.replace("import sys, json", "import sys")
    nb = nbf.v4.new_notebook()
    nb.cells = [nbf.v4.new_markdown_cell(f"""# {title}

{purpose}

**준비:** 저장소 터미널에서 python -m pip install -r requirements/week11-offline.txt 실행.
VS Code 커널에서 저장소 .venv의 **Python 3.11** 선택 후 위에서 아래로 실행합니다.
각 파일은 다른 Notebook의 변수를 요구하지 않습니다. GPU·Ollama·API 키는 필요 없습니다.

**데이터:** 교수 작성 가상 쇼핑 정책입니다. 실제 기업 규정이나 고객 기록이 아닙니다.
핵심 단계는 수업에서 함께 실행하고 확장 실험은 복습용입니다. [실습 안내](../README.md).
"""), nbf.v4.new_code_cell(setup)]
    for i,(heading,why,code,check) in enumerate(steps,1):
        nb.cells.extend([nbf.v4.new_markdown_cell(f"## {i}. {heading}\n\n{why}"),
                         nbf.v4.new_code_cell(code),
                         nbf.v4.new_markdown_cell(f"**확인과 해석**\n\n{check}")])
    nb.cells.append(nbf.v4.new_markdown_cell("## 확장 실험과 프로젝트 적용\n\n"+extension+"""

**실행 실패 시:** ModuleNotFoundError는 커널과 설치 터미널이 같은 .venv인지 확인합니다.
ROOT 오류는 저장소 안에서 파일을 열면 해결됩니다. 변수가 섞였다면 Restart Kernel 후 Run All.
예외 실험은 try/except로 설명하므로 정상 실행에서는 빨간 오류로 끝나지 않습니다.

**기록:** 변경 설정 / 예상 / 실제 관찰 / 실패 질문 ID / 다음 행동을 5줄로 적습니다.
개인 프로젝트 원문·연락처·API 키는 공개 GitHub에 올리지 않습니다.
"""))
    nb.metadata = dict(kernelspec=dict(display_name="Python 3.11 (llmops)",language="python",name="python3"),
                       language_info=dict(name="python",version="3.11"))
    OUT.mkdir(parents=True,exist_ok=True)
    nbf.write(nb,OUT/name)

build("01_dataset_contract.ipynb","01 평가 데이터의 기준과 분리",
"목표: 답변 가능 여부·필수 근거를 검증하고 같은 의도 표현이 dev/test에 섞이는 문제를 재현합니다.",[
("현재 문서와 과거 문서","폐기된 정책은 정답 근거가 아닙니다. 메타데이터로 검색 전에 필터링합니다.",
'display(pd.DataFrame(docs)[["id","title","status","version"]])',
"현재 18개, 과거 4개입니다. 과거 문서는 실패를 보여주기 위해 남겨 두었습니다."),
("평가 항목 구조","query는 입력, gold_ids는 필수 문서 집합, reference는 사람이 확인할 의미 기준입니다.",
'display(pd.DataFrame(questions).head(6))\nprint(json.dumps(questions[4],ensure_ascii=False,indent=2))',
"교환 기간과 비용은 두 문서가 필요합니다. 정답을 검색 입력이나 색인에 섞지 마세요."),
("문항과 독립 의도","말투 두 개가 곧 독립적인 두 문제는 아닙니다.",
'df=pd.DataFrame(questions)\ndisplay(pd.crosstab([df["split"],df["slice"]],df["style"]))\ndisplay(df.groupby("split").agg(questions=("id","count"),groups=("group","nunique")))',
"각 split은 24문항·12개 의도입니다. test 복수 근거 의도는 하나뿐이므로 일반화에 주의합니다."),
("정답 무결성","삭제된 문서나 과거 문서를 정답으로 쓰는 오류를 차단합니다.",
'import copy\nbad=copy.deepcopy(questions)\nbad[0]["gold_ids"]=["D999"]\ntry:\n    validate_data(docs,bad)\nexcept ValueError as error:\n    print("예상된 실패:",error)\nvalidate_data(docs,questions)',
"데이터 오류를 조용히 0점으로 만들지 않습니다."),
("표현 변형 누수","같은 의도 그룹은 한 split에만 둡니다.",
'bad=copy.deepcopy(questions)\nbad[1]["split"]="test"\ntry:\n    validate_data(docs,bad)\nexcept ValueError as error:\n    print("누수 차단:",error)\nassert {q["group"] for q in dev}.isdisjoint({q["group"] for q in test})',
"공유 정책 문서를 검색하는 조건이며 신규 도메인 일반화 실험은 아닙니다."),
("합성 질문 검토","자동 생성은 정답 검수를 대체하지 못합니다. 아래는 사람이 쓴 검토 예시입니다.",
'display(pd.DataFrame([{"query":"제주 추가 배송비는?","decision":"채택 후보"},{"query":"무료 반품은 언제까지?","decision":"무료라는 잘못된 전제 수정"},{"query":"내 운동화 내일 와요?","decision":"답변 불가 사례"}]))',
"잘못된 전제·문서 밖 정보·개별 주문 상태를 구분합니다.")
],"1. 단일·복수 근거·답변 불가 질문을 하나씩 작성합니다.\n2. group·출처·검토 상태를 기록합니다.\n3. 공개 test를 반복 최적화한 뒤에는 새 평가 세트를 준비합니다.")

build("02_retrieval_baselines.ipynb","02 검색 기준선과 원인 분리",
"목표: 단어/문자 TF-IDF와 버전 필터를 따로 비교합니다. TF-IDF는 Term Frequency–Inverse Document Frequency입니다.",[
("단어 단위 기준선","문서 내 빈도와 집합에서의 희소성을 결합합니다. 의미를 이해하는 LLM은 아닙니다.",
'retriever=Retriever(docs,Config("word-all"))\ndisplay(pd.DataFrame(retriever.search("단순 변심 반품 배송비는 얼마인가요?")))',
"점수는 정답 확률이 아닙니다. 유사도와 정책 유효성을 구분합니다."),
("벡터 크기","문서만 fit하고 질문은 transform합니다.",
'print("문서 × 특징:",retriever.matrix.shape)\nv=retriever.vectorizer.transform(["반품 배송비"])\nprint(retriever.vectorizer.get_feature_names_out()[v.indices])',
"word 토큰화는 한국어 형태소 분석기가 아닙니다."),
("겹치는 단어가 없는 질문","0점 문서 반환은 가짜 검색 성공을 만들 수 있습니다.",
'print(retriever.search("zzzzzzzz"))\nassert retriever.search("zzzzzzzz")==[]',
"빈 검색 결과와 서버 장애는 다릅니다."),
("문자 단위 검색","2~4그램은 부분 문자열을 공유하지만 동의어 의미까지 해결하지는 못합니다.",
'char=Retriever(docs,Config("char-current","char",True))\nfor query in ["반품 배송비","반품배송비","돌려보내면 택배비 얼마죠?"]:\n    print(query)\n    display(pd.DataFrame(char.search(query))[["id","title","score"]])',
"문자 TF-IDF는 신경망 임베딩이 아닙니다."),
("한 요소씩 비교","필터와 알고리즘을 동시에 바꾸면 원인이 불명확합니다.",
'configs=[Config("word-all"),Config("word-current","word",True),Config("char-current","char",True)]\ncomparison=pd.DataFrame([{"name":c.name,**summarize(evaluate(docs,dev,c))} for c in configs])\ndisplay(comparison[["name","recall","mrr","archive_in_topk","false_accept"]])',
"dev에서 원인을 탐색하고 test로 설정을 고르지 않습니다."),
("동점 처리","동점 규칙도 재현 조건입니다.",
'tiny=[dict(id=x,title="반품",text="반품",status="current") for x in ["B","A"]]\nprint(Retriever(tiny,Config("tie")).search("반품"))',
"문서 ID 오름차순으로 동점을 해소합니다.")
],"1. analyzer와 current_only 효과를 분리합니다.\n2. 실제 임베딩 검색기로 바꿀 때 id/score/text/status 계약을 유지합니다.\n3. 모델·정규화·거리 함수·인덱스 버전을 기록합니다.")

build("03_metrics_and_k.ipynb","03 지표 계산과 검색 개수",
"목표: Hit·Recall·Mean Reciprocal Rank·normalized Discounted Cumulative Gain 손계산과 코드 대조.",[
("복수 정답의 Hit와 Recall","정답 두 개 중 하나 검색이면 Hit=1, Recall=0.5입니다.",
'display(pd.DataFrame([ranking_metrics(["D03","D08","D09"],["D03","D04"],3),ranking_metrics(["D08","D03","D04"],["D03","D04"],3)],index=["하나만","둘 다"]))',
"하나라도 찾았는지와 필요한 근거를 모두 찾았는지는 다릅니다."),
("순위 할인","MRR은 첫 정답 순위, nDCG는 여러 관련 문서의 순위를 반영합니다. 이 실습은 이진 관련도입니다.",
'import math\nmetrics=ranking_metrics(["X","A","B"],["A","B"],3)\nmanual=(1/math.log2(3)+1/math.log2(4))/(1+1/math.log2(3))\nprint(metrics,manual)\nassert abs(metrics["ndcg"]-manual)<1e-12',
"이상 순위 분모는 min(k, 정답 문서 수)까지 계산합니다."),
("라이브러리 교차 검증","정의와 ties 처리를 맞춰 비교합니다.",
'from sklearn.metrics import ndcg_score\nexpected=ndcg_score([[0,1,1]],[[3,2,1]],k=3)\nassert abs(expected-metrics["ndcg"])<1e-12\nprint(expected)',
"직접 구현한 지표도 테스트 대상입니다."),
("답변 불가 분모","정답 문서가 비어 있으면 Recall은 정의되지 않습니다.",
'print("답변 불가:",ranking_metrics(["A"],[],3))\nprint("검색 실패:",ranking_metrics([],["A"],3))',
"None과 검색 실패 0점을 구분합니다."),
("검색 개수 k","Recall 상승이 생성 품질 상승을 보장하지 않습니다.",
'rows=[{"k":k,**summarize(evaluate(docs,dev,Config(f"k{k}","char",True,k)))} for k in [1,2,3,5,10]]\ndisplay(pd.DataFrame(rows)[["k","hit","recall","mrr","ndcg","false_accept"]])',
"LLM 생성이 없으므로 답변 품질·토큰 비용을 측정했다고 말할 수 없습니다."),
("중복 차단","같은 정답 반복으로 Recall이 부풀려지는 오류를 막습니다.",
'try:\n    ranking_metrics(["A","A"],["A"],3)\nexcept ValueError as error:\n    print("중복 차단:",error)',
"실제 청크 검색은 청크/문서 중 평가 단위를 먼저 고정합니다.")
],"1. k=1,3,5를 같은 질문에서 비교합니다.\n2. 서비스의 성공이 전체 근거 확보인지 정의합니다.\n3. 생성 모델 연결 시 context 길이·정확성·인용·지연을 측정합니다.")

build("04_calibration_and_error_analysis.ipynb","04 기권 기준과 실패 분석",
"목표: dev로 설정을 선택한 뒤 고정 test의 실패를 유형·말투별로 분석합니다.",[
("설정 선택","교육용 utility = 근거 확보율 − 답변 불가 수락률 − 0.25×답변 가능 기권율.",
'selected,trials=select_on_dev(docs,dev)\nprint(selected)\ndisplay(pd.DataFrame([{**t["config"],"utility":t["utility"],**t["summary"]} for t in trials]).sort_values("utility",ascending=False).head(8))',
"모든 사업의 공통 목표가 아닙니다. 동점은 작은 k, 높은 threshold 순으로 해소합니다."),
("임계값 양면","기권 증가로 위험한 시도와 유용한 응답이 함께 줄 수 있습니다.",
'from dataclasses import replace\ncurve=[{"threshold":t,**summarize(evaluate(docs,dev,replace(selected,threshold=t)))} for t in [0,.15,.3,.45,.6]]\ndisplay(pd.DataFrame(curve)[["threshold","coverage","false_accept","missed_answer","evidence_complete"]])',
"cosine 0.3은 정답 확률 30%가 아닙니다."),
("고정 test","이후 test에 맞춰 조정하면 새 평가 자료가 필요합니다.",
'baseline=evaluate(docs,test,Config("word-all"))\ncandidate=evaluate(docs,test,selected)\ndisplay(pd.DataFrame({"baseline":summarize(baseline),"candidate":summarize(candidate)}))',
"Recall과 필수 근거 확보율의 차이를 기권 정책과 연결해 봅니다."),
("말투별 분석","전체 평균에 가려진 취약 유형을 찾습니다.",
'frame=pd.DataFrame(candidate)\ndisplay(pd.DataFrame([{"style":style,**summarize(group.to_dict("records"))} for style,group in frame.groupby("style")]))\ndisplay(pd.crosstab(frame["slice"],frame["error"]))',
"작은 유형은 순위 확정보다 후속 조사 단서로 활용합니다."),
("실패 근거 추적","질문·정답·검색 결과·정책 판단을 연결합니다.",
'failures=[r for r in candidate if r["error"] not in ["evidence_complete","correct_abstain"]]\nfor r in failures[:3]:\n    print(r["id"],r["query"],r["error"],"필수",r["gold_ids"])\n    display(pd.DataFrame(r["ranked"])[["id","title","score"]] if r["ranked"] else pd.DataFrame())',
"검색 실패를 무조건 프롬프트 수정으로 해결하려 하지 않습니다."),
("분리 규칙 강제","도구가 실수를 먼저 차단합니다.",
'try:\n    select_on_dev(docs,test)\nexcept ValueError as error:\n    print("test 선택 금지:",error)',
"이미 본 test에 맞춰 새 후보를 만드는 사람의 행동까지 막아주지는 못합니다.")
],"1. 가장 비용이 큰 실패 두 개의 사용자 영향을 적습니다.\n2. 동의어·문서 개정·추가 질문 중 하나만 dev에서 실험합니다.\n3. 새 의도로 개선을 확인합니다.")

build("05_judge_rubric.ipynb","05 답변 평가와 평가자 검증",
"목표: 근거 기반 판정과 평가자 오류 분석. judge 결과는 교육용 작성 fixture이며 실제 모델 호출이나 인간 주석가 연구가 아닙니다.",[
("판정 기준","LLM-as-a-Judge는 모델이 답변을 평가하는 방식입니다. 유창성이 사실성을 대신하지 못합니다.",
'from week11.lab.judging import RUBRIC, FIXTURES, build_judge_prompt, validate_judge_json, agreement, order_consistency\ndisplay(pd.DataFrame(list(RUBRIC.items()),columns=["판정","기준"]))\ndisplay(pd.DataFrame(FIXTURES)[["id","evidence","answer","gold","judge"]])',
"supported는 제공 근거의 뒷받침이며 모든 사실을 검증했다는 뜻은 아닙니다."),
("숫자 규칙의 한계","같은 숫자가 있어도 부정 표현이면 반대 의미입니다.",
'for answer in ["수령 후 7일 이내 반품 가능","수령 후 7일 이내에는 반품 불가"]:\n    print(answer,"문자열 검사:","7일" in answer)',
"문자열 규칙은 경보로 쓰되 충실성 평가를 대체하지 않습니다."),
("구조화된 평가 요청","질문·근거·답변을 분리하고 판정과 이유를 JSON으로 요구합니다.",
'prompt=build_judge_prompt("언제까지 반품 가능한가요?",FIXTURES[0]["evidence"],FIXTURES[0]["answer"])\nprint(prompt)',
"프롬프트만 생성합니다. 구분자만으로 prompt injection 안전성이 보장되지 않습니다."),
("결과 파싱","형식 오류를 임의 점수로 바꾸지 않습니다.",
'print(validate_judge_json(\'{"verdict":"supported","reason":"7일 조건 일치"}\'))\ntry:\n    validate_judge_json(\'{"verdict":"좋음","reason":"그냥 좋아요"}\')\nexcept ValueError as error:\n    print("형식 거부:",error)',
"유효 JSON과 정확한 판정은 별도입니다."),
("불일치 분석","평가자 결과도 평가합니다.",
'a=agreement()\nprint("작성 예시 일치율:",a["agreement"])\ndisplay(pd.DataFrame(a["confusion"]).T)\ndisplay(pd.DataFrame(a["disagreement"])[["id","gold","judge","reason"]])',
"5/8=62.5%는 fixture 계산입니다. 실제 LLM 성능으로 발표하지 않습니다."),
("위치 편향","위치를 바꿔도 같은 답변을 고르는지 확인합니다.",
'pairs=[dict(winner_ab="answer1",winner_ba="answer1"),dict(winner_ab="answer1",winner_ba="answer2"),dict(winner_ab="tie",winner_ba="tie")]\nprint("작성 예시의 순서 일관성:",order_consistency(pairs))',
"슬롯 A/B가 아닌 의미상의 answer ID를 비교합니다. 일관성과 정확성은 별개입니다.")
],"1. 조건 누락·근거 부족·수치 오류를 추가합니다.\n2. 선택 확장: 승인된 모델에 prompt를 전달하고 원응답·버전·설정·비용을 기록합니다. 기본 실습은 네트워크 호출이 없습니다.\n3. 독립 검토와 불일치 조정을 설계합니다.")

build("06_release_report.ipynb","06 비교 보고서와 배포 전 판단",
"목표: 그룹 bootstrap·검증 규칙·실험 manifest와 실제 실행 HTML 보고서.",[
("전체 파이프라인","dev 선택 후 test 평가와 판단을 한 실행으로 묶습니다.",
'result=run_experiment()\nprint("run_id:",result["run_id"])\nprint(result["manifest"]["candidate"])\ndisplay(pd.DataFrame(result["summary"]))',
"ID는 데이터·코드·환경·설정에서 계산됩니다. 작은 표본의 한계는 남습니다."),
("짝 비교","같은 의도의 두 표현을 함께 재표집합니다.",
'ci=result["confidence"]\nprint(json.dumps(ci,indent=2))\nprint("차이 %p:",round(ci["delta"]*100,2))\nprint("95% 구간 %p:",[round(ci[k]*100,2) for k in ["low","high"]])',
"0 포함 시 이 절차에서 개선 방향이 명확하지 않습니다. 과업 밖 일반화 근거는 별도입니다."),
("개별 변화","좋아진 사례와 나빠진 사례를 모두 남깁니다.",
'a={r["id"]:r for r in result["rows"]["baseline"]}\nchanges=[{"id":r["id"],"query":r["query"],"delta":r["recall"]-a[r["id"]]["recall"],"error":r["error"]} for r in result["rows"]["candidate"] if r["recall"] is not None]\ndisplay(pd.DataFrame(changes).sort_values("delta"))',
"평균 상승은 모든 질문의 개선을 뜻하지 않습니다."),
("학습용 배포 기준","기권만 늘려 사용성을 잃는 후보도 걸러냅니다.",
'print(result["gate"]["decision"])\ndisplay(pd.DataFrame(list(result["gate"]["checks"].items()),columns=["조건","통과"]))',
"HOLD는 실습 실패가 아닌 판단 결과입니다. REVIEW도 자동 배포가 아닙니다. 수치 기준은 교육용입니다."),
("HTML 보고서","실제 결과를 담아 브라우저에서 필터와 근거 탐색을 사용합니다.",
'from week11.lab.run_eval import render_report\nout=ROOT/"week11/lab/reports"\nout.mkdir(exist_ok=True)\n(out/"results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")\n(out/"report.html").write_text(render_report(result),encoding="utf-8")\nprint("week11/lab/reports/report.html을 브라우저로 여세요.")',
"데이터 내장 HTML이라 인터넷 없이 열립니다. reports는 Git에서 제외됩니다."),
("재현 확인","같은 환경의 결정적 실험은 같은 결과를 내야 합니다.",
'repeat=run_experiment()\nassert repeat["run_id"]==result["run_id"]\nassert repeat["summary"]==result["summary"]\nprint("재현 확인:",repeat["run_id"])\nprint(list(result["manifest"]))',
"확률적 LLM은 반복 실행과 변동 폭을 추가 기록합니다.")
],"1. 실패 두 개와 후속 실험 하나를 선택합니다.\n2. python -m week11.lab.run_eval --enforce-gate는 HOLD일 때 종료 코드 2입니다. 의도한 차단입니다.\n3. 이 실습으로 새 과제나 제출 마감이 생기지는 않습니다.")

print("Built",len(list(OUT.glob("*.ipynb"))),"notebooks")


subprocess.run([sys.executable,"-m","ruff","format",str(OUT)],check=True)
