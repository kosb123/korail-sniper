# -*- coding: utf-8 -*-
"""Probe 10: TRAIN_SEARCH_RESULT_LIST full def + axios base + station list source."""
import re

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()

print('=== TRAIN_SEARCH_RESULT_LIST def ===')
i = b.find('TRAIN_SEARCH_RESULT_LIST')
while i != -1:
    seg = b[i:i+220]
    if 'url:' in seg or 'URL' in seg.upper()[:60]:
        print('@', i, ':', seg)
    i = b.find('TRAIN_SEARCH_RESULT_LIST', i + 1)

print()
print('=== SCHEDULE_VIEW def (context) ===')
i = b.find('SCHEDULE_VIEW')
print('@', i, ':', b[max(0, i-100):i+400])

print()
print('=== axios create / baseURL ===')
for m in list(re.finditer(r'baseURL', b))[:8]:
    i = m.start()
    print('@', i, ':', b[max(0, i-300):i+120].replace('\n', ' '))
    print()

print('=== station list fetch (recoverStationData / getStationList) ===')
for kw in ['recoverStationData', 'STATION_INFO', 'station/list', 'st_list', 'STN_LIST']:
    for m in list(re.finditer(kw, b))[:3]:
        i = m.start()
        print(f'--- {kw} @ {i} ---')
        print(b[max(0, i-250):i+400].replace('\n', ' '))
        print()
