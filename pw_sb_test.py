# -*- coding: utf-8 -*-
"""Korail: control test — search 서울->부산 (guaranteed to have trains). If trains render, headless search works."""
import json
from playwright.sync_api import sync_playwright
EXE = r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
captured = []
def on_req(req):
    try:
        if 'korail.com' not in req.url: return
        if req.method=='POST':
            captured.append({'side':'REQ','url':req.url,'data':(req.post_data or '')[:600]})
    except Exception: pass
def on_resp(resp):
    try:
        if 'korail.com' not in resp.url: return
        if any(s in resp.url for s in ['/img/','fonts','.css','.png','.gif','.svg','.woff','.ico','/bundle/']): return
        captured.append({'side':'RES','st':resp.status,'url':resp.url,'ct':resp.headers.get('content-type','')})
    except Exception: pass

def pick_station(pg, idx, name):
    pg.evaluate('''(args) => { document.querySelectorAll('a.btn_pop-openStationPop')[args[0]].click(); }''', [idx])
    pg.wait_for_timeout(1500)
    pg.locator('input[placeholder*="역 이름"]').first.fill(name)
    pg.wait_for_timeout(1500)
    pg.evaluate('''(name) => {
        const items = Array.from(document.querySelectorAll('li')).filter(e=>e.offsetParent!==null && (e.innerText||'').trim().indexOf(name)===0);
        if(items.length) items[0].click();
    }''', name)
    pg.wait_for_timeout(800)

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=EXE, args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    pg = b.new_context(user_agent=UA, locale='ko-KR', viewport={'width':1920,'height':1040}).new_page()
    pg.on('request', on_req); pg.on('response', on_resp)
    pg.goto('https://www.korail.com/ticket/main', wait_until='domcontentloaded', timeout=35000)
    pg.wait_for_timeout(4000)
    pg.click('.btn_lookup', timeout=10000)
    pg.wait_for_timeout(5000)
    pick_station(pg, 0, '서울')
    pick_station(pg, 1, '부산')
    # leave default date (today 10-07) — has lots of trains
    pg.evaluate('''() => { const btn = Array.from(document.querySelectorAll('button')).find(e=>/열차조회/.test((e.innerText||'').trim())); if(btn) btn.click(); }''')
    pg.wait_for_timeout(10000)
    body = pg.evaluate('() => document.body.innerText')
    open(r'C:\Users\jun\projects\korail-sniper\korail_result_seoulbusan.txt','w',encoding='utf-8').write(body)
    i = body.find('전체')
    print('== 결과 ==')
    print(body[i:i+1200].replace('\n',' | ') if i>0 else body[:1200].replace('\n',' | '))
    b.close()
json.dump(captured, open(r'C:\Users\jun\projects\korail-sniper\korail_sb_net.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('REQs with /classes/:', [c['url'] for c in captured if '/classes/' in c.get('url','')][:5])
print('web_s:', sum(1 for c in captured if 'web_s' in c.get('url','')), '| dynaPath:', sum(1 for c in captured if 'dynaPath' in c.get('url','')))
