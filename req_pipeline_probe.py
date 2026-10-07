# -*- coding: utf-8 -*-
"""requests pipeline probe: stations, alternative schedule endpoints, residual-seat API."""
import requests, json, time
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
s = requests.Session()
s.headers.update({'User-Agent': UA, 'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8'})
s.get('https://www.korail.com/ticket/main', timeout=30)

def show(label, r):
    ct = r.headers.get('content-type','')
    js = r.text.lstrip()[:1] in '{['
    print(f'--- {label}: st={r.status_code} ct={ct[:40]} len={len(r.text)} json={js}')
    print(r.text[:600].replace('\n',' '))
    print()

# 1) station codes
try:
    r = s.get('https://www.korail.com/com/stationCodeCenter.do', timeout=30)
    show('stationCodeCenter', r)
    open(r'C:\Users\jun\projects\korail-sniper\stations.json','w',encoding='utf-8').write(r.text)
except Exception as e: print('stations err', e)

# 2) trainsInfo.TrainSchedule (alt schedule source) with user's route
fields = [
    ('searchType','GENERAL'),('txtGoStart','평택지제'),('txtGoEnd','증평'),
    ('txtTrnGpCd','109'),('radJobId','1'),('adjStnScdlOfrFlg','N'),('adjStnScdlOfrFlg2','N'),
    ('srtCheckYn','N'),('ebizCrossCheck','N'),('txtPsgFlg_1','1'),('rtYn','N'),
    ('txtGoAbrdDt','20261008'),('txtGoHour','000000'),('txtWkndUseFlg','Y'),
    ('txtGoStartCode',''),('txtGoEndCode',''),('txtMenuId','11'),
    ('limitStartDate','20261007'),('txtTrainNm','전체'),('txtSeatAttCd_4','015'),
    ('tkTripChgQryFlg','Y'),('Device','BH'),('Version','999999999'),
]
try:
    r = s.post('https://www.korail.com/classes/com.korail.mobile.trainsInfo.TrainSchedule', data=fields,
               headers={'Referer':'https://www.korail.com/ticket/search/list'}, timeout=40)
    show('trainsInfo.TrainSchedule', r)
    open(r'C:\Users\jun\projects\korail-sniper\req_trainsched_body.txt','w',encoding='utf-8').write(r.text)
except Exception as e: print('trainsched err', e)
time.sleep(1)

# 3) lmu.scdlQry.do (timetable)
try:
    r = s.post('https://www.korail.com/classes/com.korail.mobile.lmu.scdlQry.do', data=fields,
               headers={'Referer':'https://www.korail.com/ticket/search/list'}, timeout=40)
    show('lmu.scdlQry', r)
except Exception as e: print('scdlQry err', e)
time.sleep(1)

# 4) TResidualSeatsResearch with guessed trn (expect validation error that tells required fields)
rfields = [('runDt','20261008'),('trnNo','1101'),('trnClsfCd','201'),('trnGpCd','109'),
           ('dptRsStnCd',''),('arvRsStnCd',''),('psrmClCd','1'),('seatAttCd','015'),
           ('dptStnRunOrdr','1'),('arvStnRunOrdr','2'),('totPsgCnt','1'),('srcarNo',''),
           ('langCode','ko'),('gdNo','')]
try:
    r = s.post('https://www.korail.com/classes/com.korail.mobile.research.TResidualSeatsResearch.do',
               data=rfields, headers={'Referer':'https://www.korail.com/ticket/search/list'}, timeout=40)
    show('TResidualSeatsResearch', r)
except Exception as e: print('resid err', e)
