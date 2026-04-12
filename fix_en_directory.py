"""Link the remaining ~78 directory rows in HKhotel-en.html by generating
English-district variants of each zh hotel name and searching the file.
"""
import json, re
from pathlib import Path

p = Path("pages/HKhotel-en.html")
s = p.read_text(encoding="utf-8")
dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))

# Reverse map: zh district token → English equivalents used in HKhotel-en.html
ZH_TO_EN = {
    "銅鑼灣": "Causeway Bay",
    "灣仔":   "Wan Chai",
    "尖沙咀": "Tsim Sha Tsui",
    "旺角":   "Mongkok",
    "中環":   "Central",
    "上環":   "Sheung Wan",
    "西環":   "Sai Wan",
    "金鐘":   "Admiralty",
    "佐敦":   "Jordan",
    "油麻地": "Yau Ma Tei",
    "荃灣":   "Tsuen Wan",
    "沙田":   "Sha Tin",
    "深水埗": "Sham Shui Po",
    "九龍城": "Kowloon City",
    "紅磡":   "Hung Hom",
    "北角":   "North Point",
    "鰂魚涌": "Quarry Bay",
    "太古":   "Tai Koo",
    "將軍澳": "Tseung Kwan O",
    "大埔":   "Tai Po",
    "元朗":   "Yuen Long",
    "屯門":   "Tuen Mun",
    "東涌":   "Tung Chung",
    "大嶼山": "Lantau Island",
    "迪士尼": "DISNEY",
    "愉景灣": "Discovery Bay",
    "機場":   "Airport",
    "赤鱲角": "Chek Lap Kok",
    "海景":   "Sea View",
    "海洋公園": "Ocean Park",
    "青衣":   "Tsing Yi",
    "葵涌":   "Kwai Chung",
}

dir_idx = s.find("Trip.com Full Hotel Directory")
head, tail = s[:dir_idx], s[dir_idx:]

# Count rows already linked
already = tail.count("/pages/hotels/dir-")

def variants(name):
    """Yield name variants with zh district tokens replaced by EN equivalents.
    Handles multiple substitutions combinatorially is overkill; usually 1 token swap."""
    yield name
    seen = {name}
    # Single-token substitutions
    for zh, en in ZH_TO_EN.items():
        if zh in name:
            v = name.replace(zh, en)
            if v not in seen:
                seen.add(v); yield v
    # Two-token combos (for names that have multiple swapped districts)
    for zh1, en1 in ZH_TO_EN.items():
        for zh2, en2 in ZH_TO_EN.items():
            if zh1 >= zh2 or zh1 not in name or zh2 not in name:
                continue
            v = name.replace(zh1, en1).replace(zh2, en2)
            if v not in seen:
                seen.add(v); yield v

def already_linked(name_in_file):
    # returns True if the td containing this name is already wrapped
    m = re.search(
        r'<td[^>]*font-weight:500;[^>]*>\s*<a[^>]+>' + re.escape(name_in_file) + r'</a>',
        tail)
    return bool(m)

matched = 0
for h in dir_hotels:
    name = h["name"]; slug = h["slug"]
    # Skip if the zh name is already linked
    if re.search(rf'<a href="/pages/hotels/{slug}\.html"', tail):
        continue
    for v in variants(name):
        if v == name:
            continue  # already tried by earlier scripts
        # With subtitle
        pat1 = re.compile(r'(<td[^>]*font-weight:500;[^>]*>)' + re.escape(v) + r'(<br>)')
        tail2, n1 = pat1.subn(
            rf'\1<a href="/pages/hotels/{slug}.html" style="color:#333;text-decoration:none;">{v}</a>\2',
            tail, count=1)
        if n1:
            tail = tail2; matched += 1; break
        # No subtitle
        pat2 = re.compile(r'(<td[^>]*font-weight:500;[^>]*>)' + re.escape(v) + r'(</td>)')
        tail2, n2 = pat2.subn(
            rf'\1<a href="/pages/hotels/{slug}.html" style="color:#333;text-decoration:none;">{v}</a>\2',
            tail, count=1)
        if n2:
            tail = tail2; matched += 1; break

p.write_text(head + tail, encoding="utf-8")
new_total = (head + tail).count("/pages/hotels/dir-")
print(f"newly matched: {matched}")
print(f"total directory links now: {new_total}")
