"""Fetch data for all collected titles, dedupe against existing."""
import json, urllib.request, urllib.parse, time, re
from pathlib import Path

titles = json.loads(Path("more_titles.json").read_text(encoding="utf-8"))
existing_hotels = json.loads(Path("wiki_hk_hotels.json").read_text(encoding="utf-8"))
featured = json.loads(Path("hotels_data.json").read_text(encoding="utf-8"))
dir_h = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))

def zh_only(s): return "".join(c for c in (s or "") if "\u4e00" <= c <= "\u9fff")
existing_zh = {zh_only(h["name"]) for h in featured + dir_h}
existing_en = set()
for h in featured + dir_h:
    m = re.search(r'([A-Za-z][A-Za-z0-9 &\-\'.]*)$', h["name"])
    if m: existing_en.add(m.group(1).strip().lower())

def api(u):
    req = urllib.request.Request(u, headers={"User-Agent":"broadbandhk/1.0"})
    return json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8"))

def get_page(lang, title):
    u = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
        "action":"query","titles":title,"prop":"extracts|pageimages|langlinks",
        "exintro":"1","explaintext":"1","exsentences":"3","pithumbsize":"800",
        "lllang":"zh" if lang=="en" else "en","redirects":"1","format":"json"})
    try:
        d = api(u)
        for pid,p in d.get("query",{}).get("pages",{}).items():
            if pid == "-1": continue
            return {
                "title": p.get("title",title),
                "extract": (p.get("extract") or "").strip(),
                "image": (p.get("thumbnail") or {}).get("source"),
                "other": (p.get("langlinks") or [{}])[0].get("*"),
            }
    except Exception: pass
    return None

new_hotels = []
seen_keys = set()
# Iterate en first
for t in titles["en"]:
    if t.lower() in existing_en: continue
    data = get_page("en", t)
    if not data or not data["extract"]: continue
    zh_t = data.get("other")
    key = (t, zh_t or "")
    if key in seen_keys: continue
    if zh_t and zh_only(zh_t) in existing_zh: continue
    entry = {"en_title":t,"en_extract":data["extract"],"en_image":data["image"],
             "zh_title":zh_t}
    if zh_t:
        zd = get_page("zh", zh_t)
        if zd:
            entry["zh_extract"] = zd["extract"]
            entry["zh_image"] = zd["image"]
            time.sleep(0.1)
    new_hotels.append(entry)
    seen_keys.add(key)
    time.sleep(0.1)

for t in titles["zh"]:
    if zh_only(t) in existing_zh: continue
    # Also check against already-added
    if any(h.get("zh_title") == t for h in new_hotels): continue
    data = get_page("zh", t)
    if not data or not data["extract"]: continue
    en_t = data.get("other")
    if en_t and en_t.lower() in existing_en: continue
    if any(h.get("en_title") == en_t for h in new_hotels): continue
    entry = {"zh_title":t,"zh_extract":data["extract"],"zh_image":data["image"],
             "en_title":en_t}
    if en_t:
        ed = get_page("en", en_t)
        if ed:
            entry["en_extract"] = ed["extract"]
            entry["en_image"] = ed["image"]
            time.sleep(0.1)
    new_hotels.append(entry)
    time.sleep(0.1)

# Save
Path("new_hotels2.json").write_text(
    json.dumps(new_hotels, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Found {len(new_hotels)} additional new hotels")
for h in new_hotels[:10]:
    print(f"  {h.get('en_title','-')} | {h.get('zh_title','-')}")
