"""
BroadbandHK 內部連結自動優化系統
為地區頁面加入 KB 文章連結 + 交叉地區連結
為 KB 文章加入相關文章連結 + 地區頁面連結

設計原則：
- 只喺現有頁面嘅指定位置插入連結區塊
- 唔會破壞現有 HTML 結構
- 用固定標記識別已插入嘅區塊，避免重複
- 同 SEO/GEO 完全兼容
"""

import os
import re
import glob
import json
from datetime import datetime, timezone, timedelta

HKT = timezone(timedelta(hours=8))
TODAY = datetime.now(HKT).strftime("%Y-%m-%d")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES_DIR = os.path.join(BASE_DIR, "pages")
KB_DIR = os.path.join(BASE_DIR, "kb")
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "internal_links_log.json")

# District name mapping
DISTRICTS = {
    "district-kwun-tong": "觀塘區",
    "district-sha-tin": "沙田區",
    "district-sai-kung": "西貢區",
    "district-yuen-long": "元朗區",
    "district-tsuen-wan": "荃灣區",
    "district-tuen-mun": "屯門區",
    "district-tai-po": "大埔區",
    "district-wong-tai-sin": "黃大仙區",
    "district-sham-shui-po": "深水埗區",
    "district-north": "北區",
    "district-wan-chai": "灣仔區",
    "district-central-and-western": "中西區",
    "district-eastern": "東區",
    "district-southern": "南區",
    "district-kowloon-city": "九龍城區",
    "district-yau-tsim-mong": "油尖旺區",
    "district-kwai-tsing": "葵青區",
    "district-islands": "離島區",
}

# KB articles that are relevant to ALL districts
UNIVERSAL_KB_LINKS = [
    ("搬屋寬頻全攻略", "moving-checklist-2026"),
    ("WiFi 設定指南", "home-wifi-setup-guide"),
    ("寬頻續約議價攻略", "broadband-renewal-negotiation"),
    ("WFH 上網攻略", "wfh-internet-tips"),
    ("家長控制設定教學", "parental-control-setup"),
    ("Router 選購指南", "router-guide"),
    ("寬頻速度解析", "broadband-speed-explained"),
    ("WiFi 死角解決方案", "wifi-dead-zones-fix"),
]

# 供應商專頁連結（加入到 KB 文章同地區頁面）
PROVIDER_LINKS = [
    ("寬頻方案總覽", "broadband-plan.html"),
    ("香港寬頻 HKBN 報價", "hkbn.html"),
    ("HGC 環電寬頻報價", "hgc.html"),
    ("AI WiFi 方案", "ai-wifi.html"),
]

# 新 GEO 目錄
GEO_DIRS = {
    "hkbn": "香港寬頻 HKBN",
    "hgc": "HGC 環電",
    "broadband-plan": "寬頻方案",
    "ai-wifi": "AI WiFi",
}

INTERNAL_LINK_MARKER = "<!-- BHK-INTERNAL-LINKS -->"
INTERNAL_LINK_END = "<!-- /BHK-INTERNAL-LINKS -->"


def build_district_link_block(current_district):
    """Build HTML block with KB links + other district links for a district page."""

    # KB article links
    kb_links = ""
    for title, slug in UNIVERSAL_KB_LINKS:
        kb_links += f'            <a href="https://broadbandhk.com/kb/{slug}.html" style="display:block;padding:10px 16px;background:#f0f9ff;border-radius:8px;color:#2563eb;text-decoration:none;font-weight:600;margin-bottom:8px;transition:background 0.2s;" onmouseover="this.style.background=\'#dbeafe\'" onmouseout="this.style.background=\'#f0f9ff\'">{title} →</a>\n'

    # Other district links (exclude current)
    other_districts = ""
    count = 0
    for slug, name in DISTRICTS.items():
        if slug == current_district:
            continue
        if count >= 8:  # Max 8 other districts
            break
        other_districts += f'            <a href="https://broadbandhk.com/pages/{slug}.html" style="display:inline-block;padding:6px 14px;background:#f1f5f9;border-radius:20px;color:#334155;text-decoration:none;font-size:0.85rem;margin:4px;" onmouseover="this.style.background=\'#e2e8f0\'" onmouseout="this.style.background=\'#f1f5f9\'">{name}</a>\n'
        count += 1

    block = f"""
{INTERNAL_LINK_MARKER}
    <div style="margin:40px 0;padding:30px;background:#fff;border-radius:16px;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <h3 style="font-size:1.3rem;font-weight:800;margin-bottom:16px;color:#1e293b;">寬頻攻略文章</h3>
        <p style="color:#64748b;font-size:0.9rem;margin-bottom:16px;">BroadbandHK 寬頻專家幫你解決所有上網問題：</p>
        <div style="display:grid;gap:8px;">
{kb_links}        </div>
        <div style="text-align:center;margin-top:16px;">
            <a href="https://broadbandhk.com/blog.html" style="color:#2563eb;font-weight:700;text-decoration:none;">瀏覽全部 33+ 篇攻略 →</a>
        </div>
    </div>
    <div style="margin:20px 0 40px;padding:24px;background:#f8fafc;border-radius:12px;">
        <h3 style="font-size:1.1rem;font-weight:700;margin-bottom:12px;color:#475569;">其他地區寬頻覆蓋</h3>
        <div style="display:flex;flex-wrap:wrap;gap:4px;">
{other_districts}        </div>
    </div>
{INTERNAL_LINK_END}
"""
    return block


def update_district_page(filepath, district_slug):
    """Add internal links to a district page."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove existing internal links block if present
    pattern = re.compile(
        re.escape(INTERNAL_LINK_MARKER) + r".*?" + re.escape(INTERNAL_LINK_END),
        re.DOTALL
    )
    content = pattern.sub("", content)

    # Insert before the CTA section
    link_block = build_district_link_block(district_slug)

    # Try to insert before CTA section
    cta_marker = '<div class="cta-section">'
    if cta_marker in content:
        content = content.replace(cta_marker, link_block + "\n        " + cta_marker)
    else:
        # Fallback: insert before footer
        content = content.replace('<div class="footer">', link_block + '\n<div class="footer">')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True


def scan_kb_articles():
    """Get list of all KB articles for cross-linking."""
    articles = []
    for filepath in sorted(glob.glob(os.path.join(KB_DIR, "*.html"))):
        slug = os.path.basename(filepath).replace(".html", "")
        title = ""
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read(2000)
            m = re.search(r"<title>(.*?)</title>", content)
            if m:
                title = m.group(1).split(" — ")[0].strip()
        if title:
            articles.append({"slug": slug, "title": title})
    return articles


def build_kb_crosslinks(current_slug, all_articles):
    """Build related articles block for KB pages."""
    related = []
    for a in all_articles:
        if a["slug"] != current_slug and len(related) < 5:
            related.append(a)

    if not related:
        return ""

    links = ""
    for a in related:
        links += f'                <a href="{a["slug"]}.html">{a["title"]}</a>\n'

    # Provider page links
    provider_links = ""
    for title, filename in PROVIDER_LINKS:
        provider_links += f'                <a href="../{filename}" style="color:#2563eb;font-weight:700">{title}</a>\n'

    # Also add district links
    district_links = ""
    for slug, name in list(DISTRICTS.items())[:6]:
        district_links += f'                <a href="../pages/{slug}.html" style="color:#059669;">{name}寬頻覆蓋</a>\n'

    block = f"""
{INTERNAL_LINK_MARKER}
            <div class="related-articles" style="margin-top:48px;padding:32px;background:#f8fafc;border-radius:12px;">
                <h3 style="font-size:1.2rem;margin-bottom:16px;">相關攻略文章</h3>
{links}{provider_links}            </div>
            <div style="margin-top:24px;padding:24px;background:#ecfdf5;border-radius:12px;">
                <h3 style="font-size:1.1rem;margin-bottom:12px;color:#065f46;">各區寬頻覆蓋</h3>
{district_links}            </div>
{INTERNAL_LINK_END}
"""
    return block


def update_kb_article(filepath, current_slug, all_articles):
    """Add cross-links to KB article."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove existing block
    pattern = re.compile(
        re.escape(INTERNAL_LINK_MARKER) + r".*?" + re.escape(INTERNAL_LINK_END),
        re.DOTALL
    )
    content = pattern.sub("", content)

    # Build new cross-links
    link_block = build_kb_crosslinks(current_slug, all_articles)
    if not link_block:
        return False

    # Insert before back-link or before closing article div
    if '<a href="../blog.html" class="back-link">' in content:
        content = content.replace(
            '<a href="../blog.html" class="back-link">',
            link_block + '\n            <a href="../blog.html" class="back-link">'
        )
    elif '</section>' in content:
        # Find last </section> before footer
        last_section = content.rfind('</section>')
        if last_section > 0:
            content = content[:last_section] + link_block + "\n" + content[last_section:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True


def main():
    print(f"[LINKS] Starting internal links optimization - {TODAY}")

    district_count = 0
    kb_count = 0

    # 1. Update district pages
    for slug, name in DISTRICTS.items():
        filepath = os.path.join(PAGES_DIR, f"{slug}.html")
        if os.path.exists(filepath):
            update_district_page(filepath, slug)
            district_count += 1
            print(f"  OK {slug}")
        else:
            print(f"  SKIP {slug} - file not found")

    # 2. Update KB articles
    all_articles = scan_kb_articles()
    print(f"\n[LINKS] Found {len(all_articles)} KB articles")

    for filepath in sorted(glob.glob(os.path.join(KB_DIR, "*.html"))):
        slug = os.path.basename(filepath).replace(".html", "")
        if update_kb_article(filepath, slug, all_articles):
            kb_count += 1

    # 3. Update new GEO directory pages (hkbn/, hgc/, broadband-plan/, ai-wifi/)
    geo_count = 0
    for geo_dir, label in GEO_DIRS.items():
        geo_path = os.path.join(BASE_DIR, geo_dir)
        if not os.path.isdir(geo_path):
            continue
        for filepath in sorted(glob.glob(os.path.join(geo_path, "*.html"))):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Skip if already has provider links
                if "broadband-plan.html" in content and "hkbn.html" in content and "hgc.html" in content:
                    continue

                # Add cross-links to footer area
                footer_marker = '<footer class="footer">'
                if footer_marker not in content:
                    continue

                cross_block = '\n<!-- Auto cross-links -->\n<div style="max-width:1100px;margin:0 auto 20px;padding:0 20px;text-align:center">\n'
                for title, filename in PROVIDER_LINKS:
                    cross_block += f'  <a href="../{filename}" style="display:inline-block;padding:6px 14px;margin:4px;background:#f1f5f9;border-radius:8px;font-size:13px;color:#2563eb;font-weight:600">{title}</a>\n'
                cross_block += '</div>\n'

                content = content.replace(footer_marker, cross_block + footer_marker)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                geo_count += 1
            except Exception:
                pass

    print(f"\n[LINKS] Updated {district_count} district pages + {kb_count} KB articles + {geo_count} GEO pages")

    # 4. Log
    log = {
        "date": TODAY,
        "district_pages_updated": district_count,
        "kb_articles_updated": kb_count,
        "geo_pages_updated": geo_count,
        "total_kb_articles": len(all_articles)
    }

    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(log)
    logs = logs[-30:]

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

    print(f"[LINKS] Done!")


if __name__ == "__main__":
    main()
