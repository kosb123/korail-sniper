# -*- coding: utf-8 -*-
"""Probe 7: callApi base URL, trnGpCd values, and station codes from official json."""
import re, json, requests

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}

print('=== official station json ===')
r = requests.get('https://www.korail.com/public/st_info/bt-www.json', timeout=15, headers=H)
print(r.status_code, len(r.text))
open(OUT + r'\st_info.json', 'w', encoding='utf-8').write(r.text)
try:
    d = json.loads(r.text)
    print('type:', type(d).__name__, 'len:', len(d) if hasattr(d, '__len__') else '')
    if isinstance(d, dict):
        ks = list(d.keys())[:10]
        print('keys sample:', ks)
    if isinstance(d, list):
        print('first:', json.dumps(d[0], ensure_ascii=False)[:300])
except Exception as e:
    print('json parse fail:', e, r.text[:200])

print()
print('=== trnGpCd literals ===')
for m in sorted(set(re.findall(r'trnGpCd\s*[:=]\s*"([^"]+)"', b)))[:30]:
    print(' ', m)
for m in sorted(set(re.findall(r'"([A-Z0-9]+)"\s*:\s*\{[^{}]{0,80}label:"(KTX[^"]*|SRT|ITX|ITX-Cheongsae|saemaeul|Nuriro|ITX-Maeul|MuBaeng|Subeo|Nuri)"', b)))[:30]:
    print('  map:', m)

print()
print('=== callApi definition ===')
m = re.search(r'function\s+callApi', b)
if m:
    i = m.start()
    print(b[i:i+1200])
else:
    m = re.search(r'callApi\s*[:=]', b)
    if m:
        i = m.start()
        print(b[max(0,i-200):i+1000])

print()
print('=== baseURL / prefix constants ===')
for m in sorted(set(re.findall(r'["\'](/[a-zA-Z0-9_\-/]*(?:ebiz|gateway|api)[a-zA-Z0-9_\-/]*)["\']', b)))[:40]:
    print(' ', m)
