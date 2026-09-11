"""Preserve authored picture crops when the artifact exporter substitutes fit crops.

Only native a:srcRect and picture-frame coordinates are changed. Image bytes,
slide text, tables, relationships, and speaker notes remain unchanged.
The resulting package must pass the same finalizer and PDF visual QA.
"""

import argparse
import json
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
for prefix, uri in (("a", A), ("p", P), ("r", R)):
    ET.register_namespace(prefix, uri)
NS = {"a": A, "p": P}


def repair(candidate: Path, manifest: Path) -> None:
    entries = json.loads(manifest.read_text())
    if not entries:
        raise ValueError("Expected an explicit authored crop manifest")
    with ZipFile(candidate) as archive:
        members = archive.infolist()
        payloads = {member.filename: archive.read(member) for member in members}
    for entry in entries:
        name = f"ppt/slides/slide{entry['slide']}.xml"
        root = ET.fromstring(payloads[name])
        pictures = root.findall(".//p:pic", NS)
        expected_count = entry.get("pictureCount", 1)
        if len(pictures) != expected_count:
            raise ValueError(f"Expected {expected_count} pictures on {name}")
        picture = pictures[entry.get("pictureIndex", 0)]
        fill = picture.find("p:blipFill", NS)
        crop = fill.find("a:srcRect", NS)
        if crop is None:
            crop = ET.Element(f"{{{A}}}srcRect")
            fill.insert(1, crop)
        crop.attrib.clear()
        crop.attrib.update(
            {key: str(round(value * 100000)) for key, value in entry["crop"].items()}
        )
        transform = picture.find("p:spPr/a:xfrm", NS)
        frame = entry["frame"]
        transform.find("a:off", NS).attrib.update(
            x=str(round(frame["left"] * 9525)), y=str(round(frame["top"] * 9525))
        )
        transform.find("a:ext", NS).attrib.update(
            cx=str(round(frame["width"] * 9525)), cy=str(round(frame["height"] * 9525))
        )
        payloads[name] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    repaired = candidate.with_name(candidate.stem + "-cropped.pptx")
    with ZipFile(repaired, "w") as archive:
        for member in members:
            archive.writestr(member, payloads[member.filename])
    repaired.replace(candidate)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    repair(args.candidate, args.manifest)
