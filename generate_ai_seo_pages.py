"""
BroadbandHK AI 產品 SEO 頁面生成器
自動生成 AI 產品 x 行業 x 地區 的長尾 SEO 頁面
"""

import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(os.path.dirname(BASE_DIR), "broadband-website", "pages")
SITE_URL = "https://broadbandhk.com"

# 5 個 AI 產品
AI_PRODUCTS = [
    {
        "id": "ai-wifi",
        "name": "AI WiFi 管理",
        "page": "ai-wifi.html",
        "icon": "📶",
        "color": "#2563eb",
        "gradient": "linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%)",
        "features": [
            "WiFi 6 極速上網，速度快 WiFi 5 近 3 倍",
            "AI 自動優化頻道及頻寬分配",
            "WPA3 + Trend Micro 企業級安全防護",
            "Mesh WiFi 全屋覆蓋無死角",
            "myWiFi App 隨時管理網絡",
            "進階家長控制功能",
        ],
        "keywords": "AI WiFi管理, 智能WiFi, WiFi 6, Mesh WiFi, WiFi優化",
    },
    {
        "id": "ai-automation",
        "name": "AI 流程自動化",
        "page": "ai-automation.html",
        "icon": "⚙️",
        "color": "#10b981",
        "gradient": "linear-gradient(135deg, #064e3b 0%, #10b981 100%)",
        "features": [
            "Lark AI 一站式協作平台",
            "AI 會議助手：自動轉錄及摘要",
            "AI 實時翻譯消除語言障礙",
            "SHOP-IN-A-BOX 零售自動化方案",
            "設備性能監控及自動化配置",
            "社交媒體輿情追蹤及分析",
        ],
        "keywords": "AI流程自動化, Lark AI, SHOP-IN-A-BOX, 零售自動化, AI協作",
    },
    {
        "id": "ai-monitoring",
        "name": "AI 網絡監控",
        "page": "ai-monitoring.html",
        "icon": "📡",
        "color": "#0891b2",
        "gradient": "linear-gradient(135deg, #0c4a6e 0%, #0891b2 100%)",
        "features": [
            "真．安全連線：內置 AI 防火牆",
            "支援 2.5Gbps 企業級防護",
            "24x7 Security Operation Centre 全天候監控",
            "PROTECT 全方位網絡安全方案",
            "即時異常警報及事件回應",
            "月費僅數百元，中小企都負擔得起",
        ],
        "keywords": "AI網絡監控, AI防火牆, 網絡安全, SOC, 真安全連線",
    },
    {
        "id": "ai-appliance",
        "name": "AI 一體機",
        "page": "ai-appliance.html",
        "icon": "🖥️",
        "color": "#7c3aed",
        "gradient": "linear-gradient(135deg, #4c1d95 0%, #7c3aed 100%)",
        "features": [
            "AI-IN-A-BOX 企業級生成式 AI 平台",
            "On-Premises 私有部署，數據不外洩",
            "支援手寫文件 OCR 辨識",
            "智能客服及營銷分析",
            "實時風險監控（合規）",
            "先租後買，支援概念驗證 (PoC)",
        ],
        "keywords": "AI一體機, AI-IN-A-BOX, 企業AI, 私有AI部署, 生成式AI",
    },
    {
        "id": "ai-chatbot",
        "name": "AI Chatbot",
        "page": "ai-chatbot.html",
        "icon": "💬",
        "color": "#f59e0b",
        "gradient": "linear-gradient(135deg, #92400e 0%, #f59e0b 100%)",
        "features": [
            "自動化 IVR 語音應答系統",
            "AI 虛擬助手 24/7 全天候服務",
            "進階語音處理技術",
            "智能分流至專人跟進",
            "多渠道整合（電話、網站、社交媒體）",
            "Lark AI 社交媒體輿情追蹤",
        ],
        "keywords": "AI Chatbot, AI智能客服, IVR, AI虛擬助手, 客服自動化",
    },
]

# 行業分類
INDUSTRIES = [
    {
        "id": "restaurant",
        "name": "餐飲業",
        "name_en": "restaurant",
        "icon": "🍽️",
        "pain_points": "餐廳 WiFi 唔穩定影響食客體驗、POS 系統故障影響營業、人手不足難以處理客戶查詢",
        "use_cases": {
            "ai-wifi": "為食客提供穩定高速 WiFi，AI 自動管理頻寬分配，確保 POS 系統同食客上網互不影響。",
            "ai-automation": "SHOP-IN-A-BOX 一站式管理 POS、WiFi、CCTV。Lark AI 協助員工排班、庫存管理、供應商溝通。",
            "ai-monitoring": "24/7 監控餐廳網絡，確保 POS 系統同外賣平台連接穩定，防止黑客竊取客戶付款資料。",
            "ai-appliance": "在餐廳內部部署 AI，分析銷售數據、預測食材需求、優化菜單定價，數據從不外洩。",
            "ai-chatbot": "AI 自動處理訂位查詢、外賣訂單確認、營業時間查詢，減輕前台工作負擔。",
        },
    },
    {
        "id": "retail",
        "name": "零售業",
        "name_en": "retail",
        "icon": "🛍️",
        "pain_points": "店舖 WiFi 覆蓋不足、POS 系統管理複雜、缺乏 IT 人手、網絡安全風險高",
        "use_cases": {
            "ai-wifi": "Managed WiFi+ 為店舖提供企業級 WiFi，AI 自動優化覆蓋範圍，支援大量客戶同時連接。",
            "ai-automation": "SHOP-IN-A-BOX 包辦 WiFi、POS、CCTV、網絡安全。Lark AI 統一管理多間分店營運。",
            "ai-monitoring": "PROTECT 方案保護客戶付款數據，SOC 24/7 監控防止數據洩漏，符合 PCI DSS 要求。",
            "ai-appliance": "店內部署 AI 分析客流量、購買行為、庫存水平，即時調整營銷策略。",
            "ai-chatbot": "AI 客服自動回覆產品查詢、庫存查詢、退換貨流程，支援 WhatsApp 及網站。",
        },
    },
    {
        "id": "office",
        "name": "辦公室",
        "name_en": "office",
        "icon": "🏢",
        "pain_points": "多人同時上網導致 WiFi 慢、視像會議卡頓、IT 管理成本高、網絡安全威脅",
        "use_cases": {
            "ai-wifi": "Managed WiFi+ 配合 RUCKUS AP，AI 自動優化頻寬分配，確保 Zoom/Teams 視像會議暢順。",
            "ai-automation": "Lark AI 取代多個溝通工具，一個平台搞掂即時通訊、文件協作、項目管理、會議紀錄。",
            "ai-monitoring": "真．安全連線 AI 防火牆保護公司機密文件，SOC 24/7 監控防止釣魚攻擊及數據洩漏。",
            "ai-appliance": "On-Premises AI 部署，員工可安全使用 AI 處理公司文件，數據從不離開公司網絡。",
            "ai-chatbot": "AI 虛擬助手自動處理內部 IT 支援查詢、HR 常見問題、訪客登記等重複性工作。",
        },
    },
    {
        "id": "clinic",
        "name": "診所/醫療",
        "name_en": "clinic",
        "icon": "🏥",
        "pain_points": "病人資料安全要求高、WiFi 需穩定支援醫療設備、合規要求嚴格",
        "use_cases": {
            "ai-wifi": "WPA3 企業級加密保護病人資料傳輸，Mesh WiFi 確保診所每個角落都有穩定訊號。",
            "ai-automation": "Lark AI 協助醫護人員排班、病歷管理、跨部門溝通，提升診所營運效率。",
            "ai-monitoring": "醫療數據高度敏感，AI 防火牆 + SOC 24/7 監控確保病人資料安全，符合私隱條例。",
            "ai-appliance": "On-Premises AI 處理病歷 OCR 辨識、智能分診、報告生成，所有數據留在診所內部。",
            "ai-chatbot": "AI 自動處理預約查詢、覆診提醒、診所營業時間查詢，減輕接待處工作量。",
        },
    },
    {
        "id": "education",
        "name": "教育機構",
        "name_en": "education",
        "icon": "🎓",
        "pain_points": "大量學生同時上網、家長查詢多、行政工作繁重、學生上網安全",
        "use_cases": {
            "ai-wifi": "AI WiFi 管理支援大量裝置同時連接，家長控制功能過濾不當內容，保護學生上網安全。",
            "ai-automation": "Lark AI 統一管理教師溝通、課程安排、家長通知。AI 會議助手自動記錄教職員會議內容。",
            "ai-monitoring": "保護學校網絡免受攻擊，監控學生上網行為，防止存取不當網站。",
            "ai-appliance": "校內部署 AI 協助批改作業、生成教學材料、分析學生表現數據，數據安全保存。",
            "ai-chatbot": "AI 自動回覆家長查詢（學費、校曆、活動）、處理入學申請初步篩選。",
        },
    },
    {
        "id": "logistics",
        "name": "物流/倉庫",
        "name_en": "logistics",
        "icon": "📦",
        "pain_points": "倉庫面積大 WiFi 覆蓋難、設備多需穩定連接、庫存管理複雜",
        "use_cases": {
            "ai-wifi": "Managed WiFi+ 配合 RUCKUS AP 覆蓋大面積倉庫，AI 優化訊號確保掃描器及平板穩定連接。",
            "ai-automation": "Lark AI 統一管理車隊調度、倉庫庫存、客戶訂單追蹤，自動化工作流程減少人手錯誤。",
            "ai-monitoring": "24/7 監控倉庫網絡，確保 WMS 系統穩定運行，防止黑客入侵物流系統。",
            "ai-appliance": "部署 AI 優化倉庫路線規劃、預測庫存需求、自動化揀貨排程，提升物流效率。",
            "ai-chatbot": "AI 自動回覆客戶送貨查詢、追蹤包裹狀態、處理退貨申請。",
        },
    },
    {
        "id": "beauty",
        "name": "美容/髮型",
        "name_en": "beauty-salon",
        "icon": "💇",
        "pain_points": "客戶預約管理混亂、WiFi 唔穩定影響客戶體驗、缺乏數碼化管理",
        "use_cases": {
            "ai-wifi": "為客戶提供高速穩定 WiFi，myWiFi App 輕鬆設定訪客網絡，提升客戶等候體驗。",
            "ai-automation": "SHOP-IN-A-BOX 管理 POS、WiFi、CCTV。Lark AI 統一管理預約、員工排班、客戶紀錄。",
            "ai-monitoring": "保護客戶個人資料及付款信息安全，AI 防火牆防止數據外洩。",
            "ai-appliance": "分析客戶消費模式、熱門服務時段、產品銷售數據，AI 幫你做出更精準嘅營銷決策。",
            "ai-chatbot": "AI 24/7 自動處理預約查詢、確認及取消，減少 no-show，提升預約管理效率。",
        },
    },
    {
        "id": "hotel",
        "name": "酒店/旅館",
        "name_en": "hotel",
        "icon": "🏨",
        "pain_points": "住客 WiFi 體驗直接影響評價、大範圍 WiFi 覆蓋挑戰、多語言客服需求",
        "use_cases": {
            "ai-wifi": "Managed WiFi+ 全酒店覆蓋，AI 智能分配頻寬確保每間房都有高速 WiFi，提升住客滿意度。",
            "ai-automation": "Lark AI 統一管理前台、房務、維修團隊溝通。AI 實時翻譯支援多國語言住客服務。",
            "ai-monitoring": "保護住客個人資料及付款信息，24/7 SOC 監控防止網絡攻擊。",
            "ai-appliance": "分析入住率、房價、住客偏好，AI 自動調整定價策略，最大化收入。",
            "ai-chatbot": "AI 多語言客服自動處理訂房查詢、入住指引、設施查詢、退房流程。",
        },
    },
]

# 18 區
DISTRICTS = [
    {"id": "central-western", "name": "中西區"},
    {"id": "eastern", "name": "東區"},
    {"id": "southern", "name": "南區"},
    {"id": "wan-chai", "name": "灣仔區"},
    {"id": "kowloon-city", "name": "九龍城區"},
    {"id": "kwun-tong", "name": "觀塘區"},
    {"id": "sham-shui-po", "name": "深水埗區"},
    {"id": "wong-tai-sin", "name": "黃大仙區"},
    {"id": "yau-tsim-mong", "name": "油尖旺區"},
    {"id": "islands", "name": "離島區"},
    {"id": "kwai-tsing", "name": "葵青區"},
    {"id": "north", "name": "北區"},
    {"id": "sai-kung", "name": "西貢區"},
    {"id": "sha-tin", "name": "沙田區"},
    {"id": "tai-po", "name": "大埔區"},
    {"id": "tsuen-wan", "name": "荃灣區"},
    {"id": "tuen-mun", "name": "屯門區"},
    {"id": "yuen-long", "name": "元朗區"},
]


def generate_product_industry_page(product, industry):
    """生成 AI產品 x 行業 頁面"""
    slug = f"{product['id']}-{industry['id']}"
    title = f"{industry['name']}{product['name']}方案 | BroadbandHK"
    desc = f"BroadbandHK 為{industry['name']}提供{product['name']}方案。{industry['pain_points'][:60]}... 立即 WhatsApp 免費諮詢。"
    use_case = industry["use_cases"].get(product["id"], "")
    features_html = "\n".join(
        f'                        <li>{f}</li>' for f in product["features"]
    )
    wa_text = f"你好，我係{industry['name']}，想了解{product['name']}方案"

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{product['keywords']}, {industry['name']}, 香港{industry['name']}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{SITE_URL}/pages/{slug}.html">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="product">
    <meta property="og:url" content="{SITE_URL}/pages/{slug}.html">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📶</text></svg>">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-23EZE5P385"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-23EZE5P385');</script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "{industry['name']}{product['name']}方案",
        "description": "{desc}",
        "brand": {{"@type": "Brand", "name": "BroadbandHK"}},
        "url": "{SITE_URL}/pages/{slug}.html",
        "category": "{product['name']}"
    }}
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:'Noto Sans TC',sans-serif; color:#0f172a; line-height:1.7; }}
        .header {{ background:{product['gradient']}; color:#fff; padding:20px; text-align:center; }}
        .header a {{ color:#fff; text-decoration:none; font-size:1.4em; font-weight:700; }}
        .nav {{ background:#f8fafc; padding:12px 20px; border-bottom:1px solid #e2e8f0; font-size:0.9rem; }}
        .nav a {{ color:{product['color']}; text-decoration:none; }}
        .nav a:hover {{ text-decoration:underline; }}
        .hero {{ background:{product['gradient']}; color:#fff; padding:60px 20px; text-align:center; }}
        .hero h1 {{ font-size:2em; margin-bottom:12px; }}
        .hero p {{ font-size:1.1rem; opacity:0.9; max-width:700px; margin:0 auto; }}
        .container {{ max-width:1000px; margin:0 auto; padding:40px 20px; }}
        .section-title {{ font-size:1.5em; margin-bottom:20px; color:#0f172a; }}
        .pain-box {{ background:#fef2f2; border-left:4px solid #ef4444; border-radius:8px; padding:20px; margin:30px 0; }}
        .pain-box h3 {{ color:#ef4444; margin-bottom:8px; }}
        .solution-box {{ background:#f0fdf4; border-left:4px solid #22c55e; border-radius:8px; padding:20px; margin:30px 0; }}
        .solution-box h3 {{ color:#22c55e; margin-bottom:8px; }}
        .features {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; margin:30px 0; }}
        .feature-item {{ background:#f8fafc; border-radius:12px; padding:20px; border:1px solid #e2e8f0; }}
        .feature-item::before {{ content:"✓ "; color:{product['color']}; font-weight:700; }}
        .cta-section {{ text-align:center; padding:50px 20px; background:{product['gradient']}; border-radius:16px; margin:40px 0; color:#fff; }}
        .cta-section h2 {{ margin-bottom:12px; }}
        .cta-btn {{ display:inline-block; background:#25D366; color:#fff; padding:14px 35px; border-radius:50px; text-decoration:none; font-weight:700; font-size:1.05rem; margin:8px; }}
        .cta-btn:hover {{ transform:translateY(-2px); box-shadow:0 8px 20px rgba(0,0,0,0.2); }}
        .cta-btn.outline {{ background:transparent; border:2px solid #fff; }}
        .other-products {{ margin:40px 0; }}
        .product-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px; }}
        .product-card {{ background:#f8fafc; border-radius:12px; padding:20px; text-align:center; text-decoration:none; color:#0f172a; border:1px solid #e2e8f0; transition:all 0.3s; }}
        .product-card:hover {{ transform:translateY(-4px); box-shadow:0 8px 24px rgba(0,0,0,0.08); border-color:{product['color']}; }}
        .product-card .icon {{ font-size:2rem; margin-bottom:8px; }}
        .other-industries {{ margin:40px 0; }}
        .industry-chips {{ display:flex; flex-wrap:wrap; gap:10px; }}
        .industry-chip {{ display:inline-block; padding:8px 16px; background:#f1f5f9; border-radius:50px; text-decoration:none; color:#475569; font-size:0.9rem; transition:all 0.2s; }}
        .industry-chip:hover {{ background:{product['color']}; color:#fff; }}
        .footer {{ background:#0f172a; color:#94a3b8; padding:30px 20px; text-align:center; font-size:0.85rem; }}
        .footer a {{ color:{product['color']}; text-decoration:none; }}
        .wa-float {{ position:fixed; bottom:20px; right:20px; background:#25D366; color:#fff; width:56px; height:56px; border-radius:50%; display:flex; align-items:center; justify-content:center; text-decoration:none; box-shadow:0 4px 16px rgba(0,0,0,0.2); z-index:999; }}
        .wa-float svg {{ width:28px; height:28px; fill:#fff; }}
        @media(max-width:768px) {{ .hero h1 {{ font-size:1.5em; }} .features {{ grid-template-columns:1fr; }} }}
    </style>
</head>
<body>
    <div class="header"><a href="{SITE_URL}/">BroadbandHK</a></div>
    <div class="nav">
        <a href="{SITE_URL}/">首頁</a> &gt;
        <a href="{SITE_URL}/{product['page']}">{product['name']}</a> &gt;
        <span>{industry['name']}</span>
    </div>

    <div class="hero">
        <div style="font-size:3rem;margin-bottom:16px;">{industry['icon']} {product['icon']}</div>
        <h1>{industry['name']} {product['name']}方案</h1>
        <p>專為{industry['name']}度身訂造嘅 {product['name']}解決方案，解決行業痛點，提升營運效率。</p>
    </div>

    <div class="container">
        <div class="pain-box">
            <h3>{industry['icon']} {industry['name']}常見痛點</h3>
            <p>{industry['pain_points']}</p>
        </div>

        <div class="solution-box">
            <h3>{product['icon']} {product['name']}點樣幫到{industry['name']}？</h3>
            <p>{use_case}</p>
        </div>

        <h2 class="section-title">{product['name']}主要功能</h2>
        <div class="features">
            {"".join(f'<div class="feature-item">{f}</div>' for f in product['features'])}
        </div>

        <div class="cta-section">
            <h2>想為你嘅{industry['name']}升級 {product['name']}？</h2>
            <p style="opacity:0.9;margin-bottom:20px;">WhatsApp 免費諮詢，我哋會根據你嘅需求推薦最適合嘅方案</p>
            <a href="https://api.whatsapp.com/send?phone=85252287541&text={wa_text}" class="cta-btn">WhatsApp 免費諮詢</a>
            <a href="{SITE_URL}/{product['page']}" class="cta-btn outline">了解{product['name']}詳情</a>
        </div>

        <div class="other-products">
            <h2 class="section-title">{industry['name']}其他 AI 方案</h2>
            <div class="product-grid">
                {"".join(f'''<a href="{p['id']}-{industry['id']}.html" class="product-card"><div class="icon">{p['icon']}</div><strong>{p['name']}</strong></a>''' for p in AI_PRODUCTS if p['id'] != product['id'])}
            </div>
        </div>

        <div class="other-industries">
            <h2 class="section-title">{product['name']} — 其他行業方案</h2>
            <div class="industry-chips">
                {"".join(f'''<a href="{product['id']}-{ind['id']}.html" class="industry-chip">{ind['icon']} {ind['name']}</a>''' for ind in INDUSTRIES if ind['id'] != industry['id'])}
            </div>
        </div>
    </div>

    <div class="footer">
        <p>&copy; {datetime.now().year} BroadbandHK 寬頻格價比較 | <a href="{SITE_URL}/">broadbandhk.com</a></p>
        <p style="margin-top:8px;">WhatsApp: <a href="https://api.whatsapp.com/send?phone=85252287541">5228 7541</a></p>
    </div>

    <a href="https://api.whatsapp.com/send?phone=85252287541&text={wa_text}" class="wa-float" aria-label="WhatsApp 查詢">
        <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.611.611l4.458-1.495A11.946 11.946 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.336 0-4.512-.767-6.262-2.064l-.438-.334-2.654.89.89-2.654-.334-.438A9.956 9.956 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg>
    </a>
</body>
</html>"""
    return slug, html


def generate_product_district_page(product, district):
    """生成 AI產品 x 地區 頁面"""
    slug = f"{product['id']}-{district['id']}"
    title = f"{district['name']}{product['name']} | BroadbandHK"
    desc = f"{district['name']}{product['name']}方案。BroadbandHK 為{district['name']}商戶及家庭提供專業 AI 方案，立即 WhatsApp 免費諮詢。"
    wa_text = f"你好，我喺{district['name']}，想了解{product['name']}方案"
    features_html = "\n".join(
        f'                <div class="feature-item">{f}</div>' for f in product["features"]
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{product['keywords']}, {district['name']}, 香港">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{SITE_URL}/pages/{slug}.html">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📶</text></svg>">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-23EZE5P385"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-23EZE5P385');</script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:'Noto Sans TC',sans-serif; color:#0f172a; line-height:1.7; }}
        .header {{ background:{product['gradient']}; color:#fff; padding:20px; text-align:center; }}
        .header a {{ color:#fff; text-decoration:none; font-size:1.4em; font-weight:700; }}
        .nav {{ background:#f8fafc; padding:12px 20px; border-bottom:1px solid #e2e8f0; font-size:0.9rem; }}
        .nav a {{ color:{product['color']}; text-decoration:none; }}
        .hero {{ background:{product['gradient']}; color:#fff; padding:60px 20px; text-align:center; }}
        .hero h1 {{ font-size:2em; margin-bottom:12px; }}
        .hero p {{ font-size:1.1rem; opacity:0.9; max-width:700px; margin:0 auto; }}
        .container {{ max-width:1000px; margin:0 auto; padding:40px 20px; }}
        .section-title {{ font-size:1.5em; margin-bottom:20px; }}
        .features {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; margin:30px 0; }}
        .feature-item {{ background:#f8fafc; border-radius:12px; padding:20px; border:1px solid #e2e8f0; }}
        .feature-item::before {{ content:"✓ "; color:{product['color']}; font-weight:700; }}
        .cta-section {{ text-align:center; padding:50px 20px; background:{product['gradient']}; border-radius:16px; margin:40px 0; color:#fff; }}
        .cta-btn {{ display:inline-block; background:#25D366; color:#fff; padding:14px 35px; border-radius:50px; text-decoration:none; font-weight:700; margin:8px; }}
        .cta-btn.outline {{ background:transparent; border:2px solid #fff; }}
        .district-chips {{ display:flex; flex-wrap:wrap; gap:10px; margin:20px 0; }}
        .district-chip {{ padding:8px 16px; background:#f1f5f9; border-radius:50px; text-decoration:none; color:#475569; font-size:0.9rem; transition:all 0.2s; }}
        .district-chip:hover {{ background:{product['color']}; color:#fff; }}
        .district-chip.active {{ background:{product['color']}; color:#fff; }}
        .footer {{ background:#0f172a; color:#94a3b8; padding:30px 20px; text-align:center; font-size:0.85rem; }}
        .footer a {{ color:{product['color']}; text-decoration:none; }}
        .wa-float {{ position:fixed; bottom:20px; right:20px; background:#25D366; color:#fff; width:56px; height:56px; border-radius:50%; display:flex; align-items:center; justify-content:center; text-decoration:none; box-shadow:0 4px 16px rgba(0,0,0,0.2); z-index:999; }}
        .wa-float svg {{ width:28px; height:28px; fill:#fff; }}
        @media(max-width:768px) {{ .hero h1 {{ font-size:1.5em; }} .features {{ grid-template-columns:1fr; }} }}
    </style>
</head>
<body>
    <div class="header"><a href="{SITE_URL}/">BroadbandHK</a></div>
    <div class="nav">
        <a href="{SITE_URL}/">首頁</a> &gt;
        <a href="{SITE_URL}/{product['page']}">{product['name']}</a> &gt;
        <span>{district['name']}</span>
    </div>

    <div class="hero">
        <div style="font-size:3rem;margin-bottom:16px;">{product['icon']}</div>
        <h1>{district['name']} {product['name']}</h1>
        <p>BroadbandHK 為{district['name']}商戶及家庭提供專業{product['name']}方案</p>
    </div>

    <div class="container">
        <h2 class="section-title">{product['name']}主要功能</h2>
        <div class="features">
            {features_html}
        </div>

        <div class="cta-section">
            <h2>{district['name']}商戶及家庭 — 立即升級 {product['name']}</h2>
            <p style="opacity:0.9;margin-bottom:20px;">WhatsApp 免費諮詢，為你度身推薦最適合嘅方案</p>
            <a href="https://api.whatsapp.com/send?phone=85252287541&text={wa_text}" class="cta-btn">WhatsApp 免費諮詢</a>
            <a href="{SITE_URL}/{product['page']}" class="cta-btn outline">了解{product['name']}詳情</a>
        </div>

        <h2 class="section-title">{product['name']} — 其他地區</h2>
        <div class="district-chips">
            {"".join(f'''<a href="{product['id']}-{d['id']}.html" class="district-chip{' active' if d['id'] == district['id'] else ''}">{d['name']}</a>''' for d in DISTRICTS)}
        </div>
    </div>

    <div class="footer">
        <p>&copy; {datetime.now().year} BroadbandHK 寬頻格價比較 | <a href="{SITE_URL}/">broadbandhk.com</a></p>
    </div>

    <a href="https://api.whatsapp.com/send?phone=85252287541&text={wa_text}" class="wa-float" aria-label="WhatsApp 查詢">
        <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.611.611l4.458-1.495A11.946 11.946 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.336 0-4.512-.767-6.262-2.064l-.438-.334-2.654.89.89-2.654-.334-.438A9.956 9.956 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg>
    </a>
</body>
</html>"""
    return slug, html


def generate_ai_index_page(all_pages):
    """生成 AI 產品 SEO 總覽頁面"""
    industry_links = []
    for ind in INDUSTRIES:
        links = " ".join(
            f'<a href="{p["id"]}-{ind["id"]}.html" style="color:{p["color"]};text-decoration:none;padding:4px 8px;background:#f1f5f9;border-radius:4px;font-size:0.85rem;">{p["icon"]} {p["name"]}</a>'
            for p in AI_PRODUCTS
        )
        industry_links.append(
            f'<div style="margin-bottom:16px;"><strong>{ind["icon"]} {ind["name"]}</strong><br>{links}</div>'
        )

    district_links = []
    for d in DISTRICTS:
        links = " ".join(
            f'<a href="{p["id"]}-{d["id"]}.html" style="color:{p["color"]};text-decoration:none;padding:4px 8px;background:#f1f5f9;border-radius:4px;font-size:0.85rem;">{p["icon"]}</a>'
            for p in AI_PRODUCTS
        )
        district_links.append(
            f'<div style="display:inline-block;margin:6px;padding:8px 12px;background:#f8fafc;border-radius:8px;"><strong>{d["name"]}</strong> {links}</div>'
        )

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 產品方案總覽 | BroadbandHK</title>
    <meta name="description" content="BroadbandHK AI 產品方案總覽：AI WiFi 管理、AI 流程自動化、AI 網絡監控、AI 一體機、AI Chatbot。覆蓋全港 18 區、8 大行業。">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{SITE_URL}/pages/ai-products-index.html">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-23EZE5P385"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-23EZE5P385');</script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:'Noto Sans TC',sans-serif; color:#0f172a; line-height:1.7; }}
        .header {{ background:linear-gradient(135deg,#0f172a,#1e1b4b,#0e7490); color:#fff; padding:60px 20px; text-align:center; }}
        .header h1 {{ font-size:2.2em; margin-bottom:12px; }}
        .header p {{ opacity:0.9; max-width:600px; margin:0 auto; }}
        .container {{ max-width:1100px; margin:0 auto; padding:40px 20px; }}
        h2 {{ font-size:1.5em; margin:40px 0 20px; padding-bottom:8px; border-bottom:2px solid #e2e8f0; }}
        .footer {{ background:#0f172a; color:#94a3b8; padding:30px 20px; text-align:center; }}
        .footer a {{ color:#06b6d4; text-decoration:none; }}
        .stats {{ display:flex; gap:20px; justify-content:center; margin:30px 0; flex-wrap:wrap; }}
        .stat {{ background:#f0f9ff; padding:20px 30px; border-radius:12px; text-align:center; }}
        .stat-num {{ font-size:2em; font-weight:900; color:#0e7490; }}
    </style>
</head>
<body>
    <div class="header">
        <p style="margin-bottom:12px;"><a href="{SITE_URL}/" style="color:#fff;text-decoration:none;">BroadbandHK</a></p>
        <h1>AI 產品方案總覽</h1>
        <p>覆蓋全港 18 區、8 大行業，共 {len(all_pages)} 個專業 AI 方案頁面</p>
    </div>
    <div class="container">
        <div class="stats">
            <div class="stat"><div class="stat-num">5</div>AI 產品</div>
            <div class="stat"><div class="stat-num">{len(INDUSTRIES)}</div>行業方案</div>
            <div class="stat"><div class="stat-num">{len(DISTRICTS)}</div>地區覆蓋</div>
            <div class="stat"><div class="stat-num">{len(all_pages)}</div>SEO 頁面</div>
        </div>

        <h2>按行業瀏覽</h2>
        {"".join(industry_links)}

        <h2>按地區瀏覽</h2>
        <div>{"".join(district_links)}</div>
    </div>
    <div class="footer">
        <p>&copy; {datetime.now().year} BroadbandHK | <a href="{SITE_URL}/">broadbandhk.com</a> | WhatsApp: <a href="https://api.whatsapp.com/send?phone=85252287541">5228 7541</a></p>
    </div>
</body>
</html>"""
    return html


def generate_sitemap_entries(all_pages):
    """生成 sitemap XML 條目"""
    today = datetime.now().strftime("%Y-%m-%d")
    entries = []
    entries.append(f'  <url><loc>{SITE_URL}/pages/ai-products-index.html</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>')
    for slug in all_pages:
        entries.append(f'  <url><loc>{SITE_URL}/pages/{slug}.html</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>')
    return entries


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_pages = []
    count = 0

    # 1. 生成 AI產品 x 行業 頁面 (5 x 8 = 40 頁)
    print("生成 AI 產品 x 行業頁面...")
    for product in AI_PRODUCTS:
        for industry in INDUSTRIES:
            slug, html = generate_product_industry_page(product, industry)
            filepath = os.path.join(OUTPUT_DIR, f"{slug}.html")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            all_pages.append(slug)
            count += 1

    # 2. 生成 AI產品 x 地區 頁面 (5 x 18 = 90 頁)
    print("生成 AI 產品 x 地區頁面...")
    for product in AI_PRODUCTS:
        for district in DISTRICTS:
            slug, html = generate_product_district_page(product, district)
            filepath = os.path.join(OUTPUT_DIR, f"{slug}.html")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            all_pages.append(slug)
            count += 1

    # 3. 生成 AI 產品總覽索引頁
    print("生成 AI 產品總覽頁...")
    index_html = generate_ai_index_page(all_pages)
    with open(os.path.join(OUTPUT_DIR, "ai-products-index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # 4. 生成 sitemap
    print("生成 sitemap...")
    sitemap_entries = generate_sitemap_entries(all_pages)
    sitemap_path = os.path.join(os.path.dirname(OUTPUT_DIR), "sitemap-ai.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.write("\n".join(sitemap_entries))
        f.write("\n</urlset>\n")

    print(f"\n完成！共生成 {count} 個 AI SEO 頁面 + 1 個索引頁")
    print(f"  - AI 產品 x 行業：{len(AI_PRODUCTS)} x {len(INDUSTRIES)} = {len(AI_PRODUCTS) * len(INDUSTRIES)} 頁")
    print(f"  - AI 產品 x 地區：{len(AI_PRODUCTS)} x {len(DISTRICTS)} = {len(AI_PRODUCTS) * len(DISTRICTS)} 頁")
    print(f"  - 索引頁：1 頁")
    print(f"  - Sitemap：{sitemap_path}")
    print(f"\n輸出目錄：{OUTPUT_DIR}")


if __name__ == "__main__":
    main()
