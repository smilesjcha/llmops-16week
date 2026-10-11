"""Generate reproducible offline notebooks from reviewed teaching source."""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
SETUP = '''from pathlib import Path
import sys, json
import numpy as np
from IPython.display import display, HTML
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'course_labs').is_dir())
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from course_labs.adaptation import *
OUT = ROOT / 'output' / 'validation' / 'adaptation-labs'
OUT.mkdir(parents=True, exist_ok=True)
print('Python:', sys.version.split()[0], 'NumPy:', np.__version__)
assert sys.version_info[:2] == (3, 11), '공통 환경 Python 3.11 커널을 선택하세요.'
'''

def notebook(name, title, intro, steps):
    cells = [nbf.v4.new_markdown_cell(f'# {title}\n\n{intro}\n\n모델 다운로드·API 키·GPU 없이 실행합니다. 합성 자료만 사용하며, 실제 LLM 학습·성능 검증과 구분합니다. 예측 → 실행 → 변수 변경 → 근거 기록의 순서로 진행합니다.'), nbf.v4.new_code_cell(SETUP)]
    for heading, explanation, code in steps:
        cells += [nbf.v4.new_markdown_cell(f'## {heading}\n\n{explanation}'), nbf.v4.new_code_cell(code)]
    cells.append(nbf.v4.new_markdown_cell('## 실행 기록과 기획서 연결\n\n1. 바꾼 변수와 달라진 결과\n2. 이 실험으로 확인하지 못한 부분\n3. 프로젝트에서 추가로 검증할 가정\n\n출력은 `output/validation/adaptation-labs/`에 저장됩니다. 개인정보나 학생 제출물은 공개 저장소에 넣지 않습니다.'))
    nb = nbf.v4.new_notebook(cells=cells, metadata={'kernelspec': {'display_name': 'Python 3.11 (.venv)', 'language': 'python', 'name': 'python3'}, 'language_info': {'name': 'python', 'version': '3.11'}})
    nbf.validate(nb)
    path = ROOT / 'week07/lab/notebooks' / name
    path.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, path)

notebook('01_data_quality_split.ipynb', '01 · 학습 데이터와 누출 점검', '지도 미세조정(Supervised Fine-Tuning, SFT) 준비에서 형식·출력 계약·사례 단위 분할을 확인합니다. 약 15분.', [
 ('합성 사례 48건', '24개의 사건마다 표현이 다른 두 문의를 구성합니다. 개별 문장과 사건 ID의 차이를 확인하세요.', "data = examples()\nprint(len(data)); display(data[:2])"),
 ('정상 데이터 점검', '형식 통과는 내용의 정확성이나 사용 권한의 승인을 뜻하지 않습니다.', "report = audit(data)\ndisplay(report)\nassert not report['issues'] and not report['duplicate_ids']"),
 ('중복의 주입', '복사된 사례 한 건을 추가했을 때 ID 중복과 내용 중복은 각각 어떻게 잡힐까요?', "bad = [dict(r) for r in data] + [dict(data[0])]\ndisplay(audit(bad))\nassert audit(bad)['duplicate_content'] == 1"),
 ('출력 계약의 위반', 'JSON 구문만 맞는 것과 필요한 필드가 맞는 것은 다릅니다.', "bad[1]['response'] = '{broken}'\nbad[2]['response'] = json.dumps({'answer': 'ok'})\ndisplay(audit(bad)['issues'])"),
 ('누락·권한 검토', '합성 표시가 없는 레코드를 자동 승인하지 않습니다. 실제 데이터는 별도 사용 허가가 필요합니다.', "bad[3]['instruction'] = ''\nbad[4]['synthetic'] = False\ndisplay(audit(bad)['issues'])"),
 ('문장 단위 분할의 위험', '표현이 다른 동일 사건이 train/test에 나뉘는 의도적인 잘못된 예시입니다.', "naive = {'train': data[::2], 'test': data[1::2]}\ndisplay(leakage(naive))\nassert len(leakage(naive)[0]['shared_groups']) == 24"),
 ('사례 단위 분할', '같은 사건의 모든 표현을 한 분할에 모읍니다. 개발용 dev와 최종 test를 분리합니다.', "splits = split_groups(data, seed=42)\nprint({k: len(v) for k, v in splits.items()})\nassert not leakage(splits)"),
 ('분할 재현성', '같은 seed가 같은 분할을 만듭니다. seed 변경과 성능 개선은 다른 주장입니다.', "assert splits == split_groups(data, seed=42)\nother = split_groups(data, seed=7)\nprint('seed 변경 → 같은 분할?', splits == other)"),
 ('문자 길이 점검', '문자 수는 토큰 수가 아닙니다. 실제 학습 전 해당 토크나이저로 토큰 길이를 다시 확인해야 합니다.', "lengths = [len(r['instruction'] + r['input'] + r['response']) for r in data]\nprint('문자 길이 min/median/max:', min(lengths), np.median(lengths), max(lengths))"),
 ('검증 세트 오염의 탐지', '분할 이후 데이터가 추가될 때에도 누출 검사를 다시 수행합니다.', "polluted = {k: list(v) for k, v in splits.items()}\npolluted['test'].append(splits['train'][0])\nassert leakage(polluted)\ndisplay(leakage(polluted))"),
 ('대화 템플릿', '모델별 역할·종료 토큰은 다릅니다. 아래는 역할 구조 설명용이며 특정 모델 토큰이 아닙니다.', "row = data[0]\nchat = [{'role': 'user', 'content': row['instruction'] + '\\n' + row['input']}, {'role': 'assistant', 'content': row['response']}]\ndisplay(chat)"),
 ('손실 마스킹의 경계', '가상 토큰 ID로 입력/답변 경계를 확인합니다. 실제 tokenizer나 trainer 실행이 아닙니다.', "token_ids = [10, 11, 12, 20, 21, 22]\nlabels = [-100, -100, -100, 20, 21, 22]\nassert sum(x != -100 for x in labels) == 3\nprint('답변 학습 위치:', [i for i, x in enumerate(labels) if x != -100])"),
 ('Dataset Card 기록', '자료 출처·사용 범위·분할 기준·한계를 명시합니다.', "card = {'source': '수업 합성 자료', 'permission': '교육 실험', 'rows': len(data), 'split': {k: len(v) for k,v in splits.items()}, 'seed': 42, 'limitation': '실제 고객 분포를 대표하지 않음'}\nsave_report(OUT / 'dataset-card.json', card)\ndisplay(card)"),
])

notebook('02_low_rank_adaptation.ipynb', '02 · LoRA의 행렬 구조', 'Low-Rank Adaptation(LoRA, 저차원 행렬을 이용한 모델 적응)의 원리를 작은 행렬로 관찰합니다. 실제 Adapter 학습이 아니라 특이값 분해(Singular Value Decomposition, SVD)로 변화량을 근사합니다. 약 10분.', [
 ('고정 가중치와 변화량', '기존 가중치 W와 적용할 변화량 ΔW를 분리합니다.', "rng = np.random.default_rng(42)\nW = rng.normal(size=(12, 8)); delta = rng.normal(size=(12, 8))\nW_original = W.copy()\nprint('W/ΔW:', W.shape, delta.shape)"),
 ('rank 2의 행렬', 'B는 12×2, A는 2×8이고 BA는 12×8입니다.', "r2 = rank_approximation(delta, 2)\nprint('B:', r2['b'].shape, 'A:', r2['a'].shape, 'BA:', r2['update'].shape)\nassert r2['update'].shape == W.shape"),
 ('학습 대상 수의 비교', '작은 예시에서는 rank가 커지면 오히려 전체 행렬보다 파라미터가 많아질 수 있습니다.', "rows = [{'rank': r, 'full': 96, 'factor': rank_approximation(delta, r)['factor_params']} for r in (1,2,4,8)]\ndisplay(rows)"),
 ('근사 오차', 'Frobenius norm 기준 상대 오차입니다. 언어 모델 품질 점수가 아닙니다.', "metrics = [{'rank': r, 'relative_error': rank_approximation(delta,r)['relative_error']} for r in (1,2,4,8)]\ndisplay(metrics)\nassert metrics[-1]['relative_error'] < 1e-12"),
 ('rank와 오차의 시각화', '길이가 짧을수록 행렬 근사 오차가 작은 것입니다. 업무 성능과 혼동하지 마세요.', "display(HTML(''.join(f\"<p>rank {m['rank']} <span style='display:inline-block;background:#284b72;height:14px;width:{m['relative_error']*400}px'></span> {m['relative_error']:.3f}</p>\" for m in metrics)))"),
 ('저차원 구조의 예시', '본래 rank 2인 변화량은 rank 2로 거의 완벽하게 복원할 수 있습니다.', "structured = rng.normal(size=(12,2)) @ rng.normal(size=(2,8))\nprint(rank_approximation(structured,2)['relative_error'])\nassert rank_approximation(structured,2)['relative_error'] < 1e-12"),
 ('일반 LoRA의 scaling', '설명용 α/r scaling입니다. 라이브러리의 다른 scaling 방식은 구별해야 합니다.', "alpha, rank = 16, 2\nadapted = W + (alpha/rank) * r2['update']\nassert np.array_equal(W, W_original)\nprint('원본 고정:', np.array_equal(W,W_original))"),
 ('입력에 대한 출력 변화', '행렬의 출력 변화를 직접 계산합니다. 텍스트 생성 결과가 아닙니다.', "x = rng.normal(size=8)\ny_base, y_adapted = W @ x, adapted @ x\nprint('출력 차이 L2:', np.linalg.norm(y_adapted-y_base))"),
 ('큰 층의 비용 계산', '4096×4096 선형 층 하나만 비교합니다. 전체 모델 메모리 추정이 아닙니다.', "d = 4096\nfor r in (8,16,32):\n    print(r, 'full', d*d, 'factors', 2*d*r, '비율', (2*d*r)/(d*d))"),
 ('자원 추정의 한계', '가중치 외에 gradient, optimizer state, activation, 임시 버퍼가 필요합니다.', "weight_bytes = 4096*4096*2\nprint('FP16 가중치만 MiB:', weight_bytes/1024**2)\nprint('GPU 최대 메모리 측정값 아님')"),
 ('실험 기록', '원본 가중치 고정과 오차 정의를 산출물에 함께 기록합니다.', "save_report(OUT / 'low-rank-report.json', {'method':'SVD approximation; not trained LoRA', 'shape': list(delta.shape), 'metrics': metrics, 'parameters': rows})"),
])

notebook('03_preference_dpo.ipynb', '03 · 선호 데이터와 DPO 손실', 'Direct Preference Optimization(DPO, 직접 선호 최적화)의 입력과 손실을 수치로 확인합니다. 단일 질문·두 고정 답변의 장난감 정책 학습만 실행합니다. 실제 언어 모델 미세조정이나 일반화 검증이 아닙니다. 약 15분.', [
 ('선호쌍과 선택 이유', 'chosen/rejected는 절대 정답/오답이 아니라 명시한 기준에 따른 상대 선택입니다.', "prefs = [{'prompt':'근거 문서가 없는 문의', 'chosen':'확인할 수 없어 담당자 검토가 필요합니다.', 'rejected':'무조건 승인됩니다.', 'reason':'근거 없는 단정 방지'}]\ndisplay(prefs)\nassert not preference_audit(prefs)"),
 ('무효 쌍', '동일한 두 답변은 비교 신호를 주지 않습니다.', "invalid = [dict(prefs[0], rejected=prefs[0]['chosen'])]\ndisplay(preference_audit(invalid))"),
 ('길이 편향 점검', '길이 차이는 검토 신호이지 선호쌍 삭제의 자동 기준이 아닙니다.', "for p in prefs:\n    print('문자 수:', len(p['chosen']), len(p['rejected']), '선택 근거:', p['reason'])"),
 ('log probability의 의미', '이 예시는 이미 계산된 시퀀스 log probability를 사용합니다. Judge 점수를 넣지 않습니다.', "policy = (-2.0, -5.0); reference = (-3.0, -3.0)\nmargin = (policy[0]-policy[1])-(reference[0]-reference[1])\nprint('reference 대비 선호 margin:', margin)"),
 ('기준선의 손실', 'policy와 reference의 선호 차이가 같으면 log(2)입니다.', "loss0 = dpo_loss(-3,-3,-3,-3,beta=.1)\nprint(loss0)\nassert np.isclose(loss0,np.log(2))"),
 ('선호 방향의 변화', 'chosen의 상대 log probability가 증가할 때 해당 쌍의 손실이 줄어듭니다.', "good = dpo_loss(-2,-5,-3,-3,.1)\nbad = dpo_loss(-5,-2,-3,-3,.1)\nprint('선호 방향 / 반대 방향:',good,bad)\nassert good < loss0 < bad"),
 ('beta 민감도', '하나의 margin에서 손실이 달라지는 관찰입니다. beta가 클수록 품질이 좋아진다는 결론은 아닙니다.', "betas = [.1,.5,1.]\ndisplay([{'beta': b, 'loss': dpo_loss(-2,-5,-3,-3,b)} for b in betas])"),
 ('reference의 영향', 'reference가 이미 chosen을 더 선호하면 추가 변화의 margin은 달라집니다.', "display([{'ref_chosen': c, 'loss': dpo_loss(-2,-5,c,-5,.1)} for c in (-5,-3,-2)])"),
 ('수치 안정성', 'logaddexp를 사용해 매우 큰 margin에서 overflow를 피합니다.', "assert np.isfinite(dpo_loss(-10000,0,0,0))\nprint(dpo_loss(-10000,0,0,0))"),
 ('두 답변 정책의 최적화', 'Bernoulli policy의 θ 하나를 갱신합니다. reference는 0.5/0.5로 고정합니다.', "history = toy_preference_training(beta=.5,steps=80,lr=.3)\ndisplay(history[::20])\nassert history[-1]['loss'] < history[0]['loss']"),
 ('beta별 고정 step 실험', '같은 학습률·step의 장난감 예시입니다. 실제 LLM 결과로 승격하지 마세요.', "ab = []\nfor b in betas:\n    run=toy_preference_training(beta=b)\n    ab.append({'beta':b, **run[-1]})\ndisplay(ab)"),
 ('선호 확률 시각화', '한 쌍을 더 선호하게 되었을 뿐, 새로운 질문의 안전성과 정확성을 입증하지 않습니다.', "display(HTML(''.join(f\"<p>step {r['step']:02} <span style='display:inline-block;background:#284b72;height:14px;width:{r['chosen_probability']*400}px'></span> {r['chosen_probability']:.3f}</p>\" for r in history[::20])))"),
 ('평가표의 분리', '실제 모델에서는 동일 입력의 유용성·근거·형식·과도한 거절을 따로 확인합니다.', "evaluation_plan = {'fixed_prompts':10, 'dimensions':['유용성','근거','형식','과도한 거절'], 'baseline':'SFT model', 'blind_order':True, 'judge':'human review + explicit rubric', 'limitation':'모델 비교 미실행'}\nsave_report(OUT / 'preference-report.json', {'toy_runs':ab,'evaluation_plan':evaluation_plan})"),
])

notebook('04_project_proposal.ipynb', '04 · 실험에서 기획서 초안으로', '2Pager(2페이지 제안 요약)·PRD(Product Requirements Document, 제품 요구사항 문서)의 핵심을 실행 근거와 연결합니다. HTML은 문서 시안이며 서비스 구현이 아닙니다. 약 15분.', [
 ('서비스 문제의 범위', '글쓰기 개선 서비스의 합성 기획 예시입니다. 아래 내용을 복사 제출하지 말고 자신의 문제로 바꾸세요.', "doc = {'user':'한국어 논증 글쓰기를 연습하는 대학생', 'problem':'자신의 주장과 근거가 연결되는지 확인하기 어려움. 문단별 근거 피드백 제안.', 'baseline':'교수·동료 피드백 또는 일반 채팅 도구', 'scope':'서론·본론1·본론2·결론 구조와 근거 연결만 지원. 성적 자동 결정 제외.', 'data_rights':'동의받은 글 또는 합성 글. 이름 제거·삭제 요청 경로 제공.', 'evaluation':'개발용 20건과 보류용 10건 분리; 구조 판정 일치도·근거 인용 오류·수정 수용 여부 기록.', 'fallback':'근거 부족 시 판단 보류·사용자 수정·교수 검토', 'roadmap':'7주 문제·초안; 8주 피드백 반영; 9–12주 최소 기능·평가; 13–16주 운영·발표', 'question':'구조 판정과 문체 피드백 중 먼저 검증할 범위는 무엇인가?'}\ndisplay(doc)"),
 ('기획서 필수 항목', '문자열 유무 검사입니다. 좋은 기획서인지 자동 채점하지 않습니다.', "assert proposal_check(doc) == []\nprint('항목 유무 통과 · 내용 검토 별도')"),
 ('누락의 주입', 'evaluation이 없어도 시안은 예뻐 보일 수 있습니다. 자동 검사로 누락만 찾습니다.', "incomplete = dict(doc); incomplete.pop('evaluation')\nassert proposal_check(incomplete) == ['evaluation']\nprint(proposal_check(incomplete))"),
 ('기술 대안 비교', '서비스 요구를 먼저 정한 뒤 어떤 실패를 고칠지 비교합니다.', "alternatives = [{'method':'Prompt + schema','first_test':'구조 판정과 JSON 오류','cost':'개발시간·추론비용'}, {'method':'RAG','first_test':'평가기준 문서의 근거 회수','cost':'검색·문서 관리'}, {'method':'SFT/LoRA','first_test':'반복 형식·행동 오류','cost':'허가된 학습자료·GPU·재평가'}, {'method':'DPO','first_test':'기준 있는 선호쌍과 편향','cost':'선호 라벨·reference·재평가'}]\ndisplay(alternatives)"),
 ('측정 가능한 요구사항', '아래 목표는 제안값입니다. 교수 합의나 실제 성과가 아닙니다.', "requirements = [{'id':'FR01','requirement':'주장·근거 문장을 원문 위치로 제시','acceptance':'고정 10건에서 인용 위치 오류 0건 목표'}, {'id':'FR02','requirement':'불확실한 구조는 보류','acceptance':'보류 사유·수정 버튼을 모든 보류 응답에 표시'}]\ndisplay(requirements)"),
 ('위험과 복구', '사업·사용 경험·개발 관점에서 실패를 점검합니다.', "risks = [{'risk':'학생 글 외부 노출','control':'동의·최소 수집·비공개 저장·삭제'}, {'risk':'유창한 오판','control':'원문 근거·보류·사람 검토'}, {'risk':'구현 범위 과다','control':'구조 판정 한 기능으로 시작'}]\ndisplay(risks)"),
 ('실험 근거 연결', '앞의 노트북 결과가 있는지 확인합니다. 미실행 결과를 생성한 것처럼 표시하지 않습니다.', "evidence=[]\nfor name in ['dataset-card.json','low-rank-report.json','preference-report.json']:\n    evidence.append({'file':name,'exists':(OUT/name).exists()})\ndisplay(evidence)"),
 ('역할과 완료 조건', '2–4인 팀은 역할을 나누고, 개인은 같은 항목을 혼자 점검합니다. 학생 이름을 넣지 않습니다.', "tasks = [{'role':'PM','done':'문제·대안·범위·근거 정리'}, {'role':'UX','done':'정상·오류·보류·수정 흐름'}, {'role':'개발·평가','done':'데이터 권한·고정 평가셋·복구 계획'}]\ndisplay(tasks)"),
 ('HTML 문서 생성', '입력 문자열은 escape 처리합니다. 생성 후 브라우저에서 문서를 검토하세요.', "html = proposal_html(doc)\npath = OUT/'proposal-draft.html'\npath.write_text(html,encoding='utf-8')\nprint(path)"),
 ('시안 미리보기', '이 미리보기는 문서입니다. 실제 서비스나 사용성 검증이 아닙니다.', "display(HTML(html))"),
 ('피드백 기록', '피드백을 받은 뒤 채택·보류·반박의 이유를 남깁니다. 아래는 빈 기록 양식입니다.', "feedback = {'version':'0.1','question':doc['question'],'professor_feedback':'미수신','decision':'미결정','reason':'','next_evidence':''}\nsave_report(OUT/'feedback-log.json',feedback)\ndisplay(feedback)"),
 ('제출 전 검사', '초안10/16 → 피드백 → 수정본10/23. 소속 공지의 정확한 시각·채널을 확인합니다.', "save_report(OUT/'proposal-draft.json',doc)\nprint('아주대: LMS / 다른 학교: 공지 교수 이메일')\nprint('PPT·Word·PDF·HTML 가능 / HWP 제외 / 개인정보 공개 GitHub 금지')"),
])
print('Generated 4 Week07 notebooks')
