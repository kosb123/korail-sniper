# -*- coding: utf-8 -*-
"""Probe SRT: fetch the schedule search page, dump the form fields + station options + search JS."""
import requests, re
H = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'ko-KR,ko;q=0.9,en;q=0.8','Referer':'https://etk.srail.kr/main.do'}
s = requests.Session(); s.headers.update(H)
s.get('https://etk.srail.kr/main.do', timeout=20)  # warm cookies
r = s.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000', timeout=20)
print('schedule page ->', r.status_code, 'final', r.url[:90], 'len', len(r.text), 'ct', r.headers.get('content-type'))
open(r'C:\Users\jun\projects\korail-sniper\srt_schedule.html','w',encoding='utf-8').write(r.text)
# dump all form tags + their inputs
forms = re.findall(r'<form\b[^>]*>.*?</form>', r.text, re.S)
print('num forms:', len(forms))
for k,f in enumerate(forms):
    action = re.search(r'action="([^"]+)"', f)
    method = re.search(r'method="([^"]+)"', f)
    ids = re.findall(r'<(?:input|select|button)[^>]*\b(?:id|name|class)="([^"]*)"', f)
    print(f'--- form {k}: action={action.group(1) if action else None} method={method.group(1) if method else None}')
    print('   fields:', ids[:60])
# station select options
for m in re.finditer(r'<option value="([^"]+)"[^>]*>([^<]+)</option>', r.text):
    v, label = m.group(1), m.group(2).strip()
    if any(x in label for x in ['평택지제','증평','세종','천안']):
        print('STATION:', v, label)
