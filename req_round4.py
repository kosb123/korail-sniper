# -*- coding: utf-8 -*-
"""Round 4: probe the global/foreigner portal APIs (likely WAF-free)."""
import requests, json
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
s = requests.Session(); s.headers.update({'User-Agent': UA, 'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8'})
r = s.get('https://www.korail.com/global/eng/main', timeout=30)
print('global main:', r.status_code, 'len', len(r.text))
open('C:/Users/jun/projects/korail-sniper/global_main.html','w',encoding='utf-8').write(r.text)

def probe(method, url, **kw):
    try:
        r = s.request(method, url, timeout=40, **kw)
        ct = r.headers.get('content-type','')[:40]
        print(f'{method} {url.split("korail.com")[-1][:70]} -> {r.status_code} {ct} len={len(r.text)}')
        return r
    except Exception as e:
        print(method, url, 'ERR', str(e)[:120]); return None

probe('GET', 'https://www.korail.com/ebizweb/global/stations')
probe('GET', 'https://www.korail.com/ebizweb/global/trains/time-table',
      params={'dptStnCode':'0553','arvStnCode':'0071','trnDt':'20261008','trnTime':'1800','trnClsfCd':'109'})
probe('POST', 'https://www.korail.com/ebizweb/global/trains/schedule',
      data={'dptStnCode':'0553','arvStnCode':'0071','trnDt':'20261008','trnTime':'1800','trnClsfCd':'109','psgCnt':'1','seatClsfCd':'1'})
probe('GET', 'https://www.korail.com/ebizweb/global/trains/fare',
      params={'dptStnCode':'0553','arvStnCode':'0071'})
probe('POST', 'https://www.korail.com/ebizweb/biz/train/schedule',
      data={'dptStnCode':'0553','arvStnCode':'0071','trnDt':'20261008'})
probe('GET', 'https://www.korail.com/global/eng/ticket', timeout=40)
