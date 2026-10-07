# -*- coding: utf-8 -*-
"""Probe 14: TRAIN_SEARCH_RESULT_LIST call sites + station data loader + live ScheduleView test."""
import re, json, requests
from http.cookiejar import CookieJar

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()

print('=== TRAIN_SEARCH_RESULT_LIST call sites (non-def) ===')
seen = set()
for m in re.finditer(r'TRAIN_SEARCH_RESULT_LIST', b):
    i = m.start()
    if b[i-6:i] in ('c.API.', '.API.') and 'url:' not in b[i:i+200]:
        pass
    ctx = b[max(0, i-700):i+300]
    if 'url:' in b[i:i+250]:
        continue
    key = i // 2000
    if key in seen:
        continue
    seen.add(key)
    print(f'--- @ {i} ---')
    print(ctx.replace('\n', ' '))
    print()

print('=== station loader fn ===')
m = re.search(r'\[Statio', b)
if m:
    i = m.start()
    print(b[max(0, i-100):i+2200])
