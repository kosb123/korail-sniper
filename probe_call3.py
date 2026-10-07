# -*- coding: utf-8 -*-
"""Probe 9: callApi def, station list source, search state construction."""
import re

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()

print('=== callApi def ===')
for m in list(re.finditer(r'callApi', b))[:6]:
    i = m.start()
    print('...%s...' % b[max(0, i-300):i+500].replace('\n', ' '))
    print()

print('=== StationInfo-ish endpoints ===')
for m in sorted(set(re.findall(r'["\']([^"\']*[Ss]tation[^"\']*)["\']', b)))[:30]:
    print(' ', m)

print()
print('=== txtGoStart construction contexts (first 3) ===')
for m in list(re.finditer(r'txtGoStart\s*:', b))[:3]:
    i = m.start()
    print('...%s...' % b[max(0, i-600):i+400].replace('\n', ' '))
    print()

print('=== station list data (0515 Suseo style codes) ===')
for m in sorted(set(re.findall(r'"(\d{4})"\s*:\s*"?([^",}]{2,20})"?', b)))[:40]:
    pass
# Look for a station array with ko names
i = b.find('평택지제')
print('평택지제 found at:', i)
for m in list(re.finditer('평택지제', b))[:5]:
    i = m.start()
    print('...%s...' % b[max(0, i-200):i+200].replace('\n', ' '))
    print()
i = b.find('증평')
print('증평 found at:', i)
for m in list(re.finditer('증평', b))[:5]:
    i = m.start()
    print('...%s...' % b[max(0, i-200):i+200].replace('\n', ' '))
    print()
