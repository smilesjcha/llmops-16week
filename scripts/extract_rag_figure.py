"""Read-only extraction of Figure 1 from the published RAG paper."""

import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
# Published figure only; grayscale presentation preserves the course palette.
subprocess.run(
    [
        "pdftoppm",
        "-f",
        "2",
        "-l",
        "2",
        "-r",
        "180",
        "-x",
        "262",
        "-y",
        "170",
        "-W",
        "1018",
        "-H",
        "300",
        "-gray",
        "-png",
        "-singlefile",
        "/tmp/llmops-rag-paper.pdf",
        str(root / "week04/lecture/assets/rag-paper-figure1"),
    ],
    check=True,
)
