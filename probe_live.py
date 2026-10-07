# -*- coding: utf-8 -*-
"""Probe 15: fetch station_data.json, get codes, then live-test ScheduleView."""
import json, requests, datetime, sys

H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
s = requests.Session()
s.headers.update(H)

r = s.get('https://www.korail.com/public/st_info/station_data.json', timeout=20)
print('station_data.json:', r.status_code, len(r.text))
d = r.json()
stns = d.get('stns', {}).get('stn', [])
print('total stations:', len(stns))
print('sample:', json.dumps(stns[0], ensure_ascii=False))

want = ['평택지제', '증평', '천안아산', '오송', '서산', '당진', '용산', '서울', '수서', '청량리']
found = {}
for st in stns:
    if st.get('stn_nm') in want:
        found[st['stn_nm']] = st.get('stn_cd')
        print('FOUND:', st['stn_nm'], st.get('stn_cd'), json.dumps(st, ensure_ascii=False)[:200])
json.dump({k: st.get('stn_cd') for st in stns for k in [st.get('stn_nm')] if k}, open(r'C:\Users\jun\projects\korail-sniper\station_codes.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved station_codes.json')
print('wanted:', found)

# Live ScheduleView test
date = '20261008'
body = {
    'txtGoStart': '평택지제',
    'txtGoStartCode': found.get('평택지제', ''),
    'txtGoEnd': '증평',
    'txtGoEndCode': found.get('증평', ''),
    'txtGoAbrdDt': date,
    'txtGoHour': '180000',
    'txtComeAbrdDt': '',
    'txtComeHour': '',
    'txtTrnGpCd': '',
    'txtTrnGpCd1': '',
    'psrmClCd': '',
    'txtDturDvCd': '',
    'txtPsgFlg_1': 1,
    'txtPsgFlg_2': 0,
    'txtPsgFlg_3': 0,
    'txtPsgFlg_4': 0,
    'rtYn': 'N',
    'searchType': '',
}
url = 'https://www.korail.com/classes/com.korail.mobile.seatMovie.ScheduleView'
rr = s.post(url, json=body, headers={'Content-Type': 'application/json', 'Origin': 'https://www.korail.com', 'Referer': 'https://www.korail.com/ticket'}, timeout=25)
print('ScheduleView:', rr.status_code, len(rr.text))
print(rr.text[:3000])
open(r'C:\Users\jun\projects\korail-sniper\scheduleview_resp.json', 'w', encoding='utf-8').write(rr.text)
