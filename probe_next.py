# -*- coding: utf-8 -*-
"""Probe 20: read __NEXT_DATA__ from ticket page + /dynaPath.do + dp.helper.js host logic."""
import re, requests, json

H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
s = requests.Session()
s.headers.update(H)

html = open(r'C:\Users\jun\projects\korail-sniper\ticket_page.html', encoding='utf-8').read()
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
if m:
    d = json.loads(m.group(1))
    print('NEXT_DATA keys:', list(d.keys()))
    print(json.dumps(d, ensure_ascii=False)[:3000])
    open(r'C:\Users\jun\projects\korail-sniper\next_data.json', 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))

print()
r = s.get('https://www.korail.com/dynaPath.do', timeout=20)
print('dynaPath.do ->', r.status_code, r.headers.get('content-type'))
print(r.text[:1500])
open(r'C:\Users\jun\projects\korail-sniper\dynaPath.txt', 'w', encoding='utf-8').write(r.text)

print()
r = s.get('https://cdn.korail.com/dyna/dp.helper.js', timeout=20)
print('dp.helper.js ->', r.status_code, len(r.text))
open(r'C:\Users\jun\projects\korail-sniper\dp.helper.js', 'w', encoding='utf-8').write(r.text)
print(r.text[:2000])
