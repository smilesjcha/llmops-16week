const $ = (selector) => document.querySelector(selector);

const form = $("#run-form");
const text = $("#text");
const temperature = $("#temperature");
const status = $("#status");
const runButton = $("#run-button");

function setStatus(label, state) {
  status.textContent = label;
  status.dataset.state = state;
}

function countCharacters() {
  $("#char-count").textContent = `${text.value.length} / 6000`;
}

function setTrace(trace) {
  $("#trace-id").textContent = trace.trace_id;
  $("#prompt-version").textContent = trace.prompt_version;
  $("#model").textContent = trace.model;
  $("#thinking").textContent = trace.thinking_requested ? "ON" : "OFF";
  $("#latency").textContent = `${trace.latency_ms.toFixed(2)} ms`;
  $("#model-load").textContent =
    trace.model_load_ms == null ? "—" : `${trace.model_load_ms.toFixed(2)} ms`;
  $("#tokens").textContent = trace.input_tokens_est + trace.output_tokens_est;
  $("#output-limit").textContent = trace.output_token_limit ?? "—";
  $("#model-generation").textContent =
    trace.model_generation_ms == null
      ? "—"
      : `${trace.model_generation_ms.toFixed(2)} ms · ${trace.model_output_tokens ?? "?"} tokens`;
  $("#finish-reason").textContent =
    trace.finish_reason === "length" ? "출력 상한 도달 · length" : trace.finish_reason ?? "—";
  $("#fingerprint").textContent = trace.content_fingerprint;
}

async function refreshRuntimeConfig() {
  try {
    const response = await fetch("/api/v1/config");
    const body = await response.json();
    const config = body.ollama;
    $("#runtime-model").textContent = config.model;
    $("#runtime-options").textContent =
      `Thinking ${config.thinking_requested ? "ON" : "OFF"} · ` +
      `출력 상한 ${config.num_predict} · 컨텍스트 ${config.num_ctx} · 유지 ${config.keep_alive}`;
  } catch (_error) {
    $("#runtime-model").textContent = "설정을 확인할 수 없음";
  }
}

async function refreshStats() {
  const response = await fetch("/api/v1/stats");
  const stats = await response.json();
  $("#total-runs").textContent = stats.total_requests;
  $("#success-rate").textContent = `${Math.round(stats.success_rate * 100)}%`;
  $("#p95").textContent = `${stats.p95_latency_ms.toFixed(1)} ms`;
  $("#total-tokens").textContent = stats.estimated_tokens;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  runButton.disabled = true;
  setStatus("실행 중", "running");
  $("#output").textContent = "호출 중…";

  try {
    const response = await fetch("/api/v1/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: text.value,
        task: $("#task").value,
        provider: $("#provider").value,
        temperature: Number(temperature.value),
      }),
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.detail || "요청에 실패했습니다.");
    $("#output").textContent = body.output;
    setTrace(body.trace);
    setStatus(
      body.trace.finish_reason === "length" ? "출력 상한 도달" : "정상",
      body.trace.finish_reason === "length" ? "warning" : "success",
    );
    await refreshStats();
  } catch (error) {
    $("#output").textContent = error.message;
    setStatus("오류", "error");
    await refreshStats();
  } finally {
    runButton.disabled = false;
  }
});

text.addEventListener("input", countCharacters);
temperature.addEventListener("input", () => {
  $("#temperature-value").textContent = temperature.value;
});
countCharacters();
refreshStats();
refreshRuntimeConfig();
