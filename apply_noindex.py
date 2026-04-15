"""
為長尾頁加 noindex,follow
保留 index: 首頁、broadband-plan系列、tools、kb、核心主題頁
Noindex: /pages/ (19113 大廈頁), ai-wifi/, ai-automation/, hkbn/, hgc/ (區域重複)
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent

# Noindex 目標目錄
NOINDEX_DIRS = ["pages", "ai-wifi", "ai-automation", "hkbn", "hgc"]

PATTERN = re.compile(r'<meta\s+name="robots"\s+content="[^"]*"\s*/?>', re.IGNORECASE)
REPLACEMENT = '<meta name="robots" content="noindex, follow">'

def process(path: Path) -> bool:
    try:
        html = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[SKIP] {path}: {e}")
        return False

    if PATTERN.search(html):
        new = PATTERN.sub(REPLACEMENT, html, count=1)
    else:
        # 冇 meta robots → 喺 <head> 後插入
        new = re.sub(r'(<head[^>]*>)', r'\1\n    ' + REPLACEMENT, html, count=1, flags=re.IGNORECASE)

    if new != html:
        path.write_text(new, encoding="utf-8")
        return True
    return False

total = changed = 0
for d in NOINDEX_DIRS:
    folder = ROOT / d
    if not folder.exists():
        print(f"[SKIP] {folder} 不存在")
        continue
    files = list(folder.rglob("*.html"))
    for f in files:
        total += 1
        if process(f):
            changed += 1
    print(f"[{d}] 處理 {len(files)} 個檔案")

print(f"\n總共 {total} 檔案，修改 {changed} 個")
