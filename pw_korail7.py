# -*- coding: utf-8 -*-
"""Korail: enter search page via main click, then full input recon (incl hidden)."""
import json
from playwright.sync_api import sync_playwright
EXE = r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=EXE, args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    pg = b.new_context(user_agent=UA, locale='ko-KR', viewport={'width':1920,'height':1040}).new_page()
    pg.goto('https://www.korail.com/ticket/main', wait_until='domcontentloaded', timeout=35000)
    pg.wait_for_timeout(4000)
    pg.click('.btn_lookup', timeout=10000)
    pg.wait_for_timeout(5000)
    print('url:', pg.url)
    fields = pg.evaluate('''() => Array.from(document.querySelectorAll('input, select')).map(e=>({id:e.id,name:e.name,type:e.type,ph:e.placeholder||'',val:(e.value||'').slice(0,25),cls:(e.className||'').toString().slice(0,50)}))''')
    print('ALL INPUTS:', len(fields))
    for f in fields: print(' ', json.dumps(f, ensure_ascii=False))
    # station picker area: find the two station name links and their container
    stn = pg.evaluate('''() => {
        const a = Array.from(document.querySelectorAll('a, span, div')).filter(e=>e.offsetParent!==null && (e.innerText||'').trim()==='서울')[0];
        if(!a) return 'no seoul el';
        let c = a; for(let i=0;i<4 && c.parentElement;i++) c = c.parentElement;
        return c.outerHTML.slice(0,5000);
    }''')
    print('STN AREA:'); print(stn)
    b.close()
