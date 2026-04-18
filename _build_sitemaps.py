from pathlib import Path
from datetime import date
from urllib.parse import quote

ROOT = Path(__file__).parent
RICH_LIST = ROOT / "_rich_pages.txt"
TODAY = date.today().isoformat()
BASE_URL = "https://broadbandhk.com/pages/"

rich_pages_raw = sorted(
    line.strip() for line in RICH_LIST.read_text(encoding="utf-8").splitlines() if line.strip()
)
rich_pages = [f for f in rich_pages_raw if not f.startswith("#") and not f.startswith("@")]
skipped = len(rich_pages_raw) - len(rich_pages)
print(f"Skipped filenames with leading # or @: {skipped}")
print(f"Rich pages: {len(rich_pages)}")

chunks = [rich_pages[i::3] for i in range(3)]
total_check = sum(len(c) for c in chunks)
print(f"Split into 3 chunks: {[len(c) for c in chunks]} (total {total_check})")

def url_entry(filename: str) -> str:
    encoded = quote(filename, safe="-_.")
    return (
        f'  <url><loc>{BASE_URL}{encoded}</loc>'
        f'<lastmod>{TODAY}</lastmod>'
        f'<changefreq>monthly</changefreq>'
        f'<priority>0.7</priority></url>'
    )

for i, chunk in enumerate(chunks, start=2):
    path = ROOT / f"sitemap-{i}.xml"
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    lines.extend(url_entry(f) for f in chunk)
    lines.append('</urlset>')
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {path.name} with {len(chunk)} URLs")

index_path = ROOT / "sitemap.xml"
current = index_path.read_text(encoding="utf-8").splitlines()

new_entries = [
    f'  <sitemap><loc>https://broadbandhk.com/sitemap-{i}.xml</loc><lastmod>{TODAY}</lastmod></sitemap>'
    for i in (2, 3, 4)
]

filtered = []
skip_old_234 = False
for line in current:
    if any(f'sitemap-{i}.xml' in line for i in (2, 3, 4)):
        continue
    filtered.append(line)

out_lines = []
inserted = False
for line in filtered:
    if '<sitemap><loc>https://broadbandhk.com/sitemap-5.xml' in line and not inserted:
        out_lines.extend(new_entries)
        inserted = True
    out_lines.append(line)

if not inserted:
    final_out = []
    for line in out_lines:
        if '</sitemapindex>' in line:
            final_out.extend(new_entries)
        final_out.append(line)
    out_lines = final_out

index_path.write_text("\n".join(out_lines), encoding="utf-8")
print(f"\nUpdated sitemap.xml index")
print(index_path.read_text(encoding="utf-8"))
