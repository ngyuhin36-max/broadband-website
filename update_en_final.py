"""Clean rewrite: apply all HKhotel.html-style changes to HKhotel-en.html in one pass.

Steps:
1. Klook widget after hero
2. Trip.com iframe in sidebar
3. Wrap each hotel-card in <a>, remove .hotel-platforms, swap to Wikipedia image
4. Remove directory Book column + Compare buttons, make row names clickable
"""
import json, re
from pathlib import Path

p = Path("pages/HKhotel-en.html")
s = p.read_text(encoding="utf-8")

featured = json.loads(Path("hotels_data.json").read_text(encoding="utf-8"))
dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))
wiki = json.loads(Path("wiki_images.json").read_text(encoding="utf-8"))
BAD = {"grand-hyatt-hong-kong","hotel-ease-access-tsuen-wan","dorsett-tsuen-wan",
       "bridal-tea-house-hotel","regala-skycity-hotel","w-hong-kong"}
for k in BAD: wiki[k] = None
f_map = {h["name"]: {"slug": h["slug"], "old_img": h["img"],
                     "new_img": wiki.get(h["slug"]) or h["img"]} for h in featured}
d_map = {h["name"]: h["slug"] for h in dir_hotels}

# ---- 1. Klook widget ----
widget = '''
    <!-- Klook Search Widget -->
    <div style="max-width:1100px;margin:20px auto;padding:0 15px;">
        <ins class="klk-aff-widget" data-wid="118358" data-height="340px" data-adid="1254905" data-lang="en-HK" data-prod="search_vertical" data-currency=""><a href="//www.klook.com/?aid=">Klook.com</a></ins>
        <script type="text/javascript">
            (function (d, sc, u) {
                var s = d.createElement(sc), p = d.getElementsByTagName(sc)[0];
                s.type = "text/javascript"; s.async = true; s.src = u;
                p.parentNode.insertBefore(s, p);
            })(document, "script", "https://affiliate.klook.com/widget/fetch-iframe-init.js");
        </script>
    </div>

    <!-- Intro Guide (SEO Content) -->'''
s = s.replace('    <!-- Intro Guide (SEO Content) -->', widget, 1)

# ---- 2. Trip.com iframe under Popular Areas ----
iframe_block = '''                <div class="filter-item"><span>Lantau Island</span><span class="filter-count">6</span></div>
            </div>
            <div class="filter-box" style="text-align:center;padding:10px;">
                <iframe src="https://hk.trip.com/partners/ad/S15444599?Allianceid=8067382&SID=305319575&trip_sub1=" style="width:100%;max-width:320px;height:320px;border:none;" frameborder="0" scrolling="no" id="S15444599"></iframe>
            </div>
        </aside>'''
s = s.replace(
    '                <div class="filter-item"><span>Lantau Island</span><span class="filter-count">6</span></div>\n            </div>\n        </aside>',
    iframe_block, 1)

# ---- 3. Process featured cards ----
dir_idx = s.find("Trip.com Full Hotel Directory")
head, tail = s[:dir_idx], s[dir_idx:]

# Find all hotel-cards and their full extents by balancing divs
positions = [m.start() for m in re.finditer(r'<div class="hotel-card">', head)]

# Process from END to START so positions don't shift
def card_end(start):
    # find matching </div> for the outer <div class="hotel-card">
    idx = start + len('<div class="hotel-card">')
    depth = 1
    while depth > 0 and idx < len(head):
        m = re.search(r'<div\b|</div>', head[idx:])
        if not m: return len(head)
        tag = m.group(0); idx += m.end()
        if tag == '</div>': depth -= 1
        else: depth += 1
    return idx  # points past the card's closing </div>

new_head = head
# Walk in reverse to keep indices valid
for start in reversed(positions):
    end = card_end(start)
    card = new_head[start:end]
    nm = re.search(r'<div class="hotel-name">([^<]+)</div>', card)
    if not nm: continue
    name = nm.group(1).strip()
    info = f_map.get(name)
    if not info: continue
    slug = info["slug"]
    # Remove platforms block
    new_card = re.sub(r'<div class="hotel-platforms">.*?</div>\s*', '', card, flags=re.DOTALL)
    # Swap image
    if info["old_img"] != info["new_img"]:
        new_card = new_card.replace(info["old_img"], info["new_img"], 1)
    # Wrap in <a>
    wrapped = (
        f'<a href="/pages/hotels/{slug}.html" class="hotel-card-link" style="text-decoration:none;color:inherit;display:block;">'
        f'{new_card}</a>'
    )
    new_head = new_head[:start] + wrapped + new_head[end:]

# ---- 4. Directory changes ----
# Remove Book column
tail = tail.replace(
    '<th style="padding:10px;text-align:center;border-radius:0 8px 0 0;">Book</th>',
    '')
# Round last column = Original
tail = tail.replace(
    '<th style="padding:10px;text-align:center;">Original</th>',
    '<th style="padding:10px;text-align:center;border-radius:0 8px 0 0;">Original</th>')
# Remove Compare button cells
tail = re.sub(
    r'\n\s*<td[^>]*>\s*<a href="https://hk\.trip\.com/hotels/list[^"]*"[^>]*>Compare</a></td>',
    '', tail)
# Footer note
tail = re.sub(
    r'<p style="color:#888[^"]*">[^<]*</p>',
    '<p style="color:#888;font-size:0.78em;margin-top:10px;">* Prices for reference only; actual rates depend on dates.</p>',
    tail, count=1)

# Make directory row names clickable (match both `NAME<br>` and `NAME</td>`)
for name, slug in d_map.items():
    # With subtitle <br>
    pat1 = re.compile(
        r'(<td[^>]*font-weight:500;[^>]*>)' + re.escape(name) + r'(<br>)')
    tail, _ = pat1.subn(
        rf'\1<a href="/pages/hotels/{slug}.html" style="color:#333;text-decoration:none;">{name}</a>\2',
        tail, count=1)
    # Without subtitle, ends with </td>
    pat2 = re.compile(
        r'(<td[^>]*font-weight:500;[^>]*>)' + re.escape(name) + r'(</td>)')
    tail, _ = pat2.subn(
        rf'\1<a href="/pages/hotels/{slug}.html" style="color:#333;text-decoration:none;">{name}</a>\2',
        tail, count=1)

final = new_head + tail
p.write_text(final, encoding="utf-8")

# ---- Verify ----
end_i = final.find("Trip.com Full Hotel Directory")
print("featured hotel-card-link:", final[:end_i].count("hotel-card-link"))
print("featured platform-btn (excl 2 CSS rules):", final[:end_i].count("platform-btn") - 2)
print("directory row links (/pages/hotels/dir-):", final[end_i:].count("/pages/hotels/dir-"))
print("Klook widget:", "klk-aff-widget" in final)
print("Trip iframe:", "S15444599" in final)
