# -*- coding: utf-8 -*-
"""Test SRT (etk.srail.kr) schedule list POST via requests.
Route: 평택지제(0553) -> 증평(0071), date 20261008. Form fields captured from live page."""
import requests, re, json, time
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
s = requests.Session(); s.headers.update({'User-Agent': UA, 'Accept-Language': 'ko-KR,ko;q=0.9'})
# warm: load form page for cookies
r0 = s.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000', timeout=40)
print('form page:', r0.status_code, 'len', len(r0.text), 'cookies:', list(s.cookies.keys()))

def post(tag, **over):
    d = dict(key='857', dptRsStnCd='0553', arvRsStnCd='0071', stlbTrnClsfCd='05', psgNum='1',
             seatAttCd='', isRequest='Y', srchDvNm='', dptRsStnCdNm='평택지제', arvRsStnCdNm='증평',
             chtnDvCd='1', trnGpCd='109', dlayTnumAplFlg='N', prvTms='100000',
             dptDt='20261008', dptTm='')
    d.update(over)
    r = s.post('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK01011000', data=d,
               headers={'Referer': 'https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000',
                        'Origin': 'https://etk.srail.kr'}, timeout=60)
    t = r.text
    # heuristics
    no = '열차가 없습니다' in t or '조회 결과' in t
    trn = re.findall(r'\d{3,4}\s*[A-Z]?|SRT|trnNo', t)
    print(f'--- {tag}: [{r.status_code}] len={len(t)} noResult={no}')
    # find a result table / key markers
    for kw in ['sch_result','result_list','trnNo','열차','평택지제','증평','잔여','left_seat','h_trn_no','schList','noData','없습니다']:
        i = t.find(kw)
        if i > 0:
            print(f'   kw[{kw}] @ {i}:', t[max(0,i-80):i+160].replace('\n',' ').replace('\t','')[:230])
    open(f'C:/Users/jun/projects/korail-sniper/srt_post_{tag}.html','w',encoding='utf-8').write(t)
    time.sleep(0.5)

post('v0_emptytm')
post('v1_tm090000', dptTm='090000')
post('v2_tmgp100', trnGpCd='100')
post('v3_direct0', chtnDvCd='0')
