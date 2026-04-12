"""Second pass: fix remaining issues on HKhotel-en.html.
- Wrap ALL remaining featured hotel-cards in <a> (previous run missed some)
- Link ALL directory rows to dir-*.html pages (previous run only caught <br> rows)
"""
import json, re
from pathlib import Path

p = Path("pages/HKhotel-en.html")
s = p.read_text(encoding="utf-8")

hotels = json.loads(Path("hotels_data.json").read_text(encoding="utf-8"))
dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))
wiki = json.loads(Path("wiki_images.json").read_text(encoding="utf-8"))
BAD = {"grand-hyatt-hong-kong","hotel-ease-access-tsuen-wan","dorsett-tsuen-wan",
       "bridal-tea-house-hotel","regala-skycity-hotel","w-hong-kong"}
for k in BAD: wiki[k] = None

name_to_slug_featured = {h["name"]: h["slug"] for h in hotels}
name_to_img = {h["name"]: (wiki.get(h["slug"]) or h["img"]) for h in hotels}
name_to_old_img = {h["name"]: h["img"] for h in hotels}

# ------- Fix featured cards not yet wrapped -------
dir_idx = s.find("Trip.com Full Hotel Directory")
head = s[:dir_idx]; tail = s[dir_idx:]

# Find all plain <div class="hotel-card"> (not preceded by our <a class="hotel-card-link">)
# Walk through all card markers; for each, check if preceded by <a> wrapper already.
pattern = re.compile(r'<div class="hotel-card">')
new_parts = []
last = 0
for m in pattern.finditer(head):
    start = m.start()
    prefix = head[last:start]
    # Check if prefix ends with the <a class="hotel-card-link" ...> opening (already wrapped)
    if re.search(r'<a href="/pages/hotels/[^"]+" class="hotel-card-link"[^>]*>\s*$', prefix):
        # already wrapped, skip processing (leave as-is, will be handled at end)
        new_parts.append(prefix)
        new_parts.append(m.group(0))
        last = m.end()
        continue
    # This card needs wrapping. Find end of card by balancing divs.
    depth = 1; idx = m.end()
    while depth > 0 and idx < len(head):
        mm = re.search(r'<div\b|</div>', head[idx:])
        if not mm: break
        tag = mm.group(0); idx += mm.end()
        if tag == '</div>': depth -= 1
        else: depth += 1
    card_body = head[m.end():idx]  # inside card
    # extract name
    nm = re.search(r'<div class="hotel-name">([^<]+)</div>', card_body)
    if not nm:
        new_parts.append(prefix); new_parts.append(head[m.start():idx]); last = idx; continue
    name = nm.group(1).strip()
    slug = name_to_slug_featured.get(name)
    if not slug:
        new_parts.append(prefix); new_parts.append(head[m.start():idx]); last = idx; continue
    # remove hotel-platforms block
    new_card_body = re.sub(r'<div class="hotel-platforms">.*?</div>\s*', '', card_body, flags=re.DOTALL)
    # swap image
    new_img = name_to_img.get(name); old_img = name_to_old_img.get(name)
    if new_img and old_img and new_img != old_img:
        new_card_body = new_card_body.replace(old_img, new_img, 1)
    # card closing is the last </div> within idx range (included)
    # Reconstruct: <a>...<div class="hotel-card">...card_body... (balanced)</a>
    new_card = (
        f'<a href="/pages/hotels/{slug}.html" class="hotel-card-link" style="text-decoration:none;color:inherit;display:block;">'
        '<div class="hotel-card">' + new_card_body + '</a>'
    )
    new_parts.append(prefix)
    new_parts.append(new_card)
    last = idx
new_parts.append(head[last:])
head = ''.join(new_parts)

# ------- Directory: make every row clickable by matching dir_hotels names directly -------
name_to_dir_slug = {h["name"]: h["slug"] for h in dir_hotels}

for name, slug in name_to_dir_slug.items():
    # Target 1: plain row, td ends right after name (no <br>)
    # <td ...>NAME</td>  ->  <td ...><a href=...>NAME</a></td>
    pat1 = re.compile(
        r'(<td[^>]*font-weight:500;[^>]*>)' + re.escape(name) + r'(</td>)')
    tail, n1 = pat1.subn(
        rf'\1<a href="/pages/hotels/{slug}.html" style="color:#333;text-decoration:none;">{name}</a>\2',
        tail, count=1)

# Clean up: if dir name is followed by <br> subtitle that wasn't wrapped earlier in prior run, wrap now
for name, slug in name_to_dir_slug.items():
    # Row with subtitle not yet wrapped
    pat2 = re.compile(
        r'(<td[^>]*font-weight:500;[^>]*>)' + re.escape(name) + r'(<br>)')
    tail, _ = pat2.subn(
        rf'\1<a href="/pages/hotels/{slug}.html" style="color:#333;text-decoration:none;">{name}</a>\2',
        tail, count=1)

final = head + tail
p.write_text(final, encoding="utf-8")
print("HKhotel-en.html second-pass applied")

# Verify
end = final.find("Trip.com Full Hotel Directory")
print("featured hotel-card-link:", final[:end].count("hotel-card-link"))
print("featured platform-btn (excl CSS):", final[:end].count("platform-btn") - 2)
print("directory clickable names:", final[end:].count("/pages/hotels/dir-"))
