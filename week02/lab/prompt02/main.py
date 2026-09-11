"""PROMPT/02 API. Run on loopback with the course Python environment."""

from collections import OrderedDict
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .contracts import DecisionRequest, ExperimentRequest, TicketResult
from .core import LAB_ROOT, VERSION_NAMES, fingerprint, load_dataset, load_prompt, render_prompt
from .experiments import run_experiment
from .providers import OllamaProvider, ProviderError

app = FastAPI(title="PROMPT/02 · 프롬프트 비교 실습", version="1.0.0")
RUNS: OrderedDict[str, dict] = OrderedDict()


@app.get("/health")
def health():
    return {"status": "ok", "service": "PROMPT/02", "default_provider": "demo"}


@app.get("/api/catalog")
def catalog():
    dataset = load_dataset()
    try:
        ollama_config = OllamaProvider().config()
    except ProviderError as exc:
        ollama_config = {"error": str(exc)}
    return {
        "versions": [
            {"id": version, "name": name, "prompt_hash": fingerprint(load_prompt(version))}
            for version, name in VERSION_NAMES.items()
        ],
        "dataset": dataset,
        "dataset_hash": fingerprint(dataset),
        "output_schema": TicketResult.model_json_schema(),
        "ollama": ollama_config,
    }


@app.get("/api/prompt/{version}")
def prompt_preview(version: str, case_id: str = "T01"):
    case = next((item for item in load_dataset()["cases"] if item["id"] == case_id), None)
    if case is None or version not in VERSION_NAMES:
        raise HTTPException(404, "해당 사례 또는 버전이 없습니다.")
    return render_prompt(version, case)


@app.post("/api/experiments")
async def experiment(request: ExperimentRequest):
    try:
        report = await run_experiment(request)
    except (ValueError, ProviderError) as exc:
        raise HTTPException(400, str(exc)) from exc
    RUNS[report["run_id"]] = report
    while len(RUNS) > 30:
        RUNS.popitem(last=False)
    return report


@app.get("/api/experiments/{run_id}/export")
def export(run_id: str):
    if run_id not in RUNS:
        raise HTTPException(404, "실험 기록이 없습니다. 서버 재시작 시 기록은 초기화됩니다.")
    return JSONResponse(
        RUNS[run_id],
        headers={
            "Content-Disposition": f'attachment; filename="prompt02-{run_id}.json"',
            "Cache-Control": "no-store",
        },
    )


@app.post("/api/decisions")
def decide(request: DecisionRequest):
    if request.run_id not in RUNS:
        raise HTTPException(404, "실험 기록이 없습니다.")
    report = RUNS[request.run_id]
    if request.version not in report["versions"]:
        raise HTTPException(400, "해당 실험에 포함된 버전만 선택할 수 있습니다.")
    record = {
        "created_at": datetime.now(UTC).isoformat(),
        "version": request.version,
        "reason": request.reason,
        "scope": "educational_candidate_only",
        "deployed": False,
        "simulation": report["simulation"],
        "prompt_hash": next(
            row["prompt_hash"] for row in report["rows"] if row["version"] == request.version
        ),
    }
    if len(report["decisions"]) >= 20:
        raise HTTPException(409, "한 실험의 결정 기록은 20개까지 보관합니다. 새 실험을 시작하세요.")
    report["decisions"].append(record)
    return record


app.mount("/static", StaticFiles(directory=LAB_ROOT / "prompt02" / "static"), name="static")


@app.get("/")
def index():
    return FileResponse(LAB_ROOT / "prompt02" / "static" / "index.html")
