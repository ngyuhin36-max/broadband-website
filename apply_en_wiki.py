"""Apply fetched en.wikipedia content to EN directory pages."""
import json, re, html
from pathlib import Path

en_wiki = json.loads(Path("en_wiki.json").read_text(encoding="utf-8"))
dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))
d_by_slug = {h["slug"]: h for h in dir_hotels}

changed = 0
for slug, ew in en_wiki.items():
    path = Path(f"pages/hotels-en/{slug}.html")
    if not path.exists(): continue
    h = d_by_slug.get(slug)
    if not h: continue
    content = path.read_text(encoding="utf-8")

    extract = ew["extract"]
    wiki_url = ew["wiki_url"]
    en_title = ew["en_title"]
    img = ew.get("image") or ""

    # Replace the About section body
    # Pattern: <div class="card">\n<h2>About NAME</h2>\n{old_content}\n</div>
    name = h["name"]
    about_re = re.compile(
        r'(<div class="card">\s*<h2>About [^<]+</h2>\s*)(.*?)(</div>\s*<div class="card">)',
        re.DOTALL)
    new_about_body = (
        f'<p>{html.escape(extract)}</p>'
        f'<div class="wiki-note">📖 Source: <a href="{wiki_url}" target="_blank" rel="noopener noreferrer">Wikipedia &mdash; {html.escape(en_title)}</a> (CC BY-SA)</div>\n'
    )
    new_content, n = about_re.subn(rf'\1{new_about_body}\3', content, count=1)
    if n == 0:
        # fallback: no other card follows; try till end
        about_re2 = re.compile(
            r'(<div class="card">\s*<h2>About [^<]+</h2>\s*)(.*?)(</div>)',
            re.DOTALL)
        new_content, n = about_re2.subn(rf'\1{new_about_body}\3', content, count=1)
    if n:
        # Update schema description
        new_content = re.sub(
            r'("description":")[^"]+(")',
            lambda m: m.group(1)+extract[:250].replace('"','').replace('\\','')+m.group(2),
            new_content, count=1)
        # Update og:image and hero background if we have an image
        if img:
            new_content = re.sub(
                r'(<meta property="og:image" content=")[^"]+(")',
                rf'\1{img}\2', new_content, count=1)
            new_content = re.sub(
                r"(background-image:linear-gradient\(rgba\(26,26,46,0\.55\),rgba\(15,52,96,0\.75\)\),url\(')[^']*('\))",
                rf"\1{img}\2", new_content, count=1)
            # If hero had no image (solid gradient), inject one
            new_content = re.sub(
                r'\.hero\{background:linear-gradient\(135deg,#1a1a2e,#16213e 50%,#0f3460\);',
                f".hero{{background-image:linear-gradient(rgba(26,26,46,0.55),rgba(15,52,96,0.75)),url('{img}');background-size:cover;background-position:center;",
                new_content, count=1)
        path.write_text(new_content, encoding="utf-8")
        changed += 1

print(f"Updated {changed} EN directory pages with en.wikipedia content")
