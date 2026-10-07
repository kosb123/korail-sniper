# -*- coding: utf-8 -*-
"""Round 6: matrix test scdlQry to find the trnGpCd that returns trains.
WAF-free endpoint confirmed. Goal: get actual trainList for 0553->0071 on 20261008."""
import requests, json, time
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
s = requests.Session(); s.headers.update({'User-Agent': UA, 'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8'})
s.get('https://www.korail.com/ticket/main', timeout=30)

def tryq(tag, **over):
    v = dict(dptDt='20261008', dptRsStnCd='0553', arvRsStnCd='0071', trnGpCd='109', psrmClCd='1',
             dptTm='', trn_no='', seat_att_cd='', rsvSaleDvCd='T', Device='BH')
    v.update(over)
    r = s.post('https://www.korail.com/classes/com.korail.mobile.lmu.scdlQry.do', data=v, timeout=40)
    j = None
    try: j = r.json()
    except: pass
    has = (j or {}).get('trainList')
    n = len(has) if isinstance(has, list) else 0
    cd = (j or {}).get('h_msg_cd','?')
    print(f'{tag}: [{r.status_code}] {cd} trainList={n}')
    if n:
        open(f'C:/Users/jun/projects/korail-sniper/scdlqry_{tag}.json','w',encoding='utf-8').write(r.text)
        print('   first train:', json.dumps(has[0], ensure_ascii=False)[:300])
        return True
    return False

# 1) try without dptTm, various group codes
for g in ['101','102','103','104','105','109','110','980']:
    if tryq(f'gp{g}_noTm', trnGpCd=g, dptTm=''):
        break
    time.sleep(0.4)
print('----')
# 2) KTX general with no time
for g in ['101','109']:
    if tryq(f'gp{g}_empty', trnGpCd=g, dptTm=''):
        break
    time.sleep(0.4)
print('----')
# 3) rsvSaleDvCd variants (T=sale, others)
for sale in ['T','N','']:
    if tryq(f'sale{sale!r}', rsvSaleDvCd=sale):
        break
    time.sleep(0.4)
print('----')
# 4) try a known-busy route as control: 서울(0001)->부산(0020)
for g in ['101','109']:
    if tryq(f'ctrl_gp{g}', dptRsStnCd='0001', arvRsStnCd='0020', trnGpCd=g, dptTm=''):
        break
    time.sleep(0.4)
print('done')
