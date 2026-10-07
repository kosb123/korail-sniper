# -*- coding: utf-8 -*-
"""requests test v2: ScheduleView with full real payload (incl limitStartDate, txtTrainNm)."""
import requests, time
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
s = requests.Session()
s.headers.update({'User-Agent': UA, 'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8'})
s.get('https://www.korail.com/ticket/main', timeout=30)
print('cookies:', list(s.cookies.keys()))

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
    ('txtPsgFlg_2','0'),
    ('rtYn','N'),
    ('txtGoAbrdDt','20261008'),
    ('txtGoHour','000000'),
    ('txtWkndUseFlg','Y'),
    ('txtGoStartCode','0001'),
    ('txtGoEndCode','0020'),
    ('txtMenuId','11'),
    ('limitStartDate','20261007'),
    ('txtTrainNm','전체'),
    ('txtSeatAttCd_4','015'),
    ('tkTripChgQryFlg','Y'),
    ('Device','BH'),
    ('Version','999999999'),
]
r = s.post('https://www.korail.com/classes/com.korail.mobile.seatMovie.ScheduleView',
           data=fields,
           headers={'Referer':'https://www.korail.com/ticket/search/list','Origin':'https://www.korail.com',
                    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}, timeout=40)
print('ScheduleView st:', r.status_code, 'ct:', r.headers.get('content-type'), 'len:', len(r.text))
open(r'C:\Users\jun\projects\korail-sniper\req_sv2_body.txt','w',encoding='utf-8').write(r.text)
print(r.text[:1500])
