"""Fix sitemap: URL-encode Chinese characters and split into multiple sitemaps."""

import os
import re
import math
from urllib.parse import quote

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR)
REPO_DIR = "C:/Users/tonyng/AppData/Local/Temp/broadband-website"
SITE_URL = "https://broadbandhk.com"
MAX_URLS_PER_SITEMAP = 5000


def encode_url(url):
    """URL-encode non-ASCII characters in the path portion."""
    # Split URL into base and path
    prefix = "https://broadbandhk.com/"
    if url.startswith(prefix):
        path = url[len(prefix):]
        # Encode each path segment
        parts = path.split('/')
        encoded_parts = [quote(p, safe='.-_~') for p in parts]
        return prefix + '/'.join(encoded_parts)
    return url


def parse_sitemap(filepath):
    """Extract all URLs from sitemap."""
    urls = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for match in re.finditer(r'<url>\s*<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>\s*<changefreq>(.*?)</changefreq>\s*<priority>(.*?)</priority>\s*</url>', content, re.DOTALL):
        urls.append({
            'loc': match.group(1).strip(),
            'lastmod': match.group(2).strip(),
            'changefreq': match.group(3).strip(),
            'priority': match.group(4).strip(),
        })
    return urls


def write_sitemap(filepath, urls):
    """Write a single sitemap file."""
    entries = []
    for u in urls:
        encoded_loc = encode_url(u['loc'])
        entries.append(f"""  <url>
    <loc>{encoded_loc}</loc>
    <lastmod>{u['lastmod']}</lastmod>
    <changefreq>{u['changefreq']}</changefreq>
    <priority>{u['priority']}</priority>
  </url>""")

    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(entries)}
</urlset>"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def write_sitemap_index(filepath, sitemap_files):
    """Write a sitemap index file."""
    entries = []
    for sf in sitemap_files:
        entries.append(f"""  <sitemap>
    <loc>{SITE_URL}/{sf}</loc>
    <lastmod>2026-03-17</lastmod>
  </sitemap>""")

    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(entries)}
</sitemapindex>"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    sitemap_path = os.path.join(REPO_DIR, "sitemap.xml")
    print(f"Reading sitemap from {sitemap_path}...")
    urls = parse_sitemap(sitemap_path)
    print(f"Found {len(urls)} URLs")

    # Split into chunks
    num_sitemaps = math.ceil(len(urls) / MAX_URLS_PER_SITEMAP)
    print(f"Splitting into {num_sitemaps} sitemaps ({MAX_URLS_PER_SITEMAP} URLs each)")

    sitemap_files = []
    for i in range(num_sitemaps):
        start = i * MAX_URLS_PER_SITEMAP
        end = min(start + MAX_URLS_PER_SITEMAP, len(urls))
        chunk = urls[start:end]

        filename = f"sitemap-{i+1}.xml"
        filepath = os.path.join(REPO_DIR, filename)
        write_sitemap(filepath, chunk)
        sitemap_files.append(filename)
        print(f"  {filename}: {len(chunk)} URLs")

    # Write sitemap index
    index_path = os.path.join(REPO_DIR, "sitemap.xml")
    write_sitemap_index(index_path, sitemap_files)
    print(f"\nSitemap index written to {index_path}")
    print(f"Total: {len(urls)} URLs across {num_sitemaps} sitemaps")


if __name__ == "__main__":
    main()
