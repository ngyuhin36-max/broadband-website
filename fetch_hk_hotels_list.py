"""Fetch all HK hotels from Wikipedia's Category:Hotels in Hong Kong.
For each hotel: get zh + en title, extract, image.
"""
import json, urllib.request, urllib.parse, time
from pathlib import Path

def api_call(url):
    req = urllib.request.Request(url, headers={"User-Agent":"broadbandhk/1.0"})
    return json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8"))

def list_category(lang, cat):
    """Get all page titles in a Wikipedia category, paginated."""
    pages = []
    cont = ""
    while True:
        params = {
            "action":"query","list":"categorymembers","cmtitle":cat,
            "cmlimit":"500","cmtype":"page","format":"json",
        }
        if cont: params["cmcontinue"] = cont
        api = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
        data = api_call(api)
        pages.extend(m["title"] for m in data.get("query",{}).get("categorymembers",[]))
        cont = data.get("continue",{}).get("cmcontinue")
        if not cont: break
        time.sleep(0.2)
    return pages

def get_page(lang, title):
    """Fetch extract + image + zh/en langlink for one page."""
    api = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
        "action":"query","titles":title,"prop":"extracts|pageimages|langlinks",
        "exintro":"1","explaintext":"1","exsentences":"3",
        "pithumbsize":"800","lllang":"zh" if lang=="en" else "en",
        "redirects":"1","format":"json",
    })
    try:
        data = api_call(api)
        pages = data.get("query",{}).get("pages",{})
        for pid,p in pages.items():
            if pid == "-1": continue
            extract = (p.get("extract") or "").strip()
            img = (p.get("thumbnail") or {}).get("source")
            ll = (p.get("langlinks") or [])
            other_title = ll[0].get("*") if ll else None
            return {"title":p.get("title",title),"extract":extract,"image":img,"other_lang_title":other_title}
    except Exception as e:
        print(f"  err {title}: {e}")
    return None

# Step 1: gather titles from both zh and en categories
print("Listing en.wikipedia Category:Hotels in Hong Kong...")
en_titles = list_category("en", "Category:Hotels in Hong Kong")
print(f"  got {len(en_titles)} en titles")
time.sleep(0.5)
print("Listing zh.wikipedia Category:香港酒店...")
zh_titles = list_category("zh", "Category:香港酒店")
print(f"  got {len(zh_titles)} zh titles")

# Step 2: fetch data per title, merge
all_hotels = {}  # key = en_title (lowercased) or zh_title
for t in en_titles:
    data = get_page("en", t)
    if data and data.get("extract"):
        key = t
        all_hotels[key] = {
            "en_title": t, "en_extract": data["extract"], "en_image": data["image"],
            "zh_title": data.get("other_lang_title"),
        }
    time.sleep(0.1)
print(f"after en fetch: {len(all_hotels)} hotels")

# For each en entry, if it has zh title, fetch zh data
for key, h in list(all_hotels.items()):
    zt = h.get("zh_title")
    if zt:
        data = get_page("zh", zt)
        if data and data.get("extract"):
            h["zh_extract"] = data["extract"]
            h["zh_image"] = data["image"]
        time.sleep(0.1)

# Also iterate zh-only titles not already covered
zh_only_added = 0
for t in zh_titles:
    # Find if already in all_hotels via zh_title
    already = any(h.get("zh_title") == t for h in all_hotels.values())
    if already: continue
    data = get_page("zh", t)
    if data and data.get("extract"):
        key = t  # use zh title as key
        en_t = data.get("other_lang_title")
        all_hotels[key] = {
            "en_title": en_t, "zh_title": t,
            "zh_extract": data["extract"], "zh_image": data["image"],
        }
        if en_t:
            # Fetch en too
            data2 = get_page("en", en_t)
            if data2 and data2.get("extract"):
                all_hotels[key]["en_extract"] = data2["extract"]
                all_hotels[key]["en_image"] = data2["image"]
            time.sleep(0.1)
        zh_only_added += 1
    time.sleep(0.1)

print(f"zh-only added: {zh_only_added}")
print(f"total: {len(all_hotels)} hotels")
Path("wiki_hk_hotels.json").write_text(
    json.dumps(all_hotels, ensure_ascii=False, indent=2), encoding="utf-8")
