"""
香港寬頻 SEO 頁面生成器
從政府公開數據生成每個屋苑/樓宇的 SEO 頁面
"""

import xml.etree.ElementTree as ET
import json
import os
import re
from urllib.parse import quote
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "pages")
SITE_URL = "https://broadbandhk.com"

# 18 districts mapping
DISTRICT_MAP = {
    "Central and Western": "中西區",
    "Eastern": "東區",
    "Southern": "南區",
    "Wan Chai": "灣仔區",
    "Kowloon City": "九龍城區",
    "Kwun Tong": "觀塘區",
    "Sham Shui Po": "深水埗區",
    "Wong Tai Sin": "黃大仙區",
    "Yau Tsim Mong": "油尖旺區",
    "Islands": "離島區",
    "Kwai Tsing": "葵青區",
    "North": "北區",
    "Sai Kung": "西貢區",
    "Sha Tin": "沙田區",
    "Tai Po": "大埔區",
    "Tsuen Wan": "荃灣區",
    "Tuen Mun": "屯門區",
    "Yuen Long": "元朗區",
}


def safe_filename(name):
    """Create a safe filename from building/estate name."""
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', '-', name.strip())
    name = name.lower()
    return name[:100]


def parse_rvd_xml(filepath):
    """Parse RVD building names XML file."""
    buildings = []
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        for record in root.findall('.//Record'):
            building = {
                'name_en': '',
                'name_zh': '',
                'address_en': '',
                'address_zh': '',
                'year_built': '',
                'type': 'private'
            }
            for child in record:
                tag = child.tag
                text = (child.text or '').strip()
                if tag == 'EnglishBuildingName1':
                    building['name_en'] = text
                elif tag == 'ChineseBuildingName1':
                    building['name_zh'] = text
                elif tag == 'EnglishAddress1':
                    building['address_en'] = text
                elif tag == 'ChineseAddress1':
                    building['address_zh'] = text
                elif tag == 'YearBuild':
                    building['year_built'] = text
                elif tag == 'ChinesePublicHousingType':
                    if text:
                        building['type'] = 'public'
            if building['name_en'] or building['name_zh']:
                buildings.append(building)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
    return buildings


def parse_ha_json(filepath, estate_type):
    """Parse Housing Authority JSON file."""
    estates = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            estate = {
                'name_en': item.get('Estate Name', {}).get('en', ''),
                'name_zh': item.get('Estate Name', {}).get('zh-Hant', '') or item.get('Estate Name', {}).get('zh-Hans', ''),
                'district_en': item.get('District Name', {}).get('en', ''),
                'district_zh': item.get('District Name', {}).get('zh-Hant', '') or item.get('District Name', {}).get('zh-Hans', ''),
                'region_en': item.get('Region Name', {}).get('en', ''),
                'year': item.get('Year of Intake', item.get('Year of Completion', '')),
                'blocks': item.get('No. of Blocks', ''),
                'flats': item.get('No. of Rental Flats', item.get('No. of Flats', '')),
                'block_names': item.get('Name of Block(s)', {}).get('zh-Hant', '') or item.get('Name of Block(s)', {}).get('en', ''),
                'lat': item.get('Estate Map Latitude', ''),
                'lng': item.get('Estate Map Longitude', ''),
                'type': estate_type
            }
            if estate['name_en'] or estate['name_zh']:
                estates.append(estate)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
    return estates


def generate_building_page(building, index):
    """Generate an SEO page for a single building."""
    name = building.get('name_zh') or building.get('name_en') or f"building-{index}"
    name_en = building.get('name_en', '')
    name_zh = building.get('name_zh', '')
    address_en = building.get('address_en', '')
    address_zh = building.get('address_zh', '')
    year = building.get('year_built', '')
    display_name = f"{name_zh} {name_en}".strip() if name_zh else name_en

    title = f"{display_name} 寬頻上網 | 光纖入屋月費比較 - SpeedNet"
    description = f"{display_name} 寬頻比較，比較各大供應商光纖入屋月費Plan。{address_zh} 覆蓋查詢，最平寬頻由$98起。立即免費查詢！"

    return generate_html(title, description, display_name, name_en, name_zh,
                        address_en, address_zh, year, building.get('type', 'private'),
                        '', '', '', '', '')


def generate_estate_page(estate):
    """Generate an SEO page for a housing estate."""
    name_en = estate.get('name_en', '')
    name_zh = estate.get('name_zh', '')
    district_zh = estate.get('district_zh', '')
    display_name = f"{name_zh} {name_en}".strip() if name_zh else name_en
    estate_type = "公共屋邨" if estate['type'] == 'prh' else "居屋屋苑"

    title = f"{display_name} 寬頻上網 | {estate_type}光纖寬頻比較 - SpeedNet"
    description = f"{display_name} ({district_zh}) 寬頻比較，{estate_type}光纖入屋月費由$98起。比較各大供應商Plan，免費查詢最適合你嘅寬頻方案！"

    return generate_html(title, description, display_name, name_en, name_zh,
                        '', '', estate.get('year', ''), estate['type'],
                        district_zh, estate.get('blocks', ''), estate.get('flats', ''),
                        estate.get('block_names', ''), estate_type)


def generate_html(title, description, display_name, name_en, name_zh,
                  address_en, address_zh, year, btype,
                  district_zh, blocks, flats, block_names, estate_type_label):
    """Generate the HTML page content."""

    address_section = ""
    if address_zh or address_en:
        address_section = f"""
            <div class="info-card">
                <h3>地址</h3>
                <p>{address_zh}</p>
                <p>{address_en}</p>
            </div>"""

    year_section = ""
    if year:
        year_section = f"""
            <div class="info-card">
                <h3>落成年份</h3>
                <p>{year}</p>
            </div>"""

    estate_info = ""
    if blocks or flats:
        estate_info = f"""
            <div class="info-card">
                <h3>屋苑資料</h3>
                {"<p>座數：" + str(blocks) + "</p>" if blocks else ""}
                {"<p>單位數：" + str(flats) + "</p>" if flats else ""}
                {"<p>樓宇：" + str(block_names) + "</p>" if block_names else ""}
            </div>"""

    type_label = estate_type_label or ("私人樓宇" if btype == "private" else "公營房屋")
    district_text = f" ({district_zh})" if district_zh else ""

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{SITE_URL}/pages/{safe_filename(name_en or name_zh)}.html">

    <!-- Open Graph -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{SITE_URL}/pages/{safe_filename(name_en or name_zh)}.html">
    <meta property="og:site_name" content="SpeedNet 寬頻比較">

    <!-- Schema.org -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "SpeedNet 寬頻比較 - {display_name}",
        "description": "{description}",
        "url": "{SITE_URL}/pages/{safe_filename(name_en or name_zh)}.html",
        "areaServed": {{
            "@type": "Place",
            "name": "{display_name}{district_text}"
        }},
        "serviceType": "寬頻上網服務"
    }}
    </script>

    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #333; line-height: 1.6; }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 20px; text-align: center;
        }}
        .header a {{ color: white; text-decoration: none; font-size: 1.5em; font-weight: bold; }}
        .nav {{ background: #f8f9fa; padding: 10px 20px; border-bottom: 1px solid #dee2e6; }}
        .nav a {{ color: #667eea; text-decoration: none; margin-right: 10px; }}
        .nav a:hover {{ text-decoration: underline; }}

        .hero {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white; padding: 60px 20px; text-align: center;
        }}
        .hero h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .hero p {{ font-size: 1.1em; opacity: 0.9; max-width: 700px; margin: 0 auto; }}

        .container {{ max-width: 1000px; margin: 0 auto; padding: 30px 20px; }}

        .info-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin: 30px 0; }}
        .info-card {{ background: #f8f9fa; border-radius: 12px; padding: 25px; border-left: 4px solid #667eea; }}
        .info-card h3 {{ color: #667eea; margin-bottom: 10px; }}

        .plans {{ margin: 40px 0; }}
        .plans h2 {{ color: #333; margin-bottom: 20px; text-align: center; }}
        .plan-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }}
        .plan-card {{
            border: 2px solid #e9ecef; border-radius: 12px; padding: 30px;
            text-align: center; transition: all 0.3s;
        }}
        .plan-card:hover {{ border-color: #667eea; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
        .plan-card.popular {{ border-color: #667eea; position: relative; }}
        .plan-card.popular::before {{
            content: "最受歡迎"; position: absolute; top: -12px; left: 50%;
            transform: translateX(-50%); background: #667eea; color: white;
            padding: 4px 16px; border-radius: 20px; font-size: 0.85em;
        }}
        .plan-name {{ font-size: 1.3em; font-weight: bold; color: #333; }}
        .plan-speed {{ color: #667eea; font-size: 1.1em; margin: 5px 0; }}
        .plan-price {{ font-size: 2.2em; font-weight: bold; color: #f5576c; margin: 15px 0; }}
        .plan-price span {{ font-size: 0.4em; color: #666; }}
        .plan-features {{ list-style: none; margin: 15px 0; text-align: left; }}
        .plan-features li {{ padding: 5px 0; }}
        .plan-features li::before {{ content: "✓ "; color: #28a745; font-weight: bold; }}

        .cta-btn {{
            display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2);
            color: white; padding: 14px 35px; border-radius: 30px;
            text-decoration: none; font-size: 1.1em; font-weight: bold;
            transition: all 0.3s; border: none; cursor: pointer;
        }}
        .cta-btn:hover {{ transform: scale(1.05); box-shadow: 0 5px 20px rgba(102,126,234,0.4); }}
        .cta-btn.whatsapp {{ background: #25D366; }}

        .cta-section {{ text-align: center; padding: 50px 20px; background: #f8f9fa; border-radius: 12px; margin: 40px 0; }}
        .cta-section h2 {{ margin-bottom: 15px; }}
        .cta-section p {{ margin-bottom: 25px; color: #666; }}
        .cta-buttons {{ display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; }}

        .faq {{ margin: 40px 0; }}
        .faq h2 {{ text-align: center; margin-bottom: 20px; }}
        .faq-item {{ border: 1px solid #e9ecef; border-radius: 8px; margin-bottom: 10px; padding: 20px; }}
        .faq-item h3 {{ color: #667eea; margin-bottom: 8px; font-size: 1em; }}
        .faq-item p {{ color: #666; font-size: 0.95em; }}

        .footer {{
            background: #2d3748; color: #a0aec0; padding: 30px 20px;
            text-align: center; font-size: 0.9em;
        }}
        .footer a {{ color: #667eea; text-decoration: none; }}

        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 1.5em; }}
            .plan-price {{ font-size: 1.8em; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <a href="{SITE_URL}/">SpeedNet 寬頻比較</a>
    </div>

    <div class="nav">
        <a href="{SITE_URL}/">首頁</a> &gt;
        <a href="{SITE_URL}/pages/index.html">全港屋苑</a> &gt;
        <span>{display_name}</span>
    </div>

    <div class="hero">
        <h1>{display_name} 寬頻上網</h1>
        <p>{type_label}{district_text} | 比較各大寬頻供應商月費Plan，搵出最適合你嘅光纖入屋方案</p>
    </div>

    <div class="container">
        <div class="info-grid">
            <div class="info-card">
                <h3>樓宇類型</h3>
                <p>{type_label}</p>
            </div>
            {address_section}
            {year_section}
            {estate_info}
        </div>

        <div class="plans">
            <h2>{display_name} 可選寬頻月費計劃</h2>
            <p style="text-align:center;color:#666;margin-bottom:25px;">以下為各速度等級嘅參考月費，實際收費以供應商報價為準</p>

            <div class="plan-grid">
                <div class="plan-card">
                    <div class="plan-name">基本版</div>
                    <div class="plan-speed">100M 光纖入屋</div>
                    <div class="plan-price">$78<span>起/月</span></div>
                    <ul class="plan-features">
                        <li>100Mbps 下載速度</li>
                        <li>適合輕度上網用家</li>
                        <li>免費標準安裝</li>
                        <li>24個月合約</li>
                    </ul>
                    <a href="https://wa.me/85252287541?text=你好，我想查詢{display_name}嘅100M寬頻Plan" class="cta-btn whatsapp">WhatsApp 查詢</a>
                </div>

                <div class="plan-card popular">
                    <div class="plan-name">進階版</div>
                    <div class="plan-speed">500M 光纖入屋</div>
                    <div class="plan-price">$108<span>起/月</span></div>
                    <ul class="plan-features">
                        <li>500Mbps 下載速度</li>
                        <li>適合一般家庭使用</li>
                        <li>免費 Wi-Fi Router</li>
                        <li>免安裝費</li>
                    </ul>
                    <a href="https://wa.me/85252287541?text=你好，我想查詢{display_name}嘅500M寬頻Plan" class="cta-btn whatsapp">WhatsApp 查詢</a>
                </div>

                <div class="plan-card">
                    <div class="plan-name">極速版</div>
                    <div class="plan-speed">1000M 光纖入屋</div>
                    <div class="plan-price">$148<span>起/月</span></div>
                    <ul class="plan-features">
                        <li>1000Mbps 極速下載</li>
                        <li>適合多人家庭/WFH</li>
                        <li>免費 Mesh Wi-Fi</li>
                        <li>7x24 技術支援</li>
                    </ul>
                    <a href="https://wa.me/85252287541?text=你好，我想查詢{display_name}嘅1000M寬頻Plan" class="cta-btn whatsapp">WhatsApp 查詢</a>
                </div>
            </div>
        </div>

        <div class="cta-section">
            <h2>想知 {display_name} 邊間寬頻最抵？</h2>
            <p>我哋免費幫你比較所有覆蓋 {display_name} 嘅寬頻供應商，搵出最平最快嘅Plan！</p>
            <div class="cta-buttons">
                <a href="https://wa.me/85252287541?text=你好，我住{display_name}，想查詢寬頻Plan" class="cta-btn whatsapp">WhatsApp 免費查詢</a>
                <a href="tel:+85252287541" class="cta-btn">致電查詢</a>
            </div>
        </div>

        <div class="faq">
            <h2>常見問題</h2>

            <div class="faq-item">
                <h3>{display_name} 有邊幾間寬頻供應商覆蓋？</h3>
                <p>視乎大廈嘅網絡基建，一般會有2至5間供應商覆蓋，包括網上行、香港寬頻、和記寬頻、有線寬頻及中國移動等。立即聯絡我哋免費查詢{display_name}嘅覆蓋情況。</p>
            </div>

            <div class="faq-item">
                <h3>{display_name} 最平嘅寬頻月費係幾多？</h3>
                <p>視乎速度同合約期，最平嘅Plan由$78起/月。我哋可以免費幫你格價，搵出最適合你預算嘅方案。</p>
            </div>

            <div class="faq-item">
                <h3>{display_name} 裝寬頻要幾耐？</h3>
                <p>一般情況下，如果大廈已有供應商覆蓋，最快可以即日至3個工作天內完成安裝。新屋苑或需要額外拉線嘅情況可能需要較長時間。</p>
            </div>

            <div class="faq-item">
                <h3>我而家住{display_name}，寬頻就嚟約滿，應該點做？</h3>
                <p>建議喺約滿前1至2個月開始格價比較。我哋可以免費幫你比較所有覆蓋你地址嘅供應商，通常轉台可以慳到20-40%月費。</p>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>&copy; {datetime.now().year} SpeedNet 寬頻比較 | <a href="{SITE_URL}/">broadbandhk.com</a></p>
        <p style="margin-top:8px;">免費寬頻格價比較服務 | WhatsApp: <a href="https://wa.me/85252287541">6038 1533</a></p>
    </div>
</body>
</html>"""
    return html


def generate_district_page(district_en, district_zh, buildings):
    """Generate a district index page listing all buildings."""
    title = f"{district_zh} 寬頻比較 | {district_en} 全區屋苑光纖寬頻月費 - SpeedNet"
    description = f"{district_zh}所有屋苑寬頻比較，比較各大供應商光纖入屋Plan。覆蓋全區{len(buildings)}個屋苑，免費格價查詢！"

    building_links = []
    for b in sorted(buildings, key=lambda x: x.get('name_zh', x.get('name_en', ''))):
        name = b.get('name_zh', '') or b.get('name_en', '')
        name_en = b.get('name_en', '')
        if not name:
            continue
        fname = safe_filename(name_en or name)
        display = f"{b.get('name_zh', '')} {b.get('name_en', '')}".strip()
        building_links.append(f'<li><a href="{fname}.html">{display}</a></li>')

    buildings_html = "\n".join(building_links)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{SITE_URL}/pages/district-{safe_filename(district_en)}.html">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #333; line-height: 1.6; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
        .header a {{ color: white; text-decoration: none; font-size: 1.5em; font-weight: bold; }}
        .nav {{ background: #f8f9fa; padding: 10px 20px; border-bottom: 1px solid #dee2e6; }}
        .nav a {{ color: #667eea; text-decoration: none; margin-right: 10px; }}
        .hero {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 50px 20px; text-align: center; }}
        .hero h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .hero p {{ opacity: 0.9; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 30px 20px; }}
        .building-list {{ column-count: 2; column-gap: 30px; list-style: none; }}
        .building-list li {{ padding: 8px 0; border-bottom: 1px solid #f0f0f0; break-inside: avoid; }}
        .building-list a {{ color: #667eea; text-decoration: none; }}
        .building-list a:hover {{ text-decoration: underline; }}
        .stats {{ display: flex; gap: 20px; justify-content: center; margin: 30px 0; flex-wrap: wrap; }}
        .stat {{ background: #f8f9fa; padding: 20px 30px; border-radius: 12px; text-align: center; }}
        .stat-num {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; }}
        .cta-section {{ text-align: center; padding: 40px 20px; background: #f8f9fa; border-radius: 12px; margin: 40px 0; }}
        .cta-btn {{ display: inline-block; background: #25D366; color: white; padding: 14px 35px; border-radius: 30px; text-decoration: none; font-weight: bold; }}
        .footer {{ background: #2d3748; color: #a0aec0; padding: 30px 20px; text-align: center; font-size: 0.9em; }}
        .footer a {{ color: #667eea; text-decoration: none; }}
        @media (max-width: 768px) {{ .building-list {{ column-count: 1; }} .hero h1 {{ font-size: 1.5em; }} }}
    </style>
</head>
<body>
    <div class="header"><a href="{SITE_URL}/">SpeedNet 寬頻比較</a></div>
    <div class="nav">
        <a href="{SITE_URL}/">首頁</a> &gt;
        <a href="{SITE_URL}/pages/index.html">全港屋苑</a> &gt;
        <span>{district_zh}</span>
    </div>
    <div class="hero">
        <h1>{district_zh} ({district_en}) 寬頻比較</h1>
        <p>比較{district_zh}全區所有屋苑嘅寬頻供應商及月費計劃</p>
    </div>
    <div class="container">
        <div class="stats">
            <div class="stat"><div class="stat-num">{len(buildings)}</div><div class="stat-label">個屋苑/樓宇</div></div>
            <div class="stat"><div class="stat-num">5+</div><div class="stat-label">間寬頻供應商</div></div>
            <div class="stat"><div class="stat-num">$78</div><div class="stat-label">起/月</div></div>
        </div>
        <h2 style="margin-bottom:20px;">{district_zh} 所有屋苑及樓宇</h2>
        <ul class="building-list">
            {buildings_html}
        </ul>
        <div class="cta-section">
            <h2>搵唔到你嘅大廈？</h2>
            <p style="margin:15px 0;color:#666;">WhatsApp 我哋，免費幫你查詢任何地址嘅寬頻覆蓋情況！</p>
            <a href="https://wa.me/85252287541?text=你好，我住{district_zh}，想查詢寬頻Plan" class="cta-btn">WhatsApp 免費查詢</a>
        </div>
    </div>
    <div class="footer">
        <p>&copy; {datetime.now().year} SpeedNet 寬頻比較 | <a href="{SITE_URL}/">broadbandhk.com</a></p>
    </div>
</body>
</html>"""


def generate_main_index(district_counts):
    """Generate the main index page listing all districts."""
    title = "全港屋苑寬頻比較 | 香港18區光纖寬頻月費格價 - SpeedNet"
    description = "全港18區所有屋苑寬頻比較，覆蓋超過20,000個樓宇。免費格價比較各大供應商光纖入屋Plan，搵出最平最快嘅寬頻方案！"

    total = sum(district_counts.values())

    district_cards = []
    for d_en, d_zh in sorted(DISTRICT_MAP.items(), key=lambda x: x[1]):
        count = district_counts.get(d_en, 0)
        if count == 0:
            continue
        fname = safe_filename(d_en)
        district_cards.append(f"""
            <a href="district-{fname}.html" class="district-card">
                <div class="district-name">{d_zh}</div>
                <div class="district-name-en">{d_en}</div>
                <div class="district-count">{count} 個屋苑</div>
            </a>""")

    cards_html = "\n".join(district_cards)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{SITE_URL}/pages/index.html">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #333; line-height: 1.6; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
        .header a {{ color: white; text-decoration: none; font-size: 1.5em; font-weight: bold; }}
        .hero {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 20px; text-align: center; }}
        .hero h1 {{ font-size: 2.2em; margin-bottom: 10px; }}
        .hero p {{ opacity: 0.9; font-size: 1.1em; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 30px 20px; }}
        .stats {{ display: flex; gap: 20px; justify-content: center; margin: 30px 0; flex-wrap: wrap; }}
        .stat {{ background: #f8f9fa; padding: 20px 30px; border-radius: 12px; text-align: center; min-width: 150px; }}
        .stat-num {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; }}
        .district-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 15px; margin: 30px 0; }}
        .district-card {{ display: block; background: #f8f9fa; border-radius: 12px; padding: 25px; text-decoration: none; color: #333; border: 2px solid transparent; transition: all 0.3s; }}
        .district-card:hover {{ border-color: #667eea; transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }}
        .district-name {{ font-size: 1.3em; font-weight: bold; }}
        .district-name-en {{ color: #666; font-size: 0.9em; }}
        .district-count {{ color: #667eea; margin-top: 8px; font-weight: bold; }}
        .footer {{ background: #2d3748; color: #a0aec0; padding: 30px 20px; text-align: center; font-size: 0.9em; margin-top: 40px; }}
        .footer a {{ color: #667eea; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="header"><a href="{SITE_URL}/">SpeedNet 寬頻比較</a></div>
    <div class="hero">
        <h1>全港屋苑寬頻比較</h1>
        <p>覆蓋全港18區，超過 {total:,} 個屋苑及樓宇嘅寬頻格價資料</p>
    </div>
    <div class="container">
        <div class="stats">
            <div class="stat"><div class="stat-num">{total:,}</div><div class="stat-label">個屋苑/樓宇</div></div>
            <div class="stat"><div class="stat-num">18</div><div class="stat-label">個地區</div></div>
            <div class="stat"><div class="stat-num">5+</div><div class="stat-label">間供應商</div></div>
        </div>
        <h2 style="margin-bottom:20px;">選擇你所在嘅地區</h2>
        <div class="district-grid">
            {cards_html}
        </div>
    </div>
    <div class="footer">
        <p>&copy; {datetime.now().year} SpeedNet 寬頻比較 | <a href="{SITE_URL}/">broadbandhk.com</a></p>
    </div>
</body>
</html>"""


def guess_district(address_en, address_zh):
    """Try to guess district from address."""
    addr = (address_en + ' ' + address_zh).lower()

    district_keywords = {
        "Central and Western": ["central", "sheung wan", "sai ying pun", "kennedy town", "mid-levels", "the peak", "中環", "上環", "西營盤", "堅尼地城", "半山"],
        "Eastern": ["north point", "quarry bay", "sai wan ho", "shau kei wan", "chai wan", "heng fa chuen", "taikoo", "北角", "鰂魚涌", "西灣河", "筲箕灣", "柴灣", "杏花邨", "太古"],
        "Southern": ["aberdeen", "ap lei chau", "repulse bay", "stanley", "pok fu lam", "wong chuk hang", "香港仔", "鴨脷洲", "淺水灣", "赤柱", "薄扶林", "黃竹坑"],
        "Wan Chai": ["wan chai", "causeway bay", "happy valley", "tai hang", "灣仔", "銅鑼灣", "跑馬地", "大坑"],
        "Kowloon City": ["kowloon city", "kowloon tong", "ho man tin", "hung hom", "to kwa wan", "kai tak", "九龍城", "九龍塘", "何文田", "紅磡", "土瓜灣", "啟德"],
        "Kwun Tong": ["kwun tong", "lam tin", "sau mau ping", "yau tong", "tseung kwan o", "觀塘", "藍田", "秀茂坪", "油塘"],
        "Sham Shui Po": ["sham shui po", "cheung sha wan", "lai chi kok", "mei foo", "nam cheong", "深水埗", "長沙灣", "荔枝角", "美孚", "南昌"],
        "Wong Tai Sin": ["wong tai sin", "diamond hill", "tsz wan shan", "lok fu", "choi hung", "黃大仙", "鑽石山", "慈雲山", "樂富", "彩虹"],
        "Yau Tsim Mong": ["yau ma tei", "tsim sha tsui", "mong kok", "jordan", "tai kok tsui", "油麻地", "尖沙咀", "旺角", "佐敦", "大角咀"],
        "Islands": ["tung chung", "mui wo", "cheung chau", "peng chau", "lantau", "discovery bay", "東涌", "梅窩", "長洲", "坪洲", "大嶼山", "愉景灣"],
        "Kwai Tsing": ["kwai chung", "kwai fong", "tsing yi", "葵涌", "葵芳", "青衣"],
        "North": ["sheung shui", "fanling", "sha tau kok", "ta kwu ling", "上水", "粉嶺", "沙頭角", "打鼓嶺"],
        "Sai Kung": ["sai kung", "tseung kwan o", "hang hau", "po lam", "lohas park", "西貢", "將軍澳", "坑口", "寶琳", "日出康城"],
        "Sha Tin": ["sha tin", "ma on shan", "fo tan", "tai wai", "city one", "沙田", "馬鞍山", "火炭", "大圍"],
        "Tai Po": ["tai po", "大埔"],
        "Tsuen Wan": ["tsuen wan", "荃灣"],
        "Tuen Mun": ["tuen mun", "屯門"],
        "Yuen Long": ["yuen long", "tin shui wai", "元朗", "天水圍"],
    }

    for district, keywords in district_keywords.items():
        for kw in keywords:
            if kw in addr:
                return district
    return "Other"


def main():
    print("=== 香港寬頻 SEO 頁面生成器 ===\n")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Parse all data
    print("正在讀取樓宇資料...")
    urban_buildings = parse_rvd_xml(os.path.join(DATA_DIR, "bnb-urban.xml"))
    print(f"  港九區樓宇: {len(urban_buildings)}")

    nt_buildings = parse_rvd_xml(os.path.join(DATA_DIR, "bnb-nt.xml"))
    print(f"  新界區樓宇: {len(nt_buildings)}")

    prh_estates = parse_ha_json(os.path.join(DATA_DIR, "prh-estates.json"), "prh")
    print(f"  公共屋邨: {len(prh_estates)}")

    hos_courts = parse_ha_json(os.path.join(DATA_DIR, "hos-courts.json"), "hos")
    print(f"  居屋屋苑: {len(hos_courts)}")

    # Group by district
    print("\n正在按地區分類...")
    district_buildings = {}

    # Add HA estates (they have district info)
    for estate in prh_estates + hos_courts:
        district = estate.get('district_en', 'Other')
        if district not in district_buildings:
            district_buildings[district] = []
        district_buildings[district].append(estate)

    # Add RVD buildings (guess district from address)
    for b in urban_buildings + nt_buildings:
        district = guess_district(b.get('address_en', ''), b.get('address_zh', ''))
        if district not in district_buildings:
            district_buildings[district] = []
        district_buildings[district].append(b)

    # Generate pages
    print("\n正在生成頁面...")
    sitemap_urls = []
    page_count = 0

    district_counts = {}

    for district_en, buildings in district_buildings.items():
        if district_en == "Other":
            district_zh = "其他地區"
        else:
            district_zh = DISTRICT_MAP.get(district_en, district_en)

        district_counts[district_en] = len(buildings)

        # Generate district index page
        district_filename = f"district-{safe_filename(district_en)}.html"
        district_html = generate_district_page(district_en, district_zh, buildings)
        with open(os.path.join(OUTPUT_DIR, district_filename), 'w', encoding='utf-8') as f:
            f.write(district_html)
        sitemap_urls.append(f"{SITE_URL}/pages/{district_filename}")
        page_count += 1

        # Generate individual building pages
        seen_filenames = set()
        for i, building in enumerate(buildings):
            name_en = building.get('name_en', '')
            name_zh = building.get('name_zh', '')
            fname_base = safe_filename(name_en or name_zh or f"building-{i}")

            # Handle duplicates
            fname = fname_base
            counter = 1
            while fname in seen_filenames:
                fname = f"{fname_base}-{counter}"
                counter += 1
            seen_filenames.add(fname)

            filename = f"{fname}.html"

            if 'district_en' in building:
                html = generate_estate_page(building)
            else:
                html = generate_building_page(building, i)

            with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
                f.write(html)
            sitemap_urls.append(f"{SITE_URL}/pages/{filename}")
            page_count += 1

        print(f"  {district_zh} ({district_en}): {len(buildings)} 個樓宇")

    # Generate main index page
    index_html = generate_main_index(district_counts)
    with open(os.path.join(OUTPUT_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(index_html)
    sitemap_urls.insert(0, f"{SITE_URL}/pages/index.html")
    page_count += 1

    # Generate sitemap
    print("\n正在生成 sitemap...")
    today = datetime.now().strftime('%Y-%m-%d')
    sitemap_entries = [f"""  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>""",
    f"""  <url>
    <loc>{SITE_URL}/blog.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>"""]

    for url in sitemap_urls:
        priority = "0.6" if "district-" in url or "index.html" in url else "0.5"
        sitemap_entries.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>""")

    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_entries)}
</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "..", "sitemap.xml"), 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)

    print(f"\n=== 完成！===")
    print(f"總共生成 {page_count} 個頁面")
    print(f"Sitemap 包含 {len(sitemap_urls) + 2} 個 URL")
    print(f"輸出目錄: {OUTPUT_DIR}")
    print(f"Sitemap: {os.path.join(BASE_DIR, 'sitemap.xml')}")


if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
