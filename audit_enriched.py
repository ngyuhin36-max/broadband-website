"""Audit enriched (zh wiki) entries and remove those where the Wikipedia article
doesn't look like a hotel/accommodation."""
import json, re
from pathlib import Path

enriched = json.loads(Path("directory_enriched.json").read_text(encoding="utf-8"))
en_wiki = json.loads(Path("en_wiki.json").read_text(encoding="utf-8"))
d = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))
name_by_slug = {h["slug"]: h["name"] for h in d}

HOTEL_KW = [
    "酒店","飯店","旅館","賓館","賓舘","旅店","旅舍","客棧","民宿",
    "Hotel","hotel","Inn","Lodge","Hostel","Resort","Suites","Guesthouse",
    "Mansion","Tower","House","Plaza","Residences","Suite",
    "大廈","大酒店","會館","度假村","旅店","公寓","Apartments","Apartment",
    "Chungking",  # Chungking Mansions
]

def is_hotel_like(title):
    if not title: return False
    return any(k in title for k in HOTEL_KW)

bad_enriched = {}
for slug, info in enriched.items():
    t = info.get("wiki_title","")
    if not is_hotel_like(t):
        bad_enriched[slug] = t

bad_en = {}
for slug, info in en_wiki.items():
    t = info.get("en_title","")
    if not is_hotel_like(t):
        bad_en[slug] = t

print(f"bad zh enriched: {len(bad_enriched)}")
for slug, t in list(bad_enriched.items())[:30]:
    print(f"  {slug} -> {t!r} (hotel: {name_by_slug.get(slug,'?')!r})")
print(f"\nbad en wiki: {len(bad_en)}")
for slug, t in list(bad_en.items())[:30]:
    print(f"  {slug} -> {t!r}")

# Remove
for slug in bad_enriched: enriched.pop(slug)
for slug in bad_en: en_wiki.pop(slug)
Path("directory_enriched.json").write_text(json.dumps(enriched,ensure_ascii=False,indent=2),encoding="utf-8")
Path("en_wiki.json").write_text(json.dumps(en_wiki,ensure_ascii=False,indent=2),encoding="utf-8")

# Regenerate pages that had bad content — we need to re-render these pages
# without the bad Wikipedia content. Re-run enhance_seo_geo for zh, and build_en for en
import subprocess
print("\nRegenerating pages...")
# Just reset affected subpages to template
# We'll rely on enhance_seo_geo.py + build_en to regenerate, but those scripts
# still use the coord-less template. Need to invoke them.
affected_slugs = set(bad_enriched) | set(bad_en)
print(f"\naffected slugs: {len(affected_slugs)}")
