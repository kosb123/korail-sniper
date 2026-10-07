# -*- coding: utf-8 -*-
"""SRT: POST real schedule search — 평택지제(0553) -> 증평(0071), 2026-10-08, 1 adult."""
import requests, re
H = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'ko-KR,ko;q=0.9,en;q=0.8',
     'Referer':'https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000','Origin':'https://etk.srail.kr'}
s = requests.Session(); s.headers.update(H)
s.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000', timeout=20)
data = {
 'key':'','dptRsStnCd':'0553','arvRsStnCd':'0071','stlbTrnClsfCd':'05','psgNum':'1','seatAttCd':'','isRequest':'Y','srchDvNm':'PC',
 'dptDt':'20261008','dptTm':'','psgInfoPerPrnb1':'1','psgInfoPerPrnb2':'0','psgInfoPerPrnb3':'0','psgInfoPerPrnb4':'0','psgInfoPerPrnb5':'0',
 'locSeatAttCd1':'','rqSeatAttCd1':'','chtnDvCd':'1','trnGpCd':'109','dlayTnumAplFlgN':'N','dlayTnumAplFlg':'N'
}
r = s.post('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000', data=data, timeout=30)
print('search ->', r.status_code, 'len', len(r.text), 'ct', r.headers.get('content-type'))
open(r'C:\Users\jun\projects\korail-sniper\srt_result_1008.html','w',encoding='utf-8').write(r.text)
# extract train rows
rows = re.findall(r'trnNo[^>]*>(\d+)[^~]*', r.text)
# print any table-like train info
for m in re.finditer(r'(SRT-\d+|ITX\S*)\s*[\d:]{4,8}[^a-zA-Z]{0,40}[\d:]{4,8}', r.text):
    print('row:', m.group(0)[:80])
# seat avail keywords
for kw in ['可售','예약가능','매진','잔여','좌석','seat','noSeat','remn']:
    c = len(re.findall(kw, r.text))
    if c: print('kw', kw, c)
print(r.text[:300].replace('\n',' '))
