"""Remove entries that are NOT individual HK hotels:
- Hotel groups / parent companies (朗廷集團, 文華東方集團, etc.)
- Non-hotel buildings (SkyCity airport area, Mariner's Club, The Masterpiece building)
- OSM entries with too-generic / short names
"""
import json, re
from pathlib import Path

dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))
enriched = json.loads(Path("directory_enriched.json").read_text(encoding="utf-8"))
en_wiki = json.loads(Path("en_wiki.json").read_text(encoding="utf-8"))
osm = json.loads(Path("osm_meta.json").read_text(encoding="utf-8"))

# Explicit slugs to remove (groups, companies, non-hotel structures)
EXPLICIT_REMOVE = {
    "dir-396",  # SkyCity - airport commercial area, not a hotel
    "dir-405",  # Mariner's Club - seafarers club
    "dir-406",  # 名鑄 Masterpiece - residential+commercial complex
    "dir-401",  # The Jervois - serviced residence (arguably not a hotel)
    "dir-428",  # Langham Hospitality Group (company)
    "dir-429",  # Hongkong and Shanghai Hotels (company, parent of Peninsula)
    "dir-430",  # Miramar Hotel and Investment (company)
    "dir-431",  # Rosewood Hotels & Resorts (global company)
    "dir-432",  # Regal Hotels International (company)
    "dir-433",  # Mandarin Oriental Hotel Group (company)
    "dir-434",  # Shangri-La Hotels and Resorts (company)
    "dir-435",  # Dorsett Hospitality International (company)
    "dir-436",  # Marco Polo Hotels (brand)
    "dir-437",  # Harbour Plaza Hotel Management (company)
    "dir-415",  # Ovolo Hotels (brand overview)
}

# Also check OSM entries with dubious names
OSM_DUBIOUS_KW = ["test","Test","TEST","unknown","Unknown",
                  "Hotel Test","Guest House","Guesthouse"]
# Hostels are legit but let's keep. Remove only clear non-hotels.

for slug, meta in osm.items():
    nm = (meta.get("name_en") or "") + " " + (meta.get("name_zh") or "")
    # Too generic or test names
    if nm.strip() in ("Hotel","酒店","旅館","Inn","Hostel"): EXPLICIT_REMOVE.add(slug)
    if "test" in nm.lower(): EXPLICIT_REMOVE.add(slug)

print(f"to remove: {len(EXPLICIT_REMOVE)}")
# Delete subpage files
rf = 0
for slug in EXPLICIT_REMOVE:
    for base in [Path(f"pages/hotels/{slug}.html"), Path(f"pages/hotels-en/{slug}.html")]:
        if base.exists(): base.unlink(); rf += 1
print(f"deleted {rf} subpage files")

dir_hotels = [h for h in dir_hotels if h["slug"] not in EXPLICIT_REMOVE]
for s in EXPLICIT_REMOVE:
    enriched.pop(s, None); en_wiki.pop(s, None); osm.pop(s, None)
Path("directory_hotels.json").write_text(json.dumps(dir_hotels,ensure_ascii=False,indent=2),encoding="utf-8")
Path("directory_enriched.json").write_text(json.dumps(enriched,ensure_ascii=False,indent=2),encoding="utf-8")
Path("en_wiki.json").write_text(json.dumps(en_wiki,ensure_ascii=False,indent=2),encoding="utf-8")
Path("osm_meta.json").write_text(json.dumps(osm,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"remaining directory: {len(dir_hotels)}")

for path in ("pages/HKhotel.html","pages/HKhotel-en.html"):
    p = Path(path); s = p.read_text(encoding="utf-8")
    rr = 0
    for slug in EXPLICIT_REMOVE:
        pattern = re.compile(
            r'\s*<tr[^>]*>[^<]*<td[^>]*>\s*<a href="[^"]*/' + re.escape(slug) + r'\.html"[^>]*>[^<]*</a>[^<]*</td>[^<]*<td[^>]*>[^<]*</td>[^<]*<td[^>]*>[^<]*<s[^>]*>[^<]*</s>[^<]*</td>[^<]*</tr>',
            re.DOTALL)
        s2, n = pattern.subn("", s, count=1)
        if n: s = s2; rr += 1
    p.write_text(s, encoding="utf-8")
    print(f"  {path}: removed {rr} rows")
