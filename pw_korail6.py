# -*- coding: utf-8 -*-
"""Korail: full recon of /ticket/search/list form (all inputs incl hidden) + how station is stored."""
import json
from playwright.sync_api import sync_playwright
EXE = r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=EXE, args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    pg = b.new_context(user_agent=UA, locale='ko-KR', viewport={'width':1920,'height':1040}).new_page()
    pg.goto('https://www.korail.com/ticket/search/list', wait_until='domcontentloaded', timeout=35000)
    pg.wait_for_timeout(5000)
    print('url:', pg.url)
    fields = pg.evaluate('''() => Array.from(document.querySelectorAll('input, select')).map(e=>({id:e.id,name:e.name,type:e.type,ph:e.placeholder||'',val:(e.value||'').slice(0,25),data:(e.dataset||{}),cls:(e.className||'').toString().slice(0,50)}))''')
    print('ALL INPUTS:')
    for f in fields: print(' ', json.dumps(f, ensure_ascii=False))
    # station area HTML
    stn = pg.evaluate('''() => {
        const el = document.querySelector('[class*=depart], [class*=arriv], [class*=stn], [class*=station], [class*=search_form], [class*=searchForm], form');
        return el ? el.outerHTML.slice(0,4000) : 'none';
    }''')
    print('STN AREA HTML:'); print(stn)
    b.close()
