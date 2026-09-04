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
    thinking_requested: bool = False
    output_token_limit: int | None = None
    model_load_ms: float | None = None
    model_generation_ms: float | None = None
    model_output_tokens: int | None = None
    finish_reason: str | None = None


class DemoProvider:
    """Deterministic fallback so every student can finish the lab offline."""

    name = "demo"
    model = "trace-demo-1"

    @staticmethod
    def _extract_signal_and_friction(sentences: list[str], normalized: str) -> tuple[str, str]:
        """Split a common Korean contrast without pretending to understand arbitrary text."""
        first = sentences[0] if sentences else normalized
        if "지만" in first:
            signal_clause, _, friction_clause = first.partition("지만")
            signal_clause = signal_clause.strip(" ,")
            friction_clause = friction_clause.strip(" ,")
            if signal_clause and friction_clause:
                return f"{signal_clause}다는 관찰", friction_clause

        friction_terms = ("느리", "오류", "불편", "어렵", "비싸", "안 되", "실패")
        friction = next(
            (
                sentence
                for sentence in sentences
                if any(term in sentence for term in friction_terms)
            ),
            "명시적 마찰 표현 없음",
        )
        return first, friction

    async def generate(self, text: str, task: TaskName, temperature: float) -> ProviderResult:
        del temperature
        normalized = " ".join(text.split())
        sentences = [
            part.strip() for part in re.split(r"(?<=[.!?。])\s+", normalized) if part.strip()
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
            signal, friction = self._extract_signal_and_friction(sentences, normalized)
            output = (
                f"SIGNAL — {signal[:150]}\n"
                f"FRICTION — {friction[:150]}\n"
                "NEXT ACTION — 같은 입력 세트로 다음 버전을 비교하고 지표를 기록한다."
            )
        else:
            output = f"실무 문장 — {first[:220].rstrip('.')}"

        return ProviderResult(text=output, model=self.model)


class OllamaProvider:
    """Thin client for Ollama's local chat API."""

    name = "ollama"

    def __init__(
        self,
        base_url: str,
        model: str,
        *,
        thinking_requested: bool = False,
        num_ctx: int = 2_048,
        num_predict: int = 128,
        keep_alive: str = "30m",
        seed: int = 42,
        timeout_seconds: float = 60.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.thinking_requested = thinking_requested
        self.num_ctx = num_ctx
        self.num_predict = num_predict
        self.keep_alive = keep_alive
        self.seed = seed
        self.timeout_seconds = timeout_seconds
        self.transport = transport

    def public_config(self) -> dict[str, str | int | bool]:
        """Return the reproducibility settings students are expected to record."""
        return {
            "base_url": self.base_url,
            "model": self.model,
            "thinking_requested": self.thinking_requested,
            "num_ctx": self.num_ctx,
            "num_predict": self.num_predict,
            "keep_alive": self.keep_alive,
            "seed": self.seed,
        }

    @staticmethod
    def _duration_ms(body: dict, key: str) -> float | None:
        value = body.get(key)
        if not isinstance(value, int | float):
            return None
        return round(value / 1_000_000, 2)

    async def generate(self, text: str, task: TaskName, temperature: float) -> ProviderResult:
        _, instruction = PROMPTS[task]
        payload = {
            "model": self.model,
            "stream": False,
            "think": self.thinking_requested,
            "keep_alive": self.keep_alive,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "당신은 근거를 벗어나지 않는 간결한 한국어 업무 보조자입니다. "
                        "분석 과정은 출력하지 말고 요청한 결과만 한국어로 답하세요."
                    ),
                },
                {"role": "user", "content": f"{instruction}\n\nINPUT:\n{text}"},
            ],
            "options": {
                "temperature": temperature,
                "num_ctx": self.num_ctx,
                "num_predict": self.num_predict,
                "seed": self.seed,
            },
        }
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout_seconds,
                transport=self.transport,
            ) as client:
                response = await client.post(f"{self.base_url}/api/chat", json=payload)
                response.raise_for_status()
                body = response.json()
                output = body["message"]["content"].strip()
        except httpx.TimeoutException as exc:
            raise ProviderError(
                f"Ollama 응답이 {self.timeout_seconds:.0f}초를 초과했습니다(model={self.model}). "
                "Thinking 설정과 출력 상한을 확인하세요."
            ) from exc
        except httpx.HTTPStatusError as exc:
            try:
                detail = exc.response.json().get("error", exc.response.text)
            except ValueError:
                detail = exc.response.text
            raise ProviderError(
                f"Ollama가 HTTP {exc.response.status_code}를 반환했습니다"
                f"(model={self.model}): {detail}"
            ) from exc
        except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
            raise ProviderError(
                f"Ollama 호출에 실패했습니다(model={self.model}). "
                "`ollama list`와 모델 태그를 확인하세요."
            ) from exc

        if not output:
            raise ProviderError("Ollama가 빈 응답을 반환했습니다.")
        return ProviderResult(
            text=output,
            model=self.model,
            thinking_requested=self.thinking_requested,
            output_token_limit=self.num_predict,
            model_load_ms=self._duration_ms(body, "load_duration"),
            model_generation_ms=self._duration_ms(body, "eval_duration"),
            model_output_tokens=(
                body.get("eval_count") if isinstance(body.get("eval_count"), int) else None
            ),
            finish_reason=(
                body.get("done_reason") if isinstance(body.get("done_reason"), str) else None
            ),
        )
