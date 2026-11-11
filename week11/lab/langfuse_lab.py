"""Real Ollama calls traced to the local Docker Langfuse stack (SDK 5.2.0).

Run after Docker setup: python -m week11.lab.langfuse_lab
The application computes scores; Langfuse stores and displays them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
import uuid
from pathlib import Path
from urllib.parse import urlparse

import httpx
from dotenv import dotenv_values
from langfuse import Langfuse, propagate_attributes

from .evaluation import Config, Retriever, load_data
from .ollama_lab import (
    ANSWER_SCHEMA,
    PROMPTS,
    OllamaClient,
    inspect_answer,
    judge_answer,
    validate_answer,
)

ENV_FILE = Path(__file__).with_name("langfuse") / ".env"
REPORT_DIR = Path(__file__).with_name("reports") / "langfuse"


def local_settings(path=ENV_FILE):
    """Use this lab's explicit file, never an unrelated cloud key from the shell."""
    values = dotenv_values(path)
    required = ["LANGFUSE_BASE_URL", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"]
    if any(not values.get(key) for key in required):
        raise RuntimeError("먼저 python week11/lab/langfuse/init_env.py를 실행하세요.")
    parsed = urlparse(values["LANGFUSE_BASE_URL"])
    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"localhost", "127.0.0.1", "::1"}
        or parsed.username
        or parsed.password
        or parsed.path
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError(
            "이 실습의 Langfuse 주소는 http://localhost:3011 같은 로컬 주소만 허용합니다."
        )
    return values


def connect_langfuse(path=ENV_FILE):
    config = local_settings(path)
    client = Langfuse(
        base_url=config["LANGFUSE_BASE_URL"],
        public_key=config["LANGFUSE_PUBLIC_KEY"],
        secret_key=config["LANGFUSE_SECRET_KEY"],
        environment="week11-local",
        release="week11-langfuse-v1",
        sample_rate=1.0,
        httpx_client=httpx.Client(timeout=15, trust_env=False),
    )
    try:
        authenticated = client.auth_check()
    except Exception as exc:
        raise RuntimeError("Langfuse 연결 실패. Docker 상태·3011 포트·.env를 확인하세요.") from exc
    if not authenticated:
        raise RuntimeError("Langfuse 인증 실패. 기존 DB와 .env의 프로젝트 키가 같은지 확인하세요.")
    return client


def usage(result):
    return {
        name: result[key]
        for name, key in [("input", "input_tokens"), ("output", "output_tokens")]
        if result.get(key) is not None
    }


def score_definitions(checks, judge):
    """A format/citation check is not a semantic accuracy score."""
    definitions = [
        {
            "name": name,
            "value": float(value),
            "data_type": "BOOLEAN",
            "comment": "코드 검사. 답변의 의미 정확성을 보장하지 않음.",
            "source": "code",
        }
        for name, value in checks.items()
        if value is not None
    ]
    definitions.append(
        {
            "name": "llm_groundedness",
            "value": judge["verdict"],
            "data_type": "CATEGORICAL",
            "comment": judge["reason"],
            "source": "local-llm-self-judge",
        }
    )
    return definitions


def traced_question(langfuse, ollama, question, *, prompt_version="grounded", session_id=None):
    """Record real timing around each operation, not replayed/fabricated spans."""
    if prompt_version not in PROMPTS:
        raise ValueError("prompt_version은 baseline 또는 grounded입니다.")
    if ollama.info is None:
        ollama.probe()
    docs, _ = load_data()
    session_id = session_id or "week11-" + uuid.uuid4().hex[:12]
    metadata = {
        "question_id": question["id"],
        "prompt_version": prompt_version,
        "model_digest": ollama.info["digest"],
        "synthetic_data": True,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    with propagate_attributes(session_id=session_id, tags=["week11", "ollama", prompt_version]):
        with langfuse.start_as_current_observation(
            name=f"rag-{question['id']}-{prompt_version}",
            as_type="span",
            input={"question": question["query"]},
            metadata=metadata,
        ) as root:
            with langfuse.start_as_current_observation(
                name="01-retrieval",
                as_type="retriever",
                input=question["query"],
            ) as retrieval:
                ranked = Retriever(docs, Config("live-char-current", "char", True, 3)).search(
                    question["query"]
                )
                retrieval.update(
                    output=ranked, metadata={"k": 3, "analyzer": "char", "current_only": True}
                )

            # References are for evaluation only; never included in generation input.
            context = [{"id": d["id"], "text": d["text"]} for d in ranked]
            messages = [
                {"role": "system", "content": PROMPTS[prompt_version]},
                {
                    "role": "user",
                    "content": json.dumps(
                        {"question": question["query"], "documents": context}, ensure_ascii=False
                    ),
                },
            ]
            with langfuse.start_as_current_observation(
                name="02-ollama-answer",
                as_type="generation",
                model=ollama.model,
                input=messages,
            ) as generation:
                response = ollama.chat(messages, ANSWER_SCHEMA)
                answer = validate_answer(response["parsed"])
                generation.update(
                    output=answer,
                    usage_details=usage(response),
                    model_parameters=response["options"],
                    metadata={
                        "load_ms": response["load_ms"],
                        "prompt_sha256": response["prompt_sha256"],
                    },
                )

            with langfuse.start_as_current_observation(
                name="03-code-checks",
                as_type="evaluator",
                input={"answer": answer, "gold_ids": question["gold_ids"]},
            ) as checking:
                checks = inspect_answer(
                    answer, ranked, question["gold_ids"], question["answerable"]
                )
                checking.update(output=checks)

            with langfuse.start_as_current_observation(
                name="04-ollama-judge",
                as_type="generation",
                model=ollama.model,
                input={
                    "question": question["query"],
                    "evidence": context,
                    "answer": answer["answer"],
                },
            ) as evaluating:
                judged = judge_answer(
                    ollama, question["query"], [d["text"] for d in ranked], answer["answer"]
                )
                evaluating.update(
                    output=judged["parsed"],
                    usage_details=usage(judged),
                    model_parameters=judged["options"],
                    metadata={"not_independent_judge": True},
                )

            definitions = score_definitions(checks, judged["parsed"])
            for score in definitions:
                langfuse.create_score(
                    trace_id=root.trace_id,
                    name=score["name"],
                    value=score["value"],
                    data_type=score["data_type"],
                    comment=score["comment"],
                    score_id=f"{root.trace_id}-{score['name']}",
                    metadata={"computed_by": score["source"], "synthetic_data": True},
                )
            root.update(output=answer)
            trace_id = root.trace_id
    langfuse.flush()
    return {
        "trace_id": trace_id,
        "url": langfuse.get_trace_url(trace_id=trace_id),
        "session_id": session_id,
        "question_id": question["id"],
        "prompt_version": prompt_version,
        "answer": answer,
        "checks": checks,
        "judge": judged["parsed"],
        "generation_ms": response["latency_ms"],
        "generation_load_ms": response["load_ms"],
        "output_tokens": response["output_tokens"],
        "expected_score_names": [score["name"] for score in definitions],
    }


def read_trace(langfuse, trace_id):
    observations = langfuse.api.observations.get_many(
        trace_id=trace_id,
        limit=100,
        fields="core,basic,time,io,model,usage,trace_context",
    )
    scores = langfuse.api.scores.get_many(trace_id=trace_id, limit=100, fields="details,subject")
    return {
        "observations": [o.model_dump(mode="json") for o in observations.data],
        "scores": [s.model_dump(mode="json") for s in scores.data],
    }


def wait_for_trace(langfuse, result, timeout=60):
    """flush sends the queue; API readback proves asynchronous server persistence."""
    langfuse.flush()
    deadline = time.monotonic() + timeout
    expected = set(result["expected_score_names"])
    while True:
        snapshot = read_trace(langfuse, result["trace_id"])
        names = {o["name"] for o in snapshot["observations"]}
        scores = {s["name"] for s in snapshot["scores"]}
        required = set(
            result.get(
                "expected_observation_names",
                [
                    "01-retrieval",
                    "02-ollama-answer",
                    "03-code-checks",
                    "04-ollama-judge",
                ],
            )
        )
        if required <= names and expected <= scores:
            return snapshot
        if time.monotonic() >= deadline:
            raise TimeoutError(
                "Langfuse 저장 확인 시간 초과. worker·ClickHouse 상태와 로그를 확인하세요. 재생성 전에 같은 trace URL을 새로고침하세요."
            )
        time.sleep(2)


def observation_table(snapshot):
    return [
        {
            "name": o["name"],
            "type": o["type"],
            "id": o["id"],
            "parent_id": o.get("parentObservationId"),
            "input_tokens": (o.get("usageDetails") or {}).get("input"),
            "output_tokens": (o.get("usageDetails") or {}).get("output"),
        }
        for o in snapshot["observations"]
    ]


def score_table(snapshot):
    return [
        {
            "name": s["name"],
            "value": s["value"],
            "type": s["dataType"],
            "comment": s.get("comment"),
        }
        for s in snapshot["scores"]
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=REPORT_DIR)
    args = parser.parse_args()
    langfuse, ollama = connect_langfuse(), OllamaClient()
    ollama.probe()
    _, questions = load_data()
    by_id = {q["id"]: q for q in questions}
    session_id = "week11-compare-" + uuid.uuid4().hex[:12]
    results = []
    try:
        for question, prompt in [("Q03a", "grounded"), ("Q24a", "baseline"), ("Q24a", "grounded")]:
            result = traced_question(
                langfuse, ollama, by_id[question], prompt_version=prompt, session_id=session_id
            )
            stored = wait_for_trace(langfuse, result)
            results.append({**result, "stored": stored})
            print(
                json.dumps(
                    {
                        "trace_url": result["url"],
                        "observations": len(stored["observations"]),
                        "scores": len(stored["scores"]),
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "verified-traces.json").write_text(
            json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    finally:
        langfuse.shutdown()


if __name__ == "__main__":
    main()
