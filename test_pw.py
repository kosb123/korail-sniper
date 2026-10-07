# -*- coding: utf-8 -*-
"""Test Playwright chromium launches and loads the SRT schedule page."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=r'C:\Users\jun\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe', args=['--no-sandbox','--disable-blink-features=AutomationControlled'])
    pg = b.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', locale='ko-KR', viewport={'width':1920,'height':1040})
    resp = pg.goto('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000', wait_until='domcontentloaded', timeout=30000)
    print('status', resp.status if resp else None, 'title', pg.title())
    print('has dptRsStnCd:', pg.query_selector('#dptRsStnCd') is not None)
    b.close()
print('PLAYWRIGHT OK')
