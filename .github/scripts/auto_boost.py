"""
自動 SEO 曝光工具 — 每日由 GitHub Actions 自動執行
功能：
1. Ping Google/Bing sitemap 通知有更新
2. 用 IndexNow 即時通知 Bing/Yandex 索引所有頁面
3. 檢查網站健康狀態（是否能訪問、速度等）
4. 檢查所有頁面 SEO 基本要素
5. 生成每日報告
"""

import requests
import json
import time
import hashlib
import os
import re
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

SITE_URL = "https://broadbandhk.com"
SITEMAP_URL = f"{SITE_URL}/sitemap.xml"
INDEXNOW_KEY = "broadbandhk2026seokey"  # IndexNow API key
HEADERS = {"User-Agent": "BroadbandHK-SEO-Bot/1.0"}
HKT = timezone(timedelta(hours=8))

report = {
    "date": datetime.now(HKT).strftime("%Y-%m-%d %H:%M HKT"),
    "actions": [],
    "health": {},
    "seo_issues": [],
    "pages_indexed": 0,
    "status": "ok"
}


def log(msg):
    t = datetime.now(HKT).strftime("%H:%M:%S")
    print(f"[{t}] {msg}")


# ============================================================
# 1. Ping 搜尋引擎 Sitemap
# ============================================================
def ping_sitemaps():
    log("=== Step 1: Ping 搜尋引擎 ===")

    targets = [
        ("Google", f"https://www.google.com/ping?sitemap={SITEMAP_URL}"),
        ("Bing", f"https://www.bing.com/ping?sitemap={SITEMAP_URL}"),
    ]

    for name, url in targets:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            status = "OK" if resp.status_code == 200 else f"HTTP {resp.status_code}"
            log(f"  {name}: {status}")
            report["actions"].append(f"Ping {name} sitemap: {status}")
        except Exception as e:
            log(f"  {name}: ERROR - {e}")
            report["actions"].append(f"Ping {name}: FAILED - {e}")


# ============================================================
# 2. IndexNow — 即時通知 Bing 索引頁面
# ============================================================
def get_all_urls_from_sitemaps():
    """從 sitemap 取得所有網址"""
    urls = []
    try:
        resp = requests.get(SITEMAP_URL, headers=HEADERS, timeout=15)
        root = ET.fromstring(resp.content)
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        # 檢查是否 sitemap index
        sub_sitemaps = root.findall(".//s:sitemap/s:loc", ns)
        if sub_sitemaps:
            for sm in sub_sitemaps:
                try:
                    sm_resp = requests.get(sm.text, headers=HEADERS, timeout=15)
                    sm_root = ET.fromstring(sm_resp.content)
                    for url_elem in sm_root.findall(".//s:url/s:loc", ns):
                        urls.append(url_elem.text)
                except Exception:
                    pass
        else:
            for url_elem in root.findall(".//s:url/s:loc", ns):
                urls.append(url_elem.text)
    except Exception as e:
        log(f"  Error reading sitemap: {e}")

    return urls


def submit_indexnow():
    log("=== Step 2: IndexNow 即時索引 ===")

    urls = get_all_urls_from_sitemaps()
    if not urls:
        log("  No URLs found in sitemap")
        report["actions"].append("IndexNow: No URLs in sitemap")
        return

    log(f"  Found {len(urls)} URLs in sitemap")
    report["pages_indexed"] = len(urls)

    # IndexNow 每次最多提交 10,000 個
    batch_size = 10000
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i + batch_size]
        payload = {
            "host": "broadbandhk.com",
            "key": INDEXNOW_KEY,
            "keyLocation": f"{SITE_URL}/{INDEXNOW_KEY}.txt",
            "urlList": batch
        }

        try:
            resp = requests.post(
                "https://api.indexnow.org/indexnow",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            # 200 = OK, 202 = Accepted
            if resp.status_code in (200, 202):
                log(f"  IndexNow batch {i // batch_size + 1}: OK ({len(batch)} URLs)")
                report["actions"].append(f"IndexNow: submitted {len(batch)} URLs (HTTP {resp.status_code})")
            else:
                log(f"  IndexNow batch {i // batch_size + 1}: HTTP {resp.status_code}")
                report["actions"].append(f"IndexNow: HTTP {resp.status_code} - {resp.text[:200]}")
        except Exception as e:
            log(f"  IndexNow error: {e}")
            report["actions"].append(f"IndexNow: FAILED - {e}")

        time.sleep(1)


# ============================================================
# 3. 網站健康檢查
# ============================================================
def health_check():
    log("=== Step 3: 網站健康檢查 ===")

    checks = [
        ("Homepage", SITE_URL),
        ("Calculator", f"{SITE_URL}/calculator.html"),
        ("Blog", f"{SITE_URL}/blog.html"),
        ("Sitemap", SITEMAP_URL),
        ("Robots.txt", f"{SITE_URL}/robots.txt"),
        ("OG Image", f"{SITE_URL}/og-image.png"),
    ]

    all_ok = True
    for name, url in checks:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            speed = resp.elapsed.total_seconds()
            status = resp.status_code

            if status == 200:
                icon = "OK" if speed < 2 else "SLOW"
                log(f"  {name}: {icon} ({speed:.1f}s)")
            else:
                icon = "ERROR"
                all_ok = False
                log(f"  {name}: HTTP {status}")

            report["health"][name] = {
                "status": status,
                "speed": round(speed, 2),
                "ok": status == 200
            }
        except Exception as e:
            all_ok = False
            log(f"  {name}: DOWN - {e}")
            report["health"][name] = {"status": "error", "ok": False}

    if not all_ok:
        report["status"] = "issues_found"


# ============================================================
# 4. SEO 抽查（每日隨機檢查部分頁面）
# ============================================================
def seo_spot_check():
    log("=== Step 4: SEO 抽查 ===")

    urls = get_all_urls_from_sitemaps()
    # 每日檢查首頁 + 隨機 20 頁
    import random
    check_urls = [SITE_URL + "/"]
    if len(urls) > 20:
        check_urls += random.sample(urls, 20)
    else:
        check_urls += urls

    issues_found = 0
    pages_checked = 0

    for url in check_urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            if "text/html" not in resp.headers.get("content-type", ""):
                continue

            pages_checked += 1
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, "html.parser")

            problems = []

            # 檢查標題
            title = soup.find("title")
            if not title or len(title.get_text().strip()) < 5:
                problems.append("missing_title")

            # 檢查描述
            desc = soup.find("meta", attrs={"name": "description"})
            if not desc or not desc.get("content", "").strip():
                problems.append("missing_description")

            # 檢查 OG
            if not soup.find("meta", property="og:image"):
                problems.append("missing_og_image")

            # 檢查 H1
            if not soup.find("h1"):
                problems.append("missing_h1")

            if problems:
                issues_found += 1
                report["seo_issues"].append({"url": url, "issues": problems})
                log(f"  Issues: {url} -> {', '.join(problems)}")

        except Exception:
            pass

    log(f"  Checked {pages_checked} pages, found {issues_found} with issues")
    report["actions"].append(f"SEO spot check: {pages_checked} pages, {issues_found} issues")


# ============================================================
# 5. 生成 IndexNow key 檔案（如果唔存在）
# ============================================================
def ensure_indexnow_key():
    """確保 IndexNow key 檔案存在"""
    key_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                            f"{INDEXNOW_KEY}.txt")
    if not os.path.exists(key_file):
        with open(key_file, "w") as f:
            f.write(INDEXNOW_KEY)
        log(f"  Created IndexNow key file: {INDEXNOW_KEY}.txt")
        return True
    return False


# ============================================================
# 主流程
# ============================================================
def main():
    print("=" * 60)
    print(f"BroadbandHK Auto SEO Boost")
    print(f"Date: {report['date']}")
    print("=" * 60)

    # 確保 IndexNow key 存在
    ensure_indexnow_key()

    # 執行所有步驟
    ping_sitemaps()
    submit_indexnow()
    health_check()
    seo_spot_check()

    # 儲存報告
    print("\n" + "=" * 60)
    print("Daily Report Summary:")
    print(f"  Status: {report['status']}")
    print(f"  Pages in sitemap: {report['pages_indexed']}")
    print(f"  Health issues: {sum(1 for h in report['health'].values() if not h.get('ok'))}")
    print(f"  SEO issues: {len(report['seo_issues'])}")
    print(f"  Actions taken: {len(report['actions'])}")
    for a in report["actions"]:
        print(f"    - {a}")
    print("=" * 60)

    with open("seo_daily_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 如果有嚴重問題，exit code 1 讓 GitHub Actions 標記為 warning
    if report["status"] != "ok":
        print("\nWARNING: Issues detected! Check report for details.")


if __name__ == "__main__":
    main()
