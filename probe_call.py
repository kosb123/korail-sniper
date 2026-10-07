# -*- coding: utf-8 -*-
"""Probe 5: dump the 52 stations, and find how TResidualSeatsResearch / TrainResearch are called."""
import re

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()

stns = re.findall(r'\{stn_nm:"((?:[^"\\]|\\.)*?)",stn_chn_nm:"(?:[^"\\]|\\.)*?",stn_jpn_nm:"(?:[^"\\]|\\.)*?",stn_cd:"(\d+)"[^}]*\}', b)
print(f'stations: {len(stns)}')
for n, c in stns:
    print(f'  {c} {n}')

print()
for kw in ['TResidualSeatsResearch', 'TrainResearch', 'mergeSeatsC']:
    for m in re.finditer(re.escape(kw), b):
        i = m.start()
        print(f'--- {kw} @ {i} ---')
        print(b[max(0, i-700):i+300].replace('\n', ' '))
        print()
        break  # first occurrence only
