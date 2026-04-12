"""Deep audit of all hotel data accuracy. Flag:
1. zh Wikipedia title that doesn't overlap >=3 Chinese chars with hotel name
2. en Wikipedia title that doesn't overlap meaningfully with hotel English name
3. OSM coords outside strict HK bbox (22.15-22.55, 113.82-114.44)
4. Duplicate hotel names (same zh+en in multiple slugs)
5. Non-HK named hotels that slipped through
"""
import json, re
from pathlib import Path

dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))
enriched = json.loads(Path("directory_enriched.json").read_text(encoding="utf-8"))
en_wiki = json.loads(Path("en_wiki.json").read_text(encoding="utf-8"))
osm = json.loads(Path("osm_meta.json").read_text(encoding="utf-8"))

name_by_slug = {h["slug"]: h["name"] for h in dir_hotels}

def zh_chars(s):
    return set(c for c in (s or "") if "\u4e00" <= c <= "\u9fff")

def zh_tokens(s):
    # split Chinese portion by en/numbers
    return re.findall(r"[\u4e00-\u9fff]+", s or "")

def en_tokens(s):
    return set(w.lower() for w in re.findall(r"[A-Za-z]+", s or "") if len(w) >= 3)

# 1. zh wiki audit: hotel name must share >=3 zh chars with wiki_title
bad_zh = {}
for slug, info in enriched.items():
    hname = name_by_slug.get(slug, "")
    wtitle = info.get("wiki_title", "")
    overlap = zh_chars(hname) & zh_chars(wtitle)
    if len(overlap) < 3:
        bad_zh[slug] = (hname, wtitle, len(overlap))

# 2. en wiki audit
bad_en = {}
for slug, info in en_wiki.items():
    hname = name_by_slug.get(slug, "")
    etitle = info.get("en_title", "")
    htokens = en_tokens(hname); etokens = en_tokens(etitle)
    if not htokens or not etokens: continue
    if not (htokens & etokens):
        bad_en[slug] = (hname, etitle)

# 3. OSM outside strict bbox
bad_osm = {}
for slug, m in osm.items():
    lat = m.get("lat"); lng = m.get("lng")
    if not lat or not lng: continue
    if not (22.15 <= lat <= 22.55 and 113.82 <= lng <= 114.44):
        bad_osm[slug] = (name_by_slug.get(slug,"?"), lat, lng)

# 4. duplicate names
from collections import defaultdict
name_to_slugs = defaultdict(list)
for h in dir_hotels:
    # normalize by zh-only + en-only
    n = h["name"]
    zh = "".join(c for c in n if "\u4e00" <= c <= "\u9fff")
    en = " ".join(re.findall(r"[A-Za-z]+", n))
    key = zh + "|" + en.lower().strip()
    if key.strip("|"):
        name_to_slugs[key].append(h["slug"])
dupes = {k:v for k,v in name_to_slugs.items() if len(v) > 1}

# 5. Non-HK named (if name contains 深圳/廣州 etc that slipped through)
mainland_pat = r"深圳|廣州|珠海|東莞|中山|佛山|惠州|Shenzhen|Guangzhou|Zhuhai|Huizhou|Dongguan"
bad_mainland = [h["slug"] for h in dir_hotels if re.search(mainland_pat, h["name"])]

# Write report
with open("deep_audit.txt","w",encoding="utf-8") as f:
    f.write(f"=== BAD zh Wikipedia matches (<3 char overlap): {len(bad_zh)} ===\n")
    for slug,(hn,wt,n) in bad_zh.items():
        f.write(f"  {slug} | hotel={hn!r} | wiki={wt!r} | overlap={n}\n")
    f.write(f"\n=== BAD en Wikipedia matches: {len(bad_en)} ===\n")
    for slug,(hn,et) in bad_en.items():
        f.write(f"  {slug} | hotel={hn!r} | wiki={et!r}\n")
    f.write(f"\n=== OSM outside HK bbox: {len(bad_osm)} ===\n")
    for slug,(n,lat,lng) in bad_osm.items():
        f.write(f"  {slug} | {n!r} | {lat},{lng}\n")
    f.write(f"\n=== Duplicate names: {len(dupes)} ===\n")
    for k,v in dupes.items(): f.write(f"  {k!r} -> {v}\n")
    f.write(f"\n=== Mainland names: {len(bad_mainland)} ===\n")
    for s in bad_mainland: f.write(f"  {s} | {name_by_slug.get(s)!r}\n")

print(f"bad zh wiki: {len(bad_zh)}")
print(f"bad en wiki: {len(bad_en)}")
print(f"osm outside bbox: {len(bad_osm)}")
print(f"duplicate names: {len(dupes)}")
print(f"mainland names: {len(bad_mainland)}")
print("report: deep_audit.txt")
