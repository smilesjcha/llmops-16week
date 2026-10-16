"""Apply PowerPoint's native grayscale display effect; preserve image bytes."""
import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as ET

target = Path(sys.argv[1])
slides = {f'ppt/slides/slide{n}.xml' for n in sys.argv[2:]}
ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
with ZipFile(target) as source:
    entries = [(item, source.read(item.filename)) for item in source.infolist()]
temporary = target.with_suffix('.display.tmp.pptx')
with ZipFile(temporary, 'w', ZIP_DEFLATED) as out:
    for item, data in entries:
        if item.filename in slides:
            root = ET.fromstring(data)
            for blip in root.findall('.//a:blip', ns):
                if blip.find('a:grayscl', ns) is None:
                    ET.SubElement(blip, '{'+ns['a']+'}grayscl')
            data = ET.tostring(root, encoding='utf-8', xml_declaration=True)
        out.writestr(item, data)
temporary.replace(target)
