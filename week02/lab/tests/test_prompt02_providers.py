import asyncio
import json

import httpx
import pytest
from prompt02.contracts import ExperimentRequest
from prompt02.core import load_dataset, render_prompt
from prompt02.experiments import run_experiment
from prompt02.providers import OllamaProvider, ProviderError


def call_provider(handler):
    case = load_dataset()["cases"][0]
    provider = OllamaProvider(transport=httpx.MockTransport(handler))
    return asyncio.run(provider.generate(render_prompt("v2", case), case))


def test_ollama_payload_is_bounded_and_identical_settings():
    observed = []

    def handle(request):
        payload = json.loads(request.content)
        observed.append(payload)
        return httpx.Response(
            200,
            json={
                "message": {"content": '{"example":true}'},
                "model": "qwen3:4b-instruct",
                "load_duration": 2_000_000,
            },
        )

    output = call_provider(handle)
    assert output["load_duration_ms"] == 2
    payload = observed[0]
    assert payload["think"] is False
    assert payload["stream"] is False
    assert payload["options"] == {"temperature": 0, "num_ctx": 4096, "num_predict": 384, "seed": 42}
    assert "format" not in payload
    assert payload["keep_alive"] == "30m"


@pytest.mark.parametrize("status", [404, 429, 500, 503, 302])
def test_provider_http_error_is_explicit(status):
    with pytest.raises(ProviderError, match=f"HTTP {status}"):
        call_provider(lambda request: httpx.Response(status, json={"error": "model unavailable"}))


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"message": {}},
        {"message": {"content": None}},
        {"message": {"content": ""}},
        {"message": {"content": []}},
    ],
)
def test_provider_malformed_content_is_explicit(body):
    with pytest.raises(ProviderError):
        call_provider(lambda request: httpx.Response(200, json=body))


def test_malformed_metadata_cannot_crash_request():
    result = call_provider(
        lambda request: httpx.Response(
            200,
            json={
                "message": {"content": "{}"},
                "load_duration": "bad",
                "eval_count": True,
                "done_reason": {"bad": "value"},
                "model": None,
            },
        )
    )
    assert result["load_duration_ms"] is None
    assert result["output_tokens"] is None
    assert result["finish_reason"] is None
    assert result["model"] == "qwen3:4b-instruct"


def test_provider_timeout_does_not_fallback_to_demo():
    calls = []

    def timeout(request):
        calls.append(request)
        raise httpx.ReadTimeout("late")

    provider = OllamaProvider(transport=httpx.MockTransport(timeout))
    report = asyncio.run(
        run_experiment(
            ExperimentRequest(provider="ollama", case_ids=["T01"]), provider_override=provider
        )
    )
    assert len(calls) == 1
    assert report["simulation"] is False
    assert all(row["raw_output"] == "" for row in report["rows"])
    assert all(row["error"] for row in report["rows"])
    assert all(row["validation"]["format_ok"] is None for row in report["rows"])
    assert report["summary"]["v1"]["latency_sample_count"] == 0


def test_connection_failure_is_explicit():
    def failure(request):
        raise httpx.ConnectError("refused")

    with pytest.raises(ProviderError, match="연결"):
        call_provider(failure)


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com",
        "http://example.com",
        "http://127.0.0.1:11434/api",
        "http://u:p@localhost:11434",
    ],
)
def test_remote_or_credential_urls_are_rejected(monkeypatch, url):
    monkeypatch.setenv("PROMPT02_OLLAMA_URL", url)
    with pytest.raises(ProviderError):
        OllamaProvider()
