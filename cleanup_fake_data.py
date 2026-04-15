"""
全自動清理假數據腳本
處理 /pages/ 下所有 HTML：
1. 刪除表格行「1000M 實測速度 XXX Mbps」
2. 刪除 hero-stats 假「實測速度」方塊
3. 清理 FAQ 文字中「實測 XXX Mbps」→ 中性語句
4. 清理 JSON-LD FAQPage 相同虛假內容
5. 加統一免責聲明段落（如未存在）
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "pages"

DISCLAIMER_HTML = '<p style="margin-top:14px;color:#778;font-size:.85em;padding:10px 14px;background:#f5f7fa;border-radius:6px">ℹ️ 本頁部分資料來自公開資源，實際寬頻覆蓋、速度及月費以各 ISP 最新公佈為準。如有錯漏請 WhatsApp 5228 7541 通知我哋更正。</p>'

# Pattern 1: 刪除表格行「實測速度」
ROW_PATTERN = re.compile(r'<tr>\s*<td>[^<]*實測速度[^<]*</td>\s*<td>[^<]+</td>\s*</tr>', re.IGNORECASE)

# Pattern 2: 刪除 hero-stats 實測速度方塊
HERO_PATTERN = re.compile(r'<div>\s*<span class="num">[^<]+</span>\s*<span class="lbl">[^<]*實測[^<]*</span>\s*</div>', re.IGNORECASE)

# Pattern 3: FAQ visible「實測 XXX Mbps」句子清洗
# 例：「根據用戶實測，XX 的 1000M 光纖計劃平均下載速度約 XXX Mbps (1000M計劃實測範圍)。實際速度會受路由器、線材、使用人數影響。」
FAQ_SENTENCE_PATTERN = re.compile(
    r'根據用戶實測[^<]*?實際速度會受[^。]*。',
    re.IGNORECASE
)
FAQ_REPLACEMENT = '1000M 光纖計劃理論下載速度可達 1 Gbps。實際速度受路由器規格、網線、Wi-Fi 訊號及使用裝置數量影響，建議使用 Wi-Fi 6 路由器以獲得最佳效能。'

# Pattern 4: JSON-LD FAQ 內同樣文字
JSONLD_FAQ_PATTERN = re.compile(
    r'"text":\s*"根據用戶實測[^"]*?實際速度會受[^"]*?"',
    re.IGNORECASE
)
JSONLD_REPLACEMENT = '"text": "1000M 光纖計劃理論下載速度可達 1 Gbps。實際速度受路由器規格、網線、Wi-Fi 訊號及使用裝置數量影響。"'

# Pattern 5: hero-stats「XXX 實測速度」label 簡單變數
HERO_IMPL_PATTERN = re.compile(r'<span class="lbl">實測速度</span>', re.IGNORECASE)

total = modified = 0
stats = {"row": 0, "hero": 0, "faq_visible": 0, "faq_jsonld": 0, "disclaimer_added": 0}

for f in ROOT.rglob("*.html"):
    total += 1
    try:
        html = f.read_text(encoding="utf-8")
    except Exception:
        continue
    original = html

    # 1. 刪實測速度 table 行
    new_html, n = ROW_PATTERN.subn("", html)
    stats["row"] += n
    html = new_html

    # 2. 刪 hero-stats 實測方塊
    new_html, n = HERO_PATTERN.subn("", html)
    stats["hero"] += n
    html = new_html

    # 3. 清 FAQ 文字
    new_html, n = FAQ_SENTENCE_PATTERN.subn(FAQ_REPLACEMENT, html)
    stats["faq_visible"] += n
    html = new_html

    # 4. 清 JSON-LD FAQ
    new_html, n = JSONLD_FAQ_PATTERN.subn(JSONLD_REPLACEMENT, html)
    stats["faq_jsonld"] += n
    html = new_html

    # 5. 加免責聲明（喺 footer 前，如未存在）
    if "本頁部分資料來自公開資源" not in html and "<footer" in html:
        html = html.replace("<footer", DISCLAIMER_HTML + "\n<footer", 1)
        stats["disclaimer_added"] += 1

    if html != original:
        f.write_text(html, encoding="utf-8")
        modified += 1

print(f"掃描 {total} 檔案，修改 {modified} 個")
print(f"  - 刪除實測速度表格行: {stats['row']}")
print(f"  - 刪除 hero-stats 實測方塊: {stats['hero']}")
print(f"  - 清洗 FAQ 虛假實測句子: {stats['faq_visible']}")
print(f"  - 清洗 JSON-LD FAQ: {stats['faq_jsonld']}")
print(f"  - 加免責聲明: {stats['disclaimer_added']}")
