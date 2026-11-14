"""Render the rehearsal guide against actual Notebook cell positions."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LAB=ROOT/'week12/lab'
NOTES=json.loads((LAB/'instructor-notes.json').read_text())
guide=json.loads((LAB/'notebook-guide.json').read_text())
BASE='https://smilesjcha.github.io/llmops-16week/'
text=f'''# 12주차 VS Code 리허설 · 코드 셀별 설명

[강의안]({BASE}week12/lecture/) · [브라우저에서 셀별 교수 설명]({BASE}week12/lecture/instructor/#cells) · [과제]({BASE}week12/assignment/) · [환경 준비](README.md)

**실행 순서: 01 → 02 → 03 → 04 → 05.** 각 Notebook 안에서는 위에서 아래로 실행합니다. 번호는 **코드 셀의 순서**이며 VS Code 왼쪽의 실행 횟수 `[1]`, `[2]`와 다릅니다. 아래 전체 셀 위치는 Markdown을 포함해 위에서부터 센 번호입니다.

## VS Code 사전 준비

1. 저장소 폴더 전체를 열고 기존 Python 3.11 `.venv`를 사용합니다. `git pull --ff-only`로 갱신하며 개인 수정과 충돌하면 강제로 덮어쓰지 않습니다.
2. 터미널에서 `source .venv/bin/activate`, `python -m pip install -r requirements/week12-online.txt`, `python -m pip check`를 실행합니다.
3. Notebook 오른쪽 위 **Select Kernel → 저장소 .venv / Python 3.11**을 선택합니다. 각 코드 셀의 실행 버튼 또는 `Shift+Enter`를 사용합니다.
4. 01–04는 Ollama·Docker·브라우저 서버 없이 실행합니다. 02는 실제 FastAPI 라우트를 프로세스 안에서 호출하는 TestClient입니다.
5. 05를 위해 Ollama를 실행하고 `ollama pull qwen2.5:1.5b-instruct`로 미리 모델을 준비합니다. 이미 설치했다면 다시 받을 필요 없습니다.

Windows의 환경 활성화와 최초 설치는 [실습 README](README.md#vs-code-준비)를 따릅니다. 첫 코드 셀의 Python 버전과 설정 해시부터 확인합니다. `assert` 셀은 출력이 없어도 예외 없이 끝나면 통과입니다.

## 10·11·12주차에서 달라지는 질문

| 주차 | 검증 단위 | 핵심 질문 | 대표 증거 |
|---|---|---|---|
| 10 | 요청·실행 구간 | 서비스가 정상 처리되고 복구되는가? | 로그·Span·지표·복구 요청 |
| 11 | 같은 고정 질문의 답변 | 답변이 근거와 품질 기준을 만족하는가? | 문항별 실패·회귀 평가·Langfuse A/B/C |
| 12 | 무작위 배정 사용자 | 변경이 사용자 결과를 개선하는가? | 배정·누락·분모·효과 구간·운영 위험 |

**11주차 A/B/C는 같은 질문에 여러 버전을 실행하는 오프라인 비교입니다. 12주차 A/B는 사용자별 버전을 고정하고 집단 간 행동 결과를 비교하는 설계입니다.** 같은 이름의 HOLD·REVIEW가 나와도 판단에 사용하는 근거가 다릅니다.

## 100분 수업의 실습 구간

| 파일 | 연결 장표 | 실습 시간 | 수업 중 실행 |
|---|---|---:|---|
| 01 | 21쪽 | 8분 | 코드 셀 1–7 |
| 02 | 30쪽 | 12분 | 코드 셀 1–8, 6에서 과제용 화면 캡처 |
| 03 | 38쪽 | 9분 | 코드 셀 1–7 |
| 04 | 50쪽 | 12분 | 코드 셀 1–6, 9 / 7–8은 교수 시연·복습 |
| 05 | 55쪽 | 발췌 6분 | 모델 사전 준비, 생성 원문·종료 이유·보고서 확인 |

본인 리허설에서는 모든 셀을 실행하세요. 모델 다운로드·설치 시간은 위 실습 시간에 포함하지 않습니다.

'''
all_cells=[]
for b in guide:
 key=b['file'][:2];notes=NOTES['books'][key];nb=json.loads((LAB/'notebooks'/b['file']).read_text())
 code=[(i+1,''.join(c['source']).splitlines()[0])for i,c in enumerate(nb['cells']) if c['cell_type']=='code']
 assert len(code)==b['code_cells']==len(notes['cells'])+1
 text+=f"## {b['title']}\n\n[{b['file']}](notebooks/{b['file']})\n\n{notes['summary']}\n\n**재실행:** {notes['rerun']}\n\n"
 text+='| 코드 셀 | 전체 셀 위치·첫 코드 | 실행 후 확인 |\n|---:|---|---|\n'
 items=[{'code_cell':1,'title':'환경 준비','question':'터미널과 같은 Python 환경인가요?'}]+b['steps']
 for item,(position,first) in zip(items,code):
  i=item['code_cell'];note=NOTES['common_setup'] if i==1 else notes['cells'][str(i)]
  text+=f"| {i} | {position}번째 · `{first}` | {note['expected']} |\n"
  all_cells.append({'book':key,'code_cell':i,'position':position,'first_line':first,'title':item['title'],**note,'question':item['question']})
 text+='\n'
 for cell in [c for c in all_cells if c['book']==key]:
  text+=f"### 코드 셀 {cell['code_cell']} · {cell['title']}\n\n**화면에서 볼 곳:** {cell['point']}\n\n**학생에게 설명:** {cell['talk']}\n\n**확인 질문:** {cell['question']}\n\n"
text+='''## 화면과 산출물 마무리

- 02번 코드 셀 6에서 요청 ID·배정·제공 버전이 보이는 표를 캡처합니다. 셀 8 이후에는 임시 DB가 정리됩니다.
- 04번 코드 셀 9는 `week12/lab/reports/my-slow-result.json`을 저장합니다. 화면에 나온 판단 예시를 그대로 복사하기보다 자신의 근거·다음 변경을 적습니다.
- 05번 코드 셀 5는 실제 호출 결과가 있을 때만 `my-ollama-responses.json`을 저장합니다. 두 응답이 모두 있는지 확인합니다.
- 05번 코드 셀 6은 `report.html`을 만듭니다. macOS 터미널에서 `open week12/lab/reports/report.html`을 실행하거나 VS Code 탐색기에서 파일을 운영체제 탐색기에 표시해 브라우저로 엽니다.
- 보고서는 `slow` → 사용자 수 → 차이·구간 → B p95 → HOLD 이유 순서로 읽습니다. `healthy`는 REVIEW, `srm`은 INVALID이며 효과 해석을 멈춥니다.

브라우저 서비스 시연은 별도로 `python -m uvicorn week12.lab.service:app --host 127.0.0.1 --port 8012`를 실행합니다. Notebook 임시 DB·로컬 웹 요청·합성 CSV 보고서는 서로 다른 데이터입니다. [화면별 시연 순서](README.md#화면으로-시연하는-순서)를 확인하세요.

## 학생에게 마지막으로 남길 문장

“로그는 요청을 설명하고, 평가 데이터는 답변을 검증하고, 사용자 실험은 변경의 효과를 비교합니다. 성공 수치 하나보다 **대상·분모·불확실성·운영 위험**을 함께 설명하는 것이 이번 주 목표입니다.”
'''
(LAB/'WALKTHROUGH.md').write_text(text)
(LAB/'cell-teaching-guide.json').write_text(json.dumps(all_cells,ensure_ascii=False,indent=2)+'\n')
print('Rendered',len(all_cells),'code-cell notes')
