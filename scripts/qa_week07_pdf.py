"""Geometry/text checks and readable four-slide QA sheets; no student data."""
from pathlib import Path
import json
import subprocess
import sys
import pdfplumber
from PIL import Image, ImageOps, ImageDraw

root = Path(__file__).resolve().parents[1]
week = int(sys.argv[1]) if len(sys.argv) > 1 else 7
if week not in (6, 7):
    raise ValueError('supported weeks: 6 or 7')
folder = root/f'output/validation/week{week:02}-pages-final'
folder.mkdir(parents=True, exist_ok=True)
source = root/'output/pdf'/('06_week6_sft_lora_reference.pdf' if week == 6 else '07_week7_model_adaptation_project.pdf')
doc = pdfplumber.open(source)
subprocess.run(['pdftoppm','-scale-to-x','1280','-scale-to-y','-1','-png',str(source),str(folder/'slide')],check=True)
issues=[]
for i,page in enumerate(doc.pages):
    content=page.extract_text() or ''
    if not content.strip(): issues.append({'page':i+1,'kind':'empty'})
    for word in page.extract_words():
        if word['x0'] < -1 or word['top'] < -1 or word['x1'] > page.width+1 or word['bottom'] > page.height+1:
            issues.append({'page':i+1,'kind':'outside','word':word['text']})
    if '\ufffd' in content: issues.append({'page':i+1,'kind':'replacement_glyph'})
for start in range(0,len(doc.pages),4):
    canvas=Image.new('RGB',(2560,1500),'#ffffff')
    draw=ImageDraw.Draw(canvas)
    for offset in range(min(4,len(doc.pages)-start)):
        image=Image.open(folder/f'slide-{start+offset+1:02}.png').convert('RGB')
        image=ImageOps.pad(image,(1280,720),color='#ffffff')
        x=(offset%2)*1280;y=(offset//2)*750
        canvas.paste(image,(x,y+24));draw.text((x+16,y+5),str(start+offset+1),fill='#000000')
    canvas.save(folder/f'qa-{start+1:02}-{min(start+4,len(doc.pages)):02}.jpg',quality=92)
receipt={'pages':len(doc.pages),'issues':issues,'visual_review':'See qa sheets and individual slide PNGs; automated checks do not prove visual quality.'}
(folder/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
print(receipt)
assert len(doc.pages)==(32 if week == 6 else 77) and not issues
