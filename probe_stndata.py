# -*- coding: utf-8 -*-
"""Probe 12: find the station list data source (codes for every station)."""
import re

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()

# Look for big station arrays: patterns like "stn_nm":"평택지제" with stn_cd
pat = re.compile(r'\{[^{}]*"stn_nm":"[^"]*평택지제[^{}]*\}')
for m in pat.finditer(b):
    print('CTX:', m.group(0)[:400])
    print()

# find where the 52-station list lives: search for '0386' etc? Instead: find all {stn_nm:"..",stn_chn_nm..,stn_cd:"NNNN"} objects and print ALL of them (we saw 52).
pairs = re.findall(r'"stn_nm":"((?:[^"\\]|\\.)*?)"[^}]*?"stn_cd":"(\d+)"', b)
print('pairs:', len(pairs))
for n, c in sorted(set(pairs)):
    print(c, n)

# also search for a separate list with jeongpyeong
for kw in ['jeongpyeong', 'jeongpyeong']:
    for m in list(re.finditer(kw, b))[:6]:
        i = m.start()
        print(f'--- {kw} @ {i} ---')
        print(b[max(0, i-150):i+150].replace('\n', ' '))
        print()

# find station json fetch urls
for m in sorted(set(re.findall(r'["\']([^"\']*(?:stn|stn|station|stn|stn|stn)[^"\']*\.(?:json|js|txt|xml))["\']', b, re.I)))[:30]:
    print('file:', m)
for m in list(re.finditer(r'stationList\s*[:=]', b))[:6]:
    i = m.start()
    print('SL:', b[max(0, i-200):i+300].replace('\n', ' '))
    print()
