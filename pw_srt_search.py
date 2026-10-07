# -*- coding: utf-8 -*-
"""SRT via Playwright: fill form (평택지제 0553 -> 증평 0071, 2026-10-08), submit, capture network + result rows."""
import json, time
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
            if any(k in u for k in ['selectScheduleList','selectTrain','seat','Seat','schedule','Schedule']) and 'cdn' not in u:
                body = ''
                try: body = resp.text()[:2000]
                except Exception: pass
                captured.append({'url': u, 'status': resp.status, 'ct': resp.headers.get('content-type',''), 'body': body})
        except Exception: pass
    pg.on('response', on_resp)
    pg.goto('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000', wait_until='domcontentloaded', timeout=30000)
    pg.wait_for_timeout(2500)
    # fill station selects by value
    pg.select_option('#dptRsStnCd', '0553')
    pg.select_option('#arvRsStnCd', '0071')
    pg.fill('#dptDt', '20261008')
    # passenger count (adult 1) — try psgInfoPerPrnb1
    try: pg.fill('#psgInfoPerPrnb1', '1')
    except Exception as e: print('psg fill err', e)
    # find submit button
    btn = pg.query_selector('#btnSearch') or pg.query_selector('input[type=submit]') or pg.query_selector('button:has-text("검색")')
    print('submit btn:', btn.outer_html()[:200] if btn else None)
    if btn: btn.click()
    pg.wait_for_timeout(6000)
    print('final url:', pg.url)
    print('title:', pg.title())
    # dump result table text
    body_txt = pg.evaluate('() => document.body.innerText')
    open(r'C:\Users\jun\projects\korail-sniper\srt_pw_result.txt','w',encoding='utf-8').write(body_txt)
    print('body sample:', body_txt[:1200].replace('\n',' | '))
    b.close()
json.dump(captured, open(r'C:\Users\jun\projects\korail-sniper\srt_pw_net.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('captured reqs:', len(captured))
for c in captured: print(c['status'], c['url'][:110], c['ct'][:30])
