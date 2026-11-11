"""Generate public walkthrough and a private, run-specific instructor console."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from urllib.parse import urlencode, urlsplit, urlunsplit

LAB = Path(__file__).resolve().parent
PUBLIC = "https://smilesjcha.github.io/llmops-16week/week11"
GITHUB = "https://github.com/smilesjcha/llmops-16week/blob/main/week11/lab"

STEPS = [
    (
        "준비 확인",
        "수업 전 15–30분",
        "09번 환경 셀",
        "로컬 Langfuse에 로그인 → Week 11 Ollama 프로젝트",
        "모델 이름·서버 인증 확인. Docker 여섯 서비스의 실행과 healthcheck 대상의 healthy 상태를 확인합니다.",
        "Langfuse는 답변 생성기가 아니라 요청과 평가의 기록 도구입니다.",
        "환경이 준비됐는가?",
        "home",
    ),
    (
        "요청 전체의 흐름",
        "40–45분",
        "09번 2–3단계",
        "출력된 요청 링크 → Tree → rag-Q03a-grounded",
        "부모 요청 1개 아래 검색·생성·코드 검사·모델 평가 4개가 연결됩니다.",
        "작업 순서와 각 단계의 시간부터 읽습니다. HTTP 성공과 답변 정확성은 다릅니다.",
        "어느 단계에서 오류가 생겼을까?",
        "trace",
    ),
    (
        "모델이 본 근거",
        "45–50분",
        "09번 2–3단계",
        "01-retrieval → Output, 다음 02-ollama-answer → Preview의 Input/Output",
        "실제 검색 문서·모델 입력·답변을 대조합니다. 참고 정답은 생성 입력에 없어야 합니다.",
        "교환 7일·재고 조건·왕복 배송비 6000원이 모두 설명됐는지 원문과 비교합니다.",
        "인용한 문서가 맞으면 답변도 맞을까?",
        "trace",
    ),
    (
        "코드 점수와 모델 판정",
        "50–60분",
        "09번 4–5단계",
        "트리의 부모 요청 선택 → Scores; 04-ollama-judge → 실제 판정 이유",
        "BOOLEAN 코드 검사와 CATEGORICAL llm_groundedness를 구분합니다. 재고 질문의 두 프롬프트도 비교합니다.",
        "supported도 정답 보증이 아닙니다. 사람이 근거를 읽고 반례를 찾습니다.",
        "평가 모델의 이유를 믿을 수 있을까?",
        "trace",
    ),
    (
        "실패의 평가 데이터 전환",
        "60–65분",
        "10번 1–2단계",
        "Datasets → week11-release-로 시작하는 데이터 → 재고 사례",
        "정상 사례 3개 + 경계 사례 1개, 참고 기준, 원본 실패 trace 연결을 확인합니다.",
        "이미 본 회귀 사례입니다. 새로운 질문 전체에 대한 성능으로 해석하지 않습니다.",
        "실패만 모으면 어떤 회귀를 놓칠까?",
        "dataset",
    ),
    (
        "세 버전의 같은 문제",
        "65–77분",
        "10번 3–5단계",
        "Experiments → A 선택 → Compare에 B/C → Display → Score matrix 또는 Grid",
        "A 기준선, B 근거 제한, C 기능 정책의 출력과 점수를 비교합니다. 출력이 궁금하면 Grid, 지표는 Score matrix를 사용합니다.",
        "C는 UI 메뉴·API 라우트로 받은 미지원 실시간 조회를 차단합니다. 자유형 의도 분류기를 구현한 것은 아닙니다.",
        "지시를 강화하는 것과 기능을 제한하는 것은 어떻게 다를까?",
        "compare",
    ),
    (
        "정책 처리의 실제 기록",
        "77–85분",
        "10번 6–7단계",
        "C의 Q24a trace → capability-check → contract-checks",
        "재고 조회 경로에는 generation이 없고 judge는 not_run입니다. 정상 상담 3건에는 실제 Ollama 호출이 있습니다.",
        "generation_ms=0은 호출 생략입니다. 모델 속도 개선 수치로 발표하지 않습니다.",
        "호출하지 않는 판단도 서비스 품질일까?",
        "guard",
    ),
    (
        "배포 판단과 다음 개선",
        "85–100분",
        "10번 6–8단계",
        "Notebook 결과 → HOLD/REVIEW의 checks → 답변 내용 사람 검토",
        "이 환경의 실제 사례는 B HOLD, C REVIEW였습니다. 본인 결과는 다시 확인합니다. REVIEW도 자동 배포가 아닙니다.",
        "결론 1문장, 실패 근거 1건, 다음 변경 1개를 기록합니다. 코드 통과율을 의미 정확도라 부르지 않습니다.",
        "어떤 증거가 더 있어야 배포할 수 있을까?",
        "casebook",
    ),
]

CSS = """
:root{--paper:#fff;--ink:#15191f;--muted:#515e70;--rule:#c7d0dc;--blue:#1954cb;--navy:#0b203a;--wash:#edf3fc;--light:#dce8ff;--font-body:"Course Pretendard",system-ui,sans-serif;--font-code:ui-monospace,Consolas,monospace}
*{box-sizing:border-box}html,body{overflow-x:clip}html{scroll-behavior:smooth;scrollbar-color:var(--muted) var(--paper)}body{margin:0;background:var(--paper);color:var(--ink);font:18px/1.65 var(--font-body)}::selection{background:var(--blue);color:var(--paper)}:focus-visible{outline:3px solid var(--blue);outline-offset:4px}a{color:var(--blue);text-underline-offset:4px}h1,h2,h3,p{margin:0;word-break:keep-all;text-wrap:pretty}h1{font-size:clamp(36px,5vw,64px);line-height:1.15;letter-spacing:-.025em;max-width:18ch}h2{font-size:32px;line-height:1.3;margin-bottom:20px}h3{font-size:22px;line-height:1.4;margin-bottom:12px}p+p{margin-top:16px}header{background:var(--navy);color:var(--paper);padding:64px clamp(24px,6vw,120px);display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:48px}header p{color:var(--light);margin-top:24px}.notebook-table{overflow-x:auto;margin:20px 0 40px}.notebook-table table{min-width:720px}.notebook-table td:nth-child(2){min-width:140px}.notebook-table td:nth-child(3){min-width:200px}.notebook-table th:first-child{width:60px}header nav{display:grid;align-content:center;gap:14px}header a{color:var(--light);font-size:20px}.shell{max-width:1200px;margin:auto;padding:48px 30px;display:grid;grid-template-columns:210px minmax(0,1fr);gap:56px}.side{align-self:start;position:sticky;top:24px}.side a{display:block;font-size:16px;padding:10px 0;border-bottom:1px solid var(--rule);color:var(--ink)}.content{min-width:0}section{padding:40px 0;border-bottom:1px solid var(--rule);scroll-margin-top:24px}section:first-child{padding-top:0}.meta{display:flex;gap:20px;margin:16px 0 24px;color:var(--muted);font-size:16px}.question{font-size:26px;font-weight:700;margin-top:24px;line-height:1.4}.steps{list-style:none;padding:0;margin:0;counter-reset:step}.steps>li{padding:40px 0;border-bottom:1px solid var(--rule)}.steps h2{font-size:30px}.click-path{padding:18px 20px;background:var(--wash);font-weight:700;margin:16px 0}.detail{display:grid;grid-template-columns:100px minmax(0,1fr);gap:20px;margin:18px 0}.detail strong{font-size:16px;color:var(--muted)}code,pre{font-family:var(--font-code)}code{font-size:.9em}pre{padding:24px;background:var(--wash);font-size:15px;white-space:pre-wrap;overflow-wrap:anywhere}table{width:100%;border-collapse:collapse;font-size:16px}th,td{text-align:left;padding:14px 12px;border-bottom:1px solid var(--rule);vertical-align:top}th{background:var(--wash)}figure{margin:28px 0}figure img{width:100%;border:1px solid var(--rule)}figcaption{font-size:15px;color:var(--muted);margin-top:12px}details{margin:20px 0;padding:20px 0;border-top:1px solid var(--rule)}summary{cursor:pointer;font-weight:700}.step-link{display:inline-block;margin-top:20px}.notice{padding:24px;background:var(--wash)}footer{padding:40px 24px;max-width:1200px;margin:auto;color:var(--muted);font-size:15px}.print-button{font:inherit;color:var(--paper);border:1px solid var(--light);background:transparent;padding:12px;cursor:pointer;text-align:left}.print-button:hover{background:var(--blue)}.checklist{padding-left:1.4em}.checklist li{padding:5px 0}
@media(max-width:900px){header{grid-template-columns:1fr;padding:40px 24px;gap:24px}.shell{grid-template-columns:1fr;padding:32px 24px;gap:24px}.side{position:static;display:grid;grid-template-columns:repeat(2,1fr);gap:0 20px}.detail{grid-template-columns:1fr;gap:4px}h2{font-size:28px}.steps h2{font-size:26px}table{font-size:14px}th,td{padding:12px 8px}header nav{gap:10px}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto}}@media print{header{background:var(--paper);color:var(--ink);padding:24px}header p,header a{color:var(--ink)}header nav,.side,.print-button{display:none}.shell{display:block;padding:24px}.steps>li{break-inside:avoid}details{break-inside:avoid}a{color:inherit}}
"""


def safe_local_link(value: str) -> str:
    url = urlsplit(value)
    if (
        url.scheme not in ("http", "https")
        or url.hostname not in ("localhost", "127.0.0.1", "::1")
        or url.username
        or url.password
    ):
        raise ValueError("로컬 실습 URL만 안내에 사용할 수 있습니다.")
    return value


def notebook_tables() -> str:
    guides = json.loads((LAB / "notebook-steps.json").read_text())
    sections = []
    for key, guide in guides.items():
        rows = "".join(
            f'<tr><th scope="row">{i}</th><td>{html.escape(heading)}</td><td>{html.escape(screen)}</td><td>{html.escape(result)}</td></tr>'
            for i, (heading, screen, result) in enumerate(guide["steps"], 1)
        )
        sections.append(f'<h3>{html.escape(guide["title"])}</h3><p><a href="{GITHUB}/notebooks/{guide["filename"]}">{key} Notebook 열기</a></p><div class="notebook-table" tabindex="0" aria-label="{key} 코드 셀 실행 순서. 좁은 화면에서는 가로로 스크롤합니다."><table><thead><tr><th>코드 셀</th><th>단계</th><th>누를 곳</th><th>확인 결과</th></tr></thead><tbody>{rows}</tbody></table></div>')
    return '<section id="notebooks"><h2>VS Code에서 한 셀씩 실행</h2><p>아래 번호는 설명 셀을 제외하고 위에서부터 세는 코드 셀 순서입니다. VS Code 왼쪽 [숫자]는 실행 횟수이므로 기준으로 사용하지 않습니다. 각 셀이 끝난 뒤 다음 셀로 이동합니다.</p><p>09를 마친 뒤 10을 열고 첫 환경 셀부터 다시 시작하세요. 실행이 여러 번 쌓였다면 이번 Notebook이 출력한 요청·실험 링크를 사용합니다.</p>'+''.join(sections)+'</section>'


def render(links: dict[str, str], *, private: bool) -> str:
    esc = html.escape
    items = []
    for i, (title, time, notebook, path, result, explain, question, key) in enumerate(STEPS, 1):
        label = "이번 실행 화면 열기" if private else "로컬 프로젝트 열기"
        if key == "casebook":
            label = "검증한 실제 비교 결과 보기"
        items.append(
            f'''<li id="step-{i}"><h2>{i}. {title}</h2><div class="meta"><span>{time}</span><span>{notebook}</span></div><p class="click-path">{path}</p><div class="detail"><strong>확인 결과</strong><p>{result}</p></div><div class="detail"><strong>설명 포인트</strong><p>{explain}</p></div><p class="question">{question}</p><a class="step-link" href="{esc(links[key], quote=True)}">{label}</a></li>'''
        )
    notice = (
        "이 PC의 최신 실행 파일에서 읽은 실제 요청·실험 링크입니다. 서버 데이터가 남아 있는 동안 사용할 수 있습니다. 다른 학생의 PC에서는 해당 요청이 존재하지 않습니다."
        if private
        else "설치 없이 아래 비교 결과와 강의안을 먼저 볼 수 있습니다. localhost 링크는 본인 PC의 Docker 서버를 실행한 뒤 열립니다. 개별 요청 링크는 Notebook 실행 결과를 사용합니다."
    )
    notebook_links = " · ".join(
        f'<a href="{GITHUB}/notebooks/{name}">{label}</a>'
        for name, label in [
            ("09_langfuse_ollama_tracing.ipynb", "09 요청 추적"),
            ("10_langfuse_experiments_release_gate.ipynb", "10 실험·배포 판단"),
        ]
    )
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>11주차 · 실습 화면과 시연 순서</title><style>{CSS}</style></head><body><header><div><h1>실패 요청에서<br>배포 판단까지</h1><p>11주차 실습 시연 안내 · 100분 수업<br>실제 Ollama × 로컬 Langfuse</p></div><nav aria-label="학습 자료"><a href="{PUBLIC}/lecture/">64쪽 HTML 강의안</a><a href="{PUBLIC}/lab/sample/langfuse/">실제 A/B/C 비교 결과 미리 보기</a><a href="{GITHUB}/langfuse/README.md">Docker·VS Code 준비와 문제 해결</a><button class="print-button" onclick="window.print()">안내 인쇄 / PDF 저장</button></nav></header><div class="shell"><nav class="side" aria-label="시연 순서"><a href="#prepare">시작 전 확인</a><a href="#notebooks">09·10 코드 셀 순서</a>{"".join(f'<a href="#step-{i}">{i}. {s[0]}</a>' for i, s in enumerate(STEPS, 1))}<a href="#recovery">시간 지연·문제 해결</a></nav><main class="content"><section id="prepare"><h2>먼저 열어 둘 세 화면</h2><p class="notice">{notice}</p><ol class="checklist"><li>강의안: 43쪽 미션 → 44쪽 구조의 ‘흐름 보기’</li><li>VS Code: {notebook_links} / 커널은 저장소 .venv</li><li>Langfuse: <a href="{esc(links["home"], quote=True)}">Week 11 Ollama 프로젝트</a></li></ol><p>로그인은 <code>week11/lab/langfuse/.env</code>의 <code>LANGFUSE_LOGIN_EMAIL</code>과 <code>LANGFUSE_LOGIN_PASSWORD</code>를 사용합니다. API 키를 강의 화면이나 제출물에 표시하지 않습니다.</p><details><summary>복사할 준비 명령 · 저장소 루트에서 실행</summary><pre>python -m pip install -r requirements/week11-langfuse.txt
python -m pip check
python week11/lab/langfuse/init_env.py
ollama pull qwen2.5:1.5b-instruct
docker compose -f week11/lab/langfuse/compose.yaml up -d --wait --wait-timeout 300</pre><p>Python 3.11 가상환경을 먼저 선택합니다. 최초 설치·이미지 다운로드는 수업 전에 완료합니다. 09/10 노트북은 각각 첫 환경 셀부터 실행합니다.</p></details><table><thead><tr><th>시간</th><th>내용</th></tr></thead><tbody><tr><td>0–25분</td><td>서비스 구조·평가 데이터·검색 비교 / 01–04 발췌</td></tr><tr><td>25–40분</td><td>실제 생성·작은 모델 평가의 한계 / 07–08</td></tr><tr><td>40–60분</td><td>09 요청 추적 / 아래 2–4단계</td></tr><tr><td>60–85분</td><td>10 실험·배포 조건 / 아래 5–7단계</td></tr><tr><td>85–100분</td><td>사람 검토·배포 판단 / 아래 8단계</td></tr></tbody></table></section>{notebook_tables()}<ol class="steps">{"".join(items)}</ol><section id="recovery"><h2>수업 중 지연에 대한 대응</h2><details open><summary>기록이 아직 보이지 않는 경우</summary><p>Notebook의 <code>wait_for_trace</code>가 저장 완료를 확인한 다음 같은 요청을 새로고침합니다. 전송 직후에는 worker 처리 시간이 필요합니다. 반복 실행으로 새 요청을 계속 만들지 않습니다.</p></details><details><summary>모델 호출 또는 Docker가 준비되지 않은 경우</summary><p>설치 점검은 최대 3분으로 제한하고 교수 화면·실제 비교 결과로 판단 활동을 이어갑니다. 이를 본인의 실시간 실행으로 제출하지 않습니다. 수업 후 준비 안내의 오류 항목을 따라 실행합니다.</p></details><details><summary>이미지·포트·시간 예산</summary><p>여섯 컨테이너가 실행되므로 기기 여유 메모리가 필요합니다. 이 자료는 Docker VM RAM 약 16GB인 macOS에서 검증했습니다. 3011은 Langfuse, 11434는 Ollama입니다. 실행 시간은 장비마다 달라집니다. 3초 조건은 교육용 기본 예산이며 실험 전에 합의합니다.</p></details><details><summary>이번 실행의 바로가기 갱신</summary><pre>python -m week11.lab.demo_guide</pre><p>09의 기록 저장, 10의 비교 저장 후 실행합니다. <code>week11/lab/reports/langfuse/instructor-console.html</code>을 브라우저로 열면 이번 실행의 trace·실험 링크로 연결됩니다. 이 파일은 Git 제외입니다.</p></details></section></main></div><footer>합성 쇼핑 정책 사례 · 실제 실행은 학생 PC에 저장 · 2026-11-11 검증<br>통과율은 인용·기권 계약 검사이며 서비스 의미 정확도나 일반 성능 벤치마크가 아닙니다.</footer></body></html>'''


def build(private: bool = True) -> Path:
    home = "http://localhost:3011/project/week11-local"
    links = dict.fromkeys(["home", "trace", "dataset", "compare", "guard"], home)
    links["casebook"] = PUBLIC + "/lab/sample/langfuse/"
    if private:
        traces = json.loads((LAB / "reports/langfuse/lesson09-traces.json").read_text())
        run = json.loads((LAB / "reports/langfuse/release-comparison.json").read_text())
        links["trace"] = safe_local_link(traces[0]["url"])
        split = urlsplit(links["trace"])
        links["home"] = urlunsplit((split.scheme, split.netloc, "/project/week11-local", "", ""))
        links["dataset"] = links["home"] + "/datasets"
        compare = urlsplit(safe_local_link(run["baseline"]["experiment_url"]))
        links["compare"] = urlunsplit(
            (
                compare.scheme,
                compare.netloc,
                compare.path,
                urlencode(
                    {
                        "baseline": run["baseline"]["experiment_id"],
                        "c": run["guarded"]["experiment_id"],
                    }
                ),
                "",
            )
        )
        guard = next(r for r in run["guarded"]["rows"] if r["question_id"] == "Q24a")
        links["guard"] = safe_local_link(guard["output"]["url"])
        out = LAB / "reports/langfuse/instructor-console.html"
    else:
        out = LAB / "demo/index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(links, private=private), encoding="utf-8")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public", action="store_true", help="개인 실행 ID 없는 공개 안내 생성")
    args = parser.parse_args()
    try:
        print(build(private=not args.public))
    except FileNotFoundError as exc:
        raise SystemExit(
            "09·10 Notebook의 마지막 기록 저장 셀을 먼저 실행하세요. " + str(exc)
        ) from exc


if __name__ == "__main__":
    main()
