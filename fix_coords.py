"""Replace generic HK coords with real OSM coords where available.
Updates zh and en subpages in-place by replacing the geo meta and GPS display.
"""
import json, re
from pathlib import Path

osm = json.loads(Path("osm_meta.json").read_text(encoding="utf-8"))
print(f"OSM hotels with coords: {len(osm)}")

# HK districts for reverse-geocoding: (en_name, zh_name, lat_range, lng_range)
# Rough mapping by centroid distance — we'll pick nearest centroid
DISTRICTS = [
    ("Tsim Sha Tsui","尖沙咀",22.2985,114.1722),
    ("Tsim Sha Tsui East","尖沙咀東",22.3005,114.1784),
    ("Causeway Bay","銅鑼灣",22.2808,114.1846),
    ("Wan Chai","灣仔",22.2775,114.1722),
    ("Admiralty","金鐘",22.2790,114.1644),
    ("Central","中環",22.2816,114.1580),
    ("Sheung Wan","上環",22.2869,114.1509),
    ("Sai Wan","西環",22.2848,114.1406),
    ("West Kowloon","西九龍",22.3030,114.1606),
    ("Mongkok","旺角",22.3193,114.1694),
    ("Prince Edward","太子",22.3247,114.1688),
    ("Tai Kok Tsui","大角咀",22.3175,114.1632),
    ("Yau Ma Tei","油麻地",22.3080,114.1705),
    ("Jordan","佐敦",22.3043,114.1716),
    ("North Point","北角",22.2903,114.1996),
    ("Fortress Hill","炮台山",22.2888,114.1914),
    ("Hung Hom","紅磡",22.3044,114.1866),
    ("To Kwa Wan","土瓜灣",22.3168,114.1886),
    ("Kowloon City","九龍城",22.3276,114.1880),
    ("Kowloon Bay","九龍灣",22.3245,114.2097),
    ("Kwun Tong","觀塘",22.3137,114.2259),
    ("Tsuen Wan","荃灣",22.3722,114.1114),
    ("Kwai Chung","葵涌",22.3613,114.1292),
    ("Tsing Yi","青衣",22.3513,114.1065),
    ("Sha Tin","沙田",22.3815,114.1880),
    ("Ma On Shan","馬鞍山",22.4250,114.2320),
    ("Tai Po","大埔",22.4499,114.1649),
    ("Yuen Long","元朗",22.4430,114.0320),
    ("Tuen Mun","屯門",22.3907,113.9753),
    ("Tin Shui Wai","天水圍",22.4590,114.0050),
    ("Tung Chung","東涌",22.2870,113.9427),
    ("Chek Lap Kok","赤鱲角",22.3080,113.9185),
    ("Discovery Bay","愉景灣",22.2947,114.0147),
    ("Lantau Island","大嶼山",22.2617,113.9427),
    ("Sham Shui Po","深水埗",22.3302,114.1622),
    ("Cheung Sha Wan","長沙灣",22.3360,114.1566),
    ("Wong Tai Sin","黃大仙",22.3419,114.1939),
    ("Diamond Hill","鑽石山",22.3425,114.2020),
    ("Ho Man Tin","何文田",22.3177,114.1842),
    ("Wong Chuk Hang","黃竹坑",22.2482,114.1720),
    ("Aberdeen","香港仔",22.2483,114.1543),
    ("Ap Lei Chau","鴨脷洲",22.2413,114.1560),
    ("Repulse Bay","淺水灣",22.2357,114.1985),
    ("Stanley","赤柱",22.2190,114.2117),
    ("Sai Kung","西貢",22.3810,114.2700),
    ("Tseung Kwan O","將軍澳",22.3075,114.2590),
    ("Tiu Keng Leng","調景嶺",22.3089,114.2523),
    ("Shau Kei Wan","筲箕灣",22.2790,114.2295),
    ("Chai Wan","柴灣",22.2654,114.2377),
    ("Quarry Bay","鰂魚涌",22.2881,114.2133),
    ("Tai Koo","太古",22.2845,114.2170),
    ("Sheung Shui","上水",22.5020,114.1280),
    ("Fanling","粉嶺",22.4946,114.1386),
]

def nearest_district(lat, lng):
    best = None; best_d = 1e9
    for en, zh, dlat, dlng in DISTRICTS:
        dd = (lat-dlat)**2 + (lng-dlng)**2
        if dd < best_d:
            best_d = dd; best = (en, zh)
    return best

updated_zh = 0; updated_en = 0
for slug, meta in osm.items():
    lat = meta.get("lat"); lng = meta.get("lng")
    if not lat or not lng: continue
    en_name, zh_name = nearest_district(lat, lng)
    # Update zh page
    zp = Path(f"pages/hotels/{slug}.html")
    if zp.exists():
        s = zp.read_text(encoding="utf-8")
        new = s
        new = re.sub(r'<meta name="geo.position" content="[^"]+">',
                     f'<meta name="geo.position" content="{lat};{lng}">', new)
        new = re.sub(r'<meta name="ICBM" content="[^"]+">',
                     f'<meta name="ICBM" content="{lat}, {lng}">', new)
        new = re.sub(r'<dd>[\d.]+°N, [\d.]+°E</dd>',
                     f'<dd>{lat}°N, {lng}°E</dd>', new)
        new = re.sub(r'GPS 座標 [\d.]+°N, [\d.]+°E',
                     f'GPS 座標 {lat}°N, {lng}°E', new)
        # Update Schema geo coords
        new = re.sub(r'"latitude":\s*[\d.\-]+,"longitude":\s*[\d.\-]+',
                     f'"latitude":{lat},"longitude":{lng}', new)
        # Update placename to zh district
        new = re.sub(r'<meta name="geo.placename" content="[^"]+">',
                     f'<meta name="geo.placename" content="{zh_name}, Hong Kong">', new)
        # Update addressLocality in schema
        new = re.sub(r'"addressLocality":"[^"]+"',
                     f'"addressLocality":"{zh_name}"', new)
        if new != s: zp.write_text(new, encoding="utf-8"); updated_zh += 1
    # Update en page
    ep = Path(f"pages/hotels-en/{slug}.html")
    if ep.exists():
        s = ep.read_text(encoding="utf-8")
        new = s
        new = re.sub(r'<meta name="geo.position" content="[^"]+">',
                     f'<meta name="geo.position" content="{lat};{lng}">', new)
        new = re.sub(r'<meta name="ICBM" content="[^"]+">',
                     f'<meta name="ICBM" content="{lat}, {lng}">', new)
        new = re.sub(r'<dd>[\d.]+°N, [\d.]+°E</dd>',
                     f'<dd>{lat}°N, {lng}°E</dd>', new)
        new = re.sub(r'GPS \([\d.]+°N, [\d.]+°E\)',
                     f'GPS ({lat}°N, {lng}°E)', new)
        new = re.sub(r'\([\d.]+°N, [\d.]+°E\)',
                     f'({lat}°N, {lng}°E)', new)
        new = re.sub(r'"latitude":\s*[\d.\-]+,"longitude":\s*[\d.\-]+',
                     f'"latitude":{lat},"longitude":{lng}', new)
        new = re.sub(r'<meta name="geo.placename" content="[^"]+">',
                     f'<meta name="geo.placename" content="{en_name}, Hong Kong">', new)
        new = re.sub(r'"addressLocality":"[^"]+"',
                     f'"addressLocality":"{en_name}"', new)
        if new != s: ep.write_text(new, encoding="utf-8"); updated_en += 1

print(f"Updated zh pages: {updated_zh}")
print(f"Updated en pages: {updated_en}")
