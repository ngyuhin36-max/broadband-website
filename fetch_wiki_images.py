"""Query Wikipedia API for each hotel's lead image URL (Wikimedia Commons)."""
import json, urllib.request, urllib.parse
from pathlib import Path

# Map each slug to best Wikipedia article title (English) for image lookup
WIKI_TITLES = {
    "the-peninsula-hong-kong": "The Peninsula Hong Kong",
    "mandarin-oriental": "Mandarin Oriental, Hong Kong",
    "the-ritz-carlton": "The Ritz-Carlton, Hong Kong",
    "hyatt-regency-tst": "Hyatt Regency Hong Kong, Tsim Sha Tsui",
    "the-murray": "Murray Building",
    "w-hong-kong": "W Hong Kong",
    "dorsett-mongkok": "Dorsett Mongkok, Hong Kong",
    "crowne-plaza-cwb": "Crowne Plaza Hong Kong Causeway Bay",
    "bridal-tea-house-hotel": "Bridal Tea House Hotel",
    "auberge-discovery-bay": "Auberge Discovery Bay Hong Kong",
    "four-seasons-hong-kong": "Four Seasons Hotel Hong Kong",
    "grand-hyatt-hong-kong": "Grand Hyatt Hong Kong",
    "rosewood-hong-kong": "Rosewood Hong Kong",
    "marriott-ocean-park": "Hong Kong Ocean Park Marriott Hotel",
    "hotel-icon": "Hotel ICON",
    "empire-prestige-cwb": "Empire Hotel Hong Kong",
    "nina-hotel-tsuen-wan-west": "Nina Hotel Tsuen Wan West",
    "sheraton-hong-kong": "Sheraton Hong Kong Hotel and Towers",
    "regala-skycity-hotel": "Regala Skycity Hotel",
    "panda-hotel": "Panda Hotel",
    "dorsett-wanchai": "Dorsett Wanchai, Hong Kong",
    "hopewell-hotel": "Hopewell Centre II",
    "rosedale-hotel-hong-kong": "Rosedale Hotel Hong Kong",
    "empire-hotel-wan-chai": "Empire Hotel Hong Kong",
    "maple-leaf-hotel": "Maple Leaf Hotel",
    "royal-garden-hotel": "The Royal Garden Hotel",
    "empire-hotel-cwb": "Empire Hotel Hong Kong",
    "conrad-hong-kong": "Conrad Hong Kong",
    "kerry-hotel-hong-kong": "Kerry Hotel, Hong Kong",
    "hk-disneyland-hotel": "Hong Kong Disneyland Hotel",
    "new-world-millennium-hk": "New World Millennium Hong Kong Hotel",
    "royal-plaza-hotel": "Royal Plaza Hotel",
    "four-points-tung-chung": "Four Points by Sheraton Hong Kong, Tung Chung",
    "regal-airport-hotel": "Regal Airport Hotel",
    "the-harbourview": "The Harbourview",
    "hotel-ease-access-tsuen-wan": "Silka Tsuen Wan Hong Kong",
    "disneys-hollywood-hotel": "Disney's Hollywood Hotel",
    "dorsett-tsuen-wan": "Dorsett Tsuen Wan, Hong Kong",
}

def fetch_image(title):
    """Query Wikipedia API for page image URL."""
    # Try English first
    for lang in ("en", "zh"):
        try:
            api = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
                "action": "query",
                "titles": title,
                "prop": "pageimages",
                "pithumbsize": "800",
                "format": "json",
                "redirects": "1",
            })
            req = urllib.request.Request(api, headers={"User-Agent": "broadbandhk/1.0"})
            data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for pid, p in pages.items():
                if pid == "-1":
                    continue
                thumb = p.get("thumbnail", {}).get("source")
                if thumb:
                    return thumb
        except Exception as e:
            print(f"  {lang} error: {e}")
    return None

results = {}
for slug, title in WIKI_TITLES.items():
    img = fetch_image(title)
    results[slug] = img
    print(f"{slug}: {'OK' if img else 'MISS'} {img or ''}")

Path("wiki_images.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nFound: {sum(1 for v in results.values() if v)} / {len(results)}")
