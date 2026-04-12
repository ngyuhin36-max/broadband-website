"""Fetch HK hotels from OpenStreetMap via Overpass API.
Query all tourism=hotel within HK bounding box with name tags.
"""
import json, urllib.request, urllib.parse, re, time
from pathlib import Path

# HK bounding box (south, west, north, east)
BBOX = "22.15,113.82,22.58,114.44"

query = f"""
[out:json][timeout:60];
(
  node["tourism"="hotel"]({BBOX});
  way["tourism"="hotel"]({BBOX});
);
out center tags;
"""

req = urllib.request.Request(
    "https://overpass-api.de/api/interpreter",
    data=query.encode("utf-8"),
    headers={"User-Agent":"broadbandhk/1.0","Content-Type":"text/plain"},
)
print("Querying Overpass API...")
data = json.loads(urllib.request.urlopen(req, timeout=90).read().decode("utf-8"))
elements = data.get("elements", [])
print(f"got {len(elements)} OSM hotel elements")

# Load existing for dedup
featured = json.loads(Path("hotels_data.json").read_text(encoding="utf-8"))
dir_h = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))

def zh_only(s): return "".join(c for c in (s or "") if "\u4e00" <= c <= "\u9fff")
existing_zh = {zh_only(h["name"]) for h in featured+dir_h if zh_only(h["name"])}
existing_en = set()
for h in featured+dir_h:
    m = re.search(r'([A-Za-z][A-Za-z0-9 &\-\'.]*)$', h["name"])
    if m: existing_en.add(m.group(1).strip().lower())

osm_hotels = []
for el in elements:
    t = el.get("tags", {})
    name_en = t.get("name:en") or t.get("int_name") or t.get("name")
    name_zh = t.get("name:zh-Hant") or t.get("name:zh") or t.get("name:zh-Hans")
    if not name_en and not name_zh: continue
    # Need at least a proper-looking name (avoid "Hotel" or very short strings)
    nm = (name_en or name_zh or "").strip()
    if len(nm) < 4: continue
    # Dedup
    zo = zh_only(name_zh or "")
    if zo and zo in existing_zh: continue
    en_low = (name_en or "").lower().strip()
    if en_low and en_low in existing_en: continue
    # Coords
    if el["type"] == "node":
        lat, lng = el.get("lat"), el.get("lon")
    else:
        c = el.get("center", {}); lat, lng = c.get("lat"), c.get("lon")
    osm_hotels.append({
        "name_en": name_en, "name_zh": name_zh,
        "lat": lat, "lng": lng,
        "address": t.get("addr:full") or f"{t.get('addr:street','') } {t.get('addr:housenumber','')}".strip(),
        "website": t.get("website") or t.get("contact:website"),
        "stars": t.get("stars"),
        "phone": t.get("phone") or t.get("contact:phone"),
    })

# Dedup within OSM set
seen = set(); unique = []
for h in osm_hotels:
    key = (h.get("name_en","").lower().strip(), zh_only(h.get("name_zh") or ""))
    if key in seen: continue
    seen.add(key); unique.append(h)

print(f"unique new OSM hotels (after dedup): {len(unique)}")
Path("osm_hotels.json").write_text(
    json.dumps(unique, ensure_ascii=False, indent=2), encoding="utf-8")
for h in unique[:10]:
    print(f"  {h.get('name_en','-')} | {h.get('name_zh','-')}")
