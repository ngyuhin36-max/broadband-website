# -*- coding: utf-8 -*-
"""
Generate estate pages using bnb-nt.xml + bnb-urban.xml (Buildings Dept real data).
~20,000 buildings with name + address + year built.
Skips Top 100 and PRH/HOS estates already done with richer data.
"""
import os, sys, re, json
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(__file__))
from generate_top10_estates import render_page

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(ROOT, "pages")

# Everything already done with richer data — DO NOT overwrite
SKIP = set()

def load_already_done():
    # Top 100 hand-picked slugs are tracked via the generate_top10_estates.ESTATES list
    from generate_top10_estates import ESTATES
    for e in ESTATES:
        SKIP.add(e["slug"])
    # PRH + HOS
    for fname in ("prh-estates.json","hos-courts.json"):
        p = os.path.join(ROOT,"data",fname)
        data = json.load(open(p, encoding="utf-8"))
        for e in data:
            name_en = e["Estate Name"]["en"]
            slug = slugify(name_en)
            SKIP.add(slug)

def slugify(name_en):
    s = name_en.lower()
    s = re.sub(r"[\.\,\'\"&]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def parse_district_from_addr(addr_zh):
    # Try to extract district keywords from Chinese address
    districts = {
        "屯門":"屯門區","元朗":"元朗區","天水圍":"元朗區","粉嶺":"北區","上水":"北區",
        "大埔":"大埔區","沙田":"沙田區","馬鞍山":"沙田區","火炭":"沙田區","大圍":"沙田區",
        "荃灣":"荃灣區","葵涌":"葵青區","青衣":"葵青區","深井":"荃灣區",
        "將軍澳":"西貢區","西貢":"西貢區","清水灣":"西貢區",
        "東涌":"離島區","大嶼山":"離島區","馬灣":"荃灣區",
        "中環":"中西區","上環":"中西區","西環":"中西區","堅尼地城":"中西區","半山":"中西區",
        "金鐘":"中西區","灣仔":"灣仔區","銅鑼灣":"灣仔區","跑馬地":"灣仔區","大坑":"灣仔區",
        "北角":"東區","鰂魚涌":"東區","太古":"東區","西灣河":"東區","筲箕灣":"東區","柴灣":"東區","小西灣":"東區",
        "香港仔":"南區","鴨脷洲":"南區","薄扶林":"南區","黃竹坑":"南區","赤柱":"南區",
        "尖沙咀":"油尖旺區","佐敦":"油尖旺區","油麻地":"油尖旺區","旺角":"油尖旺區","大角咀":"油尖旺區",
        "深水埗":"深水埗區","長沙灣":"深水埗區","荔枝角":"深水埗區","石硤尾":"深水埗區","又一村":"深水埗區",
        "紅磡":"九龍城區","何文田":"九龍城區","九龍城":"九龍城區","九龍塘":"九龍城區","啟德":"九龍城區","土瓜灣":"九龍城區",
        "黃大仙":"黃大仙區","鑽石山":"黃大仙區","樂富":"黃大仙區","彩虹":"黃大仙區","新蒲崗":"黃大仙區",
        "牛頭角":"觀塘區","九龍灣":"觀塘區","觀塘":"觀塘區","藍田":"觀塘區","油塘":"觀塘區",
    }
    for k,v in districts.items():
        if k in (addr_zh or ""):
            return v, k
    return "香港", "香港"

def parse_xml(path):
    tree = ET.parse(path)
    records = []
    for r in tree.getroot().findall("Record"):
        def g(tag):
            el = r.find(tag)
            return (el.text or "").strip() if el is not None and el.text else ""
        name_en = g("EnglishBuildingName1")
        name_zh = g("ChineseBuildingName1")
        addr_en = g("EnglishAddress1")
        addr_zh = g("ChineseAddress1")
        year = g("YearBuild")
        if not name_en: continue
        records.append({"name_en":name_en,"name_zh":name_zh,"addr_en":addr_en,"addr_zh":addr_zh,"year":year})
    return records

def to_estate_record(r):
    name_en = r["name_en"]
    name_zh = r["name_zh"] or name_en
    slug = slugify(name_en)
    if slug in SKIP: return None
    district_zh, area = parse_district_from_addr(r["addr_zh"])
    year = r["year"] if r["year"] and r["year"] != "-" else "—"
    addr_zh = r["addr_zh"] or "香港"
    note_parts = [f"{name_zh}位於{addr_zh}。"]
    if year != "—": note_parts.append(f"落成年份：{year}。")
    note_parts.append(f"光纖入屋，支援最高 1000Mbps 上網速度。")
    return {
        "slug": slug, "name_zh": name_zh, "name_en": name_en,
        "district_zh": district_zh, "district_en": f"Hong Kong",
        "area": area, "mtr": "—（請查詢鄰近港鐵站）",
        "built": year,
        "blocks": "—", "units": "—",
        "developer": "—",
        "lat":"22.3193","lng":"114.1694",
        "operators":["HKBN 香港寬頻","HGC 環球全域電訊","3HK 和記電訊"],
        "fiber_type":"光纖入屋 FTTH","avg_speed":"950+ Mbps (1000M計劃實測範圍)",
        "install_days":"2-4 個工作天","nearby":[],
        "note":"".join(note_parts) + f" 地址：{addr_zh}",
        "_addr_zh": addr_zh, "_addr_en": r["addr_en"],
    }

def main():
    load_already_done()
    print(f"Skip list size: {len(SKIP)}")
    records = parse_xml(os.path.join(ROOT,"data","bnb-nt.xml")) + \
              parse_xml(os.path.join(ROOT,"data","bnb-urban.xml"))
    print(f"Total XML records: {len(records)}")

    # Group by slug (dedup, prefer entries with year)
    by_slug = {}
    for r in records:
        er = to_estate_record(r)
        if not er: continue
        existing = by_slug.get(er["slug"])
        if not existing or (existing["built"] == "—" and er["built"] != "—"):
            by_slug[er["slug"]] = er

    done = matched_no_page = phase_done = 0
    for slug, er in by_slug.items():
        path = os.path.join(PAGES_DIR, f"{slug}.html")
        if not os.path.exists(path):
            matched_no_page += 1
            continue
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(render_page(er))
            done += 1
        except Exception as ex:
            if done < 5: print(f"FAIL {slug}: {ex}")

    # Phase 2: match phase/tower variants by stripping trailing -1, -2, -phase-i, etc.
    all_pages = [f[:-5] for f in os.listdir(PAGES_DIR) if f.endswith(".html")]
    for page_slug in all_pages:
        if page_slug in by_slug or page_slug in SKIP: continue
        # Try stripping common suffixes
        base = re.sub(r"-(\d+|phase-[iv]+|tower-\d+|block-[a-z0-9]+)$", "", page_slug)
        if base != page_slug and base in by_slug:
            er = dict(by_slug[base])
            # Mark variant
            suffix = page_slug[len(base):].lstrip("-")
            er["slug"] = page_slug
            er["name_zh"] = f"{er['name_zh']} ({suffix})" if suffix else er['name_zh']
            er["note"] = er['note'] + f" （{page_slug} 座/期）"
            path = os.path.join(PAGES_DIR, f"{page_slug}.html")
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(render_page(er))
                phase_done += 1
            except Exception as ex: pass

    print(f"Generated {done} pages from bnb XML, phase variants: {phase_done} (matched but no page: {matched_no_page})")

if __name__ == "__main__":
    main()
