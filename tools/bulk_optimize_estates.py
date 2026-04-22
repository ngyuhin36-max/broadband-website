# -*- coding: utf-8 -*-
"""
Bulk SEO+GEO optimization for all remaining estate pages (~19,000).
Extracts building name + type from existing pages, regenerates with:
  - Full schema suite (LocalBusiness + BreadcrumbList + FAQPage)
  - geo meta tags (HK region)
  - Consistent pricing $98/158/228
  - Building-name-injected unique FAQ
  - Internal nav links
Skips the Top 10 already hand-optimized.
"""
import os, re, json, html, sys, glob

ROOT = os.path.join(os.path.dirname(__file__), "..")
PAGES_DIR = os.path.abspath(os.path.join(ROOT, "pages"))

# Top 10 already done — do NOT overwrite
SKIP = {
    "taikoo-shing","city-one-shatin","mei-foo-sun-chuen","whampoa-garden",
    "laguna-city","telford-gardens","heng-fa-chuen","south-horizons",
    "kornhill","discovery-park"
}

RE_TITLE = re.compile(r"<title>([^<]+)</title>")
RE_H1    = re.compile(r"<h1>([^<]+)</h1>")
RE_TYPE  = re.compile(r"樓宇類型</h3>\s*<p>([^<]+)</p>")

def esc(s): return html.escape(s, quote=True)

def extract(path):
    with open(path, "r", encoding="utf-8") as f:
        t = f.read()
    h1 = RE_H1.search(t)
    if not h1: return None
    h1_txt = h1.group(1).strip()
    m = re.match(r"^(.+?)\s+([A-Za-z0-9][A-Za-z0-9\s\-\.&']*?)\s*寬頻上網\s*$", h1_txt)
    if m:
        zh, en = m.group(1).strip(), m.group(2).strip()
    else:
        m2 = re.match(r"^(.+?)\s*寬頻上網\s*$", h1_txt)
        if not m2: return None
        zh, en = m2.group(1).strip(), ""
    btype_m = RE_TYPE.search(t)
    btype = btype_m.group(1).strip() if btype_m else "住宅樓宇"
    return {"zh": zh, "en": en, "type": btype}

def full_name(d):
    return f"{d['zh']} {d['en']}".strip()

def wa_link(msg):
    return f"https://api.whatsapp.com/send?phone=85252287541&text={esc(msg)}"

def schemas(slug, d):
    url = f"https://broadbandhk.com/pages/{slug}.html"
    fn = full_name(d)
    faqs = [
        (f"{fn}有邊幾間寬頻供應商覆蓋？",
         f"{fn}一般有 HKBN 香港寬頻、CMHK 中國移動香港、HGC 環球全域電訊、3HK 等 2-5 間 ISP 覆蓋。實際可選供應商視乎你嘅單位座數，建議 WhatsApp 5228 7541 免費查詢。"),
        (f"{fn}最平寬頻月費係幾多？",
         f"{fn} 最平寬頻月費為 HK$98/月（100M 光纖），500M $158，1000M $228。所有計劃免安裝費、免 Router 費、無隱藏收費。"),
        (f"{fn}裝寬頻要等幾耐？",
         f"一般 {fn} 如已有光纖覆蓋，1-3 個工作天可完成上門安裝。WhatsApp 預約裝機時段最快即日安排。"),
        (f"我住 {fn}，寬頻就嚟約滿應該點做？",
         f"建議合約到期前 2-3 個月開始格價。可使用 BroadbandHK 免費到期提醒工具（broadbandhk.com/reminder.html）計算可慳金額，或 WhatsApp 我哋獲取 {fn} 最新優惠報價。"),
    ]
    schemaList = [
        {"@context":"https://schema.org","@type":"LocalBusiness",
         "name":f"BroadbandHK - {fn}寬頻服務","description":f"{fn} 寬頻月費比較及安裝服務，光纖入屋月費 $98 起。",
         "url":url,"telephone":"+852-5228-7541",
         "areaServed":{"@type":"Place","name":fn},
         "priceRange":"HK$98 - HK$228",
         "aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","ratingCount":"89","bestRating":"5"}},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"主頁","item":"https://broadbandhk.com/"},
            {"@type":"ListItem","position":2,"name":"屋苑寬頻","item":"https://broadbandhk.com/pages/"},
            {"@type":"ListItem","position":3,"name":fn,"item":url}]},
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]},
    ]
    html_out = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemaList)
    return html_out, faqs

PLAN_ROWS = [
    ("100M","$98","輕度上網、睇片、瀏覽"),
    ("500M","$158","一般家庭、4K、WFH、網課"),
    ("1000M","$228","多人家庭、遊戲、雲端備份"),
]

def render(slug, d):
    fn = full_name(d)
    url = f"https://broadbandhk.com/pages/{slug}.html"
    title = f"{fn} 寬頻月費比較｜光纖入屋 $98 起 - BroadbandHK"
    desc = f"【2026最新】{fn} 寬頻方案比較：支援 HKBN、CMHK、HGC、3HK 等 ISP，100M $98 / 500M $158 / 1000M $228，免安裝費，1-3 個工作天上門安裝。WhatsApp 5228 7541 免費格價。"
    schemas_html, faqs = schemas(slug, d)
    keywords = f"{d['zh']}寬頻,{d['en']} broadband,{d['zh']}光纖,{d['zh']}上網,HKBN {d['zh']},CMHK {d['zh']},{d['zh']}1000M" if d['en'] else f"{d['zh']}寬頻,{d['zh']}光纖,{d['zh']}上網,HKBN {d['zh']},CMHK {d['zh']}"

    plans_html = ""
    for i,(speed,price,target) in enumerate(PLAN_ROWS):
        popular = " popular" if i==1 else ""
        plans_html += f"""
<div class="plan-card{popular}">
<div class="plan-name">{speed} 光纖入屋</div>
<div class="plan-price">{price}<span>/月</span></div>
<p class="plan-target">{esc(target)}</p>
<ul class="plan-features"><li>{speed}bps 下載</li><li>免 Router 費</li><li>免安裝費</li><li>24 個月合約</li></ul>
<a href="{wa_link(f'你好，我住{fn}，想查詢 {speed} 寬頻Plan')}" class="cta-btn">WhatsApp 查詢</a>
</div>"""

    faq_html = "".join(f'<div class="faq-item"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>' for q,a in faqs)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(keywords)}">
<meta name="robots" content="index, follow">
<meta name="geo.region" content="HK">
<meta name="geo.placename" content="{esc(fn)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:locale" content="zh_HK">
<meta property="og:site_name" content="BroadbandHK">
<meta property="og:image" content="https://broadbandhk.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-23EZE5P385"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-23EZE5P385');gtag('config','AW-959473638');</script>
{schemas_html}
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang HK","Microsoft JhengHei",sans-serif;color:#1a1a1a;line-height:1.7;background:#f5f7fa}}
.header{{background:#0a1628;color:#fff;padding:14px 20px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:100;box-shadow:0 2px 10px rgba(0,0,0,.15)}}
.header a.logo{{color:#fff;text-decoration:none;font-size:1.2em;font-weight:700}}
.header a.logo span{{color:#ff6b35}}
.header nav a{{color:#fff;text-decoration:none;margin-left:16px;font-size:.95em}}
.header nav a:hover{{color:#ff6b35}}
.breadcrumb{{background:#eef2f7;padding:10px 20px;font-size:.9em;color:#556}}
.breadcrumb a{{color:#0a5fbf;text-decoration:none}}
.hero{{background:linear-gradient(135deg,#0a1628 0%,#1a3a6e 100%);color:#fff;padding:44px 20px;text-align:center}}
.hero h1{{font-size:1.8em;margin-bottom:10px}}
.hero .sub{{font-size:1em;opacity:.92}}
.hero-stats{{display:flex;justify-content:center;gap:26px;flex-wrap:wrap;margin-top:20px}}
.hero-stats div{{text-align:center}}
.hero-stats .num{{font-size:1.5em;font-weight:800;color:#ff6b35;display:block}}
.hero-stats .lbl{{font-size:.82em;opacity:.85}}
.container{{max-width:1000px;margin:0 auto;padding:26px 20px}}
.card{{background:#fff;border-radius:12px;padding:24px;margin-bottom:18px;box-shadow:0 2px 10px rgba(0,0,0,.05)}}
.card h2{{color:#0a1628;margin-bottom:12px;font-size:1.3em;border-left:4px solid #ff6b35;padding-left:12px}}
.plans-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:14px}}
.plan-card{{border:2px solid #e5e9f0;border-radius:12px;padding:22px;text-align:center;background:#fff;transition:all .2s}}
.plan-card:hover{{border-color:#ff6b35;transform:translateY(-3px)}}
.plan-card.popular{{border-color:#ff6b35;position:relative}}
.plan-card.popular::before{{content:"最受歡迎";position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:#ff6b35;color:#fff;padding:3px 12px;border-radius:14px;font-size:.75em;font-weight:700}}
.plan-name{{font-size:1.15em;font-weight:700;color:#0a1628}}
.plan-price{{font-size:2.2em;font-weight:800;color:#ff6b35;margin:8px 0}}
.plan-price span{{font-size:.38em;color:#666;font-weight:500}}
.plan-target{{color:#667;font-size:.86em;margin-bottom:10px}}
.plan-features{{list-style:none;text-align:left;margin:10px 0}}
.plan-features li{{padding:3px 0;font-size:.9em}}
.plan-features li::before{{content:"✓";color:#28a745;font-weight:700;margin-right:6px}}
.cta-btn{{display:inline-block;background:#25D366;color:#fff;padding:10px 22px;border-radius:22px;text-decoration:none;font-weight:700;font-size:.92em}}
.cta-btn:hover{{transform:scale(1.04)}}
.faq-item{{border-bottom:1px solid #eef1f5;padding:13px 0}}
.faq-item:last-child{{border:none}}
.faq-item h3{{color:#0a1628;font-size:1.02em;margin-bottom:6px}}
.faq-item p{{color:#556;font-size:.94em}}
.info-table{{width:100%;border-collapse:collapse}}
.info-table td{{padding:9px 12px;border-bottom:1px solid #eef1f5;font-size:.94em}}
.info-table td:first-child{{font-weight:600;color:#556;width:40%}}
.final-cta{{background:linear-gradient(135deg,#ff6b35 0%,#e8551f 100%);color:#fff;border-radius:14px;padding:28px;text-align:center;margin:20px 0}}
.final-cta h2{{color:#fff;border:none;padding:0;margin-bottom:8px}}
.final-cta .cta-btn{{background:#fff;color:#ff6b35;margin-top:12px;padding:12px 28px;font-size:1em}}
.float-wa{{position:fixed;bottom:20px;right:20px;background:#25D366;width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(37,211,102,.5);z-index:99}}
.float-wa svg{{width:28px;height:28px;fill:#fff}}
.footer{{background:#0a1628;color:#a0aec0;padding:22px 20px;text-align:center;font-size:.86em;margin-top:36px}}
.footer a{{color:#ff6b35;text-decoration:none}}
@media(max-width:768px){{.hero h1{{font-size:1.4em}}.header nav{{display:none}}}}
</style>
</head>
<body>

<header class="header">
<a class="logo" href="/"><span>⚡</span> BroadbandHK</a>
<nav><a href="/">主頁</a><a href="/calculator.html">格價</a><a href="/reminder.html">到期提醒</a><a href="/blog.html">知識庫</a></nav>
</header>

<div class="breadcrumb">
<a href="/">主頁</a> › <a href="/pages/">屋苑寬頻</a> › <strong>{esc(fn)}</strong>
</div>

<section class="hero">
<h1>{esc(fn)} 寬頻月費比較</h1>
<p class="sub">{esc(d['type'])} · 支援 HKBN、CMHK、HGC、3HK 等多間 ISP</p>
<div class="hero-stats">
<div><span class="num">$98</span><span class="lbl">月費起</span></div>
<div><span class="num">1000M</span><span class="lbl">最高速度</span></div>
<div><span class="num">1-3天</span><span class="lbl">上門安裝</span></div>
<div><span class="num">24/7</span><span class="lbl">WhatsApp</span></div>
</div>
</section>

<div class="container">

<div class="card">
<h2>🏢 {esc(fn)} 基本資料</h2>
<table class="info-table">
<tr><td>屋苑名稱</td><td>{esc(fn)}</td></tr>
<tr><td>樓宇類型</td><td>{esc(d['type'])}</td></tr>
<tr><td>寬頻基建</td><td>光纖入屋 FTTH</td></tr>
<tr><td>支援最高速度</td><td>1000Mbps</td></tr>
<tr><td>ISP 覆蓋</td><td>HKBN、CMHK、HGC、3HK 等</td></tr>
<tr><td>裝機時間</td><td>1-3 個工作天</td></tr>
</table>
</div>

<div class="card">
<h2>💰 {esc(fn)} 寬頻月費計劃</h2>
<p>為 {esc(fn)} 住戶提供 3 個光纖計劃：</p>
<div class="plans-grid">{plans_html}</div>
<p style="text-align:center;margin-top:14px;color:#667;font-size:.86em">免安裝費 · 免 Router 費 · 24 個月合約 · 無隱藏收費</p>
</div>

<div class="card">
<h2>❓ {esc(fn)} 寬頻常見問題</h2>
{faq_html}
</div>

<div class="card">
<h2>🛠️ 免費工具</h2>
<p>
<a href="/reminder.html" style="color:#0a5fbf;margin-right:14px">📅 寬頻到期提醒</a>
<a href="/calculator.html" style="color:#0a5fbf;margin-right:14px">🧮 寬頻格價計算</a>
<a href="/pages/" style="color:#0a5fbf">🏢 全港 5,600+ 屋苑</a>
</p>
</div>

<div class="final-cta">
<h2>📞 即刻查 {esc(fn)} 寬頻優惠</h2>
<p>WhatsApp 5 分鐘回覆 · 免費格價 · 無壓力推銷</p>
<a href="{wa_link(f'你好，我住{fn}，想查詢寬頻優惠')}" class="cta-btn">💬 WhatsApp 5228 7541</a>
</div>

</div>

<a class="float-wa" href="https://api.whatsapp.com/send?phone=85252287541" target="_blank" aria-label="WhatsApp">
<svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
</a>

<footer class="footer">
<p>&copy; 2026 BroadbandHK 香港光纖寬頻格價比較 | <a href="https://broadbandhk.com/">broadbandhk.com</a></p>
<p style="margin-top:6px">WhatsApp: <a href="https://api.whatsapp.com/send?phone=85252287541">5228 7541</a> · 免費寬頻格價比較服務</p>
</footer>

</body></html>"""

def main():
    files = glob.glob(os.path.join(PAGES_DIR, "*.html"))
    total = len(files)
    done = skipped = failed = 0
    for i, path in enumerate(files):
        slug = os.path.splitext(os.path.basename(path))[0]
        if slug in SKIP or slug in ("index",):
            skipped += 1
            continue
        d = extract(path)
        if not d:
            failed += 1
            continue
        try:
            out = render(slug, d)
            with open(path, "w", encoding="utf-8") as f:
                f.write(out)
            done += 1
        except Exception as ex:
            failed += 1
            if failed < 5: print(f"FAIL {slug}: {ex}")
        if (i+1) % 2000 == 0:
            print(f"  progress {i+1}/{total}")
    print(f"\nDone={done} Skipped={skipped} Failed={failed} Total={total}")

if __name__ == "__main__":
    main()
