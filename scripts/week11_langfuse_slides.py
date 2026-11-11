"""Twelve practical slides: real Docker traces, experiment comparison and release gates."""
import json


def extend(slides, helpers, root):
    table,two,rows,para,code,img,flow=[helpers[k] for k in ['table','two','rows','para','code','img','flow']]
    from week11_refinement import diagram
    sources=helpers['SOURCES']
    sources.update({
        'lf-compose':('Langfuse / Docker Compose','https://langfuse.com/self-hosting/deployment/docker-compose'),
        'lf-sdk':('Langfuse / SDK instrumentation','https://langfuse.com/docs/observability/sdk/instrumentation'),
        'lf-scores':('Langfuse / Scores via SDK','https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk'),
        'lf-experiments':('Langfuse / Experiments via SDK','https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk'),
    })
    sample=json.loads((root/'week11/lab/sample/langfuse/results.json').read_text())
    url='https://github.com/smilesjcha/llmops-16week/blob/main/week11/lab/langfuse/README.md'
    extra=[]
    def emit(title,sub,body,notes,source=None,kind='platform-lab'):
        extra.append(dict(title=title,sub=sub,body=body,notes=notes,source=source,kind=kind,chapter='7 Langfuse 실습',dark=False))
    slides[2]['body']=table(['시간','핵심 활동','실습'],[
        ['0–10분','배포 상황·성공 조건·결과 예측','아키텍처'],['10–25분','평가 데이터·검색 지표','01–04 발췌'],
        ['25–40분','실제 생성·평가자의 오류','07–08 핵심 셀'],['40–60분','요청 트리·입출력·점수 확인','09 요청 추적'],
        ['60–85분','같은 데이터로 A/B/C 비교','10 실험·배포 조건'],['85–100분','사람 검토·결정 근거·다음 개선','결과 토론']])
    slides[2]['notes']='모델과 Docker 이미지는 수업 전에 준비한다. 기존 01–08의 모든 셀을 재실행하지 않는다. 오늘의 중심은 09의 실제 요청 추적과 10의 실험 비교다. 가설을 먼저 정하고 결과를 본 뒤 배포 결정을 설명한다. 설치 대기를 강의 시간에 포함하지 않는다.'
    emit('실습 미션: 새 버전의 배포 판단','가상 반품·교환 상담 AI / 금요일 오후의 변경 검토',
         two(para('“답변이 더 자연스러워졌으니<br>배포해도 괜찮을까?”','statement'),rows([
             ('미션 1','재고 오답의 실제 근거 추적'),('미션 2','같은 질문의 세 버전 비교'),('미션 3','보류·검토 결론과 개선 근거') ])),
         '답변을 보기 전에 어떤 버전이 재고 질문에 기권할지 학생들이 예측하게 한다. 글의 자연스러움보다 서비스의 제공 가능 기능과 검증 근거를 본다. 개인정보가 없는 합성 사례다.')
    emit('로컬 실습의 실행 구조','VS Code는 실행 / Ollama는 생성 / Langfuse는 기록',diagram([
        (20,150,260,110,'VS Code · Python','검색·생성 요청·평가','focus'),
        (400,20,280,100,'Ollama · :11434','호스트의 instruct 모델',''),
        (400,285,280,100,'Langfuse · :3011','Docker의 UI·API','focus'),
        (850,285,330,100,'저장과 비동기 처리','worker·DB·큐·객체 저장','')],
        [('M280 190 H335 V70 H400','모델 호출',330,145),('M280 230 H335 V335 H400','추적·점수',330,285),('M680 335 H850','',0,0)],
        'Ollama는 호스트에서 실행. 컨테이너 내부에서 Ollama를 호출하지 않는 구조.'),
        'Langfuse가 모델 응답을 생성하는 것이 아니다. Python이 Ollama를 호출하고 평가한 뒤 SDK가 기록을 보낸다. PostgreSQL은 설정, ClickHouse는 관찰·점수, Redis는 큐, MinIO는 이벤트 저장을 담당한다. 학생은 구성요소를 외우기보다 실행 경로와 실패 지점을 이해한다.',source='lf-compose')
    emit('Docker 준비와 시작 조건','수업 전 다운로드·기동 / 수업 중에는 실험',
         two(code('python -m pip install \\\n  -r requirements/week11-langfuse.txt\n\npython week11/lab/langfuse/init_env.py\n\ndocker compose \\\n  -f week11/lab/langfuse/compose.yaml \\\n  up -d --wait'),
             rows([('서버 / SDK','Langfuse 4.78.0 / Python SDK 5.2.0'),('화면','http://localhost:3011'),('로그인','로컬 .env의 EMAIL·PASSWORD'),('준비 완료','인증·모델 확인 + healthy 상태')]))+para(f'<a href="{url}">복사 가능한 전체 명령·포트·문제 해결 안내</a>','label'),
         '화면의 명령은 길이 때문에 시각적으로 나누었다. 실제 복사는 연결된 안내의 한 줄 명령을 사용한다. init_env는 무작위 키를 생성하고 기존 설정을 보존한다. 키를 장표나 노트북 출력에 쓰지 않는다. Docker VM RAM 약16GB 환경에서 검증했다.',source='lf-compose')
    emit('실제 요청의 작업 트리','09번 Q03a / 이 수업 환경에서 실행한 Langfuse 화면',
         img('langfuse-local-trace.png','실제 로컬 실행. 검색·생성·코드 검사·모델 평가가 하나의 요청에 연결.',True),
         '트리에서 01-retrieval을 눌러 문서를 보고 02-ollama-answer의 Input에서 실제 모델 입력을 확인한다. 참고 정답은 생성 입력에 들어가지 않는다. 입력 문서는 맞아도 조건이 누락될 수 있다. 그림 확대 기능으로 원본 화면을 보여준다.',source='lf-sdk',kind='local-screen')
    emit('코드 점수와 모델 평가의 분리','같은 요청에 연결된 BOOLEAN·CATEGORICAL Scores',
         img('langfuse-local-scores.png','실제 SDK 점수 저장 화면. 1/True는 해당 코드 검사 통과이며 의미 정확도 100%가 아님.',True),
         '코드 검사는 인용 ID와 기권 일관성을 확인한다. llm_groundedness는 작은 모델의 실제 판정이다. 사람이 읽은 검토만 human_review로 기록하고 미실행 검토는 비워 둔다. score 이름과 comment가 검증 범위를 설명해야 한다.',source='lf-scores',kind='local-screen')
    emit('실습 09의 확인 지점','실행 결과와 서버 저장의 구분',
         two(code('result = traced_question(\n    lf, ollama, question\n)\n\nstored = wait_for_trace(lf, result)\n\n# 모델 입력·출력·Scores 확인\nprint(result["url"])'),rows([
             ('20분 핵심','09번 2–5단계'),('부모·자식','전체 요청 1개 + 하위 작업 4개'),('실패 질문','Q24a: 현재 재고 확인'),('완료','화면과 API에서 같은 기록 확인')])),
         'flush는 전송 큐를 비우는 단계이며 worker 저장 완료 자체는 아니다. wait_for_trace는 실제 API를 재조회한다. 큐 처리 지연이 있으면 같은 요청을 새로고침한다. 보이지 않는다고 재실행을 반복하여 기록을 복제하지 않는다.',source='lf-sdk')
    emit('실패 사례의 회귀 평가 전환','관찰한 문제를 다음 변경에서도 다시 검사하는 구조',
         flow([('실패 관찰','재고 질문의 실제 trace'),('참고 기준','문서에 재고 정보 없음'),('평가 데이터','정상 3건 + 경계 1건'),('변경 비교','같은 질문·같은 모델')])+para('실패 사례만 모으지 않음. 데이터 내용 해시와 원본 trace의 연결 유지.','label'),
         '10번에서 Datasets에 4개 사례를 생성한다. source trace로 실패의 출처를 보존한다. 원격 자료가 바뀌면 자동 덮어쓰지 않고 새 버전으로 분리한다. 이미 수업에서 관찰한 사례이므로 미공개 test의 성능 추정으로 사용하지 않는다.',source='lf-experiments')
    emit('세 가지 변경의 비교','프롬프트 개선과 서비스 기능 정책의 역할',
         table(['버전','변경','실시간 재고 질문'],[
             ['A 기준선','기존 프롬프트','모델에 답변 요청'],['B 프롬프트','근거 제한 지시 강화','모델에 답변 요청'],
             ['C 기능 정책','B + 미지원 조회 분기','정책 응답·모델 호출 없음']])+para('요청 유형은 UI 메뉴·API 라우트 입력. 정답 라벨로 분기하지 않음.','label'),
         'C는 policy_qa만 연결된 서비스에서 live_inventory 기능을 제공하지 않는다. 현재 재고를 추측하도록 모델을 부르지 않고 안내 응답을 반환한다. 정상 상담 3건은 실제 Ollama를 실행한다. 자유형 질문의 의도 분류기는 이 실습에서 구현하지 않았다. 미지원 기능을 명확히 설명하는 제품 UX도 함께 검토한다.')
    emit('Langfuse의 실제 실험 비교','Experiments에서 같은 데이터의 버전별 점수 확인',
         img('langfuse-local-experiments.png','실제 로컬 실험 화면. 비교 대상·점수 범위·개별 실패를 함께 확인.',True),
         'A 기준선과 C 기능 정책 비교 화면이다. UI의 비교 선택으로 B도 추가한다. 평균만 보고 결정하지 않고 재고 질문으로 내려가 실제 출력과 trace를 연다. 기능 정책 경로의 generation_ms=0은 호출하지 않았다는 뜻이며 모델 속도 향상 측정값이 아니다.',source='lf-experiments',kind='local-screen')
    values=[]
    for label,key,decision_key,summarykey in [('A 기준선','baseline','decision','baseline'),('B 프롬프트','candidate','decision','candidate'),('C 기능 정책','guarded','guarded_decision','candidate')]:
        m=sample[decision_key]['summary'][summarykey]
        values.append([label,f'{m["structural_pass_rate"]:.0%}',f'{m["false_accepts"]}건',('기준선' if key=='baseline' else sample[decision_key]['decision'])])
    emit('실제 비교 결과와 남은 검토','선택한 합성 회귀 사례 4건 / 일반 성능 추정 아님',
         table(['버전','인용·기권 계약 검사','답변 불가 수락','배포 전 판단'],values)+para('REVIEW도 자동 배포가 아님. 기간·비용·조건의 의미 검토는 별도.','label'),
         '실제 실행값에서 B는 재고 질문의 계약 위반을 해결하지 못했다. C는 기능 경계로 해당 실패를 막았다. 그러나 모든 답변 의미가 맞는 것은 아니다. 특히 취소·반품 조건은 사람이 원문과 대조해야 한다. 코드 통과율과 judge 판정을 서비스 정확도라 부르지 않는다.')
    emit('배포 전 자동 차단의 조건','실행 누락과 필수 실패를 평균에 숨기지 않는 판단',
         two(rows([('완료성','같은 데이터의 모든 문항 실행'),('필수 조건','답변 불가 수락 0건'),('품질·속도','계약 검사·기준선 비교·시간 예산'),('다음 단계','HOLD 또는 사람 검토 REVIEW')]),
             code('python -m week11.lab.release_lab\n\n# B가 HOLD이면 종료 코드 2\npython -m week11.lab.release_lab \\\n  --enforce-gate')),
         '조건은 결과를 보기 전에 고정한다. 수업 기본 3초는 기기와 서비스 요구에 맞춰 사전에 조정한다. 4건으로 p95를 계산해 성능을 주장하지 않는다. 실제 배포나 롤백은 실행하지 않으며 이 코드는 배포 전 차단 단계를 보여준다.')
    emit('실습 완료와 다음 개선','20분 요청 추적 + 25분 실험 비교 + 근거 토론',
         rows([('09 완료','요청 트리·실제 입출력·Scores 설명'),('10 완료','A/B/C 비교와 보류·검토 근거'),('토론','자연스러운 오답과 명확한 기능 제한 중 선택'),('다음 실험','조건 누락 사례 추가·사람 검토 반영')])+para(f'<a href="{url}">시간표·실행 안내</a> · <a href="https://smilesjcha.github.io/llmops-16week/week11/lab/sample/langfuse/">실제 비교 결과 미리 보기</a>','label'),
         '수업 마지막 활동은 한 문장 결론, 실패 사례 하나, 다음 변경 하나다. 설치 문제가 있으면 검증한 실제 캡처로 같은 판단 활동을 진행하고 로컬 실행을 이어간다. 개인 결과는 본인 PC에 남으며 GitHub에 자동 게시되지 않는다.')
    for s in slides[42:]: s['chapter']='8 배포 판단'
    slides[41]['notes']='09는 같은 용어를 실제 Langfuse SDK로 연결한다. LangSmith는 비교 개념 사례로 남겨두고 별도 계정 연동을 하지 않는다. 원래 07–08 JSONL과 실제 SDK 전송 규격은 다르다.'
    slides[-1]['notes']='09–10은 실제 로컬 Langfuse 서버를 사용한다. 공식 플랫폼 전체 운영을 외우기보다 실패 관찰부터 평가·변경 검증·배포 판단까지 연결한다. 실제 클라우드 전송은 없다.'
    result=slides[:42]+extra+slides[42:]
    assert len(result)==64
    return result
