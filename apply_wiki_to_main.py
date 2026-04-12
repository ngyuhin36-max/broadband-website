"""Update HKhotel.html featured card images with real Wikipedia photos."""
import json, re
from pathlib import Path

images = json.loads(Path("wiki_images.json").read_text(encoding="utf-8"))
BAD = {"grand-hyatt-hong-kong","hotel-ease-access-tsuen-wan","dorsett-tsuen-wan",
       "bridal-tea-house-hotel","regala-skycity-hotel","w-hong-kong"}
for k in BAD: images[k] = None

hotels = json.loads(Path("hotels_data.json").read_text(encoding="utf-8"))
name_to_new = {}
for h in hotels:
    new_img = images.get(h["slug"])
    if new_img:
        name_to_new[h["name"]] = (h["img"], new_img)

path = Path("pages/HKhotel.html")
s = path.read_text(encoding="utf-8")
changed = 0
for name,(old,new) in name_to_new.items():
    # Find card by hotel-name, then replace its background-image
    pattern = re.compile(
        r'(<div class="hotel-card">.*?background-image:url\(\')'
        + re.escape(old) + r"('\).*?" + re.escape(name) + r")",
        re.DOTALL)
    s2, n = pattern.subn(rf"\1{new}\2", s, count=1)
    if n:
        s = s2; changed += 1

path.write_text(s, encoding="utf-8")
print(f"Updated {changed} main-list cards in HKhotel.html")
