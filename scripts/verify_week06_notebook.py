"""Run Week06 numerical examples in a fresh kernel; keep receipts private."""
import json
from pathlib import Path
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
path = root/'week06/lab/notebooks/01_loss_quantization.ipynb'
notebook = nbformat.read(path, as_version=4)
nbformat.validate(notebook)
NotebookClient(notebook, timeout=120, kernel_name='python3', resources={'metadata':{'path':str(path.parent)}}).execute()
errors = [o for c in notebook.cells if c.cell_type=='code' for o in c.outputs if o.output_type=='error']
assert not errors
out = root/'output/validation/week06-concepts'
out.mkdir(parents=True,exist_ok=True)
nbformat.write(notebook,out/path.name)
report = json.loads((out/'concept-report.json').read_text())
assert report['mask']['answer_targets']==[20,21,22]
assert [r['answer_targets'] for r in report['truncation']]==[0,1,3]
assert [r['raw_weight_gb'] for r in report['raw_weight_storage']]==[14,7,3.5]
receipt = {'notebook':str(path.relative_to(root)),'cells':len(notebook.cells),'code_cells':sum(c.cell_type=='code' for c in notebook.cells),'errors':len(errors),'claim':'Numerical examples only; no LLM training or GPU measurements.'}
(out/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
print(receipt)
