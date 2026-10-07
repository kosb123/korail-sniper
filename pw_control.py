# -*- coding: utf-8 -*-
"""DEFINITIVE control: 서울->부산 10-08. Trains MUST exist. web_s status is the signal."""
import json, re
from playwright.sync_api import sync_playwright
EXE = r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
ws = []
def on_resp(resp):
    try:
        if 'korail.com' not in resp.url: return
        if any(s in resp.url for s in ['/img/','fonts','.css','.png','.gif','.svg','.woff','.ico','/bundle/']): return
        u = resp.url
        if 'web_s' in u or '/classes/' in u:
            body=''
            try: body=resp.text()
            except: body='[x]'
            ws.append({'st':resp.status,'url':u,'ct':resp.headers.get('content-type',''),'len':len(body),'body':body[:3000]})
    except: pass
def pick(pg, idx, name):
    pg.evaluate('''(a)=>{document.querySelectorAll('a.btn_pop-openStationPop')[a[0]].click();}''',[idx])
    pg.wait_for_timeout(1200)
    pg.locator('input[placeholder*="역 이름"]').first.fill(name)
    pg.wait_for_timeout(1200)
    pg.evaluate('''(n)=>{const i=Array.from(document.querySelectorAll('li')).filter(e=>e.offsetParent!==null&&(e.innerText||'').trim().indexOf(n)===0);if(i.length)i[0].click();}''',name)
    pg.wait_for_timeout(700)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,executable_path=EXE,args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    ctx=b.new_context(user_agent=UA,locale='ko-KR',viewport={'width':1920,'height':1040})
    pg=ctx.new_page(); pg.on('response',on_resp)
    pg.goto('https://www.korail.com/ticket/main',wait_until='domcontentloaded',timeout=35000)
    pg.wait_for_timeout(4000)
    pg.click('.btn_lookup',timeout=10000); pg.wait_for_timeout(5000)
    pick(pg,0,'서울'); pick(pg,1,'부산')
    # advance to tomorrow (10-08)
    pg.evaluate('''()=>{const n=document.getElementById('dateinput__next');if(n)n.click();}''')
    pg.wait_for_timeout(800)
    print('date:',pg.evaluate('''()=>document.getElementById('startDate').value'''))
    # capture the datetime picker DOM to understand hour control
    picker = pg.evaluate('''()=>{
        const d = document.querySelector('[id*=dateinput], [class*=date], [class*=datetime], [class*=picker], [class*=calendar]');
        return d?d.outerHTML.slice(0,3000):'none';
    }''')
    print('PICKER:', picker[:1500])
    pg.evaluate('''()=>{const btn=Array.from(document.querySelectorAll('button')).find(e=>/열차조회/.test((e.innerText||'').trim()));if(btn)btn.click();}''')
    pg.wait_for_timeout(10000)
    body=pg.evaluate('()=>document.body.innerText')
    i=body.find('전체')
    print('RESULT:', (body[i:i+700].replace('\n',' | ') if i>0 else body[:700].replace('\n',' | ')))
    b.close()
print('=== web_s/classes responses ===')
for w in ws: print(w['st'], w['url'][:90], w['ct'], 'len=',w['len'])
# check if any returned JSON
for w in ws:
    if w['body'].strip().startswith('{') or '"trnNm"' in w['body'] or '"code"' in w['body']:
        print('JSON FOUND in:', w['url'][:80]); print(w['body'][:1000]); break
else:
    print('NO JSON in any web_s/classes response')
