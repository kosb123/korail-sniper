# -*- coding: utf-8 -*-
"""Korail: full UI search 평택지제->증평 10/08, capture ScheduleView API req/resp. THE key probe."""
import json
from playwright.sync_api import sync_playwright
EXE = r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
captured = []
def on_req(req):
    try:
        if 'korail.com' not in req.url: return
        if any(s in req.url for s in ['/img/','fonts','.css','.png','.gif','.svg','.woff','.ico','/bundle/']): return
        if req.method=='POST':
            captured.append({'side':'REQ','m':'POST','url':req.url,'data':(req.post_data or '')[:2500]})
    except Exception: pass
def on_resp(resp):
    try:
        if 'korail.com' not in resp.url: return
        if any(s in resp.url for s in ['/img/','fonts','.css','.png','.gif','.svg','.woff','.ico','/bundle/','.cache']): return
        body=''
        try:
            ct=resp.headers.get('content-type','')
            if 'json' in ct or 'xml' in ct: body=resp.text()[:12000]
        except Exception: pass
        captured.append({'side':'RES','m':resp.request.method,'st':resp.status,'url':resp.url,'ct':resp.headers.get('content-type',''),'body':body})
    except Exception: pass

def pick_station(pg, idx, name):
    """Open the station popup (idx 0=dep,1=arr), type name, click first match, confirm."""
    pg.evaluate('''(args) => {
        const btns = Array.from(document.querySelectorAll('a.btn_pop-openStationPop'));
        btns[args[0]].click();
    }''', [idx])
    pg.wait_for_timeout(1500)
    # find search input inside popup
    info = pg.evaluate('''(name) => {
        const inp = document.querySelector('.stationPop input, [class*=station] input[type=text], [class*=Station] input, [class*=stn] input, input[placeholder*="역"], input[placeholder*="검색"]');
        const pop = document.querySelector('[class*=stationPop], [class*=StationPop], [class*=stationpop], [class*=stnPop]');
        return {hasInput: !!inp, inpId: inp?inp.id:'', inpPh: inp?inp.placeholder:'', popCls: pop?pop.className.toString().slice(0,80):'', popHtml: pop?pop.outerHTML.slice(0,2500):''};
    }''', name)
    print(f'  [pick {name}]', json.dumps(info, ensure_ascii=False)[:900])
    if info['hasInput']:
        sel = 'input'
        # locate selector robustly
        loc = pg.locator('.stationPop input, [class*=station] input[type=text], [class*=stn] input, input[placeholder*="역"], input[placeholder*="검색"]').first
        loc.fill(name)
        pg.wait_for_timeout(1500)
        # click first result li containing name
        ok = pg.evaluate('''(name) => {
            const items = Array.from(document.querySelectorAll('li, [class*=item], [class*=list] > *')).filter(e=>e.offsetParent!==null && (e.innerText||'').trim().indexOf(name)===0);
            if(items.length){ items[0].click(); return {clicked:(items[0].innerText||'').trim().slice(0,30), n:items.length}; }
            return {clicked:null, n:items.length};
        }''', name)
        print(f'  [click] ', ok)
        pg.wait_for_timeout(800)
        # maybe a confirm button
        c = pg.evaluate('''() => {
            const b = Array.from(document.querySelectorAll('button, a, [role=button]')).find(e=>e.offsetParent!==null && /(선택|확인|적용)/.test((e.innerText||'').trim()));
            if(b){b.click(); return (b.innerText||'').trim();}
            return null;
        }''')
        print('  [confirm]', c)
        pg.wait_for_timeout(800)

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=EXE, args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    pg = b.new_context(user_agent=UA, locale='ko-KR', viewport={'width':1920,'height':1040}).new_page()
    pg.on('request', on_req)
    pg.on('response', on_resp)
    pg.goto('https://www.korail.com/ticket/main', wait_until='domcontentloaded', timeout=35000)
    pg.wait_for_timeout(4000)
    pg.click('.btn_lookup', timeout=10000)
    pg.wait_for_timeout(5000)
    print('on search page:', pg.url)
    print('== pick departure 평택지제 ==')
    pick_station(pg, 0, '평택지제')
    print('== pick arrival 증평 ==')
    pick_station(pg, 1, '증평')
    # set date to 2026-10-08: click 다음날 (next day) — today is 10-07
    pg.evaluate('''() => { const n = document.getElementById('dateinput__next'); if(n) n.click(); }''')
    pg.wait_for_timeout(1000)
    print('date now:', pg.evaluate('''() => document.getElementById('dateinput__input-wrapper') ? document.getElementById('dateinput__input-wrapper').innerText : (document.getElementById('startDate')?document.getElementById('startDate').value:'?')'''))
    # click 열차조회
    pg.evaluate('''() => { const btn = Array.from(document.querySelectorAll('button')).find(e=>/열차조회/.test((e.innerText||'').trim())); if(btn) btn.click(); }''')
    pg.wait_for_timeout(8000)
    print('final url:', pg.url)
    body = pg.evaluate('() => document.body.innerText')
    open(r'C:\Users\jun\projects\korail-sniper\korail_search_result.txt','w',encoding='utf-8').write(body)
    import re
    m = re.findall(r'(KTX|ITX|무궁화|새마을|누리로)[^\n]{0,80}', body)
    print('train mentions:', m[:10])
    print('body mid:', body[400:1800].replace('\n',' | '))
    b.close()
json.dump(captured, open(r'C:\Users\jun\projects\korail-sniper\korail_sv_net.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('captured:', len(captured))
for c in captured:
    if 'ScheduleView' in c.get('url','') or 'Research' in c.get('url','') or 'dynaPath' in c.get('url','') or 'web_s' in c.get('url',''):
        print(c['side'], c.get('m'), c.get('st'), c['url'][:110])
