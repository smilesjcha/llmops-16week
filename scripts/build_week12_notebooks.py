"""Independent, guided notebooks: execute, inspect, change, explain."""
from pathlib import Path
import json
import nbformat as nb

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "week12/lab/notebooks"
NOTES = json.loads((OUT.parent / "instructor-notes.json").read_text())
SETUP = '''from pathlib import Path
import sys, json, os
ROOT = next((p for p in [Path.cwd(), *Path.cwd().parents] if (p / "week12/lab/analysis.py").exists()), None)
if ROOT is None:
    raise RuntimeError("저장소 폴더를 VS Code로 열고 실행하세요.")
if sys.version_info[:2] != (3, 11):
    raise RuntimeError("저장소 .venv의 Python 3.11 커널을 선택하세요.")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import pandas as pd
from IPython.display import display, HTML
from week12.lab.experiment import DEFAULT, assign
from week12.lab.analysis import analyze
from week12.lab.simulate import load_units
print("준비 완료:", sys.version.split()[0], "실험 설정", DEFAULT.version)
'''
INDEX = []


def build(name, title, minutes, purpose, steps, extension):
    teaching = NOTES['books'][name[:2]]
    cells = [nb.v4.new_markdown_cell(f'''# {title}

**핵심 실행 {minutes}분** · {purpose}

준비: 저장소 터미널에서 `python -m pip install -r requirements/week12-online.txt` 실행.
VS Code 오른쪽 위 **Select Kernel → 저장소 .venv의 Python 3.11**을 선택합니다.
다른 Notebook의 변수나 실행 순서를 요구하지 않습니다. 이 파일의 셀은 위에서 아래로 실행하세요.

**출처 구분:** CSV는 교수 작성 합성 사용자 데이터입니다. FastAPI 요청은 실제 실습 서비스 실행이며 실제 고객 실험이 아닙니다.
05번의 Ollama만 실제 로컬 모델을 호출합니다. Docker·클라우드 계정·유료 API는 필수가 아닙니다.

## 코드 셀 실행 지도

| 코드 셀 | 실행 | 확인할 결과 |
|---:|---|---|
| 1 | 환경 준비 | Python 3.11과 설정 버전 |
'''+"\n".join(f"| {i+2} | {s[0]} | {teaching['cells'][str(i+2)]['expected']} |" for i,s in enumerate(steps))+
        f"\n\n**이번 파일의 역할:** {teaching['summary']}\n\n**재실행 방법:** {teaching['rerun']}\n\n**코드 셀 1 설명:** {NOTES['common_setup']['talk']}\n\n번호는 코드 셀 순서이며 실행 횟수 `[1]`, `[2]`와 다릅니다. [셀별 교수 설명](https://smilesjcha.github.io/llmops-16week/week12/lecture/instructor/#book-{name[:2]})"), nb.v4.new_code_cell(SETUP)]
    for i, (heading, why, code, check, question) in enumerate(steps,2):
        note = teaching['cells'][str(i)]
        cells.extend([nb.v4.new_markdown_cell(f"## 코드 셀 {i} · {heading}\n\n{why}"),
                      nb.v4.new_code_cell(code.strip()),
                      nb.v4.new_markdown_cell(f"**확인과 해석:** {note['expected']}\n\n**화면에서 볼 곳:** {note['point']}\n\n**설명 핵심:** {note['talk']}\n\n**직접 설명:** {question}")])
    cells.append(nb.v4.new_markdown_cell(f'''## 복습과 다음 단계

{extension}

실행 오류는 Kernel을 다시 시작한 뒤 위에서부터 실행해 확인합니다. `ModuleNotFoundError`는 설치 터미널과 Notebook 커널이 같은 `.venv`인지 확인하세요.
실험 결과는 `week12/lab/reports/`에 저장하고 공개 GitHub에 학생 답안·개인정보를 올리지 않습니다.
[실행 안내](../WALKTHROUGH.md) · [100분 강의안](https://smilesjcha.github.io/llmops-16week/week12/lecture/) · [9–12주차 과제](https://smilesjcha.github.io/llmops-16week/week12/assignment/)
'''))
    doc=nb.v4.new_notebook(cells=cells,metadata={"kernelspec":{"display_name":"Python 3.11 (llmops)","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.11"}})
    if (OUT/name).exists():
        previous=nb.read(OUT/name,as_version=4)
        if len(previous.cells)==len(doc.cells):
            for old,new in zip(previous.cells,doc.cells):
                new['id']=old['id']
    OUT.mkdir(parents=True,exist_ok=True);nb.write(doc,OUT/name)
    INDEX.append({"file":name,"title":title,"minutes":minutes,"cells":len(cells),"code_cells":1+len(steps),"steps":[{"code_cell":i+2,"title":s[0],"expected":s[3],"question":s[4]} for i,s in enumerate(steps)]})


build("01_experiment_contract.ipynb","01 · 가설·지표·고정 배정",8,
"실험을 시작하기 전에 바꿀 것 하나, 분석 단위, 종료 기준을 정합니다.",[
("실험 계약 읽기","성과를 보기 전에 정한 기준입니다. 이 숫자는 수업용 운영 기준이며 보편적인 산업 표준이 아닙니다.",
'''from dataclasses import asdict, replace
display(pd.DataFrame(asdict(DEFAULT).items(), columns=["설정", "값"]))''',
"A/B 50:50, 각 1000명, 14일, 30분 결과 관찰 창을 확인합니다.","p95 기준을 결과 확인 뒤 높이면 어떤 문제가 생길까요?"),
("변경 하나와 가설","A는 짧은 직접 답변, B는 조건·비용·다음 행동입니다. 모델·정책 원문·대상·기능은 같게 둡니다.",
'''hypothesis = {"change": "답변 구성 A → B", "unit": "첫 실험 진입 사용자", "primary": "30분 내 해결 확인 사용자 / 진입 사용자", "guardrails": "p95 ≤ 1800ms, 오류율 ≤ 3%", "expected_reason": "다음 행동 이해 개선"}
display(pd.Series(hypothesis))''',
"확인 지표와 기대 이유를 분리했습니다.","모델과 프롬프트를 동시에 바꾸면 어떤 변경의 효과인지 알 수 있나요?"),
("동일 사용자 재방문","Python의 기본 hash는 실행 간 고정되지 않을 수 있습니다. 실습은 SHA-256 해시로 배정합니다.",
'''visits = pd.DataFrame({"visitor_id": ["u-alpha"]*4 + ["u-beta"]*4})
visits["variant"] = visits.visitor_id.map(assign)
display(visits)
assert visits.groupby("visitor_id").variant.nunique().max() == 1''',
"같은 ID의 모든 방문에서 같은 버전입니다.","요청할 때마다 동전을 던지면 같은 사람의 경험이 어떻게 달라질까요?"),
("2400명 배정 확인","개별 사용자의 버전이 안정적이어도 전체 비율은 정확히 1200:1200일 필요가 없습니다.",
'''users = pd.DataFrame({"visitor_id": [f"u-{i:05d}" for i in range(2400)]})
users["variant"] = users.visitor_id.map(assign)
display(users.variant.value_counts().rename("사용자 수"))
from week12.lab.analysis import srm_test
counts = users.variant.value_counts()
print(srm_test(int(counts["A"]), int(counts["B"])))''',
"A 1196명, B 1204명이며 SRM p-value는 약 0.870입니다.","8명 차이가 있다는 사실만으로 버그라고 판단해도 될까요?"),
("실험 중 배정 비율 변경","설정을 50:50에서 80:20으로 바꾸면 같은 사용자도 다른 버전이 될 수 있습니다. 수업 구현은 실험 계약을 고정합니다.",
'''changed = replace(DEFAULT, allocation_b=.2)
users["new_variant"] = users.visitor_id.map(lambda u: assign(u, changed))
print("버전 변경 사용자:", int((users.variant != users.new_variant).sum()))
print("기존/변경 설정:", DEFAULT.version, changed.version)''',
"설정 버전과 일부 사용자 배정이 달라집니다.","점진 배포 트래픽 비율과 실험 내부의 A/B 비율을 왜 분리할까요?"),
("요청 수와 사용자 수의 차이","한 사용자의 반복 요청은 독립 사용자를 추가하지 않습니다. metric의 분모를 미리 고정합니다.",
'''data = load_units("slow")
display(data.groupby("variant").agg(users=("visitor_id","nunique"), requests=("requests","sum")))
print("분석은 사용자 한 명당 첫 요청 결과 한 건입니다.")''',
"요청 수는 사용자 수보다 큽니다.","요청이 많은 몇 명에게 결론이 좌우되지 않으려면 어떻게 집계할까요?")],
"종이에 실험 가설을 4줄로 적고, 실험 ID·설정 버전을 바꾸어 배정이 달라지는지 복습합니다. 다음은 실제 API에서 이 계약을 지키는지 확인합니다.")

build("02_service_events.ipynb","02 · API·이벤트·중복 방지",12,
"9주차 API 계약과 10주차 운영 기록을 사용자 단위 실험으로 연결합니다.",[
("격리된 실습 API","TestClient는 실제 FastAPI 경로·검증·SQLite 저장을 호출합니다. TCP 네트워크나 실제 고객 트래픽을 재현한 것은 아닙니다.",
'''from tempfile import TemporaryDirectory
from fastapi.testclient import TestClient
from week12.lab.service import create_app
temp = TemporaryDirectory(prefix="w12-notebook-")
client = TestClient(create_app(Path(temp.name)/"events.sqlite3"))
print(client.get("/health").json())''',
"status=ok와 실험 설정 버전이 보입니다.","HTTP 계약 검증과 운영 환경 부하 검증은 무엇이 다른가요?"),
("두 버전의 실제 API 응답","서버가 버전을 정합니다. 사용자가 마음대로 B를 고르면 비교 집단이 달라집니다.",
'''ids = {v: next(f"u-{i}" for i in range(100) if assign(f"u-{i}")==v) for v in ["A","B"]}
responses = {}
for variant, uid in ids.items():
    payload = {"visitor_id":uid,"request_id":f"req-{variant}","topic":"exchange","provider":"template"}
    response = client.post("/api/answer", json=payload)
    assert response.status_code == 200
    responses[variant] = response.json()
    print(variant, response.json()["answer"])
print("정책 템플릿 실행: 여기서는 모델을 호출하지 않았습니다.")''',
"A와 B의 구성은 다르지만 정책 기간과 비용은 같습니다.","응답 모양이 달라도 반드시 같아야 할 사실은 무엇인가요?"),
("같은 요청의 재전송","재시도는 흔합니다. 같은 request_id를 그대로 재전송하면 결과만 재사용하며 기록을 늘리지 않습니다.",
'''same = {"visitor_id":ids["A"],"request_id":"req-A","topic":"exchange","provider":"template"}
print(client.post("/api/answer", json=same).json()["replayed"])
assert len(client.get("/api/events").json()) == 2
conflict = client.post("/api/answer", json={**same,"topic":"return"})
print("서로 다른 요청에 ID 재사용:", conflict.status_code)
assert conflict.status_code == 409''',
"동일 요청 재전송은 True, 내용 변경 재사용은 409입니다.","중복 이벤트가 주로 B에서 발생하면 배정 비율은 어떻게 보일까요?"),
("사용자 피드백과 분모","해결 확인은 사용자 피드백이며 모델 judge 점수가 아닙니다. 미응답은 확인 없음으로 남깁니다.",
'''print(client.post("/api/feedback",json={"request_id":"req-B","resolved":True}).json())
summary = client.get("/api/summary").json()
display(pd.DataFrame(summary["arms"]).T)
print(summary["decision"], summary["reasons"])''',
"사용자 2명의 결과이며 WAIT입니다. A의 미응답은 분모에서 사라지지 않습니다.","두 번의 요청에서 B의 비율이 높다고 배포할 수 있나요?"),
("이벤트 원본과 운영 지표","동일 요청에 ID·할당·실제 제공 버전·오류·지연을 남깁니다. metrics는 요청 수, 분석은 사용자 수를 사용합니다.",
'''display(pd.DataFrame(client.get("/api/events").json())[["request_id","visitor_id","assigned_variant","served_variant","status","latency_ms","resolved"]])
print(client.get("/metrics").text)''',
"Prometheus가 읽을 수 있는 지표 텍스트가 출력됩니다. Prometheus 서버 자체를 띄운 것은 아닙니다.","p95가 좋아졌다는 운영 관찰만으로 B의 사업 효과를 주장할 수 있나요?"),
("긴급 중단 스위치","운영 위험이 있으면 새 요청을 A로 되돌립니다. 중단 뒤 기록을 기존 A/B 효과 분석에 합치지 않습니다.",
'''print(client.post("/api/control",json={"enabled":False}).json())
rolled = client.post("/api/answer",json={"visitor_id":ids["B"],"request_id":"req-rollback","topic":"exchange","provider":"template"}).json()
print("원래 배정 / 실제 제공:", rolled["assigned_variant"], rolled["variant"])
print(client.get("/api/summary").json())''',
"원래 B였던 사용자에게 A를 제공하고, 혼합 결과 분석은 INVALID입니다.","운영 복구가 성공했다는 사실과 실험이 유효하다는 사실은 같은가요?"),
("API 계약의 잘못된 입력","새로운 모델을 붙이기 전에 요청·응답 계약을 유지해야 합니다.",
'''bad = client.post("/api/answer", json={"visitor_id":"name@example.com","request_id":"invalid","topic":"exchange"})
print("잘못된 실습 ID:",bad.status_code)
assert bad.status_code == 422
client.close()
temp.cleanup()
print("Notebook 임시 DB 정리 완료")''',
"422가 반환되고 Notebook의 임시 DB가 정리됩니다.","서비스의 입력 검증이 실험 신뢰성과 개인정보 보호에 어떤 역할을 하나요?")],
"**실제 화면 실행:** VS Code 터미널에서 `python -m uvicorn week12.lab.service:app --host 127.0.0.1 --port 8012`를 실행하고 http://127.0.0.1:8012 를 엽니다. 요청 → 피드백 → 결과 확인 → 중단 스위치 순서로 시연합니다. 이 로컬 제어 API에는 운영용 인증이 없으므로 외부 공개 서버로 실행하지 않습니다.")

build("03_data_quality_srm.ipynb","03 · 사용자 집계와 SRM",9,
"좋아 보이는 지표를 해석하기 전에 데이터의 신뢰성을 확인합니다.",[
("종료된 합성 스냅샷","가상 14일 실험의 사용자별 첫 요청 결과입니다. 합성 데이터 생성 규칙은 공개 코드에 있습니다.",
'''data = load_units("healthy")
display(data.head())
metadata = json.loads((ROOT/"week12/lab/data/metadata.json").read_text())
print(metadata["notes"])''',
"2400명 중 A 1196명·B 1204명입니다.","이 데이터로 실제 제품 효과를 주장하면 왜 잘못인가요?"),
("집계 계약 검증","결측·중복·잘못된 버전은 계산 전에 막습니다. 무조건 dropna로 지우지 않습니다.",
'''from week12.lab.analysis import validate_units
assert validate_units(data) == []
duplicate = pd.concat([data,data.iloc[[0]]],ignore_index=True)
print(validate_units(duplicate))
assert analyze(duplicate)["decision"] == "INVALID"''',
"중복 사용자를 추가하면 INVALID입니다.","반복 요청을 사용자가 늘어난 것으로 세면 신뢰구간에 어떤 문제가 생기나요?"),
("정상 배정과 비율 불일치","SRM은 Sample Ratio Mismatch, 설정한 배정 비율과 관찰한 사용자 비율의 불일치입니다. 원인을 알려주는 판결이 아니라 진단 신호입니다.",
'''from week12.lab.analysis import srm_test
for name in ["healthy","srm"]:
    frame = load_units(name)
    n = frame.variant.value_counts()
    result = srm_test(int(n["A"]),int(n["B"]))
    print(name,n.to_dict(),result)''',
"정상 p≈0.870, 누락 사례 p는 매우 작습니다.","B의 효과가 좋아 보이더라도 먼저 무엇을 멈춰야 하나요?"),
("원래 배정과 수집 결과 대조","이 사례는 B 사용자 일부를 의도적으로 누락한 예시입니다. 배정 로직이 정확해도 수집·조인·필터에서 편향이 생깁니다.",
'''broken = load_units("srm")
missing = data[~data.visitor_id.isin(broken.visitor_id)]
display(missing.groupby("variant").size().rename("누락 사용자"))
report = analyze(broken)
print(report["decision"], report["reasons"])
assert report["effect"] is None''',
"B 602명 누락, 효과 구간을 출력하지 않고 해석을 중단합니다.","누락된 사람은 무작위 일부일까요, 특정 결과를 경험한 사람일까요?"),
("성공 응답만 남기는 함정","실패 사용자를 지우면 관찰 대상이 결과에 의해 바뀝니다. 오류는 분모에 남기고 운영 기준으로도 봅니다.",
'''all_users = data.groupby("variant").resolved.mean()
only_ok = data[data.error==0].groupby("variant").resolved.mean()
display(pd.DataFrame({"진입 사용자 전체":all_users,"성공 응답만":only_ok}))
display(data.groupby("variant")[["error","feedback_received"]].mean())''',
"실패를 제거한 비율은 정의가 바뀌었습니다. 비슷한 숫자여도 같은 지표가 아닙니다.","‘답변한 사람 중 만족 비율’과 ‘전체 진입자 중 해결 확인율’의 분모는 어떻게 다른가요?"),
("관찰 지표와 사람의 행동","피드백 미응답은 실제 해결 실패를 뜻하지 않습니다. 수집률과 별도 사용성 관찰을 함께 봅니다.",
'''observed = data[data.feedback_received==1].groupby("variant").resolved.mean()
display(pd.DataFrame({"전체 사용자 해결 확인율":all_users,"피드백 응답자 내 비율":observed}))
print("응답자만의 만족도와 전체 사용자 지표를 혼동하지 않습니다.")''',
"서로 다른 두 비율이 나옵니다.","B에서 피드백 버튼이 더 잘 보이도록 바꾸면 어떤 측정 변화가 생길까요?")],
"MSN의 이미지 카드 실험 사례와 비교해 보세요. 결과에 영향받은 사용자만 필터링되면 판단 방향까지 바뀔 수 있습니다. 다음 Notebook은 유효한 데이터의 불확실성과 운영 기준을 함께 봅니다.")

build("04_effect_and_release.ipynb","04 · 효과·불확실성·배포 판단",12,
"해결 확인율 상승과 지연 악화가 공존할 때 근거를 설명합니다. 이번 과제의 핵심 파일입니다.",[
("과제 사례 불러오기","slow는 정상 A/B 배정이지만 B의 지연이 큰 사례입니다. 여기서 구한 수치를 과제에 그대로 사용할 수 있습니다.",
'''data = load_units("slow")
report = analyze(data)
display(pd.DataFrame(report["arms"]).T)
print(report["decision"], report["reasons"])''',
"A 해결 확인율 약 55.0%, B 약 64.0%, B p95 약 2868ms, 결론 HOLD입니다.","해결 확인율이 약 9%p 높아져도 배포를 보류하는 이유는 무엇인가요?"),
("절대 차이와 상대 개선","퍼센트포인트(%p)와 상대 비율(%)을 구분합니다. 같은 결과를 두 방식으로 표현할 수 있습니다.",
'''a,b = report["arms"]["A"],report["arms"]["B"]
absolute = b["rate"]-a["rate"]
relative = absolute/a["rate"]
print(f"절대 차이 {100*absolute:.2f}%p / 상대 개선 {100*relative:.2f}%")''',
"절대 차이는 약 9.02%p, 상대 개선은 약 16.4%입니다.","9%와 9%p를 구분하지 않으면 어떤 오해가 생기나요?"),
("95% 구간 직접 확인","독립 사용자의 이진 지표에 Newcombe–Wilson 방법을 사용합니다. 확률 95%로 특정 참값이 있다는 뜻으로 해석하지 않습니다.",
'''from week12.lab.analysis import difference_interval
interval = difference_interval(a["resolved"],a["n"],b["resolved"],b["n"])
print({k:round(100*interval[k],2) for k in ["difference","low","high"]}, "%p")
assert interval["low"] > 0''',
"95% 구간은 약 [5.10, 12.91]%p입니다.","이 구간이 양수라는 사실만으로 지연 문제를 무시해도 될까요?"),
("판단 조건의 순서","데이터 불량 → 해석 중단, 위험 → 보류, 계획 미달 → 대기, 효과 불확실 → 결론 유보, 통과 → 사람 검토입니다.",
'''results = {name: analyze(load_units(name)) for name in ["healthy","slow","srm"]}
display(pd.DataFrame([{"사례":name,"판단":r["decision"],"이유":" / ".join(r["reasons"])} for name,r in results.items()]))
print("healthy라도 REVIEW이지 자동 배포가 아닙니다.")''',
"REVIEW / HOLD / INVALID를 각각 확인합니다.","11주차 HOLD·REVIEW에 12주차 WAIT·INVALID가 추가된 이유는 무엇인가요?"),
("표본·기간과 중간 결과","효과가 보이기 시작했다는 이유로 종료일을 당기지 않습니다. 운영 장애로 중단하는 것과 성과 승리 선언을 구분합니다.",
'''valid = load_units("healthy")
print("2일 중간 결과:",analyze(valid,elapsed_days=2)["decision"])
print("관찰 창 미완료:",analyze(valid,outcomes_mature=False)["decision"])
print("지연 위험 조기 중단:",analyze(data,elapsed_days=2)["decision"])''',
"WAIT / WAIT / HOLD입니다.","왜 성과 판단은 기다리지만 심한 오류나 지연은 바로 중단할 수 있나요?"),
("작은 효과와 필요한 표본 · 심화","이진 지표·50:50 배정·양측 5%·검정력 80%의 근사 계획입니다. 요청 수가 아니라 독립 사용자 수입니다.",
'''from week12.lab.analysis import sample_size
display(pd.DataFrame([{"목표 절대 차이":f"{100*d:.1f}%p","필요 사용자/버전":sample_size(.55,d)} for d in [.10,.05,.025]]))''',
"탐지할 효과를 줄일수록 표본 요구량이 크게 늘어납니다.","사용자 20명으로 작지만 유용한 효과를 확정하기 어려운 이유는 무엇인가요?"),
("매일 유의성 확인 후 종료 · 심화","실제 효과가 없는 가상 세계를 반복합니다. 매일의 일반 p-value를 보고 유의하면 멈추는 규칙은 고정 시점 보장을 유지하지 않습니다.",
'''from week12.lab.analysis import peeking_demo
peek = peeking_demo()
display(pd.Series(peek))''',
"한 번의 종료 시점 판정보다 매일 확인한 거짓 양성 비율이 높습니다. 값은 시뮬레이션의 seed와 반복 수에 종속됩니다.","순차 검정은 매일 일반 검정을 반복하는 것과 무엇이 달라야 할까요?"),
("내 판단 근거 저장","숫자 하나보다 결론·근거·다음 행동을 남깁니다. 과제는 한 페이지면 충분합니다.",
'''out = ROOT/"week12/lab/reports"
out.mkdir(exist_ok=True,parents=True)
(out/"my-slow-result.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
decision_note = {"결론":"HOLD", "주요 근거":"B 해결 확인율 상승, p95 1800ms 기준 위반", "다음 변경":"출력 길이를 줄이고 오프라인 회귀 평가 후 새 실험", "한계":"합성 데이터이며 실제 제품 성과가 아님"}
display(pd.Series(decision_note))
print(out/"my-slow-result.json")''',
"결과 JSON이 reports 폴더에 저장됩니다. 판단 문장은 자신의 말로 보완하세요.","답변 길이를 줄인 다음 11주차의 어떤 검사를 다시 실행해야 할까요?")],
"결과를 맞추기 위해 p95 기준을 3000ms로 바꾸지 마세요. 변경안의 품질·속도를 다시 확인한 뒤 새 실험으로 검증합니다. 9–12주차 과제는 02번의 요청 기록 한 장과 이 파일의 slow 결과로 완성할 수 있습니다.")

build("05_ollama_and_report.ipynb","05 · 실제 Ollama 응답과 검토 보고서",10,
"동일 모델의 실제 A/B 응답을 보고, 개별 답변 품질과 사용자 실험 효과를 구분합니다.",[
("실제 모델 호출 선택","Ollama는 11주차의 작은 Instruct 모델을 재사용합니다. API 키나 Docker가 필요 없습니다. 모델이 없으면 `ollama pull qwen2.5:1.5b-instruct`를 먼저 실행하세요.",
'''RUN_OLLAMA = os.getenv("W12_RUN_OLLAMA", "1") == "1"
print("실제 모델 호출" if RUN_OLLAMA else "명시적 건너뛰기: 실제 LLM 생성 없음")
from week12.lab.ollama import generate, MODEL
print("모델:",MODEL,"/ temperature 0 / num_predict 128 / think false")''',
"기본값은 실제 Ollama 호출입니다. 필요하면 RUN_OLLAMA=False로 다음 셀의 모델 호출만 건너뜁니다.","빠른 instruct 모델을 써도 어떤 내용 검토가 필요할까요?"),
("같은 질문의 실제 A/B 응답","두 번만 생성합니다. 지연에는 첫 모델 로딩도 포함될 수 있어 버전별 속도 벤치마크로 쓰지 않습니다.",
'''live = []
if RUN_OLLAMA:
    try:
        for variant in ["A","B"]:
            result = generate("exchange", variant)
            live.append({"variant":variant, **result})
            print(variant,result["answer"],"\\n")
    except (RuntimeError,ValueError) as exc:
        print("실제 호출 미완료:",exc)
        print("가상 응답으로 대체하지 않습니다. Ollama 상태를 확인한 후 셀 재실행.")
else:
    print("SKIP: 실제 모델 미실행")''',
"모델이 실행 중이면 두 개의 실제 답변이 나옵니다. 연결 실패 시 성공한 것처럼 표시하지 않습니다.","두 답변 중 마음에 드는 것을 고르는 것과 사용자 A/B 실험은 왜 다른가요?"),
("11주차 품질 기준으로 재검토","기간·배송비·재고 조건을 사람이 확인합니다. 포함 여부 검사는 의미 정확성을 보장하지 않습니다.",
'''if live:
    checks = [{"variant":r["variant"],"7일 문자열":"7" in r["answer"],"6000원 문자열":"6000" in r["answer"].replace(",",""),"재고 문자열":"재고" in r["answer"],"종료 이유":r["done_reason"],"실제 응답":r["answer"]} for r in live]
    display(pd.DataFrame(checks))
    print("문자열 검사와 사람의 의미 검토를 구분합니다. done_reason=length는 잘림 가능성.")
else:
    print("실제 생성 결과 없음: 표를 만들지 않습니다.")''',
"실제 출력의 누락·잘림을 확인합니다. False를 억지로 True로 바꾸지 않습니다.","조건이 빠진 B를 온라인 실험에 바로 넣으면 어떤 위험이 있나요?"),
("실제 실행 증거 저장","모델 응답과 합성 사용자 실험 결과는 다른 파일에 보관합니다. 사용자의 답변 만족도를 생성 결과에서 만들어내지 않습니다.",
'''out = ROOT/"week12/lab/reports"
out.mkdir(exist_ok=True,parents=True)
if live:
    (out/"my-ollama-responses.json").write_text(json.dumps({"source":"actual_local_ollama","responses":live},ensure_ascii=False,indent=2))
    print(out/"my-ollama-responses.json")
else:
    print("실제 응답 파일 저장 생략")''',
"실제 호출이 있었을 때만 실제 응답 파일을 저장합니다.","이 파일만으로 ‘B가 해결률을 9%p 높였다’고 말할 수 있나요?"),
("합성 사례 보고서 재생성","이 보고서는 교수 작성 2400명 스냅샷의 계산 결과입니다. 방금 생성한 실제 응답과 합치지 않습니다.",
'''from week12.lab.report import build_reports
reports = build_reports(out)
print({k:v["report"]["decision"] for k,v in reports.items()})
print("브라우저에서 열 파일:",out/"report.html")''',
"healthy REVIEW, slow HOLD, srm INVALID가 재현됩니다.","왜 실습 서비스 화면과 종료된 합성 실험 보고서를 따로 제공할까요?"),
("다음 변경의 실행 순서","출력 길이 축소는 속도를 개선할 수도 있지만 근거 누락을 만들 수 있습니다. 새 설정은 기존 실험 기록과 분리합니다.",
'''next_plan = pd.DataFrame([
    ["09 API","request_id·응답 계약 유지"],
    ["10 운영","오류·지연·중단 상태 기록"],
    ["11 품질","기간·비용·재고 조건 회귀 평가"],
    ["12 실험","새 버전·새 ID로 배정·사용자 결과 비교"],
],columns=["단원","다음 확인"])
display(next_plan)''',
"한 번의 변경이 9–12주차 전체 검증 흐름으로 연결됩니다.","다음 실험을 시작하기 전에 문서에 먼저 고정할 것은 무엇인가요?")],
"과제에서 실제 Ollama 호출은 선택입니다. 필수는 API 기록 한 장과 합성 slow 사례의 판단 한 페이지입니다. 모델이 느리면 01–04 핵심 경로를 먼저 완료하고 05를 복습하세요.")

if __name__ == "__main__":
    import json
    (OUT.parent/"notebook-guide.json").write_text(json.dumps(INDEX,ensure_ascii=False,indent=2))
    print({"notebooks":len(INDEX),"cells":sum(x["cells"] for x in INDEX),"code_cells":sum(x["code_cells"] for x in INDEX)})
