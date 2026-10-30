"""Fresh kernel per notebook; keep executed outputs private."""

import json
from pathlib import Path
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
out = root / "output/validation/week09-notebooks"
out.mkdir(parents=True, exist_ok=True)
records = []
for path in sorted((root / "week09/lab/notebooks").glob("*.ipynb")):
    nb = nbformat.read(path, as_version=4)
    nbformat.validate(nb)
    NotebookClient(
        nb, timeout=120, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}}
    ).execute()
    assert not [
        o for c in nb.cells if c.cell_type == "code" for o in c.outputs if o.output_type == "error"
    ]
    nbformat.write(nb, out / path.name)
    records.append(
        {
            "notebook": path.name,
            "cells": len(nb.cells),
            "code_cells": sum(c.cell_type == "code" for c in nb.cells),
            "errors": 0,
        }
    )
    print(records[-1], flush=True)
(out / "receipt.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
