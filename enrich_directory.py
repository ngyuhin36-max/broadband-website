"""Query Wikipedia for each directory hotel; enrich pages that match."""
import json, urllib.request, urllib.parse, time
from pathlib import Path

hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))

def wiki_lookup(title, lang):
    """Return (extract, image_url, canonical_title) or (None,None,None)."""
    try:
        api = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
            "action":"query","titles":title,"prop":"extracts|pageimages|info",
            "exintro":"1","explaintext":"1","exsentences":"3",
            "pithumbsize":"800","redirects":"1","format":"json","inprop":"url",
        })
        req = urllib.request.Request(api, headers={"User-Agent":"broadbandhk/1.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        for pid,p in pages.items():
            if pid == "-1": continue
            extract = (p.get("extract") or "").strip()
            thumb = (p.get("thumbnail") or {}).get("source")
            ctitle = p.get("title","")
            if extract and len(extract) >= 40:  # meaningful content
                return extract, thumb, ctitle
    except Exception:
        pass
    return None, None, None

def wiki_search(query, lang="zh"):
    """Search Wikipedia for an article matching query, return first title."""
    try:
        api = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
            "action":"query","list":"search","srsearch":query,
            "srlimit":"3","format":"json",
        })
        req = urllib.request.Request(api, headers={"User-Agent":"broadbandhk/1.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8"))
        hits = data.get("query", {}).get("search", [])
        # Filter: must contain 酒店 or 飯店 or Hotel for relevance
        for h in hits:
            t = h.get("title","")
            if any(k in t for k in ("酒店","飯店","Hotel","Inn","Resort")):
                return t
        return hits[0]["title"] if hits else None
    except Exception:
        return None

enriched = {}
for i,h in enumerate(hotels, start=1):
    name = h["name"]
    # Try zh direct, then zh search, then en search (translate 飯店->Hotel pattern hard)
    extract,img,ctitle = wiki_lookup(name, "zh")
    if not extract:
        # search variations
        # remove parenthetical notes
        base = name.split("（")[0]
        # try variant: 飯店 -> 酒店
        variants = {name, base, base.replace("飯店","酒店"), base.replace("酒店","飯店")}
        for v in variants:
            if v == name: continue
            extract,img,ctitle = wiki_lookup(v, "zh")
            if extract: break
    if not extract:
        q = wiki_search(name, "zh")
        if q and q != name:
            extract,img,ctitle = wiki_lookup(q, "zh")
    if extract:
        enriched[h["slug"]] = {
            "name": h["name"], "price": h["price"], "orig": h["orig"],
            "extract": extract, "image": img, "wiki_title": ctitle,
            "wiki_url": f"https://zh.wikipedia.org/wiki/{urllib.parse.quote(ctitle)}",
        }
        print(f"[{i}/{len(hotels)}] HIT {h['slug']}")
    else:
        print(f"[{i}/{len(hotels)}] --- {h['slug']}")
    time.sleep(0.1)

Path("directory_enriched.json").write_text(
    json.dumps(enriched, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nEnriched {len(enriched)} / {len(hotels)} directory hotels")
