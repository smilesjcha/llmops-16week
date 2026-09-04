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
  $("#latency").textContent = `${trace.latency_ms.toFixed(2)} ms`;
  $("#tokens").textContent = trace.input_tokens_est + trace.output_tokens_est;
  $("#fingerprint").textContent = trace.content_fingerprint;
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
    setStatus("정상", "success");
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
