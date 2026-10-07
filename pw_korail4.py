# -*- coding: utf-8 -*-
"""Korail: /ticket/search/general — inspect form, fill, search, capture network."""
import json
from playwright.sync_api import sync_playwright
EXE = r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
captured = []
def on_req(req):
    try:
        u = req.url
        if any(s in u for s in ['cdn.korail.com','/img/','fonts','.css','.png','.gif','.jpg','.svg','.woff','.ico']): return
        if 'korail.com' not in u: return
        if req.method=='POST':
            pd = req.post_data or ''
            captured.append({'m':'POST','url':u,'data':pd[:1500]})
    except Exception: pass
def on_resp(resp):
    try:
        u = resp.url
        if any(s in u for s in ['cdn.korail.com','/img/','fonts','.css','.png','.gif','.jpg','.svg','.woff','.ico']): return
        if 'korail.com' not in u: return
        body=''
        try:
            ct=resp.headers.get('content-type','')
            if 'json' in ct or 'xml' in ct or ('text' in ct and 'html' not in ct): body=resp.text()[:5000]
        except Exception: pass
        captured.append({'m':resp.request.method,'st':resp.status,'url':u,'ct':resp.headers.get('content-type',''),'body':body})
    except Exception: pass
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=EXE, args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    pg = b.new_context(user_agent=UA, locale='ko-KR', viewport={'width':1920,'height':1040}).new_page()
    pg.on('request', on_req)
    pg.on('response', on_resp)
    # main page, click 조회 with values pre-filled by JS before click
    pg.goto('https://www.korail.com/ticket/main', wait_until='domcontentloaded', timeout=35000)
    pg.wait_for_timeout(4000)
    pg.evaluate('''() => {
        document.getElementById('labelstart').value = '평택지제';
        document.getElementById('labelend').value = '증평';
    }''')
    # click 열차 조회하기
    btn = pg.query_selector('.btn_lookup') or pg.query_selector('button:has-text("열차 조회하기")')
    print('btn found:', bool(btn))
    if btn: btn.click()
    pg.wait_for_timeout(6000)
    print('url after click:', pg.url)
    print('title:', pg.title())
    # form fields on search page
    fields = pg.evaluate('''() => Array.from(document.querySelectorAll('form input, form select, form button, [class*=search] input, [class*=search] button, [class*=btn]')).filter(e=>e.offsetParent!==null).map(e=>({id:e.id,name:e.name,type:e.type||'',tag:e.tagName,ph:e.placeholder||'',val:(e.value||'').slice(0,25),txt:(e.innerText||'').trim().replace(/\\n/g,' ').slice(0,25)}))''')
    print('SEARCH PAGE FIELDS:', len(fields))
    for f in fields: print(' ', f)
    body = pg.evaluate('() => document.body.innerText')
    open(r'C:\Users\jun\projects\korail-sniper\korail_search_page.txt','w',encoding='utf-8').write(body)
    print('body head:', body[:600].replace('\n',' | '))
    b.close()
json.dump(captured, open(r'C:\Users\jun\projects\korail-sniper\korail_search_net.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('captured:', len(captured))
for c in captured:
    print(c.get('m'), c.get('st',''), c['url'][:130])
