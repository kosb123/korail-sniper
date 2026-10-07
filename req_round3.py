# -*- coding: utf-8 -*-
"""Round 3: legacy servlet schedule + SRAIL SRT schedule via pure requests."""
import requests, re
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

# --- 1) legacy KORAIL servlet ---
s = requests.Session(); s.headers.update({'User-Agent':UA,'Accept-Language':'ko-KR,ko;q=0.9,en;q=0.8'})
s.get('https://www.korail.com/ticket/main', timeout=30)
params = {'txtGoAbrdDt':'20261008','txtGoHour':'180000','txtGoStartCode':'0553','txtGoEndCode':'0071',
          'checkStnNm':'N','radJobId':'1','txtPsgCnt1':'1','txtTrnGpCd':'109'}
for url in ['https://www.korail.com/servlets/pr.pr21100.sw_pr21111_i1Svt',
            'http://www.korail.com/servlets/pr.pr21100.sw_pr21111_i1Svt']:
    try:
        r = s.get(url, params=params, timeout=40, allow_redirects=True)
        print(url, r.status_code, r.headers.get('content-type','')[:40], 'len', len(r.text), 'final:', r.url[:80])
        if r.status_code==200 and 'train' in r.text.lower():
            open('C:/Users/jun/projects/korail-sniper/legacy_sched.html','w',encoding='utf-8').write(r.text)
        print(r.text[:300].replace('\n',' '))
        break
    except Exception as e:
        print(url,'ERR',type(e).__name__, str(e)[:150])

# --- 2) SRT schedule ---
s2 = requests.Session(); s2.headers.update({'User-Agent':UA,'Accept-Language':'ko-KR,ko;q=0.9,en;q=0.8'})
try:
    r0 = s2.get('https://etk.srail.kr/hpg/hra/01/selectMapInfo.do', timeout=40)
    print('SRT mapInfo:', r0.status_code, 'len', len(r0.text), r0.headers.get('content-type','')[:30])
    # find stn codes for our stations in map info
    for nm in ['평택지제','천안아산','오송','증평','충주','대전']:
        m = re.findall(rf"onclick='[^']*'{re.escape(nm)}[^']*'([^']*)'", r0.text)
        m2 = re.findall(rf"'\d+'[^']{{0,40}}{re.escape(nm)}|{re.escape(nm)}[^']{{0,40}}'(\d+)'", r0.text)
        print(f'  SRT stn {nm}:', m[:2], m2[:2])
    body = {'dptRsStnCd':'','arvRsStnCd':'','stlbTrnClsfCd':'05','psgNum':'1','seatAttCd':'015','isRequest':'Y',
            'dptRsStnCdNm':'평택지제','arvRsStnCdNm':'증평','dptDt':'20261008','dptTm':'180000','chtnDvCd':'1',
            'psgInfoPerPrnb1':'1','psgInfoPerPrnb5':'0','psgInfoPerPrnb4':'0','psgInfoPerPrnb2':'0','psgInfoPerPrnb3':'0',
            'locSeatAttCd1':'000','rqSeatAttCd1':'015','trnGpCd':'300','dlayTnumAplFlg':'Y'}
    r1 = s2.post('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do', data=body, timeout=40)
    print('SRT schedule:', r1.status_code, 'len', len(r1.text), r1.headers.get('content-type','')[:30])
    open('C:/Users/jun/projects/korail-sniper/srt_sched.html','w',encoding='utf-8').write(r1.text)
    print(r1.text[:300].replace('\n',' '))
except Exception as e:
    print('SRT ERR', type(e).__name__, str(e)[:200])
