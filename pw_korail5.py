# -*- coding: utf-8 -*-
"""Korail: recon the station picker modal structure."""
import json
from playwright.sync_api import sync_playwright
EXE = r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=EXE, args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    pg = b.new_context(user_agent=UA, locale='ko-KR', viewport={'width':1920,'height':1040}).new_page()
    pg.goto('https://www.korail.com/ticket/main', wait_until='domcontentloaded', timeout=35000)
    pg.wait_for_timeout(4000)
    # click the departure station link (출발역)
    pg.evaluate('''() => {
        const links = Array.from(document.querySelectorAll('a, span, div, button')).filter(e=>e.offsetParent!==null && /출발역/.test((e.innerText||'').trim().slice(0,10)));
        console.log('cands:', links.length);
        if (links.length) links[links.length-1].click();
        return links.length;
    }''')
    pg.wait_for_timeout(2500)
    # dump modal
    modal = pg.evaluate('''() => {
        const m = document.querySelector('.modal, .modal__wrap, [class*=modal], [class*=popup], [class*=layer], [class*=drawer], [role=dialog]');
        if (!m) return null;
        const inputs = Array.from(m.querySelectorAll('input, select, textarea')).map(e=>({id:e.id,name:e.name,type:e.type,ph:e.placeholder||'',cls:(e.className||'').toString().slice(0,40)}));
        const lists = Array.from(m.querySelectorAll('li, option, [class*=item], [class*=list] > *')).slice(0,15).map(e=>({tag:e.tagName, txt:(e.innerText||'').trim().slice(0,20), cls:(e.className||'').toString().slice(0,40), id:e.id}));
        return {cls:(m.className||'').toString().slice(0,80), html:m.outerHTML.slice(0,3000), inputs, lists};
    }''')
    print('MODAL:', json.dumps(modal, ensure_ascii=False)[:3500] if modal else 'NONE')
    if not modal:
        # maybe it's a full-page nav
        print('url now:', pg.url)
        body = pg.evaluate('() => document.body.innerText')
        print('body:', body[:500].replace('\\n',' | '))
    b.close()
