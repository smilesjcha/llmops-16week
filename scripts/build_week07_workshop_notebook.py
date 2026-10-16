"""Build the numerical and synthetic evaluation workshop for Week07."""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
setup = '''from pathlib import Path
import sys, json
import numpy as np
from IPython.display import display
ROOT = next(p for p in [Path.cwd(),*Path.cwd().parents] if (p/'course_labs').is_dir())
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from course_labs.adaptation import dpo_loss, toy_preference_training
from course_labs.preference_evaluation import *
OUT = ROOT/'output/validation/week07-workshop'
OUT.mkdir(parents=True,exist_ok=True)
assert sys.version_info[:2] == (3,11), 'Python 3.11 .venv 커널 선택'
print('Python:',sys.version.split()[0],'NumPy:',np.__version__)
'''
steps = [
('토큰 확률과 시퀀스 확률','기대 답변 토큰에 부여한 가상 조건부 확률입니다. 실제 tokenizer나 모델을 실행하지 않습니다.', '''token_probabilities = [.8,.5,.2]
logp = sequence_logprob(token_probabilities)
assert np.isclose(logp, np.log(.08))
print('log P:',logp,'P:',np.exp(logp))'''),
('긴 답변의 확률 비교','원 논문의 기본 DPO 계산은 답변 토큰 log probability의 합입니다. 평균·길이 정규화를 섞으면 다른 목적이 될 수 있습니다.', '''short = sequence_logprob([.8,.8])
long = sequence_logprob([.8,.8,.8,.8])
assert long < short
print('두 토큰:',short,'네 토큰:',long,'토큰당 평균:',short/2,long/4)'''),
('reference 대비 변화','policy의 chosen/rejected 차이에서 고정 reference의 차이를 뺍니다. Judge 점수를 넣지 않습니다.', '''policy = (-2.,-5.)
reference = (-3.,-3.)
margin = (policy[0]-policy[1])-(reference[0]-reference[1])
assert margin == 3
print('margin:',margin,'loss:',dpo_loss(*policy,*reference,.1))'''),
('기준선과 반대 방향','세 조건의 수식 계산을 비교합니다. 업무 평가 결과가 아닙니다.', '''conditions = [{'label':label,'margin':m,'loss':float(np.logaddexp(0,-.1*m))} for label,m in [('baseline',0),('preferred',3),('opposite',-3)]]
assert conditions[1]['loss'] < conditions[0]['loss'] < conditions[2]['loss']
display(conditions)'''),
('beta별 고정 margin','동일한 margin에서 수식 민감도만 관찰합니다. beta가 클수록 실제 모델 품질이 좋다는 뜻은 아닙니다.', '''margins = [-6,-3,0,3,6]
beta_curves = [{'beta':b,'values':[float(np.logaddexp(0,-b*m)) for m in margins]} for b in (.1,.5,1.)]
display(beta_curves)
assert all(np.isclose(r['values'][2],np.log(2)) for r in beta_curves)'''),
('두 답변 정책의 80회 갱신','질문 하나·답변 두 개의 Bernoulli policy입니다. 언어 모델이나 새 질문의 일반화를 검증하지 않습니다.', '''history = toy_preference_training(beta=.5,steps=80,lr=.3)
assert history[-1]['loss'] < history[0]['loss']
assert history[-1]['chosen_probability'] > history[0]['chosen_probability']
display(history[::20])'''),
('평가 fixture 12건','직접 작성한 0/1 플래그 조합입니다. 모델 출력도 사람의 실제 평가 결과도 아닙니다. 네 차원은 근거·형식·유용성·과도한 거절 없음입니다.', '''fixtures = evaluation_fixtures()
assert len(fixtures)==12 and all(r['synthetic'] for r in fixtures)
display(fixtures[:3])'''),
('수업용 비교 규칙','근거·형식의 필수 조건을 먼저 확인합니다. 둘 다 위반하면 검토, 둘 다 통과하면 유용성·거절을 비교합니다. 서비스별 기준은 별도 합의가 필요합니다.', '''verdicts = [{'id':r['id'],'verdict':fixture_verdict(r['baseline'],r['candidate'])} for r in fixtures]
summary = fixture_summary(fixtures)
assert summary['counts']=={'candidate':4,'baseline':4,'tie':3,'review':1}
display(verdicts); display(summary)'''),
('차원별 결과와 회귀','형식 통과율은 좋아지지만 근거 통과율은 나빠지도록 만든 fixture입니다. 평균·승률 한 개만으로 배포하지 않습니다.', '''b,c = summary['rates']['baseline'],summary['rates']['candidate']
assert c['format'] > b['format'] and c['evidence'] < b['evidence']
display([{'dimension':k,'baseline':b[k],'candidate':c[k]} for k in DIMENSIONS])
print('모델 개선 성과가 아닌, 집계 해석을 위한 합성 입력')'''),
('사람 검토와 답변 순서 가림','답변 A/B에 모델 이름을 표시하지 않는 배치 예시입니다. 가림 자체가 편향 제거를 보장하지는 않습니다.', '''rng = np.random.default_rng(42)
presentation = [{'id':r['id'],'A':name,'B':'candidate' if name=='baseline' else 'baseline'} for r in fixtures for name in [str(rng.choice(['baseline','candidate']))]]
assert all(r['A'] != r['B'] for r in presentation)
display(presentation[:4])
print('이 대응표는 평가자에게 공개하지 않는 관리용 정보')'''),
('실패 사례와 배포 판단','사전 합의한 기준과 회귀 사례를 사람이 검토하는 계획입니다. 이 코드는 모델 승격이나 성적 평가를 실행하지 않습니다.', '''regressions = [r['id'] for r in fixtures if r['baseline']['evidence'] and not r['candidate']['evidence']]
assert regressions == ['SYN-03','SYN-12']
decision = {'status':'human_review_required','evidence_regressions':regressions,'missing':'실제 모델 응답·보류 입력·시간·메모리 측정'}
display(decision)'''),
('PRD 요구사항 연결','서비스 구현 요구를 측정 방법과 실패 처리로 연결합니다. 목표값은 제안값이며 실제 성과가 아닙니다.', '''requirements = [{'id':'FR01','requirement':'근거 문장과 원문 위치 표시','test':'고정 입력에서 인용 위치 검토','fallback':'근거 부족 시 보류'}, {'id':'FR02','requirement':'구조화 출력 형식 준수','test':'JSON schema 검사','fallback':'재시도 후 검토 요청'}]
assert all(all(row.get(k) for k in ['id','requirement','test','fallback']) for row in requirements)
display(requirements)'''),
('실행 근거 저장','새 차트의 숫자와 가정을 함께 남깁니다. 학생 제출물·개인정보는 사용하지 않습니다.', '''report = {'method':'numerical DPO + authored evaluation fixtures; no LLM training or measured model quality',
 'conditions':conditions,'margins':margins,'beta_curves':beta_curves,'toy_history':history,
 'evaluation':summary,'decision':decision,'requirements':requirements}
(OUT/'workshop-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(OUT/'workshop-report.json')'''),
]
cells=[nbf.v4.new_markdown_cell('# 05 · DPO 계산과 비교 평가 워크숍\n\n80쪽 7주차 강의안의 단계별 실습입니다. 공통 Python 3.11 환경에서 GPU·API 키·모델 다운로드 없이 실행합니다. 실제 DPO 모델 학습·모델 품질 평가·학생 성적 자동 결정과 구분합니다. 권장 20분.'),nbf.v4.new_code_cell(setup)]
for title,explanation,code in steps:
    cells += [nbf.v4.new_markdown_cell(f'## {title}\n\n{explanation}'),nbf.v4.new_code_cell(code)]
cells.append(nbf.v4.new_markdown_cell('## 기획서에 남길 근거\n\n1. 바꾼 변수와 결과\n2. 합성 fixture를 실제 품질 측정으로 옮기기 위해 필요한 자료\n3. 채택 판단에 필요한 추가 실험\n\n기획서 수정본 마감: 2026-10-22(목) 23:59 한국시간. 10월 23일은 시험·실시간 수업 없이 제출물 평가입니다. 이 워크숍을 별도 필수 미세조정 과제로 추가하지 않습니다.\n\n근거: [DPO 원 논문](https://arxiv.org/abs/2305.18290), [TRL DPO Trainer](https://huggingface.co/docs/trl/dpo_trainer). 평가 fixture와 판단 규칙은 자체 교육용 예시입니다.'))
nb=nbf.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python 3.11 (.venv)','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.11'}})
nbf.validate(nb)
target=ROOT/'week07/lab/notebooks/05_dpo_evaluation_workshop.ipynb'
nbf.write(nb,target)
print({'path':str(target.relative_to(ROOT)),'cells':len(cells),'code_cells':sum(c.cell_type=='code' for c in cells)})
