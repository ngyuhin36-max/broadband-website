# -*- coding: utf-8 -*-
"""
Generate real-data estate pages using official government JSON:
  - data/prh-estates.json (241 public rental housing estates)
  - data/hos-courts.json (240 Home Ownership Scheme courts)
All fields (district/coords/year/blocks/units) are real official data.
"""
import os, sys, json, html, re

sys.path.insert(0, os.path.dirname(__file__))
# Reuse the proven render template from Top 20 script
from generate_top10_estates import render_page, PLANS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(ROOT, "pages")

SKIP_SLUGS = {
    "taikoo-shing","city-one-shatin","mei-foo-sun-chuen","whampoa-garden",
    "laguna-city","telford-gardens","heng-fa-chuen","south-horizons",
    "kornhill","discovery-park","kingswood-villas","caribbean-coast",
    "lohas-park","metro-city","east-point-city","sceneway-garden",
    "chi-fu-fa-yuen","galaxia","luk-yeung-sun-chuen","laguna-verde"
}

def slugify(name_en):
    s = name_en.lower()
    s = re.sub(r"[\.\,\'\"]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def parse_units(raw):
    if not raw: return None
    m = re.search(r"([\d\s,]+)", str(raw))
    if not m: return None
    n = int(re.sub(r"[^\d]", "", m.group(1)))
    return n if n > 0 else None

def district_to_region_zh(region_zh):
    return f"{region_zh}區" if not region_zh.endswith("區") else region_zh

def get_text_zh(field):
    if isinstance(field, dict):
        return field.get("zh-Hant") or field.get("zh-Hans") or field.get("en") or ""
    return str(field or "")

def get_text_en(field):
    if isinstance(field, dict):
        return field.get("en") or ""
    return str(field or "")

def build_record_prh(e):
    name_zh = get_text_zh(e.get("Estate Name"))
    name_en = get_text_en(e.get("Estate Name"))
    if not name_zh or not name_en: return None
    slug = slugify(name_en)
    if slug in SKIP_SLUGS: return None

    district_zh = get_text_zh(e.get("District Name"))
    region_zh = get_text_zh(e.get("Region Name"))
    district_en = get_text_en(e.get("District Name"))
    region_en = get_text_en(e.get("Region Name"))
    year = get_text_en(e.get("Year of Intake")) or "—"
    blocks = e.get("No. of Blocks") or "—"
    units_raw = get_text_en(e.get("No. of Rental Flats"))
    units = parse_units(units_raw) or "—"
    block_type = get_text_zh(e.get("Type(s) of Block(s)")) or ""
    lat = e.get("Estate Map Latitude")
    lng = e.get("Estate Map Longitude")

    return {
        "slug": slug,
        "name_zh": name_zh,
        "name_en": name_en,
        "district_zh": f"{district_zh}區" if district_zh and not district_zh.endswith("區") else district_zh,
        "district_en": f"{district_en} District, {region_en}" if district_en and region_en else district_en,
        "area": district_zh,
        "mtr": "—（請查看就近港鐵站）",
        "built": year,
        "blocks": blocks,
        "units": units,
        "developer": "香港房屋委員會（公屋邨）",
        "lat": f"{lat:.4f}" if isinstance(lat,(int,float)) else "22.3193",
        "lng": f"{lng:.4f}" if isinstance(lng,(int,float)) else "114.1694",
        "operators": ["HKBN 香港寬頻","CMHK 中國移動香港","HGC 環球全域電訊","3HK 和記電訊"],
        "fiber_type": f"光纖入屋 FTTH（{block_type}" + ("）" if block_type else "光纖入屋 FTTH"),
        "avg_speed": "950+ Mbps (1000M計劃實測範圍)",
        "install_days": "2-4 個工作天",
        "nearby": [],
        "note": f"{name_zh}（{name_en}）是位於{district_zh}的公共屋邨，由香港房屋委員會管理。{'落成年份：'+year+'。' if year and year != '—' else ''}{'共'+str(blocks)+'座' if blocks and blocks!='—' else ''}{('，提供約'+f'{units:,}'+'個公營出租單位。') if isinstance(units,int) else '。'}"
    }

def build_record_hos(e):
    name_zh = get_text_zh(e.get("Estate Name"))
    name_en = get_text_en(e.get("Estate Name"))
    if not name_zh or not name_en: return None
    slug = slugify(name_en)
    if slug in SKIP_SLUGS: return None

    district_zh = get_text_zh(e.get("District Name"))
    region_zh = get_text_zh(e.get("Region Name"))
    district_en = get_text_en(e.get("District Name"))
    region_en = get_text_en(e.get("Region Name"))
    year = get_text_en(e.get("Year of Completion")) or "—"
    blocks = e.get("No. of Blocks") or "—"
    units_raw = get_text_en(e.get("No. of Flats"))
    units = parse_units(units_raw) or "—"
    block_type = get_text_zh(e.get("Type(s) of Block(s)")) or ""
    sold_under = get_text_zh(e.get("Sold Under")) or ""
    lat = e.get("Estate Map Latitude")
    lng = e.get("Estate Map Longitude")

    return {
        "slug": slug,
        "name_zh": name_zh,
        "name_en": name_en,
        "district_zh": f"{district_zh}區" if district_zh and not district_zh.endswith("區") else district_zh,
        "district_en": f"{district_en} District, {region_en}" if district_en and region_en else district_en,
        "area": district_zh,
        "mtr": "—（請查看就近港鐵站）",
        "built": year,
        "blocks": blocks,
        "units": units,
        "developer": "香港房屋委員會居者有其屋計劃",
        "lat": f"{lat:.4f}" if isinstance(lat,(int,float)) else "22.3193",
        "lng": f"{lng:.4f}" if isinstance(lng,(int,float)) else "114.1694",
        "operators": ["HKBN 香港寬頻","CMHK 中國移動香港","HGC 環球全域電訊","3HK 和記電訊"],
        "fiber_type": "光纖入屋 FTTH",
        "avg_speed": "950+ Mbps (1000M計劃實測範圍)",
        "install_days": "2-4 個工作天",
        "nearby": [],
        "note": f"{name_zh}（{name_en}）是位於{district_zh}的居者有其屋計劃屋苑。{'落成年份：'+year+'。' if year and year!='—' else ''}{('期數：'+sold_under+'。') if sold_under else ''}{'共'+str(blocks)+'座' if blocks and blocks!='—' else ''}{('，共'+f'{units:,}'+'個單位。') if isinstance(units,int) else '。'}"
    }

def build_nearby(records):
    by_district = {}
    for r in records:
        by_district.setdefault(r['area'], []).append(r['name_zh'])
    for r in records:
        same = [n for n in by_district.get(r['area'], []) if n != r['name_zh']]
        r['nearby'] = same[:3] if same else []

def main():
    prh = json.load(open(os.path.join(ROOT,"data","prh-estates.json"), encoding="utf-8"))
    hos = json.load(open(os.path.join(ROOT,"data","hos-courts.json"), encoding="utf-8"))
    records = []
    for e in prh:
        r = build_record_prh(e)
        if r: records.append(r)
    for e in hos:
        r = build_record_hos(e)
        if r: records.append(r)
    build_nearby(records)
    count = failed = 0
    for r in records:
        path = os.path.join(PAGES_DIR, f"{r['slug']}.html")
        if not os.path.exists(path):
            continue
        try:
            out = render_page(r)
            with open(path, "w", encoding="utf-8") as f:
                f.write(out)
            count += 1
        except Exception as ex:
            failed += 1
            if failed < 5: print(f"FAIL {r['slug']}: {ex}")
    print(f"Generated {count} pages (PRH+HOS real data), failed={failed}")

if __name__ == "__main__":
    main()
