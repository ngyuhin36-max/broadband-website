"""
清理 sitemap：移除已 noindex 嘅 URL
保留：首頁、broadband-plan/*、tools/*、kb/*、頂層主題頁
移除：/pages/*, /ai-wifi/*, /ai-automation/*, /hkbn/*, /hgc/*
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SITEMAPS = ["sitemap-1.xml", "sitemap-2.xml", "sitemap-3.xml", "sitemap-4.xml", "sitemap-5.xml"]

# 要移除嘅 path prefix
EXCLUDE_PREFIXES = ["/pages/", "/ai-wifi/", "/ai-automation/", "/hkbn/", "/hgc/"]

URL_BLOCK = re.compile(r'<url>\s*<loc>([^<]+)</loc>.*?</url>', re.DOTALL)

def should_exclude(url: str) -> bool:
    for p in EXCLUDE_PREFIXES:
        if p in url:
            return True
    return False

total_removed = 0
for name in SITEMAPS:
    f = ROOT / name
    if not f.exists():
        print(f"[SKIP] {name} 不存在")
        continue
    content = f.read_text(encoding="utf-8")
    original_count = len(URL_BLOCK.findall(content))

    def replace(m):
        url = m.group(1)
        if should_exclude(url):
            return ""
        return m.group(0)

    new = URL_BLOCK.sub(replace, content)
    # 清理空行
    new = re.sub(r'\n\s*\n+', '\n', new)
    kept = len(URL_BLOCK.findall(new))
    removed = original_count - kept
    total_removed += removed
    f.write_text(new, encoding="utf-8")
    print(f"[{name}] 原 {original_count} → 剩 {kept} (移除 {removed})")

print(f"\n總共移除 {total_removed} 個 noindex URL")
