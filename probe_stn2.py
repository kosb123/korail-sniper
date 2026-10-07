# -*- coding: utf-8 -*-
"""Probe 13: inspect the 52-station block + try live ScheduleView call."""
import re, json, requests

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()

# find the block of 52 stations: look for repeated code+English name patterns
m = re.search(r'0001.{0,40}Seoul', b)
print('seoul block @', m.start() if m else None)
if m:
    i = m.start()
    print(b[max(0, i-300):i+2500])
