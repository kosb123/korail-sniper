# -*- coding: utf-8 -*-
"""Probe 21: dp.helper.js WAF path rules + test all /classes/ endpoints raw."""
import re, requests

H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
     'Origin': 'https://www.korail.com', 'Referer': 'https://www.korail.com/ticket',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'Accept': 'application/json, text/plain, */*',
     'X-Requested-With': 'XMLHttpRequest'}
s = requests.Session()
s.get('https://www.korail.com/ticket', headers={'User-Agent': H['User-Agent']}, timeout=25)

paths = [
    ('/classes/com.korail.mobile.seatMovie.ScheduleView', 'POST', {'txtGoStart':'평택지제','txtGoStartCode':'0386','txtGoEnd':'증평','txtGoEndCode':'0040','txtGoAbrdDt':'20261008','txtGoHour':'180000','txtComeAbrdDt':'','txtComeHour':'','txtTrnGpCd':'','txtTrnGpCd1':'','psrmClCd':'','txtDturDvCd':'','txtPsgFlg_1':'1','txtPsgFlg_2':'0','txtPsgFlg_3':'0','txtPsgFlg_4':'0','rtYn':'N','searchType':''}),
    ('/classes/com.korail.mobile.research.mergeSeatsC.do', 'POST', {}),
    ('/classes/com.korail.mobile.trn.fresScar.do', 'POST', {}),
    ('/classes/com.korail.mobile.research.TrainResearch', 'POST', {}),
    ('/classes/com.korail.mobile.research.TResidualSeatsResearch.do', 'POST', {}),
    ('/ebizcross/getUUID.do', 'POST', {}),
]
for p, m, d in paths:
    r = s.post('https://www.korail.com'+p, data=d, headers=H, timeout=25)
    ct = r.headers.get('content-type','')
    body = r.text[:150].replace('\n',' ')
    print(f'{p} -> {r.status_code} {ct} | {body}')
    print()

# WAF path rules in dp.helper.js
t = open(r'C:\Users\jun\projects\korail-sniper\dp.helper.js', encoding='utf-8').read()
for m2 in re.finditer(r'classes|\.do|/dyna|path', t):
    i = m2.start()
    seg = t[max(0,i-80):i+80].replace('\n',' ')
    print('DP:', seg)
    print()
