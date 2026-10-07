# -*- coding: utf-8 -*-
"""Probe 11: SEATSRESEARCH (TResidualSeatsResearch) call sites + params."""
import re

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()

print('=== SEATSRESEARCH call sites (non-def) ===')
seen = set()
for m in re.finditer(r'SEATSRESEARCH', b):
    i = m.start()
    if 'url:' in b[i:i+200]:
        continue
    ctx = b[max(0, i-900):i+500]
    key = i // 1000
    if key in seen:
        continue
    seen.add(key)
    print(f'--- @ {i} ---')
    print(ctx.replace('\n', ' '))
    print()

print('=== BUSSEATSRESEARCH call sites (non-def) ===')
seen = set()
for m in re.finditer(r'BUSSEATSRESEARCH', b):
    i = m.start()
    if 'url:' in b[i:i+200]:
        continue
    ctx = b[max(0, i-500):i+300]
    key = i // 1000
    if key in seen:
        continue
    seen.add(key)
    print(f'--- @ {i} ---')
    print(ctx.replace('\n', ' '))
    print()
