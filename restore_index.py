"""
恢復重要頁面為 index,follow（之前被誤傷）
只有 Trip.com 聯盟頁 + AI 產品總覽
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "pages"

RESTORE_FILES = [
    "HKhotel.html", "HKhotel-en.html",
    "flights.html", "flights-en.html",
    "carhire.html", "carhire-en.html",
    "trains.html",
    "ai-products-index.html",
]

PATTERN = re.compile(r'<meta\s+name="robots"\s+content="noindex,\s*follow"\s*/?>', re.IGNORECASE)
REPLACEMENT = '<meta name="robots" content="index, follow">'

for name in RESTORE_FILES:
    f = ROOT / name
    if not f.exists():
        print(f"[SKIP] {name} 不存在")
        continue
    html = f.read_text(encoding="utf-8")
    new = PATTERN.sub(REPLACEMENT, html, count=1)
    if new != html:
        f.write_text(new, encoding="utf-8")
        print(f"[OK] {name} 恢復 index")
    else:
        print(f"[?] {name} 冇 noindex tag")
