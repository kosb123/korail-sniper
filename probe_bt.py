# -*- coding: utf-8 -*-
"""Probe 8: BT stations + biz/train/schedule call shape + callApi impl."""
import re, json

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()
d = json.load(open(OUT + r'\st_info.json', encoding='utf-8'))
BT = d['BT']
print('BT type:', type(BT).__name__, 'len:', len(BT))
if isinstance(BT, list):
    print('sample:', json.dumps(BT[:3], ensure_ascii=False))
    for s in BT:
        nm = s.get('stn_nm', s.get('name', ''))
        cd = s.get('stn_cd', s.get('code', ''))
        if any(w in str(nm) for w in ['평택지제', '증평', '천안아산', '오송', '서산', '당진', '용산', '서울']):
            print('  match:', json.dumps(s, ensure_ascii=False)[:200])
elif isinstance(BT, dict):
    print('keys:', list(BT.keys())[:20])
    print(json.dumps(BT, ensure_ascii=False)[:800])

print()
print('=== biz/train/schedule contexts ===')
for m in re.finditer(r'biz/train/schedule', b):
    i = m.start()
    print('...%s...' % b[max(0, i-500):i+300].replace('\n', ' '))
    print()

print('=== biz/ticket/reserve contexts ===')
for m in list(re.finditer(r'biz/ticket/reserve', b))[:3]:
    i = m.start()
    print('...%s...' % b[max(0, i-400):i+400].replace('\n', ' '))
    print()

print('=== biz/login context ===')
for m in list(re.finditer(r'/biz/login["\']', b))[:2]:
    i = m.start()
    print('...%s...' % b[max(0, i-400):i+200].replace('\n', ' '))
    print()
