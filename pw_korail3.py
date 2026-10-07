# -*- coding: utf-8 -*-
"""Korail: open /ticket/main, find search form, capture network."""
import json
from playwright.sync_api import sync_playwright
EXE = r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=EXE, args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    pg = b.new_context(user_agent=UA, locale='ko-KR', viewport={'width':1920,'height':1040}).new_page()
    pg.goto('https://www.korail.com/ticket/main', wait_until='domcontentloaded', timeout=35000)
    pg.wait_for_timeout(5000)
    print('url:', pg.url, '| title:', pg.title())
    # all visible inputs/selects/buttons with labels
    fields = pg.evaluate('''() => Array.from(document.querySelectorAll('input, select, button, [role=tab], .btn, a.btn')).filter(e=>e.offsetParent!==null).map(e=>({id:e.id,name:e.name,type:e.type||'',tag:e.tagName,ph:e.placeholder||'',val:(e.value||'').slice(0,20),txt:(e.innerText||'').trim().replace(/\\n/g,' ').slice(0,25),cls:(e.className||'').toString().slice(0,40)}))''')
    print('FIELDS:', len(fields))
    for f in fields: print(' ', f)
    # visible links with text containing 조회/검색
    links = pg.evaluate('''() => Array.from(document.querySelectorAll('a,button')).filter(e=>e.offsetParent!==null && (e.innerText||'').trim()).map(e=>({txt:(e.innerText||'').trim().replace(/\\n/g,' ').slice(0,40), href:e.getAttribute('href')||'', id:e.id})).filter(x=>/조회|검색|예매|열차|일반/.test(x.txt))''')
    print('LINKS:')
    for l in links: print(' ', l)
    body = pg.evaluate('() => document.body.innerText')
    open(r'C:\Users\jun\projects\korail-sniper\korail_main_body.txt','w',encoding='utf-8').write(body)
    print('body head:', body[:800].replace('\n',' | '))
    b.close()
