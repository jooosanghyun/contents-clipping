#!/usr/bin/env python3
"""clippings/ 폴더를 스캔해서 index.html(아카이브 landing)을 생성.
새 클리핑 추가 후 실행: python3 build_index.py"""
import os, re, glob, html

CLIP_DIR = 'clippings'
items = []
for path in sorted(glob.glob(os.path.join(CLIP_DIR, '*.html')), reverse=True):
    date = os.path.basename(path).replace('.html', '')
    s = open(path, encoding='utf-8').read()
    # 신호등
    m = re.search(r'<div class="v"[^>]*>[^가-힣]*(평온|주목|이슈)</div>', s)
    if not m:
        m = re.search(r'<div class="light"><span class="dot"></span><b>([^<]+)</b>', s)
    light = m.group(1) if m else '평온'
    # 요약 첫 항목
    sums = re.findall(r'<li><b>(.*?)</b>(.*?)</li>', s, re.S)
    bullets = []
    for a, b in sums[:3]:
        txt = re.sub(r'<[^>]+>', '', a + b)
        bullets.append(txt.strip()[:120])
    items.append({'date': date, 'light': light, 'bullets': bullets})

LIGHT_COLOR = {'평온': '#2a8f5a', '주목': '#e6b800', '이슈': '#c0392b'}

cards = []
for i, it in enumerate(items):
    color = LIGHT_COLOR.get(it['light'], '#888')
    latest = ' <span class="latest">최신</span>' if i == 0 else ''
    bl = ''.join(f'<li>{html.escape(b)}</li>' for b in it['bullets'])
    cards.append(f'''  <a class="card" href="{CLIP_DIR}/{it['date']}.html">
    <div class="cd"><span class="dot" style="background:{color}"></span><b>{it['date']}</b>{latest}
      <span class="lt" style="color:{color}">{it['light']}</span></div>
    <ul class="cb">{bl}</ul>
  </a>''')

body = '\n'.join(cards) if cards else '<p class="empty">아직 발행된 클리핑이 없습니다.</p>'

TPL = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>상용차 콘텐츠 클리핑</title>
<meta name="description" content="국내 상용차 시장 유튜브 여론·경쟁사 동향 데일리 모니터링">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Malgun Gothic","Noto Sans KR",sans-serif;background:#f4f4f2;color:#1a1a1a;font-size:14px;line-height:1.6}}
.wrap{{max-width:820px;margin:0 auto;background:#fff;min-height:100vh;box-shadow:0 0 20px rgba(0,0,0,.05)}}
header{{background:linear-gradient(135deg,#1a1a1a,#333);color:#fff;padding:30px 34px}}
header h1{{font-size:22px;font-weight:800}}
header p{{font-size:12.5px;opacity:.72;margin-top:6px}}
main{{padding:24px 34px 44px}}
.card{{display:block;border:1px solid #e6e6e6;border-radius:10px;padding:14px 18px;margin-bottom:12px;text-decoration:none;color:inherit;background:#fcfcfb;transition:.15s}}
.card:hover{{border-color:#c8472b;background:#fff;transform:translateY(-1px);box-shadow:0 3px 10px rgba(0,0,0,.06)}}
.cd{{display:flex;align-items:center;gap:8px;font-size:14px;flex-wrap:wrap}}
.dot{{width:10px;height:10px;border-radius:50%;flex-shrink:0}}
.lt{{font-size:11.5px;font-weight:700;margin-left:auto}}
.latest{{background:#c8472b;color:#fff;font-size:10.5px;padding:1px 8px;border-radius:9px;font-weight:700}}
.cb{{margin:8px 0 0 16px;font-size:12.5px;color:#555}}
.cb li{{margin:3px 0}}
.empty{{color:#999;text-align:center;padding:40px}}
footer{{padding:16px 34px;background:#fafafa;border-top:1px solid #e6e6e6;font-size:11px;color:#999}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>상용차 콘텐츠 클리핑</h1>
  <p>국내 상용차 유튜브·커뮤니티 콘텐츠 여론 모니터링 · 경쟁사 채널 동향<br>
  평일 자동 발행 · 신규 이슈가 있는 날만 게시</p>
</header>
<main>
{body}
</main>
<footer>
소스: YouTube Data API · 상용차신문 · 보배드림 · 공개 정보 기반 · 커뮤니티/댓글 인용은 개인 의견이며 시사점은 분석 의견입니다.
</footer>
</div>
</body>
</html>
'''
open('index.html', 'w', encoding='utf-8').write(TPL)
print(f'index.html generated with {len(items)} clipping(s)')
