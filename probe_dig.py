# -*- coding: utf-8 -*-
"""Probe 2: dig korail SPA bundle for API paths; fetch SR schedule form + JS for ajax endpoints."""
import re, requests

H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
     'Accept-Language': 'ko-KR,ko;q=0.9'}
OUT = r'C:\Users\jun\projects\korail-sniper'

# 1) korail SPA bundle
r = requests.get('https://cdn.korail.com/bundle/bundle.5b79b7a7ab4cbca53b24.js?v=1.0.221', timeout=20, headers=H)
print('bundle:', r.status_code, len(r.text))
open(OUT + r'\korail_bundle.js', 'w', encoding='utf-8').write(r.text)
paths = sorted(set(re.findall(r'["\'](/(?:ticket|tickets|api|resv|booking|search)[^"\'\\]*)["\']', r.text)))
print('--- korail candidate paths (first 80) ---')
for p in paths[:80]:
    print(' ', p)

# 2) SR schedule inquiry form
r2 = requests.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000', timeout=20, headers=H)
open(OUT + r'\srt_schedule.html', 'w', encoding='utf-8').write(r2.text)
print('sr schedule:', r2.status_code, len(r2.text))
m = re.findall(r'<script[^>]*>(.*?)</script>', r2.text, re.S)
for s in m:
    if re.search(r'\.(do|action|ajax|url)', s, re.I):
        print('--- SR inline JS with endpoints ---')
        print(s[:4000])
        break

# 3) SR common/navi js
for js in ['https://etk.srail.kr/js/Common.js', 'https://etk.srail.kr/js/Navi.js']:
    r3 = requests.get(js, timeout=20, headers=H)
    name = js.split('/')[-1]
    open(OUT + rf'\srt_{name}', 'w', encoding='utf-8').write(r3.text)
    hits = sorted(set(re.findall(r'["\']([^"\']*\.do[^"\']*)["\']', r3.text)))
    print(f'--- srt {name} ({r3.status_code}, {len(r3.text)}b) endpoints ---')
    for h in hits[:40]:
        print(' ', h)
