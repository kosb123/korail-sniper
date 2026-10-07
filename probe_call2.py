# -*- coding: utf-8 -*-
"""Probe 6: find API host config + TRAIN_RESEARCH / SEATSRESEARCH call sites & param shapes."""
import re

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()

# host candidates
print('=== host-ish strings ===')
for m in sorted(set(re.findall(r'["\'](https?://[a-z0-9\.\-]*korail[a-z0-9\.\-]*[^"\']*)["\']', b)))[:40]:
    print(' ', m)
for m in sorted(set(re.findall(r'(?:API_HOST|apiHost|API_URL|apiUrl|GATEWAY|gateway)[^,]{0,80}', b)))[:20]:
    print(' ', m)

# call sites: TRAIN_RESEARCH: usage (not the definition)
print()
print('=== call sites referencing TRAIN_RESEARCH / SEATSRESEARCH / TICKET_RESERVATION (non-def) ===')
for key in ['TRAIN_RESEARCH', 'SEATSRESEARCH', 'TICKET_RESERVATION', 'TRAIN_SEARCH_RESULT_LIST']:
    for m in re.finditer(key, b):
        i = m.start()
        ctx = b[max(0, i-250):i+450]
        if 'url:' in ctx and '{url:' in ctx[:260]:
            continue  # skip the definition line
        print(f'--- {key} @ {i} ---')
        print(ctx.replace('\n', ' '))
        print()
