"""Remove fabricated prices from newly-added hotels (dir-391+).
Show 'Check Trip.com / 查Trip.com' instead of fake HK$XXX.
"""
import json, re
from pathlib import Path

dir_hotels = json.loads(Path("directory_hotels.json").read_text(encoding="utf-8"))
# Fake prices applied to slug >= dir-391
def is_fake(slug):
    try:
        return int(slug.split("-")[1]) >= 391
    except Exception:
        return False

fake_slugs = {h["slug"] for h in dir_hotels if is_fake(h["slug"])}
print(f"hotels with fake prices to fix: {len(fake_slugs)}")

# Mark fake prices in json as empty (keep orig name/slug only)
for h in dir_hotels:
    if h["slug"] in fake_slugs:
        h["price"] = "—"
        h["orig"] = "—"
Path("directory_hotels.json").write_text(json.dumps(dir_hotels,ensure_ascii=False,indent=2),encoding="utf-8")
print("directory_hotels.json updated")

# Update rows in both main pages
for path, price_label, orig_label in [
    ("pages/HKhotel.html", "查 Trip.com", "—"),
    ("pages/HKhotel-en.html", "Check Trip.com", "—"),
]:
    p = Path(path); s = p.read_text(encoding="utf-8")
    changed = 0
    for slug in fake_slugs:
        # Match <tr>...href=/.../slug.html...<td ... ff4757>PRICE</td><td ...><s>ORIG</s></td></tr>
        pattern = re.compile(
            r'(<tr[^>]*>[^<]*<td[^>]*>\s*<a href="[^"]*/' + re.escape(slug) + r'\.html"[^>]*>[^<]*</a>[^<]*</td>[^<]*)'
            r'(<td[^>]*color:#ff4757[^>]*>)([^<]+)(</td>[^<]*<td[^>]*>)[^<]*<s[^>]*>([^<]+)</s>([^<]*</td>)',
            re.DOTALL)
        def rep(m):
            return m.group(1) + m.group(2) + price_label + m.group(4) + orig_label + m.group(6)
        s, n = pattern.subn(rep, s, count=1)
        if n: changed += 1
    p.write_text(s, encoding="utf-8")
    print(f"  {path}: {changed} rows updated")
