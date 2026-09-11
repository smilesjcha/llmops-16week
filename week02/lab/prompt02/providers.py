"""Local demo replay and explicit, bounded Ollama execution; no provider fallback."""

from __future__ import annotations

import json
import math
import os
from urllib.parse import urlsplit

import httpx

from .core import LAB_ROOT, fingerprint


class ProviderError(RuntimeError):
    pass


class DemoProvider:
    name = "demo"
    model = "fixed-teaching-fixtures-v1"

    def __init__(self):
        self.fixtures = json.loads((LAB_ROOT / "data" / "demo_responses.json").read_text())

    def config(self) -> dict:
        return {
            "model": self.model,
            "simulation": True,
            "fixture_hash": fingerprint(self.fixtures),
            "temperature": None,
            "notice": self.fixtures["notice"],
        }

    async def generate(self, prompt: dict, case: dict) -> dict:
        value = self.fixtures[prompt["version"]][case["id"]]
        return {
            "text": value if isinstance(value, str) else json.dumps(value, ensure_ascii=False),
            "model": self.model,
            "finish_reason": "fixture_replay",
            "output_tokens": None,
        }


class OllamaProvider:
    name = "ollama"

    def __init__(self, *, transport=None, timeout_seconds: float = 35):
        self.base_url = os.getenv("PROMPT02_OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
        url = urlsplit(self.base_url)
        if url.scheme != "http" or url.hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise ProviderError("이 실습은 로컬 Ollama 주소만 허용합니다.")
        if url.username or url.password or url.query or url.fragment or url.path:
            raise ProviderError("Ollama 주소는 인증 정보·경로가 없는 로컬 기본 주소여야 합니다.")
        self.model = os.getenv("PROMPT02_MODEL", "qwen3:4b-instruct")
        self.timeout_seconds = min(max(timeout_seconds, 1), 35)
        self.transport = transport

    def config(self) -> dict:
        return {
            "model": self.model,
            "base_url": self.base_url,
            "simulation": False,
            "think": False,
            "temperature": 0,
            "num_ctx": 4096,
            "num_predict": 384,
            "seed": 42,
            "keep_alive": "30m",
            "timeout_seconds": self.timeout_seconds,
            "structured_decoding": False,
            "notice": "실제 로컬 모델 호출. format 옵션은 사용하지 않아 프롬프트만 비교합니다.",
        }

    async def generate(self, prompt: dict, case: dict) -> dict:
        del case
        config = self.config()
        payload = {
            "model": self.model,
            "messages": prompt["messages"],
            "stream": False,
            "think": False,
            "keep_alive": config["keep_alive"],
            "options": {
                key: config[key] for key in ("temperature", "num_ctx", "num_predict", "seed")
            },
        }
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout_seconds, transport=self.transport, follow_redirects=False
            ) as client:
                response = await client.post(f"{self.base_url}/api/chat", json=payload)
                response.raise_for_status()
                body = response.json()
                output = body["message"]["content"]
                if not isinstance(output, str) or not output.strip():
                    raise ValueError("empty or malformed content")
                if len(output) > 20_000:
                    raise ValueError("content exceeds limit")
        except httpx.TimeoutException as exc:
            raise ProviderError(
                "Ollama 응답이 35초 상한을 초과했습니다. 모델을 먼저 로드하고 1건만 실행하세요."
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise ProviderError(
                f"Ollama HTTP {exc.response.status_code}. "
                f"ollama list에서 {self.model} 설치 여부를 확인하세요."
            ) from exc
        except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
            raise ProviderError(
                "Ollama 연결 또는 응답 오류. ollama serve와 모델 설치 상태를 확인하세요."
            ) from exc
        duration = body.get("load_duration")
        duration = (
            round(duration / 1_000_000, 2)
            if type(duration) in {float, int} and math.isfinite(duration) and duration >= 0
            else None
        )
        tokens = body.get("eval_count")
        return {
            "text": output.strip(),
            "model": body.get("model") if isinstance(body.get("model"), str) else self.model,
            "finish_reason": body.get("done_reason")
            if isinstance(body.get("done_reason"), str)
            else None,
            "output_tokens": tokens if type(tokens) is int and tokens >= 0 else None,
            "load_duration_ms": duration,
        }
