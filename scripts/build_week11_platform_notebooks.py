"""Build the Docker/Langfuse trace and release-comparison teaching notebooks."""

import json
from pathlib import Path

import nbformat as n

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "week11/lab/notebooks"
SETUP = """from pathlib import Path
import sys, json
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'week11/lab/langfuse_lab.py').exists())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
assert sys.version_info[:2] == (3, 11), 'Python 3.11 .venv 커널을 선택하세요.'
import pandas as pd
from IPython.display import display, Markdown
from week11.lab.evaluation import load_data
from week11.lab.ollama_lab import OllamaClient
from week11.lab.langfuse_lab import connect_langfuse, traced_question, wait_for_trace, observation_table, score_table
lf = connect_langfuse()  # 이 실습 폴더의 .env만 사용. 키를 출력하지 않음.
ollama = OllamaClient()
print(ollama.probe())
by_id = {q['id']: q for q in load_data()[1]}
"""


def build(name, title, intro, steps):
    guide = json.loads((ROOT / "week11/lab/notebook-steps.json").read_text())[name[:2]]
    assert len(guide["steps"]) == len(steps) + 1
    cell_map = "\n\n**위에서부터 코드 셀을 세는 실행 지도**\n\nVS Code 왼쪽 `[숫자]`는 실행 횟수입니다. 아래 번호는 설명 셀을 제외한 코드 셀 순서입니다. 첫 셀부터 한 개씩 실행하고 완료 후 다음 셀로 이동합니다.\n\n| 코드 셀 | 단계 | 화면에서 누를 곳 | 확인 결과 |\n|---|---|---|---|\n"
    cell_map += "\n".join(f"| {i} | {heading} | {screen} | {result} |" for i, (heading, screen, result) in enumerate(guide["steps"], 1))
    cells = [
        n.v4.new_markdown_cell(f"""# {title}

{intro}

**수업 전 준비:** [Docker·VS Code 안내](../langfuse/README.md)의 명령을 터미널에서 마친 뒤 실행합니다.

```sh
python -m pip install -r requirements/week11-langfuse.txt
python week11/lab/langfuse/init_env.py
docker compose -f week11/lab/langfuse/compose.yaml up -d --wait --wait-timeout 300
ollama pull qwen2.5:1.5b-instruct
```

Ollama 앱과 Docker Desktop이 실행 중이어야 합니다. [Langfuse 화면](http://localhost:3011)에 접속하고
`week11/lab/langfuse/.env`의 `LANGFUSE_LOGIN_EMAIL`, `LANGFUSE_LOGIN_PASSWORD`로 로그인합니다.
이 파일은 본인 PC의 비공개 설정입니다. 노트북 출력이나 GitHub에 키·비밀번호를 복사하지 않습니다.

`.venv` Python 3.11 커널에서 위부터 Shift+Enter. 다른 Notebook의 변수는 필요 없습니다.
모델의 의미 오류는 관찰 대상이며, 연결 실패·파싱 오류를 가짜 성공으로 대체하지 않습니다.
""" + cell_map),
        n.v4.new_code_cell(
            SETUP
            if name.startswith("09")
            else SETUP.replace(", observation_table, score_table", "")
        ),
    ]
    for i, (heading, why, code, check) in enumerate(steps, 1):
        cells += [
            n.v4.new_markdown_cell(f"## {i}. {heading}\n\n{why}"),
            n.v4.new_code_cell(code),
            n.v4.new_markdown_cell("**확인 결과 / 화면에서 볼 것**\n\n" + check),
        ]
    cells += [
        n.v4.new_markdown_cell("""## 마무리

연결이 끝나면 `lf.flush()`로 전송합니다. 실제 저장은 API 재조회로 확인합니다. 모델·프롬프트·기기 상태에 따라 답변과 지연은 달라집니다.
수업 결과는 합성 사례이며 일반적인 서비스 정확도 또는 운영 배포 승인이 아닙니다.

Docker 중지(데이터 유지): `docker compose -f week11/lab/langfuse/compose.yaml stop`
재개: 같은 경로의 `up -d --wait`. **`down -v`는 데이터를 삭제하므로 일반 종료에 사용하지 않습니다.**
[화면별 시연 안내](https://smilesjcha.github.io/llmops-16week/week11/lab/demo/) / [100분 진행·문제 해결](../langfuse/README.md) / [전체 실행 순서](../WALKTHROUGH.md)
""")
    ]
    for i, c in enumerate(cells):
        c["id"] = f"{name[:2]}-cell-{i:02d}"
    nb = n.v4.new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {
                "display_name": "Python 3.11 (llmops)",
                "language": "python",
                "name": "python3",
            }
        },
    )
    n.write(nb, OUT / name)


build(
    "09_langfuse_ollama_tracing.ipynb",
    "09 실제 Ollama 요청의 Langfuse 추적",
    """**상황:** 반품·교환 상담 AI가 왜 잘못 답했는지 요청 하나를 추적합니다.

**20분 핵심:** 2–5단계. 1단계는 SDK 사용법, 6–8단계는 비교·검토·기록 확장입니다.
실제 모델 호출: 1단계 1회, 전체 요청 3건 × 생성·평가 2회 = 총 7회.
평가 코드는 VS Code에서 실행되고, Docker Langfuse는 기록을 저장·표시합니다.""",
    [
        (
            "with 문으로 직접 기록하는 실제 생성",
            "전체 프레임워크 전에 SDK의 최소 구문을 실행합니다. 질문·답변·토큰이 화면에 어떻게 대응되는지 확인합니다.",
            """from week11.lab.ollama_lab import ANSWER_SCHEMA
with lf.start_as_current_observation(name='mini-ollama-request', input='반품 기간은?') as root:
    with lf.start_as_current_observation(name='ollama-generation', as_type='generation', model=ollama.model) as generation:
        messages = [{'role':'user','content':'정책: 수령 후 7일 이내 반품 접수. 질문: 반품 기간은? JSON answer, citations=[], abstain=false로 답하라.'}]
        actual = ollama.chat(messages, ANSWER_SCHEMA)
        generation.update(input=messages, output=actual['parsed'], usage_details={'input':actual['input_tokens'],'output':actual['output_tokens']})
    root.update(output=actual['parsed'])
    mini_trace_id = root.trace_id
lf.flush()
display(Markdown(f"[실제 생성 요청 열기]({lf.get_trace_url(trace_id=mini_trace_id)})"))""",
            "로그인한 브라우저에서 링크를 엽니다. root 아래 generation 하나가 보이고 실제 입력·출력·모델·토큰을 확인합니다. 이 최소 예제에는 검색·평가 단계가 아직 없습니다.",
        ),
        (
            "검색·생성·검사·평가를 한 요청으로 연결",
            "Q03a는 교환 기간과 비용을 함께 묻습니다. 실행 전에 기간·비용·조건이 모두 나올지 예상해 보세요.",
            """first = traced_question(lf, ollama, by_id['Q03a'])
print(first['answer'])
display(Markdown(f"[Q03a 전체 요청 열기]({first['url']})"))""",
            "전체 요청 아래 01-retrieval → 02-ollama-answer → 03-code-checks → 04-ollama-judge가 생깁니다. 원본 구현은 [langfuse_lab.py](../langfuse_lab.py)의 traced_question이며 각 실제 작업을 with 문으로 감쌉니다.",
        ),
        (
            "서버 저장과 부모·자식 관계 확인",
            "SDK 전송 성공과 서버 저장 완료를 구분합니다. 백그라운드 worker 처리 후 API로 다시 읽습니다.",
            """stored = wait_for_trace(lf, first)
display(pd.DataFrame(observation_table(stored)))
roots = [o for o in stored['observations'] if o['name'].startswith('rag-')]
assert len(roots) == 1
root_id = roots[0]['id']
assert sum(o.get('parentObservationId') == root_id for o in stored['observations']) == 4
print('실제 부모 1개 + 하위 작업 4개 확인')""",
            "요청 하나에 observations 5개. generation 2개에는 실제 토큰이 있습니다. 검색 문서는 retrieval Output, 모델에 보낸 메시지는 answer Input에서 확인합니다.",
        ),
        (
            "평가 점수와 판단 근거 확인",
            "코드 점수와 실제 모델 판정은 서로 다른 근거입니다. 모델이 supported라고 해도 코드 실패를 덮지 않습니다.",
            """display(pd.DataFrame(score_table(stored)))
print('참고 기준:', by_id['Q03a']['reference'])
print('실제 답변:', first['answer']['answer'])
print('실제 평가자:', first['judge'])""",
            "Trace의 Scores에서 BOOLEAN 검사와 CATEGORICAL llm_groundedness를 확인합니다. 숫자 1은 해당 코드 조건 통과이며 답변 정확도 100%가 아닙니다. 기간·비용·미착용·재고 조건을 직접 읽어봅니다.",
        ),
        (
            "문서 밖 재고 질문의 두 응답 비교",
            "“현재 재고가 없다”와 “재고를 확인할 수 없다”는 의미가 다릅니다. 어느 단계에서 추측했는지 찾습니다.",
            """baseline = traced_question(lf, ollama, by_id['Q24a'], prompt_version='baseline')
grounded = traced_question(lf, ollama, by_id['Q24a'], prompt_version='grounded')
for result in [baseline, grounded]:
    wait_for_trace(lf, result)
    print(result['prompt_version'], result['answer'], result['judge'])
    display(Markdown(f"[{result['prompt_version']} 요청 열기]({result['url']})"))""",
            "두 요청의 검색 문서와 모델이 실제로 보았던 Input을 비교합니다. 확인 불가 문장인데 abstain=false일 수 있습니다. 실제 판정은 실행마다 달라집니다.",
        ),
        (
            "사람 검토의 기록",
            "먼저 실제 답변을 읽고 아래 REVIEW를 직접 선택하세요. 기본값 None은 사람 평가를 수행하지 않았다는 뜻입니다.",
            """REVIEW = None  # 읽은 뒤 'supported', 'unsupported', 'needs_review' 중 선택
COMMENT = ''  # 판단 근거를 한 문장으로 작성
if REVIEW is None:
    print('사람 검토 미실행. 답변·근거를 읽은 뒤 REVIEW와 COMMENT를 채우세요.')
else:
    assert REVIEW in {'supported','unsupported','needs_review'} and COMMENT.strip()
    lf.create_score(trace_id=grounded['trace_id'], name='human_review', value=REVIEW,
                    data_type='CATEGORICAL', comment=COMMENT, score_id=grounded['trace_id']+'-human-review')
    lf.flush()
    print('사람 검토 전송. Scores를 새로고침하세요.')""",
            "미실행 평가를 사람 평가로 채우지 않습니다. 실제 검토 후 이름이 다른 human_review와 llm_groundedness를 비교합니다.",
        ),
        (
            "실패 요청을 다음 실습으로 전달",
            "가짜 재고 안내가 반복되지 않도록, 관찰한 실패를 회귀 평가 사례로 남깁니다.",
            """out = ROOT/'week11/lab/reports/langfuse'
out.mkdir(parents=True, exist_ok=True)
(out/'lesson09-traces.json').write_text(json.dumps([first,baseline,grounded], ensure_ascii=False, indent=2), encoding='utf-8')
print(out/'lesson09-traces.json')
print('다음 실습: 같은 질문 집합으로 세 버전을 비교한 뒤 배포 기준 적용')""",
            "파일은 본인 로컬 Git 제외 폴더에 저장됩니다. 10번은 독립 실행되므로 이 파일이 없어도 됩니다.",
        ),
        (
            "관찰에서 개선으로 이어지는 질문",
            "실험 전에 결론을 예측하되, 결과는 실제 기록으로 설명합니다.",
            """display(pd.DataFrame([
 {'관찰':'재고를 단정한 답변','검토':'검색 문서에 실시간 재고가 있는가','다음 실험':'기능 제한 정책'},
 {'관찰':'확인 불가 문장 + abstain=false','검토':'응답 계약이 의미와 일치하는가','다음 실험':'코드 검사 + 정책 분기'},
 {'관찰':'평가자도 supported','검토':'사람 기준과 독립적으로 대조했는가','다음 실험':'실패 사례 회귀 평가'},
]))
lf.flush()""",
            "모델에게 더 강하게 부탁하는 변경과, 애초에 제공하지 않는 기능을 차단하는 서비스 변경을 구분합니다.",
        ),
    ],
)

build(
    "10_langfuse_experiments_release_gate.ipynb",
    "10 세 버전의 실험 비교와 배포 전 검증",
    """**상황:** “금요일 오후, 새 상담 AI를 배포해도 될까?” 3개 정상 질문과 재고 실패 질문 1개로 변경을 검증합니다.

**25분 핵심:** 1–7단계. Docker·모델은 수업 전에 준비합니다. 기본 실행은 모델 호출 총 24회(실패 요청 2 + 기준선 8 + 프롬프트 개선 8 + 기능 정책 6), 동시성 1입니다.

A 기준 프롬프트 / B 근거 제한 프롬프트 / C 근거 제한 + 기능 정책.
C의 실시간 조회 요청은 실제 서비스 정책으로 중단하며 모델 호출을 수행하지 않습니다. 가짜 모델 응답이 아닙니다.
같은 4개 사례와 같은 모델을 사용하고, 모델의 오판을 포함한 원본 결과를 보존합니다.""",
    [
        (
            "실패 관찰과 개선 가설",
            "재고 질문의 실제 응답을 확인합니다. 단일 질문을 본 뒤 전체 성능이 좋아졌다고 판단하지 않습니다.",
            """from week11.lab.release_lab import ensure_dataset, run_version, release_decision, DEFAULT_POLICY
incident = traced_question(lf, ollama, by_id['Q24a'], prompt_version='baseline')
wait_for_trace(lf, incident)
display(Markdown(f"[재고 질문 관찰 요청 열기]({incident['url']})"))
print(incident['answer'])
print('가설 B: 근거 제한 프롬프트로 개선 / 가설 C: 미지원 기능을 서비스에서 차단')""",
            "실제 답변이 우연히 올바르더라도 경계 사례로 유지합니다. 실패 사례만 모으지 않고 정상 사례도 함께 넣습니다.",
        ),
        (
            "정상 사례와 실패 사례의 고정 데이터",
            "내용 해시가 같은 데이터만 재사용합니다. 다른 사람이 바꾼 평가 기준은 자동 덮어쓰지 않습니다.",
            """dataset = ensure_dataset(lf, incident)
display(pd.DataFrame([{'id':i.input['question_id'], 'question':i.input['question'],
                      'request_type':i.input['requested_capability'], 'expected':i.expected_output} for i in dataset.items]))
print('데이터:', dataset.name)
POLICY = dict(DEFAULT_POLICY)  # 실험 결과를 보기 전에 고정
print('배포 전 조건:', POLICY)""",
            "Datasets에 4개 사례가 보입니다. Q24a는 source trace와 연결됩니다. requested_capability는 상담 화면의 메뉴/라우트 입력입니다. 정답의 answerable 값으로 서비스 분기를 선택하지 않으며, 자유 문장의 의도 분류는 이 실습 범위 밖입니다.",
        ),
        (
            "A 기준선의 실제 실험",
            "같은 검색기와 모델을 사용합니다. 기본 동시성 1로 로컬 모델 큐 적체를 피합니다.",
            """baseline = run_version(lf, ollama, dataset, 'baseline')
display(Markdown(f"[A 기준선 실험 열기]({baseline['experiment_url']})"))
display(pd.DataFrame([{'id':r['question_id'], 'answer':r['output']['answer'],
                      'judge':r['output']['judge']} for r in baseline['rows']]))""",
            "Experiments에 기준선 실행 4개가 생깁니다. generation_ms, structural_pass, false_accept와 실제 답변을 함께 읽습니다.",
        ),
        (
            "B 프롬프트 개선의 실제 실험",
            "평가 데이터와 모델을 고정하고 프롬프트만 변경합니다. 성공을 가정하지 않습니다.",
            """candidate = run_version(lf, ollama, dataset, 'grounded')
display(Markdown(f"[B 프롬프트 개선 실험 열기]({candidate['experiment_url']})"))
decision_b = release_decision(baseline, candidate, POLICY)
print(decision_b['decision'])
display(pd.DataFrame(decision_b['checks']))""",
            "실제 실행에서 더 좋아질 수도, 비슷하거나 나빠질 수도 있습니다. 문장은 확인 불가인데 기권 필드가 틀린 사례를 찾아봅니다.",
        ),
        (
            "C 기능 정책의 실제 적용",
            "policy_qa만 구현된 서비스에서는 live_inventory를 조회할 수 없습니다. 서비스의 능력 범위를 코드로 제한합니다.",
            """from week11.lab.release_lab import capability_response
print('정책 안내:', capability_response('policy_qa'))
print('미지원 실시간 조회:', capability_response('live_inventory'))
guarded = run_version(lf, ollama, dataset, 'capability_guard')
display(Markdown(f"[C 기능 정책 실험 열기]({guarded['experiment_url']})"))
guard_case = next(row for row in guarded['rows'] if row['question_id'] == 'Q24a')
display(Markdown(f"[C 재고 질문 요청 열기]({guard_case['output']['url']})"))
decision_c = release_decision(baseline, guarded, POLICY)
print(decision_c['decision'])
display(pd.DataFrame(decision_c['checks']))""",
            "Q24a trace에는 capability-check와 contract-checks가 보이고 모델 generation은 없습니다. 정책 응답임을 명시합니다. 정상 질문 3개는 여전히 실제 Ollama 생성·평가를 실행합니다.",
        ),
        (
            "한 화면에서 비교하고 배포 보류·검토 결정",
            "평균 점수가 필수 실패를 상쇄하지 않도록 개별 조건을 확인합니다. 4건으로 p95나 일반 성능을 주장하지 않습니다.",
            """display(pd.DataFrame([
 {'version':'A 기준선', **decision_b['summary']['baseline']},
 {'version':'B 프롬프트', **decision_b['summary']['candidate']},
 {'version':'C 기능 정책', **decision_c['summary']['candidate']},
]))
for label,decision in [('B',decision_b),('C',decision_c)]:
    print(label,decision['decision'],decision['reason'])""",
            "HOLD는 배포 보류, REVIEW는 사람 검토 대상으로 이동입니다. REVIEW도 자동 배포가 아닙니다. 인용·기권 검사 통과율은 답변 의미 정확도와 다릅니다. 작은 모델의 판정은 필수 실패를 덮어쓰지 않습니다.",
        ),
        (
            "서버에 저장된 실험과 점수 검증",
            "반환된 Python 객체만 믿지 않고 실제 Langfuse API에서 각 요청을 재조회합니다.",
            """checks = []
for experiment in [baseline,candidate,guarded]:
    for row in experiment['rows']:
        saved = wait_for_trace(lf,row['output'])
        checks.append({'version':experiment['version'],'id':row['question_id'],
                       'observations':len(saved['observations']),'scores':len(saved['scores'])})
display(pd.DataFrame(checks))
print('3개 실험 × 4개 요청의 서버 저장 확인')""",
            "Experiments에서 같은 데이터의 A/B/C를 선택하여 비교하고, 실패 셀에서 개별 trace로 이동합니다. 서비스 기능 정책의 경로는 generation이 없는 것이 정상입니다.",
        ),
        (
            "배포 판단 근거와 다음 실험 기록",
            "관찰 → 실패 사례 → 고정 평가 → 변경 비교 → 배포 조건 → 사람 검토까지 연결합니다.",
            """out = ROOT/'week11/lab/reports/langfuse'
out.mkdir(parents=True,exist_ok=True)
report = {'baseline':baseline,'candidate':candidate,'guarded':guarded,'decision':decision_b,'guarded_decision':decision_c}
(out/'release-comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(out/'release-comparison.json')
print('다음 과제: 정상 답변의 조건 누락을 사람이 검토하고, 검토 근거와 다음 변경 하나를 제안')
lf.flush()""",
            "09번도 기록 저장을 마쳤다면 터미널에서 `python -m week11.lab.demo_guide`로 이번 실행의 화면별 바로가기를 만듭니다. `reports/langfuse/instructor-console.html`을 브라우저로 여세요. 새 마감 과제가 아닌 수업 활동입니다. CLI의 --enforce-gate는 B가 HOLD이면 종료 코드 2로 자동 차단합니다. 실제 운영 배포·롤백은 실행하지 않습니다. 3초 예산은 교육용 기본값이며 기기·서비스 조건에 맞게 실험 전에 정해야 합니다.",
        ),
    ],
)
print("Built platform notebooks 09 and 10")
