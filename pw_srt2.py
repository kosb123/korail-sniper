# -*- coding: utf-8 -*-
"""SRT via Playwright: set hidden inputs directly, click search, capture network + results."""
import json
from playwright.sync_api import sync_playwright
EXE = r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
captured = []
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=EXE, args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    pg = b.new_context(user_agent=UA, locale='ko-KR', viewport={'width':1920,'height':1040}).new_page()
    def on_resp(resp):
        try:
            u = resp.url
            if ('etk.srail.kr' in u or 'srail' in u) and 'cdn' not in u and any(k in u for k in ['select','Seat','seat','Schedule','schedule','trn']):
                body = ''
                try: body = resp.text()[:4000]
                except Exception: pass
                captured.append({'url': u, 'status': resp.status, 'ct': resp.headers.get('content-type',''), 'body': body})
        except Exception: pass
    pg.on('response', on_resp)
    pg.goto('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000', wait_until='domcontentloaded', timeout=30000)
    pg.wait_for_timeout(2500)
    # set hidden values via JS
    ok = pg.evaluate('''() => {
        function setv(id, v){ const el = document.getElementById(id) || document.querySelector('[name='+id+']'); if(!el) return false; el.value = v; el.dispatchEvent(new Event('change',{bubbles:true})); return true; }
        return [setv('dptRsStnCd','0553'), setv('arvRsStnCd','0071'), setv('dptDt','20261008'), setv('psgInfoPerPrnb1','1')];
    }''')
    print('setv results:', ok)
    # click search button
    btn = pg.query_selector('button:has-text("검색")') or pg.query_selector('input[type=submit]') or pg.query_selector('#btnSearch')
    if btn: btn.click()
    else: print('NO SEARCH BUTTON FOUND')
    pg.wait_for_timeout(8000)
    print('final url:', pg.url)
    print('title:', pg.title())
    body_txt = pg.evaluate('() => document.body.innerText')
    open(r'C:\Users\jun\projects\korail-sniper\srt_pw_result.txt','w',encoding='utf-8').write(body_txt)
    print('body sample:', body_txt[:1500].replace('\n',' | '))
    b.close()
json.dump(captured, open(r'C:\Users\jun\projects\korail-sniper\srt_pw_net.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('captured reqs:', len(captured))
for c in captured: print(c['status'], c['url'][:120], '|', c['ct'][:40])
