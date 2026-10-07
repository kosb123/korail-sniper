# -*- coding: utf-8 -*-
"""Probe 16: find the actual base host for callApi (.do endpoints)."""
import re

OUT = r'C:\Users\jun\projects\korail-sniper'
b = open(OUT + r'\korail_bundle.js', encoding='utf-8').read()

# The callApi function: search for 'classes/com.korail.mobile' combined with host selection
# Look for process.env / REACT_APP / axios.create
for m in list(re.finditer(r'axios\.create|REACT_APP_|process\.env', b))[:10]:
    i = m.start()
    print('@', i, ':', b[max(0, i-200):i+300].replace('\n', ' '))
    print()

# look for host constants near the API map
i = b.find('TRAIN_SEARCH_RESULT_LIST')
# the API map is at ~38835; the host config is probably near the top of that module
seg = b[30000:60000]
for m in re.finditer(r'https?://[^"\']+', seg):
    print('url in module:', m.group(0))

# search for 'mobile.korail' / 'm.korail' / 'api.korail' / 'ebiz' hosts anywhere
for m in sorted(set(re.findall(r'https?://[a-z0-9\.\-]*\.[a-z]{2,10}[^"\']{0,40}', b)))[:60]:
    print('H:', m)
