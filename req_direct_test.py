# -*- coding: utf-8 -*-
"""Pure-requests test: no browser at all. GET main for cookies, then POST /classes/ ScheduleView directly."""
import requests, time
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
s = requests.Session()
s.headers.update({'User-Agent': UA, 'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8'})
r1 = s.get('https://www.korail.com/ticket/main', timeout=30)
print('main:', r1.status_code, 'cookies:', list(s.cookies.keys()))

fields = [
    ('searchType','GENERAL'),
    ('txtGoStart','서울'),
    ('txtGoEnd','부산'),
    ('txtTrnGpCd','109'),
    ('radJobId','1'),
    ('adjStnScdlOfrFlg','N'),
    ('adjStnScdlOfrFlg2','N'),
    ('srtCheckYn','N'),
    ('ebizCrossCheck','N'),
    ('txtPsgFlg_1','1'),
    ('rtYn','N'),
    ('txtGoAbrdDt','20261008'),
    ('txtGoHour','000000'),
    ('txtWkndUseFlg','Y'),
    ('txtGoStartCode','0001'),
    ('txtGoEndCode','0020'),
    ('txtMenuId','11'),
    ('txtSeatAttCd_4','015'),
    ('tkTripChgQryFlg','Y'),
    ('Device','BH'),
    ('Version','999999999'),
]
for url in [
    'https://www.korail.com/classes/com.korail.mobile.seatMovie.ScheduleView',
    'https://www.korail.com/classes/com.korail.mobile.research.TrainResearch',
]:
    try:
        r = s.post(url, data=fields, headers={'Referer':'https://www.korail.com/ticket/search/list','Origin':'https://www.korail.com'}, timeout=30)
        ct = r.headers.get('content-type','')
        body = r.text
        isjson = body.lstrip()[:1] in '{['
        print(url)
        print('  st:', r.status_code, 'ct:', ct, 'len:', len(body), 'json:', isjson)
        print('  body[:300]:', body[:300].replace('\n',' '))
    except Exception as e:
        print(url, 'ERR', e)
    time.sleep(1)
