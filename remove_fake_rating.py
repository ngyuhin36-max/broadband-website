"""
移除所有大廈頁嘅 fake aggregateRating
Google 會因為虛假評分 schema 手動處罰
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "pages"

# 匹配 "aggregateRating": {....}, 嘅 JSON 片段（包括前面逗號）
PATTERN = re.compile(r',\s*"aggregateRating":\s*\{[^}]+\}')

changed = 0
total = 0
for f in ROOT.rglob("*.html"):
    total += 1
    html = f.read_text(encoding="utf-8")
    new = PATTERN.sub("", html)
    if new != html:
        f.write_text(new, encoding="utf-8")
        changed += 1

print(f"掃描 {total} 個檔案，移除 fake rating 於 {changed} 個檔案")
