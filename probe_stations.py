# -*- coding: utf-8 -*-
"""Probe 4: find SPA axios/baseURL + station codes for Pyeongtaek-Jijang & Jungpyeong."""
import re, json

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()

# station entries embedded in bundle: {stn_nm, stn_chn_nm, stn_jpn_nm, stn_cd}
stns = re.findall(r'\{stn_nm:"([^"]+)",stn_chn_nm:"[^"]*",stn_jpn_nm:"[^"]*",stn_cd:"(\d+)"[^}]*\}', b)
print(f'stations found: {len(stns)}')
want = ['평택지제', '증평', '천안아산', '오송', '용산', '서산', '당진']
for name, cd in stns:
    if any(w in name for w in want):
        print(f'  {name} = {cd}')

# axios baseURL / fetch endpoints
print()
print('=== baseURL-ish ===')
for m in sorted(set(re.findall(r'baseURL\s*[:=]\s*["\']([^"\']+)["\']', b)))[:20]:
    print(' ', m)
print()
print('=== url: strings with /api or v1 or v2 ===')
for m in sorted(set(re.findall(r'["\']((?:/api/|/v[0-9]/)[^"\']{3,80})["\']', b)))[:80]:
    print(' ', m)
print()
print('=== .do endpoints containing research/reserve/trn/stn ===')
pats = sorted(set(re.findall(r'["\'](/classes/com\.korail\.mobile\.[^"\']+)["\']', b)))
for p in pats:
    if re.search(r'research|reserv|trn|stn|trns|schdul|schdul|seat|list', p):
        print(' ', p)
