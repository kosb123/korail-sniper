# -*- coding: utf-8 -*-
"""SRT: fetch station list (selectStnCdInfo.do) and try schedule search (selectTrainScheduleList.do)."""
import requests, re, json
H = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
     'Accept':'*/*','Accept-Language':'ko-KR,ko;q=0.9,en;q=0.8',
     'Referer':'https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000',
     'Origin':'https://etk.srail.kr', 'X-Requested-With':'XMLHttpRequest'}
s = requests.Session(); s.headers.update(H)
s.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000', timeout=20)

# 1) station list
r1 = s.get('https://etk.srail.kr/hpg/hra/01/selectStnCdInfo.do', timeout=20)
print('selectStnCdInfo ->', r1.status_code, 'len', len(r1.text), 'ct', r1.headers.get('content-type'))
open(r'C:\Users\jun\projects\korail-sniper\srt_stncd.txt','w',encoding='utf-8').write(r1.text)
stns = re.findall(r'(\d{4})[\'",:\s]+([^\'",]+?)[\'",]', r1.text)
hits = [(c,n) for c,n in stns if any(k in n for k in ['평택지제','증평','수서','천안','세종','온양','오송','청주'])]
print('station hits:', hits)

# 2) schedule search — try GET first with guessed params (평택지제 0553? -> 증평). Try POST too.
dpt, arv = '0553', None
params = {'dptRsStnCd': dpt, 'arvRsStnCd': arv or '0000', 'dptDt': '20261008', 'dptTm': '', 'stlbTrnClsfCd':'', 'psgNum':'1', 'seatAttCd':'', 'isRequest':'N', 'srchDvNm':'PC'}
r2 = s.post('https://etk.srail.kr/hpg/hra/01/selectTrainScheduleList.do', data=params, timeout=25)
print('schedule search ->', r2.status_code, 'len', len(r2.text), 'ct', r2.headers.get('content-type'))
open(r'C:\Users\jun\projects\korail-sniper\srt_schedule_try.html','w',encoding='utf-8').write(r2.text)
print(r2.text[:600].replace('\n',' '))
