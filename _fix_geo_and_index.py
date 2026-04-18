import os
import re
from pathlib import Path

PAGES_DIR = Path(__file__).parent / "pages"

GEO_TAGS = '''<meta name="geo.region" content="HK">
<meta name="geo.placename" content="Hong Kong">
<meta name="geo.position" content="22.3193;114.1694">
<meta name="ICBM" content="22.3193, 114.1694">
'''

RICH_MARKERS = ("屋苑資料", "落成年份")

stats = {
    "total": 0,
    "geo_added": 0,
    "geo_existed": 0,
    "noindex_removed": 0,
    "noindex_kept": 0,
    "rich_pages": [],
}

def process_file(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[SKIP] {path.name}: {e}")
        return

    original = text
    is_rich = any(marker in text for marker in RICH_MARKERS)

    if 'name="geo.region"' not in text:
        anchor = '<meta name="viewport"'
        idx = text.find(anchor)
        if idx != -1:
            line_end = text.find(">", idx) + 1
            text = text[:line_end] + "\n" + GEO_TAGS.rstrip() + text[line_end:]
            stats["geo_added"] += 1
        else:
            head_idx = text.find("<head>")
            if head_idx != -1:
                insert_pos = head_idx + len("<head>")
                text = text[:insert_pos] + "\n" + GEO_TAGS.rstrip() + text[insert_pos:]
                stats["geo_added"] += 1
    else:
        stats["geo_existed"] += 1

    if is_rich:
        new_text, n = re.subn(
            r'<meta\s+name="robots"\s+content="noindex,\s*follow"\s*/?>',
            '<meta name="robots" content="index, follow">',
            text,
        )
        if n > 0:
            text = new_text
            stats["noindex_removed"] += 1
        stats["rich_pages"].append(path.name)
    else:
        if 'noindex' in text:
            stats["noindex_kept"] += 1

    if text != original:
        path.write_text(text, encoding="utf-8")

    stats["total"] += 1

def main():
    files = sorted(PAGES_DIR.glob("*.html"))
    print(f"Processing {len(files)} files...")
    for i, f in enumerate(files, 1):
        process_file(f)
        if i % 2000 == 0:
            print(f"  {i}/{len(files)}")

    print("\n=== Summary ===")
    print(f"Total files:          {stats['total']}")
    print(f"GEO tags added:       {stats['geo_added']}")
    print(f"GEO tags existed:     {stats['geo_existed']}")
    print(f"Noindex removed:      {stats['noindex_removed']}")
    print(f"Noindex kept (thin):  {stats['noindex_kept']}")
    print(f"Rich pages found:     {len(stats['rich_pages'])}")

    rich_list = Path(__file__).parent / "_rich_pages.txt"
    rich_list.write_text("\n".join(stats["rich_pages"]), encoding="utf-8")
    print(f"\nRich pages list saved to: {rich_list.name}")

if __name__ == "__main__":
    main()
