"""
自動 SEO 曝光工具 — 每日由 GitHub Actions 自動執行
功能：
1. Ping Bing sitemap 通知有更新（Google 已於 2023 棄用 sitemap ping）
2. 用 IndexNow 即時通知 Bing/Yandex 索引新增/更新頁面（智能過濾，避免重複提交）
3. 驗證 sitemap.xml 結構完整性
4. 檢查網站健康狀態（是否能訪問、速度、Content-Type、內部連結）
5. 檢查所有頁面 SEO 基本要素
6. 生成每日報告及可執行建議
"""

import requests
import json
import time
import hashlib
import os
import re
import random
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET

SITE_URL = "https://broadbandhk.com"
SITEMAP_URL = f"{SITE_URL}/sitemap.xml"
INDEXNOW_KEY = "broadbandhk2026seokey"  # IndexNow API key
HEADERS = {"User-Agent": "BroadbandHK-SEO-Bot/1.0"}
HKT = timezone(timedelta(hours=8))

# IndexNow 提交記錄檔案路徑
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INDEXNOW_LOG_FILE = os.path.join(SCRIPT_DIR, "indexnow_submitted.json")

report = {
    "date": datetime.now(HKT).strftime("%Y-%m-%d %H:%M HKT"),
    "actions": [],
    "health": {},
    "seo_issues": [],
    "sitemap_issues": [],
    "recommendations": [],
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

    # Google 已於 2023 年棄用 sitemap ping API
    log("  Google: SKIPPED - Google deprecated sitemap ping in 2023.")
    log("          Use Google Search Console for indexing requests.")
    report["actions"].append(
        "Google sitemap ping: SKIPPED (deprecated 2023). "
        "Use Google Search Console to request indexing."
    )

    # Bing sitemap ping 仍然有效
    bing_url = f"https://www.bing.com/ping?sitemap={SITEMAP_URL}"
    try:
        resp = requests.get(bing_url, headers=HEADERS, timeout=15)
        status = "OK" if resp.status_code == 200 else f"HTTP {resp.status_code}"
        log(f"  Bing: {status}")
        report["actions"].append(f"Ping Bing sitemap: {status}")
    except Exception as e:
        log(f"  Bing: ERROR - {e}")
        report["actions"].append(f"Ping Bing: FAILED - {e}")


# ============================================================
# 2. IndexNow — 智能提交新增/更新頁面
# ============================================================
def load_indexnow_log():
    """載入之前的 IndexNow 提交記錄"""
    if os.path.exists(INDEXNOW_LOG_FILE):
        try:
            with open(INDEXNOW_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_indexnow_log(submitted):
    """儲存 IndexNow 提交記錄"""
    try:
        with open(INDEXNOW_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(submitted, f, ensure_ascii=False, indent=2)
    except IOError as e:
        log(f"  Warning: Could not save IndexNow log: {e}")


def get_all_urls_from_sitemaps():
    """從 sitemap 取得所有網址，連同 lastmod 日期"""
    urls = {}  # {url: lastmod_str or None}
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
                    for url_elem in sm_root.findall(".//s:url", ns):
                        loc = url_elem.find("s:loc", ns)
                        lastmod = url_elem.find("s:lastmod", ns)
                        if loc is not None:
                            urls[loc.text] = lastmod.text if lastmod is not None else None
                except Exception:
                    pass
        else:
            for url_elem in root.findall(".//s:url", ns):
                loc = url_elem.find("s:loc", ns)
                lastmod = url_elem.find("s:lastmod", ns)
                if loc is not None:
                    urls[loc.text] = lastmod.text if lastmod is not None else None
    except Exception as e:
        log(f"  Error reading sitemap: {e}")

    return urls


def filter_urls_for_indexnow(all_urls):
    """篩選需要提交的 URL：只提交新增或最近更新的頁面"""
    submitted_log = load_indexnow_log()
    now = datetime.now(timezone.utc)
    seven_days_ago = now - timedelta(days=7)
    to_submit = []
    homepage = SITE_URL + "/"

    for url, lastmod_str in all_urls.items():
        # 始終提交首頁
        if url.rstrip("/") == SITE_URL.rstrip("/") or url == homepage:
            to_submit.append(url)
            continue

        # 新 URL（不在提交記錄中）
        if url not in submitted_log:
            to_submit.append(url)
            continue

        # 檢查 sitemap 中的 lastmod
        if lastmod_str:
            try:
                # 支援多種 lastmod 格式
                lastmod_str_clean = lastmod_str.strip()
                if "T" in lastmod_str_clean:
                    lastmod_dt = datetime.fromisoformat(
                        lastmod_str_clean.replace("Z", "+00:00")
                    )
                else:
                    lastmod_dt = datetime.strptime(
                        lastmod_str_clean, "%Y-%m-%d"
                    ).replace(tzinfo=timezone.utc)

                # 最近 7 天修改過的頁面
                if lastmod_dt >= seven_days_ago:
                    to_submit.append(url)
                    continue
            except (ValueError, TypeError):
                pass

        # 檢查上次提交時間，若超過 30 天則重新提交
        last_submitted_str = submitted_log.get(url, {}).get("submitted_at")
        if last_submitted_str:
            try:
                last_submitted = datetime.fromisoformat(last_submitted_str)
                if (now - last_submitted).days > 30:
                    to_submit.append(url)
                    continue
            except (ValueError, TypeError):
                to_submit.append(url)
                continue

    # 去重
    to_submit = list(dict.fromkeys(to_submit))
    return to_submit, submitted_log


def submit_indexnow():
    log("=== Step 2: IndexNow 智能索引 ===")

    all_urls = get_all_urls_from_sitemaps()
    if not all_urls:
        log("  No URLs found in sitemap")
        report["actions"].append("IndexNow: No URLs in sitemap")
        return

    log(f"  Found {len(all_urls)} total URLs in sitemap")
    report["pages_indexed"] = len(all_urls)

    to_submit, submitted_log = filter_urls_for_indexnow(all_urls)

    if not to_submit:
        log("  No new or changed URLs to submit")
        report["actions"].append(
            f"IndexNow: 0 URLs submitted (all {len(all_urls)} URLs already up to date)"
        )
        return

    log(f"  Submitting {len(to_submit)} new/changed URLs (skipping {len(all_urls) - len(to_submit)} unchanged)")

    # IndexNow 小批量提交，避免伺服器負載過高
    batch_size = 100
    success = False
    for i in range(0, len(to_submit), batch_size):
        batch = to_submit[i:i + batch_size]
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
                success = True
                log(f"  IndexNow batch {i // batch_size + 1}: OK ({len(batch)} URLs)")
                report["actions"].append(
                    f"IndexNow: submitted {len(batch)} new/changed URLs (HTTP {resp.status_code})"
                )
            else:
                log(f"  IndexNow batch {i // batch_size + 1}: HTTP {resp.status_code}")
                report["actions"].append(f"IndexNow: HTTP {resp.status_code} - {resp.text[:200]}")
        except Exception as e:
            log(f"  IndexNow error: {e}")
            report["actions"].append(f"IndexNow: FAILED - {e}")

        time.sleep(1)

    # 更新提交記錄
    if success:
        now_str = datetime.now(timezone.utc).isoformat()
        for url in to_submit:
            submitted_log[url] = {
                "submitted_at": now_str,
                "lastmod": all_urls.get(url)
            }
        save_indexnow_log(submitted_log)
        log(f"  Updated IndexNow submission log ({len(submitted_log)} total URLs tracked)")


# ============================================================
# 3. Sitemap 驗證
# ============================================================
def validate_sitemap():
    log("=== Step 3: Sitemap 驗證 ===")

    issues = []

    try:
        resp = requests.get(SITEMAP_URL, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            issues.append(f"sitemap.xml returned HTTP {resp.status_code}")
            log(f"  ERROR: sitemap.xml HTTP {resp.status_code}")
            report["sitemap_issues"] = issues
            return

        root = ET.fromstring(resp.content)
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        # 檢查是否為 sitemap index
        sub_sitemaps = root.findall(".//s:sitemap/s:loc", ns)

        if sub_sitemaps:
            sub_sitemap_urls = [sm.text for sm in sub_sitemaps]
            log(f"  Sitemap index contains {len(sub_sitemap_urls)} sub-sitemaps:")
            for sm_url in sub_sitemap_urls:
                log(f"    - {sm_url}")

            # 檢查 sitemap-5.xml 是否被引用
            has_sitemap5 = any("sitemap-5.xml" in url for url in sub_sitemap_urls)
            if not has_sitemap5:
                issues.append(
                    "sitemap-5.xml is NOT referenced in sitemap.xml. "
                    "Add it to ensure all pages are discoverable."
                )
                log("  WARNING: sitemap-5.xml is NOT referenced in sitemap.xml")

            # 驗證每個子 sitemap 可以訪問
            total_urls = 0
            for sm_url in sub_sitemap_urls:
                try:
                    sm_resp = requests.get(sm_url, headers=HEADERS, timeout=15)
                    if sm_resp.status_code != 200:
                        issues.append(f"Sub-sitemap {sm_url} returned HTTP {sm_resp.status_code}")
                        log(f"  ERROR: {sm_url} -> HTTP {sm_resp.status_code}")
                    else:
                        sm_root = ET.fromstring(sm_resp.content)
                        url_count = len(sm_root.findall(".//s:url", ns))
                        total_urls += url_count
                        log(f"  OK: {sm_url} ({url_count} URLs)")
                except Exception as e:
                    issues.append(f"Sub-sitemap {sm_url} failed: {e}")
                    log(f"  ERROR: {sm_url} -> {e}")

            log(f"  Total URLs across all sub-sitemaps: {total_urls}")
        else:
            # 單一 sitemap
            url_count = len(root.findall(".//s:url", ns))
            log(f"  Single sitemap with {url_count} URLs")

            # 仍然檢查 sitemap-5.xml 是否存在
            try:
                s5_resp = requests.head(
                    f"{SITE_URL}/sitemap-5.xml", headers=HEADERS, timeout=10
                )
                if s5_resp.status_code == 200:
                    issues.append(
                        "sitemap-5.xml exists but is not referenced in sitemap.xml. "
                        "Consider using a sitemap index."
                    )
                    log("  WARNING: sitemap-5.xml exists but not referenced")
            except Exception:
                pass

    except ET.ParseError as e:
        issues.append(f"sitemap.xml XML parse error: {e}")
        log(f"  ERROR: XML parse error: {e}")
    except Exception as e:
        issues.append(f"sitemap.xml fetch error: {e}")
        log(f"  ERROR: {e}")

    if issues:
        report["sitemap_issues"] = issues
        report["status"] = "issues_found"
        for issue in issues:
            report["recommendations"].append(f"[Sitemap] {issue}")
    else:
        log("  All sitemap checks passed")
        report["sitemap_issues"] = []


# ============================================================
# 4. 網站健康檢查
# ============================================================
def health_check():
    log("=== Step 4: 網站健康檢查 ===")

    checks = [
        ("Homepage", SITE_URL, "text/html"),
        ("Calculator", f"{SITE_URL}/calculator.html", "text/html"),
        ("Blog", f"{SITE_URL}/blog.html", "text/html"),
        ("Licenses", f"{SITE_URL}/licenses.html", "text/html"),
        ("Shops", f"{SITE_URL}/shops.html", "text/html"),
        ("Sitemap", SITEMAP_URL, "xml"),
        ("Robots.txt", f"{SITE_URL}/robots.txt", "text/plain"),
        ("OG Image", f"{SITE_URL}/og-image.png", "image/"),
    ]

    all_ok = True
    for name, url, expected_type in checks:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            speed = resp.elapsed.total_seconds()
            status = resp.status_code
            content_type = resp.headers.get("content-type", "")

            type_ok = expected_type in content_type
            if status == 200 and type_ok:
                icon = "OK" if speed < 2 else "SLOW"
                log(f"  {name}: {icon} ({speed:.1f}s) [Content-Type: {content_type}]")
            elif status == 200 and not type_ok:
                icon = "TYPE_MISMATCH"
                log(f"  {name}: Content-Type mismatch! Expected '{expected_type}', got '{content_type}'")
                report["recommendations"].append(
                    f"[Health] {name} ({url}): Content-Type is '{content_type}', "
                    f"expected '{expected_type}'"
                )
            else:
                icon = "ERROR"
                all_ok = False
                log(f"  {name}: HTTP {status}")
                report["recommendations"].append(
                    f"[Health] {name} ({url}): returned HTTP {status}"
                )

            report["health"][name] = {
                "url": url,
                "status": status,
                "speed": round(speed, 2),
                "content_type": content_type,
                "type_ok": type_ok,
                "ok": status == 200
            }

            if speed >= 2 and status == 200:
                report["recommendations"].append(
                    f"[Performance] {name} ({url}): slow response ({speed:.1f}s). "
                    f"Consider caching or optimization."
                )

        except Exception as e:
            all_ok = False
            log(f"  {name}: DOWN - {e}")
            report["health"][name] = {"url": url, "status": "error", "ok": False}
            report["recommendations"].append(
                f"[Health] {name} ({url}): unreachable - {e}"
            )

    # 內部連結檢查：隨機抽查 5 個頁面
    log("  --- Checking internal links (sample 5 pages) ---")
    check_internal_links()

    if not all_ok:
        report["status"] = "issues_found"


def check_internal_links():
    """隨機抽查 5 個頁面的內部連結"""
    from bs4 import BeautifulSoup

    all_urls = get_all_urls_from_sitemaps()
    html_urls = [u for u in all_urls if u.endswith(".html") or u.endswith("/")]

    if not html_urls:
        log("  No HTML pages to check for internal links")
        return

    sample_size = min(5, len(html_urls))
    sample = random.sample(html_urls, sample_size)
    broken_links = []

    for page_url in sample:
        try:
            resp = requests.get(page_url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            if "text/html" not in resp.headers.get("content-type", ""):
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            links = soup.find_all("a", href=True)

            for link in links:
                href = link["href"]
                # 只檢查內部連結
                if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
                    continue
                if href.startswith("http") and SITE_URL not in href:
                    continue

                # 組合完整 URL
                full_url = urljoin(page_url, href).split("#")[0]
                if SITE_URL not in full_url:
                    continue

                try:
                    link_resp = requests.head(full_url, headers=HEADERS, timeout=10,
                                              allow_redirects=True)
                    if link_resp.status_code >= 400:
                        broken_links.append({
                            "source": page_url,
                            "broken_link": full_url,
                            "status": link_resp.status_code
                        })
                except Exception:
                    broken_links.append({
                        "source": page_url,
                        "broken_link": full_url,
                        "status": "timeout"
                    })

        except Exception:
            pass

    if broken_links:
        log(f"  Found {len(broken_links)} broken internal link(s):")
        for bl in broken_links:
            log(f"    {bl['source']} -> {bl['broken_link']} (HTTP {bl['status']})")
            report["recommendations"].append(
                f"[Broken Link] {bl['source']} links to {bl['broken_link']} "
                f"(HTTP {bl['status']})"
            )
        report["status"] = "issues_found"
    else:
        log(f"  No broken internal links found (checked {sample_size} pages)")


# ============================================================
# 5. SEO 抽查（每日隨機檢查部分頁面）
# ============================================================
def seo_spot_check():
    log("=== Step 5: SEO 抽查 ===")

    all_urls = get_all_urls_from_sitemaps()
    urls = list(all_urls.keys())
    # 每日檢查首頁 + 隨機 20 頁
    check_urls = [SITE_URL + "/"]
    if len(urls) > 20:
        check_urls += random.sample(urls, 20)
    else:
        check_urls += urls

    issues_found = 0
    pages_checked = 0

    from bs4 import BeautifulSoup

    for url in check_urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            if "text/html" not in resp.headers.get("content-type", ""):
                continue

            pages_checked += 1
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

            # 檢查 canonical
            canonical = soup.find("link", rel="canonical")
            if not canonical or not canonical.get("href", "").strip():
                problems.append("missing_canonical")

            if problems:
                issues_found += 1
                report["seo_issues"].append({"url": url, "issues": problems})
                log(f"  Issues: {url} -> {', '.join(problems)}")

                # 為每個問題生成具體建議
                for p in problems:
                    report["recommendations"].append(
                        f"[SEO] {url}: {p.replace('_', ' ')}"
                    )

        except Exception:
            pass

    log(f"  Checked {pages_checked} pages, found {issues_found} with issues")
    report["actions"].append(f"SEO spot check: {pages_checked} pages, {issues_found} issues")


# ============================================================
# 6. 生成 IndexNow key 檔案（如果唔存在）
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
# 7. 生成 SEO 問題摘要及建議
# ============================================================
def generate_summary():
    log("=== Summary: SEO Issues & Recommendations ===")

    if not report["recommendations"]:
        log("  No issues found. Everything looks good!")
        report["recommendations"].append("No issues found. All checks passed.")
        return

    # 分類建議
    categories = {}
    for rec in report["recommendations"]:
        # 提取 [Category] 前綴
        match = re.match(r"\[(\w[\w\s]*)\]", rec)
        cat = match.group(1) if match else "Other"
        categories.setdefault(cat, []).append(rec)

    for cat, items in categories.items():
        log(f"  [{cat}] ({len(items)} issue(s)):")
        for item in items:
            log(f"    - {item}")


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
    validate_sitemap()
    health_check()
    seo_spot_check()
    generate_summary()

    # 儲存報告
    print("\n" + "=" * 60)
    print("Daily Report Summary:")
    print(f"  Status: {report['status']}")
    print(f"  Pages in sitemap: {report['pages_indexed']}")
    print(f"  Sitemap issues: {len(report.get('sitemap_issues', []))}")
    print(f"  Health issues: {sum(1 for h in report['health'].values() if not h.get('ok'))}")
    print(f"  SEO issues: {len(report['seo_issues'])}")
    print(f"  Actions taken: {len(report['actions'])}")
    for a in report["actions"]:
        print(f"    - {a}")
    if report["recommendations"]:
        print(f"\n  Recommendations ({len(report['recommendations'])}):")
        for r in report["recommendations"]:
            print(f"    * {r}")
    print("=" * 60)

    with open("seo_daily_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 如果有嚴重問題，exit code 1 讓 GitHub Actions 標記為 warning
    if report["status"] != "ok":
        print("\nWARNING: Issues detected! Check report for details.")


if __name__ == "__main__":
    main()
