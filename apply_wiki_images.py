"""Replace hotel page images with real Wikipedia images."""
import json, re
from pathlib import Path

images = json.loads(Path("wiki_images.json").read_text(encoding="utf-8"))

# Clear out bad matches (wrong buildings / logos / unrelated photos)
BAD = {
    "grand-hyatt-hong-kong",          # HKCEC photo, not the hotel
    "hotel-ease-access-tsuen-wan",    # Lam Tin Street unrelated
    "dorsett-tsuen-wan",              # Kwai Chung industrial unrelated
    "bridal-tea-house-hotel",         # only a logo
    "regala-skycity-hotel",           # just a shuttle bus
    "w-hong-kong",                    # Cullinan residential, not the hotel
}
for k in BAD:
    images[k] = None

changed = 0
for slug, url in images.items():
    if not url:
        continue
    path = Path(f"pages/hotels/{slug}.html")
    if not path.exists():
        continue
    content = path.read_text(encoding="utf-8")
    # Replace og:image and background-image url
    new = re.sub(
        r'(<meta property="og:image" content=")[^"]+(")',
        rf'\1{url}\2', content, count=1)
    new = re.sub(
        r"(background-image:url\(')[^']+('\))",
        rf"\1{url}\2", new, count=1)
    # Replace JSON-LD image field (single occurrence in the Hotel schema)
    new = re.sub(
        r'("image"\s*:\s*")[^"]+(")',
        rf'\1{url}\2', new, count=1)
    if new != content:
        path.write_text(new, encoding="utf-8")
        changed += 1
        print(f"updated {slug}")

print(f"\nUpdated {changed} hotel pages")
print(f"Kept Unsplash stock for: {', '.join(sorted(BAD))} + maple-leaf-hotel")
