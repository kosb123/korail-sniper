# -*- coding: utf-8 -*-
"""Korail via Playwright: go to reservation page, fill 평택지제->증평 10/08, search, capture ALL network + result DOM."""
import json
from playwright.sync_api import sync_playwright
EXE = r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
captured = []
def mk_logger(tag):
    def on_resp(resp):
        try:
            u = resp.url
            if 'cdn.korail.com' in u or 'fonts' in u or '.css' in u or '.js' in u or '.png' in u or '.gif' in u or '.jpg' in u: return
            if 'korail.com' not in u and 'letskorail' not in u: return
            body=''
            try:
                ct=resp.headers.get('content-type','')
                if 'json' in ct or 'text' in ct or 'xml' in ct: body=resp.text()[:3000]
            except Exception: pass
            captured.append({'t':tag,'url':u,'status':resp.status,'ct':resp.headers.get('content-type',''),'body':body})
        except Exception: pass
    return on_resp
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=EXE, args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    pg = b.new_context(user_agent=UA, locale='ko-KR', viewport={'width':1920,'height':1040}).new_page()
    pg.on('response', mk_logger('nav'))
    # reservation page
    pg.goto('https://www.korail.com/ticket/reservation', wait_until='domcontentloaded', timeout=35000)
    pg.wait_for_timeout(3500)
    print('reservation url:', pg.url, '| title:', pg.title())
    # dump inputs to understand form
    fields = pg.evaluate('''() => Array.from(document.querySelectorAll('input, select, button')).map(e=>({id:e.id,name:e.name,type:e.type,tag:e.tagName,ph:e.placeholder||'',val:e.value||'',txt:(e.innerText||'').trim().slice(0,16),vis:(e.offsetParent!==null)})).filter(x=>x.vis)''')
    print('FIELDS:')
    for f in fields: print(' ', f)
    b.close()
json.dump(captured, open(r'C:\Users\jun\projects\korail-sniper\korail_resv_nav.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('captured:', len(captured))
for c in captured: print(c['status'], c['url'][:130], '|', c['ct'][:30])
