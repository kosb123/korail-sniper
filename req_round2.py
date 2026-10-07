# -*- coding: utf-8 -*-
"""Round 2: residual seats (device variants), scdlQry with real station codes, mobile host."""
import requests, time, re, json
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
def sess(host):
    s = requests.Session()
    s.headers.update({'User-Agent': UA, 'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8'})
    s.get(host + '/ticket/main', timeout=30)
    return s

s = sess('https://www.korail.com')

# --- 1) TResidualSeatsResearch device variants ---
base = dict(runDt='20261008', trnNo='1101', trnClsfCd='201', trnGpCd='109',
            dptRsStnCd='0553', arvRsStnCd='0071', psrmClCd='1', seatAttCd='015',
            dptStnRunOrdr='1', arvStnRunOrdr='2', totPsgCnt='1', srcarNo='', langCode='ko', gdNo='')
for dev in ['BH','AD','IOS','BE','BH999999999']:
    f = dict(base); f['Device']=dev; f['Version']='999999999'
    r = s.post('https://www.korail.com/classes/com.korail.mobile.research.TResidualSeatsResearch.do',
               data=f, headers={'Referer':'https://www.korail.com/ticket/search/list','Origin':'https://www.korail.com'}, timeout=40)
    print('resid Device=',dev, r.status_code, r.text[:200].replace('\n',' '))
    time.sleep(0.5)

# --- 2) lmu.scdlQry (timetable) with real codes ---
for variant in [
    {'searchType':'GENERAL','txtGoStart':'평택지제','txtGoEnd':'증평','txtGoStartCode':'0553','txtGoEndCode':'0071',
     'txtGoAbrdDt':'20261008','txtTrnGpCd':'109','txtTrnClsfCd':'201','Device':'BH','Version':'999999999'},
    {'dptStnNm':'평택지제','arvStnNm':'증평','runDt':'20261008','Device':'BH'},
]:
    r = s.post('https://www.korail.com/classes/com.korail.mobile.lmu.scdlQry.do', data=variant, timeout=40)
    print('scdlQry', r.status_code, r.text[:250].replace('\n',' '))
    time.sleep(0.5)

# --- 3) trainsInfo.TrainSchedule with codes ---
v = dict(searchType='GENERAL', txtGoStart='평택지제', txtGoEnd='증평', txtTrnGpCd='109', radJobId='1',
         adjStnScdlOfrFlg='N', adjStnScdlOfrFlg2='N', srtCheckYn='N', ebizCrossCheck='N', txtPsgFlg_1='1',
         rtYn='N', txtGoAbrdDt='20261008', txtGoHour='180000', txtWkndUseFlg='Y',
         txtGoStartCode='0553', txtGoEndCode='0071', txtMenuId='11', txtSeatAttCd_4='015',
         tkTripChgQryFlg='Y', Device='BH', Version='999999999')
r = s.post('https://www.korail.com/classes/com.korail.mobile.trainsInfo.TrainSchedule', data=v, timeout=40)
print('TrainSchedule', r.status_code, r.text[:250].replace('\n',' '))
open('C:/Users/jun/projects/korail-sniper/req_trainsched2.txt','w',encoding='utf-8').write(r.text)
time.sleep(0.5)

# --- 4) direct ScheduleView again but with EXACT captured payload (no extras) ---
exact = [('searchType','GENERAL'),('txtGoStart','평택지제'),('txtGoEnd','증평'),('txtTrnGpCd','109'),
 ('radJobId','1'),('adjStnScdlOfrFlg','N'),('adjStnScdlOfrFlg2','N'),('srtCheckYn','N'),('ebizCrossCheck','N'),
 ('txtPsgFlg_1','1'),('rtYn','N'),('txtGoAbrdDt','20261008'),('txtGoHour','180000'),('txtWkndUseFlg','Y'),
 ('txtGoStartCode','0553'),('txtGoEndCode','0071'),('txtMenuId','11'),('txtSeatAttCd_4','015'),
 ('tkTripChgQryFlg','Y'),('Device','BH'),('Version','999999999')]
r = s.post('https://www.korail.com/classes/com.korail.mobile.seatMovie.ScheduleView', data=exact, timeout=40)
print('ScheduleView(exact payload)', r.status_code, 'len', len(r.text), r.text[:200].replace('\n',' '))

# --- 5) mobile host ---
for host in ['https://m.korail.com']:
    try:
        sm = sess(host)
        rr = sm.post(host+'/classes/com.korail.mobile.seatMovie.ScheduleView', data=exact, timeout=40)
        print(host, 'ScheduleView', rr.status_code, rr.headers.get('content-type','')[:30], rr.text[:200].replace('\n',' '))
    except Exception as e:
        print(host, 'ERR', e)
