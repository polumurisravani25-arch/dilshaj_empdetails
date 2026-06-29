import re
import json
from pathlib import Path
path = Path('employees.json')
text = path.read_text(encoding='utf-8')
data = json.loads(text)
pattern1 = re.compile(r'https?://drive\.google\.com/open\?id=([A-Za-z0-9_-]+)')
pattern2 = re.compile(r'https?://drive\.google\.com/file/d/([A-Za-z0-9_-]+)/view(?:\?.*)?')
pattern3 = re.compile(r'https?://drive\.google\.com/file/d/([A-Za-z0-9_-]+)')
changed = False
for item in data:
    src = item.get('img_src', '')
    if not src:
        continue
    new = pattern1.sub(r'https://drive.google.com/uc?export=view&id=\1', src)
    new = pattern2.sub(r'https://drive.google.com/uc?export=view&id=\1', new)
    if new == src:
        m = pattern3.search(src)
        if m:
            new = f'https://drive.google.com/uc?export=view&id={m.group(1)}'
    if new != src:
        item['img_src'] = new
        changed = True
if changed:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Updated employees.json with direct Drive image URLs.')
else:
    print('No Drive URLs were changed.')
