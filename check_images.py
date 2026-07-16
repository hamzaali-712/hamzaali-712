import re, urllib.request, ssl, sys
from pathlib import Path
root=Path('.')
text=(root/'README.md').read_text(encoding='utf-8')
srcs=re.findall(r'<img\s+[^>]*src=["\']([^"\']+)["\']', text)
srcs += re.findall(r'!\[[^\]]*\]\((https?[^)]+)\)', text)
seen=set()
ctx=ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode=ssl.CERT_NONE
print('Found',len(srcs),'image srcs')
for s in srcs:
    if s in seen: continue
    seen.add(s)
    print('\nChecking:', s)
    try:
        req=urllib.request.Request(s, method='HEAD', headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            print('->', r.status)
    except Exception as e:
        try:
            # try GET
            req=urllib.request.Request(s, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
                print('GET ->', r.status)
        except Exception as e2:
            print('ERROR ->', type(e2).__name__, e2)
sys.exit(0)
