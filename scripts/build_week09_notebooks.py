"""Generate output-free, independent notebooks without changing source code at runtime."""

from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
SETUP = """from pathlib import Path
import sys, asyncio, json, time
from dataclasses import replace
import numpy as np
import httpx
from IPython.display import display
ROOT = next(p for p in [Path.cwd(),*Path.cwd().parents] if (p/'course_labs').is_dir())
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from week09.lab.app import create_app
from week09.lab.service import Settings, ChatRequest, Service, TTLCache, TokenBucket, cache_key
from week09.lab.benchmark import run_load, summarize
assert sys.version_info[:2] == (3,11), 'Python 3.11 .venv 커널 선택'
OUT = ROOT/'output/validation/week09-lab'
OUT.mkdir(parents=True,exist_ok=True)
print('Python',sys.version.split()[0],'NumPy',np.__version__,'HTTPX',httpx.__version__)
"""


def notebook(name, title, intro, steps):
    cells = [
        nbf.v4.new_markdown_cell(
            f"# {title}\n\n{intro}\n\n위에서 아래로 실행합니다. 각 실험은 새 앱을 사용하며 실제 LLM·GPU·외부 API는 기본 경로에 없습니다. 먼저 결과를 예상하고 실행한 뒤 변수 하나를 바꾸고 관찰을 기록하세요."
        ),
        nbf.v4.new_code_cell(SETUP),
    ]
    for heading, explanation, code in steps:
        cells += [
            nbf.v4.new_markdown_cell(f"## {heading}\n\n{explanation}"),
            nbf.v4.new_code_cell(code),
        ]
    cells.append(
        nbf.v4.new_markdown_cell(
            "## 포트폴리오 기록\n\n변경 변수 / 고정 조건 / 실제 관측값 / 실패 사례 / 해석의 한계 / 다음 확인을 기록하세요. 개인정보·학생 원문은 공개 저장소에 넣지 않습니다. 별도 과제 마감은 소속 공지를 따르며 이 실습에서 새 제출 기한을 만들지 않습니다."
        )
    )
    nb = nbf.v4.new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {
                "display_name": "Python 3.11 (.venv)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.11"},
        },
    )
    nbf.validate(nb)
    target = ROOT / "week09/lab/notebooks" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, target)
    print(name, len(cells), "cells", sum(c.cell_type == "code" for c in cells), "code")


notebook(
    "01_api_contract.ipynb",
    "01 · API 계약과 오류 응답",
    "FastAPI·Pydantic의 입출력 계약을 실제 요청으로 확인합니다. 권장 15분.",
    [
        (
            "입력 명세",
            "생성 함수 호출 전에 필드·길이·타입을 검사합니다. max_tokens는 MOCK에서 토큰 수를 실제 계산하지 않으며 Ollama에만 생성 제한으로 전달합니다.",
            "display(ChatRequest.model_json_schema())\nrequest = ChatRequest(message='반품 정책의 근거', max_tokens=64)\nassert request.message == '반품 정책의 근거'",
        ),
        (
            "앱과 서버의 구분",
            "이 커널 안에서 앱을 직접 호출합니다. 포트·네트워크·Uvicorn 성능은 측정하지 않습니다.",
            "app = create_app()\ntransport = httpx.ASGITransport(app=app)\nprint('별도 서버 없이 HTTP 계약 검사')",
        ),
        (
            "상태와 준비",
            "alive는 프로세스, ready는 제공자 준비 확인입니다. MOCK 준비는 모델 다운로드를 뜻하지 않습니다.",
            "async with httpx.AsyncClient(transport=transport,base_url='http://lab') as client:\n    health = await client.get('/health')\n    ready = await client.get('/ready')\nassert health.status_code == ready.status_code == 200\ndisplay(health.json()); display(ready.json())",
        ),
        (
            "정상 응답",
            "요청 ID·버전·캐시 여부를 함께 확인합니다. 200은 의미 정확성의 증거가 아닙니다.",
            "async with httpx.AsyncClient(transport=transport,base_url='http://lab') as client:\n    response = await client.post('/api/v1/chat',json=request.model_dump())\nbody = response.json()\nassert response.status_code == 200 and body['simulated']\nassert body['request_id'] == response.headers['x-request-id']\ndisplay(body)",
        ),
        (
            "빈 문자열과 공백",
            "둘 다 의미 없는 입력이므로 거부합니다. 원문 입력을 오류 응답에 복사하지 않습니다.",
            "invalid = []\nasync with httpx.AsyncClient(transport=transport,base_url='http://lab') as client:\n    for value in ['', '   ']:\n        invalid.append(await client.post('/api/v1/chat',json={'message':value}))\nassert all(r.status_code == 422 for r in invalid)\ndisplay(invalid[0].json())",
        ),
        (
            "타입과 추가 필드",
            "숫자 문자열의 조용한 변환과 임의 필드를 허용하지 않습니다.",
            "cases = [{'message':'x','max_tokens':'64'},{'message':'x','role':'admin'},{'message':'x'*1001}]\nresults = []\nasync with httpx.AsyncClient(transport=transport,base_url='http://lab') as client:\n    for case in cases:\n        results.append(await client.post('/api/v1/chat',json=case))\nassert all(r.status_code == 422 for r in results)\ndisplay([r.json()['error']['fields'] for r in results])",
        ),
        (
            "OpenAPI 확인",
            "브라우저 /docs와 같은 명세를 읽습니다. 프레임워크의 최신 기능 대신 고정된 0.115.14에서 지원하는 기능을 사용합니다.",
            "schema = app.openapi()\nassert '/api/v1/chat' in schema['paths']\ndisplay(schema['components']['schemas']['ChatResponse']['properties'])",
        ),
        (
            "개인정보 없는 추적",
            "메시지·답변 원문 없이 상태와 경과 시간만 기록합니다. 메모리 캐시는 답변을 보유하므로 민감 데이터에 안전한 저장소가 아닙니다.",
            "stats = list(app.state.service.traces)\nassert all('message' not in r and 'output' not in r for r in stats)\ndisplay(stats)",
        ),
        (
            "상태 코드 분류",
            "404는 경로, 422는 입력, 502는 상류 응답 문제입니다. 같은 재시도 정책을 적용하지 않습니다.",
            "async with httpx.AsyncClient(transport=transport,base_url='http://lab') as client:\n    missing = await client.get('/missing')\nassert missing.status_code == 404\nstatus_plan = {'422':'입력 수정','429':'빈도 감소','503':'용량·연결 확인','504':'시간 예산·상류 확인'}\ndisplay(status_plan)",
        ),
        (
            "내 서비스 계약",
            "자신의 기획서 요구사항을 입력·출력·실패 계약으로 옮깁니다.",
            "contract = {'input':'질문 1–1000자','output':['답변','request_id','버전'],'failure':'근거가 없으면 검토 안내','excluded':'자동 성적 결정'}\nassert contract['failure'] and contract['excluded']\ndisplay(contract)",
        ),
    ],
)

notebook(
    "02_async_reliability.ipynb",
    "02 · 비동기 처리와 실패 복구",
    "동시성·용량 제한·대기시간을 각각 바꿉니다. 권장 20분.",
    [
        (
            "기다리는 작업",
            "asyncio.sleep은 네트워크 대기를 흉내 냅니다. CPU·GPU 연산이 빨라진다는 증거가 아닙니다.",
            "async def io_job():\n    await asyncio.sleep(.03)\n    return 'done'\nstart = time.perf_counter()\nserial = []\nfor _ in range(4):\n    serial.append(await io_job())\nserial_s = time.perf_counter()-start\nstart = time.perf_counter()\nparallel = await asyncio.gather(*(io_job() for _ in range(4)))\nconcurrent_s = time.perf_counter()-start\nassert serial == parallel\ndisplay({'serial_s':serial_s,'concurrent_s':concurrent_s,'scope':'수면 모사'})",
        ),
        (
            "블로킹 호출의 분리",
            "동기 I/O 함수는 필요 시 스레드로 이동할 수 있습니다. GIL이 있는 CPU Python 코드를 같은 이유로 병렬화하지 않습니다.",
            "def blocking_io():\n    time.sleep(.01)\n    return 'blocking I/O demo'\nvalue = await asyncio.to_thread(blocking_io)\nassert value == 'blocking I/O demo'",
        ),
        (
            "용량 한도",
            "max_inflight=1이면 실행 중 요청 외의 요청을 즉시 503으로 거절합니다. 무제한 대기열이 없습니다.",
            "app = create_app(Settings(max_inflight=1,mock_delay_s=.08,timeout_s=.3))\nasync with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n    first = asyncio.create_task(client.post('/api/v1/chat',json={'message':'A','use_cache':False}))\n    while app.state.service.active == 0: await asyncio.sleep(.001)\n    second = await client.post('/api/v1/chat',json={'message':'B'})\n    original = await first\nassert original.status_code == 200 and second.status_code == 503\nassert app.state.service.active == 0\ndisplay(second.json())",
        ),
        (
            "제한시간 초과",
            "asyncio.timeout이 상류 호출을 감쌉니다. 외부 GPU 작업의 종료 보장과는 다릅니다.",
            "app = create_app(Settings(timeout_s=.02))\nasync with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n    timeout_response = await client.post('/api/v1/chat',json={'message':'x','scenario':'timeout'})\nassert timeout_response.status_code == 504 and app.state.service.active == 0\ndisplay(timeout_response.json())",
        ),
        (
            "상류 오류",
            "502와 504를 구분하고 원본 제공자 오류 본문을 노출하지 않습니다.",
            "async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n    upstream = await client.post('/api/v1/chat',json={'message':'x','scenario':'upstream_error'})\nassert upstream.status_code == 502\ndisplay(upstream.json())",
        ),
        (
            "취소 후 자원 해제",
            "클라이언트 취소 후 active가 남으면 후속 요청이 계속 거절될 수 있습니다.",
            "service = Service(Settings(timeout_s=1,mock_delay_s=.2))\ntask = asyncio.create_task(service.chat(ChatRequest(message='x'),'cancel-demo'))\nawait asyncio.sleep(.001)\ntask.cancel()\ntry:\n    await task\nexcept asyncio.CancelledError:\n    pass\nassert service.active == 0\ndisplay(list(service.traces))",
        ),
        (
            "빈도 제한과 용량 제한",
            "Token bucket은 시간당 유입, active는 실행 중 작업 수입니다. 이 예시는 전체 프로세스 버킷 하나입니다.",
            "now = [0.]\nbucket = TokenBucket(2,2,clock=lambda:now[0])\nassert [bucket.allow() for _ in range(3)] == [True,True,False]\nnow[0] = .5\nassert bucket.allow()\nprint('0.5초 후 토큰 1개 보충')",
        ),
        (
            "429 응답",
            "캐시 적중 요청도 유입 한도를 소비합니다.",
            "app = create_app(Settings(burst=1,rate_per_s=.001))\nasync with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n    one = await client.post('/api/v1/chat',json={'message':'x'})\n    two = await client.post('/api/v1/chat',json={'message':'x'})\nassert one.status_code == 200 and two.status_code == 429\ndisplay(two.headers.get('retry-after'))",
        ),
        (
            "재시도의 조건",
            "이번 앱은 자동 재시도를 하지 않습니다. 생성 중복·과금·증폭 위험과 서버 안내를 먼저 검토합니다.",
            "retry_plan = {'422':'재시도 전 입력 수정','429':'Retry-After·전체 시간 예산','503':'백오프·횟수 상한·용량 확인','504':'상류 작업 생존 여부·중복 비용 확인'}\nassert len(retry_plan) == 4\ndisplay(retry_plan)",
        ),
        (
            "실패 복구 기록",
            "실패 코드를 지우고 정상값으로 바꾸지 않습니다.",
            "report = {'observed':[503,504,502,429],'resource_release':'active=0 확인','remaining':'실제 제공자 취소·다중 worker·인증 미검증'}\n(OUT/'reliability.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')\ndisplay(report)",
        ),
    ],
)

notebook(
    "03_cache_versions.ipynb",
    "03 · 캐시와 버전 경계",
    "적중률보다 같은 답을 재사용해도 되는 조건부터 정의합니다. 권장 15분.",
    [
        (
            "같은 요청 두 번",
            "두 번째 요청의 캐시 적중과 제공자 호출 수를 확인합니다.",
            "app = create_app()\nasync with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n    a = (await client.post('/api/v1/chat',json={'message':'반품 정책'})).json()\n    b = (await client.post('/api/v1/chat',json={'message':'반품 정책'})).json()\nassert not a['cached'] and b['cached'] and app.state.service.provider_calls == 1\ndisplay([a,b])",
        ),
        (
            "파라미터와 버전",
            "모델·제공자·프롬프트·출력 스키마·생성 설정은 캐시 의미를 바꿉니다.",
            "req = ChatRequest(message='x')\ncfg = Settings()\nkeys = [cache_key(req,cfg), cache_key(req,replace(cfg,prompt_version='v2')),cache_key(req.model_copy(update={'max_tokens':32}),cfg)]\nassert len(set(keys)) == 3\ndisplay(keys)",
        ),
        (
            "권한 경계",
            "아래는 설계 명세입니다. 이번 앱에는 인증·tenant·RAG 문서가 없어 다중 사용자 권한 분리를 구현하지 않습니다.",
            "production_key_spec = ['인증된 tenant/권한','질문','모델 revision','프롬프트 버전','문서 revision','생성 설정','출력 schema']\nassert '인증된 tenant/권한' in production_key_spec\ndisplay(production_key_spec)",
        ),
        (
            "만료 경계",
            "가짜 시계로 빠르게 실험합니다. 만료 시각과 같으면 적중하지 않습니다.",
            "clock = [0.]\ncache = TTLCache(2,2,clock=lambda:clock[0])\ncache.set('A','version1')\nassert cache.get('A') == 'version1'\nclock[0] = 2\nassert cache.get('A') is None",
        ),
        (
            "메모리 상한",
            "가장 최근에 접근하지 않은 항목부터 제거합니다. 용량 상한이 없으면 긴 수업에서도 메모리가 누적됩니다.",
            "cache = TTLCache(30,2)\ncache.set('A','a'); cache.set('B','b'); cache.get('A'); cache.set('C','c')\nassert cache.get('B') is None and len(cache.values) == 2\nprint(list(cache.values))",
        ),
        (
            "동시에 같은 질문",
            "캐시는 진행 중인 작업을 합치지 않습니다. 콜드 캐시에서 중복 호출이 발생하는 반례입니다.",
            "app = create_app(Settings(max_inflight=2))\nasync with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n    responses = await asyncio.gather(*(client.post('/api/v1/chat',json={'message':'동일 질문'}) for _ in range(2)))\nassert app.state.service.provider_calls == 2\nassert all(not r.json()['cached'] for r in responses)\nprint('중복 진행 작업 병합(single-flight)은 별도 확장 과제')",
        ),
        (
            "실패 응답의 재사용 방지",
            "장애 주입은 성공 캐시를 우회합니다. 오류를 정상 답변으로 캐시하지 않습니다.",
            "app = create_app(Settings(timeout_s=.01))\nasync with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n    failed = await client.post('/api/v1/chat',json={'message':'x','scenario':'timeout'})\nassert failed.status_code == 504 and len(app.state.service.cache.values) == 0",
        ),
        (
            "캐시 비활성화",
            "같은 질문으로도 제공자를 매번 호출할 수 있습니다. 부하 비교에서는 조건을 고정합니다.",
            "app = create_app()\nasync with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n    for _ in range(2):\n        await client.post('/api/v1/chat',json={'message':'x','use_cache':False})\nassert app.state.service.provider_calls == 2",
        ),
        (
            "캐시 삭제와 개인정보",
            "해시는 암호화가 아니며 짧은 입력은 추측될 수 있습니다. 원문·캐시값·백업·로그를 함께 다룹니다.",
            "policy = {'allow':'합성 공개 예시만','retention':'30초, 최대128항목','restart':'메모리 초기화','production_gap':'권한별 분리·암호화·삭제 감사·다중 worker 동기화'}\n(OUT/'cache-policy.json').write_text(json.dumps(policy,ensure_ascii=False,indent=2),encoding='utf-8')\ndisplay(policy)",
        ),
    ],
)

notebook(
    "04_streaming_failures.ipynb",
    "04 · 스트리밍과 완료 계약",
    "SSE 이벤트 형식과 실패·취소를 다룹니다. 권장 15분. ASGITransport는 응답을 버퍼링하므로 첫 조각 지연을 측정하지 않습니다.",
    [
        (
            "SSE 프레임",
            "event와 data 뒤의 빈 줄이 한 프레임의 끝입니다. 실제 LLM 토큰이 아닌 문자 조각입니다.",
            "frame = 'event: delta\\ndata: {\"text\":\"hello\"}\\n\\n'\nassert frame.endswith('\\n\\n')\nprint(frame)",
        ),
        (
            "프레임 파서",
            "가독성을 위한 완성 응답 파서입니다. 브라우저 예제는 네트워크 조각 경계를 따로 누적합니다.",
            "def parse_events(text):\n    rows = []\n    for block in text.strip().split('\\n\\n'):\n        fields = dict(line.split(':',1) for line in block.splitlines() if ':' in line)\n        if 'data' in fields:\n            rows.append({'event':fields.get('event','message').strip(),'data':json.loads(fields['data'])})\n    return rows\nassert parse_events(frame)[0]['data']['text'] == 'hello'",
        ),
        (
            "정상 스트림",
            "meta 이후 delta들을 합치고 done을 확인합니다. HTTP 200만으로 완료 처리하지 않습니다.",
            "app = create_app(Settings(mock_delay_s=.001,timeout_s=.1))\nasync with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n    r = await client.post('/api/v1/chat/stream',json={'message':'반품 정책'})\nevents = parse_events(r.text)\nassert events[0]['event'] == 'meta' and events[-1]['event'] == 'done'\nanswer = ''.join(x['data']['text'] for x in events if x['event']=='delta')\nassert '[합성 정책 예시]' in answer\ndisplay(events)",
        ),
        (
            "헤더 이후의 실패",
            "응답이 이미 시작됐으므로 오류 이벤트로 미완료를 알립니다. 상태 코드는 200으로 남습니다.",
            "async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n    r = await client.post('/api/v1/chat/stream',json={'message':'x','scenario':'timeout'})\nfailed_events = parse_events(r.text)\nassert r.status_code == 200 and failed_events[-1]['event'] == 'error'\nassert not any(e['event']=='done' for e in failed_events)\nassert app.state.service.active == 0\ndisplay(failed_events)",
        ),
        (
            "상류 오류와 사용자 표시",
            "불완전 답변을 성공 결과로 저장하지 않습니다.",
            "async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n    r = await client.post('/api/v1/chat/stream',json={'message':'x','scenario':'upstream_error'})\nassert parse_events(r.text)[-1]['data']['complete'] is False\nprint('화면: 실패 사유·재시도 가능 여부·다음 행동')",
        ),
        (
            "중도 종료와 자원",
            "생성기를 닫았을 때도 finally에서 active가 해제돼야 합니다.",
            "class Connected:\n    async def is_disconnected(self): return False\nservice = Service(Settings(mock_delay_s=.001))\nservice.admit()\ngenerator = service.stream(ChatRequest(message='x'),'manual-close',Connected())\nprint(await anext(generator))\nawait generator.aclose()\nassert service.active == 0",
        ),
        (
            "첫 응답과 첫 내용",
            "meta 도착을 첫 토큰 도착으로 측정하면 빠르게 보이는 착시가 생깁니다.",
            "timing_spec = {'first_byte':'첫 바이트','first_delta':'첫 내용 조각','complete':'done 수신','transport':'실제 로컬 TCP에서 별도 측정'}\ndisplay(timing_spec)",
        ),
        (
            "실제 서버로 확장",
            "터미널에서 서버를 띄운 후 curl -N 또는 브라우저로 확인합니다. 자동 실행은 외부 서버를 호출하지 않습니다.",
            "print('python -m uvicorn week09.lab.app:app --host 127.0.0.1 --port 8009')\nprint('브라우저: http://127.0.0.1:8009/ → 스트리밍 → 수신 중단')\nprint('별도 검증: python scripts/verify_week09_live.py')",
        ),
        (
            "완료 계약 기록",
            "SSE는 웹소켓과 다른 단방향 전달 형식입니다. POST는 fetch를 사용하며 기본 EventSource에 POST body를 넣지 않습니다.",
            "contract = {'normal':['meta','delta','done'],'failed':['meta','error'],'cancelled':'done 없음, 자원 해제','transport_test':'실제 TCP 필요'}\n(OUT/'stream-contract.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2),encoding='utf-8')\ndisplay(contract)",
        ),
    ],
)

notebook(
    "05_load_and_project.ipynb",
    "05 · 부하 실험과 프로젝트 연결",
    "성공 지연·오류율·성공 처리량을 같이 읽습니다. 권장 20분. 고정 응답·수면 모사이며 GPU 벤치마크가 아닙니다.",
    [
        (
            "실험 조건",
            "새 앱에서 캐시를 끄고 동일 작업을 수행합니다. warmup은 지표에서 제외합니다.",
            "cfg = Settings(max_inflight=2,mock_delay_s=.03,timeout_s=.3)\nreports = []\nfor c in [1,2,6]:\n    app = create_app(cfg)\n    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n        report = await run_load(client,n=24,concurrency=c,use_cache=False,warmup=2)\n    reports.append({'concurrency':c,**report})\nassert all(r['summary']['n']==24 for r in reports)\ndisplay([{'c':r['concurrency'],**r['summary']} for r in reports])",
        ),
        (
            "성공과 거절",
            "동시 요청 수가 처리 용량보다 크면 503이 늘 수 있습니다. 낮은 지연을 개선으로만 읽지 않습니다.",
            "assert reports[0]['summary']['success'] == 24\nassert reports[1]['summary']['success'] == 24\nassert reports[2]['summary']['error_rate'] > 0\ndisplay([{'c':r['concurrency'],'errors':r['summary']['status_counts'],'goodput':r['summary']['successful_rps']} for r in reports])",
        ),
        (
            "분위수의 의미",
            "수식용 합성 데이터로 계산을 확인합니다. 24개 요청의 p99를 안정된 운영 지표로 보지 않습니다.",
            "sample = [10,10,10,10,100]\nassert np.percentile(sample,50) == 10\nassert np.percentile(sample,95) > 80\ndisplay({'mean':np.mean(sample),'p50':np.percentile(sample,50),'p95':np.percentile(sample,95),'method':'linear interpolation'})",
        ),
        (
            "실패를 섞은 착시",
            "빠른 거절이 전체 평균을 낮춥니다. 성공 지연 분포와 실패율을 함께 보고합니다.",
            "rows = [{'status':200,'elapsed_ms':100}]+[{'status':503,'elapsed_ms':1} for _ in range(9)]\ns = summarize(rows,1)\nassert s['error_rate'] == .9 and s['success_latency_ms']['p50'] == 100\ndisplay({'all_mean':np.mean([r['elapsed_ms'] for r in rows]),**s})",
        ),
        (
            "캐시 적중 부하의 분리",
            "같은 질문을 먼저 캐시한 뒤 비교합니다. 모델을 호출하지 않은 결과를 모델 추론 속도라고 쓰지 않습니다.",
            "app = create_app(cfg)\nasync with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n    cached = await run_load(client,n=24,concurrency=2,use_cache=True,warmup=2)\nassert app.state.service.provider_calls == 1\ndisplay(cached['summary'])",
        ),
        (
            "실험 한계",
            "폐쇄형 부하에서는 응답이 느려지면 다음 요청 유입도 줄어듭니다. 고정 도착률 시험과 구분합니다.",
            "limitations = ['ASGI 직접 호출: 실제 네트워크 제외','고정 수면: GPU·토큰 생성 제외','동시성 한도: 8, 요청 최대100','폐쇄형 부하: 도착률 고정 아님','표본24: 장시간 SLO 보장 아님']\ndisplay(limitations)",
        ),
        (
            "실제 제공자 어댑터 검사",
            "외부 모델 없이 HTTPX MockTransport로 연결·모델명 오류를 확인합니다. 다음 셀은 실제 Ollama를 호출하지 않습니다.",
            "def upstream(request):\n    if request.url.path == '/api/tags': return httpx.Response(200,json={'models':[]})\n    return httpx.Response(404,json={'error':'synthetic missing model'})\napp = create_app(Settings(provider='ollama',model='not-installed'),transport=httpx.MockTransport(upstream))\nasync with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://lab') as client:\n    ready = await client.get('/ready')\n    missing = await client.post('/api/v1/chat',json={'message':'x'})\nassert ready.status_code == 503 and missing.json()['error']['code'] == 'model_not_found'\ndisplay(missing.json())",
        ),
        (
            "성공 조건과 실패 처리",
            "요구사항을 API·시험·실패 동작에 연결합니다. 목표 시간은 제안값이지 측정 성과가 아닙니다.",
            "requirements = [{'id':'FR01','endpoint':'POST /api/v1/chat','test':'정상·공백·필드 오류','fallback':'입력 수정 안내'}, {'id':'FR02','endpoint':'/api/v1/chat/stream','test':'done·error·중단','fallback':'미완료 표시'}, {'id':'NFR01','endpoint':'부하 실험','test':'성공 p95+오류율+성공 처리량','fallback':'요청 제한·용량 조정'}]\nassert all(r['test'] and r['fallback'] for r in requirements)\ndisplay(requirements)",
        ),
        (
            "실험 근거 저장",
            "숫자는 실행 환경마다 달라집니다. 표본 수·정의·조건과 함께 저장합니다.",
            "report = {'scope':'local ASGI mock; not LLM or network benchmark','settings':{'delay_s':.03,'capacity':2,'requests':24,'cache':False},'runs':reports,'cached':cached,'requirements':requirements,'limitations':limitations}\n(OUT/'benchmark-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')\nprint(OUT/'benchmark-report.json')",
        ),
        (
            "기획서 이후의 작업",
            "새 기획서 제출을 반복하지 않고 최소 기능·실패 복구·실험 증거를 구현 포트폴리오에 누적합니다.",
            "next_step = {'service':'API로 제공할 최소 기능 1개','proof':'성공·입력 오류·시간 초과·취소','decision':'유지/수정/보류와 근거','next_week':'배포 구조·관찰·복구'}\ndisplay(next_step)",
        ),
    ],
)
