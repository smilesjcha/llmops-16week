"""Build a portable, source-attributed 64-page HTML lecture from actual lab results."""
from pathlib import Path
import sys, json, base64, html
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from week11.lab.evaluation import Config, load_data, evaluate, summarize
P=ROOT/"week11/lecture"
R=json.loads((ROOT/"week11/lab/sample/results.json").read_text())
docs,qs=load_data()
dev=[q for q in qs if q["split"]=="dev"]
B,C=R["summary"]["baseline"],R["summary"]["candidate"]
h=html.escape
pct=lambda x:f"{100*x:.1f}%"
slides=[]
SOURCES={
 "ragas":("Ragas / Es et al.","https://arxiv.org/html/2309.15217v2"),
 "ares":("ARES / Saad-Falcon et al., Fig. 1","https://arxiv.org/html/2311.09476v2"),
 "aresresults":("ARES / NQ context relevance, Fig. 2","https://arxiv.org/html/2311.09476v2"),
 "lost":("Lost in the Middle / Liu et al., 2023","https://arxiv.org/abs/2307.03172"),
 "judge":("Judging LLM-as-a-Judge / Zheng et al., 2023","https://arxiv.org/abs/2306.05685"),
 "tfidf":("scikit-learn 1.7 / TfidfVectorizer","https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html"),
 "ndcg":("scikit-learn 1.7 / ndcg_score","https://scikit-learn.org/1.7/modules/generated/sklearn.metrics.ndcg_score.html"),
 "leak":("scikit-learn / data leakage","https://scikit-learn.org/1.7/common_pitfalls.html#data-leakage"),
}
def para(x,cls=""):return f'<p class="{cls}">{x}</p>'
def two(a,b,cls=""):return f'<div class="two {cls}"><div>{a}</div><div>{b}</div></div>'
def rows(items):return '<div class="rows">'+''.join(f'<div class="row"><strong>{a}</strong><p>{b}</p></div>' for a,b in items)+'</div>'
def table(head,data,small=False):
 return ('<div class="small-table">' if small else '<div>')+'<table><thead><tr>'+''.join(f'<th scope="col">{x}</th>' for x in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{v}</td>' for v in row)+'</tr>' for row in data)+'</tbody></table></div>'
def flow(items):
 return '<div class="flow">'+ '<span class="connector" aria-hidden="true">›</span>'.join(f'<div class="step"><span class="number">{i+1}</span><strong>{a}</strong><p>{b}</p></div>' for i,(a,b) in enumerate(items))+'</div>'
def code(x):return '<pre><code>'+h(x)+'</code></pre>'
def img(name,caption,external=False):
 raw=(P/"assets"/name).read_bytes()
 return f'<figure class="{"external" if external else ""}"><img class="{"screenshot" if name.startswith("lab") else ""}" src="data:image/png;base64,{base64.b64encode(raw).decode()}" alt="{h(caption)}"><figcaption>{caption}</figcaption></figure>'
def metric(label,value,detail):return f'<div class="metric-box"><p>{label}</p><div class="big">{value}</div><p>{detail}</p></div>'
def add(title,sub,body,notes,chapter="평가 설계",source=None,kind="editorial",dark=False):
 slides.append(dict(title=title,sub=sub,body=body,notes=notes,chapter=chapter,source=source,kind=kind,dark=dark))
def section(title,statement,detail,chapter):
 add(title,"",f'<div class="body section-opening"><p class="statement">{statement}</p><p class="index-line">{detail}</p></div>',
     "앞 구간의 결과를 한 문장으로 연결하고 이번 구간에서 학생이 직접 확인할 산출물을 안내한다.",chapter,kind="section",dark=True)
def bars(labels,series,title):
 # Numeric values are taken from current lab execution; zero-to-one scale.
 width,height=1180,390;left=290;plot=730;top=25;row=78
 svg=f'<svg class="chart" role="img" aria-label="{h(title)}" viewBox="0 0 {width} {height}">'
 for j,t in enumerate([0,.25,.5,.75,1]):
  x=left+t*plot;svg+=f'<line class="axis" x1="{x}" y1="10" x2="{x}" y2="335"/><text x="{x}" y="375" text-anchor="middle">{t:.2f}</text>'
 for i,l in enumerate(labels):
  y=top+i*row
  svg+=f'<text x="0" y="{y+35}">{h(l)}</text>'
  for j,(name,vals) in enumerate(series):
   v=vals[i]; yy=y+j*29
   svg+=f'<rect class="{"baseline" if j==0 else "candidate"}" x="{left}" y="{yy}" width="{plot*v}" height="22"/><text x="{left+plot*v+12}" y="{yy+19}">{pct(v)}</text>'
 svg+='</svg>'
 return svg+'<div class="chart-values">'+table(["지표","기준선","후보"],[[l,pct(series[0][1][i]),pct(series[1][1][i])] for i,l in enumerate(labels)])+'</div>'+para("기준선: 회색 / 후보: 파랑. 가로축 0~1, 같은 test의 실제 검색 평가.", "label")
def linechart(points,keys,labels,title):
 svg=f'<svg class="chart" role="img" aria-label="{h(title)}" viewBox="0 0 1160 410">'
 for t in [0,.25,.5,.75,1]:
  y=340-t*290
  svg+=f'<line class="axis" x1="100" y1="{y}" x2="1020" y2="{y}"/><text x="60" y="{y+8}" text-anchor="end">{t:.2f}</text>'
 for i,p in enumerate(points):
  x=100+i*920/(len(points)-1);svg+=f'<text x="{x}" y="384" text-anchor="middle">{p["x"]}</text>'
 for j,key in enumerate(keys):
  coords=' '.join(f'{100+i*920/(len(points)-1)},{340-p[key]*290}' for i,p in enumerate(points))
  color='var(--blue)' if j==0 else 'var(--muted)'
  svg+=f'<polyline points="{coords}" stroke="{color}" stroke-width="4" fill="none"/>'
  for i,p in enumerate(points):
   svg+=f'<circle cx="{100+i*920/(len(points)-1)}" cy="{340-p[key]*290}" r="6" fill="{color}"/>'
 svg+='</svg>'
 return svg+'<div class="chart-values">'+table(["설정",*labels],[[p["x"],*[pct(p[k]) for k in keys]] for p in points])+'</div>'+para("파랑: "+labels[0]+" / 회색: "+labels[1]+" / 개발 세트(dev) 실측","label")

add("LLM 서비스의<br>품질 검증","11주차 오프라인 평가 체계",
    '<div class="bookend"><div>'+para("좋아 보이는 답변에서<br>검증 가능한 개선으로","statement")+para("2026.11.13<br>차성재 | 무신사 Core AI PM × AI 대학원 겸임교수","subtitle")+'</div><div class="cover-proof">'+para("오늘의 실험 결과")+f'<div class="big">{R["gate"]["decision"]}</div>'+para("검색 점수는 상승.<br>배포 판단은 보류.")+'</div></div>',
    "표지의 HOLD는 꾸민 수치가 아니라 이번 실습의 실제 결과다. 왜 검색 성능이 좋아졌는데도 배포를 보류하는지 수업 전체에서 설명한다. Core AI PM은 핵심 인공지능 제품 관리 역할이다.",
    kind="cover",dark=True)
add("하나의 점수로 부족한 판단","같은 test에서 관찰한 변화",
    '<div class="thirds">'+metric("검색 Recall@3",pct(B["recall"])+" → "+pct(C["recall"]),"필수 문서 중 검색한 비율")+metric("필수 근거 확보율",pct(B["evidence_complete"])+" → "+pct(C["evidence_complete"]),"기권 여부까지 반영")+metric("답변 불가 수락률",pct(B["false_accept"])+" → "+pct(C["false_accept"]),"문서에 없는 질문의 수락")+'</div>',
    "가상 정책 데이터의 실제 TF-IDF 실행이다. LLM 답변 생성 정확도가 아니다. 답변 가능한 test 16개, 답변 불가 8개를 서로 다른 분모로 사용한다. 어떤 수치를 보면 후보를 채택하고 싶은지 먼저 묻는다.",kind="metrics")
add("수업의 세 가지 산출물","정의, 비교, 판단을 연결하는 평가 기록",
    rows([("평가 데이터","질문·필수 근거·답변 가능 여부·의도 그룹·버전"),
          ("비교 결과","기준선과 후보의 지표, 유형별 실패, 질문별 검색 근거"),
          ("의사결정","채택·추가 검토·보류의 이유와 다음 실험")]),
    "오늘 목표는 도구 이름을 많이 외우는 것이 아니라 평가 결과로 한 번의 의사결정을 설명하는 것이다.",kind="ledger")
road=[("01","서비스 운영","09.04"),("02","프롬프트 설계","09.11"),("03","평가와 오류","09.18"),("04","검색 근거","09.25 녹화"),("05","검색 품질","10.02"),("06","휴일","10.09 수업 없음"),("07","모델 적응·기획","10.16"),("08","기획서 평가","제출 10.22"),("09","API 계약","10.30"),("10","배포와 관찰","11.06"),("11","오프라인 평가","11.13 현재"),("12","온라인 실험","11.20"),("13","안전과 거버넌스","11.27"),("14","비용과 지연","12.04"),("15","통합 검증","12.11"),("16","프로젝트 발표","12.18")]
add("16주 과정의 현재 위치","전 과정 온라인 운영 / 정규 수업은 실시간",
    '<div class="roadmap">'+''.join(f'<div class="{"current" if n=="11" else ""}"><strong>{n} {t}</strong><span>{d}</span></div>' for n,t,d in road)+'</div>',
    "6주차는 녹화영상과 신규 과제도 없었다. 8주차는 중간고사 없이 제출물 평가였으며 10월22일23:59 마감이었다. 16주차는 온라인 실시간 발표다. 오늘은 11주차 평가 데이터를 프로젝트 증거로 추가한다.",kind="roadmap")
add("100분 수업의 진행","설명과 실행을 짧게 번갈아 진행",
    table(["구간","핵심 내용","실행"],[["0–20분","평가 기준·데이터 분리","Notebook 01"],["20–42분","검색 기준선·지표","Notebook 02–03"],["42–63분","임계값·실패 분석","Notebook 04"],["63–80분","답변 평가·평가자 검증","Notebook 05"],["80–100분","보고서·배포 판단·질의응답","Notebook 06"]]),
    "76쪽 전체를 같은 속도로 읽지 않는다. 계산 심화와 참고 장표는 필요할 때 열고 핵심 셀 위주로 실행한다. 수업 전 requirements 설치를 완료하면 시간을 확보할 수 있다.",kind="schedule")
add("실행 관찰과 품질 평가","10주차의 실행 기록을 11주차의 비교 근거로 연결",
    two('<h3>실행 관찰</h3>'+rows([("Trace","요청이 어떤 단계를 거쳤는가"),("Metrics","오류·지연·처리량은 어떠한가")]),
        '<h3>품질 평가</h3>'+rows([("평가 세트","같은 문제에서 무엇이 달라졌는가"),("판단 기준","사용자에게 유용한 개선인가")])),
    "HTTP 200과 낮은 지연은 중요한 운영 신호지만 정답이라는 증거가 아니다. OpenTelemetry와 Prometheus는 오늘 품질 지표를 대신 채점하는 도구가 아니다.",kind="comparison")
add("오프라인 평가와 온라인 실험","고정 문제의 비교와 실제 사용 환경의 관찰",
    table(["구분","오프라인","온라인"],[["입력","버전이 고정된 평가 세트","실제 사용자의 요청"],["장점","같은 질문으로 반복 비교","실제 행동·분포 관찰"],["한계","표본이 사용 환경을 다 담지 못함","사용자 영향과 교란 요인"],["연결","배포 전 근거 확보","제한된 배포·모니터링·중단"]]),
    "오프라인을 통과하면 즉시 전체 사용자에게 배포하는 것이 아니다. 온라인에서 실패 범위를 제한하며 검증해야 한다.",kind="comparison")
add("평가 파이프라인의 구조","모든 결과를 입력과 버전까지 추적하는 설계",
    flow([("데이터 계약","질문과 필수 근거"),("고정 실행","검색·설정·버전"),("지표와 오류","평균과 개별 사례"),("판단 기록","근거와 다음 행동")]),
    "각 단계의 산출물이 다음 단계 입력이 된다. 좋은 보고서에도 데이터 출처나 버전이 없으면 재현이 어렵다.",kind="flow")
add("평가 단위의 결정","문서, 청크, 답변, 서비스 중 무엇을 판단하는가",
    table(["단위","예시 질문","혼동 위험"],[["문서/청크","필수 근거를 찾았는가","같은 원문의 중복 청크"],["답변","근거와 핵심 주장이 일치하는가","유창하지만 조건이 틀린 답"],["서비스","허용 위험과 사용성을 만족하는가","기권만 늘린 안전성"]]),
    "이번 검색 지표는 문서 ID 기준이다. 실제 프로젝트에서 청크를 사용하면 정답 단위와 중복 처리 규칙을 다시 정의한다.",kind="table")
add("평가 기준의 지도","품질은 한 축으로 정리되지 않는 서비스 속성",
    two('<p class="statement">검색 성공<br>답변 정확성<br>사용자 효용</p>',
        rows([("검색","관련 근거의 확보와 순위"),("생성","정확성·근거 충실성·질문 응답"),("운영","기권·지연·비용·안전")])),
    "같은 지표 이름도 입력과 분모가 다르면 비교할 수 없다. 이 수업의 검색 점수를 범용 LLM 성능으로 확대 해석하지 않는다.",kind="map")
section("평가 데이터","좋은 질문과<br>명확한 정답 기준","문서 버전 / 필수 근거 / 답변 불가 / 의도 그룹","데이터")
add("오늘의 서비스 사례","가상 쇼핑 정책 안내 서비스",
    two('<div class="well"><p class="quote">“사이즈가 작아요.<br>언제까지 바꿀 수 있고<br>비용은 얼마죠?”</p></div>',
        rows([("사용자 요구","교환 가능 기간과 배송비"),("필요 근거","D03 교환 정책 + D04 비용"),("실패 영향","일부 정보 누락 또는 잘못된 안내")])),
    "실제 무신사 정책이나 법률 안내가 아니다. 학습을 위해 만든 가상 쇼핑 정책임을 분명히 말한다. 사용자 질문은 한 문장이지만 필요한 근거는 여러 개일 수 있다.",chapter="데이터",kind="case")
add("정답처럼 보이는 구버전 문서","유사도와 유효성의 분리",
    table(["문서","내용","상태"],[["D01","수령 후 7일 이내 반품 접수","현재"],["D19","수령 후 14일 이내 반품 접수","폐기"],["D02","단순 변심 반품 배송비 3000원","현재"],["D20","단순 변심 반품 무료","폐기"]]),
    "잘못된 답이 반드시 모델 환각은 아니다. 잘못된 버전의 검색 근거에서 출발할 수 있다. status와 version을 색인 계약에 포함한다.",chapter="데이터",kind="table")
add("질문 한 건의 데이터 계약","정답 문장 하나보다 중요한 판단 정보",
    two(code('{\n  "id": "Q03a",\n  "group": "exchange",\n  "split": "test",\n  "gold_ids": ["D03", "D04"],\n  "answerable": true\n}'),
        rows([("질문","교환 가능 기간과 왕복 배송비"),("참고 기준","7일 이내, 재고 필요, 6000원"),("출처","교수 작성 합성 사례")])),
    "reference는 검토용이다. 검색기에 넣으면 정답을 입력으로 제공하는 오류다. gold 문서가 실제 존재하는지 자동 검증한다.",chapter="데이터",kind="code")
add("정답 근거의 판정","문장을 그대로 복사해야만 정답인 것은 아닌 평가",
    rows([("필수 사실","교환 신청은 수령 후 7일 이내"),
          ("필수 조건","재고가 없으면 반품 안내"),
          ("허용 표현","‘일주일 이내’처럼 같은 의미의 표현"),
          ("오류 표현","‘언제든 교환’처럼 조건을 확대하는 표현")]),
    "문자열 일치만으로 의미를 판정하면 같은 뜻의 답을 오답 처리하거나 조건이 다른 답을 통과시킬 수 있다.",chapter="데이터",kind="ledger")
add("복수 근거 질문의 성공 조건","정답 문서 두 개 중 한 개만 찾은 상황",
    two('<div class="stack"><div class="well"><h3>D03 교환 기간</h3><p>수령 후 7일 이내 / 재고 필요</p></div><div class="well"><h3>D04 교환 비용</h3><p>단순 변심 왕복 6000원</p></div></div>',
        '<p class="big">1 / 2</p><p class="subtitle">하나라도 찾으면 Hit는 1.<br>필수 문서 Recall은 0.5.</p>'),
    "초기 AS-IS 실습의 단일 정답에서는 Hit와 Recall이 같아 차이를 보기 어려웠다. 복수 근거로 지표의 의미를 구분한다.",chapter="데이터",kind="evidence")
add("답변할 수 없는 질문","문서에 없는 사실을 평가 데이터에 포함",
    table(["유형","예시","적절한 처리"],[["정책 범위 밖","해외 관세는 얼마인가요?","범위 안내·담당 채널 연결"],["실시간 상태","택배 기사님 현재 위치는?","조회 도구가 필요함을 안내"],["개별 상품 정보","내일 재입고 몇 시인가요?","확인 불가 또는 추가 조회"]]),
    "문서에 답이 없으면 검색기가 비슷한 문서를 찾아도 정답 근거가 아니다. 이 실습은 기권 정책만 검사하며 실제 외부 조회를 수행하지 않는다.",chapter="데이터",kind="taxonomy")
add("개발 세트와 평가 세트의 분리","문장보다 의도 그룹을 먼저 분리",
    two('<h3>개발 세트(dev)</h3>'+metric("12개 의도","24문항","검색 방식·k·임계값 선택"),
        '<h3>고정 평가 세트(test)</h3>'+metric("다른 12개 의도","24문항","선택한 설정의 결과 관찰")),
    "같은 의도의 정중한 질문과 구어체 질문은 같은 split에 둔다. 문서 집합은 공유하며, 새로운 도메인 적응 실험으로 주장하지 않는다.",chapter="데이터",source="leak",kind="partition")
add("누수의 대표적인 경로","좋아진 점수가 새 질문의 성능을 뜻하지 않는 상황",
    flow([("표현만 변경","같은 의도 두 문장"),("서로 다른 split","한 문장은 dev, 하나는 test"),("반복 조정","이미 본 규칙에 최적화")])+para("방지: 원문·의도·고객·시간 등 실제 의존 관계를 기준으로 그룹 분리.","subtitle"),
    "코드에서는 group이 dev/test에 동시에 나타나면 예외를 발생시킨다. 실제 운영은 사용자나 대화 단위 의존성도 확인해야 한다.",chapter="데이터",source="leak",kind="flow")
add("합성 평가 데이터의 제작 과정","생성과 검토를 분리한 데이터 준비",
    flow([("원문 선택","출처·버전·사용 권한"),("질문 후보","직접·구어체·복수 근거"),("검수","답변 가능성·모호성"),("분리와 고정","그룹·버전·변경 기록")]),
    "이번 사례는 교수 작성 합성 데이터다. LLM을 자동 호출해 생성한 데이터가 아니다. 실제 모델 생성으로 확장하더라도 검수 단계는 생략하지 않는다.",chapter="데이터",kind="process")
add("연구 사례: ARES의 평가 구조","합성 데이터, 평가 모델, 사람의 검토를 연결",
    img("ares-framework.png","ARES Figure 1. Saad-Falcon et al. CC BY 4.0. 원본 그림을 회색조로 표시.",True),
    "ARES는 합성 데이터를 활용해 평가 모델을 학습하고 사람 주석과 예측 기반 추론으로 시스템 평가를 보정한다. 우리 실습은 ARES를 실행한 재현이 아니다. 원본 연구의 역할 분리를 참고한다.",chapter="데이터",source="ares",kind="paper")
add("연구 구조와 수업 실습의 범위","비슷한 흐름과 서로 다른 구현",
    table(["구성","ARES 연구","오늘 실습"],[["데이터","LLM 합성 데이터 활용","교수 작성 합성 정책·질문"],["평가자","학습한 언어 모델 평가자","검색 지표 + 작성 예시"],["불확실성","Prediction-Powered Inference","의도 그룹 bootstrap"],["해석","연구 설정의 평가 결과","작은 학습용 실험"]]),
    "PPI는 Prediction-Powered Inference다. bootstrap을 PPI라고 부르지 않는다. 논문에 있는 방법과 우리가 직접 구현한 범위를 구분해 설명한다.",chapter="데이터",source="ares",kind="comparison")
add("합성 질문의 검수 기준","질문 수보다 먼저 확인할 항목",
    table(["검수 항목","통과 예","수정 예"],[["근거 존재","제주 추가 배송비는?","문서 없는 해외 관세 질문"],["전제의 정확성","반품 비용은?","모든 반품이 무료라는 전제"],["모호성","교환 기간과 비용은?","‘이거 되나요?’만 있는 질문"],["유형 분리","답변 불가로 명시","없는 답을 임의로 작성"]]),
    "문서 없는 질문을 모두 버릴 필요는 없다. 답변 불가 유형으로 정확하게 라벨링하면 중요한 위험 평가 데이터가 된다.",chapter="데이터",kind="rubric")
add("실습 01: 데이터 계약 검증","01_dataset_contract.ipynb",
    two(code('docs, questions = load_data()\nvalidate_data(docs, questions)\n\n# 의도 그룹이 섞인 경우\nbad[1]["split"] = "test"\nvalidate_data(docs, bad)'),
        rows([("실행","정상 데이터 확인 후 누수 예시"),("확인","예상된 ValueError 메시지"),("변경","새 질문 1개와 gold_ids 작성")])),
    "Notebook의 try/except가 예상 오류를 잡으므로 전체 실행이 멈추지 않는다. 코드를 고치기 전에 데이터 구조를 읽게 한다.",chapter="데이터",kind="lab")
add("데이터 검증의 결과물","문항 수와 독립적인 의도 수를 함께 기록",
    table(["구분","dev","test"],[["답변 가능","16문항","16문항"],["답변 불가","8문항","8문항"],["독립 의도","12개","12개"],["표현 방식","직접 질문 + 구어체","직접 질문 + 구어체"]]),
    "각 유형의 수가 작다. 특히 복수 근거 test는 한 의도 두 문항뿐이다. 표본 수를 숨기지 않는 습관이 중요하다.",chapter="데이터",kind="results")
section("검색 기준선과 지표","무엇을 찾았는가,<br>어떤 순위인가","단어·문자 검색 / 버전 필터 / Hit·Recall·MRR·nDCG","검색")
add("TF-IDF의 계산 관점","Term Frequency-Inverse Document Frequency / 빈도와 희소성",
    two('<p class="formula">문서 내 빈도 ×<br>문서 집합에서의 희소성</p>'+para("정규화된 문서 벡터와 질문 벡터의 내적으로 유사도 계산.","subtitle"),
        flow([("fit","문서 집합에서 특징·IDF 계산"),("transform","질문을 같은 특징 공간으로 변환")])),
    "scikit-learn은 smoothing과 sublinear_tf 같은 구체 설정을 제공한다. 이 수업은 sublinear_tf=True, L2 정규화다. 슬라이드 표현은 직관이고 정확한 구현은 evaluation.py를 읽는다.",chapter="검색",source="tfidf",kind="formula")
add("단어 검색과 문자 검색","한국어 표현 변화에 대한 서로 다른 반응",
    table(["항목","단어 1–2그램","문자 2–4그램"],[["특징","공백 중심 토큰과 조합","부분 문자열 조각"],["장점","설명하기 쉬운 기준선","띄어쓰기·어미 변화 일부 대응"],["한계","표현이 달라지면 누락","뜻이 달라도 문자열 중복"],["해석","둘 다 어휘 기반 검색","신경망 임베딩과 구분"]]),
    "문자 방식이 모든 질문에서 우월하다고 결론내리지 않는다. 예를 들어 의미가 비슷하지만 문자열이 다른 질문은 두 방식 모두 어렵다.",chapter="검색",source="tfidf",kind="comparison")
add("기준선으로서의 단순 검색","복잡한 검색 모델 도입 전 필요한 비교",
    rows([("어휘 검색","빠르고 해석 가능 / 용어 불일치에 취약"),
          ("신경망 임베딩","의미 유사성을 학습 / 모델·거리·인덱스 관리"),
          ("혼합 검색","상호 보완 가능 / 결합 설정과 비용 평가 필요")]),
    "4~5주차 검색 방법을 다시 길게 설명하는 대신 오늘은 비교 조건과 결과 해석에 집중한다. 실습은 의도적으로 단순한 기준선을 쓴다.",chapter="검색",kind="map")
add("버전 필터의 적용 위치","검색 후 주의 문구보다 앞선 유효 문서 선택",
    flow([("전체 문서","현재 18 + 과거 4"),("메타데이터 필터","status == current"),("색인","현재 문서만 fit"),("검색 결과","유효 문서 ID와 점수")]),
    "권한 필터도 비슷한 구조를 가질 수 있지만 여기서 실제 접근 제어를 구현한 것은 아니다. 버전 필터의 효과만 확인한다.",chapter="검색",kind="flow")
ablation=[(c.name,summarize(evaluate(docs,dev,c))) for c in [Config("word-all"),Config("word-current","word",True),Config("char-current","char",True)]]
add("변경 요소를 분리한 실험","개발 세트(dev)에서 실제 실행한 결과",
    table(["설정","Recall@3","구버전 포함","답변 불가 수락"],[[name,pct(s["recall"]),pct(s["archive_in_topk"]),pct(s["false_accept"])] for name,s in ablation]),
    "threshold=0인 상태에서 문서 필터와 analyzer를 한 요소씩 바꿨다. 정확한 실험 조건을 함께 말해야 수치의 원인을 설명할 수 있다.",chapter="검색",kind="ablation")
add("검색 결과의 세 가지 상태","빈 결과, 동점, 관련 문서 누락",
    rows([("점수 0","겹치는 특징 없음 / 문서 반환 제외"),
          ("같은 점수","문서 ID 순으로 결정적 정렬"),
          ("관련 문서 누락","오류 기록 후 검색·문서 원인 분석")]),
    "0점 문서를 억지로 k개 채우면 임의 순서의 문서가 정답과 우연히 겹쳐 지표를 부풀릴 수 있다. 코드는 점수가 양수인 결과만 반환한다.",chapter="검색",kind="ledger")
add("실습 02: 검색 결과의 원인 추적","02_retrieval_baselines.ipynb",
    two(code('retriever = Retriever(\n    docs,\n    Config("char-current", "char", True)\n)\nretriever.search("반품배송비")'),
        '<h3>변경할 입력</h3>'+rows([("띄어쓰기","반품 배송비 / 반품배송비"),("구어체","돌려보내면 택배비 얼마죠?"),("관찰","문서 ID·점수·원문 비교")])),
    "같은 질문의 표현만 바꿔 결과를 비교한다. 모델을 더 크게 바꾸기 전에 실패 원인을 설명하도록 유도한다.",chapter="검색",kind="lab")
rank='<div id="rank-demo">'+''.join(f'<div class="rank {"relevant" if x in ["A","B"] else ""}"><span>{i+1}</span><span class="rank-id">{x}</span><span>{"관련" if x in ["A","B"] else "무관"}</span></div>' for i,x in enumerate(["X","A","Y","B","Z"]))+'</div>'
add("검색 지표의 계산 실험","정답 문서 A·B / 순위 X, A, Y, B, Z",
    two(rank,'<label class="range-control">검색 개수 k <input id="metric-k" type="range" min="1" max="5" value="3"><output id="metric-k-label">3</output></label><p id="metric-live">Hit 1.00 / Recall 0.50 / MRR 0.50 / nDCG 0.39</p><p class="subtitle">k만 바꿔도 지표가 서로 다르게 반응합니다.</p>'),
    "HTML에서 슬라이더를 조작한다. 인쇄 PDF에는 기본 k=3 결과가 보인다. 학생에게 k=4일 때 Recall과 MRR 중 무엇이 바뀌는지 먼저 예측하게 한다.",chapter="검색",kind="interactive")
add("평균 역순위: MRR","Mean Reciprocal Rank / 첫 관련 문서의 위치",
    two('<p class="formula">1등 → 1<br>2등 → 1/2<br>3등 → 1/3<br>없음 → 0</p>',
        '<h3>관찰 대상</h3>'+para("사용자가 첫 유용한 근거를 얼마나 빨리 만나는가.","quote")+para("복수 근거를 모두 찾았는지는 별도 평가가 필요합니다.","subtitle")),
    "여기서는 k 안의 첫 정답만 계산하므로 MRR@k라고 표기한다. 여러 질문의 reciprocal rank를 평균낸다.",chapter="검색",kind="formula")
add("정규화 할인 누적 이득: nDCG","normalized Discounted Cumulative Gain / 순위별 관련도 누적",
    two(code('DCG@k = Σ relᵢ / log₂(i + 1)\nnDCG@k = DCG@k / IDCG@k\n\n실습: rel ∈ {0, 1}\nIDCG: 가능한 이상적 순위의 DCG'),
        rows([("할인","뒤에 있는 관련 문서의 기여 감소"),("정규화","이상적 순위 대비 0–1"),("조건","관련도 정의·k·동점 규칙 명시")])),
    "수식의 i는 1부터 시작한다. 실습 구현의 enumerate는 0부터 시작해서 log2(i+2)를 쓴다. 직접 계산과 sklearn ndcg_score 결과를 교차 검증한다.",chapter="검색",source="ndcg",kind="formula")
add("지표의 분모와 해석","답변 가능 질문과 답변 불가 질문의 분리",
    table(["지표","분모","의미"],[["Hit·Recall·MRR·nDCG","답변 가능한 질문","필수 문서 검색의 품질"],["답변 불가 수락률","답변 불가 질문","기권해야 할 질문을 수락한 비율"],["답변 가능 기권율","답변 가능한 질문","유용한 응답 기회를 놓친 비율"],["응답 시도 비율","전체 질문","검색 점수로 수락한 비율"]]),
    "답변 불가 문항의 Recall은 None이다. 0점으로 평균에 넣지 않는다. 수락은 실제 정답 생성이 아니라 검색 후 응답 시도 정책을 뜻한다.",chapter="검색",kind="denominators")
add("검색 성공과 응답 시도의 차이","순위 평가는 기권 정책 이전의 신호",
    flow([("검색 순위","관련 문서가 top-k 안에 있는가"),("기권 판단","최고 점수 ≥ 임계값인가"),("필수 근거 확보","수락 + 모든 gold 문서 확보")])+para("필수 근거 확보도 생성된 답변의 정확성을 보장하지 않습니다.","subtitle"),
    "오늘 서비스는 LLM 답변을 생성하지 않는다. evidence_complete는 검색 파이프라인의 진단 지표이며 생성 품질 점수로 바꾸어 말하지 않는다.",chapter="검색",kind="flow")
kp=[{"x":k,**summarize(evaluate(docs,dev,Config("k","char",True,k)))} for k in [1,2,3,5,10]]
add("검색 개수에 따른 지표 변화","문자 검색 / 현재 문서 / threshold=0 / dev",
    linechart(kp,["recall","ndcg"],["Recall@k","nDCG@k"],"검색 개수 k별 Recall과 nDCG"),
    "x축은 표시한 k의 이산 범주다. 점을 이은 선은 추세를 읽기 위한 안내다. LLM의 토큰 비용과 생성 정확성은 이 그래프에서 측정하지 않았다.",chapter="검색",kind="chart")
add("긴 문맥과 답변 품질의 관계","검색된 문서를 많이 넣는 것만으로 해결되지 않는 문제",
    ''.join('<div class="context-row"><strong>'+label+'</strong><div class="context-strip">'+''.join('<span class="'+('evidence' if j==pos else '')+'">'+('근거' if j==pos else '문서')+'</span>' for j in range(9))+'</div></div>' for label,pos in [('앞부분',0),('중간',4),('뒷부분',8)])+para("같은 근거도 위치·길이·모델에 따라 활용 결과가 달라질 수 있습니다.","subtitle"),
    "Lost in the Middle 연구는 당시 모델과 과업에서 관련 정보 위치에 따른 성능 변화를 관찰했다. 이 그림은 위치 조건을 설명한 재구성 도식이며 논문 성능 곡선을 복제한 것이 아니다. 최신 모든 모델에 같은 수치가 적용된다고 말하지 않는다.",chapter="검색",source="lost",kind="research-diagram")
add("실습 03: 손계산과 코드의 대조","03_metrics_and_k.ipynb",
    two(code('ranking_metrics(\n    ["X", "A", "B"],\n    gold=["A", "B"],\n    k=3\n)'),
        rows([("예측","Hit=1 / Recall=1 / MRR=0.5"),("검증","nDCG 손계산과 sklearn 비교"),("오류 실험","중복 ID / 정답 없는 질문")])),
    "모든 숫자를 외울 필요는 없다. 지표가 무엇을 보지 못하는지 설명할 수 있는지가 학습 기준이다.",chapter="검색",kind="lab")
section("기권과 오류 분석","좋아진 평균 뒤의<br>놓친 질문","임계값 선택 / 유형별 분석 / 실패 사례의 원인","오류 분석")
add("기권 임계값의 역할","응답 시도를 줄여 근거 없는 안내의 가능성을 관리",
    two('<p class="formula">최고 검색 점수 ≥ τ<br>그리고 점수 > 0</p>'+para("조건 충족 시 수락, 그렇지 않으면 기권.","subtitle"),
        rows([("낮은 τ","더 많이 응답 시도 / 무관한 질문 수락 위험"),("높은 τ","더 많이 기권 / 답할 수 있는 질문 누락")])),
    "유사도는 정답 확률이 아니다. 특정 숫자 하나를 다른 모델과 인덱스에 그대로 옮기면 안 된다.",chapter="오류 분석",kind="tradeoff")
tp=[{"x":t,**summarize(evaluate(docs,dev,Config("threshold","char",True,3,t)))} for t in [0,.15,.3,.45,.6]]
add("임계값과 사용성의 변화","문자 검색 / 현재 문서 / k=3 / dev",
    linechart(tp,["false_accept","missed_answer"],["답변 불가 수락률","답변 가능 기권율"],"임계값별 수락 오류와 기권 오류"),
    "x축 threshold를 올릴수록 두 오류가 어떻게 달라지는지 본다. 무조건 기권하면 false_accept는 낮아지지만 유용성을 잃는다.",chapter="오류 분석",kind="chart")
add("후보 선택의 기준과 순서","30개 설정을 dev에서 비교한 뒤 test 평가",
    two(code('후보 = 2개 analyzer\n     × 3개 k\n     × 5개 threshold\n\nutility = 근거 확보율\n        - 답변 불가 수락률\n        - 0.25 × 답변 가능 기권율'),
        '<div class="well"><h3>선택된 후보</h3>'+para(h(R["manifest"]["candidate"]["name"]),"quote")+para("교육용 목적함수와 동점 규칙을 사전 정의.","subtitle")+'</div>'),
    "후보는 모두 현재 문서만 색인한다. k는1,3,5이고 threshold는0,.15,.3,.45,.6이다. test를 입력하면 select_on_dev가 거부한다.",chapter="오류 분석",kind="selection")
add("고정 test의 실제 비교 결과","같은 24문항 / 검색 지표는 답변 가능 16문항 기준",
    bars(["Recall@3","필수 근거 확보율","답변 불가 수락률"],[("기준선",[B["recall"],B["evidence_complete"],B["false_accept"]]),("후보",[C["recall"],C["evidence_complete"],C["false_accept"]])],"기준선과 후보의 실제 평가"),
    "파랑이 항상 좋아야 하는 그래프가 아니다. 답변 불가 수락률은 낮을수록 좋다. 근거 확보율의 감소는 기권 정책과 연결된다.",chapter="오류 분석",kind="measured-chart")
by_style=[(style,summarize([r for r in R["rows"]["candidate"] if r["style"]==style])) for style in ["direct","conversational"]]
add("말투별로 달라지는 결과","후보 검색기의 test 유형별 관찰",
    table(["표현","문항 수","Recall@3","답변 가능 기권율"],[[{"direct":"직접 질문","conversational":"구어체"}[style],s["n"],pct(s["recall"]),pct(s["missed_answer"])] for style,s in by_style]),
    "각 말투에 답변 가능8개·불가4개가 있다. 적은 표본에서 말투 전체의 성능을 단정하지 말고 실패 질문을 골라 추가 데이터를 만들 단서로 쓴다.",chapter="오류 분석",kind="slice")
add("실패 사례의 검색 근거","HTML 보고서에서 직접 확인한 답변 불가 수락",
    two('<p class="quote">“검정 운동화 270 사이즈<br>현재 재고는?”</p>'+rows([("검색 근거","사이즈 교환·배송비 규정"),("실제 요구","개별 상품의 실시간 재고"),("판단","비슷한 문서가 있어도 기권 필요")]),img("lab-error-detail.png","실제 Q24a의 검색 결과. 원본 확대 지원.")),
    "기권해야 하는 질문을 수락한 사례다. 문서가 비슷해 보이는 것과 질문에 대한 답이 있다는 것을 구분한다. 보고서에서 근거 원문을 읽고 판단하도록 한다.",chapter="오류 분석",kind="screenshot")
add("오류 원인별 다음 행동","모든 문제를 프롬프트 수정으로 해결하지 않는 진단",
    table(["관찰","우선 확인","다음 실험"],[["필수 문서가 없음","문서 범위·수집·갱신","원문 보강 또는 기능 범위 축소"],["있는데 검색 실패","표현·색인·필터","검색 방식·동의어 비교"],["검색했으나 기권","임계값·점수 분포","dev에서 사용성·위험 재검토"],["잘못된 답 생성","조건·근거 활용","생성 평가·출력 검증"]]),
    "현재 기본 실습은 마지막 생성 오류를 실제로 측정하지 않는다. 생성 단계는 fixture와 선택 확장으로 다룬다.",chapter="오류 분석",kind="triage")
add("실습 04: 실패 질문의 재현","04_calibration_and_error_analysis.ipynb",
    two(code('selected, trials = select_on_dev(docs, dev)\nrows = evaluate(docs, test, selected)\n\nfailures = [r for r in rows\n  if r["error"] not in\n  ["evidence_complete", "correct_abstain"]]'),
        rows([("확인","질문 ID·gold_ids·검색 문서"),("분류","누락 / 기권 / 잘못된 수락"),("기록","원인 가설과 다음 실험 1개")])),
    "질문을 고친 뒤 기존 test 점수만 높이는 행위와 새 일반화 근거를 확보하는 행위의 차이를 설명한다.",chapter="오류 분석",kind="lab")
section("답변 평가와 평가자","채점 결과를<br>검증하는 기준","근거 충실성 / 판정 기준 / 불일치 / 편향","답변 평가")
add("검색 평가와 생성 평가의 분리","RAG: Retrieval-Augmented Generation / 검색 증강 생성",
    '<div class="thirds">'+metric("문맥 관련성","검색 근거","질문에 필요한 내용인가")+metric("근거 충실성","답변의 주장","제공 근거로 뒷받침되는가")+metric("답변 관련성","질문과 답","사용자가 물은 바에 답하는가")+'</div>',
    "Ragas는 서로 다른 평가 차원을 분리하는 참고 사례다. metric 이름과 계산법은 구현 버전마다 확인해야 한다. 오늘 검색 Recall을 Ragas faithfulness로 부르지 않는다.",chapter="답변 평가",source="ragas",kind="axes")
add("정확성과 근거 충실성의 차이","정답을 우연히 맞힌 답변도 근거가 없을 수 있는 사례",
    table(["제공 근거","답변","판정 관점"],[["기간만 있는 교환 정책","왕복 배송비 6000원","사실과 맞아도 제공 근거 부족"],["폐기된 무료 반품 정책","반품 무료","근거를 따라도 최신 규정과 충돌"],["현재 7일 반품 정책","7일 이내 가능","기간은 일치, 추가 조건 확인"]]),
    "근거 충실성만 높여도 데이터가 틀리면 사용자에게 잘못된 정보를 줄 수 있다. 반대로 외부 지식으로 맞힌 답은 근거 기반 서비스의 요구를 어길 수 있다.",chapter="답변 평가",kind="counterexample")
add("연구 사례: 평가 점수와 기준값","ARES의 Natural Questions(NQ) 문맥 관련성 비교",
    two(img("ares-context-results.png","ARES Figure 2. NQ 문맥 관련성. CC BY 4.0. 회색조 표시.",True),
        rows([("가로축","검색기와 생성 모델의 조합"),("세로축","문맥 관련성 정확도"),("비교","평가 점수·기준값·신뢰구간")])),
    "원 논문의 Figure2는 NQ에서 시스템 조합별 문맥 관련성 평가를 비교한 그래프다. ARES·RAGAS·기준값과 ARES 신뢰구간을 보여준다. 현재 최신 모델의 순위가 아니며 수업 실행 결과도 아니다. 회색조에서는 범례가 가까워 원문도 함께 확인한다. 평가자를 기준값과 비교해야 한다는 관점에 집중한다.",chapter="답변 평가",source="aresresults",kind="paper")
add("수업용 답변 판정 기준","판정 이유를 함께 남기는 세 가지 상태",
    table(["판정","기준","예"],[["supported","근거가 주장과 조건을 뒷받침","7일 규정에 7일 안내"],["unsupported","근거와 충돌하거나 주장이 과도함","7일을 30일로 확대"],["uncertain","필수 근거가 불완전하여 검토 필요","비용 문서 없이 비용 안내"]]),
    "이 세 범주는 수업용 루브릭이다. 연구 프레임워크의 공식 분류로 가장하지 않는다. 제공 자료가 불완전한 상황을 사람 검토로 보내는 예시다.",chapter="답변 평가",kind="rubric")
add("평가 요청과 결과의 계약","LLM-as-a-Judge / 언어 모델을 이용한 답변 평가",
    two(code('입력: question / evidence / answer\n기준: supported / unsupported / uncertain\n\n출력:\n{\n  "verdict": "supported",\n  "reason": "7일 조건과 일치"\n}'),
        rows([("자료와 지시","평가 대상 문서의 명령은 실행 금지"),("형식 검증","잘못된 JSON을 임의 점수로 변환 금지"),("내용 검토","유효 JSON과 올바른 판단은 별개")])),
    "기본 실습에서는 이 프롬프트를 만들 뿐 실제 LLM에 전송하지 않는다. 구분자만으로 prompt injection을 막을 수 있다고 말하지 않는다.",chapter="답변 평가",kind="contract")
add("빠른 규칙 검사의 한계","같은 숫자가 있어도 반대 의미가 되는 답변",
    two('<div class="stack"><div class="well"><p>“수령 후 7일 이내 반품 가능”</p></div><div class="well"><p>“수령 후 7일 이내에는 반품 불가”</p></div></div>',
        code('"7일" in answer\n\n두 답변 모두 True\n하지만 의미는 반대')),
    "규칙 기반 검증은 싸고 빠른 경보지만 의미 전체를 평가하지 못한다. 반대로 LLM 판정도 오류가 있으므로 서로 다른 검사를 조합한다.",chapter="답변 평가",kind="counterexample")
add("평가자와 참고 판정의 불일치","계산법 학습을 위한 작성 예시 8건",
    table(["참고 판정 / 예시 평가자","supported","unsupported","uncertain"],[["supported","3","1","0"],["unsupported","1","2","0"],["uncertain","1","0","0"]])+para("일치 5 / 8 = 62.5%. 실제 LLM 또는 인간 평가자 연구 결과가 아닙니다.","subtitle"),
    "행은 교수 작성 참고 판정, 열은 교수 작성 예시 평가자 출력이다. 조건 확대·근거 누락·다른 표기의 오판을 한 건씩 읽는다. 합성 예시 수치를 실측 모델 성능으로 발표하지 않는다.",chapter="답변 평가",kind="confusion")
add("위치 편향과 길이 편향","답의 내용 이외에 판정에 영향을 줄 수 있는 요소",
    two(flow([("A / B 제시","답변 1과 답변 2"),("B / A 제시","같은 내용을 순서만 교체")]),
        rows([("위치 편향","앞에 제시된 답을 선호하는 경향"),("길이 편향","장황한 답을 과대평가하는 경향"),("확인","슬롯이 아닌 의미상의 답 ID 비교")])),
    "MT-Bench 연구는 LLM 평가자의 위치·장황함·자기 선호 등의 한계를 분석했다. 모든 모델과 설정에서 같은 정도로 나타난다고 말하지 않는다.",chapter="답변 평가",source="judge",kind="bias")
add("실제 LLM 평가로 확장할 조건","기본 실습은 API 호출 없이 기준과 분석 방법에 집중",
    rows([("실행 정보","평가 모델·버전·프롬프트·온도·재시도"),
          ("비교 기준","독립 검토 사례·불일치 조정·순서 교체"),
          ("운영 기록","원응답·형식 실패·비용·실행 시간"),
          ("자료 관리","허용된 데이터만 전송·비공개 결과 보관")]),
    "LLM judge를 도입하면 결과를 정답으로 고정하지 말고 검증해야 한다. 평가자 모델을 바꾸면 같은 시스템의 점수가 바뀔 수 있다.",chapter="답변 평가",kind="manifest")
add("실습 05: 평가자 오류 읽기","05_judge_rubric.ipynb",
    two(code('a = agreement()\na["confusion"]\na["disagreement"]\n\nvalidate_judge_json(raw_response)'),
        rows([("실행","루브릭·형식 검증·불일치 표"),("관찰","조건 확대·근거 부족·표현 오판"),("확장","승인된 모델의 실제 결과와 비교")])),
    "fixture는 실제 LLM 응답이 아니라 작성 예시임을 다시 확인한다. 숫자를 높이는 것보다 어떤 오판이 위험한지 설명하게 한다.",chapter="답변 평가",kind="lab")
section("보고서와 의사결정","점수, 실패, 한계를<br>같이 남기는 판단","짝 비교 / 불확실성 / 검증 조건 / 프로젝트 기록","판단")
add("같은 질문의 짝 비교","후보와 기준선의 차이를 같은 평가 입력에서 계산",
    flow([("문항별 차이","후보 점수 − 기준선 점수"),("의도별 묶음","같은 의도 두 표현 유지"),("그룹 재표집","그룹을 복원 추출"),("구간 요약","차이 평균의 분포")]),
    "bootstrap은 관측 그룹을 다시 뽑는 계산이다. 새로운 실제 사용자 분포를 생성하는 것은 아니다. 여기서는 그룹 평균에 같은 가중치를 준다.",chapter="판단",kind="bootstrap")
ci=R["confidence"]
add("개선 폭의 불확실성","의도 그룹 bootstrap 2,000회 / seed=11",
    '<div class="thirds">'+metric("Recall 평균 차이",f'{ci["delta"]*100:.1f}%p',"후보 − 기준선")+metric("95% bootstrap 구간",f'{ci["low"]*100:.1f} ~ {ci["high"]*100:.1f}',"단위: %p")+metric("비교 가능한 그룹",str(ci["groups"]),"답변 가능한 의도 수")+'</div>',
    "작은 표본의 percentile bootstrap 구간이다. 0 포함 여부만으로 사업 의사결정을 끝내지 않는다. 데이터 대표성과 중요한 실패 유형도 검토한다. 이 결과는 ARES의 PPI가 아니다.",chapter="판단",kind="uncertainty")
checks=R["gate"]["checks"]
labels=["답변 불가 수락률 ≤ 10%","필수 근거 확보율 ≥ 80%","Recall 관측 하락 없음","Recall 차이 구간 하한 ≥ −5%p"]
add("배포 전 검증 조건의 결과","교육용 기준 / 실제 서비스는 위험과 비용에 맞게 재정의",
    table(["조건","측정","결과"],[[labels[0],pct(C["false_accept"]),"통과" if list(checks.values())[0] else "보류"],[labels[1],pct(C["evidence_complete"]),"통과" if list(checks.values())[1] else "보류"],[labels[2],f'{ci["delta"]*100:+.1f}%p',"통과" if list(checks.values())[2] else "보류"],[labels[3],f'{ci["low"]*100:.1f}%p',"통과" if list(checks.values())[3] else "보류"]]),
    "결론은 HOLD다. CI가 개선 방향을 지지하더라도 사용성과 답변 불가 질문 처리의 기준을 충족하지 못한다. 통과 수를 평균내어 실패 조건을 상쇄하지 않는다.",chapter="판단",kind="gate")
add("평가 보고서의 실제 화면","수치에서 질문별 근거로 이동하는 탐색",
    '<div class="report-shots">'+img("lab-report-metrics.png","실제 보고서의 핵심 지표. 답변 가능한 질문과 불가능한 질문의 분모 구분.")+img("lab-report-filters.png","질문 유형·실패 종류·검색어로 결과 탐색. 각 질문에서 문서 근거 확인.")+'</div>',
    "sample/report.html로 즉시 시연할 수 있고 Notebook06이나 CLI로 재생성할 수 있다. 보고서의 수치는 LLM 생성 정확도가 아니다.",chapter="판단",kind="screenshot")
add("실습 06: 보고서 재생성과 확인","06_release_report.ipynb",
    two(code('python -m week11.lab.run_eval\n\n# 생성 파일\nweek11/lab/reports/report.html\nweek11/lab/reports/results.json'),
        rows([("비교","같은 조건으로 실행 ID·결과 확인"),("탐색","실패 유형과 질문 필터"),("판단","실패 2건과 다음 실험 1개 기록")])),
    "VS Code 탐색기에서 report.html을 브라우저로 연다. 서버가 필요 없다. HTML은 결과 데이터가 내장되어 오프라인으로 열린다.",chapter="판단",kind="lab")
add("지속적 통합에서의 평가 연결","Continuous Integration / 변경마다 자동 검증",
    flow([("변경","데이터·검색·프롬프트"),("검증 실행","테스트 + 고정 평가"),("판단","HOLD면 차단"),("검토","근거와 실패 확인")])+code("python -m week11.lab.run_eval --enforce-gate"),
    "CLI는 HOLD일 때 종료 코드2를 반환한다. 설치 오류가 아니라 의도한 차단이다. 기본 명령은 학습을 위해 보고서를 만들고0으로 종료한다. REVIEW도 자동 배포를 의미하지 않는다.",chapter="판단",kind="ci")
add("프로젝트에 추가할 평가 근거","기획의 주장과 실제 실행 결과의 연결",
    table(["기획의 주장","필요한 증거","기록 예"],[["질문에 정확히 답함","대표 질문과 참고 기준","의도·근거·답변 불가 분리"],["기준선보다 개선","같은 입력의 비교","설정·실행 ID·차이·실패"],["운영 가능","위험과 중단 조건","기권·검토·롤백 기준"],["다음 개선","가장 큰 실패의 원인","한 요소 변경·새 평가"]]),
    "2pager·PRD·PPT에 모든 코드를 넣지 않는다. 주장과 근거, 선택 이유를 짧게 쓰고 상세 보고서를 연결한다. 여러 프로젝트도 각자의 검증 근거를 제시한다.",chapter="판단",kind="project")
add("한 페이지 평가 기록의 구조","복잡한 과정 설명보다 결과와 근거를 먼저 제시",
    rows([("결론","후보 보류 / 무엇이 기준을 충족하지 못했는가"),
          ("실험 조건","데이터·분리·기준선·후보·실행 ID"),
          ("주요 증거","핵심 지표·실패 2건·불확실성"),
          ("다음 행동","데이터 보강 또는 한 가지 기술 변경")]),
    "제안서의 두괄식 원칙을 평가 보고서에도 적용한다. 개선 과정의 일지를 길게 붙이지 않고 현재 판단을 먼저 설명한다.",chapter="판단",kind="document")
add("오프라인 통과 이후의 확인","사용 환경에서 확인할 추가 조건",
    table(["확인 영역","방법","중단 또는 재검토"],[["사용자 영향","제한된 배포·사람 검토","중요 오류·기권 급증"],["운영 품질","10주차 로그·trace·지표","지연·장애·비용 증가"],["분포 변화","새 질문 유형·문서 개정","평가 세트와 사용 환경 차이"]]),
    "오늘 기본 실습의 HOLD 후보를 실제 사용자에게 배포하라는 안내가 아니다. 일반적인 다음 검증 단계를 정리한다.",chapter="판단",kind="handoff")
add("다음 주차와의 연결","12주차 온라인 관찰과 실험",
    two('<p class="statement">고정 질문의 비교에서<br>실제 사용의 변화로</p>',
        rows([("오늘","평가 세트·실행 결과·오류 분석"),("다음 주","운영 지표·실험 설계·판단 기록"),("프로젝트","같은 버전 정보로 두 증거 연결")])),
    "11월20일은 현행 커리큘럼상 실시간 온라인 수업이다. 새 제출 일정이나 추가 배점은 이 자료에서 만들지 않는다.",chapter="정리",kind="transition")
add("학습 확인 질문","설명할 수 있는지 점검할 다섯 가지",
    rows([("지표","Hit와 Recall이 달라지는 사례는?"),("분리","같은 의도의 표현을 왜 묶는가?"),("기권","안전해졌는데 사용성은 왜 나빠지는가?"),("평가자","JSON 형식이 맞아도 왜 검토가 필요한가?"),("판단","어떤 실패 때문에 후보를 보류했는가?")]),
    "답을 외워 읽게 하기보다 자신의 실험 결과 한 건을 근거로 설명하게 한다. 수업 중 활동이며 새 별도 과제 마감은 없다.",chapter="정리",kind="questions")
add("논문과 공식 문서","개념과 구현을 구분해서 확인할 읽기 자료",
    table(["자료","핵심 관점"],[[f'<a href="{SOURCES[k][1]}">{SOURCES[k][0]}</a>',v] for k,v in [("ragas","검색·답변 평가 차원"),("ares","합성 데이터·평가자·사람 주석"),("lost","문맥 위치와 활용 한계"),("judge","평가자 편향과 검증"),("ndcg","순위 지표의 구현 정의")]],True),
    "수업 결과는 논문 재현이 아니다. 출처의 과업·모델·조건을 확인한 뒤 프로젝트에 적용한다. 링크는 원문 자료다.",chapter="참고",kind="references")
add("자료의 출처와 실행 범위","원본 그림, 재구성 도식, 실제 실행, 작성 예시의 구분",
    table(["표현","출처 또는 생성 방식","주의"],[["ARES 그림 2종","원 논문 / CC BY 4.0","회색조 표시·원문 링크"],["비교 차트·보고서","동봉 코드의 실제 TF-IDF 실행","가상 데이터 / LLM 생성 없음"],["평가자 판정 표","교수 작성 fixture","모델 성능 측정 아님"],["HTML 디자인","Impeccable·Hallmark 공식 지침 참고","강의용 페이지·인쇄에 맞춰 적용"]],True),
    "디자인 하네스는 검수 기준으로 활용했고 상표나 공식 제휴를 나타내지 않는다. 저작권과 라이선스는 assets/SOURCES.md에서 확인한다.",chapter="참고",kind="provenance")
add("실습 파일과 실행 순서","VS Code에서 01부터 06까지 / 각 파일 독립 실행",
    two(code('python -m pip install \\\n  -r requirements/week11-offline.txt\n\npython -m week11.lab.run_eval\npython -m pytest week11/lab/tests -q'),
        rows([("Notebook","week11/lab/notebooks/"),("즉시 볼 보고서","week11/lab/sample/report.html"),("실행 결과","week11/lab/reports/report.html")])),
    "HTML 강의안은 내려받아 브라우저로 연다. 방향키·목차·노트를 사용할 수 있고 인쇄 버튼으로 전체 PDF를 저장할 수 있다. 코드 실행은 Python3.11의 기존.venv에서 진행한다. 네트워크는 최초 패키지 설치에만 필요하다.",chapter="참고",kind="runbook")

from week11_refinement import refine
slides = refine(slides, globals(), R)
from week11_langfuse_slides import extend
slides = extend(slides, globals(), ROOT)
from week11_conference import enhance
slides = enhance(slides)
assert len(slides)==64, len(slides)
css=(P/"deck.css").read_text()
fonts="".join('@font-face{font-family:\"Course Pretendard\";font-weight:'+str(w)+';font-style:normal;font-display:swap;src:url(data:font/woff2;base64,'+base64.b64encode((P/"assets"/name).read_bytes()).decode()+') format(\"woff2\");}' for w,name in [(400,"Pretendard-Regular.woff2"),(700,"Pretendard-Bold.woff2")])
sections=[]
for i,s in enumerate(slides,1):
 src='<span>실습 코드·교수 작성 설명</span>'
 if s["source"]:
  label,url=SOURCES[s["source"]];src=f'<a href="{url}" target="_blank" rel="noopener">{h(label)}</a>'
 title_tag="h1" if i==1 else "h2"
 body=s["body"]
 if s["kind"]=="section":
  content=body
 else: content=f'<div class="body">{body}</div>'
 sections.append(f'<section class="slide {"dark" if s["dark"] else ""}" id="slide-{i}" data-kind="{s["kind"]}" data-chapter="{h(s["chapter"])}" aria-label="{i}페이지 {h(s["title"].replace("<br>"," "))}"><header><{title_tag}>{s["title"]}</{title_tag}>{para(s["sub"],"subtitle") if s["sub"] else ""}</header>{content}<footer><span class="source">{src}</span><span class="pageno">{s["chapter"]} / {i:02d}</span></footer><aside class="presenter-note">{h(s["notes"])}</aside></section>')
controls='''<dialog id="image-viewer" aria-labelledby="image-heading"><header><strong id="image-heading">그림 확대</strong><button id="image-close">닫기</button></header><button id="image-zoom" aria-pressed="false">원본 크기</button><div id="image-content" tabindex="0" aria-label="확대 이미지. 가로로 스크롤할 수 있습니다."></div><p id="image-caption"></p></dialog><nav id="chapter-nav" aria-label="학습 단계"></nav><nav class="controls" aria-label="프레젠테이션 조작"><button id="previous">이전</button><span id="status" role="status" aria-live="polite"></span><button id="next">다음</button><label id="jump-label" for="jump">페이지</label><input id="jump" type="number" min="1" max="64" value="1"><button id="overview-button" aria-controls="overview">목차</button><button id="notes-button" aria-expanded="false" aria-controls="notes-panel">설명 노트</button><button id="fullscreen">전체 화면</button><button id="print">인쇄 / PDF</button></nav><aside id="notes-panel"><strong>교수 설명 노트</strong><p id="notes-text"></p></aside><div id="overview" role="dialog" aria-modal="true" aria-labelledby="overview-heading"><header><h2 id="overview-heading">11주차 전체 목차</h2><button id="overview-close">목차 닫기</button></header><label class="overview-search-label" for="overview-search">장표 검색</label><input id="overview-search" type="search" placeholder="예: 기권, Langfuse, 실습" autocomplete="off"><p id="overview-empty" hidden>일치하는 장표가 없습니다. 다른 검색어를 입력하세요.</p><div class="overview-list"></div></div>'''
result='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="LLMOps 11주차 오프라인 평가 체계. 64쪽 HTML 강의안과 실제 Ollama 평가 실습."><title>11주차 | LLM 서비스의 품질 검증</title><style>'+css+fonts+'</style></head><body><main class="deck-shell">'+"\n".join(sections)+'</main>'+controls+'<script>'+(P/"deck.js").read_text()+'</script></body></html>'
result=result.replace("–","~")
(P/"index.html").write_text(result,encoding="utf-8")
(P/"lecture-notes.md").write_text("# 11주차 강의 노트\n\n"+"\n\n".join(f'## {i:02d}. {s["title"].replace("<br>"," ")}\n\n{s["notes"]}\n'+(f'\n출처: {SOURCES[s["source"]][1]}' if s["source"] else "") for i,s in enumerate(slides,1)))
(P/"slide-manifest.json").write_text(json.dumps([dict(page=i,**{k:v for k,v in s.items() if k!="body"}) for i,s in enumerate(slides,1)],ensure_ascii=False,indent=2))
print("Built",len(slides),"slides;",len(result.encode()),"bytes; run",R["run_id"])
