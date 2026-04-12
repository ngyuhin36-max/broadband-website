"""Resolve ambiguous directory rows by matching (normalized name, price)."""
import json, re
from pathlib import Path

p = Path("pages/HKhotel-en.html")
s = p.read_text(encoding="utf-8")
dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))

EN_TO_ZH = {"Tsim Sha Tsui":"尖沙咀","Causeway Bay":"銅鑼灣","Wan Chai":"灣仔",
    "Mongkok":"旺角","Mong Kok":"旺角","Central":"中環","Sheung Wan":"上環",
    "Sai Wan":"西環","West Kowloon":"西九龍","Admiralty":"金鐘","Jordan":"佐敦",
    "Yau Ma Tei":"油麻地","Tsuen Wan":"荃灣","Sha Tin":"沙田","Sham Shui Po":"深水埗",
    "Kowloon City":"九龍城","Hung Hom":"紅磡","North Point":"北角","Quarry Bay":"鰂魚涌",
    "Tai Koo":"太古","Tseung Kwan O":"將軍澳","Tai Po":"大埔","Yuen Long":"元朗",
    "Tuen Mun":"屯門","Tung Chung":"東涌","Lantau Island":"大嶼山","Lantau":"大嶼山",
    "Discovery Bay":"愉景灣","Airport":"機場","Chek Lap Kok":"赤鱲角",
    "Sea View":"海景","Ocean Park":"海洋公園","Tsing Yi":"青衣","Kwai Chung":"葵涌",
    "Business":"商務","DISNEY":"迪士尼","Disney":"迪士尼","Harbour View":"海景",
}

def normalize(name):
    for en in sorted(EN_TO_ZH, key=len, reverse=True):
        name = name.replace(en, EN_TO_ZH[en])
    return "".join(c for c in name if "\u4e00" <= c <= "\u9fff")

# key = (normalized_zh, price)
price_map = {(normalize(h["name"]), h["price"]): h["slug"] for h in dir_hotels}

dir_idx = s.find("Trip.com Full Hotel Directory")
head, tail = s[:dir_idx], s[dir_idx:]

# Match row pattern: <tr...><td...font-weight:500...>NAME</td><td...>PRICE</td><td...><s>ORIG</s></td></tr>
row_re = re.compile(
    r'(<tr[^>]*>\s*<td[^>]*font-weight:500;[^>]*>)((?!<a)[^<]{2,120})(</td>\s*<td[^>]*>\s*)([^<]+)(</td>)',
    re.DOTALL)

matched = 0; still = 0
def replacer(m):
    global matched, still
    open_td, name, mid, price, close = m.group(1,2,3,4,5)
    key = (normalize(name), price.strip())
    slug = price_map.get(key)
    if slug:
        matched += 1
        return f'{open_td}<a href="/pages/hotels/{slug}.html" style="color:#333;text-decoration:none;">{name}</a>{mid}{price}{close}'
    still += 1
    return m.group(0)

tail = row_re.sub(replacer, tail)
p.write_text(head + tail, encoding="utf-8")
print(f"matched: {matched}, still unlinked rows: {still}")
total = (head+tail).count("/pages/hotels/dir-")
print(f"total directory links: {total} / {len(dir_hotels)}")
