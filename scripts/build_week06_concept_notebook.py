"""Build the executable numerical examples used by the 76-slide Week06 deck."""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
steps = [
    ("정답 확률과 교차 엔트로피", "가상 정답 확률을 자연로그 손실로 바꿉니다. 실제 모델 측정값이 아닙니다.", '''probabilities = np.array([0.2, 0.5, 0.8])
losses = -np.log(probabilities)
assert losses[0] > losses[1] > losses[2]
display([{'probability': float(p), 'loss': float(v)} for p, v in zip(probabilities, losses)])'''),
    ("다음 토큰의 위치", "입력 위치 t에서 정답은 t+1입니다. 가상 ID를 실제 tokenizer 출력으로 해석하지 않습니다.", '''ids = np.array([10, 11, 12, 20, 21, 22])
display([{'position': i, 'input': int(a), 'target': int(b)} for i, (a,b) in enumerate(zip(ids[:-1], ids[1:]))])
assert ids[1:].tolist() == [11, 12, 20, 21, 22]'''),
    ("답변 마스킹과 Shift", "원본 label의 답변 위치 3,4,5는 shift 후 예측 위치 2,3,4에 대응합니다.", '''labels = np.array([-100, -100, -100, 20, 21, 22])
targets = labels[1:]
active = targets != -100
assert targets[active].tolist() == [20, 21, 22]
assert np.flatnonzero(active).tolist() == [2, 3, 4]
print('학습 정답:', targets[active], '예측 위치:', np.flatnonzero(active))'''),
    ("마스킹한 평균 손실", "각 예측 위치에서 해당 정답에 부여한 가상 확률입니다. 전체 위치 평균과 답변 위치 평균은 다릅니다.", '''target_probabilities = np.array([0.9, 0.9, 0.2, 0.5, 0.8])
answer_loss = float(-np.log(target_probabilities[active]).mean())
full_loss = float(-np.log(target_probabilities).mean())
assert np.isclose(answer_loss, losses.mean())
print('답변 위치 평균:', answer_loss, '전체 위치 평균:', full_loss)'''),
    ("학습할 정답이 없는 배치", "모든 label이 -100이면 평균 계산 전에 중단해야 합니다. 실제 trainer 오류 형태는 구현마다 다릅니다.", '''empty_labels = np.full_like(labels, -100)
assert np.count_nonzero(empty_labels[1:] != -100) == 0
print('STOP: 학습할 정답 위치 없음. 경계·잘림·마스크 확인')'''),
    ("길이 제한과 답변 누락", "가상 ID 앞부분만 남겼을 때 학습할 답변 수를 비교합니다. 실제 모델 토큰 길이 검사는 별도로 필요합니다.", '''length_report = []
for length in (3, 4, 6):
    retained = labels[:length][1:]
    length_report.append({'length': length, 'answer_targets': int(np.count_nonzero(retained != -100))})
assert [r['answer_targets'] for r in length_report] == [0, 1, 3]
display(length_report)'''),
    ("LoRA 초기 변화량", "A를 무작위, B를 0으로 두면 시작 시 변화량 BA는 0입니다. 모델 최적화 실행이 아닌 행렬 계산입니다.", '''rng = np.random.default_rng(42)
W = rng.normal(size=(12, 8))
A = rng.normal(size=(2, 8))
B = np.zeros((12, 2))
assert np.allclose(B @ A, 0)
before = W.copy()
adapted = W + B @ A
assert np.array_equal(W, before)
assert np.array_equal(adapted, W)
print('원본 고정:', np.array_equal(W, before), '초기 변화량:', np.linalg.norm(B @ A))'''),
    ("일반 LoRA 배율", "동일한 BA에서 α/r 배율만 비교합니다. 실제 rank 변경 실험에서는 BA도 다시 학습합니다.", '''scales = [{'rank': r, 'alpha': a, 'scale': a/r} for r,a in [(8,16),(16,16),(16,32)]]
assert [r['scale'] for r in scales] == [2, 1, 2]
display(scales)'''),
    ("2-bit 균등 양자화", "[-1,1] 범위의 네 코드값으로 반올림합니다. NF4·bitsandbytes 구현이 아닙니다. NumPy 배열 자체는 실제 2-bit로 패킹하지 않습니다.", '''x = np.array([-1.0, -0.4, 0.2, 1.0])
levels = 2**2 - 1
q = np.rint((x + 1) * levels / 2)
restored = q * 2 / levels - 1
assert np.allclose(restored, [-1, -1/3, 1/3, 1])
display([{'original': float(a), 'code': int(b), 'restored': float(c)} for a,b,c in zip(x,q,restored)])'''),
    ("bit 수와 복원 오차", "고정된 1,001개 균등 격자 값에서 평균제곱오차를 계산합니다. 모델 정확도·NF4 성능으로 일반화할 수 없습니다.", '''grid = np.linspace(-1, 1, 1001)
quantization = []
for bit in (2, 3, 4, 8):
    levels = 2**bit - 1
    codes = np.rint((grid + 1) * levels / 2)
    reconstructed = codes * 2 / levels - 1
    quantization.append({'bits': bit, 'mse': float(np.mean((grid-reconstructed)**2))})
assert all(a['mse'] > b['mse'] for a,b in zip(quantization,quantization[1:]))
display(quantization)'''),
    ("7B 가중치 저장량", "가중치 원시 비트 수를 계산합니다. 스케일·학습 상태·활성값·버퍼는 제외하며 총 VRAM이 아닙니다. GB는 10의 9승 bytes입니다.", '''storage = [{'bits': bit, 'raw_weight_gb': 7_000_000_000 * bit / 8 / 1e9} for bit in (16,8,4)]
assert [r['raw_weight_gb'] for r in storage] == [14.0, 7.0, 3.5]
display(storage)'''),
    ("큰 선형 층의 파라미터", "4096×4096 층 하나에서 A·B 개수와 원본 대비 비율을 계산합니다. 전체 모델 비율은 아닙니다.", '''large_layer = [{'rank': r, 'factor_params': 2*4096*r, 'ratio': (2*4096*r)/(4096**2)} for r in (8,16,32)]
assert [r['factor_params'] for r in large_layer] == [65536, 131072, 262144]
display(large_layer)'''),
    ("실험 기록", "수치와 가정을 함께 저장합니다. 장표의 새 차트는 이 실행 결과를 사용합니다.", '''report = {'method':'offline numerical examples; not SFT/LoRA/QLoRA model training',
          'probability_loss':[{'probability':float(p),'loss':float(v)} for p,v in zip(probabilities,losses)],
          'mask':{'active_predictions':np.flatnonzero(active).tolist(),'answer_targets':targets[active].tolist(),'answer_loss':answer_loss},
          'truncation':length_report, 'uniform_quantization':quantization,
          'raw_weight_storage':storage, 'large_layer':large_layer}
(OUT/'concept-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(OUT/'concept-report.json')'''),
]
setup = '''from pathlib import Path
import sys, json
import numpy as np
from IPython.display import display
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p/'course_labs').is_dir())
OUT = ROOT/'output/validation/week06-concepts'
OUT.mkdir(parents=True, exist_ok=True)
assert sys.version_info[:2] == (3,11), 'Python 3.11 .venv 커널 선택'
print('Python:',sys.version.split()[0],'NumPy:',np.__version__)
'''
cells = [nbf.v4.new_markdown_cell('# 6주차 · 손실·마스킹·양자화 수치 실험\n\n76쪽 강의안의 실행 예시입니다. GPU·API 키·모델 다운로드가 필요 없습니다. 예측값을 적고 실행한 뒤 한 변수를 바꾸어 비교합니다. 실제 SFT·LoRA·QLoRA 학습은 실행하지 않습니다. 권장 20분.'), nbf.v4.new_code_cell(setup)]
for title, explanation, code in steps:
    cells += [nbf.v4.new_markdown_cell(f'## {title}\n\n{explanation}'), nbf.v4.new_code_cell(code)]
cells.append(nbf.v4.new_markdown_cell('## 결과 해석\n\n- 가장 민감하게 변한 설정과 이유\n- 실제 모델에서 추가로 측정할 품질·메모리 항목\n- 이번 계산으로 확인하지 못한 점\n\n데이터 분할·rank 근사 실험은 7주차 Notebook 01·02에서 이어갑니다. 이 실습은 휴일의 새 과제나 제출 요구가 아닙니다.\n\n근거: [TRL SFT](https://huggingface.co/docs/trl/sft_trainer), [LoRA](https://arxiv.org/abs/2106.09685), [QLoRA](https://arxiv.org/abs/2305.14314). 균등 양자화 코드는 자체 교육용 수치 예시입니다.'))
nb = nbf.v4.new_notebook(cells=cells, metadata={'kernelspec':{'display_name':'Python 3.11 (.venv)','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.11'}})
nbf.validate(nb)
target = ROOT/'week06/lab/notebooks/01_loss_quantization.ipynb'
target.parent.mkdir(parents=True,exist_ok=True)
nbf.write(nb,target)
print({'path':str(target.relative_to(ROOT)), 'cells':len(cells), 'code_cells':sum(c.cell_type=='code' for c in cells)})
