# -*- coding: utf-8 -*-
"""Test with REAL user Chrome binary (channel=chrome) + persistent profile.
Also dump response headers of the ScheduleView 500 to confirm WAF source."""
import requests, json, os
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
s = requests.Session(); s.headers.update({'User-Agent': UA})
s.get('https://www.korail.com/ticket/main', timeout=30)
fields = [('searchType','GENERAL'),('txtGoStart','서울'),('txtGoEnd','부산'),('txtTrnGpCd','109'),
 ('radJobId','1'),('adjStnScdlOfrFlg','N'),('adjStnScdlOfrFlg2','N'),('srtCheckYn','N'),
 ('ebizCrossCheck','N'),('txtPsgFlg_1','1'),('rtYn','N'),('txtGoAbrdDt','20261008'),
 ('txtGoHour','000000'),('txtWkndUseFlg','Y'),('txtGoStartCode','0001'),('txtGoEndCode','0020'),
 ('txtMenuId','11'),('limitStartDate','20261007'),('txtTrainNm','전체'),('txtSeatAttCd_4','015'),
 ('tkTripChgQryFlg','Y'),('Device','BH'),('Version','999999999')]
r = s.post('https://www.korail.com/classes/com.korail.mobile.seatMovie.ScheduleView', data=fields, timeout=40)
print('ScheduleView st:', r.status_code)
for k,v in r.headers.items():
    if any(x in k.lower() for x in ['nf','netfunnel','x-','via','server','set-cookie']):
        print('  hdr:', k, '=', v[:120])
open(r'C:\Users\jun\projects\korail-sniper\sv500_headers.txt','w',encoding='utf-8').write(str(dict(r.headers)))

# ---- real chrome binary test ----
from playwright.sync_api import sync_playwright
PROFILE = r'C:\Users\jun\AppData\Local\hermes\cache\scratch\korail_realchrome_profile'
ws = []
def on_resp(resp):
    try:
        if 'korail.com' not in resp.url: return
        if any(x in resp.url for x in ['/img/','fonts','.css','.png','.gif','.svg','.woff','.ico','/bundle/']): return
        if 'web_s' in resp.url or 'ScheduleView' in resp.url or 'runDt' in resp.url:
            body=''
            try: body=resp.text()
            except: pass
            ws.append({'st':resp.status,'url':resp.url[:100],'len':len(body),'json':body.lstrip()[:1] in '{[','head':body[:200]})
    except: pass
def pick(pg, idx, name):
    pg.evaluate('''(a)=>{document.querySelectorAll('a.btn_pop-openStationPop')[a[0]].click();}''',[idx])
    pg.wait_for_timeout(1500)
    pg.locator('input[placeholder*="역 이름"]').first.fill(name)
    pg.wait_for_timeout(1500)
    pg.evaluate('''(n)=>{const i=Array.from(document.querySelectorAll('li')).filter(e=>e.offsetParent!==null&&(e.innerText||'').trim().indexOf(n)===0);if(i.length)i[0].click();}''',name)
    pg.wait_for_timeout(900)
with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(PROFILE, channel='chrome', headless=False,
        locale='ko-KR', viewport={'width':1400,'height':950}, args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()
    pg.on('response', on_resp)
    pg.goto('https://www.korail.com/ticket/main', wait_until='domcontentloaded', timeout=40000)
    pg.wait_for_timeout(8000)
    # close popups
    pg.evaluate('''()=>{document.querySelectorAll('.ReactModal__Content .btn_close, [class*=close]').forEach(b=>b.click());document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',keyCode:27,bubbles:true}));}''')
    pg.wait_for_timeout(1000)
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
    print('RESULT:', (body[i:i+500].replace('\n',' | ') if i>0 else body[:500].replace('\n',' | ')))
    print('KTX count:', body.count('KTX'), '| 좌석 mentions:', body.count('좌석'))
    ctx.close()
print('=== endpoints ===')
for w in ws: print(w['st'], w['url'], 'len=',w['len'], 'json=',w['json'], w['head'][:150].replace('\n',' '))
