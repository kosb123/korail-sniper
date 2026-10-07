# -*- coding: utf-8 -*-
"""Probe 19: where is the SPA served from? test alternate hosts/paths for the API."""
import requests

H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}

s = requests.Session()
r = s.get('https://www.korail.com/ticket', headers=H, timeout=25, allow_redirects=True)
print('GET /ticket ->', r.status_code, 'final url:', r.url, 'len:', len(r.text))
open(r'C:\Users\jun\projects\korail-sniper\ticket_page.html', 'w', encoding='utf-8').write(r.text)
# find script srcs and meta
import re
for m in re.findall(r'<script[^>]*src="([^"]+)"', r.text)[:20]:
    print('script:', m)
for m in re.findall(r'<link[^>]*href="([^"]+)"', r.text)[:10]:
    print('link:', m)
# look for API host hints in html
for m in re.findall(r'["\'](https?://[^"\']+)["\']', r.text)[:20]:
    print('url:', m)

# Now test /com/propDataSource.do on www
for path in ['/com/propDataSource.do', '/ebizcross/getUUID.do']:
    try:
        rr = s.post('https://www.korail.com' + path, data={}, headers=H, timeout=20)
        print('www.korail.com', path, '->', rr.status_code, rr.text[:200].replace('\n', ' '))
    except Exception as e:
        print('ERR', path, e)

# Maybe the SPA is on m.korail.com (mobile)?
for host in ['m.korail.com', 'ticket.korail.com', 'ebiz.korail.com']:
    try:
        rr = s.get(f'https://{host}/', headers=H, timeout=15, allow_redirects=True)
        print(host, '->', rr.status_code, rr.url[:100], 'len:', len(rr.text))
    except Exception as e:
        print(host, 'ERR', type(e).__name__, str(e)[:100])
