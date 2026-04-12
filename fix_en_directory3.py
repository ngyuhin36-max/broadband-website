"""Final pass: normalize by replacing EN district tokens back to zh, then
strip remaining ASCII, then compare with zh dir hotel names also ASCII-stripped.
"""
import json, re
from pathlib import Path

p = Path("pages/HKhotel-en.html")
s = p.read_text(encoding="utf-8")
dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))

EN_TO_ZH = {
    "Tsim Sha Tsui": "尖沙咀", "Causeway Bay": "銅鑼灣", "Wan Chai": "灣仔",
    "Mongkok": "旺角", "Mong Kok": "旺角", "Central": "中環",
    "Sheung Wan": "上環", "Sai Wan": "西環", "West Kowloon": "西九龍",
    "Admiralty": "金鐘", "Jordan": "佐敦", "Yau Ma Tei": "油麻地",
    "Tsuen Wan": "荃灣", "Sha Tin": "沙田", "Sham Shui Po": "深水埗",
    "Kowloon City": "九龍城", "Hung Hom": "紅磡", "North Point": "北角",
    "Quarry Bay": "鰂魚涌", "Tai Koo": "太古", "Tseung Kwan O": "將軍澳",
    "Tai Po": "大埔", "Yuen Long": "元朗", "Tuen Mun": "屯門",
    "Tung Chung": "東涌", "Lantau Island": "大嶼山", "Lantau": "大嶼山",
    "Discovery Bay": "愉景灣", "Airport": "機場", "Chek Lap Kok": "赤鱲角",
    "Sea View": "海景", "Ocean Park": "海洋公園", "Tsing Yi": "青衣",
    "Kwai Chung": "葵涌", "Business": "商務", "DISNEY": "迪士尼",
    "Disney": "迪士尼", "Harbour View": "海景",
}

def normalize(name):
    """Replace EN district tokens with zh equivalents, then strip ASCII + spaces."""
    # Sort keys by length descending for proper multi-word replacement
    for en in sorted(EN_TO_ZH, key=len, reverse=True):
        name = name.replace(en, EN_TO_ZH[en])
    return "".join(c for c in name if "\u4e00" <= c <= "\u9fff")

zh_map = {}
for h in dir_hotels:
    k = normalize(h["name"])
    zh_map.setdefault(k, []).append(h["slug"])

dir_idx = s.find("Trip.com Full Hotel Directory")
head, tail = s[:dir_idx], s[dir_idx:]

pattern = re.compile(
    r'(<td[^>]*font-weight:500;[^>]*>)((?!<a)[^<]{2,120})(</td>|<br>)')

matched = 0; ambiguous = 0; unresolved_samples = []

def replacer(m):
    global matched, ambiguous
    opening, name, closing = m.group(1), m.group(2), m.group(3)
    k = normalize(name)
    if not k:
        unresolved_samples.append(name); return m.group(0)
    hits = zh_map.get(k)
    if hits and len(hits) == 1:
        slug = hits[0]; matched += 1
        return f'{opening}<a href="/pages/hotels/{slug}.html" style="color:#333;text-decoration:none;">{name}</a>{closing}'
    if hits and len(hits) > 1:
        ambiguous += 1
        unresolved_samples.append(f"AMBIG({len(hits)}): {name}")
    else:
        unresolved_samples.append(name)
    return m.group(0)

tail = pattern.sub(replacer, tail)
p.write_text(head + tail, encoding="utf-8")

total = (head + tail).count("/pages/hotels/dir-")
print(f"matched: {matched}, ambiguous: {ambiguous}")
print(f"total directory links: {total} / {len(dir_hotels)}")
if unresolved_samples:
    print(f"\nunresolved ({len(unresolved_samples)}):")
    for n in unresolved_samples[:20]: print(" ", repr(n))
