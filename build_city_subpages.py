"""Wave 2: Generate subpages for 6 cities x 15 hotels x 2 languages = 180 pages.

For each city:
  1. Extract 15 featured hotels from zh main page (name, tags, desc, score, rating, amount, img, location)
  2. Same from en main page
  3. Generate pages/{city}hotels/{slug}.html (zh) and pages/{city}hotels-en/{slug}.html (en)
  4. Rewrite main page cards: remove .hotel-platforms, wrap card in <a>
"""
import re, json, html
from pathlib import Path

CITIES = {
    "BJ":{"zh":"北京","en":"Beijing","lat":39.9042,"lng":116.4074,"country":"CN","tz":"Asia/Shanghai","cur":"¥"},
    "GZ":{"zh":"廣州","en":"Guangzhou","lat":23.1291,"lng":113.2644,"country":"CN","tz":"Asia/Shanghai","cur":"¥"},
    "KH":{"zh":"高雄","en":"Kaohsiung","lat":22.6273,"lng":120.3014,"country":"TW","tz":"Asia/Taipei","cur":"NT$"},
    "MO":{"zh":"澳門","en":"Macau","lat":22.1987,"lng":113.5439,"country":"MO","tz":"Asia/Macau","cur":"MOP$"},
    "SH":{"zh":"上海","en":"Shanghai","lat":31.2304,"lng":121.4737,"country":"CN","tz":"Asia/Shanghai","cur":"¥"},
    "TP":{"zh":"台北","en":"Taipei","lat":25.0330,"lng":121.5654,"country":"TW","tz":"Asia/Taipei","cur":"NT$"},
}

TRIP = "https://hk.trip.com/?Allianceid=8067382&SID=305319575&trip_sub1=&trip_sub3=D15329722"
KLOOK = "https://affiliate.klook.com/redirect?aid=118358&aff_adid=1254708"

def slugify(name, index):
    # Prefer English tail; fallback to index
    m = re.search(r'([A-Za-z][A-Za-z0-9 &\-\'.]*)$', name)
    base = m.group(1).strip() if m else ""
    if not base:
        return f"hotel-{index:02d}"
    s = base.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s or f"hotel-{index:02d}"

def extract_cards(html_content):
    """Extract featured hotel cards. Returns list of dicts."""
    head = html_content  # scan entire page; card blocks are self-contained

    cards = []
    # Split by <div class="hotel-card"> and balance divs
    starts = [m.start() for m in re.finditer(r'<div class="hotel-card">', head)]
    for i, start in enumerate(starts):
        idx = start + len('<div class="hotel-card">')
        depth = 1
        while depth > 0 and idx < len(head):
            m = re.search(r'<div\b|</div>', head[idx:])
            if not m: break
            tag = m.group(0); idx += m.end()
            if tag == '</div>': depth -= 1
            else: depth += 1
        block = head[start:idx]
        def grab(pat, default=""):
            mm = re.search(pat, block, re.DOTALL)
            return mm.group(1).strip() if mm else default
        name = grab(r'<div class="hotel-name">([^<]+)</div>')
        if not name: continue
        cards.append({
            "name": name,
            "stars": grab(r'<div class="hotel-stars">([^<]+)</div>'),
            "location": grab(r'<div class="hotel-location">([^<]+)</div>'),
            "tags": re.findall(r'<span class="hotel-tag">([^<]+)</span>', block),
            "desc": grab(r'<div class="hotel-desc">([^<]+)</div>'),
            "score": grab(r'<span class="rating-score">([^<]+)</span>'),
            "rtext": grab(r'<span class="rating-text">([^<]+)</span>'),
            "amount": grab(r'<div class="amount">([^<]+)</div>'),
            "img": grab(r"background-image:url\('([^']+)'\)"),
        })
    return cards

def common_css():
    return """*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang TC',sans-serif;background:#f8f9fa;color:#333;line-height:1.75;}
.topbar{background:#1a1a2e;color:white;padding:12px 20px;font-size:0.9em;}
.topbar a{color:#ffd700;text-decoration:none;}
.hero{background:linear-gradient(135deg,#1a1a2e,#16213e 50%,#0f3460);color:white;padding:45px 20px;text-align:center;}
.hero h1{font-size:1.9em;margin-bottom:8px;}
.hero .stars{color:#ffd700;margin-bottom:10px;}
.hero .loc{opacity:0.9;font-size:0.95em;}
.container{max-width:920px;margin:-20px auto 40px;padding:0 15px;}
.card{background:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08);margin-bottom:20px;}
.hotel-img{width:100%;height:360px;background-size:cover;background-position:center;border-radius:12px 12px 0 0;}
.body{padding:28px 32px;}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 18px;}
.tag{background:#f0f2ff;color:#667eea;padding:4px 12px;border-radius:12px;font-size:0.82em;}
.rating{display:flex;align-items:center;gap:12px;margin:15px 0;}
.score{background:#ff4757;color:white;padding:6px 14px;border-radius:6px;font-weight:bold;font-size:1.1em;}
.desc{font-size:0.95em;color:#555;margin:15px 0;}
.price{font-size:1.6em;color:#ff4757;font-weight:bold;margin:15px 0 5px;}
.price small{font-size:0.6em;color:#888;font-weight:normal;}
.platforms{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px;}
.btn{flex:1;min-width:150px;padding:14px 20px;border-radius:8px;text-decoration:none;color:white;text-align:center;font-weight:bold;font-size:0.95em;}
.btn:hover{opacity:0.88;}
.btn-trip{background:#287DFA;}
.btn-klook{background:#FF5722;}
.btn-agoda{background:#C91A1A;}
.section{background:white;border-radius:12px;padding:25px 32px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,0.06);}
.section h2{font-size:1.25em;border-left:4px solid #667eea;padding-left:12px;margin-bottom:14px;color:#222;}
.section p{color:#555;margin-bottom:10px;}
.section ul{padding-left:20px;color:#555;}
.info-grid{display:grid;grid-template-columns:120px 1fr;gap:8px 20px;font-size:0.93em;}
.info-grid dt{color:#888;}
.cta{background:linear-gradient(135deg,#667eea,#764ba2);color:white;border-radius:12px;padding:25px 32px;text-align:center;margin-bottom:20px;}
.back{display:inline-block;margin:15px 0;color:#667eea;text-decoration:none;}
.faq-q{font-weight:bold;color:#222;margin-top:16px;}
.faq-a{color:#555;margin-top:4px;}"""

def render(city_code, lang, slug, h):
    c = CITIES[city_code]
    is_zh = (lang == "zh")
    dir_name = f"{city_code}hotels" if is_zh else f"{city_code}hotels-en"
    alt_dir = f"{city_code}hotels-en" if is_zh else f"{city_code}hotels"
    url = f"https://broadbandhk.com/pages/{dir_name}/{slug}.html"
    alt_url = f"https://broadbandhk.com/pages/{alt_dir}/{slug}.html"
    main_back = f"/pages/{city_code}hotel{'' if is_zh else '-en'}.html"
    main_label = f"{c['zh']}酒店" if is_zh else f"{c['en']} Hotels"
    name_h = html.escape(h["name"])
    loc_clean = html.escape(h.get("location","").replace("📍","").strip())
    tags_html = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in h.get("tags",[]))
    amount = h.get("amount","").strip()
    amount_plus = amount + ("+" if not is_zh and amount and not amount.endswith("+") else "")
    price_html = f"{html.escape(amount_plus)} <small>/ night</small>" if not is_zh else f"{html.escape(amount)} <small>／每晚起</small>"
    desc_clean = (h.get("desc","") or "")[:200].replace('"',"'")

    schema = {
        "@context":"https://schema.org","@type":"Hotel",
        "name": h["name"],
        "description": h.get("desc","")[:250],
        "url": url,
        "image": h.get("img",""),
        "address":{"@type":"PostalAddress","addressLocality":c["zh" if is_zh else "en"],"addressCountry":c["country"]},
        "geo":{"@type":"GeoCoordinates","latitude":c["lat"],"longitude":c["lng"]},
        "starRating":{"@type":"Rating","ratingValue":"5"},
        "priceRange": amount,
    }
    bc = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"首頁" if is_zh else "Home","item":"https://broadbandhk.com/"},
        {"@type":"ListItem","position":2,"name":main_label,"item":"https://broadbandhk.com"+main_back},
        {"@type":"ListItem","position":3,"name":h["name"]}
    ]}
    schemas = (
        f'<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json">{json.dumps(bc,ensure_ascii=False)}</script>'
    )

    # Title / description per language
    if is_zh:
        title = f"{h['name']}｜{c['zh']}酒店格價．2026住宿推介 - Broadband HK"
        desc_meta = f"{h['name']}{c['zh']}住宿：{loc_clean}。{desc_clean[:80]} Trip.com／Klook／Agoda 即時比較至抵。"
    else:
        title = f"{h['name']} | {c['en']} Hotel Price Comparison 2026 - Broadband HK"
        desc_meta = f"{h['name']} in {c['en']}. {loc_clean}. {desc_clean[:80]} Compare Trip.com / Klook / Agoda instantly."
    desc_meta = html.escape(desc_meta[:160])

    # Compose body texts
    about_label = "酒店簡介" if is_zh else "About this Hotel"
    tips_label = "預訂貼士" if is_zh else "Booking Tips"
    faq_label = "常見問題" if is_zh else "FAQ"
    info_label = "酒店資料" if is_zh else "Hotel Information"
    price_label = "優惠價" if is_zh else "Starting Price"
    cta_head = "立即比較 3 大平台格價" if is_zh else "Compare Prices on 3 Platforms"
    cta_sub = "Trip.com、Klook、Agoda 即時格價" if is_zh else "Trip.com, Klook and Agoda instant price comparison"
    btn_trip = "Trip.com 格價" if is_zh else "Compare on Trip.com"
    btn_klook = "Klook 格價" if is_zh else "Klook"
    btn_agoda = "Agoda 格價" if is_zh else "Agoda"
    back_label = "← 返回" + main_label if is_zh else "← Back to " + main_label
    city_loc = c["zh"] if is_zh else c["en"]

    faq_html = (f'''<div class="faq-q">Q：{h['name']}位於邊度？</div>
<div class="faq-a">A：{loc_clean or (city_loc+" 市區")}。具體地址及交通路線建議查 Trip.com／Klook 酒店頁面。</div>
<div class="faq-q">Q：{c['zh']}酒店 check-in 時間？</div>
<div class="faq-a">A：一般下午 2:00-3:00 入住；中午 12:00 退房。Early / Late check-in 視乎房況。</div>
<div class="faq-q">Q：邊個訂房平台最抵？</div>
<div class="faq-a">A：同酒店不同日期最抵平台都唔同，建議同時開 Trip.com／Klook／Agoda 三個 tab 格價。</div>
''' if is_zh else f'''<div class="faq-q">Q: Where is {h['name']} located?</div>
<div class="faq-a">A: {loc_clean or (city_loc+" downtown")}. Check Trip.com / Klook for the exact address and directions.</div>
<div class="faq-q">Q: What is the typical check-in time for {c['en']} hotels?</div>
<div class="faq-a">A: Usually 2:00-3:00 pm check-in; noon check-out. Early / late check-in subject to availability.</div>
<div class="faq-q">Q: Which booking platform is cheapest?</div>
<div class="faq-a">A: It varies by date and room type. Open Trip.com, Klook and Agoda side-by-side to compare before booking.</div>
''')

    return f"""<!DOCTYPE html>
<html lang="{'zh-HK' if is_zh else 'en'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc_meta}">
<meta name="keywords" content="{name_h}, {city_loc}{'酒店' if is_zh else ' hotel'}, 2026, Trip.com, Klook, Agoda">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc_meta}">
<meta property="og:image" content="{h.get('img','')}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{'zh_HK' if is_zh else 'en_HK'}">
<meta property="og:site_name" content="Broadband HK">
<meta name="geo.region" content="{c['country']}">
<meta name="geo.placename" content="{city_loc}">
<meta name="geo.position" content="{c['lat']};{c['lng']}">
<meta name="ICBM" content="{c['lat']}, {c['lng']}">
<meta name="timezone" content="{c['tz']}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="{'en' if is_zh else 'zh-Hant-HK'}" href="{alt_url}">
<link rel="alternate" hreflang="{'zh-Hant-HK' if is_zh else 'en'}" href="{url}">
{schemas}
<style>{common_css()}</style>
</head>
<body>
<div class="topbar">📍 <a href="/">Broadband HK</a> &gt; <a href="{main_back}">{main_label}</a> &gt; {name_h} | <a href="{main_back.replace('-en','') if is_zh else main_back.replace('.html','-en.html')}">{"EN" if is_zh else "中文"}</a></div>
<div class="hero">
<h1>{name_h}</h1>
<div class="stars">{html.escape(h.get('stars',''))}</div>
<div class="loc">{html.escape(h.get('location',''))}</div>
</div>
<div class="container">

<div class="card">
<div class="hotel-img" style="background-image:url('{h.get('img','')}');"></div>
<div class="body">
<div class="tags">{tags_html}</div>
<div class="rating"><span class="score">{html.escape(h.get('score',''))}</span><span>{html.escape(h.get('rtext',''))}</span></div>
<div class="desc">{html.escape(h.get('desc',''))}</div>
<div class="price">{price_html}</div>
<div class="platforms">
<a href="{TRIP}" class="btn btn-trip" target="_blank" rel="noopener noreferrer nofollow">{btn_trip}</a>
<a href="{KLOOK}" class="btn btn-klook" target="_blank" rel="noopener noreferrer nofollow">{btn_klook}</a>
<span class="btn btn-agoda" style="opacity:0.7;cursor:not-allowed;">{btn_agoda}</span>
</div>
</div>
</div>

<div class="section">
<h2>{info_label}</h2>
<dl class="info-grid">
<dt>{'酒店名稱' if is_zh else 'Hotel Name'}</dt><dd>{name_h}</dd>
<dt>{'城市' if is_zh else 'City'}</dt><dd>{city_loc}</dd>
<dt>{'位置' if is_zh else 'Location'}</dt><dd>{loc_clean}</dd>
<dt>{price_label}</dt><dd>{html.escape(amount_plus if not is_zh else amount)}{'' if not is_zh else ' 起'} {'/ night' if not is_zh else '／每晚'}</dd>
<dt>GPS</dt><dd>{c['lat']}°N, {c['lng']}°E</dd>
</dl>
</div>

<div class="section">
<h2>{about_label}</h2>
<p>{html.escape(h.get('desc',''))}</p>
<p>{'位於 '+city_loc+'，建議喺 Trip.com／Klook／Agoda 三大平台比較格價，同一酒店可差 15-30%。' if is_zh else 'Located in '+city_loc+'. Compare Trip.com, Klook and Agoda before booking — the same hotel can vary 15-30%.'}</p>
</div>

<div class="section">
<h2>{tips_label}</h2>
<ul>
{'<li><strong>提早預訂</strong>：旺季房價可升 50-100%。</li><li><strong>揀免費取消</strong>：彈性應對。</li><li><strong>三平台格價</strong>：Trip.com、Klook、Agoda 必比。</li>' if is_zh else '<li><strong>Book early</strong> — peak rates can rise 50-100%.</li><li><strong>Free cancellation</strong> — flexibility for changes.</li><li><strong>Compare 3 platforms</strong> — Trip.com / Klook / Agoda can differ 15-30%.</li>'}
</ul>
</div>

<div class="section">
<h2>{faq_label}</h2>
{faq_html}
</div>

<div class="cta">
<h3>{cta_head}</h3>
<p>{cta_sub}</p>
<div class="platforms">
<a href="{TRIP}" class="btn btn-trip" target="_blank" rel="noopener noreferrer nofollow" style="background:white;color:#287DFA;">{btn_trip}</a>
<a href="{KLOOK}" class="btn btn-klook" target="_blank" rel="noopener noreferrer nofollow" style="background:white;color:#FF5722;">{btn_klook}</a>
</div>
</div>

<a href="{main_back}" class="back">{back_label}</a>
</div>
</body>
</html>
"""

# ---- Main ----
all_hotels = {}  # {city: [(slug, zh_dict, en_dict), ...]}

for city in CITIES:
    zh_s = Path(f"pages/{city}hotel.html").read_text(encoding="utf-8")
    en_s = Path(f"pages/{city}hotel-en.html").read_text(encoding="utf-8")
    zh_cards = extract_cards(zh_s)
    en_cards = extract_cards(en_s)
    print(f"{city}: zh={len(zh_cards)}, en={len(en_cards)}")
    # Match by position (same index = same hotel)
    pairs = []
    for i, zh_h in enumerate(zh_cards):
        en_h = en_cards[i] if i < len(en_cards) else zh_h
        # Use zh name for slug basis; fall back to en
        slug = slugify(zh_h["name"], i+1) or slugify(en_h["name"], i+1)
        pairs.append((slug, zh_h, en_h))
    # Ensure unique slugs
    used = set(); final = []
    for slug, zh_h, en_h in pairs:
        orig = slug; j = 2
        while slug in used: slug = f"{orig}-{j}"; j += 1
        used.add(slug); final.append((slug, zh_h, en_h))
    all_hotels[city] = final

# Save mapping for rewrite step
Path("city_hotels_map.json").write_text(
    json.dumps({k:[(s,zh["name"],en["name"]) for s,zh,en in v] for k,v in all_hotels.items()},
               ensure_ascii=False, indent=2), encoding="utf-8")

# Generate subpages
Path("pages").mkdir(exist_ok=True)
for city, pairs in all_hotels.items():
    zh_dir = Path(f"pages/{city}hotels"); zh_dir.mkdir(exist_ok=True)
    en_dir = Path(f"pages/{city}hotels-en"); en_dir.mkdir(exist_ok=True)
    for slug, zh_h, en_h in pairs:
        (zh_dir/f"{slug}.html").write_text(render(city,"zh",slug,zh_h), encoding="utf-8")
        (en_dir/f"{slug}.html").write_text(render(city,"en",slug,en_h), encoding="utf-8")
    print(f"{city}: generated {len(pairs)*2} subpages")

# Rewrite main pages: wrap each card in <a>, remove .hotel-platforms
def rewrite_main(path, city, lang, pairs):
    p = Path(path); s = p.read_text(encoding="utf-8")
    head = s; tail = ""
    starts = [m.start() for m in re.finditer(r'<div class="hotel-card">', head)]
    dir_name = f"{city}hotels" if lang == "zh" else f"{city}hotels-en"
    for idx, start in enumerate(reversed(starts)):
        pair_index = len(starts) - 1 - idx
        if pair_index >= len(pairs): continue
        slug, _, _ = pairs[pair_index]
        # find end
        j = start + len('<div class="hotel-card">'); depth = 1
        while depth > 0 and j < len(head):
            mm = re.search(r'<div\b|</div>', head[j:])
            if not mm: break
            tag = mm.group(0); j += mm.end()
            if tag == '</div>': depth -= 1
            else: depth += 1
        card = head[start:j]
        # remove platforms block
        new_card = re.sub(r'<div class="hotel-platforms">.*?</div>\s*', '', card, flags=re.DOTALL)
        wrapped = (f'<a href="/pages/{dir_name}/{slug}.html" class="hotel-card-link" '
                   f'style="text-decoration:none;color:inherit;display:block;">{new_card}</a>')
        head = head[:start] + wrapped + head[j:]
    p.write_text(head + tail, encoding="utf-8")

for city, pairs in all_hotels.items():
    rewrite_main(f"pages/{city}hotel.html", city, "zh", pairs)
    rewrite_main(f"pages/{city}hotel-en.html", city, "en", pairs)
    print(f"{city}: main pages rewired")

print("\nDONE — Wave 2 complete")
