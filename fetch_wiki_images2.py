"""Search Wikimedia Commons for hotel images for misses."""
import json, urllib.request, urllib.parse
from pathlib import Path

existing = json.loads(Path("wiki_images.json").read_text(encoding="utf-8"))

# Chinese Wiki titles + Commons search fallback queries per miss
SEARCH_QUERIES = {
    "dorsett-mongkok": ["Dorsett Mongkok", "帝盛酒店 旺角"],
    "crowne-plaza-cwb": ["Crowne Plaza Causeway Bay", "銅鑼灣皇冠假日"],
    "auberge-discovery-bay": ["Auberge Discovery Bay", "愉景灣酒店"],
    "marriott-ocean-park": ["Ocean Park Marriott", "海洋公園萬豪"],
    "empire-prestige-cwb": ["Empire Hotel Causeway Bay", "皇悅酒店"],
    "nina-hotel-tsuen-wan-west": ["Nina Hotel Tsuen Wan", "如心酒店", "Nina Tower"],
    "sheraton-hong-kong": ["Sheraton Hong Kong Hotel", "喜來登酒店 尖沙咀"],
    "regala-skycity-hotel": ["Regala Skycity", "Skycity Hong Kong"],
    "hopewell-hotel": ["Hopewell Centre II", "合和中心二期"],
    "rosedale-hotel-hong-kong": ["Rosedale Causeway Bay", "珀麗酒店"],
    "empire-hotel-wan-chai": ["Empire Hotel Wan Chai", "皇悅 灣仔"],
    "maple-leaf-hotel": ["Maple Leaf Hotel Hong Kong"],
    "royal-garden-hotel": ["Royal Garden Hotel Hong Kong", "帝苑酒店"],
    "empire-hotel-cwb": ["Empire Hotel Causeway Bay"],
    "conrad-hong-kong": ["Conrad Hong Kong", "港麗酒店", "Pacific Place Hong Kong"],
    "kerry-hotel-hong-kong": ["Kerry Hotel Hong Kong", "嘉里酒店 紅磡"],
    "new-world-millennium-hk": ["New World Millennium Hong Kong", "千禧新世界"],
    "royal-plaza-hotel": ["Royal Plaza Hotel", "帝京酒店", "MOKO Mong Kok"],
    "four-points-tung-chung": ["Four Points Sheraton Tung Chung"],
    "regal-airport-hotel": ["Regal Airport Hotel", "富豪機場酒店"],
    "the-harbourview": ["Harbourview Hotel Hong Kong", "灣景國際"],
    "hotel-ease-access-tsuen-wan": ["Silka Tsuen Wan", "Hotel Ease Access"],
    "dorsett-tsuen-wan": ["Dorsett Tsuen Wan", "帝盛 荃灣"],
}

def commons_search(query):
    """Search Wikimedia Commons for an image matching query."""
    api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query",
        "generator": "search",
        "gsrsearch": f"{query} filetype:bitmap",
        "gsrlimit": "5",
        "gsrnamespace": "6",  # File namespace
        "prop": "imageinfo",
        "iiprop": "url|size",
        "iiurlwidth": "960",
        "format": "json",
    })
    try:
        req = urllib.request.Request(api, headers={"User-Agent": "broadbandhk/1.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        # pick first decent-sized image
        candidates = []
        for pid, p in pages.items():
            info = (p.get("imageinfo") or [{}])[0]
            url = info.get("thumburl") or info.get("url")
            w = info.get("width", 0)
            h = info.get("height", 0)
            if url and w >= 400 and h >= 300:
                candidates.append((w*h, url, p.get("title", "")))
        candidates.sort(reverse=True)
        if candidates:
            return candidates[0][1], candidates[0][2]
    except Exception as e:
        print(f"  err: {e}")
    return None, None

for slug, queries in SEARCH_QUERIES.items():
    if existing.get(slug):
        continue
    found = None
    for q in queries:
        url, title = commons_search(q)
        if url:
            print(f"{slug}: {title} -> {url}")
            found = url
            break
    if not found:
        print(f"{slug}: STILL MISS")
    existing[slug] = found

Path("wiki_images.json").write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nTotal found: {sum(1 for v in existing.values() if v)} / {len(existing)}")
