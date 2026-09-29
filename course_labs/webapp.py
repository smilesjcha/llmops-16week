"""Small lab UI. Trusted local teaching roles are NOT authentication controls."""

from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from course_labs.retrieval import answer_from_evidence, evaluate, retrieve


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    method: Literal["bm25", "tfidf", "rrf"] = "bm25"
    size: int = Field(default=120, ge=30, le=600)
    overlap: int = Field(default=24, ge=0, le=200)
    k: int = Field(default=3, ge=1, le=8)
    as_of: str = "2026-09-29"
    role: Literal["public", "staff"] = "public"
    expand: bool = False
    rerank: bool = False


def create_app(week: int) -> FastAPI:
    app = FastAPI(title=f"LLMOps W{week:02d} Retrieval Lab")

    @app.get("/", response_class=HTMLResponse)
    def home():
        return (
            (Path(__file__).parent / "web/index.html")
            .read_text()
            .replace("__WEEK__", f"{week:02d}")
        )

    @app.get("/health")
    def health():
        return {"status": "ok", "week": week, "mode": "offline", "synthetic_data": True}

    @app.post("/api/search")
    def search(req: SearchRequest):
        from fastapi import HTTPException

        try:
            report = retrieve(**req.model_dump())
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return {**report, "answer": answer_from_evidence(report)}

    @app.post("/api/evaluate")
    def eval_report(req: SearchRequest):
        from fastapi import HTTPException

        options = req.model_dump(exclude={"query", "as_of", "role"})
        try:
            return evaluate(**options)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app
