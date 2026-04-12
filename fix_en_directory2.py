"""Link remaining directory rows via fuzzy CJK-only matching.
For each still-unlinked row name in HKhotel-en.html, strip ASCII characters
and match against zh directory names (also ASCII-stripped).
"""
import json, re
from pathlib import Path

p = Path("pages/HKhotel-en.html")
s = p.read_text(encoding="utf-8")
dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))

def zh_only(text):
    """Keep only CJK Unified Ideographs and common CJK punctuation."""
    return "".join(c for c in text if "\u4e00" <= c <= "\u9fff" or c in "（）")

# Build map: zh_only(name) -> list of (slug, original_name)
zh_map = {}
for h in dir_hotels:
    k = zh_only(h["name"])
    zh_map.setdefault(k, []).append((h["slug"], h["name"]))

dir_idx = s.find("Trip.com Full Hotel Directory")
head, tail = s[:dir_idx], s[dir_idx:]

# Find unlinked rows: font-weight:500 td not already wrapped in <a>
unlinked_pattern = re.compile(
    r'(<td[^>]*font-weight:500;[^>]*>)((?!<a)[^<]{2,120})(</td>|<br>)')

matched = 0; ambiguous = 0; unresolved = 0
def replacer(m):
    global matched, ambiguous, unresolved
    opening, name, closing = m.group(1), m.group(2), m.group(3)
    k = zh_only(name)
    if not k:
        unresolved += 1; return m.group(0)
    hits = zh_map.get(k, [])
    if len(hits) == 1:
        slug = hits[0][0]
        matched += 1
        return f'{opening}<a href="/pages/hotels/{slug}.html" style="color:#333;text-decoration:none;">{name}</a>{closing}'
    elif len(hits) > 1:
        ambiguous += 1
    else:
        unresolved += 1
    return m.group(0)

tail = unlinked_pattern.sub(replacer, tail)
p.write_text(head + tail, encoding="utf-8")

total = (head + tail).count("/pages/hotels/dir-")
print(f"newly matched via zh-only: {matched}")
print(f"ambiguous zh keys: {ambiguous}")
print(f"unresolved: {unresolved}")
print(f"total directory links now: {total} / {len(dir_hotels)}")
