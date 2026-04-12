"""Enhance SEO/GEO on all 390 directory hotel pages.

Detects district from hotel name, adds geo.position / ICBM / GeoCoordinates
schema.  Re-renders enriched + basic pages with full SEO/GEO while preserving
wikipedia content where available.
"""
import json, html, re
from pathlib import Path

hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))
enriched = json.loads(Path("directory_enriched.json").read_text(encoding="utf-8"))

# District keyword -> (中文 name, lat, lng)
DISTRICTS = [
    ("尖沙咀東", "尖沙咀東", 22.3005, 114.1784),
    ("尖東",    "尖沙咀東", 22.3005, 114.1784),
    ("尖沙咀",  "尖沙咀",   22.2985, 114.1722),
    ("銅鑼灣",  "銅鑼灣",   22.2808, 114.1846),
    ("灣仔",    "灣仔",     22.2775, 114.1722),
    ("金鐘",    "金鐘",     22.2790, 114.1644),
    ("中環",    "中環",     22.2816, 114.1580),
    ("上環",    "上環",     22.2869, 114.1509),
    ("西環",    "西環",     22.2848, 114.1406),
    ("中西區",  "中西區",   22.2820, 114.1500),
    ("旺角",    "旺角",     22.3193, 114.1694),
    ("太子",    "太子",     22.3247, 114.1688),
    ("大角咀",  "大角咀",   22.3175, 114.1632),
    ("油麻地",  "油麻地",   22.3080, 114.1705),
    ("佐敦",    "佐敦",     22.3043, 114.1716),
    ("北角",    "北角",     22.2903, 114.1996),
    ("炮台山",  "炮台山",   22.2888, 114.1914),
    ("紅磡",    "紅磡",     22.3044, 114.1866),
    ("土瓜灣",  "土瓜灣",   22.3168, 114.1886),
    ("九龍城",  "九龍城",   22.3276, 114.1880),
    ("九龍灣",  "九龍灣",   22.3245, 114.2097),
    ("觀塘",    "觀塘",     22.3137, 114.2259),
    ("荃灣",    "荃灣",     22.3722, 114.1114),
    ("葵涌",    "葵涌",     22.3613, 114.1292),
    ("青衣",    "青衣",     22.3513, 114.1065),
    ("沙田",    "沙田",     22.3815, 114.1880),
    ("大圍",    "大圍",     22.3714, 114.1798),
    ("馬鞍山",  "馬鞍山",   22.4250, 114.2320),
    ("大埔",    "大埔",     22.4499, 114.1649),
    ("元朗",    "元朗",     22.4430, 114.0320),
    ("屯門",    "屯門",     22.3907, 113.9753),
    ("天水圍",  "天水圍",   22.4590, 114.0050),
    ("機場",    "赤鱲角",   22.3080, 113.9185),
    ("赤鱲角",  "赤鱲角",   22.3080, 113.9185),
    ("東涌",    "東涌",     22.2870, 113.9427),
    ("愉景灣",  "愉景灣",   22.2947, 114.0147),
    ("迪士尼",  "大嶼山",   22.3131, 114.0389),
    ("大嶼山",  "大嶼山",   22.2617, 113.9427),
    ("深水埗",  "深水埗",   22.3302, 114.1622),
    ("長沙灣",  "長沙灣",   22.3360, 114.1566),
    ("黃大仙",  "黃大仙",   22.3419, 114.1939),
    ("鑽石山",  "鑽石山",   22.3425, 114.2020),
    ("何文田",  "何文田",   22.3177, 114.1842),
    ("黃竹坑",  "黃竹坑",   22.2482, 114.1720),
    ("香港仔",  "香港仔",   22.2483, 114.1543),
    ("鴨脷洲",  "鴨脷洲",   22.2413, 114.1560),
    ("淺水灣",  "淺水灣",   22.2357, 114.1985),
    ("赤柱",    "赤柱",     22.2190, 114.2117),
    ("西貢",    "西貢",     22.3810, 114.2700),
    ("將軍澳",  "將軍澳",   22.3075, 114.2590),
    ("調景嶺",  "調景嶺",   22.3089, 114.2523),
    ("筲箕灣",  "筲箕灣",   22.2790, 114.2295),
    ("柴灣",    "柴灣",     22.2654, 114.2377),
    ("鰂魚涌",  "鰂魚涌",   22.2881, 114.2133),
    ("太古",    "太古",     22.2845, 114.2170),
    ("銅鑼",    "銅鑼灣",   22.2808, 114.1846),
]
HK_CENTER = ("香港", 22.3193, 114.1694)

def detect_district(name):
    for kw, zh, lat, lng in DISTRICTS:
        if kw in name:
            return zh, lat, lng
    return HK_CENTER

TRIP = "https://hk.trip.com/hotels/list?city=58&display=%E9%A6%99%E6%B8%AF&optionId=58&optionType=City&optionName=%E9%A6%99%E6%B8%AF&Allianceid=8067382&SID=305319575&trip_sub1=&trip_sub3=D15325011"
KLOOK = "https://affiliate.klook.com/redirect?aid=118358&aff_adid=1254708&k_site=https%3A%2F%2Fwww.klook.com%2Fzh-HK%2Fsearch%2Fresult%2F%3Fquery%3D%25E9%25A6%2599%25E6%25B8%25AF%26sort%3Dmost_relevant%26tab_key%3D54%26start%3D1"

def render(h):
    slug = h["slug"]; name = h["name"]; price = h["price"]; orig = h["orig"]
    district_zh, lat, lng = detect_district(name)
    en_info = enriched.get(slug)
    extract = en_info["extract"] if en_info else ""
    img = (en_info or {}).get("image") or ""
    wiki_title = (en_info or {}).get("wiki_title","")
    wiki_url = (en_info or {}).get("wiki_url","")

    name_h = html.escape(name); price_h = html.escape(price); orig_h = html.escape(orig)
    extract_h = html.escape(extract)
    desc_meta = f"{name}位於香港{district_zh}，優惠價{price}起（原價{orig}）。{extract[:60]} Trip.com／Klook／Agoda 即時格價比較。" if extract else f"{name}位於香港{district_zh}，優惠價{price}起（原價{orig}）。Trip.com／Klook／Agoda 即時格價比較至抵。"
    desc_meta = html.escape(desc_meta[:160])

    hotel_schema = {
        "@context":"https://schema.org","@type":"Hotel",
        "name":name,
        "description": (extract[:250] if extract else f"{name}香港{district_zh}住宿，優惠價{price}起。"),
        "url":f"https://broadbandhk.com/pages/hotels/{slug}.html",
        "address":{
            "@type":"PostalAddress",
            "addressLocality":district_zh,
            "addressRegion":"Hong Kong",
            "addressCountry":"HK"
        },
        "geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lng},
        "priceRange":price,
    }
    if img:
        hotel_schema["image"] = img
    breadcrumb = {
        "@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"首頁","item":"https://broadbandhk.com/"},
            {"@type":"ListItem","position":2,"name":"香港酒店推介","item":"https://broadbandhk.com/pages/HKhotel.html"},
            {"@type":"ListItem","position":3,"name":name}
        ]}
    schemas = (
        f'<script type="application/ld+json">{json.dumps(hotel_schema,ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json">{json.dumps(breadcrumb,ensure_ascii=False)}</script>'
    )

    hero_bg = (f"background-image:linear-gradient(rgba(26,26,46,0.55),rgba(15,52,96,0.75)),url('{img}');"
               "background-size:cover;background-position:center;") if img else (
               "background:linear-gradient(135deg,#1a1a2e,#16213e 50%,#0f3460);")

    about_html = (
        f'<p>{extract_h}</p>'
        f'<div class="wiki-note">📖 資料來源：<a href="{wiki_url}" target="_blank" rel="noopener noreferrer">維基百科 — {html.escape(wiki_title)}</a>（CC BY-SA 授權）</div>'
    ) if extract else (
        f'<p>{name_h}係香港{district_zh}嘅酒店選擇之一，目前 Trip.com 優惠價 <strong>{price_h}</strong>／晚起（原價 {orig_h}）。此頁面整合 Trip.com、Klook、Agoda 三大平台實時格價，幫你一次搵至抵住宿。</p>'
        f'<p>預訂前建議睇清楚房型、入住日期、取消政策。同一間酒店喺不同平台可差 15-30%，格價必做。</p>'
    )

    return f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{name_h}｜{district_zh}酒店格價．2026香港住宿推介 - Broadband HK</title>
<meta name="description" content="{desc_meta}">
<meta name="keywords" content="{name_h}, {district_zh}酒店, 香港酒店, 格價, 2026, Trip.com, Klook, Agoda">
<meta property="og:title" content="{name_h}｜{district_zh}酒店格價．Broadband HK">
<meta property="og:description" content="{desc_meta}">
<meta property="og:image" content="{img}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://broadbandhk.com/pages/hotels/{slug}.html">
<meta property="og:locale" content="zh_HK">
<meta property="og:site_name" content="Broadband HK">
<meta name="geo.region" content="HK">
<meta name="geo.placename" content="{district_zh}, Hong Kong">
<meta name="geo.position" content="{lat};{lng}">
<meta name="ICBM" content="{lat}, {lng}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="https://broadbandhk.com/pages/hotels/{slug}.html">
{schemas}
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang TC','Microsoft JhengHei',sans-serif;background:#f8f9fa;color:#333;line-height:1.75;}}
.topbar{{background:#1a1a2e;color:white;padding:12px 20px;font-size:0.9em;}}
.topbar a{{color:#ffd700;text-decoration:none;}}
.hero{{{hero_bg}color:white;padding:60px 20px;text-align:center;}}
.hero h1{{font-size:1.85em;margin-bottom:10px;text-shadow:0 2px 4px rgba(0,0,0,0.5);}}
.hero .loc{{opacity:0.92;font-size:0.95em;margin-top:6px;}}
.hero .price{{color:#ffd700;font-size:1.2em;margin-top:8px;text-shadow:0 2px 4px rgba(0,0,0,0.5);}}
.hero .price s{{color:#ccc;font-size:0.75em;margin-left:8px;}}
.container{{max-width:900px;margin:-20px auto 40px;padding:0 15px;}}
.card{{background:white;border-radius:12px;padding:28px 32px;box-shadow:0 2px 8px rgba(0,0,0,0.08);margin-bottom:20px;}}
.card h2{{font-size:1.25em;border-left:4px solid #667eea;padding-left:12px;margin-bottom:14px;color:#222;}}
.card p{{color:#555;margin-bottom:10px;}}
.card ul{{padding-left:20px;color:#555;}}
.card li{{margin-bottom:6px;}}
.info-grid{{display:grid;grid-template-columns:120px 1fr;gap:8px 20px;font-size:0.93em;}}
.info-grid dt{{color:#888;}}
.info-grid dd{{color:#333;}}
.wiki-note{{font-size:0.82em;color:#888;margin-top:12px;border-top:1px dashed #ddd;padding-top:10px;}}
.wiki-note a{{color:#667eea;}}
.platforms{{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0;}}
.btn{{flex:1;min-width:150px;padding:14px 20px;border-radius:8px;text-decoration:none;color:white;text-align:center;font-weight:bold;font-size:0.95em;}}
.btn:hover{{opacity:0.88;}}
.btn-trip{{background:#287DFA;}}
.btn-klook{{background:#FF5722;}}
.btn-agoda{{background:#C91A1A;}}
.cta{{background:linear-gradient(135deg,#667eea,#764ba2);color:white;border-radius:12px;padding:25px;text-align:center;margin-bottom:20px;}}
.back{{display:inline-block;margin:10px 0;color:#667eea;text-decoration:none;}}
</style>
</head>
<body>
<div class="topbar">📍 <a href="/">Broadband HK</a> ＞ <a href="/pages/HKhotel.html">香港酒店推介</a> ＞ <a href="/pages/HKhotel.html">{district_zh}</a> ＞ {name_h}</div>
<div class="hero">
<h1>{name_h}</h1>
<div class="loc">📍 香港 {district_zh}</div>
<div class="price">由 {price_h}／晚起 <s>原價 {orig_h}</s></div>
</div>
<div class="container">

<div class="cta">
<h2 style="color:white;border:0;">立即比較三大平台格價</h2>
<p style="opacity:0.92;margin:8px 0 15px;">Trip.com、Klook、Agoda 即時格價搵最抵</p>
<div class="platforms">
<a href="{TRIP}" class="btn btn-trip" target="_blank" rel="noopener noreferrer nofollow" style="background:white;color:#287DFA;">Trip.com 格價</a>
<a href="{KLOOK}" class="btn btn-klook" target="_blank" rel="noopener noreferrer nofollow" style="background:white;color:#FF5722;">Klook 格價</a>
<span class="btn btn-agoda" style="background:rgba(255,255,255,0.5);color:#C91A1A;">Agoda 格價</span>
</div>
</div>

<div class="card">
<h2>關於 {name_h}</h2>
{about_html}
</div>

<div class="card">
<h2>酒店資料</h2>
<dl class="info-grid">
<dt>酒店名稱</dt><dd>{name_h}</dd>
<dt>所在地區</dt><dd>香港 {district_zh}</dd>
<dt>優惠價</dt><dd>由 {price_h}／晚起</dd>
<dt>原價</dt><dd>{orig_h}</dd>
<dt>GPS 座標</dt><dd>{lat}°N, {lng}°E</dd>
</dl>
</div>

<div class="card">
<h2>價格與預訂</h2>
<p><strong>目前優惠價：</strong>由 {price_h}／晚起（原價 {orig_h}，已折扣）</p>
<p><strong>建議：</strong>同一間酒店喺 Trip.com、Klook、Agoda 價錢可差 15-30%，逐個比較。旺季（聖誕、農曆新年、煙花期）加 30-80%，提早 4-8 週預訂。</p>
</div>

<div class="card">
<h2>{district_zh}酒店簡介</h2>
<p>香港酒店按地區：<strong>尖沙咀</strong>（購物觀光，半島／文華／W）、<strong>銅鑼灣</strong>（購物商業，時代廣場／崇光）、<strong>中環／金鐘</strong>（商務金融，IFC／太古廣場）、<strong>灣仔</strong>（會展商務）、<strong>旺角</strong>（本地風味、性價比高）、<strong>機場／東涌</strong>（過境短住）、<strong>迪士尼／愉景灣</strong>（親子度假）。</p>
<p>揀酒店：<strong>行程優先</strong>、<strong>交通方便（近地鐵站）</strong>、<strong>三平台格價</strong>。</p>
</div>

<div class="card">
<h2>預訂香港酒店 3 大貼士</h2>
<ul>
<li><strong>提早預訂</strong>：旺季房價升 50-100%，提早 4-8 週鎖定優惠。</li>
<li><strong>揀免費取消</strong>：優先 Free Cancellation，行程有變唔蝕錢。</li>
<li><strong>三大平台格價</strong>：Trip.com、Klook、Agoda 同酒店可差 15-30%。</li>
</ul>
</div>

<div class="card">
<h2>常見問題 FAQ</h2>
<p><strong>Q: {name_h}位置喺邊？</strong><br>A: 位於香港 {district_zh}，GPS 座標 {lat}°N, {lng}°E。具體地址及交通請查 Trip.com／Klook 酒店頁面。</p>
<p><strong>Q: 香港酒店 check-in 時間？</strong><br>A: 一般 check-in 下午 2:00-3:00、check-out 中午 12:00。</p>
<p><strong>Q: 邊個訂房平台最抵？</strong><br>A: 同酒店不同日子不同平台最抵，同時開三 tab 格價先訂。</p>
<p><strong>Q: 需要訂金嗎？</strong><br>A: 預訂時扣卡費（Non-refundable）或保留卡（Free Cancellation）。Check-in 時再押金。</p>
</div>

<a href="/pages/HKhotel.html" class="back">← 返回香港酒店推介列表</a>
</div>
</body>
</html>
"""

count = 0
for h in hotels:
    path = Path(f"pages/hotels/{h['slug']}.html")
    path.write_text(render(h), encoding="utf-8")
    count += 1
print(f"Re-rendered {count} directory pages with full SEO/GEO")
