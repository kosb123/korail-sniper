# -*- coding: utf-8 -*-
"""Round 7: scdlQry with REALISTIC times (previous tests used 00:00 = legitimately no trains).
Test 0553->0071 and control 0001->0020 across times and group codes."""
import requests, json, time
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
s = requests.Session(); s.headers.update({'User-Agent': UA, 'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
                                          'Referer': 'https://www.korail.com/ticket/search/list'})
s.get('https://www.korail.com/ticket/main', timeout=30)
s.get('https://www.korail.com/ticket/search/list', timeout=30)

def tryq(tag, dpt='0553', arv='0071', tm='090000', gp='101', **over):
    v = dict(dptDt='20261008', dptRsStnCd=dpt, arvRsStnCd=arv, trnGpCd=gp, psrmClCd='1',
             dptTm=tm, trn_no='', seat_att_cd='', rsvSaleDvCd='T', Device='BH')
    v.update(over)
    r = s.post('https://www.korail.com/classes/com.korail.mobile.lmu.scdlQry.do', data=v, timeout=40)
    try: j = r.json()
    except: j = None
    tl = (j or {}).get('trainList')
    n = len(tl) if isinstance(tl, list) else 0
    cd = (j or {}).get('h_msg_cd','?')
    print(f'{tag}: [{r.status_code}] {cd} trainList={n}')
    if n:
        open(f'C:/Users/jun/projects/korail-sniper/scdlqry_OK_{tag}.json','w',encoding='utf-8').write(r.text)
        print('   sample:', json.dumps(tl[0], ensure_ascii=False)[:400])
        return True
    return False

# realistic times
for tm in ['090000','100000','120000','180000']:
    if tryq(f'0553-0071_{tm}', tm=tm):
        print('   *** HIT ***'); break
    time.sleep(0.5)
print('---- control route ----')
for tm in ['090000','120000']:
    for gp in ['101','109']:
        if tryq(f'0001-0020_{tm}_{gp}', dpt='0001', arv='0020', tm=tm, gp=gp):
            print('   *** CONTROL HIT ***'); break
    time.sleep(0.5)
print('done')
