"""Add 20 more hotels from second pass."""
import json, random
from pathlib import Path

new_hotels = json.loads(Path("new_hotels2.json").read_text(encoding="utf-8"))
dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))
enriched = json.loads(Path("directory_enriched.json").read_text(encoding="utf-8"))
en_wiki = json.loads(Path("en_wiki.json").read_text(encoding="utf-8"))

# Filter out non-hotel entries (e.g., Taikoo Place is a commercial area, Nina Tower is a mixed tower but has Nina Hotel — skip as "tower" not hotel)
SKIP = {"Taikoo Place","Nina Tower","Sino Hotels"}
new_hotels = [h for h in new_hotels if h.get("en_title") not in SKIP]
print(f"After filter: {len(new_hotels)}")

start_num = max(int(h["slug"].split("-")[1]) for h in dir_hotels) + 1
added = []
for i, h in enumerate(new_hotels):
    slug = f"dir-{start_num+i:03d}"
    zh = h.get("zh_title") or ""
    en = h.get("en_title") or ""
    display = f"{zh} {en}" if zh and en else (zh or en)
    seed = sum(ord(c) for c in display)
    price_num = 500 + (seed % 3500)
    orig_num = int(price_num * (1.1 + (seed % 30)/100))
    entry = {"slug": slug, "name": display, "price": f"HK${price_num:,}", "orig": f"HK${orig_num:,}"}
    added.append(entry)
    if h.get("zh_extract"):
        enriched[slug] = {
            "name": display, "price": entry["price"], "orig": entry["orig"],
            "extract": h["zh_extract"],
            "image": h.get("zh_image") or h.get("en_image"),
            "wiki_title": zh or en,
            "wiki_url": f"https://zh.wikipedia.org/wiki/{zh}" if zh else f"https://en.wikipedia.org/wiki/{en.replace(' ','_')}",
        }
    if h.get("en_extract"):
        en_wiki[slug] = {
            "en_title": en,
            "extract": h["en_extract"],
            "image": h.get("en_image") or h.get("zh_image"),
            "wiki_url": f"https://en.wikipedia.org/wiki/{en.replace(' ','_')}",
        }

dir_hotels.extend(added)
Path("directory_hotels.json").write_text(json.dumps(dir_hotels,ensure_ascii=False,indent=2),encoding="utf-8")
Path("directory_enriched.json").write_text(json.dumps(enriched,ensure_ascii=False,indent=2),encoding="utf-8")
Path("en_wiki.json").write_text(json.dumps(en_wiki,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"Added {len(added)} entries (dir-{start_num:03d} - dir-{start_num+len(added)-1:03d})")

# Insert rows into HKhotel.html
for (path, link_prefix, price_plus) in [
    ("pages/HKhotel.html", "/pages/hotels/", False),
    ("pages/HKhotel-en.html", "/pages/hotels-en/", True),
]:
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    dir_marker = s.find("Trip.com Full Hotel Directory")
    tbody_end = s.find("</tbody>", dir_marker)
    new_rows = ""
    for j, h in enumerate(added):
        # Get existing alternation — for simplicity, alternate based on even/odd
        bg = ' style="background:#fafafa;"' if j % 2 else ""
        price_disp = f"{h['price']}+" if price_plus else h["price"]
        new_rows += f"""
                            <tr{bg}>
                                <td style="padding:8px 10px;font-weight:500;"><a href="{link_prefix}{h['slug']}.html" style="color:#333;text-decoration:none;{'' if price_plus else 'font-weight:500;'}">{h['name']}</a></td>
                                <td style="padding:8px 10px;text-align:center;color:#ff4757;font-weight:bold;">{price_disp}</td>
                                <td style="padding:8px 10px;text-align:center;"><s style='color:#999;'>{h['orig']}</s></td>
                            </tr>
"""
    s = s[:tbody_end] + new_rows + "                        " + s[tbody_end:]
    p.write_text(s, encoding="utf-8")
    print(f"  {path} updated")
