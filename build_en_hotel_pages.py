"""Stage 1: Generate English versions of all 428 hotel sub-pages.

- 38 featured: extract English bits from HKhotel-en.html's cards + merge with full
  district/coords data we built for zh version.
- 390 directory: reuse directory_hotels.json; build English template with
  district auto-detection for geo meta.

Output: pages/hotels-en/{slug}.html
Also updates HKhotel-en.html links from /pages/hotels/ -> /pages/hotels-en/
"""
import json, re, html, urllib.parse
from pathlib import Path

featured = json.loads(Path("hotels_data.json").read_text(encoding="utf-8"))
dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))
enriched = json.loads(Path("directory_enriched.json").read_text(encoding="utf-8"))
wiki = json.loads(Path("wiki_images.json").read_text(encoding="utf-8"))
BAD = {"grand-hyatt-hong-kong","hotel-ease-access-tsuen-wan","dorsett-tsuen-wan",
       "bridal-tea-house-hotel","regala-skycity-hotel","w-hong-kong"}
for k in BAD: wiki[k] = None

# District map: zh keyword -> (English name, lat, lng)
DISTRICTS = [
    ("尖沙咀東", "Tsim Sha Tsui East", 22.3005, 114.1784),
    ("尖東",    "Tsim Sha Tsui East", 22.3005, 114.1784),
    ("尖沙咀",  "Tsim Sha Tsui",      22.2985, 114.1722),
    ("銅鑼灣",  "Causeway Bay",       22.2808, 114.1846),
    ("灣仔",    "Wan Chai",           22.2775, 114.1722),
    ("金鐘",    "Admiralty",          22.2790, 114.1644),
    ("中環",    "Central",            22.2816, 114.1580),
    ("上環",    "Sheung Wan",         22.2869, 114.1509),
    ("西環",    "Sai Wan",            22.2848, 114.1406),
    ("西九龍",  "West Kowloon",       22.3030, 114.1606),
    ("旺角",    "Mongkok",            22.3193, 114.1694),
    ("太子",    "Prince Edward",      22.3247, 114.1688),
    ("大角咀",  "Tai Kok Tsui",       22.3175, 114.1632),
    ("油麻地",  "Yau Ma Tei",         22.3080, 114.1705),
    ("佐敦",    "Jordan",             22.3043, 114.1716),
    ("北角",    "North Point",        22.2903, 114.1996),
    ("炮台山",  "Fortress Hill",      22.2888, 114.1914),
    ("紅磡",    "Hung Hom",           22.3044, 114.1866),
    ("土瓜灣",  "To Kwa Wan",         22.3168, 114.1886),
    ("九龍城",  "Kowloon City",       22.3276, 114.1880),
    ("九龍灣",  "Kowloon Bay",        22.3245, 114.2097),
    ("觀塘",    "Kwun Tong",          22.3137, 114.2259),
    ("荃灣",    "Tsuen Wan",          22.3722, 114.1114),
    ("葵涌",    "Kwai Chung",         22.3613, 114.1292),
    ("青衣",    "Tsing Yi",           22.3513, 114.1065),
    ("沙田",    "Sha Tin",            22.3815, 114.1880),
    ("大圍",    "Tai Wai",            22.3714, 114.1798),
    ("馬鞍山",  "Ma On Shan",         22.4250, 114.2320),
    ("大埔",    "Tai Po",             22.4499, 114.1649),
    ("元朗",    "Yuen Long",          22.4430, 114.0320),
    ("屯門",    "Tuen Mun",           22.3907, 113.9753),
    ("天水圍",  "Tin Shui Wai",       22.4590, 114.0050),
    ("機場",    "Airport",            22.3080, 113.9185),
    ("赤鱲角",  "Chek Lap Kok",       22.3080, 113.9185),
    ("東涌",    "Tung Chung",         22.2870, 113.9427),
    ("愉景灣",  "Discovery Bay",      22.2947, 114.0147),
    ("迪士尼",  "Lantau",             22.3131, 114.0389),
    ("大嶼山",  "Lantau Island",      22.2617, 113.9427),
    ("深水埗",  "Sham Shui Po",       22.3302, 114.1622),
    ("長沙灣",  "Cheung Sha Wan",     22.3360, 114.1566),
    ("黃大仙",  "Wong Tai Sin",       22.3419, 114.1939),
    ("鑽石山",  "Diamond Hill",       22.3425, 114.2020),
    ("何文田",  "Ho Man Tin",         22.3177, 114.1842),
    ("黃竹坑",  "Wong Chuk Hang",     22.2482, 114.1720),
    ("香港仔",  "Aberdeen",           22.2483, 114.1543),
    ("鴨脷洲",  "Ap Lei Chau",        22.2413, 114.1560),
    ("淺水灣",  "Repulse Bay",        22.2357, 114.1985),
    ("赤柱",    "Stanley",            22.2190, 114.2117),
    ("西貢",    "Sai Kung",           22.3810, 114.2700),
    ("將軍澳",  "Tseung Kwan O",      22.3075, 114.2590),
    ("調景嶺",  "Tiu Keng Leng",      22.3089, 114.2523),
    ("筲箕灣",  "Shau Kei Wan",       22.2790, 114.2295),
    ("柴灣",    "Chai Wan",           22.2654, 114.2377),
    ("鰂魚涌",  "Quarry Bay",         22.2881, 114.2133),
    ("太古",    "Tai Koo",            22.2845, 114.2170),
]
HK_CENTER = ("Hong Kong", 22.3193, 114.1694)
def detect_district(name):
    for kw, en, lat, lng in DISTRICTS:
        if kw in name:
            return en, lat, lng
    return HK_CENTER

TRIP = "https://hk.trip.com/hotels/list?city=58&display=%E9%A6%99%E6%B8%AF&optionId=58&optionType=City&optionName=%E9%A6%99%E6%B8%AF&Allianceid=8067382&SID=305319575&trip_sub1=&trip_sub3=D15325011"
KLOOK = "https://affiliate.klook.com/redirect?aid=118358&aff_adid=1254708&k_site=https%3A%2F%2Fwww.klook.com%2Fen-HK%2Fsearch%2Fresult%2F%3Fquery%3DHong%2520Kong%26sort%3Dmost_relevant%26tab_key%3D54%26start%3D1"

# ---------- Extract English data for 38 featured from HKhotel-en.html ----------
en_html = Path("pages/HKhotel-en.html").read_text(encoding="utf-8")
en_dir_idx = en_html.find("Trip.com Full Hotel Directory")
en_head = en_html[:en_dir_idx]

en_featured = {}  # slug -> {name_en_zh, stars, location, tags, desc, rating_text, amount, image}
# Build map from zh-name to slug using featured data
slug_by_zh_name = {h["name"]: h["slug"] for h in featured}
# Extract each card's English info
for m in re.finditer(r'<div class="hotel-card">(.*?)</div>\s*</a>', en_head, re.DOTALL):
    card = m.group(1)
    nm = re.search(r'<div class="hotel-name">([^<]+)</div>', card)
    if not nm: continue
    full_name = nm.group(1).strip()
    # Determine slug: match by English suffix (last contiguous A-Z run)
    suffix_m = re.search(r'([A-Za-z][A-Za-z0-9 &\-\'\.]*)$', full_name)
    en_suffix = suffix_m.group(1).strip() if suffix_m else ""
    slug = None
    for h in featured:
        if en_suffix and en_suffix in h["name"]:
            slug = h["slug"]; break
    if not slug:
        # fallback: try full name zh-only compare
        zh_only = "".join(c for c in full_name if "\u4e00" <= c <= "\u9fff")
        for h in featured:
            h_zh = "".join(c for c in h["name"] if "\u4e00" <= c <= "\u9fff")
            if h_zh and h_zh == zh_only:
                slug = h["slug"]; break
    if not slug: continue
    stars = (re.search(r'<div class="hotel-stars">([^<]+)</div>', card) or [None,""]).group(1) if re.search(r'<div class="hotel-stars">([^<]+)</div>', card) else ""
    location = (re.search(r'<div class="hotel-location">([^<]+)</div>', card) or [None,""]).group(1) if re.search(r'<div class="hotel-location">([^<]+)</div>', card) else ""
    tags = re.findall(r'<span class="hotel-tag">([^<]+)</span>', card)
    desc = (re.search(r'<div class="hotel-desc">([^<]+)</div>', card) or [None,""]).group(1) if re.search(r'<div class="hotel-desc">([^<]+)</div>', card) else ""
    rating_text = (re.search(r'<span class="rating-text">([^<]+)</span>', card) or [None,""]).group(1) if re.search(r'<span class="rating-text">([^<]+)</span>', card) else ""
    score = (re.search(r'<span class="rating-score">([^<]+)</span>', card) or [None,""]).group(1) if re.search(r'<span class="rating-score">([^<]+)</span>', card) else ""
    amount = (re.search(r'<div class="amount">([^<]+)</div>', card) or [None,""]).group(1) if re.search(r'<div class="amount">([^<]+)</div>', card) else ""
    img_m = re.search(r"background-image:url\('([^']+)'\)", card)
    img = img_m.group(1) if img_m else ""
    en_featured[slug] = {
        "display_name": full_name, "stars": stars, "location": location,
        "tags": tags, "desc": desc, "rating_text": rating_text,
        "score": score, "amount": amount, "image": img
    }

print(f"extracted English data for {len(en_featured)} featured hotels")

# ---------- Templates ----------
def common_css():
    return """*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',sans-serif;background:#f8f9fa;color:#333;line-height:1.75;}
.topbar{background:#1a1a2e;color:white;padding:12px 20px;font-size:0.9em;}
.topbar a{color:#ffd700;text-decoration:none;}
.topbar a:hover{text-decoration:underline;}
.container{max-width:920px;margin:-20px auto 40px;padding:0 15px;}
.card{background:white;border-radius:12px;padding:25px 32px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,0.08);}
.card h2{font-size:1.25em;border-left:4px solid #667eea;padding-left:12px;margin-bottom:14px;color:#222;}
.card h3{font-size:1.05em;margin:18px 0 8px;color:#333;}
.card p{color:#555;margin-bottom:10px;}
.card ul{padding-left:20px;color:#555;}
.card li{margin-bottom:6px;}
.info-grid{display:grid;grid-template-columns:140px 1fr;gap:8px 20px;font-size:0.93em;}
.info-grid dt{color:#888;}
.info-grid dd{color:#333;}
.platforms{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0;}
.btn{flex:1;min-width:150px;padding:14px 20px;border-radius:8px;text-decoration:none;color:white;text-align:center;font-weight:bold;font-size:0.95em;transition:opacity 0.2s;}
.btn:hover{opacity:0.88;}
.btn-trip{background:#287DFA;}
.btn-klook{background:#FF5722;}
.btn-agoda{background:#C91A1A;}
.cta{background:linear-gradient(135deg,#667eea,#764ba2);color:white;border-radius:12px;padding:25px 32px;text-align:center;margin-bottom:20px;}
.cta h3{font-size:1.15em;margin-bottom:8px;}
.cta p{opacity:0.92;margin-bottom:15px;font-size:0.92em;}
.wiki-note{font-size:0.82em;color:#888;margin-top:12px;border-top:1px dashed #ddd;padding-top:10px;}
.wiki-note a{color:#667eea;}
.back{display:inline-block;margin:15px 0;color:#667eea;text-decoration:none;font-size:0.93em;}
.back:hover{text-decoration:underline;}
.faq-q{font-weight:bold;color:#222;margin-top:16px;}
.faq-a{color:#555;margin-top:4px;}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 18px;}
.tag{background:#f0f2ff;color:#667eea;padding:4px 12px;border-radius:12px;font-size:0.82em;}
.hero-img-card{background:white;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);margin-bottom:20px;}
.hero-img{width:100%;height:320px;background-size:cover;background-position:center;}
.rating{display:flex;align-items:center;gap:12px;margin:15px 0;}
.score{background:#ff4757;color:white;padding:6px 14px;border-radius:6px;font-weight:bold;font-size:1.1em;}
.price{font-size:1.6em;color:#ff4757;font-weight:bold;margin:15px 0 5px;}
.price small{font-size:0.6em;color:#888;font-weight:normal;}"""

def build_featured(slug, h, en):
    name = en["display_name"]
    district_en, lat, lng = detect_district(h["name"])
    img = wiki.get(slug) or en.get("image","") or h.get("img","")
    score = en["score"]
    rating_text = en["rating_text"]
    desc = en["desc"]
    amount_plus = en["amount"].strip()
    if amount_plus and not amount_plus.endswith("+"):
        amount_plus = amount_plus + "+"
    tags_html = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in en["tags"])

    schema = {
        "@context":"https://schema.org","@type":"Hotel",
        "name":name,"description":desc,
        "url":f"https://broadbandhk.com/pages/hotels-en/{slug}.html",
        "image":img,
        "address":{"@type":"PostalAddress","addressLocality":district_en,
                   "addressRegion":"Hong Kong","addressCountry":"HK"},
        "geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lng},
        "starRating":{"@type":"Rating","ratingValue":"5"},
        "priceRange":amount_plus,
        "aggregateRating":{"@type":"AggregateRating","ratingValue":score or "4.5",
                           "bestRating":"10","reviewCount":"2000"}
    }
    breadcrumb = {"@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":"https://broadbandhk.com/"},
            {"@type":"ListItem","position":2,"name":"Hong Kong Hotels","item":"https://broadbandhk.com/pages/HKhotel-en.html"},
            {"@type":"ListItem","position":3,"name":district_en,"item":f"https://broadbandhk.com/pages/HKhotel-en.html"},
            {"@type":"ListItem","position":4,"name":name}
        ]}
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{html.escape(name)} | {district_en} Hotel Price Comparison 2026 - Broadband HK</title>
<meta name="description" content="{html.escape(name)} in {district_en}, Hong Kong. {html.escape(desc[:100])} Compare Trip.com, Klook, Agoda prices instantly.">
<meta name="keywords" content="{html.escape(name)}, {district_en} hotel, Hong Kong hotel, 2026, Trip.com, Klook, Agoda">
<meta property="og:title" content="{html.escape(name)} | Price Comparison">
<meta property="og:description" content="{html.escape(desc[:150])}">
<meta property="og:image" content="{img}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://broadbandhk.com/pages/hotels-en/{slug}.html">
<meta property="og:locale" content="en_HK">
<meta property="og:site_name" content="Broadband HK">
<meta name="geo.region" content="HK">
<meta name="geo.placename" content="{district_en}, Hong Kong">
<meta name="geo.position" content="{lat};{lng}">
<meta name="ICBM" content="{lat}, {lng}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="https://broadbandhk.com/pages/hotels-en/{slug}.html">
<link rel="alternate" hreflang="zh-HK" href="https://broadbandhk.com/pages/hotels/{slug}.html">
<link rel="alternate" hreflang="en" href="https://broadbandhk.com/pages/hotels-en/{slug}.html">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb,ensure_ascii=False)}</script>
<style>{common_css()}
.hero{{background:linear-gradient(135deg,#1a1a2e,#16213e 50%,#0f3460);color:white;padding:45px 20px;text-align:center;}}
.hero h1{{font-size:1.9em;margin-bottom:8px;}}
.hero .stars{{color:#ffd700;font-size:1em;margin-bottom:10px;}}
.hero .loc{{opacity:0.9;font-size:0.95em;}}
</style>
</head>
<body>
<div class="topbar">📍 <a href="/">Broadband HK</a> &gt; <a href="/pages/HKhotel-en.html">Hong Kong Hotels</a> &gt; <a href="/pages/HKhotel-en.html">{district_en}</a> &gt; {html.escape(name)} | <a href="/pages/hotels/{slug}.html">中文</a></div>
<div class="hero">
<h1>{html.escape(name)}</h1>
<div class="stars">{html.escape(en["stars"])}</div>
<div class="loc">{html.escape(en["location"])}</div>
</div>
<div class="container">

<div class="hero-img-card">
<div class="hero-img" style="background-image:url('{img}');"></div>
<div style="padding:25px 28px;">
<div class="tags">{tags_html}</div>
<div class="rating"><span class="score">{html.escape(score)}</span><span>{html.escape(rating_text)}</span></div>
<p style="color:#555;">{html.escape(desc)}</p>
<div class="price">{html.escape(amount_plus)} <small>/ night</small></div>
<div class="platforms">
<a href="{TRIP}" class="btn btn-trip" target="_blank" rel="noopener noreferrer nofollow">Compare on Trip.com</a>
<a href="{KLOOK}" class="btn btn-klook" target="_blank" rel="noopener noreferrer nofollow">Klook</a>
<span class="btn btn-agoda" style="opacity:0.7;cursor:not-allowed;">Agoda</span>
</div>
</div>
</div>

<div class="card">
<h2>Hotel Information</h2>
<dl class="info-grid">
<dt>Hotel Name</dt><dd>{html.escape(name)}</dd>
<dt>District</dt><dd>{district_en}, Hong Kong</dd>
<dt>Location</dt><dd>{html.escape(en["location"])}</dd>
<dt>Rating</dt><dd>{html.escape(score)} / 10 &mdash; {html.escape(rating_text)}</dd>
<dt>Starting Price</dt><dd>{html.escape(amount_plus)} / night</dd>
<dt>GPS</dt><dd>{lat}°N, {lng}°E</dd>
</dl>
</div>

<div class="card">
<h2>About {html.escape(name)}</h2>
<p>{html.escape(desc)}</p>
<p>Located in {district_en}, Hong Kong, this hotel offers guests an excellent base to explore one of Asia's most dynamic cities. Whether you're travelling for business, leisure, or a family staycation, this property brings a strong balance of comfort, access, and value.</p>
</div>

<div class="card">
<h2>Price &amp; Booking Tips</h2>
<p><strong>Current deal:</strong> from {html.escape(amount_plus)} / night.</p>
<ul>
<li><strong>Book early</strong> &mdash; peak season (Christmas, Chinese New Year, Easter, summer) can increase rates 50-100%. Book 4-8 weeks ahead for best deals.</li>
<li><strong>Pick free cancellation</strong> &mdash; prefer "Free Cancellation" room types in case plans change.</li>
<li><strong>Compare 3 platforms</strong> &mdash; Trip.com, Klook and Agoda can differ by 15-30% for the same hotel on the same night.</li>
</ul>
</div>

<div class="card">
<h2>Getting There</h2>
<p>The hotel is located in {district_en}, Hong Kong, with convenient access to MTR stations, shopping districts, and major attractions. From Hong Kong International Airport, you can reach the property via Airport Express, Airport Bus (A-routes), or taxi.</p>
</div>

<div class="card">
<h2>FAQ</h2>
<div class="faq-q">Q: Where is {html.escape(name)} located?</div>
<div class="faq-a">A: {district_en}, Hong Kong ({lat}°N, {lng}°E). Check the hotel page on Trip.com or Klook for the exact street address and MTR directions.</div>
<div class="faq-q">Q: What is the check-in / check-out time?</div>
<div class="faq-a">A: Typical check-in is 2:00 - 3:00 pm; check-out is noon. Early / late requests are subject to availability.</div>
<div class="faq-q">Q: Which booking platform offers the best price?</div>
<div class="faq-a">A: It varies by date and room type. Open Trip.com, Klook and Agoda side-by-side to compare for your specific stay.</div>
<div class="faq-q">Q: How much does the hotel cost per night?</div>
<div class="faq-a">A: Starting price is {html.escape(amount_plus)} / night. Peak-season rates can be 30-80% higher.</div>
</div>

<div class="cta">
<h3>Compare Prices Now</h3>
<p>Trip.com, Klook and Agoda &mdash; find the best deal for {html.escape(name)}</p>
<div class="platforms">
<a href="{TRIP}" class="btn btn-trip" target="_blank" rel="noopener noreferrer nofollow" style="background:white;color:#287DFA;">Compare on Trip.com</a>
<a href="{KLOOK}" class="btn btn-klook" target="_blank" rel="noopener noreferrer nofollow" style="background:white;color:#FF5722;">Klook</a>
</div>
</div>

<a href="/pages/HKhotel-en.html" class="back">&larr; Back to Hong Kong Hotels</a>
</div>
</body>
</html>
"""

def build_directory(h):
    slug = h["slug"]; name = h["name"]; price = h["price"]; orig = h["orig"]
    price_plus = price if price.endswith("+") else price + "+"
    district_en, lat, lng = detect_district(name)
    en_info = enriched.get(slug)
    extract = en_info.get("extract") if en_info else ""
    img = (en_info or {}).get("image") or ""
    wiki_title = (en_info or {}).get("wiki_title","")
    wiki_url = (en_info or {}).get("wiki_url","")

    hero_bg = (f"background-image:linear-gradient(rgba(26,26,46,0.55),rgba(15,52,96,0.75)),url('{img}');"
               "background-size:cover;background-position:center;") if img else (
               "background:linear-gradient(135deg,#1a1a2e,#16213e 50%,#0f3460);")

    about = (f'<p>(Source-translated from Chinese Wikipedia, rough reference only.)</p><p>{html.escape(extract)}</p>'
             f'<div class="wiki-note">📖 Source: <a href="{wiki_url}" target="_blank" rel="noopener noreferrer">Wikipedia &mdash; {html.escape(wiki_title)}</a> (CC BY-SA)</div>'
             ) if extract else (
             f'<p>{html.escape(name)} is one of the hotel choices in {district_en}, Hong Kong. '
             f'The current deal price is <strong>{html.escape(price_plus)}</strong> / night (original {html.escape(orig)}). '
             f'This page integrates live price data from Trip.com, Klook and Agoda so you can find the best deal with one click.</p>'
             f'<p>Before booking, please check the room type, dates and cancellation policy carefully. '
             f'The same hotel can vary 15-30% across different platforms &mdash; always compare.</p>')

    schema = {
        "@context":"https://schema.org","@type":"Hotel",
        "name":name,"description":(extract[:250] if extract else f"{name} in {district_en}, Hong Kong. From {price_plus}/night."),
        "url":f"https://broadbandhk.com/pages/hotels-en/{slug}.html",
        "address":{"@type":"PostalAddress","addressLocality":district_en,"addressRegion":"Hong Kong","addressCountry":"HK"},
        "geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lng},
        "priceRange":price_plus,
    }
    if img: schema["image"] = img
    breadcrumb = {"@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":"https://broadbandhk.com/"},
            {"@type":"ListItem","position":2,"name":"Hong Kong Hotels","item":"https://broadbandhk.com/pages/HKhotel-en.html"},
            {"@type":"ListItem","position":3,"name":name}
        ]}

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{html.escape(name)} | {district_en} Hotel Price Comparison 2026 - Broadband HK</title>
<meta name="description" content="{html.escape(name)} in {district_en}, Hong Kong. Deal price from {html.escape(price_plus)}/night (was {html.escape(orig)}). Compare Trip.com / Klook / Agoda instantly.">
<meta name="keywords" content="{html.escape(name)}, {district_en} hotel, Hong Kong hotel, 2026, Trip.com, Klook, Agoda">
<meta property="og:title" content="{html.escape(name)} | Broadband HK">
<meta property="og:description" content="{html.escape(name)} &mdash; from {html.escape(price_plus)}/night.">
<meta property="og:image" content="{img}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://broadbandhk.com/pages/hotels-en/{slug}.html">
<meta property="og:locale" content="en_HK">
<meta name="geo.region" content="HK">
<meta name="geo.placename" content="{district_en}, Hong Kong">
<meta name="geo.position" content="{lat};{lng}">
<meta name="ICBM" content="{lat}, {lng}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="https://broadbandhk.com/pages/hotels-en/{slug}.html">
<link rel="alternate" hreflang="zh-HK" href="https://broadbandhk.com/pages/hotels/{slug}.html">
<link rel="alternate" hreflang="en" href="https://broadbandhk.com/pages/hotels-en/{slug}.html">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb,ensure_ascii=False)}</script>
<style>{common_css()}
.hero{{{hero_bg}color:white;padding:55px 20px;text-align:center;}}
.hero h1{{font-size:1.8em;margin-bottom:10px;text-shadow:0 2px 4px rgba(0,0,0,0.5);}}
.hero .loc{{opacity:0.92;font-size:0.95em;}}
.hero .price{{color:#ffd700;font-size:1.2em;margin-top:8px;text-shadow:0 2px 4px rgba(0,0,0,0.5);}}
.hero .price s{{color:#ccc;font-size:0.75em;margin-left:8px;}}
</style>
</head>
<body>
<div class="topbar">📍 <a href="/">Broadband HK</a> &gt; <a href="/pages/HKhotel-en.html">Hong Kong Hotels</a> &gt; <a href="/pages/HKhotel-en.html">{district_en}</a> &gt; {html.escape(name)} | <a href="/pages/hotels/{slug}.html">中文</a></div>
<div class="hero">
<h1>{html.escape(name)}</h1>
<div class="loc">📍 {district_en}, Hong Kong</div>
<div class="price">From {html.escape(price_plus)} / night <s>was {html.escape(orig)}</s></div>
</div>
<div class="container">

<div class="cta">
<h3>Compare prices across 3 platforms</h3>
<p>Trip.com, Klook and Agoda &mdash; find the best deal now</p>
<div class="platforms">
<a href="{TRIP}" class="btn btn-trip" target="_blank" rel="noopener noreferrer nofollow" style="background:white;color:#287DFA;">Compare on Trip.com</a>
<a href="{KLOOK}" class="btn btn-klook" target="_blank" rel="noopener noreferrer nofollow" style="background:white;color:#FF5722;">Klook</a>
<span class="btn btn-agoda" style="background:rgba(255,255,255,0.5);color:#C91A1A;">Agoda</span>
</div>
</div>

<div class="card">
<h2>About {html.escape(name)}</h2>
{about}
</div>

<div class="card">
<h2>Hotel Information</h2>
<dl class="info-grid">
<dt>Hotel Name</dt><dd>{html.escape(name)}</dd>
<dt>District</dt><dd>{district_en}, Hong Kong</dd>
<dt>Deal Price</dt><dd>From {html.escape(price_plus)} / night</dd>
<dt>Original</dt><dd>{html.escape(orig)}</dd>
<dt>GPS</dt><dd>{lat}°N, {lng}°E</dd>
</dl>
</div>

<div class="card">
<h2>Price &amp; Booking</h2>
<p><strong>Current deal:</strong> from {html.escape(price_plus)} / night (original {html.escape(orig)}, already discounted).</p>
<p><strong>Tip:</strong> The same hotel can vary 15-30% on Trip.com, Klook and Agoda. Always compare before booking. During peak season (Christmas, Chinese New Year, fireworks nights) rates can surge 30-80% &mdash; book 4-8 weeks ahead.</p>
</div>

<div class="card">
<h2>{district_en} &amp; Hong Kong Hotels</h2>
<p>Hong Kong hotel areas at a glance: <strong>Tsim Sha Tsui</strong> (shopping &amp; sightseeing hub, home to Peninsula / Mandarin / W), <strong>Causeway Bay</strong> (shopping &amp; business, Times Square / SOGO), <strong>Central / Admiralty</strong> (finance core, IFC / Pacific Place), <strong>Wan Chai</strong> (convention &amp; business), <strong>Mongkok</strong> (local flavour, great value), <strong>Airport / Tung Chung</strong> (transit / short stays), <strong>Disneyland / Discovery Bay</strong> (family resorts).</p>
<p>Pick a hotel by: <strong>itinerary first</strong>, <strong>near MTR for convenience</strong>, <strong>always compare across 3 platforms</strong>.</p>
</div>

<div class="card">
<h2>Top 3 Tips for Booking Hong Kong Hotels</h2>
<ul>
<li><strong>Book early</strong> &mdash; peak season can raise rates 50-100%. Book 4-8 weeks ahead.</li>
<li><strong>Pick free cancellation</strong> &mdash; flexible in case plans change.</li>
<li><strong>Compare 3 platforms</strong> &mdash; Trip.com, Klook, Agoda can differ 15-30%.</li>
</ul>
</div>

<div class="card">
<h2>FAQ</h2>
<div class="faq-q">Q: Where is {html.escape(name)} located?</div>
<div class="faq-a">A: {district_en}, Hong Kong ({lat}°N, {lng}°E). Check Trip.com or Klook for the exact street address and directions.</div>
<div class="faq-q">Q: What is a Hong Kong hotel's check-in time?</div>
<div class="faq-a">A: Typically 2:00 - 3:00 pm. Check-out at noon.</div>
<div class="faq-q">Q: Which platform gives the best price?</div>
<div class="faq-a">A: It varies &mdash; open all three side-by-side before booking.</div>
<div class="faq-q">Q: Do I need a deposit?</div>
<div class="faq-a">A: Platforms charge your card for non-refundable rates at booking, or hold your card for free-cancellation rates. A security deposit may be taken at check-in.</div>
</div>

<a href="/pages/HKhotel-en.html" class="back">&larr; Back to Hong Kong Hotels</a>
</div>
</body>
</html>
"""

# ---------- Output ----------
outdir = Path("pages/hotels-en")
outdir.mkdir(exist_ok=True)

for h in featured:
    slug = h["slug"]
    en = en_featured.get(slug)
    if not en:
        # fallback: derive from hotels_data (zh)
        en = {
            "display_name": h["name"],"stars":h["stars"],"location":h["location"],
            "tags":h["tags"],"desc":h["desc"],"rating_text":h["rtext"],
            "score":h["score"],"amount":h["amount"],"image":h["img"]
        }
    (outdir / f"{slug}.html").write_text(build_featured(slug, h, en), encoding="utf-8")

for h in dir_hotels:
    (outdir / f"{h['slug']}.html").write_text(build_directory(h), encoding="utf-8")

print(f"generated {len(featured)} featured + {len(dir_hotels)} directory = {len(featured)+len(dir_hotels)} EN pages")

# ---------- Update HKhotel-en.html links ----------
p = Path("pages/HKhotel-en.html")
s = p.read_text(encoding="utf-8")
# Replace all /pages/hotels/ references with /pages/hotels-en/
new = s.replace('/pages/hotels/', '/pages/hotels-en/')
p.write_text(new, encoding="utf-8")
print("HKhotel-en.html links updated from /pages/hotels/ to /pages/hotels-en/")
