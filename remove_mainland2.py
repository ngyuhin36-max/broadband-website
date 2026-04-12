"""Aggressive second-pass removal of mainland hotels."""
import json, re
from pathlib import Path

osm = json.loads(Path("osm_meta.json").read_text(encoding="utf-8"))
dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))
enriched = json.loads(Path("directory_enriched.json").read_text(encoding="utf-8"))
en_wiki = json.loads(Path("en_wiki.json").read_text(encoding="utf-8"))

# Mainland chain keywords (zh + en)
MAINLAND_CHAINS = [
    "7 Days","7Days","7天","莫泰","Motel 168","Motel168",
    "Home Inn","如家","Hanting","汉庭","漢庭",
    "Atour","亚朵","亞朵","Ji Hotel","全季","Jinjiang","錦江","锦江",
    "Huazhu","华住","Xana","希岸","Mehood","美豪","Lanou","兰欧","蘭歐",
    "Orange Hotel","桔子","Super 8","速8","Vienna International","維也納國際","维也纳国际",
    "Campanile","郁金香","CitiGo","城際","城际","IntercityHotel",
    "Yi Xuan","GreenTree","格林豪泰","華美達","Ramada",
    "Pudding","布丁","Metropark","維景","维景 酒店",
    "GDH","如格","Hampton","Shangri-La Shenzhen",
    "Kempinski Shenzhen","InterContinental Shenzhen",
]
# Shenzhen-specific name keywords
SHENZHEN_AREAS = ["蛇口","前海","華強","华强","南山","寶安","福田","羅湖","罗湖","皇崗","皇岗",
                   "龍華","龙华","龍崗","龙岗","坪山","坪地","光明","鹽田","盐田","Shekou","Qianhai","Huaqiang","Luohu","Futian","Bao'an","Nanshan","Longhua","Longgang","Yantian"]

def looks_mainland(name, lat):
    if not name: return False
    for kw in MAINLAND_CHAINS + SHENZHEN_AREAS:
        if kw in name:
            return True
    return False

remove = set()
for slug, d in osm.items():
    lat = d.get("lat") or 0
    nm = (d.get("name_zh") or "") + " " + (d.get("name_en") or "")
    # Rule 1: lat > 22.52 and not near 上水/粉嶺/沙頭角
    if lat > 22.52 and not re.search(r"上水|粉嶺|Sheung Shui|Fanling|Sha Tau Kok|沙頭角", nm):
        remove.add(slug); continue
    # Rule 2: chain/area keyword
    if looks_mainland(nm, lat):
        remove.add(slug); continue

# Also check non-osm directory hotels for mainland keywords
for h in dir_hotels:
    slug = h["slug"]
    if slug in osm: continue
    if looks_mainland(h["name"], 0):
        remove.add(slug)

print(f"to remove: {len(remove)}")

# Delete files
rf = 0
for slug in remove:
    for base in [Path(f"pages/hotels/{slug}.html"), Path(f"pages/hotels-en/{slug}.html")]:
        if base.exists(): base.unlink(); rf += 1
print(f"deleted {rf} subpage files")

dir_hotels = [h for h in dir_hotels if h["slug"] not in remove]
for s in remove:
    enriched.pop(s, None); en_wiki.pop(s, None); osm.pop(s, None)
Path("directory_hotels.json").write_text(json.dumps(dir_hotels,ensure_ascii=False,indent=2),encoding="utf-8")
Path("directory_enriched.json").write_text(json.dumps(enriched,ensure_ascii=False,indent=2),encoding="utf-8")
Path("en_wiki.json").write_text(json.dumps(en_wiki,ensure_ascii=False,indent=2),encoding="utf-8")
Path("osm_meta.json").write_text(json.dumps(osm,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"remaining directory: {len(dir_hotels)}")

for path in ("pages/HKhotel.html","pages/HKhotel-en.html"):
    p = Path(path); s = p.read_text(encoding="utf-8")
    rr = 0
    for slug in remove:
        pattern = re.compile(
            r'\s*<tr[^>]*>[^<]*<td[^>]*>\s*<a href="[^"]*/' + re.escape(slug) + r'\.html"[^>]*>[^<]*</a>[^<]*</td>[^<]*<td[^>]*>[^<]*</td>[^<]*<td[^>]*>[^<]*<s[^>]*>[^<]*</s>[^<]*</td>[^<]*</tr>',
            re.DOTALL)
        s2, n = pattern.subn("", s, count=1)
        if n: s = s2; rr += 1
    p.write_text(s, encoding="utf-8")
    print(f"  {path}: removed {rr} rows")
