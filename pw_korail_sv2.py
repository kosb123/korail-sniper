# -*- coding: utf-8 -*-
"""Korail: search 평택지제->증평 10/08 18:00 with FULL response bodies captured."""
import json, re
from playwright.sync_api import sync_playwright
EXE = r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
captured = []
SKIP = ['/img/','fonts','.css','.png','.gif','.svg','.woff','.ico','/bundle/','.cache','cdn.korail']
def on_req(req):
    try:
        if 'korail.com' not in req.url: return
        if req.method=='POST':
            captured.append({'side':'REQ','m':'POST','url':req.url,'data':(req.post_data or '')[:4000]})
    except Exception: pass
def on_resp(resp):
    try:
        if 'korail.com' not in resp.url: return
        if any(s in resp.url for s in SKIP): return
        body=''
        try: body=resp.text()
        except Exception: body='[binary/err]'
        captured.append({'side':'RES','m':resp.request.method,'st':resp.status,'url':resp.url,'ct':resp.headers.get('content-type',''),'len':len(body),'body':body[:20000]})
    except Exception: pass

def pick_station(pg, idx, name):
    pg.evaluate('''(args) => { document.querySelectorAll('a.btn_pop-openStationPop')[args[0]].click(); }''', [idx])
    pg.wait_for_timeout(1500)
    loc = pg.locator('input[placeholder*="역 이름"]').first
    loc.fill(name)
    pg.wait_for_timeout(1500)
    r = pg.evaluate('''(name) => {
        const items = Array.from(document.querySelectorAll('li')).filter(e=>e.offsetParent!==null && (e.innerText||'').trim().indexOf(name)===0);
        if(items.length){ items[0].click(); return (items[0].innerText||'').trim().slice(0,30); }
        return null;
    }''', name)
    pg.wait_for_timeout(800)
    print(f'  picked {name}:', r)

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=EXE, args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    pg = b.new_context(user_agent=UA, locale='ko-KR', viewport={'width':1920,'height':1040}).new_page()
    pg.on('request', on_req); pg.on('response', on_resp)
    pg.goto('https://www.korail.com/ticket/main', wait_until='domcontentloaded', timeout=35000)
    pg.wait_for_timeout(4000)
    pg.click('.btn_lookup', timeout=10000)
    pg.wait_for_timeout(5000)
    pick_station(pg, 0, '평택지제')
    pick_station(pg, 1, '증평')
    # datetime: inspect picker, then set 2026-10-08 18:00
    dt = pg.evaluate('''() => {
        const el = document.getElementById('startDate');
        const wrap = document.querySelector('[id*=dateinput], [class*=date], [class*=datetime]');
        return {val: el?el.value:'', wrapCls: wrap?wrap.className:''};
    }''')
    print('datetime before:', dt)
    # click next-day (today=10-07 -> target 10-08), then set hour via picker inputs if present
    pg.evaluate('''() => { const n = document.getElementById('dateinput__next'); if(n) n.click(); }''')
    pg.wait_for_timeout(1000)
    # try to find hour input in picker
    h = pg.evaluate('''() => {
        const ins = Array.from(document.querySelectorAll('input')).filter(e=>e.offsetParent!==null && (e.id||e.className).toString().match(/hour|Hour|min|Hour/));
        return ins.map(e=>({id:e.id, cls:e.className.toString().slice(0,40), val:e.value}));
    }''')
    print('picker hour inputs:', h)
    # direct set: dispatch input events on startDate
    pg.evaluate('''() => {
        const el = document.getElementById('startDate');
        el.removeAttribute('readonly');
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
        setter.call(el, '2026-10-08(목) 18:00');
        el.dispatchEvent(new Event('input',{bubbles:true}));
        el.dispatchEvent(new Event('change',{bubbles:true}));
        el.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',code:'Enter',keyCode:13,bubbles:true}));
        el.blur();
    }''')
    pg.wait_for_timeout(1500)
    print('datetime after:', pg.evaluate('''() => document.getElementById('startDate').value'''))
    # search
    pg.evaluate('''() => { const btn = Array.from(document.querySelectorAll('button')).find(e=>/열차조회/.test((e.innerText||'').trim())); if(btn) btn.click(); }''')
    pg.wait_for_timeout(9000)
    body = pg.evaluate('() => document.body.innerText')
    open(r'C:\Users\jun\projects\korail-sniper\korail_result_18.txt','w',encoding='utf-8').write(body)
    print('== result snippet ==')
    i = body.find('전체')
    print(body[i:i+1500].replace('\n',' | ') if i>0 else body[:1500].replace('\n',' | '))
    b.close()
json.dump(captured, open(r'C:\Users\jun\projects\korail-sniper\korail_sv_full.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('captured:', len(captured))
