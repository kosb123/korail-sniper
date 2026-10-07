# -*- coding: utf-8 -*-
"""Korail: from /ticket/reservation, click into the train-search screen and capture network + form."""
import json
from playwright.sync_api import sync_playwright
EXE = r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
captured = []
def on_resp(resp):
    try:
        u = resp.url
        if any(s in u for s in ['cdn.korail.com','fonts','images','/img/','.css','.js','.png','.gif','.jpg','.svg','.woff']): return
        body=''
        try:
            ct=resp.headers.get('content-type','')
            if 'json' in ct or 'text' in ct or 'xml' in ct: body=resp.text()[:3000]
        except Exception: pass
        captured.append({'url':u,'status':resp.status,'ct':resp.headers.get('content-type',''),'body':body})
    except Exception: pass
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=EXE, args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    pg = b.new_context(user_agent=UA, locale='ko-KR', viewport={'width':1920,'height':1040}).new_page()
    pg.on('response', on_resp)
    pg.goto('https://www.korail.com/ticket/reservation', wait_until='domcontentloaded', timeout=35000)
    pg.wait_for_timeout(4000)
    # list clickable elements with text on this page
    els = pg.evaluate('''() => Array.from(document.querySelectorAll('a,button,[role=button],li,span,div')).filter(e=>e.offsetParent!==null && (e.innerText||'').trim()).map(e=>({tag:e.tagName, id:e.id, txt:(e.innerText||'').trim().replace(/\\n/g,' ').slice(0,30), href:e.getAttribute('href')||''})).filter(x=>x.txt)''')
    seen=set(); 
    for e in els:
        k=(e['tag'],e['txt'],e['href'])
        if k in seen: continue
        seen.add(k)
        print(f"{e['tag']:6} id={e['id'][:24]:24} href={e['href'][:40]:40} | {e['txt']}")
    b.close()
json.dump(captured, open(r'C:\Users\jun\projects\korail-sniper\korail_main_nav.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('captured:', len(captured))
