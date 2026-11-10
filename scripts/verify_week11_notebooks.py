"""Fresh kernel execution; outputs are private verification artifacts."""
import json
from pathlib import Path
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
out = root / "output/validation/week11-notebooks"
out.mkdir(parents=True, exist_ok=True)
records = []
for path in sorted((root / "week11/lab/notebooks").glob("*.ipynb")):
    nb = nbformat.read(path, as_version=4)
    nbformat.validate(nb)
    NotebookClient(nb, timeout=180, kernel_name="python3",
                   resources={"metadata": {"path": str(path.parent)}}).execute()
    assert not [o for c in nb.cells if c.cell_type == "code" for o in c.outputs if o.output_type == "error"]
    nbformat.write(nb, out / path.name)
    row = dict(notebook=path.name, cells=len(nb.cells),
               code_cells=sum(c.cell_type == "code" for c in nb.cells), errors=0)
    records.append(row)
    print(row, flush=True)
(out / "receipt.json").write_text(json.dumps(records, indent=2))
