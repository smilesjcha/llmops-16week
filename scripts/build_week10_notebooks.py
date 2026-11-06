"""Build independent, output-free teaching notebooks; all fixtures are synthetic."""

from pathlib import Path
import textwrap
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
SETUP = """
from pathlib import Path
import sys
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "week10/lab/app.py").exists())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import asyncio, json
from dataclasses import replace
from week10.lab.config import Settings
from week10.lab.experiments import lab_client, fixture_check, window_delta, compare_releases
"""


def make(name, title, intro, cells):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell(
            f"# {title}\n\n{intro}\n\n**실행:** Python 3.11 공통 .venv 커널에서 위→아래. 다른 Notebook·서버·Docker·모델 설치 없이 독립 실행. 코드는 MOCK 고정 문장·대기만 사용한다. 실제 LLM 품질·처리량 측정이 아니다."
        ),
        nbf.v4.new_code_cell(textwrap.dedent(SETUP).strip()),
    ]
    for heading, explanation, code in cells:
        nb.cells += [
            nbf.v4.new_markdown_cell(f"## {heading}\n\n{explanation}"),
            nbf.v4.new_code_cell(textwrap.dedent(code).strip()),
        ]
    nb.cells += [
        nbf.v4.new_markdown_cell(
            "## 프로젝트 적용 기록\n\n예상 → 관찰 → 근거 → 다음 변경을 한 줄씩 기록한다. 실제로 실행하지 않은 조건은 미측정으로 표시한다. 학생 정보나 원문 입력은 공개 저장소에 올리지 않는다."
        )
    ]
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3.11 (.venv)",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3.11"},
    }
    path = ROOT / "week10/lab/notebooks" / name
    path.write_text(nbf.writes(nb), encoding="utf-8")
    print(name, len(nb.cells), "cells")


make(
    "01_release_configuration.ipynb",
    "01 · 배포 버전과 실행 설정",
    "목표: 같은 코드의 설정 차이를 식별하고 시작·준비·종료 상태를 확인한다. 약12분.",
    [
        (
            "기본 설정",
            "릴리스·프롬프트·모델·데이터가 따로 기록되는 이유를 설명해본다.",
            "cfg = Settings()\nmanifest = cfg.manifest()\nmanifest",
        ),
        (
            "설정의 동일성",
            "같은 입력은 같은 config_id다. 코드 commit이나 이미지 digest를 대신하는 값은 아니다.",
            'assert manifest == Settings().manifest()\nchanged = replace(cfg, timeout_s=0.5)\nassert changed.manifest()["config_id"] != manifest["config_id"]\nchanged.manifest()',
        ),
        (
            "시작 전 실패",
            "오타·NaN·과도한 처리량을 조용히 수용하지 않는다.",
            'for values in [{"release":"latest"}, {"timeout_s":float("nan")}, {"capacity":0}]:\n    try:\n        Settings(**values)\n    except ValueError as e:\n        print(type(e).__name__, str(e))\n    else:\n        raise AssertionError("invalid configuration accepted")',
        ),
        (
            "앱의 수명주기",
            "ASGITransport는 startup을 자동 실행하지 않는다. lab_client가 lifespan을 명시적으로 연다.",
            'from week10.lab.app import create_app\napp = create_app(cfg)\nassert not app.state.started\nasync with lab_client(cfg) as (running, client):\n    print((await client.get("/health/live")).json())\n    assert (await client.get("/health/ready")).status_code == 200\nassert not running.state.started and running.state.draining',
        ),
        (
            "버전 응답",
            "요청 결과의 release와 서버 manifest를 대조한다.",
            'async with lab_client(cfg) as (app, client):\n    r = await client.post("/api/v1/assist", json={"message":"신청 절차"})\n    assert r.headers["X-Release"] == (await client.get("/release")).json()["release"]\n    print(r.json())',
        ),
        (
            "컨테이너 실행 경로",
            "파일을 읽기만 한다. Docker 설치·다운로드·데몬 실행을 자동 수행하지 않는다.",
            'dockerfile = (ROOT / "week10/lab/Dockerfile").read_text()\nprint(dockerfile)\nassert "USER 10001" in dockerfile and "--host" in dockerfile',
        ),
        (
            "내 설정의 경계",
            "동시 처리량을 1·2로 바꿔 manifest 차이를 확인한다. 다음 장에서 실제 거절 수를 관찰한다.",
            "for cap in [1, 2]:\n    print(Settings(capacity=cap).manifest())",
        ),
    ],
)
make(
    "02_logs_correlation.ipynb",
    "02 · 구조화 로그와 요청 연결",
    "목표: 로그를 JSON 필드로 조회하고 요청·추적 ID와 개인정보의 경계를 이해한다. 약12분.",
    [
        (
            "비교 요청",
            "정상·검색 오류·잘못된 입력을 한 번씩 보낸다.",
            'async with lab_client() as (app, client):\n    ok = await client.post("/api/v1/assist", json={"message":"SYNTHETIC-ONLY"})\n    bad = await client.post("/api/v1/assist", json={"message":"예시", "scenario":"retrieval_error"})\n    invalid = await client.post("/api/v1/assist", json={"message":" "})\n    snapshot = app.state.telemetry.snapshot()\nassert [ok.status_code, bad.status_code, invalid.status_code] == [200, 502, 422]',
        ),
        (
            "허용 필드",
            "원문 대신 route·상태·시간·버전을 남긴다.",
            'logs = snapshot["logs"]\nprint(json.dumps(logs, ensure_ascii=False, indent=2))\nassert "SYNTHETIC-ONLY" not in json.dumps(snapshot)',
        ),
        (
            "오류 조회",
            "문자열 검색보다 필드 조건으로 필요한 이벤트를 좁힌다.",
            'errors = [r for r in logs if r["status"] >= 500]\nassert len(errors) == 1\nerrors',
        ),
        (
            "사용자 문의와 연결",
            "X-Request-ID로 해당 실행을 찾는다. 질문 자체를 로그에 복제할 필요가 없다.",
            'rid = bad.headers["X-Request-ID"]\nmatched = [r for r in logs if r["request_id"] == rid]\nassert len(matched) == 1\nmatched[0]',
        ),
        (
            "Trace 연결",
            "같은 trace_id의 span을 모은다. ID는 인증·권한 증명이 아니다.",
            'tid = matched[0]["trace_id"]\nspans = [s for s in snapshot["spans"] if s["trace_id"] == tid]\n[(s["name"], s["status"]) for s in spans]',
        ),
        (
            "라벨 조합의 증가",
            "예시 계산이다. 요청 ID를 지표 라벨에 넣을 때 1만 건만으로 조합 수가 급증한다.",
            'status_values, route_values, request_ids = 6, 4, 10_000\nprint("유한 상태·경로 상한:", status_values * route_values)\nprint("요청 ID까지 곱한 가상 상한:", status_values * route_values * request_ids)\nassert "request_id" not in app.state.telemetry.prometheus()',
        ),
        (
            "메모리 보존 범위",
            "200건 보관과 누적 완료 건수는 다른 값이다. 재시작하면 둘 다 초기화된다.",
            'print(snapshot["retention"])\nassert set(logs[0]) == {"event","timestamp","request_id","trace_id","route","status","duration_ms","release","config_id"}',
        ),
    ],
)
make(
    "03_traces_and_context.ipynb",
    "03 · Span과 단계별 실행 추적",
    "목표: 부모·자식 관계, 실행 시간, 동시 요청의 context 격리를 확인한다. 약15분.",
    [
        (
            "정상 경로",
            "검색·생성·출력을 assist 부모 작업으로 묶는다.",
            'async with lab_client() as (app, client):\n    r = await client.post("/api/v1/assist", json={"message":"신청 절차"})\n    snap = app.state.telemetry.snapshot()\nspans = sorted(snap["spans"], key=lambda s:s["offset_ms"])\n[(s["name"], s["offset_ms"], s["duration_ms"]) for s in spans]',
        ),
        (
            "부모·자식 검증",
            "자식 span은 assist의 span_id를 parent_id로 가진다.",
            'root = next(s for s in spans if s["name"] == "assist")\nchildren = [s for s in spans if s["name"] != "assist"]\nassert all(s["parent_id"] == root["span_id"] for s in children)\nassert all(s["trace_id"] == root["trace_id"] for s in children)',
        ),
        (
            "시간 해석",
            "부모 시간은 자식을 포함한다. 부모+자식 합계는 이중 집계다.",
            'print("부모 실행 ms:", root["duration_ms"])\nprint("자식 합계 ms:", sum(s["duration_ms"] for s in children))\nprint("가장 긴 자식:", max(children, key=lambda s:s["duration_ms"])["name"])',
        ),
        (
            "W3C header의 제한된 예시",
            "00 버전·01 flags의 유효한 context만 전달한다. 전체 표준·샘플러·OTLP 구현이 아니다.",
            'header = "00-" + "a"*32 + "-" + "b"*16 + "-01"\nasync with lab_client() as (app, client):\n    r = await client.post("/api/v1/assist", json={"message":"예시"}, headers={"traceparent":header})\n    root = next(s for s in app.state.telemetry.spans if s["name"] == "assist")\nassert root["trace_id"] == "a"*32 and root["parent_id"] == "b"*16',
        ),
        (
            "잘못된 context",
            "올제로 ID나 지원하지 않는 버전은 새 ID로 시작한다.",
            'from week10.lab.telemetry import trace_context\nfor h in ["not-a-header", "00-"+"0"*32+"-"+"b"*16+"-01"]:\n    tid, parent = trace_context(h)\n    assert int(tid,16)>0 and parent is None\n    print(tid)',
        ),
        (
            "동시 요청 격리",
            "한 context 전역 변수를 공유할 때의 오염을 ContextVar로 피한다.",
            'async with lab_client(Settings(capacity=2)) as (app, client):\n    responses = await asyncio.gather(*[client.post("/api/v1/assist", json={"message":str(i)}) for i in range(2)])\n    snap = app.state.telemetry.snapshot()\ntids = {r.headers["X-Trace-ID"] for r in responses}\nassert len(tids) == 2\nassert all(len([s for s in snap["spans"] if s["trace_id"] == tid]) == 4 for tid in tids)',
        ),
        (
            "실패 지점",
            "검색 실패 때 generate span이 생기지 않는 이유를 설명한다.",
            'async with lab_client() as (app, client):\n    await client.post("/api/v1/assist", json={"message":"예시","scenario":"retrieval_error"})\n    spans = list(app.state.telemetry.spans)\nassert not any(s["name"] == "generate" for s in spans)\n[(s["name"],s["status"]) for s in spans]',
        ),
    ],
)
make(
    "04_metrics_and_windows.ipynb",
    "04 · 지표·분모·관찰 구간",
    "목표: 누적 counter와 구간 비율을 구분하고 histogram을 읽는다. 약15분.",
    [
        (
            "관찰 전 스냅샷",
            "상태 확인·UI·metrics 조회는 assist 분모에서 제외한다.",
            'async with lab_client() as (app, client):\n    await client.get("/health/live")\n    await client.get("/metrics")\n    before = app.state.telemetry.snapshot()\n    for scenario in ["normal","normal","retrieval_error","provider_error"]:\n        await client.post("/api/v1/assist", json={"message":"예시","scenario":scenario})\n    await client.post("/api/v1/assist", json={"message":" "})\n    after = app.state.telemetry.snapshot()\n    exposition = (await client.get("/metrics")).text\nassert before["total"] == 0 and after["total"] == 5',
        ),
        (
            "기간 차이",
            "5xx/전체 assist 요청으로 2/5를 계산한다. 422 포함 여부를 먼저 명시한다.",
            'delta = window_delta(before, after)\nassert delta["requests"] == 5 and delta["5xx"] == 2\nassert delta["error_rate"] == 0.4\ndelta',
        ),
        (
            "텍스트 노출 형식",
            "counter·gauge·histogram이 어떤 줄인지 찾는다. Prometheus 서버는 띄우지 않는다.",
            'print(exposition)\nassert "trace_id" not in exposition and "request_id" not in exposition',
        ),
        (
            "누적 버킷",
            "le=0.1은 0.1초 이하 전체다. 버킷을 단순 합산하면 중복된다.",
            'buckets = [line for line in exposition.splitlines() if "_bucket" in line]\ncounts = [float(line.split()[-1]) for line in buckets]\nassert counts == sorted(counts) and counts[-1] == 5\nbuckets',
        ),
        (
            "성공 지연과 전체 지연",
            "실패가 빨리 반환되면 전체 평균이 작아질 수 있다. logs는 최근 200건만이다.",
            'success = [r["duration_ms"] for r in after["logs"] if r["status"] == 200]\nall_ms = [r["duration_ms"] for r in after["logs"]]\nprint("성공 평균:",sum(success)/len(success), "전체 평균:",sum(all_ms)/len(all_ms))\nprint("분모:", len(success), len(all_ms))',
        ),
        (
            "트래픽 없는 구간",
            "요청0은 100% 성공이 아니라 관측 불충분이다.",
            'assert window_delta(after, after)["error_rate"] is None\ntry:\n    window_delta(after, before)\nexcept ValueError as e:\n    print("재시작/역순 거부:", e)',
        ),
        (
            "알림 판단",
            "수업용 규칙. 운영 SLO·확정 배점이 아니다.",
            'def review_signal(d):\n    return "관측 부족" if d["requests"] < 5 else "원인 확인" if d["error_rate"] > 0.1 else "관찰 유지"\nprint(review_signal(delta))\nprint(review_signal(window_delta(after,after)))',
        ),
    ],
)
make(
    "05_incident_and_recovery.ipynb",
    "05 · 장애 진단과 복구 확인",
    "목표: 상태→영향→Trace→완화→재검증 순서로 장애 기록을 만든다. 약15분.",
    [
        (
            "준비 상태와 생존 상태",
            "의존성 장애에서 프로세스를 무조건 재시작하는 것이 적절한지 토론한다.",
            'async with lab_client() as (app, client):\n    app.state.dependency_ok = False  # test fixture; production control API 아님\n    live = await client.get("/health/live")\n    ready = await client.get("/health/ready")\n    blocked = await client.post("/api/v1/assist", json={"message":"예시"})\nassert [live.status_code,ready.status_code,blocked.status_code] == [200,503,503]',
        ),
        (
            "시간 초과의 원인",
            "정상과 지연 조건을 한 앱에서 비교한다.",
            'async with lab_client() as (app, client):\n    normal = await client.post("/api/v1/assist", json={"message":"예시"})\n    failed = await client.post("/api/v1/assist", json={"message":"예시","scenario":"slow"})\n    snap = app.state.telemetry.snapshot()\nassert failed.status_code == 504 and snap["active"] == 0',
        ),
        (
            "실패 Trace 조회",
            "HTTP 상태만으로 검색 장애·생성 지연을 같은 원인으로 결론내리지 않는다.",
            'tid = failed.headers["X-Trace-ID"]\nfault_trace = [s for s in snap["spans"] if s["trace_id"] == tid]\n[(s["name"],s["duration_ms"],s["status"]) for s in fault_trace]',
        ),
        (
            "복구 실험",
            "주입 조건을 normal로 돌리고 이후 요청의 성공과 active 해제를 함께 본다.",
            'async with lab_client() as (app, client):\n    await client.post("/api/v1/assist", json={"message":"예시","scenario":"slow"})\n    recovered = await client.post("/api/v1/assist", json={"message":"예시"})\n    assert recovered.status_code == 200 and app.state.telemetry.active == 0\n    print(recovered.json())',
        ),
        (
            "수신 중단과 처리 종료",
            "이 앱은 비스트리밍이다. 연결 종료만으로 외부 모델 계산이 멈춘다고 가정하지 않는다.",
            'print("이 실험의 제공자: 고정 문장+asyncio.sleep")\nprint("외부 GPU 취소: 미구현·미측정")',
        ),
        (
            "상태 복원",
            "의존성 fixture 복원 후 ready·정상 응답·기준 통과를 확인한다.",
            'async with lab_client() as (app, client):\n    app.state.dependency_ok = False\n    assert (await client.get("/health/ready")).status_code == 503\n    app.state.dependency_ok = True\n    assert (await client.get("/health/ready")).status_code == 200\n    r = await client.post("/api/v1/assist", json={"message":"예시"})\n    assert fixture_check(r.json()["answer"])',
        ),
        (
            "장애 기록",
            "실측·가설·실험실 조작을 구분한다. 재시작은 영구 해결의 증거가 아니다.",
            'incident = {"symptom":"504", "evidence_trace":tid, "hypothesis":"generate 지연", "mitigation":"주입 조건 normal 복원", "verification":"후속200 + 기준통과 + active0", "remaining":"실제 제공자/장기 관찰 미검증"}\nincident',
        ),
    ],
)
make(
    "06_release_gate_portfolio.ipynb",
    "06 · 배포 전 검증과 기획서 개선",
    "목표: HTTP 성공·내용 기준을 따로 평가하고 배포/중단 결정을 기록한다. 약15분.",
    [
        (
            "릴리스 비교",
            "v2는 의도적으로 잘못된 고정 문장을 내보낸다. 실제 모델 성능 비교가 아니다.",
            "rows = await compare_releases()\nrows",
        ),
        (
            "HTTP와 내용 기준",
            "동일 입력4건씩인 합성 fixture다. 표본을 전체 서비스 정확도로 일반화하지 않는다.",
            'assert [r["http_success"] for r in rows] == [4,4]\nassert [r["fixture_pass"] for r in rows] == [4,0]\n[(r["release"],r["http_success"]/r["requests"],r["fixture_pass"]/r["requests"]) for r in rows]',
        ),
        (
            "배포 차단 조건",
            "이번 fixture 전부 통과를 데모 gate로 사용한다. 운영 기준은 프로젝트에 맞게 별도 정한다.",
            'def gate(row):\n    return row["http_success"] == row["requests"] and row["fixture_pass"] == row["requests"]\nassert gate(rows[0]) and not gate(rows[1])\nprint({r["release"]:gate(r) for r in rows})',
        ),
        (
            "이전 버전 재검증",
            "이전 설정 앱을 새로 시작해 확인하는 로컬 시뮬레이션이다. 실제 트래픽 전환은 수행하지 않는다.",
            'async with lab_client(Settings(release="v1")) as (app, client):\n    r = await client.post("/api/v1/assist", json={"message":"신청 절차"})\n    assert fixture_check(r.json()["answer"])\n    print((await client.get("/release")).json())',
        ),
        (
            "서로 다른 품질 위험",
            "단순 문자열 규칙의 우회 사례를 만든다. 더 나은 평가에는 검수된 정답·다양한 부정 예시가 필요하다.",
            'tricky = "D01 담당자 확인이라고 쓰지만 무조건 승인됩니다."\nassert not fixture_check(tricky)\nprint("규칙은 작은 회귀 방지 장치이며 의미 이해 평가가 아니다.")',
        ),
        (
            "프로젝트 증거의 계층",
            "기획 주장·실행·검증·남은 위험을 연결한다. 새 파일을 자동 저장하거나 기존 작성본을 덮어쓰지 않는다.",
            'record = {"requirement":"신청 절차 안내", "release":"v1", "contract":"200+schema", "content_check":"D01+담당자 확인", "failures":["502","503","504"], "evidence":"실제 실행 결과 첨부", "unverified":"실제 모델·권한·부하·운영배포"}\nrecord',
        ),
        (
            "2차 기획서 제출",
            "2026-11-06 금요일 오늘 제출. 미제출자는 늦어도 2026-11-07 토요일까지. 별도 시각·감점 규칙을 추정하지 않는다.",
            'form = ROOT / "curriculum/2026-2/web/project-portfolio-week10.html"\nassert form.exists()\nprint(form)\nprint("아주대AI대학원: LMS / 군산대·창원대 등 별도 수강생: 공지된 이메일")',
        ),
    ],
)
