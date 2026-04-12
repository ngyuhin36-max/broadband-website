"""Fetch coordinates from Wikipedia for hotels we added without OSM data."""
import json, urllib.request, urllib.parse, time, re
from pathlib import Path

osm = json.loads(Path("osm_meta.json").read_text(encoding="utf-8"))
en_wiki = json.loads(Path("en_wiki.json").read_text(encoding="utf-8"))
enriched = json.loads(Path("directory_enriched.json").read_text(encoding="utf-8"))

def api_call(u):
    req = urllib.request.Request(u, headers={"User-Agent":"broadbandhk/1.0"})
    return json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8"))

def get_coords(lang, title):
    u = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
        "action":"query","titles":title,"prop":"coordinates",
        "redirects":"1","format":"json"})
    try:
        d = api_call(u)
        for pid,p in d.get("query",{}).get("pages",{}).items():
            coords = p.get("coordinates", [])
            if coords:
                return coords[0].get("lat"), coords[0].get("lon")
    except Exception: pass
    return None, None

# Union of slugs needing coords (wiki-added that are NOT in OSM)
candidates = set(en_wiki.keys()) | set(enriched.keys())
todo = [s for s in candidates if s not in osm]
print(f"wiki-added without OSM: {len(todo)}")

coords_map = {}
for s in todo:
    # Try English first, then zh
    en_info = en_wiki.get(s)
    zh_info = enriched.get(s)
    lat, lng = None, None
    if en_info and en_info.get("en_title"):
        lat, lng = get_coords("en", en_info["en_title"])
    if (not lat or not lng) and zh_info and zh_info.get("wiki_title"):
        lat, lng = get_coords("zh", zh_info["wiki_title"])
    if lat and lng:
        coords_map[s] = (lat, lng)
        print(f"  {s}: {lat},{lng}")
    time.sleep(0.12)

Path("wiki_coords.json").write_text(json.dumps(coords_map,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"\ngot coords for {len(coords_map)} / {len(todo)}")
