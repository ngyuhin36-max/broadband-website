"""Filter OSM hotels: keep only genuine HK hotels, exclude Shenzhen / obvious duplicates."""
import json, re
from pathlib import Path

osm = json.loads(Path("osm_hotels.json").read_text(encoding="utf-8"))
# HK latitude range: 22.15 - 22.57 (but most hotels south of 22.50)
# Shenzhen is generally 22.50+. Allow up to 22.56 for Lok Ma Chau area
SHENZHEN_KW = ["Shenzhen","深圳","福田","南山","羅湖","寶安","龍崗","龍華","光明","坪山","坪地","葵涌","鹽田","沙井","觀瀾","松崗","布吉","橫崗","西鄉"]

# Shenzhen keywords are Chinese districts; Hong Kong has 葵涌 too so be careful.
# Best heuristic: lat >= 22.45 AND name has Shenzhen district keyword -> skip.
# Simpler: skip if name contains "Shenzhen" or "深圳"
clean = []
for h in osm:
    nm = (h.get("name_en") or "") + " " + (h.get("name_zh") or "")
    if any(k in nm for k in ["Shenzhen","深圳","福田","羅湖","南山","寶安"]):
        continue
    lat = h.get("lat") or 0
    if lat and lat > 22.56:  # definitely mainland China
        continue
    clean.append(h)

print(f"after filter: {len(clean)} / {len(osm)}")
Path("osm_hotels_clean.json").write_text(
    json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")

# Count by what data each has
with_zh = sum(1 for h in clean if h.get("name_zh"))
with_website = sum(1 for h in clean if h.get("website"))
with_stars = sum(1 for h in clean if h.get("stars"))
with_phone = sum(1 for h in clean if h.get("phone"))
print(f"has name_zh: {with_zh}")
print(f"has website: {with_website}")
print(f"has stars: {with_stars}")
print(f"has phone: {with_phone}")
