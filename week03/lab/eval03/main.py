"""Loopback-only EVAL/03 API and teaching workspace."""

from collections import OrderedDict
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .contracts import DecisionRequest, EvaluationRequest
from .core import LAB_ROOT, REQUIRED_SECTIONS, VERSIONS, fingerprint, load_dataset, load_prompt
from .experiments import run_evaluation

app = FastAPI(title="EVAL/03 · 프롬프트 평가와 오류 분류", version="1.0.0")
RUNS: OrderedDict[str, dict] = OrderedDict()


@app.get("/health")
def health():
    return {"status": "ok", "service": "EVAL/03", "provider": "fixed-teaching-fixtures-v1"}


@app.get("/api/catalog")
def catalog():
    dataset = load_dataset()
    return {
        "versions": [
            {"id": version, "name": name, "prompt_hash": fingerprint(load_prompt(version))}
            for version, name in VERSIONS.items()
        ],
        "dataset": dataset,
        "dataset_hash": fingerprint(dataset),
        "required_sections": REQUIRED_SECTIONS,
    }


@app.get("/api/prompt/{version}")
def prompt(version: str):
    if version not in VERSIONS:
        raise HTTPException(404, "해당 버전이 없습니다.")
    template = load_prompt(version)
    return {
        "version": version,
        "name": VERSIONS[version],
        "template": template,
        "prompt_hash": fingerprint(template),
    }


@app.post("/api/evaluations")
def evaluate(request: EvaluationRequest):
    report = run_evaluation(request)
    RUNS[report["run_id"]] = report
    while len(RUNS) > 30:
        RUNS.popitem(last=False)
    return report


@app.post("/api/decisions")
def decision(request: DecisionRequest):
    report = RUNS.get(request.run_id)
    if report is None:
        raise HTTPException(404, "평가 실행 기록이 없습니다. 서버 재시작 시 기록은 초기화됩니다.")
    if request.version not in report["versions"]:
        raise HTTPException(400, "실행한 버전만 결정할 수 있습니다.")
    record = {
        "created_at": datetime.now(UTC).isoformat(),
        "version": request.version,
        "decision": request.decision,
        "reason": request.reason,
        "scope": "educational_candidate_only",
        "deployed": False,
    }
    report["decisions"].append(record)
    return record


@app.get("/api/evaluations/{run_id}/export")
def export(run_id: str):
    report = RUNS.get(run_id)
    if report is None:
        raise HTTPException(404, "평가 실행 기록이 없습니다.")
    return JSONResponse(
        report,
        headers={
            "Content-Disposition": f'attachment; filename="eval03-{run_id}.json"',
            "Cache-Control": "no-store",
        },
    )


app.mount("/static", StaticFiles(directory=LAB_ROOT / "eval03" / "static"), name="static")


@app.get("/")
def index():
    return FileResponse(LAB_ROOT / "eval03" / "static" / "index.html")
