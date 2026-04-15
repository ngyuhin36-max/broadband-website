"""
清理 sitemap-ai.xml：只保留 ai-products-index.html
其他 ai-*-{區域/類別} 頁係 noindex doorway pattern
sitemap-travel.xml 7 個 URL 全部係重要聯盟頁，唔使改
"""
import re
from pathlib import Path

f = Path(__file__).parent / "sitemap-ai.xml"
content = f.read_text(encoding="utf-8")

URL_BLOCK = re.compile(r'<url>.*?</url>', re.DOTALL)
KEEP = ["ai-products-index.html"]

def replace(m):
    block = m.group(0)
    for k in KEEP:
        if k in block:
            return block
    return ""

new = URL_BLOCK.sub(replace, content)
new = re.sub(r'\n\s*\n+', '\n', new)
f.write_text(new, encoding="utf-8")

kept = len(URL_BLOCK.findall(new))
print(f"sitemap-ai.xml: 剩 {kept} URL")
