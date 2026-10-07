# -*- coding: utf-8 -*-
"""Probe: fetch korail + SR home pages, save HTML, print links/scripts of interest."""
import re, requests, sys

H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
     'Accept-Language': 'ko-KR,ko;q=0.9'}

def grab(name, url):
    try:
        r = requests.get(url, timeout=15, headers=H, allow_redirects=True)
        p = rf'C:\Users\jun\projects\korail-sniper\{name}.html'
        open(p, 'w', encoding='utf-8').write(r.text)
        print(f'{name}: {r.status_code} {r.url} {len(r.text)} bytes')
        return r.text
    except Exception as e:
        print(f'{name}: FAIL {type(e).__name__} {e}')
        return ''

t1 = grab('korail_ticket', 'https://www.korail.com/ticket/')
t2 = grab('sr_home', 'https://etk.srail.kr/')

for label, txt in (('korail', t1), ('sr', t2)):
    print(f'=== {label} links ===')
    for m in sorted(set(re.findall(r'href="([^"]+)"', txt))):
        print(' ', m)
    print(f'--- {label} scripts ---')
    for m in sorted(set(re.findall(r'src="([^"]+\.js[^"]*)"', txt)))[:30]:
        print(' ', m)
    print(f'--- {label} title/meta ---')
    for m in re.findall(r'<title>(.*?)</title>', txt, re.S):
        print('  TITLE:', m.strip()[:120])
