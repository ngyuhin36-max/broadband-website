"""Fetch more HK hotels from additional sources:
- Wikipedia zh/en subcategories (Hotels in Tsim Sha Tsui, Hotels in Central, etc.)
- Wikipedia "List of hotels in Hong Kong" article
"""
import json, urllib.request, urllib.parse, time
from pathlib import Path

def api_call(url):
    req = urllib.request.Request(url, headers={"User-Agent":"broadbandhk/1.0"})
    return json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8"))

def list_category(lang, cat):
    pages = []; cont = ""
    while True:
        params = {"action":"query","list":"categorymembers","cmtitle":cat,
                  "cmlimit":"500","cmtype":"page","format":"json"}
        if cont: params["cmcontinue"] = cont
        api = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
        try:
            data = api_call(api)
            pages.extend(m["title"] for m in data.get("query",{}).get("categorymembers",[]))
            cont = data.get("continue",{}).get("cmcontinue")
            if not cont: break
            time.sleep(0.15)
        except Exception as e:
            print(f"  err {cat}: {e}"); break
    return pages

def list_subcategories(lang, cat):
    params = {"action":"query","list":"categorymembers","cmtitle":cat,
              "cmlimit":"500","cmtype":"subcat","format":"json"}
    api = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
    try:
        data = api_call(api)
        return [m["title"] for m in data.get("query",{}).get("categorymembers",[])]
    except Exception: return []

def get_page(lang, title):
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
            ll = p.get("langlinks") or []
            other_title = ll[0].get("*") if ll else None
            return {"title":p.get("title",title),"extract":extract,"image":img,"other":other_title}
    except Exception as e:
        print(f"  err {title}: {e}")
    return None

# Collect titles from subcategories on both wikis
all_titles_en = set()
all_titles_zh = set()

print("Fetching en.wikipedia subcategories...")
en_subs = list_subcategories("en", "Category:Hotels in Hong Kong")
print(f"  en subcats: {len(en_subs)}")
for sub in en_subs:
    titles = list_category("en", sub)
    all_titles_en.update(titles)
    print(f"    {sub}: +{len(titles)}")

print("\nFetching zh.wikipedia subcategories...")
# Try various zh category names
for zh_cat in ["Category:香港酒店","Category:香港飯店","Category:香港旅館"]:
    titles = list_category("zh", zh_cat)
    if titles:
        all_titles_zh.update(titles)
        print(f"  {zh_cat}: +{len(titles)}")
    subs = list_subcategories("zh", zh_cat)
    for sub in subs:
        t = list_category("zh", sub)
        all_titles_zh.update(t)
        print(f"    {sub}: +{len(t)}")

print(f"\nTotal en titles: {len(all_titles_en)}")
print(f"Total zh titles: {len(all_titles_zh)}")

Path("more_titles.json").write_text(
    json.dumps({"en":list(all_titles_en),"zh":list(all_titles_zh)},ensure_ascii=False,indent=2),
    encoding="utf-8")
