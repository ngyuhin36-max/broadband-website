"""Apply same structural changes to HKhotel-en.html as we did to HKhotel.html:
1. Add Klook search widget after hero
2. Add Trip.com iframe in sidebar under Popular Areas
3. Wrap each hotel-card with <a> to /pages/hotels/{slug}.html; remove .hotel-platforms
4. Apply Wikipedia real images to featured cards
5. Directory table: remove 'Book' column + 'Compare' button cells, make row names clickable
"""
import json, re
from pathlib import Path

p = Path("pages/HKhotel-en.html")
s = p.read_text(encoding="utf-8")

hotels = json.loads(Path("hotels_data.json").read_text(encoding="utf-8"))   # 38 featured
dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))
wiki = json.loads(Path("wiki_images.json").read_text(encoding="utf-8"))
BAD = {"grand-hyatt-hong-kong","hotel-ease-access-tsuen-wan","dorsett-tsuen-wan",
       "bridal-tea-house-hotel","regala-skycity-hotel","w-hong-kong"}
for k in BAD: wiki[k] = None

name_to_slug_featured = {h["name"]: h["slug"] for h in hotels}
name_to_img = {h["name"]: (wiki.get(h["slug"]) or h["img"]) for h in hotels}
name_to_old_img = {h["name"]: h["img"] for h in hotels}

# --- 1. Add Klook widget after hero (before Intro Guide) ---
widget_block = '''
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
s = s.replace('    <!-- Intro Guide (SEO Content) -->', widget_block, 1)

# --- 2. Add Trip.com iframe under Popular Areas ---
trip_iframe_block = '''                <div class="filter-item"><span>Lantau Island</span><span class="filter-count">6</span></div>
            </div>
            <div class="filter-box" style="text-align:center;padding:10px;">
                <iframe src="https://hk.trip.com/partners/ad/S15444599?Allianceid=8067382&SID=305319575&trip_sub1=" style="width:100%;max-width:320px;height:320px;border:none;" frameborder="0" scrolling="no" id="S15444599"></iframe>
            </div>
        </aside>'''
s = s.replace(
    '                <div class="filter-item"><span>Lantau Island</span><span class="filter-count">6</span></div>\n            </div>\n        </aside>',
    trip_iframe_block, 1)

# --- 3. Wrap hotel-card with <a>, remove .hotel-platforms block, update images ---
# Split the head (before directory) and process featured cards
dir_idx = s.find("Trip.com Full Hotel Directory")
head = s[:dir_idx]
tail = s[dir_idx:]

parts = re.split(r'(<div class="hotel-card">)', head)
out = [parts[0]]
for i in range(1, len(parts), 2):
    marker = parts[i]
    content = parts[i+1] if i+1 < len(parts) else ''
    nm = re.search(r'<div class="hotel-name">([^<]+)</div>', content)
    if not nm:
        out.append(marker + content); continue
    name = nm.group(1).strip()
    slug = name_to_slug_featured.get(name)
    if not slug:
        out.append(marker + content); continue
    # Balance div count to find card end
    depth = 1; idx = 0
    while depth > 0 and idx < len(content):
        m = re.search(r'<div\b|</div>', content[idx:])
        if not m: break
        tag = m.group(0); idx += m.end()
        if tag == '</div>': depth -= 1
        else: depth += 1
    inner = content[:idx]; rest = content[idx:]
    # remove .hotel-platforms block
    inner = re.sub(r'<div class="hotel-platforms">.*?</div>\s*', '', inner, flags=re.DOTALL)
    # update image
    new_img = name_to_img.get(name)
    old_img = name_to_old_img.get(name)
    if new_img and old_img and new_img != old_img:
        inner = inner.replace(old_img, new_img, 1)
    # wrap with <a>
    new_marker = f'<a href="/pages/hotels/{slug}.html" class="hotel-card-link" style="text-decoration:none;color:inherit;display:block;">{marker}'
    inner = inner + '</a>'
    out.append(new_marker + inner + rest)
head = ''.join(out)

# --- 4. Directory: remove 'Book' column header + 'Compare' cell; make rows clickable ---
name_to_dir_slug = {h["name"]: h["slug"] for h in dir_hotels}

# Remove the 'Book' th
tail = tail.replace(
    '<th style="padding:10px;text-align:center;border-radius:0 8px 0 0;">Book</th>',
    '')
# Round last column: 'Original' becomes the last column
tail = tail.replace(
    '<th style="padding:10px;text-align:center;">Original</th>',
    '<th style="padding:10px;text-align:center;border-radius:0 8px 0 0;">Original</th>')
# Remove <td>...Compare button...</td>
tail = re.sub(
    r'\n\s*<td[^>]*>\s*<a href="https://hk\.trip\.com/hotels/list[^\"]*"[^>]*>Compare</a></td>',
    '', tail)
# Footer note: 'Click "Compare" ...'
tail = re.sub(
    r'<p style="color:#888[^"]*">\* Prices.*?</p>',
    '<p style="color:#888;font-size:0.78em;margin-top:10px;">* Prices for reference only; actual rates depend on dates.</p>',
    tail, count=1, flags=re.DOTALL)

# Make each directory row name clickable. Pattern: <td ... font-weight:500;">ZH_NAME<br>...
def repl_row(match):
    full = match.group(0)
    zh_name = match.group(1).strip()
    slug = name_to_dir_slug.get(zh_name)
    if not slug:
        return full
    return full.replace(
        f'>{zh_name}<br>',
        f'><a href="/pages/hotels/{slug}.html" style="color:#333;text-decoration:none;">{zh_name}</a><br>',
        1)
tail = re.sub(
    r'<td[^>]*font-weight:500;[^>]*>([^<]+)<br>',
    repl_row, tail)

new_content = head + tail
p.write_text(new_content, encoding="utf-8")
print("HKhotel-en.html updated")
