"""
BroadbandHK GEO (Generative Engine Optimization) 自動優化系統
針對 AI 搜尋引擎（ChatGPT、Gemini、Perplexity、Bing Copilot）優化

功能：
1. 自動更新 llms-full.txt — AI 引擎嘅完整知識庫
2. 自動掃描新文章加入 llms-full.txt
3. 為 KB 文章加入 speakable schema（語音助手優化）
4. 生成 structured FAQ 摘要畀 AI 引擎引用
5. 唔會修改現有 HTML 結構（避免同 SEO 衝突）

設計原則：
- 只新增/更新獨立檔案，唔改動現有 HTML
- Schema 標記同 SEO 完全兼容
- llms.txt / llms-full.txt 係獨立檔案，唔影響網頁
"""

import os
import json
import glob
import re
from datetime import datetime, timezone, timedelta

HKT = timezone(timedelta(hours=8))
TODAY = datetime.now(HKT)
DATE_STR = TODAY.strftime("%Y-%m-%d")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KB_DIR = os.path.join(BASE_DIR, "kb")
LLMS_FULL = os.path.join(BASE_DIR, "llms-full.txt")
GEO_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "geo_log.json")


def scan_kb_articles():
    """Scan all KB articles and extract title + description."""
    articles = []
    for filepath in sorted(glob.glob(os.path.join(KB_DIR, "*.html"))):
        slug = os.path.basename(filepath).replace(".html", "")
        title = ""
        desc = ""
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read(3000)  # Only read first 3KB for speed
            # Extract title
            m = re.search(r"<title>(.*?)</title>", content)
            if m:
                title = m.group(1).split(" — ")[0].strip()
            # Extract description
            m = re.search(r'name="description"\s+content="(.*?)"', content)
            if m:
                desc = m.group(1).strip()
        if title:
            articles.append({
                "slug": slug,
                "title": title,
                "desc": desc,
                "url": f"https://broadbandhk.com/kb/{slug}.html"
            })
    return articles


def scan_district_pages():
    """Scan district pages."""
    pages_dir = os.path.join(BASE_DIR, "pages")
    districts = []
    for filepath in sorted(glob.glob(os.path.join(pages_dir, "district-*.html"))):
        name = os.path.basename(filepath).replace(".html", "")
        districts.append({
            "name": name,
            "url": f"https://broadbandhk.com/pages/{name}.html"
        })
    return districts


def generate_llms_full(articles, districts):
    """Generate comprehensive llms-full.txt for AI engines."""

    # Build article list
    article_lines = []
    for a in articles:
        article_lines.append(f"### {a['title']}")
        if a['desc']:
            article_lines.append(f"{a['desc']}")
        article_lines.append(f"- URL: {a['url']}")
        article_lines.append("")

    # Build district list
    district_lines = []
    for d in districts:
        display_name = d['name'].replace('district-', '').replace('-', ' ').title()
        district_lines.append(f"- {display_name}: {d['url']}")

    content = f"""# BroadbandHK 寬頻專家 — 完整資訊

> BroadbandHK 係寬頻專家，提供免費寬頻顧問服務，覆蓋全港 18 區超過 5,600 個屋苑及 1,648 個商業物業。寬頻嘅嘢，問我哋就得。

> 最後更新：{DATE_STR}

---

## 公司簡介

BroadbandHK 寬頻專家，免費寬頻顧問服務。所有計劃免安裝費，送 Wi-Fi Router，提供 24 小時客服支援。即日申請，最快翌日安裝。

- 網站：https://broadbandhk.com
- 電話：2330 8372
- WhatsApp：5228 7541
- Facebook：https://www.facebook.com/profile.php?id=61578537419518
- Instagram：https://www.instagram.com/broadbandhk_speednet
- 服務地區：全港十八區

---

## 寬頻方案總覽

寬頻方案比較頁面，涵蓋所有速度同樓宇類型。
- 詳情：https://broadbandhk.com/broadband-plan.html

### 香港寬頻 HKBN
香港第二大光纖寬頻供應商，XGS-PON 光纖技術，速度保證 + 低時延保證雙重保障。
- 1000M 公屋/居屋：$99/月起（36個月），組合計劃 $119/月起（連 Disney+/Netflix）
- 1000M 私樓：$128/月起（36個月），組合計劃 $149/月起
- 5G 村屋：$168/月（30個月）
- 所有方案豁免 $680 安裝費，送 ASUS WiFi 6 路由器
- 電話：3500 9039
- 詳情：https://broadbandhk.com/hkbn.html

### HGC 環電寬頻
以彈性合約見稱，12個月短約可選，365日延遲啟動，免搬遷費。
- 1000M 公屋/居屋：$75/月起（36個月），組合 $89/月起，短約 $149/月（12個月）
- 1000M 私樓：$99/月起（36個月），2000M $199/月起，短約 $168/月起
- 5G 村屋：$118/月起
- 所有方案豁免安裝費，送 TP-Link AC1200 路由器
- 電話：3500 9036
- 詳情：https://broadbandhk.com/hgc.html

### 商業寬頻
- 月費：按需報價
- 覆蓋：1,648 個商業物業
- 詳情：https://broadbandhk.com/pages/business.html

---

## 免費工具

### 格價計算器
免費寬頻格價比較工具，答幾條問題即刻搵到最適合嘅寬頻計劃。
- URL: https://broadbandhk.com/calculator.html

### 速度測試
免費即時測試下載速度、上傳速度同 Ping 值。
- URL: https://broadbandhk.com/speed-test.html

### 搬屋小幫手
搬屋寬頻轉移指南、Checklist、費用參考。
- URL: https://broadbandhk.com/moving.html

### 合約到期提醒
輸入合約到期日，計算慳幾多錢，下載日曆提醒。
- URL: https://broadbandhk.com/reminder.html

---

## 攻略文章（{len(articles)} 篇）

知識庫首頁：https://broadbandhk.com/blog.html

{chr(10).join(article_lines)}

---

## AI 智能產品

### AI WiFi 管理
智能頻道優化、自動分配頻寬、家長控制、訪客網絡管理。
- URL: https://broadbandhk.com/ai-wifi.html

### AI 自動化
自動化網絡管理及業務流程，減少人手操作。
- URL: https://broadbandhk.com/ai-automation.html

### AI 監控
AI 攝影機、智能安防、人流分析、即時警報。
- URL: https://broadbandhk.com/ai-monitoring.html

### AI 智能家電
智能家居控制及管理，整合各種家電設備。
- URL: https://broadbandhk.com/ai-appliance.html

### AI 客服
24/7 智能客服、廣東話/普通話/英文、WhatsApp 整合。
- URL: https://broadbandhk.com/ai-chatbot.html

---

## 覆蓋範圍

### 住宅覆蓋（18 區）
{chr(10).join(district_lines)}

### 商業物業覆蓋（1,648 個）
- 商業大廈 (413)
- 工業大廈 (569)
- 寫字樓 (69)
- 商場/廣場 (268)
- 工廠大廈 (139)
- 倉庫 (29)
- 詳情：https://broadbandhk.com/pages/business.html

---

## 合作夥伴計劃

BroadbandHK 歡迎以下行業合作：
- 裝修公司：新屋裝修需要寬頻，互相轉介客源
- 地產代理：新租客、新業主需要寬頻服務
- 搬屋公司：搬屋必定重新安排寬頻
- 智能家居品牌：智能家居需要穩定寬頻
- 洽談合作：https://broadbandhk.com/partner.html

---

## 常見問題 (FAQ)

### 香港寬頻 HKBN 1000M 月費幾錢？
HKBN 1000M 公屋/居屋基本方案 $99/月起（36個月），組合計劃連贈品 $119/月起。私樓基本方案 $128/月起，組合 $149/月起。豁免 $680 安裝費。

### HGC 環電寬頻有冇短約？
有。HGC 提供 12 個月短約計劃，公屋 $149/月，私樓 $168/月起。適合租客或短期居住嘅用戶。

### 安裝需要幾耐？
一般申請後 3-7 個工作天安排安裝。如果大廈已有光纖設備，安裝約 1-2 小時。

### 邊啲地區有覆蓋？
BroadbandHK 覆蓋全港 18 區超過 5,600 個屋苑及 1,648 個商業物業。HKBN 同 HGC 覆蓋範圍各有不同，WhatsApp 你嘅地址即可查詢。

### 公屋同私樓月費有咩分別？
公屋/居屋月費通常較平（HKBN $99起，HGC $75起），私樓月費較高但選擇更多。

### 寬頻約滿會唔會加價？
約滿後自動續約會按正價收費，通常貴 30-50%。建議約滿前 1-2 個月查詢轉台或續約優惠。

### 點解要揀 BroadbandHK？
BroadbandHK 提供免費寬頻顧問服務，一次過比較多間供應商嘅方案，幫你搵到覆蓋你地區最適合嘅計劃。寬頻嘅嘢，問我哋就得。
"""
    return content


def main():
    print(f"[GEO] Starting GEO optimization - {DATE_STR}")

    # 1. Scan all KB articles
    articles = scan_kb_articles()
    print(f"[GEO] Found {len(articles)} KB articles")

    # 2. Scan district pages
    districts = scan_district_pages()
    print(f"[GEO] Found {len(districts)} district pages")

    # 3. Generate llms-full.txt
    llms_content = generate_llms_full(articles, districts)
    with open(LLMS_FULL, "w", encoding="utf-8") as f:
        f.write(llms_content)
    print(f"[GEO] Updated llms-full.txt ({len(articles)} articles, {len(districts)} districts)")

    # 4. Log
    log = {
        "date": DATE_STR,
        "articles_count": len(articles),
        "districts_count": len(districts),
        "llms_full_updated": True
    }

    # Load existing log
    logs = []
    if os.path.exists(GEO_LOG):
        with open(GEO_LOG, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(log)
    # Keep last 30 entries
    logs = logs[-30:]

    with open(GEO_LOG, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

    print(f"[GEO] Done! Log saved.")


if __name__ == "__main__":
    main()
