const WEEK_MIN = 1;
const WEEK_MAX = 16;

function resolveCurrentWeek() {
  const queryWeek = Number(new URLSearchParams(window.location.search).get("week"));
  const fallbackWeek = Number(document.body.dataset.currentWeek || "1");
  const candidate = Number.isInteger(queryWeek) ? queryWeek : fallbackWeek;
  return Math.min(WEEK_MAX, Math.max(WEEK_MIN, candidate));
}

function setCurrentWeek(week) {
  document.querySelectorAll("[data-week]").forEach((element) => {
    const isCurrent = Number(element.dataset.week) === week;
    element.classList.toggle("is-current", isCurrent);
    if (isCurrent) {
      element.setAttribute("aria-current", "step");
    } else {
      element.removeAttribute("aria-current");
    }
  });

  document.querySelectorAll("[data-current-week-number]").forEach((element) => {
    element.textContent = String(week).padStart(2, "0");
  });

  const currentElement = document.querySelector(`[data-week="${week}"]`);
  const topic = currentElement?.dataset.topic;
  document.querySelectorAll("[data-current-week-topic]").forEach((element) => {
    if (topic) element.textContent = topic;
  });

  const scheduleRow = document.querySelector(`.schedule-table tr[data-week="${week}"]`);
  const scheduleCells = scheduleRow?.querySelectorAll("td");
  if (scheduleCells?.length >= 5) {
    const date = scheduleCells[1].textContent.trim();
    const mode = scheduleCells[2].textContent.trim();
    const output = scheduleCells[4].textContent.trim();
    document.querySelectorAll("[data-current-week-copy]").forEach((element) => {
      element.textContent = `${date} · ${mode} / 산출물 · ${output}`;
    });
  }
}

document.querySelectorAll("[data-set-week]").forEach((button) => {
  button.addEventListener("click", () => {
    const week = Number(button.dataset.setWeek);
    if (!Number.isInteger(week) || week < WEEK_MIN || week > WEEK_MAX) return;
    const url = new URL(window.location.href);
    url.searchParams.set("week", String(week));
    window.history.replaceState({}, "", url);
    setCurrentWeek(week);
  });
});

document.querySelectorAll("[data-print]").forEach((button) => {
  button.addEventListener("click", () => window.print());
});

setCurrentWeek(resolveCurrentWeek());
