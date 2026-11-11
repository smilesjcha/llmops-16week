"""Teaching sequence: architecture, evidence, real generation, traces and decisions."""
import html
import hashlib
import json


def diagram(nodes, paths, caption, height=440):
    """Editable SVG, explicit edges, text fallback for small screens."""
    escape=html.escape
    marker='arrow-'+hashlib.sha256(caption.encode()).hexdigest()[:12]
    svg=f'<svg class="architecture" role="img" aria-label="{escape(caption)}" viewBox="0 0 1200 {height}"><defs><marker id="{marker}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z"/></marker></defs>'
    for d,label,x,y in paths:
        svg+=f'<path class="edge" d="{d}" marker-end="url(#{marker})"/>'
        if label:svg+=f'<text class="edge-label" x="{x}" y="{y}" text-anchor="middle">{escape(label)}</text>'
    for x,y,w,hh,title,sub,tone in nodes:
        shape=(f'<polygon points="{x+w/2},{y} {x+w},{y+hh/2} {x+w/2},{y+hh} {x},{y+hh/2}"/>' if 'decision' in tone else f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="4"/>')
        svg+=f'<g class="node {tone}">{shape}<text x="{x+w/2}" y="{y+hh/2-5}" text-anchor="middle">{escape(title)}</text><text class="node-sub" x="{x+w/2}" y="{y+hh/2+27}" text-anchor="middle">{escape(sub)}</text></g>'
    svg+='</svg>'
    fallback='<div class="architecture-text">'+''.join(f'<p><strong>{escape(t)}</strong>: {escape(s)}</p>' for _,_,_,_,t,s,_ in nodes)+'</div>'
    return svg+fallback+f'<p class="label">{caption}</p>'


def refine(old, helpers, result):
    para,two,rows,table,flow,code,img,metric=[helpers[k] for k in ['para','two','rows','table','flow','code','img','metric']]
    h=html.escape
    out=[]
    chapter='수업 안내'
    def emit(title,sub,body,notes,source=None,kind='architecture',dark=False):
        out.append(dict(title=title,sub=sub,body=body,notes=notes,chapter=chapter,source=source,kind=kind,dark=dark))
    def keep(n,**changes):
        item=old[n-1].copy();item.update(chapter=chapter,**changes);out.append(item)
    def lablink(n):
        return f'<a href="https://github.com/smilesjcha/llmops-16week/blob/main/week11/lab/WALKTHROUGH.md">실습 {n} 실행 순서·확인 결과</a>'
    S=helpers['SOURCES']
    S.update({
        'mlflow':('MLflow / Evaluation 구성','https://mlflow.org/docs/latest/genai/eval-monitor/'),
        'workflow':('MLflow / Evaluation-driven development','https://mlflow.org/docs/latest/genai/datasets/end-to-end-workflow/'),
        'langsmith':('LangSmith / Evaluation concepts','https://docs.langchain.com/langsmith/evaluation-concepts'),
        'langfuse':('Langfuse / Tracing overview','https://langfuse.com/docs/observability/overview'),
        'lf-eval':('Langfuse / Evaluation overview','https://langfuse.com/docs/evaluation/overview'),
        'otel':('OpenTelemetry / Traces','https://opentelemetry.io/docs/concepts/signals/traces/'),
        'ollama':('Ollama / Chat API','https://docs.ollama.com/api/chat'),
        'qwen':('Ollama / Qwen2.5 1.5B Instruct','https://ollama.com/library/qwen2.5:1.5b-instruct'),
    })
    live=json.loads((helpers['ROOT']/'week11/lab/sample/ollama/ollama-results.json').read_text())
    # 01–06: One map for the entire class, before details.
    keep(1,sub='11주차 / 2026.11.13',body=two('<p class="statement">평가 기준과<br>실제 응답의 검증</p><p class="subtitle">차성재<br>무신사 Core AI PM × AI 대학원 겸임교수</p>',rows([('판단','이 변경을 배포해도 되는가'),('실행','검색·생성·평가·추적'),('결과','실패 근거와 다음 개선')])),notes='오늘은 검색 점수부터 실제 LLM 답변, 평가자의 오판, 실행 기록까지 확인한다. 특정 도구 이름이 목적이 아니라 변경을 검증하는 흐름이 목적이다. Core AI PM은 핵심 인공지능 제품 관리 역할이다.')
    keep(4)
    emit('100분 수업의 진행','개념 설명과 핵심 셀 실행의 반복',table(['시간','핵심 질문','Notebook'],[
        ['0–15분','어디에서 무엇을 평가할까','01 핵심 셀'],['15–35분','검색 개선은 어떻게 비교할까','02–04 핵심 셀'],['35–60분','실제 모델은 근거대로 답할까','07 실제 생성'],['60–80분','평가자와 실행 기록은 믿을 만한가','05 → 08 실제 평가'],['80–100분','어떤 근거로 배포를 결정할까','06 보고서·토론']]),'모든 셀을 동시에 설명하지 않는다. 03의 계산 심화는 필요한 경우만 열고, 07과 08은 반드시 실제로 실행한다. 수업 전 모델 다운로드를 마친다. 시간 부족 시 준비된 실제 실행 보고서를 보되 실시간 실행으로 소개하지 않는다.',kind='schedule')
    emit('LLM 서비스와 평가 지점','검색 증강 생성 / Retrieval-Augmented Generation',diagram([
        (20,20,240,90,'정책 원문','버전·접근 권한',''),(330,20,240,90,'검색 색인','문서·청크·메타데이터',''),
        (20,180,240,100,'사용자 질문','입력 검증',''),(330,180,240,100,'검색','근거와 순위','focus'),
        (640,180,240,100,'LLM 생성','근거·프롬프트','focus'),(950,180,230,100,'응답 처리','출처·기권·후속 안내',''),
        (330,350,550,80,'평가와 실행 기록','검색 지표 / 답변 판정 / 지연·토큰','focus')],
        [('M260 65 H330','',0,0),('M450 110 V180','',0,0),('M260 230 H330','',0,0),('M570 230 H640','',0,0),('M880 230 H950','',0,0),('M450 280 V350','',0,0),('M760 280 V350','',0,0)],
        '자체 구성한 참조 아키텍처. 파랑 영역: 이번 실습에서 실행·검사하는 범위.'),
        '모든 서비스에 적용되는 단일 표준 도식은 없다. 공식 문서의 데이터·실행·평가 구조를 RAG 사례로 재구성했다. 검색 문서가 맞아도 생성 단계에서 조건을 빠뜨릴 수 있다. 운영에서는 권한, 비용, 안전 검사를 서비스 요구에 맞춰 추가한다.',source='langsmith')
    emit('배포 전 평가 아키텍처','같은 입력, 분리된 참고 기준, 두 버전의 비교',diagram([
        (10,165,230,105,'고정 평가 세트','질문 + 참고 기준',''),(330,30,240,100,'기준선 실행','현재 버전',''),(330,285,240,100,'후보 실행','변경한 버전','focus'),
        (680,165,230,105,'평가기','코드·모델·사람',''),(990,165,200,105,'검토 보고서','지표 + 실패 근거','')],
        [('M240 195 H285 V80 H330','질문',315,150),('M240 235 H285 V335 H330','',0,0),('M570 80 H625 V195 H680','실제 출력',700,135),('M570 335 H625 V235 H680','',0,0),('M910 215 H990','',0,0),('M125 270 V420 H795 V270','참고 기준',500,452)],
        '참고 정답은 평가기에만 전달. 생성 모델 입력에 정답을 섞지 않는 구조.',height=480),
        'MLflow는 dataset, predict function, scorers로 평가 실행을 설명한다. LangSmith도 example의 reference outputs를 애플리케이션에 전달하지 않고 evaluator에서 사용한다. 실습 ollama_lab.py도 gold_ids와 reference를 생성 프롬프트에서 제외한다.',source='mlflow')
    emit('Trace와 Span의 역할','전체 요청과 내부 작업의 구분',two(code('Trace: 질문 한 건\n├─ retrieval: 검색 문서·점수\n├─ generation: 프롬프트·응답\n├─ code_checks: 형식·인용 검사\n└─ llm_judge: 판정·근거'),rows([('Trace','요청 전체의 연결 기록'),('Span','요청 안의 작업 한 단계'),('원인 추적','어느 단계에서 실패했는지 확인')])),
        'OpenTelemetry의 trace는 관련 span의 연결이다. 본 수업 JSON trace는 그 관계를 배우는 로컬 기록이며 OpenTelemetry 표준 전송 형식 자체는 아니다. 응답 지연만 보고 정답 여부를 알 수는 없다.',source='otel',kind='trace-tree')
    # 07–12: Dataset decisions, not an extended glossary.
    chapter='1 평가 기준'
    keep(12,title='서비스 사례와 성공 조건')
    keep(14,title='질문과 참고 기준의 구조')
    keep(13,title='문서 버전과 정답 근거')
    keep(17)
    keep(18,notes=old[17]['notes']+' Notebook01은 각 세트의 24문항·12의도와 그룹 교집합이 없음을 검증한다. 잘못된 split을 입력한 누수 차단 메시지는 의도한 실험 결과다.')
    keep(24,sub='01_dataset_contract.ipynb',body=two(code('문서 22개 = 현재 18 + 과거 4\n질문 48개 = dev 24 + test 24\n각 세트: 12개 의도'),rows([('실행','첫 환경 셀 → 1~5단계'),('확인','없는 문서와 그룹 누수 차단'),('기록','복수 근거 질문 Q03a')]))+para(lablink('01'),'label'))
    # 13–20: Metrics together with their blind spots.
    chapter='2 검색 비교'
    keep(28,sub="TF-IDF: Term Frequency–Inverse Document Frequency / 단어 빈도와 문서 희소성")
    keep(31,title='한 요소씩 바꾼 비교',sub='개발 세트(dev) / 기권 임계값 0')
    keep(16)
    keep(34,title='검색 개수와 지표의 변화',notes='정답은 A와 B다. k=3일 때 Recall=0.5, k=4일 때 Recall=1이다. 첫 정답 순위는 2이므로 MRR=0.5로 유지된다. 학생이 값을 바꾼 뒤 변화 이유를 말하도록 한다.')
    emit('MRR과 nDCG의 차이','첫 정답의 순위와 여러 근거의 순위',table(['지표','관찰 대상','예: [X, A, B], 정답 A·B'],[
        ['MRR','첫 정답 순위의 역수 평균','첫 정답 2위 → 0.5'],['nDCG','여러 관련 문서의 순위 할인','이진 관련도 기준 약 0.6934']])+para('MRR: Mean Reciprocal Rank<br>nDCG: normalized Discounted Cumulative Gain','label'),
        'Notebook03은 nDCG를 손계산하고 sklearn과 대조한다. 정답이 아예 없는 질문의 Recall은 None이고, 정답은 있지만 못 찾은 경우는 0이다. 여러 문서가 필요한 문제는 Hit만으로 완전성을 판단할 수 없다.',source='ndcg',kind='metric-comparison')
    keep(39)
    keep(40)
    emit('검색 실습의 확인 지점','02_retrieval_baselines / 03_metrics_and_k',table(['실행','확인할 결과','해석'],[
        ['02 / 기준선','D02·D20·D04 검색','폐기 문서 D20 포함'],['02 / 필터 비교','구버전 포함 비율 0%','문서 상태 필터의 효과'],['03 / 손계산','Hit=1, Recall=0.5','정답 2개 중 1개 검색'],['03 / k 비교','k=3과 5의 dev Recall 동일','검색 개수 증가의 한계']])+para(lablink('02–03'),'label'),
        '02는 빈 검색 []와 동점 정렬 A,B도 확인한다. 03은 None과 0, 중복 ID 차단을 확인한다. 시간 제약이 있으면 실습 안내에 있는 결과표로 대조하고 계산 심화는 복습으로 진행한다.',kind='lab')
    # 21–27: Error diagnosis with decisions, not just scores.
    chapter='3 실패 분석'
    emit('응답과 기권의 판단 흐름','정답 확률이 아닌 검색 점수의 임계값',diagram([
        (20,165,245,100,'검색 결과','최고 점수 s',''),(370,165,280,100,'수락 조건','s > 0 그리고 s ≥ τ','focus'),
        (850,35,310,100,'응답 시도','근거를 생성 모델에 전달',''),(850,295,310,100,'기권','확인 불가·추가 질문','')],
        [('M265 215 H370','',0,0),('M650 195 H750 V85 H850','충족',795,145),('M650 235 H750 V345 H850','미충족',795,295)],
        'τ: 기권 임계값. 이 규칙만으로 답변의 사실성이 보장되지는 않음.'),
        '01–06은 이 점수 기반 기권 정책을 평가한다. 07은 그 정책을 그대로 배포하지 않고, 같은 검색 결과를 LLM에 주었을 때의 생성과 프롬프트 기반 기권을 별도 실험한다. 따라서 두 실험의 수락률을 합쳐 비교하면 안 된다.')
    keep(44)
    keep(46,title='기권 정책 적용 후의 결과')
    keep(47)
    keep(48,body=two('<p class="quote">“검정 운동화 270 사이즈<br>현재 재고는?”</p>'+rows([('검색','교환 규정과 배송비'),('부족한 정보','실시간 재고'),('필요한 처리','기권 또는 재고 조회')]),img('lab-error-detail.png','Q24a의 실제 검색 결과. 그림 확대 가능.')),title='관련 문서와 답변 근거의 차이')
    keep(49,title='실패 원인과 다음 실험')
    keep(50,sub='04_calibration_and_error_analysis.ipynb',body=two(code('선택: char-current-k3-t0.3\nRecall: 56.25% → 81.25%\n필수 근거 확보: 56.25% → 50%'),rows([('확인','Q05b: 문서는 찾았지만 기권'),('원인','최고 점수 < 임계값 0.3'),('다음 실험','dev에서 위험과 사용성 비교')]))+para(lablink('04'),'label'))
    # 28–32: Real local generation.
    chapter='4 실제 LLM 응답'
    emit('빠른 로컬 모델의 실행 조건','Qwen2.5 1.5B Instruct / 실제 호출',two(code('ollama pull qwen2.5:1.5b-instruct\n\n# 앱이 실행 중이지 않을 때\nollama serve'),table(['설정','수업 기본값'],[['문맥 / 출력 상한','2,048 / 192 tokens'],['temperature / seed','0 / 11'],['모델 유지','10분'],['추론 출력','thinking 지원 시 비활성화']])),
        '모델은 최초 한 번 내려받는다. qwen2.5:1.5b-instruct는 completion 모델이다. thinking을 지원하는 다른 모델을 선택하면 think=False를 보낸다. 낮은 temperature라도 환경이 바뀌면 완전한 재현을 보장하지 않는다. API 키와 클라우드 계정은 필요 없다.',source='qwen',kind='setup')
    emit('실제 RAG 요청의 실행 순서','검색 결과를 입력으로 전달하고 응답을 검사하는 구조',flow([('검색','현재 문서 상위 3개'),('생성','질문 + 문서 + 지시'),('검사','JSON·인용·기권'),('기록','응답·지연·버전')])+para('정답 문장·gold_ids는 생성 입력에서 제외. 실제 요청은 로컬 Ollama에만 전송.','label'),
        'generate_one 함수를 열어 단계별 경계를 확인한다. 모델이 문서를 잘못 사용해도 코드 검사는 통과할 수 있으므로 실제 응답의 의미를 별도로 검토한다. 사용자 요청 자체를 실행 가능한 명령으로 취급하지 않는다.',source='ollama',kind='flow')
    q24=[r for r in live['rows'] if r['question_id']=='Q24a']
    emit('프롬프트 변경의 실제 결과','같은 재고 질문 / 같은 검색기 / 같은 instruct 모델',two(*['<h3>'+('기준 프롬프트' if r['prompt_version']=='baseline' else '근거 제한 프롬프트')+'</h3>'+para(h(r['answer']['answer']),'quote')+para('기권: '+str(r['answer']['abstain'])+' / 인용: '+h(', '.join(r['answer']['citations']) or '없음'),'subtitle') for r in q24])+para('확인 불가 문장뿐 아니라 abstain·인용 값의 일관성도 검사.','label'),
        '저장된 실제 호출 결과다. 응답이 개선되더라도 인용 일관성이 남아 있을 수 있다. 07의 현재 실행은 이 화면과 문장이 달라질 수 있다. 작은 시연 사례이며 프롬프트 개선의 일반화된 성능 향상을 증명하지 않는다.',kind='real-response')
    emit('기계적 검사와 의미 검토','형식 통과와 답변 정확성의 구분',table(['검사','자동 확인','사람이 추가로 볼 부분'],[
        ['JSON','필드·타입·빈 응답','표현이 질문에 적절한가'],['인용','검색된 문서 ID인지','주장을 실제로 뒷받침하는가'],['기권','참고 기준과 일치하는지','필요한 후속 안내가 있는가'],['완전성','필수 문서 인용 여부','기간·비용·조건을 모두 설명했는가']]),
        '검사 이름에 accuracy를 붙이지 않는다. 문서를 모두 인용했어도 답변 본문이 기간을 빠뜨릴 수 있다. generated citations에는 불필요한 ID가 들어갈 수 있으며 이를 자동 교정해 성공으로 꾸미지 않는다.',kind='checks')
    emit('실습 07: 실제 응답 비교','07_ollama_rag_generation.ipynb',rows([('실행','기준 응답 → 근거 제한 응답 → 경계 질문'),('확인','Q03a 기간·비용 / Q24a 재고 질문 기권'),('기록','실제 답변·인용·모델 로드·생성 시간')])+para(lablink('07'),'label'),
        '파일 하나에서 실제 생성 4회를 실행한다. 준비된 모델이 없으면 해결 방법을 표시하고 중단한다. 응답 텍스트를 특정 정답 문자열로 대체하지 않는다. 보고서 경로는 reports/ollama-report.html이다.',kind='lab')
    # 33–38: Judge limits before tools.
    chapter='5 답변 평가'
    keep(55)
    keep(57)
    keep(58,title='평가자 검증의 작은 기준 세트',sub='05번: 작성 예시 8개 / 계산 구조의 사전 확인')
    judged=[r for r in live['rows'] if r['question_id']=='Q24a' and r['prompt_version']=='baseline'][0]
    emit('작은 모델 평가자의 실제 판정','생성 모델과 같은 모델을 평가자로 사용한 사례',two('<h3>생성 답변</h3>'+para(h(judged['answer']['answer']),'quote'),'<h3>평가 모델의 판정</h3>'+para(h(judged['judge']['parsed']['verdict']),'quote')+para(h(judged['judge']['parsed']['reason']),'subtitle')),
        '실제 로컬 호출에서 생성과 평가가 같은 모델을 사용했다. 자기 평가가 독립적인 품질 보증은 아니다. 판정이 맞으면 이유를 검토하고, 틀리면 사람이 정의한 기준과 대조해 오류를 기록한다. 실습08은 J01,J02,J03,J05에 대한 실제 판정도 실행한다.',source='judge',kind='judge-example')
    keep(21,title='ARES: 평가자와 사람 검토의 결합',sub='연구의 평가 구조 / 이번 실습과 다른 구현',notes='ARES는 합성 데이터로 평가 모델을 학습하고 사람 주석을 활용한 예측 기반 추론으로 평가를 보정한다. 이번 실습은 ARES 구현이나 재현이 아니다. 여기서 배울 점은 자동 평가자 자체도 검증 대상이라는 역할 분리다.')
    emit('실습 08: 실제 평가와 추적','08_ollama_judge_and_traces.ipynb',rows([('평가자 점검','4개 기준 사례에 실제 모델 판정'),('서비스 응답','새로 생성한 Q03a 답변의 평가'),('추적','검색·생성·코드 검사·모델 판정 연결')])+para(lablink('08')+' / 05번 작성 예시와 actual 판정의 구분','label'),
        '08은 독립 실행이다. 4개 judge 호출, 실제 생성1회, 생성 답변 judge1회가 수행된다. 일치율이 낮아도 실행 실패가 아니다. actual 열은 fixture judge 값을 복사한 것이 아니라 실제 모델 출력이다.',kind='lab')
    # 39–43: Product cases mapped to this exact lab.
    chapter='6 LLMOps 도구'
    emit('필요한 기능과 선택 가능한 도구','Langfuse·LangSmith의 수업 내 역할',table(['서비스에 필요한 기능','도구 없이 시작','플랫폼 도입 시'],[
        ['요청 추적','로컬 JSONL·trace_id','요청 검색·단계별 탐색'],['반복 비교','같은 데이터의 두 실행','실험 이력·버전 비교'],['검토 기록','실패 사례·사람 판정','점수·검토 큐·팀 협업']]),
        '특정 제품 설치는 필수가 아니다. 하지만 이 세 기능을 아예 생략하면 품질 문제를 찾고 고치는 과정을 배우기 어렵다. 기존 자료의 누락을 보완하여 원리와 제품 사례를 연결한다. 무료 여부나 배포 선택의 세부 조건은 최신 제품 문서를 확인한다.',source='lf-eval',kind='tool-purpose')
    emit('Langfuse: 실패 요청의 원인 추적','공식 문서의 실제 UI 사례',two(img('langfuse-trace.png','공식 화면 일부 확대 / 전체 그림 확인 가능',True).replace('<img','<div class="product-crop"><img').replace('<figcaption','</div><figcaption'),rows([('작업 트리','어느 단계가 느리거나 실패했는가'),('입력·출력','실제로 무엇을 받아 반환했는가'),('검토·평가','점수와 검토 의견을 어디에 남기는가')]))+para('수업 계정의 실행 화면이 아닌 공식 문서 사례.','label'),
        '확대한 화면 왼쪽의 중첩 작업과 오른쪽의 입력·출력을 읽는다. 전체 그림에서는 요청 목록·Scores·Annotate 위치도 확인한다. 같은 역할을 08의 trace_id와 spans에서 찾는다. 이 그림은 공식 제품 예시로 수업의 지연 측정값이 아니다. 화면은 확대 버튼으로 확인할 수 있다.',source='langfuse',kind='product-screen')
    emit('LangSmith: 같은 질문의 실험 비교','Dataset example과 Experiment의 연결',diagram([
        (20,150,260,110,'Dataset example','입력 + 참고 출력',''),(380,30,250,110,'Experiment A','기준 프롬프트',''),(380,275,250,110,'Experiment B','근거 제한 프롬프트','focus'),
        (800,150,350,110,'비교와 검토','실제 출력·점수·실행 trace','')],
        [('M280 185 H330 V85 H380','',0,0),('M280 225 H330 V330 H380','',0,0),('M630 85 H710 V185 H800','',0,0),('M630 330 H710 V225 H800','',0,0)],
        '공식 문서의 개념을 수업 사례로 재구성. 제품 화면을 모사한 그림이 아님.'),
        '07의 baseline/grounded 두 실행을 같은 데이터의 두 experiment로 볼 수 있다. LangSmith에서는 평가 점수와 실제 출력, 하위 실행을 비교하고 검토 기록을 남긴다. 평가자가 참고 출력을 볼 수 있어도 애플리케이션 입력에 참고 정답을 섞지 않는다.',source='langsmith')
    emit('실습 기록과 제품 용어의 대응','기능의 역할로 읽는 도구 비교',table(['이번 실습','Langfuse','LangSmith'],[
        ['trace_id + spans','Trace / observations','Run trace / child runs'],['질문 + 참고 기준','Dataset item','Dataset example'],['프롬프트별 실행','Experiment','Experiment'],['검사·평가·검토','Scores / annotation','Feedback / annotation queue']]),
        '도구의 명칭이 달라도 질문과 실행, 평가 근거가 연결되는 구조는 같다. 플랫폼 계정 연동과 서버 배포는 이 수업의 필수 실습에 추가하지 않는다. 현재 JSONL은 어느 제품의 전송 규격도 아니며 SDK로 변환·전송해야 한다.',source='langsmith',kind='mapping')
    emit('운영 실패의 재평가 흐름','실제 요청을 다음 평가 세트로 연결하는 절차',flow([('운영 관찰','오류·낮은 평가·기권'),('검토','권한·비식별·기준 확인'),('평가 세트','대표 실패와 정상 사례'),('변경 검증','같은 입력으로 재실행')])+para('실패 사례만 모으면 사용 분포가 왜곡될 수 있음. 대표 사례와 위험 사례를 함께 관리.','label'),
        'Langfuse와 LangSmith 모두 운영 trace와 오프라인 평가를 연결한다. 원문 개인정보를 그대로 공개 저장소로 옮기지 않고 검토된 자료를 사용한다. 이 흐름은 12주차 온라인 평가로 이어진다.',source='workflow',kind='feedback-process')
    # 44–52: Release decision grounded in measurements.
    chapter='7 배포 판단'
    keep(64)
    keep(65)
    emit('품질 검증과 배포 승인','교육용 HOLD는 차단 / 통과 이후에도 검토',diagram([
        (10,155,240,110,'변경 버전','모델·검색·프롬프트',''),(350,135,280,150,'기준 충족?','사전 정의한 기준','decision focus'),
        (820,20,340,100,'보류·원인 분석','기준 미달 또는 불확실',''),(820,310,340,100,'사람 검토·제한 배포','운영 관찰·중단 조건','')],
        [('M250 210 H350','',0,0),('M630 210 H730 V70 H820','미충족',775,132),('M730 210 V360 H820','충족',775,300)],
        '검증 조건은 서비스 위험·비용에 맞게 정의. 점수 평균으로 필수 실패를 상쇄하지 않는 예시.'),
        '실습의 10%와 80%는 교육용 기준이며 보편적인 산업 표준 수치가 아니다. 파이프라인을 코드로 연결할 때 --enforce-gate는 HOLD에 종료 코드2를 반환한다. REVIEW라도 자동 배포 명령은 없다.',source='mlflow')
    keep(66,notes='이 화면은 실제 TF-IDF 평가 보고서다. Ollama 생성 보고서는 별도 파일이며 점수나 run_id를 혼합하지 않는다. 앞에서 원인을 살펴본 Q24a를 필터로 다시 찾는다.')
    keep(67,body=two(code('python -m week11.lab.run_eval\n\n# 실제 생성과 평가\npython -m week11.lab.ollama_lab \\\n  --limit 3 --judge'),rows([('06 / 검색 평가','report.html / HOLD'),('07–08 / 실제 LLM','ollama-report.html / 실제 응답'),('열기','VS Code 탐색기 → 브라우저')]))+para(lablink('06–08'),'label'),notes='기본 CLI의 HOLD는 정상 결과다. --enforce-gate 옵션만 종료 코드2로 차단한다. Ollama CLI는 모델의 의미 오류를 테스트 실패처럼 숨기지 않고 실제 출력과 판정을 저장한다. 두 보고서는 평가 범위가 다르다.')
    emit('실제 생성의 지연과 실행 기록','Ollama API 응답에서 가져온 토큰·소요 시간',table(['질문','프롬프트','응답 시간','출력 토큰'],[[r['question_id'],r['prompt_version'],f'{r["generation"]["latency_ms"]:,.0f} ms',r['generation']['output_tokens']] for r in live['rows'][:4]],True)+para('로컬 기기 관측값. 최초 모델 로드·동시 실행·질문 길이에 따라 달라짐.','label'),
        '이 수치는 현재 저장된 실제 실행 예시다. 다른 모델과의 속도 순위나 모든 학생 기기의 지연을 보장하지 않는다. 자신의 실습에서는 latency_ms와 load_ms, output_tokens를 함께 확인한다.',source='ollama',kind='real-timing')
    keep(70,title='프로젝트의 한 페이지 평가 기록',body=rows([('결론','채택·추가 검토·보류와 이유'),('조건','데이터·모델·검색·프롬프트 버전'),('근거','지표와 실제 실패 응답 2건'),('다음 행동','한 가지 변경과 재평가 계획')]))
    emit('학습 확인과 다음 단계','자신의 실행 결과를 근거로 설명할 세 가지',rows([('검색','근거를 찾았는데도 왜 잘못 답할 수 있는가'),('평가','평가자가 supported라 해도 무엇을 더 확인할까'),('운영','이번 실패를 다음 변경에서 어떻게 재검증할까')]),
        '07의 실제 답변 하나와 08의 판정을 골라 답하게 한다. 시험이나 새 과제 마감을 추가하는 공지가 아니다. 다음 주에는 온라인 관찰과 실험의 차이를 이어간다.',kind='questions')
    emit('실습 안내와 참고 자료','실행 순서, 공개 보고서, 공식 문서',two(rows([('실습 안내',lablink('01–08')),('실제 응답','<a href="https://smilesjcha.github.io/llmops-16week/week11/lab/sample/ollama/ollama-report.html">Ollama 실행 보고서</a>'),('검색 평가','<a href="https://smilesjcha.github.io/llmops-16week/week11/lab/sample/report.html">기준선·후보 비교 보고서</a>')]),table(['참고','핵심 관점'],[[f'<a href="{S[k][1]}">{name}</a>',purpose] for k,name,purpose in [('langfuse','Langfuse','실행 추적·평가'),('langsmith','LangSmith','데이터·실험 비교'),('mlflow','MLflow','평가 실행 구성'),('ares','ARES','평가자 검증'),('lost','Lost in the Middle','문맥 활용의 한계')]],True)),
        '모든 공식 도구를 설치해야 수료할 수 있는 과정이 아니다. 로컬 실습에서 구조를 이해한 뒤 팀의 협업·보관·운영 요구에 따라 도구를 선택한다. 링크의 제품 화면과 API는 확인일 이후 달라질 수 있다.',kind='references')
    assert len(out)==52,len(out)
    return out
