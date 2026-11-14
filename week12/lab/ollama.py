"""Real local generation; connection failures are errors, never synthetic fallbacks."""
import os
import time
import requests
from .experiment import POLICIES, PROMPTS

MODEL = "qwen2.5:1.5b-instruct"


def generate(topic, variant, *, base_url=None, model=MODEL, timeout=60):
    url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")).rstrip("/")
    started = time.perf_counter()
    try:
        response = requests.post(url+"/api/chat", json={
            "model": model, "stream": False, "think": False, "keep_alive": "10m",
            "options": {"temperature": 0, "seed": 12, "num_ctx": 1024, "num_predict": 128},
            "messages": [{"role": "system", "content": PROMPTS[variant]+" 근거 밖 내용을 만들지 마세요."},
                         {"role": "user", "content": POLICIES[topic]+"\n이 정책에 따라 안내해 주세요."}],
        }, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Ollama 연결·모델 오류: ollama serve / ollama pull {model} 확인. {type(exc).__name__}") from exc
    data = response.json()
    answer = data.get("message", {}).get("content", "").strip()
    if not answer:
        raise RuntimeError("Ollama 응답 본문이 비어 있습니다. 모델·출력 상한을 확인하세요.")
    return {"answer": answer, "provider": "ollama", "model": model,
            "latency_ms": round((time.perf_counter()-started)*1000, 2),
            "output_tokens": data.get("eval_count"), "done_reason": data.get("done_reason"),
            "load_duration_ms": data.get("load_duration", 0)/1e6}
