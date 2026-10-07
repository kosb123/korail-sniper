# -*- coding: utf-8 -*-
"""Round 5: scdlQry with CORRECT field names (from bundle KTX-BUS payload)."""
import requests, json, time
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
s = requests.Session(); s.headers.update({'User-Agent': UA, 'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8'})
s.get('https://www.korail.com/ticket/main', timeout=30)

variants = [
  # KTX general (109)
  dict(dptDt='20261008', dptRsStnCd='0553', arvRsStnCd='0071', trnGpCd='109', psrmClCd='1',
       dptTm='180000', trn_no='', seat_att_cd='', rsvSaleDvCd='T', Device='BH'),
  # KTX-BUS (980) as in bundle
  dict(dptDt='20261008', dptRsStnCd='0553', arvRsStnCd='0071', trnGpCd='980', psrmClCd='1',
       dptTm='180000', trn_no='', seat_att_cd='', rsvSaleDvCd='T', Device='BH'),
  # variant with dptStnNm / no dptTm
  dict(dptDt='20261008', dptRsStnCd='0553', arvRsStnCd='0071', trnGpCd='109', psrmClCd='1',
       trn_no='', seat_att_cd='', rsvSaleDvCd='T'),
]
for i, v in enumerate(variants):
    r = s.post('https://www.korail.com/classes/com.korail.mobile.lmu.scdlQry.do', data=v, timeout=40)
    print(f'--- scdlQry v{i} [{r.status_code}] ---')
    print(r.text[:800].replace('\n',' '))
    if r.status_code==200 and 'trainList' in r.text and 'null' not in r.text[r.text.find('"trainList"'):r.text.find('"trainList"')+20]:
        open(f'C:/Users/jun/projects/korail-sniper/scdlqry_v{i}.json','w',encoding='utf-8').write(r.text)
        print('  *** SAVED trainList ***')
    time.sleep(0.6)
