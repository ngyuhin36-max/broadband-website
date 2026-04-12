"""Stage 2: For directory hotels that already have zh Wikipedia content,
fetch the English Wikipedia equivalent via langlinks and save in a new json.
"""
import json, urllib.request, urllib.parse, time
from pathlib import Path

enriched = json.loads(Path("directory_enriched.json").read_text(encoding="utf-8"))

def fetch_en_from_zh(zh_title):
    """Use zh.wikipedia langlinks to find English title, then fetch extract."""
    # Step 1: langlinks zh -> en
    api = "https://zh.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
        "action":"query","titles":zh_title,"prop":"langlinks",
        "lllang":"en","redirects":"1","format":"json",
    })
    try:
        req = urllib.request.Request(api, headers={"User-Agent":"broadbandhk/1.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        en_title = None
        for pid, p in pages.items():
            if pid == "-1": continue
            ll = p.get("langlinks") or []
            if ll:
                en_title = ll[0].get("*")
                break
        if not en_title:
            return None, None, None
        # Step 2: fetch en extract + image
        api2 = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
            "action":"query","titles":en_title,"prop":"extracts|pageimages",
            "exintro":"1","explaintext":"1","exsentences":"4",
            "pithumbsize":"800","redirects":"1","format":"json",
        })
        req2 = urllib.request.Request(api2, headers={"User-Agent":"broadbandhk/1.0"})
        data2 = json.loads(urllib.request.urlopen(req2, timeout=10).read().decode("utf-8"))
        pages2 = data2.get("query", {}).get("pages", {})
        for pid, p in pages2.items():
            if pid == "-1": continue
            ex = (p.get("extract") or "").strip()
            img = (p.get("thumbnail") or {}).get("source")
            if ex:
                return en_title, ex, img
    except Exception as e:
        print(f"  err: {e}")
    return None, None, None

results = {}
for i,(slug, info) in enumerate(enriched.items(), start=1):
    zh_title = info.get("wiki_title")
    if not zh_title: continue
    en_title, extract, img = fetch_en_from_zh(zh_title)
    if extract:
        results[slug] = {
            "en_title": en_title, "extract": extract, "image": img,
            "wiki_url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(en_title)}",
        }
        print(f"[{i}/{len(enriched)}] HIT {slug}")
    else:
        print(f"[{i}/{len(enriched)}] --- {slug}")
    time.sleep(0.1)

Path("en_wiki.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nFetched en wiki for {len(results)} / {len(enriched)}")
