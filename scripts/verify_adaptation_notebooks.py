"""Execute each new notebook in a fresh kernel and save private QA output."""
import json
from pathlib import Path
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
out = root / 'output/validation/adaptation-notebooks'
out.mkdir(parents=True, exist_ok=True)
records = []
for path in sorted(root.glob('week07/lab/notebooks/*.ipynb')):
    nb = nbformat.read(path, as_version=4)
    nbformat.validate(nb)
    NotebookClient(nb, timeout=120, kernel_name='python3', resources={'metadata': {'path': str(path.parent)}}).execute()
    errors = [o for c in nb.cells if c.cell_type == 'code' for o in c.outputs if o.output_type == 'error']
    assert not errors
    nbformat.write(nb, out/path.name)
    records.append({'notebook': str(path.relative_to(root)), 'cells': len(nb.cells), 'code_cells': sum(c.cell_type == 'code' for c in nb.cells), 'errors':len(errors)})
    print(records[-1], flush=True)
(out/'receipt.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
