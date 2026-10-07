# -*- coding: utf-8 -*-
"""Probe 17: dump the API module (host + callApi impl)."""
import re

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()

i = b.find('TRAIN_SEARCH_RESULT_LIST')
# find module start: go back to 'function(t,e,n)'
start = b.rfind('function(t,e,n)', 0, i)
seg = b[start:start+14000]
# find the O function definition (callApi)
m = re.search(r'[,;]O=function', seg)
if m:
    print('callApi def found at module offset', m.start())
    print(seg[m.start():m.start()+4000])
else:
    # maybe O is assigned differently; print first 6000 chars of module
    print(seg[:6000])
open(OUT + r'\api_module.txt', 'w', encoding='utf-8').write(seg)
print('saved api_module.txt', len(seg))
