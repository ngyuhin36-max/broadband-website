"""Wrap the remaining 14 featured cards where name has English district tokens.
Match by the English suffix of the hotel name instead of full zh name.
"""
import json, re
from pathlib import Path

p = Path("pages/HKhotel-en.html")
s = p.read_text(encoding="utf-8")
featured = json.loads(Path("hotels_data.json").read_text(encoding="utf-8"))
wiki = json.loads(Path("wiki_images.json").read_text(encoding="utf-8"))
BAD = {"grand-hyatt-hong-kong","hotel-ease-access-tsuen-wan","dorsett-tsuen-wan",
       "bridal-tea-house-hotel","regala-skycity-hotel","w-hong-kong"}
for k in BAD: wiki[k] = None

# Build map from English suffix → slug/imgs
def en_tail(name):
    m = re.search(r'([A-Za-z][A-Za-z0-9 &\-\'.]*)$', name)
    return m.group(1).strip() if m else name

en_map = {en_tail(h["name"]): {"slug": h["slug"], "old_img": h["img"],
                               "new_img": wiki.get(h["slug"]) or h["img"]}
          for h in featured}

dir_idx = s.find("Trip.com Full Hotel Directory")
head, tail = s[:dir_idx], s[dir_idx:]

# Find all unwrapped <div class="hotel-card"> (not preceded by hotel-card-link)
positions = []
for m in re.finditer(r'<div class="hotel-card">', head):
    pos = m.start()
    back = head[max(0, pos-300):pos]
    if 'class="hotel-card-link"' in back and back.rstrip().endswith('>'):
        continue  # already wrapped
    positions.append(pos)

def card_end(start):
    idx = start + len('<div class="hotel-card">')
    depth = 1
    while depth > 0 and idx < len(head):
        m = re.search(r'<div\b|</div>', head[idx:])
        if not m: return len(head)
        tag = m.group(0); idx += m.end()
        if tag == '</div>': depth -= 1
        else: depth += 1
    return idx

for start in reversed(positions):
    end = card_end(start)
    card = head[start:end]
    nm = re.search(r'<div class="hotel-name">([^<]+)</div>', card)
    if not nm: continue
    name = nm.group(1).strip()
    suffix = en_tail(name)
    info = en_map.get(suffix)
    if not info: continue
    slug = info["slug"]
    new_card = re.sub(r'<div class="hotel-platforms">.*?</div>\s*', '', card, flags=re.DOTALL)
    if info["old_img"] != info["new_img"]:
        new_card = new_card.replace(info["old_img"], info["new_img"], 1)
    wrapped = (
        f'<a href="/pages/hotels/{slug}.html" class="hotel-card-link" style="text-decoration:none;color:inherit;display:block;">'
        f'{new_card}</a>'
    )
    head = head[:start] + wrapped + head[end:]
    print(f"wrapped: {name} -> {slug}")

p.write_text(head + tail, encoding="utf-8")
final = head + tail
end_i = final.find("Trip.com Full Hotel Directory")
print("featured hotel-card-link:", final[:end_i].count("hotel-card-link"))
print("featured platform-btn (excl CSS):", final[:end_i].count("platform-btn") - 2)
