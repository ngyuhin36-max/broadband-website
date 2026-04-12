"""Match remaining rows against featured hotels (not directory) — some rows in
EN file reference the 38 featured hotels via directory-table format.
"""
import json, re
from pathlib import Path

p = Path("pages/HKhotel-en.html")
s = p.read_text(encoding="utf-8")
featured = json.loads(Path("hotels_data.json").read_text(encoding="utf-8"))

EN_TO_ZH = {"Tsim Sha Tsui":"尖沙咀","Causeway Bay":"銅鑼灣","Wan Chai":"灣仔",
    "Mongkok":"旺角","Central":"中環","West Kowloon":"西九龍","Tsuen Wan":"荃灣",
    "Ocean Park":"海洋公園","Sea View":"海景","Business":"商務","DISNEY":"迪士尼",
    "Admiralty":"金鐘","Jordan":"佐敦","Harbour View":"海景","Disney":"迪士尼",
    "Hung Hom":"紅磡","Tung Chung":"東涌","Lantau":"大嶼山","Airport":"機場",
}
def norm(n):
    for en in sorted(EN_TO_ZH, key=len, reverse=True): n = n.replace(en, EN_TO_ZH[en])
    return "".join(c for c in n if "\u4e00" <= c <= "\u9fff")

# Map normalized zh of featured hotel -> slug
feat_map = {norm(h["name"]): h["slug"] for h in featured}

dir_idx = s.find("Trip.com Full Hotel Directory")
head, tail = s[:dir_idx], s[dir_idx:]

row_re = re.compile(
    r'(<tr[^>]*>\s*<td[^>]*font-weight:500;[^>]*>)((?!<a)[^<]{2,120})(</td>)')
matched = 0; missed = []
def rep(m):
    global matched
    opening, name, closing = m.group(1), m.group(2), m.group(3)
    k = norm(name)
    slug = feat_map.get(k)
    if slug:
        matched += 1
        return f'{opening}<a href="/pages/hotels/{slug}.html" style="color:#333;text-decoration:none;">{name}</a>{closing}'
    missed.append((name, k))
    return m.group(0)

tail = row_re.sub(rep, tail)
p.write_text(head + tail, encoding="utf-8")

print(f"matched to featured: {matched}")
total = (head+tail).count("/pages/hotels/")
print(f"total hotel links in file: {total}")
print(f"\nstill missed ({len(missed)}):")
for n, k in missed[:20]:
    print(f"  name_normalized={k!r}")
