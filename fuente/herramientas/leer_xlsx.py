"""Lee un .xlsx sin dependencias y lo vuelca a JSON: {hoja: [[celdas]]}."""
import json, re, sys, zipfile
import xml.etree.ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
src, out = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(src)
shared = []
if 'xl/sharedStrings.xml' in z.namelist():
    for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', NS):
        shared.append(''.join(t.text or '' for t in si.iter('{%s}t' % NS['m'])))
wb = ET.fromstring(z.read('xl/workbook.xml'))
rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
target = {r.get('Id'): r.get('Target') for r in rels}
col = lambda ref: sum((ord(c) - 64) * 26 ** i for i, c in enumerate(reversed(re.match(r'[A-Z]+', ref).group())))
res = {}
for sh in wb.find('m:sheets', NS):
    path = 'xl/' + target[sh.get('{%s}id' % NS['r'])].lstrip('/').replace('xl/', '')
    root = ET.fromstring(z.read(path))
    rows = []
    for row in root.iter('{%s}row' % NS['m']):
        cells = {}
        for c in row.findall('m:c', NS):
            t, v = c.get('t'), c.find('m:v', NS)
            if t == 's' and v is not None: val = shared[int(v.text)]
            elif t == 'inlineStr': val = ''.join(x.text or '' for x in c.iter('{%s}t' % NS['m']))
            else: val = v.text if v is not None else None
            cells[col(c.get('r'))] = val
        if cells:
            rows.append([cells.get(i) for i in range(1, max(cells) + 1)])
    res[sh.get('name')] = rows
json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in res.items():
    print('=== HOJA', k, len(v), 'filas')
    for r in v[:6]: print(r)
