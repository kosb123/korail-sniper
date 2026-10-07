# -*- coding: utf-8 -*-
"""HEADFUL persistent-profile test: does a real (non-headless) browser pass NetFunnel WAF on korail?
This window pops up on screen. Seoul->Busan tomorrow; web_s 200+JSON = WAF passes."""
import json, os
from playwright.sync_api import sync_playwright
EXE = r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
PROFILE = r'C:\Users\jun\AppData\Local\hermes\cache\scratch\korail_headful_profile'
ws = []
def on_resp(resp):
    try:
        if 'korail.com' not in resp.url: return
        if any(s in resp.url for s in ['/img/','fonts','.css','.png','.gif','.svg','.woff','.ico','/bundle/']): return
        if 'web_s' in resp.url or '/classes/' in resp.url:
            body=''
            try: body=resp.text()
            except: body='[x]'
            ws.append({'st':resp.status,'url':resp.url,'len':len(body),'isjson':body.lstrip()[:1] in '{[' and '"code"' in body or 'trnNm' in body,'head':body[:300]})
    except: pass
def pick(pg, idx, name):
    pg.evaluate('''(a)=>{document.querySelectorAll('a.btn_pop-openStationPop')[a[0]].click();}''',[idx])
    pg.wait_for_timeout(1500)
    pg.locator('input[placeholder*="역 이름"]').first.fill(name)
    pg.wait_for_timeout(1500)
    pg.evaluate('''(n)=>{const i=Array.from(document.querySelectorAll('li')).filter(e=>e.offsetParent!==null&&(e.innerText||'').trim().indexOf(n)===0);if(i.length)i[0].click();}''',name)
    pg.wait_for_timeout(900)
with sync_playwright() as p:
    # headful + persistent profile (real fingerprint, no automation flags)
    ctx = p.chromium.launch_persistent_context(PROFILE, headless=False, executable_path=EXE,
        user_agent=UA, locale='ko-KR', viewport={'width':1400,'height':950},
        args=['--no-sandbox'])
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()
    pg.on('response', on_resp)
    pg.goto('https://www.korail.com/ticket/main', wait_until='domcontentloaded', timeout=40000)
    pg.wait_for_timeout(6000)
    print('main loaded:', pg.url)
    # close any modal popup (terms/notice) before clicking
    pg.evaluate('''()=>{
        // try common close buttons on ReactModal content
        const modals = Array.from(document.querySelectorAll('.ReactModal__Content, [role=dialog]'));
        for(const m of modals){
            const btn = m.querySelector('.btn_close, .close, [class*=close], button, a');
            if(btn){ btn.click(); }
        }
        // fallback: Escape
        document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',keyCode:27,which:27,bubbles:true}));
    }''')
    pg.wait_for_timeout(1500)
    pg.evaluate('''()=>{
        document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',keyCode:27,which:27,bubbles:true}));
        const ov = document.querySelector('.ReactModal__Overlay');
        if(ov) ov.click();
    }''')
    pg.wait_for_timeout(1500)
    try:
        pg.click('.btn_lookup', timeout=12000)
    except Exception as e:
        print('btn_lookup fail:', e)
        # last resort: direct click
        pg.evaluate('''()=>{const b=document.querySelector('.btn_lookup');if(b)b.click();}''')
    pg.wait_for_timeout(6000)
    pick(pg,0,'서울'); pick(pg,1,'부산')
    pg.evaluate('''()=>{const n=document.getElementById('dateinput__next');if(n)n.click();}''')
    pg.wait_for_timeout(1000)
    print('date:', pg.evaluate('''()=>document.getElementById('startDate').value'''))
    pg.evaluate('''()=>{const btn=Array.from(document.querySelectorAll('button')).find(e=>/열차조회/.test((e.innerText||'').trim()));if(btn)btn.click();}''')
    pg.wait_for_timeout(12000)
    body=pg.evaluate('()=>document.body.innerText')
    i=body.find('전체')
    print('RESULT:', (body[i:i+600].replace('\n',' | ') if i>0 else body[:600].replace('\n',' | ')))
    print('KTX mentions:', body.count('KTX'))
    ctx.close()
print('=== web_s/classes ===')
ok=0
for w in ws:
    flag='JSON' if w['isjson'] else ''
    if w['isjson']: ok+=1
    print(w['st'], w['url'][:80], 'len=',w['len'], flag)
print('web_s JSON count:', ok)
