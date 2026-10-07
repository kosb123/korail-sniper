# -*- coding: utf-8 -*-
"""Probe 22: does the mobile site m.korail.com expose the seat API WITHOUT the WAF?"""
import requests
H = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
     'Accept':'application/json, text/plain, */*', 'X-Requested-With':'XMLHttpRequest'}
s = requests.Session()
for base in ['https://m.korail.com']:
    try:
        r = s.get(base+'/', headers=H, timeout=20, allow_redirects=True)
        print(base, 'GET / ->', r.status_code, 'final', r.url[:80], 'len', len(r.text), 'ct', r.headers.get('content-type'))
        print('  set-cookie:', r.headers.get('set-cookie'))
        # try the mobile seat schedule API
        p = base + '/classes/com.korail.mobile.research.mergeSeatsC.do'
        data = {'txtGoStart':'평택지제','txtGoStartCode':'0386','txtGoEnd':'증평','txtGoEndCode':'0040',
                'txtGoAbrdDt':'20261008','txtGoHour':'180000','txtComeAbrdDt':'','txtComeHour':'',
                'txtTrnGpCd':'','psrmClCd':'','txtPsgFlg_1':'1','txtPsgFlg_2':'0','rtYn':'N','searchType':''}
        r2 = s.post(p, data=data, headers=H, timeout=20)
        print('  POST', p, '->', r2.status_code, 'len', len(r2.text))
        print('  body:', r2.text[:500])
        open(r'C:\Users\jun\projects\korail-sniper\mobile_api.txt','w',encoding='utf-8').write(r2.text)
    except Exception as e:
        print(base, 'ERR', type(e).__name__, str(e)[:200])
