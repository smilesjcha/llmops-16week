# Week 03 deck build

`build_deck.mjs` is the editable source of the 72-slide PowerPoint. It uses the bundled ArtifacTool runtime, enforces a visible 14pt minimum, adds speaker notes with sources on every slide, and validates the final package.

Build from the repository root with the bundled runtime paths supplied by Codex. The final file is created under `week03/lecture/build/<revision>/final/` and then copied to `week03/lecture/`.

Do not edit the `.pptx` ZIP package directly. Update the source script, build a new revision, render all slides, and inspect the generated validation receipt before replacing the published file.
