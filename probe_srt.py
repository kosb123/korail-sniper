# -*- coding: utf-8 -*-
"""Probe SRT: booking system at etk.srail.kr — find the seat/schedule API."""
import requests, re
H = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'ko-KR,ko;q=0.9,en;q=0.8'}
s = requests.Session(); s.headers.update(H)
for url in ['https://etk.srail.kr/','https://etk.srail.kr/resv','https://etk.srail.kr/seatSearch.do']:
    try:
        r = s.get(url, timeout=20, allow_redirects=True)
        print(url, '->', r.status_code, 'final', r.url[:90], 'len', len(r.text), 'ct', r.headers.get('content-type'))
        print('  set-cookie:', (r.headers.get('set-cookie') or '')[:150])
        # capture script srcs
        for m in re.findall(r'<script[^>]*src="([^"]+)"', r.text)[:25]:
            print('   script:', m)
        for m in re.findall(r'<form[^>]*action="([^"]+)"', r.text)[:10]:
            print('   form action:', m)
        if r.status_code==200 and len(r.text)>500:
            open(r'C:\Users\jun\projects\korail-sniper\srt_page_'+re.sub(r'\W','_',url).strip('_')+'.html','w',encoding='utf-8').write(r.text)
    except Exception as e:
        print(url, 'ERR', type(e).__name__, str(e)[:150])
