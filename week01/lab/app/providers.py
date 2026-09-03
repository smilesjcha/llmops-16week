"""Offline-first and Ollama providers behind one tiny interface."""

from __future__ import annotations

import re
from dataclasses import dataclass

import httpx

from .schemas import TaskName

PROMPTS: dict[TaskName, tuple[str, str]] = {
    "summarize": (
        "w01.summary.v1",
        "다음 텍스트의 핵심을 한 문장으로 요약하고, 근거가 되는 키워드 3개를 제시하세요.",
    ),
    "extract": (
        "w01.signal.v1",
        "고객 피드백에서 SIGNAL, FRICTION, NEXT ACTION을 각각 한 줄로 추출하세요.",
    ),
    "rewrite": (
        "w01.rewrite.v1",
        "다음 문장을 명확하고 간결한 실무 문장으로 다시 쓰세요. 사실을 추가하지 마세요.",
    ),
}


class ProviderError(RuntimeError):
    """A predictable provider failure suitable for an HTTP 503 response."""


@dataclass(slots=True)
class ProviderResult:
    text: str
    model: str


class DemoProvider:
    """Deterministic fallback so every student can finish the lab offline."""

    name = "demo"

    async def generate(
        self, text: str, task: TaskName, temperature: float
    ) -> ProviderResult:
        del temperature
        normalized = " ".join(text.split())
        sentences = [
            part.strip()
            for part in re.split(r"(?<=[.!?。])\s+", normalized)
            if part.strip()
        ]
        first = sentences[0] if sentences else normalized

        if task == "summarize":
            words = [word.strip(".,!?()[]{}\"'") for word in normalized.split()]
            keywords = []
            for word in sorted(words, key=len, reverse=True):
                if len(word) >= 3 and word not in keywords:
                    keywords.append(word)
                if len(keywords) == 3:
                    break
            keyword_text = " · ".join(keywords or ["핵심", "근거", "행동"])
            output = f"핵심 — {first[:180]}\n키워드 — {keyword_text}"
        elif task == "extract":
            friction_terms = ("느리", "오류", "불편", "어렵", "비싸", "안 되", "실패")
            friction = next((s for s in sentences if any(t in s for t in friction_terms)), first)
            output = (
                f"SIGNAL — {first[:150]}\n"
                f"FRICTION — {friction[:150]}\n"
                "NEXT ACTION — 같은 입력 세트로 다음 버전을 비교하고 지표를 기록한다."
            )
        else:
            output = f"실무 문장 — {first[:220].rstrip('.')}"

        return ProviderResult(text=output, model="trace-demo-1")


class OllamaProvider:
    """Thin client for Ollama's local chat API."""

    name = "ollama"

    def __init__(self, base_url: str, model: str, timeout_seconds: float = 60.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    async def generate(
        self, text: str, task: TaskName, temperature: float
    ) -> ProviderResult:
        _, instruction = PROMPTS[task]
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": "당신은 근거를 벗어나지 않는 간결한 한국어 업무 보조자입니다.",
                },
                {"role": "user", "content": f"{instruction}\n\nINPUT:\n{text}"},
            ],
            "options": {"temperature": temperature},
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(f"{self.base_url}/api/chat", json=payload)
                response.raise_for_status()
                body = response.json()
                output = body["message"]["content"].strip()
        except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
            raise ProviderError(
                "Ollama 호출에 실패했습니다. `ollama serve`와 모델 설치 상태를 확인하세요."
            ) from exc

        if not output:
            raise ProviderError("Ollama가 빈 응답을 반환했습니다.")
        return ProviderResult(text=output, model=self.model)
