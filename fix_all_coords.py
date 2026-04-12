"""Final coord fix:
1. Apply wiki_coords (filtered to HK bbox) to subpages.
2. For pages that still have generic HK-center coord AND have no real data,
   REMOVE geo meta / GPS display so we don't show fake coordinates.
"""
import json, re
from pathlib import Path

osm = json.loads(Path("osm_meta.json").read_text(encoding="utf-8"))
wiki_coords = json.loads(Path("wiki_coords.json").read_text(encoding="utf-8"))

# HK bbox filter
def in_hk(lat, lng):
    return 22.15 <= lat <= 22.58 and 113.82 <= lng <= 114.44

# Merge: osm coords + wiki coords (wiki only where osm doesn't have)
real_coords = {}
for s, m in osm.items():
    if m.get("lat") and m.get("lng"): real_coords[s] = (m["lat"], m["lng"])
for s, (lat, lng) in wiki_coords.items():
    if s in real_coords: continue
    if in_hk(float(lat), float(lng)):
        real_coords[s] = (float(lat), float(lng))

print(f"hotels with real coords: {len(real_coords)}")

# HK districts
DISTRICTS_ZH_EN = [
    (22.2985,114.1722,"尖沙咀","Tsim Sha Tsui"),
    (22.3005,114.1784,"尖沙咀東","Tsim Sha Tsui East"),
    (22.2808,114.1846,"銅鑼灣","Causeway Bay"),
    (22.2775,114.1722,"灣仔","Wan Chai"),
    (22.2790,114.1644,"金鐘","Admiralty"),
    (22.2816,114.1580,"中環","Central"),
    (22.2869,114.1509,"上環","Sheung Wan"),
    (22.2848,114.1406,"西環","Sai Wan"),
    (22.3030,114.1606,"西九龍","West Kowloon"),
    (22.3193,114.1694,"旺角","Mongkok"),
    (22.3247,114.1688,"太子","Prince Edward"),
    (22.3175,114.1632,"大角咀","Tai Kok Tsui"),
    (22.3080,114.1705,"油麻地","Yau Ma Tei"),
    (22.3043,114.1716,"佐敦","Jordan"),
    (22.2903,114.1996,"北角","North Point"),
    (22.2888,114.1914,"炮台山","Fortress Hill"),
    (22.3044,114.1866,"紅磡","Hung Hom"),
    (22.3168,114.1886,"土瓜灣","To Kwa Wan"),
    (22.3276,114.1880,"九龍城","Kowloon City"),
    (22.3245,114.2097,"九龍灣","Kowloon Bay"),
    (22.3137,114.2259,"觀塘","Kwun Tong"),
    (22.3722,114.1114,"荃灣","Tsuen Wan"),
    (22.3613,114.1292,"葵涌","Kwai Chung"),
    (22.3513,114.1065,"青衣","Tsing Yi"),
    (22.3815,114.1880,"沙田","Sha Tin"),
    (22.4250,114.2320,"馬鞍山","Ma On Shan"),
    (22.4499,114.1649,"大埔","Tai Po"),
    (22.4430,114.0320,"元朗","Yuen Long"),
    (22.3907,113.9753,"屯門","Tuen Mun"),
    (22.4590,114.0050,"天水圍","Tin Shui Wai"),
    (22.2870,113.9427,"東涌","Tung Chung"),
    (22.3080,113.9185,"赤鱲角","Chek Lap Kok"),
    (22.2947,114.0147,"愉景灣","Discovery Bay"),
    (22.2617,113.9427,"大嶼山","Lantau Island"),
    (22.3302,114.1622,"深水埗","Sham Shui Po"),
    (22.3360,114.1566,"長沙灣","Cheung Sha Wan"),
    (22.3419,114.1939,"黃大仙","Wong Tai Sin"),
    (22.3425,114.2020,"鑽石山","Diamond Hill"),
    (22.3177,114.1842,"何文田","Ho Man Tin"),
    (22.2482,114.1720,"黃竹坑","Wong Chuk Hang"),
    (22.2483,114.1543,"香港仔","Aberdeen"),
    (22.2413,114.1560,"鴨脷洲","Ap Lei Chau"),
    (22.2357,114.1985,"淺水灣","Repulse Bay"),
    (22.2190,114.2117,"赤柱","Stanley"),
    (22.3810,114.2700,"西貢","Sai Kung"),
    (22.3075,114.2590,"將軍澳","Tseung Kwan O"),
    (22.3089,114.2523,"調景嶺","Tiu Keng Leng"),
    (22.2790,114.2295,"筲箕灣","Shau Kei Wan"),
    (22.2654,114.2377,"柴灣","Chai Wan"),
    (22.2881,114.2133,"鰂魚涌","Quarry Bay"),
    (22.2845,114.2170,"太古","Tai Koo"),
    (22.5020,114.1280,"上水","Sheung Shui"),
    (22.4946,114.1386,"粉嶺","Fanling"),
]
def nearest(lat, lng):
    best = None; bd = 1e9
    for dlat, dlng, zh, en in DISTRICTS_ZH_EN:
        d = (lat-dlat)**2 + (lng-dlng)**2
        if d < bd: bd = d; best = (zh, en)
    return best

def apply_coords(page_dir, slug, lat, lng, lang):
    p = Path(f"pages/{page_dir}/{slug}.html")
    if not p.exists(): return False
    s = p.read_text(encoding="utf-8")
    zh, en = nearest(lat, lng)
    placename = f"{zh}, Hong Kong" if lang == "zh" else f"{en}, Hong Kong"
    locality = zh if lang == "zh" else en
    new = s
    new = re.sub(r'<meta name="geo.position" content="[^"]+">',
                 f'<meta name="geo.position" content="{lat};{lng}">', new)
    new = re.sub(r'<meta name="ICBM" content="[^"]+">',
                 f'<meta name="ICBM" content="{lat}, {lng}">', new)
    new = re.sub(r'<meta name="geo.placename" content="[^"]+">',
                 f'<meta name="geo.placename" content="{placename}">', new)
    new = re.sub(r'"latitude":\s*[\d.\-]+,"longitude":\s*[\d.\-]+',
                 f'"latitude":{lat},"longitude":{lng}', new)
    new = re.sub(r'"addressLocality":"[^"]+"',
                 f'"addressLocality":"{locality}"', new)
    new = re.sub(r'<dd>[\d.]+°N, [\d.]+°E</dd>',
                 f'<dd>{lat}°N, {lng}°E</dd>', new)
    # zh template
    new = re.sub(r'GPS 座標 [\d.]+°N, [\d.]+°E',
                 f'GPS 座標 {lat}°N, {lng}°E', new)
    # en template may use ({lat}°N, ...)
    new = re.sub(r'\([\d.]+°N, [\d.]+°E\)',
                 f'({lat}°N, {lng}°E)', new)
    if new != s:
        p.write_text(new, encoding="utf-8"); return True
    return False

u_zh = u_en = 0
for slug, (lat, lng) in real_coords.items():
    if apply_coords("hotels", slug, lat, lng, "zh"): u_zh += 1
    if apply_coords("hotels-en", slug, lat, lng, "en"): u_en += 1
print(f"Applied real coords: zh={u_zh}, en={u_en}")

# STEP 2: For pages STILL containing generic 22.3193;114.1694 (not actually Mongkok),
# remove the GPS meta and display.
def strip_generic(page_dir, slug):
    p = Path(f"pages/{page_dir}/{slug}.html")
    if not p.exists(): return False
    s = p.read_text(encoding="utf-8")
    if "22.3193;114.1694" not in s: return False
    new = s
    # Remove geo.position / ICBM / GeoCoordinates schema
    new = re.sub(r'<meta name="geo.position" content="22\.3193;114\.1694">\n', "", new)
    new = re.sub(r'<meta name="ICBM" content="22\.3193, 114\.1694">\n', "", new)
    new = re.sub(r',\s*"geo":\{"@type":"GeoCoordinates","latitude":22\.3193,"longitude":114\.1694\}', "", new)
    # Remove GPS rows in info-grid
    new = re.sub(r'<dt>GPS[^<]*</dt><dd>22\.3193°N, 114\.1694°E</dd>\n?', "", new)
    new = re.sub(r'<dt>GPS 座標</dt><dd>22\.3193°N, 114\.1694°E</dd>\n?', "", new)
    # Remove FAQ line referencing those coords
    new = re.sub(r'，GPS 座標 22\.3193°N, 114\.1694°E', "", new)
    new = re.sub(r' \(22\.3193°N, 114\.1694°E\)', "", new)
    if new != s: p.write_text(new, encoding="utf-8"); return True
    return False

s_zh = s_en = 0
slugs = [p.stem for p in Path("pages/hotels").glob("dir-*.html")]
for slug in slugs:
    if strip_generic("hotels", slug): s_zh += 1
    if strip_generic("hotels-en", slug): s_en += 1
print(f"Removed generic coords: zh={s_zh}, en={s_en}")
