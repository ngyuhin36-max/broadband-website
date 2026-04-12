"""Remove Shenzhen/mainland hotels misidentified as HK in OSM import.
Threshold: lat > 22.545 AND not a known HK area (Sheung Shui/Fanling stay).
Also remove by name containing obvious mainland chains or simplified 宾馆.
"""
import json, re
from pathlib import Path

osm = json.loads(Path("osm_meta.json").read_text(encoding="utf-8"))
dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))
enriched = json.loads(Path("directory_enriched.json").read_text(encoding="utf-8"))
en_wiki = json.loads(Path("en_wiki.json").read_text(encoding="utf-8"))

# HK areas near border that are OK
HK_NORTH_KW = ["上水","粉嶺","沙頭角","Sheung Shui","Fanling","Sha Tau Kok","Lok Ma Chau","落馬洲"]

remove = set()
for slug, d in osm.items():
    lat = d.get("lat")
    nm = (d.get("name_zh") or "") + " " + (d.get("name_en") or "")
    is_hk_north = any(k in nm for k in HK_NORTH_KW)
    # Simplified chinese detection: 宾/馆/饭/华/资/业 — CN-only chars
    cn_simplified = bool(re.search(r"[宾馆饭华体这来会发电话图爱书国亲绝银双见过钱让实际后长门问开关热马风飞龙兴节业长东为亿张将来还业响应轻团课]", nm))
    if lat and lat > 22.545 and not is_hk_north:
        remove.add(slug)
    elif lat and lat > 22.50 and cn_simplified and not is_hk_north:
        remove.add(slug)
    elif cn_simplified and not is_hk_north and lat and lat > 22.45:
        # simplified chinese + somewhat north = likely mainland
        remove.add(slug)

# Also check non-OSM entries (wiki-added) for any mainland patterns
for h in dir_hotels:
    slug = h["slug"]
    if slug in osm: continue  # already handled
    nm = h["name"]
    if re.search(r"深圳|廣州|珠海|東莞|中山|佛山|惠州|Shenzhen|Guangzhou|Zhuhai|Huizhou", nm):
        remove.add(slug)

print(f"to remove: {len(remove)}")

# Delete subpage files
removed_files = 0
for slug in remove:
    for base in [Path(f"pages/hotels/{slug}.html"), Path(f"pages/hotels-en/{slug}.html")]:
        if base.exists():
            base.unlink(); removed_files += 1
print(f"deleted {removed_files} subpage files")

# Filter jsons
dir_hotels = [h for h in dir_hotels if h["slug"] not in remove]
for slug in remove:
    enriched.pop(slug, None); en_wiki.pop(slug, None); osm.pop(slug, None)
Path("directory_hotels.json").write_text(json.dumps(dir_hotels, ensure_ascii=False, indent=2), encoding="utf-8")
Path("directory_enriched.json").write_text(json.dumps(enriched, ensure_ascii=False, indent=2), encoding="utf-8")
Path("en_wiki.json").write_text(json.dumps(en_wiki, ensure_ascii=False, indent=2), encoding="utf-8")
Path("osm_meta.json").write_text(json.dumps(osm, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"remaining directory: {len(dir_hotels)}")

# Remove rows from HKhotel.html / HKhotel-en.html directory tables
for path in ("pages/HKhotel.html", "pages/HKhotel-en.html"):
    p = Path(path); s = p.read_text(encoding="utf-8")
    removed_rows = 0
    for slug in remove:
        # Match <tr ...>...<a href=".../{slug}.html">...</a>...</tr> and remove
        pattern = re.compile(
            r'\s*<tr[^>]*>[^<]*<td[^>]*>\s*<a href="[^"]*/' + re.escape(slug) + r'\.html"[^>]*>[^<]*</a>[^<]*</td>[^<]*<td[^>]*>[^<]*</td>[^<]*<td[^>]*>[^<]*<s[^>]*>[^<]*</s>[^<]*</td>[^<]*</tr>',
            re.DOTALL)
        s2, n = pattern.subn("", s, count=1)
        if n:
            s = s2; removed_rows += 1
    p.write_text(s, encoding="utf-8")
    print(f"  {path}: removed {removed_rows} rows")
