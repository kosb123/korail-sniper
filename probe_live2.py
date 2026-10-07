# -*- coding: utf-8 -*-
"""Probe 18: live ScheduleView with form-urlencoded (matching axios default)."""
import json, requests
from requests.cookies import RequestsCookieJar

H = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Origin': 'https://www.korail.com',
    'Referer': 'https://www.korail.com/ticket',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
}
s = requests.Session()
# warm up cookies
s.get('https://www.korail.com/ticket', headers={k: v for k, v in H.items() if k != 'Content-Type'}, timeout=25)
print('cookies after warmup:', s.cookies.get_dict())

data = {
    'txtGoStart': '평택지제',
    'txtGoStartCode': '0386',
    'txtGoEnd': '증평',
    'txtGoEndCode': '0040',
    'txtGoAbrdDt': '20261008',
    'txtGoHour': '180000',
    'txtComeAbrdDt': '',
    'txtComeHour': '',
    'txtTrnGpCd': '',
    'txtTrnGpCd1': '',
    'psrmClCd': '',
    'txtDturDvCd': '',
    'txtPsgFlg_1': '1',
    'txtPsgFlg_2': '0',
    'txtPsgFlg_3': '0',
    'txtPsgFlg_4': '0',
    'rtYn': 'N',
    'searchType': '',
}
for url in [
    'https://www.korail.com/classes/com.korail.mobile.seatMovie.ScheduleView',
]:
    r = s.post(url, data=data, headers=H, timeout=25)
    print(url, '->', r.status_code, len(r.text))
    print(r.text[:2500])
    open(r'C:\Users\jun\projects\korail-sniper\scheduleview_form.json', 'w', encoding='utf-8').write(r.text)
