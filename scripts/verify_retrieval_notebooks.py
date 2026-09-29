"""Execute every required notebook in a fresh kernel; keep outputs private."""

import json
from pathlib import Path

import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
out = root / "output" / "validation" / "retrieval-notebooks"
out.mkdir(parents=True, exist_ok=True)
records = []
for p in sorted(root.glob("week0[45]/lab/notebooks/*.ipynb")):
    nb = nbformat.read(p, as_version=4)
    nbformat.validate(nb)
    NotebookClient(
        nb, timeout=180, kernel_name="python3", resources={"metadata": {"path": str(p.parent)}}
    ).execute()
    target = out / (p.parents[2].name + "_" + p.name)
    nbformat.write(nb, target)
    errors = [
        o for c in nb.cells if c.cell_type == "code" for o in c.outputs if o.output_type == "error"
    ]
    assert not errors
    records.append(
        {
            "notebook": str(p.relative_to(root)),
            "cells": len(nb.cells),
            "code_cells": sum(c.cell_type == "code" for c in nb.cells),
            "errors": len(errors),
        }
    )
    print(records[-1], flush=True)
(out / "receipt.json").write_text(json.dumps(records, ensure_ascii=False, indent=2))
