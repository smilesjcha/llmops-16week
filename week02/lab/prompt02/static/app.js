"use strict";
const $ = (id) => document.getElementById(id);
const state = { catalog: null, version: "v1", report: null, busy: false };
const labels = {
  format_ok: "형식",
  routing_ok: "분류",
  promise_ok: "확정 약속",
  review_ok: "검토·우선순위",
};
function node(tag, text, className) {
  const e = document.createElement(tag);
  if (text !== undefined) e.textContent = text;
  if (className) e.className = className;
  return e;
}
function flag(value) {
  return value === null ? "미평가" : value ? "통과" : "실패";
}
async function api(path, body) {
  const response = await fetch(
    path,
    body
      ? {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        }
      : {},
  );
  if (!response.ok) {
    let msg;
    try {
      const data = await response.json();
      msg =
        typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail);
    } catch {
      msg = `HTTP ${response.status}`;
    }
    throw new Error(msg);
  }
  return response.json();
}
function selected() {
  return [...document.querySelectorAll(".case input:checked")].map(
    (e) => e.value,
  );
}
function updateCount() {
  $("case-count").textContent = `${selected().length}건 선택`;
  $("run").disabled = state.busy || !selected().length;
}
function setStatus(text, error = false) {
  $("status").textContent = text;
  $("status").classList.toggle("error-text", error);
}
async function preview() {
  try {
    const data = await api(
      `/api/prompt/${state.version}?case_id=${encodeURIComponent($("preview-case").value)}`,
    );
    $("prompt-text").textContent = data.template;
    $("input-text").textContent = data.messages[1].content;
    $("prompt-hash").textContent = data.prompt_hash;
  } catch (error) {
    setStatus(error.message, true);
  }
}
function renderCatalog(catalog) {
  state.catalog = catalog;
  for (const item of catalog.dataset.cases) {
    const label = node("label", undefined, "case");
    const top = node("span", undefined, "case-top");
    const check = node("input");
    check.type = "checkbox";
    check.value = item.id;
    check.checked = true;
    check.addEventListener("change", updateCount);
    top.append(check, node("span", `${item.id} · ${item.tag}`));
    label.append(top, node("span", item.text, "case-text"));
    $("cases").append(label);
    const option = node("option", `${item.id} · ${item.tag}`);
    option.value = item.id;
    $("preview-case").append(option);
  }
  updateCount();
  preview();
}
function renderReport(report) {
  state.report = report;
  $("run-kind").textContent = report.simulation
    ? "고정 응답 · 교육용 시뮬레이션"
    : "실제 로컬 모델 · Ollama";
  $("summary").replaceChildren();
  for (const version of report.versions) {
    const metrics = report.summary[version],
      card = node("article", undefined, "summary-card");
    card.append(
      node(
        "div",
        `${version} · ${state.catalog.versions.find((x) => x.id === version).name}`,
        "version",
      ),
    );
    const score = node(
      "div",
      `${metrics.overall_ok.passed} / ${metrics.total}`,
      "score",
    );
    score.append(node("span", "전체 검사 통과"));
    card.append(score);
    for (const [key, title] of Object.entries(labels)) {
      const row = node("div", undefined, "metric-line");
      row.append(
        node("span", title),
        node(
          "strong",
          `${metrics[key].passed}/${metrics.total} · ${(metrics[key].rate * 100).toFixed(0)}%`,
        ),
      );
      card.append(row);
    }
    const timing = node(
      "p",
      `평균 ${metrics.average_latency_ms.toFixed(1)} ms${report.simulation ? " · fixture 재생 시간" : " · 호출·검증 포함"}`,
      "muted",
    );
    card.append(timing);
    $("summary").append(card);
  }
  $("comparison-body").replaceChildren();
  for (const caseId of report.case_ids) {
    const rows = report.rows.filter((r) => r.case_id === caseId),
      first = rows[0],
      tr = node("tr"),
      td = node("td");
    td.append(
      node("strong", `${caseId} · ${first.tag}`),
      node("p", first.input),
      node("span", `기준: ${first.expected.category}`),
    );
    tr.append(td);
    for (const version of ["v1", "v2", "v3"]) {
      const row = rows.find((r) => r.version === version),
        cell = node("td");
      if (!row) {
        cell.textContent = "미실행";
        tr.append(cell);
        continue;
      }
      const button = node("button"),
        passed = row.validation.overall_ok;
      button.append(
        node(
          "span",
          row.error
            ? "호출 실패 / 미실행 ↗"
            : `${passed ? "전체 통과" : "실패 원인 확인"} ↗`,
          `result-label ${passed ? "pass" : ""}`,
        ),
      );
      const parsed = row.validation.parsed;
      if (parsed)
        button.append(node("p", `${parsed.category} / ${parsed.priority}`));
      button.append(
        node(
          "span",
          Object.entries(labels)
            .map(([key, title]) => `${title} ${flag(row.validation[key])}`)
            .join(" · "),
          "check-mini",
        ),
      );
      button.addEventListener("click", () => showDetail(row));
      cell.append(button);
      tr.append(cell);
    }
    $("comparison-body").append(tr);
  }
  $("metadata-text").textContent = JSON.stringify(
    {
      run_id: report.run_id,
      created_at: report.created_at,
      dataset_id: report.dataset_id,
      dataset_hash: report.dataset_hash,
      input_set_hash: report.input_set_hash,
      evaluator_version: report.evaluator_version,
      config: report.config,
    },
    null,
    2,
  );
  $("save-decision").disabled = false;
  $("decision-status").textContent = "";
  $("export").href = `/api/experiments/${report.run_id}/export`;
  $("export").classList.remove("disabled");
  $("export").setAttribute("aria-disabled", "false");
}
function showDetail(row) {
  $("detail-title").textContent =
    `${row.case_id} / ${row.version} / ${row.tag}`;
  $("detail-input").textContent = row.input;
  $("detail-expected").textContent = JSON.stringify(row.expected, null, 2);
  $("detail-output").textContent = row.raw_output || "응답 없음";
  $("detail-checks").replaceChildren();
  for (const [key, title] of Object.entries(labels)) {
    const line = node("div", undefined, "check-line");
    line.append(node("span", title), node("strong", flag(row.validation[key])));
    $("detail-checks").append(line);
  }
  $("detail-issues").replaceChildren();
  for (const issue of row.validation.issues.length
    ? row.validation.issues
    : ["이 평가 기준에서 탐지된 실패 없음. 다른 데이터에서 추가 검증 필요."]) {
    $("detail-issues").append(node("li", issue));
  }
  $("detail-metadata").textContent = JSON.stringify(
    {
      latency_ms: row.latency_ms,
      prompt_hash: row.prompt_hash,
      input_hash: row.input_hash,
      model: row.model_metadata,
    },
    null,
    2,
  );
  $("detail-dialog").showModal();
}
$("run").addEventListener("click", async () => {
  state.busy = true;
  updateCount();
  $("provider").disabled = true;
  $("save-decision").disabled = true;
  const provider = $("provider").value;
  setStatus(
    provider === "demo"
      ? "동일 입력으로 고정 응답 비교 중…"
      : "Ollama 실제 모델 호출 중… 개별 호출 최대 35초, 실험 전체 최대 120초입니다.",
  );
  try {
    const report = await api("/api/experiments", {
      provider,
      case_ids: selected(),
      versions: ["v1", "v2", "v3"],
    });
    renderReport(report);
    const errors = report.rows.filter((x) => x.error);
    setStatus(
      errors.length
        ? `오류 또는 미실행 ${errors.length}건. ${errors[0].error} demo로 자동 전환되지 않습니다.`
        : `${report.rows.length}개 결과 비교 완료. 결과와 실패 원인을 확인하세요.`,
      !!errors.length,
    );
    $("results").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    setStatus(error.message, true);
    if (state.report) $("save-decision").disabled = false;
  } finally {
    state.busy = false;
    updateCount();
    $("provider").disabled = false;
  }
});
$("provider").addEventListener("change", () => {
  const ollama = $("provider").value === "ollama";
  $("mode-notice").replaceChildren(
    node("strong", ollama ? "실제 로컬 모델" : "교육용 시뮬레이션"),
    node(
      "span",
      ollama
        ? "로컬 Ollama를 호출합니다. 동일한 모델 설정으로 프롬프트만 비교하며, 실패 시 오류를 그대로 표시합니다."
        : "고정 응답을 재생합니다. 실제 모델의 성능 측정이 아니며, 프롬프트를 수정해도 demo 응답은 바뀌지 않습니다.",
    ),
  );
  $("provider-details").textContent = ollama
    ? `${state.catalog.ollama.model || "qwen3:4b-instruct"} · think=false · temperature=0 · context=4096 · output=384 · seed=42. 먼저 1건으로 확인하세요.`
    : "API 키와 모델 설치 없이 모든 필수 실습을 진행할 수 있습니다.";
  if (ollama) {
    document
      .querySelectorAll(".case input")
      .forEach((e, i) => (e.checked = i === 0));
  }
  updateCount();
});
$("select-all").addEventListener("click", () => {
  document.querySelectorAll(".case input").forEach((e) => (e.checked = true));
  updateCount();
});
document.querySelectorAll("[data-version]").forEach((e) =>
  e.addEventListener("click", () => {
    state.version = e.dataset.version;
    document
      .querySelectorAll("[data-version]")
      .forEach((b) => b.setAttribute("aria-selected", String(b === e)));
    preview();
  }),
);
$("preview-case").addEventListener("change", preview);
$("close-dialog").addEventListener("click", () => $("detail-dialog").close());
$("save-decision").addEventListener("click", async () => {
  if (!state.report) return;
  const reason = $("reason").value.trim();
  if (reason.length < 15) {
    $("decision-status").textContent = "선택 근거를 15자 이상 입력해주세요.";
    return;
  }
  try {
    const record = await api("/api/decisions", {
      run_id: state.report.run_id,
      version: $("candidate").value,
      reason,
    });
    $("decision-status").textContent =
      `${record.version} 후보 선택 기록 완료. 실제 배포는 수행하지 않았습니다. JSON 보고서를 저장하세요.`;
  } catch (error) {
    $("decision-status").textContent = error.message;
  }
});
api("/api/catalog")
  .then(renderCatalog)
  .catch((error) => setStatus(`초기화 실패: ${error.message}`, true));
