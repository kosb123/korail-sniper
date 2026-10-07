# -*- coding: utf-8 -*-
"""Probe 3: extract real API endpoints from korail bundle + SR schedule page JS."""
import re

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()

print('=== korail bundle: http api urls ===')
for m in sorted(set(re.findall(r'https?:\\?/\\?/[a-zA-Z0-9\.\-/:%_]*?(?:api|ticket|resv|search|schedule|train)[a-zA-Z0-9\.\-/:%_]*', b)))[:100]:
    print(' ', m.replace('\\/', '/'))

print()
print('=== korail bundle: fetch/ajax-ish snippets (first 60) ===')
seen = set()
for m in re.finditer(r'["\']((?:/|https?://)[^"\']{5,120}\.(?:do|json|api|graphql)[^"\']*)["\']', b):
    s = m.group(1)
    if s not in seen:
        seen.add(s)
        print(' ', s)
    if len(seen) >= 60:
        break

# search for key words in context
print()
print('=== keyword contexts (korail) ===')
for kw in ['seatSearch', 'trainSearch', 'canceled', 'cancels', 'reservationSearch', 'searchTrains', 'getSchedule', 'seatInfo', 'available']:
    idxs = [m.start() for m in re.finditer(kw, b)][:3]
    for i in idxs:
        print(f'  [{kw}] ...{b[max(0,i-120):i+120]}...'.replace('\\n',' '))
    if not idxs:
        print(f'  [{kw}] (none)')

# SR schedule page: all script srcs + any .do references
print()
print('=== SR schedule page script srcs ===')
s = open(OUT + r'\srt_schedule.html', encoding='utf-8').read()
for m in sorted(set(re.findall(r'<script[^>]+src="([^"]+)"', s))):
    print(' ', m)
print()
print('=== SR schedule page: .do/.action endpoints in inline JS ===')
for m in sorted(set(re.findall(r'["\']([^"\']*?(?:\.do|\.action|/hpg/|/sss/)[^"\']*)["\']', s))):
    print(' ', m)
