"""
Generate travel hotel pages for all major cities worldwide
Creates both Chinese (zh) and English (en) versions
With Trip.com affiliate links
"""

import os
import urllib.parse
from hotel_data import HOTELS

# Affiliate config
ALLIANCE_ID = "8067382"
SID = "305319575"
TRIP_SUB3 = "D15323828"

OUTPUT_DIR = "pages/travel"

# City data: (city_id, url_name, zh_name, en_name, country_zh, country_en, country_flag, region)
CITIES = [
    # Asia - Japan
    (317, "東京", "東京", "Tokyo", "日本", "Japan", "🇯🇵", "asia"),
    (293, "大阪", "大阪", "Osaka", "日本", "Japan", "🇯🇵", "asia"),
    (430, "京都", "京都", "Kyoto", "日本", "Japan", "🇯🇵", "asia"),
    (677, "福岡", "福岡", "Fukuoka", "日本", "Japan", "🇯🇵", "asia"),
    (660, "沖繩", "沖繩", "Okinawa", "日本", "Japan", "🇯🇵", "asia"),
    (605, "北海道", "北海道", "Hokkaido", "日本", "Japan", "🇯🇵", "asia"),
    (282, "名古屋", "名古屋", "Nagoya", "日本", "Japan", "🇯🇵", "asia"),
    # Asia - Korea
    (234, "首爾", "首爾", "Seoul", "韓國", "South Korea", "🇰🇷", "asia"),
    (776, "釜山", "釜山", "Busan", "韓國", "South Korea", "🇰🇷", "asia"),
    (3138, "濟州島", "濟州島", "Jeju Island", "韓國", "South Korea", "🇰🇷", "asia"),
    # Asia - Southeast Asia
    (95, "曼谷", "曼谷", "Bangkok", "泰國", "Thailand", "🇹🇭", "asia"),
    (109, "布吉", "布吉", "Phuket", "泰國", "Thailand", "🇹🇭", "asia"),
    (208, "清邁", "清邁", "Chiang Mai", "泰國", "Thailand", "🇹🇭", "asia"),
    (3658, "芭堤雅", "芭堤雅", "Pattaya", "泰國", "Thailand", "🇹🇭", "asia"),
    (73, "新加坡", "新加坡", "Singapore", "新加坡", "Singapore", "🇸🇬", "asia"),
    (171, "吉隆坡", "吉隆坡", "Kuala Lumpur", "馬來西亞", "Malaysia", "🇲🇾", "asia"),
    (3937, "蘭卡威", "蘭卡威", "Langkawi", "馬來西亞", "Malaysia", "🇲🇾", "asia"),
    (613, "峇里島", "峇里島", "Bali", "印尼", "Indonesia", "🇮🇩", "asia"),
    (193, "胡志明市", "胡志明市", "Ho Chi Minh City", "越南", "Vietnam", "🇻🇳", "asia"),
    (680, "河內", "河內", "Hanoi", "越南", "Vietnam", "🇻🇳", "asia"),
    (561, "峴港", "峴港", "Da Nang", "越南", "Vietnam", "🇻🇳", "asia"),
    (395, "馬尼拉", "馬尼拉", "Manila", "菲律賓", "Philippines", "🇵🇭", "asia"),
    (400, "宿霧", "宿霧", "Cebu", "菲律賓", "Philippines", "🇵🇭", "asia"),
    # Asia - Greater China
    (58, "香港", "香港", "Hong Kong", "香港", "Hong Kong", "🇭🇰", "asia"),
    (72, "澳門", "澳門", "Macau", "澳門", "Macau", "🇲🇴", "asia"),
    (360, "台北", "台北", "Taipei", "台灣", "Taiwan", "🇹🇼", "asia"),
    (2, "上海", "上海", "Shanghai", "中國", "China", "🇨🇳", "asia"),
    (1, "北京", "北京", "Beijing", "中國", "China", "🇨🇳", "asia"),
    (32, "深圳", "深圳", "Shenzhen", "中國", "China", "🇨🇳", "asia"),
    (152, "廣州", "廣州", "Guangzhou", "中國", "China", "🇨🇳", "asia"),
    # Asia - South Asia & Middle East
    (356, "杜拜", "杜拜", "Dubai", "阿聯酋", "UAE", "🇦🇪", "middleeast"),
    (986, "馬爾代夫", "馬爾代夫", "Maldives", "馬爾代夫", "Maldives", "🇲🇻", "asia"),
    # Europe
    (192, "倫敦", "倫敦", "London", "英國", "United Kingdom", "🇬🇧", "europe"),
    (419, "巴黎", "巴黎", "Paris", "法國", "France", "🇫🇷", "europe"),
    (382, "羅馬", "羅馬", "Rome", "意大利", "Italy", "🇮🇹", "europe"),
    (506, "巴塞隆拿", "巴塞隆拿", "Barcelona", "西班牙", "Spain", "🇪🇸", "europe"),
    (538, "阿姆斯特丹", "阿姆斯特丹", "Amsterdam", "荷蘭", "Netherlands", "🇳🇱", "europe"),
    (547, "伊斯坦堡", "伊斯坦堡", "Istanbul", "土耳其", "Turkey", "🇹🇷", "europe"),
    (433, "布拉格", "布拉格", "Prague", "捷克", "Czech Republic", "🇨🇿", "europe"),
    (508, "蘇黎世", "蘇黎世", "Zurich", "瑞士", "Switzerland", "🇨🇭", "europe"),
    # Americas
    (645, "紐約", "紐約", "New York", "美國", "United States", "🇺🇸", "americas"),
    (250, "洛杉磯", "洛杉磯", "Los Angeles", "美國", "United States", "🇺🇸", "americas"),
    (248, "拉斯維加斯", "拉斯維加斯", "Las Vegas", "美國", "United States", "🇺🇸", "americas"),
    # Oceania
    (263, "悉尼", "悉尼", "Sydney", "澳洲", "Australia", "🇦🇺", "oceania"),
    (303, "墨爾本", "墨爾本", "Melbourne", "澳洲", "Australia", "🇦🇺", "oceania"),
]

# Hotel descriptions per city (zh, en)
CITY_DESCRIPTIONS = {
    "Tokyo": {
        "zh": "東京是日本的首都，融合了傳統與現代。從淺草寺的古老魅力到新宿的霓虹燈海，這座城市永遠充滿驚喜。新宿、池袋及淺草是最受歡迎的住宿區域，日圓持續低水令旅遊性價比更高。",
        "en": "Tokyo, Japan's capital, is a mesmerizing blend of traditional culture and cutting-edge modernity. From the ancient charm of Senso-ji Temple to the neon-lit streets of Shinjuku, this city never fails to amaze. Shinjuku, Ikebukuro, and Asakusa are the most popular areas for accommodation."
    },
    "Osaka": {
        "zh": "大阪被譽為日本的「天下廚房」，以道頓堀的街頭美食聞名。心齋橋、難波及梅田是住宿首選地段。大阪環球影城令這裡成為親子遊熱點。",
        "en": "Osaka, known as Japan's 'Kitchen of the World', is famous for its street food in Dotonbori. Shinsaibashi, Namba, and Umeda are top areas to stay. Universal Studios Japan makes it a family favorite."
    },
    "Seoul": {
        "zh": "首爾是K-pop文化及美食的天堂。明洞購物區、弘大文青區及江南時尚區各具特色。韓國酒店性價比高，同級酒店比日本便宜約20-30%。",
        "en": "Seoul is a paradise for K-pop culture and cuisine. Myeongdong shopping district, Hongdae's indie scene, and Gangnam's upscale vibe each offer unique experiences. Korean hotels offer great value compared to Japan."
    },
    "Bangkok": {
        "zh": "曼谷是東南亞最受歡迎的旅遊城市之一。Sukhumvit、Silom及Siam商圈是住宿熱點。五星級酒店價格僅為香港的一半，按摩SPA體驗更是必試。",
        "en": "Bangkok is one of Southeast Asia's most popular tourist cities. Sukhumvit, Silom, and Siam are prime areas to stay. Five-star hotels cost roughly half of Hong Kong prices, and spa experiences are a must."
    },
    "Singapore": {
        "zh": "新加坡是亞洲最整潔的城市之一，濱海灣金沙酒店是地標。烏節路購物、牛車水美食及聖淘沙島度假是必遊行程。",
        "en": "Singapore is one of Asia's cleanest cities, with Marina Bay Sands as its iconic landmark. Orchard Road shopping, Chinatown dining, and Sentosa Island are must-visit attractions."
    },
    "London": {
        "zh": "倫敦是全球最具歷史文化底蘊的城市之一。西區劇院、大英博物館、白金漢宮等景點舉世聞名。住宿建議選擇Zone 1-2，交通最方便。",
        "en": "London is one of the world's most historically and culturally rich cities. The West End theatres, British Museum, and Buckingham Palace are world-renowned. Staying in Zone 1-2 is recommended for convenience."
    },
    "Paris": {
        "zh": "巴黎是浪漫之都，艾菲爾鐵塔、羅浮宮及香榭麗舍大道是必到景點。酒店選擇建議靠近地鐵站，以第1-8區最便利。",
        "en": "Paris is the City of Romance. The Eiffel Tower, Louvre Museum, and Champs-Élysées are must-visit landmarks. Hotels near Metro stations in the 1st-8th arrondissements are most convenient."
    },
    "Dubai": {
        "zh": "杜拜是奢華與現代的代名詞。帆船酒店、哈利法塔及棕櫚島是標誌性地標。沙漠體驗及購物節令杜拜成為獨特的度假選擇。",
        "en": "Dubai is synonymous with luxury and modernity. The Burj Al Arab, Burj Khalifa, and Palm Jumeirah are iconic landmarks. Desert safaris and shopping festivals make Dubai a unique vacation choice."
    },
}

# Default descriptions for cities without specific ones
DEFAULT_DESC = {
    "zh": "探索這座精彩城市的最佳酒店住宿。我們精選了從經濟型到豪華型的酒店推薦，即時比較價錢，幫你搵到最抵住宿優惠。",
    "en": "Discover the best hotel accommodations in this amazing city. We've curated recommendations from budget to luxury, with instant price comparisons to help you find the best deals."
}

MAIN_AFFILIATE_URL = f"https://tw.trip.com/hotels/list?city=58&display=%E9%A6%99%E6%B8%AF&optionId=58&optionType=City&optionName=%E9%A6%99%E6%B8%AF&Allianceid={ALLIANCE_ID}&SID={SID}&trip_sub1=&trip_sub3={TRIP_SUB3}"

def get_affiliate_url(city_id=None, city_name=None):
    """All pages link to the same Trip.com affiliate URL - the site has global search built in"""
    return MAIN_AFFILIATE_URL

def get_desc(en_name, lang):
    if en_name in CITY_DESCRIPTIONS:
        return CITY_DESCRIPTIONS[en_name][lang]
    return DEFAULT_DESC[lang]

def generate_hotel_cards(city_en_name, aff_url, is_zh):
    """Generate hotel listing cards for a city"""
    hotels = HOTELS.get(city_en_name, [])
    if not hotels:
        return ""

    title = "精選酒店推薦" if is_zh else "Featured Hotels"
    cards_html = f'<div class="info-section"><h2>{title}</h2>\n'

    for i, h in enumerate(hotels):
        name_zh, name_en, stars, dist_zh, dist_en, rating, reviews, price_hkd, tags_zh, tags_en, img = h
        name = name_zh if is_zh else name_en
        dist = dist_zh if is_zh else dist_en
        tags = tags_zh.split(",") if is_zh else tags_en.split(",")
        star_str = "★" * stars
        star_label = f"{stars}星級酒店" if is_zh else f"{stars}-Star Hotel"

        rating_label = ""
        if rating >= 9.0:
            rating_label = "卓越" if is_zh else "Excellent"
        elif rating >= 8.5:
            rating_label = "極好" if is_zh else "Very Good"
        elif rating >= 8.0:
            rating_label = "好" if is_zh else "Good"
        else:
            rating_label = "不錯" if is_zh else "Fair"

        reviews_text = f"{rating_label} · {reviews:,}{'則評價' if is_zh else ' reviews'}"
        price_label = "每晚低至" if is_zh else "From"
        per_night = "/ 每晚" if is_zh else "/ night"
        book_text = "Trip.com 格價" if is_zh else "Compare on Trip.com"

        badge_html = ""
        if i == 0:
            badge_html = f'<div class="hotel-badge">{"TOP推薦" if is_zh else "TOP PICK"}</div>'
        elif rating >= 9.5:
            badge_html = f'<div class="hotel-badge">{"極佳評分" if is_zh else "TOP RATED"}</div>'

        tags_html = "".join(f'<span class="hotel-tag">{t.strip()}</span>' for t in tags[:4])

        cards_html += f"""
            <div class="hotel-card">
                <div class="hotel-img" style="background-image:url('{img}');">{badge_html}<div class="hotel-rank">#{i+1}</div></div>
                <div class="hotel-body">
                    <div class="hotel-name">{name}</div>
                    <div class="hotel-stars">{star_str} {star_label}</div>
                    <div class="hotel-loc">📍 {dist}</div>
                    <div class="hotel-tags">{tags_html}</div>
                    <div class="hotel-bottom">
                        <div>
                            <div class="hotel-rating"><span class="rating-score">{rating}</span><span class="rating-text">{reviews_text}</span></div>
                            <a href="{aff_url}" class="book-link" target="_blank" rel="noopener noreferrer nofollow">{book_text}</a>
                        </div>
                        <div class="hotel-price">
                            <div class="per">{price_label}</div>
                            <div class="amount">HK${price_hkd:,}</div>
                            <div class="per">{per_night}</div>
                        </div>
                    </div>
                </div>
            </div>"""

    cards_html += "\n</div>"
    return cards_html


def generate_city_page(city, lang="zh"):
    city_id, url_name, zh_name, en_name, country_zh, country_en, flag, region = city

    is_zh = lang == "zh"
    display_name = zh_name if is_zh else en_name
    country = country_zh if is_zh else country_en
    aff_url = get_affiliate_url(city_id, zh_name)
    desc = get_desc(en_name, lang)

    # Text translations
    t = {
        "title": f"{display_name}酒店住宿推介 | 2026年精選排行榜 - SpeedNet Travel" if is_zh else f"Best {en_name} Hotels {country_en} | 2026 Top Picks - SpeedNet Travel",
        "meta_desc": f"2026年{display_name}酒店住宿推介！精選{display_name}最受歡迎酒店，即時格價比較，低至半價優惠。" if is_zh else f"Best {en_name} hotels in 2026! Compare top-rated hotels with instant price comparison. Up to 50% off deals.",
        "h1": f"{flag} {display_name}酒店住宿推介｜2026年精選排行榜" if is_zh else f"{flag} Best Hotels in {en_name} | 2026 Top Picks",
        "subtitle": desc,
        "search_btn": "搜尋酒店" if is_zh else "Search Hotels",
        "book_btn": "Trip.com 格價" if is_zh else "Compare on Trip.com",
        "book_btn2": "立即預訂" if is_zh else "Book Now",
        "browse_all": f"瀏覽全部{display_name}酒店 →" if is_zh else f"Browse All {en_name} Hotels →",
        "other_cities": "其他熱門目的地" if is_zh else "Other Popular Destinations",
        "price_from": "每晚低至" if is_zh else "From",
        "per_night": "/ 每晚" if is_zh else "/ night",
        "home": "首頁" if is_zh else "Home",
        "travel": "旅遊酒店" if is_zh else "Travel Hotels",
        "lang_switch": "English" if is_zh else "中文",
        "lang_url": f"travel-{en_name.lower().replace(' ', '-')}-hotels-en.html" if is_zh else f"travel-{en_name.lower().replace(' ', '-')}-hotels.html",
        "disclaimer": "以上資料只供參考，實際價格以預訂平台為準。本頁面包含聯盟推廣連結，透過連結預訂我們可能獲得佣金，不影響你的價格。" if is_zh else "Information is for reference only. Actual prices are subject to the booking platform. This page contains affiliate links — booking through these links may earn us a commission at no extra cost to you.",
        "faq_title": f"{display_name}酒店常見問題" if is_zh else f"{en_name} Hotel FAQs",
    }

    # Generate FAQ
    if is_zh:
        faq_html = f"""
                <div class="faq-item">
                    <div class="faq-q">Q: {display_name}酒店幾錢一晚？</div>
                    <div class="faq-a">{display_name}酒店價錢視乎星級及地段，經濟型酒店約HK$200-500/晚，4星級約HK$500-1500/晚，5星級豪華酒店HK$1500以上。建議透過格價連結比較各平台價錢。</div>
                </div>
                <div class="faq-item">
                    <div class="faq-q">Q: {display_name}住邊區最方便？</div>
                    <div class="faq-a">建議選擇市中心或主要交通樞紐附近的酒店，方便前往各大景點。可透過我哋嘅格價連結查看各區酒店分佈及價錢。</div>
                </div>
                <div class="faq-item">
                    <div class="faq-q">Q: 幾時訂{display_name}酒店最平？</div>
                    <div class="faq-a">一般而言，提早2-4星期預訂可享早鳥優惠。避開當地公眾假期及旅遊旺季，平日入住通常比週末便宜20-40%。</div>
                </div>
                <div class="faq-item">
                    <div class="faq-q">Q: 預訂酒店可以免費取消嗎？</div>
                    <div class="faq-a">大部分酒店提供免費取消選項，一般可於入住前24-72小時免費取消。預訂時留意「免費取消」標籤，確保行程有彈性。</div>
                </div>"""
    else:
        faq_html = f"""
                <div class="faq-item">
                    <div class="faq-q">Q: How much do hotels in {en_name} cost per night?</div>
                    <div class="faq-a">Hotel prices in {en_name} vary by star rating and location. Budget hotels start from ~$30-70/night, 4-star from ~$70-200/night, and luxury 5-star hotels from $200+. Use our price comparison links for the best deals.</div>
                </div>
                <div class="faq-item">
                    <div class="faq-q">Q: What's the best area to stay in {en_name}?</div>
                    <div class="faq-a">We recommend staying near the city center or major transport hubs for easy access to attractions. Check our comparison links to see hotels by district and price range.</div>
                </div>
                <div class="faq-item">
                    <div class="faq-q">Q: When is the cheapest time to book {en_name} hotels?</div>
                    <div class="faq-a">Booking 2-4 weeks in advance typically offers early bird discounts. Avoid local holidays and peak seasons. Weekday stays are usually 20-40% cheaper than weekends.</div>
                </div>
                <div class="faq-item">
                    <div class="faq-q">Q: Can I get free cancellation?</div>
                    <div class="faq-a">Most hotels offer free cancellation options, typically up to 24-72 hours before check-in. Look for the 'Free Cancellation' tag when booking to ensure flexibility.</div>
                </div>"""

    # Generate other cities links (same region first, then others)
    other_cities_html = ""
    count = 0
    for c in CITIES:
        if c[3] == en_name:
            continue
        if count >= 12:
            break
        c_url = get_affiliate_url(c[0], c[2])
        c_display = c[2] if is_zh else c[3]
        other_cities_html += f'                    <a href="{c_url}" class="city-chip" target="_blank" rel="noopener noreferrer nofollow"><span class="flag">{c[6]}</span> {c_display}</a>\n'
        count += 1

    html = f"""<!DOCTYPE html>
<html lang="{"zh-Hant-HK" if is_zh else "en"}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t['title']}</title>
    <meta name="description" content="{t['meta_desc']}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://broadbandhk.com/pages/travel/travel-{en_name.lower().replace(' ', '-')}-hotels{'-en' if not is_zh else ''}.html">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{t['title']}">
    <meta property="og:description" content="{t['meta_desc']}">
    <meta property="og:locale" content="{"zh_HK" if is_zh else "en_US"}">
    <link rel="alternate" hreflang="zh" href="https://broadbandhk.com/pages/travel/travel-{en_name.lower().replace(' ', '-')}-hotels.html">
    <link rel="alternate" hreflang="en" href="https://broadbandhk.com/pages/travel/travel-{en_name.lower().replace(' ', '-')}-hotels-en.html">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "{t['title']}",
        "description": "{t['meta_desc']}",
        "inLanguage": "{"zh-HK" if is_zh else "en"}",
        "publisher": {{ "@type": "Organization", "name": "SpeedNet Travel" }}
    }}
    </script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #333; line-height: 1.6; background: #f5f6fa; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 20px; display: flex; align-items: center; justify-content: space-between; }}
        .header a {{ color: white; text-decoration: none; font-size: 1.3em; font-weight: bold; }}
        .header-nav a {{ color: rgba(255,255,255,0.85); text-decoration: none; margin-left: 15px; font-size: 0.9em; }}
        .header-nav a:hover {{ color: white; }}
        .lang-btn {{ background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 15px; }}
        .breadcrumb {{ background: white; padding: 10px 20px; border-bottom: 1px solid #e2e8f0; font-size: 0.85em; }}
        .breadcrumb a {{ color: #667eea; text-decoration: none; }}
        .hero {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: white; padding: 60px 20px 50px; text-align: center; }}
        .hero h1 {{ font-size: 2em; margin-bottom: 12px; }}
        .hero p {{ opacity: 0.85; font-size: 1em; max-width: 700px; margin: 0 auto 25px; line-height: 1.7; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 30px 20px; }}
        .cta-main {{ display: block; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 18px; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 1.2em; margin: 30px 0; box-shadow: 0 4px 15px rgba(102,126,234,0.4); transition: transform 0.2s, box-shadow 0.2s; }}
        .cta-main:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(102,126,234,0.5); }}
        .cta-secondary {{ display: inline-block; background: #003580; color: white; padding: 14px 30px; border-radius: 10px; text-decoration: none; font-weight: bold; font-size: 1em; margin: 10px 8px; }}
        .info-section {{ background: white; border-radius: 12px; padding: 28px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }}
        .info-section h2 {{ font-size: 1.3em; margin-bottom: 15px; border-left: 4px solid #667eea; padding-left: 12px; }}
        .info-section p {{ color: #555; font-size: 0.92em; line-height: 1.8; margin-bottom: 12px; }}
        .city-chips {{ display: flex; gap: 10px; flex-wrap: wrap; margin: 16px 0; }}
        .city-chip {{ display: inline-block; background: white; border: 1px solid #ddd; padding: 10px 18px; border-radius: 25px; text-decoration: none; color: #333; font-size: 0.88em; transition: all 0.2s; }}
        .city-chip:hover {{ border-color: #667eea; color: #667eea; background: #f0f0ff; }}
        .city-chip .flag {{ margin-right: 4px; }}
        .faq-item {{ border-bottom: 1px solid #f0f0f0; padding: 14px 0; }}
        .faq-item:last-child {{ border-bottom: none; }}
        .faq-q {{ font-weight: bold; color: #1a1a2e; margin-bottom: 4px; }}
        .faq-a {{ color: #666; font-size: 0.9em; }}
        .disclaimer {{ text-align: center; padding: 15px; color: #999; font-size: 0.78em; margin-top: 20px; }}
        .footer {{ background: #1a1a2e; color: #a0aec0; padding: 30px 20px; text-align: center; font-size: 0.85em; }}
        .footer a {{ color: #667eea; text-decoration: none; }}
        .stats {{ display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin: 20px 0; }}
        .stat {{ background: rgba(255,255,255,0.15); padding: 15px 25px; border-radius: 10px; text-align: center; }}
        .stat-num {{ font-size: 1.5em; font-weight: bold; color: #ffd700; }}
        .stat-label {{ font-size: 0.8em; opacity: 0.8; }}
        .hotel-card {{ background: white; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); margin-bottom: 16px; overflow: hidden; display: flex; transition: box-shadow 0.2s; }}
        .hotel-card:hover {{ box-shadow: 0 4px 20px rgba(0,0,0,0.12); }}
        .hotel-img {{ width: 240px; min-height: 180px; background-size: cover; background-position: center; position: relative; flex-shrink: 0; }}
        .hotel-rank {{ position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); color: #ffd700; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.8em; }}
        .hotel-badge {{ position: absolute; top: 10px; left: 10px; background: #ff4757; color: white; padding: 3px 10px; border-radius: 4px; font-size: 0.72em; font-weight: bold; }}
        .hotel-body {{ flex: 1; padding: 16px; display: flex; flex-direction: column; }}
        .hotel-name {{ font-size: 1.05em; font-weight: bold; color: #1a1a2e; margin-bottom: 2px; }}
        .hotel-stars {{ color: #ffc107; font-size: 0.8em; margin-bottom: 4px; }}
        .hotel-loc {{ color: #888; font-size: 0.82em; margin-bottom: 6px; }}
        .hotel-tags {{ display: flex; gap: 5px; flex-wrap: wrap; margin-bottom: 8px; }}
        .hotel-tag {{ background: #f0f0ff; color: #667eea; padding: 2px 8px; border-radius: 10px; font-size: 0.7em; }}
        .hotel-desc {{ color: #666; font-size: 0.82em; line-height: 1.5; flex: 1; }}
        .hotel-bottom {{ display: flex; justify-content: space-between; align-items: flex-end; margin-top: 8px; padding-top: 10px; border-top: 1px solid #f0f0f0; }}
        .hotel-rating {{ display: flex; align-items: center; gap: 6px; }}
        .rating-score {{ background: #667eea; color: white; padding: 3px 7px; border-radius: 5px; font-weight: bold; font-size: 0.82em; }}
        .rating-text {{ font-size: 0.72em; color: #888; }}
        .hotel-price .amount {{ font-size: 1.2em; font-weight: bold; color: #ff4757; }}
        .hotel-price .per {{ font-size: 0.68em; color: #888; }}
        .book-link {{ display: inline-block; background: #287DFA; color: white; padding: 6px 14px; border-radius: 6px; text-decoration: none; font-size: 0.78em; font-weight: bold; margin-top: 6px; }}
        .book-link:hover {{ opacity: 0.9; }}
        @media (max-width: 768px) {{ .hero h1 {{ font-size: 1.4em; }} .stats {{ gap: 10px; }} .stat {{ padding: 10px 15px; }} .hotel-card {{ flex-direction: column; }} .hotel-img {{ width: 100%; height: 180px; }} }}
    </style>
</head>
<body>
    <div class="header">
        <a href="https://broadbandhk.com/">SpeedNet Travel</a>
        <div class="header-nav">
            <a href="https://broadbandhk.com/pages/travel/index.html">{"全部目的地" if is_zh else "All Destinations"}</a>
            <a href="https://broadbandhk.com/pages/travel/{t['lang_url']}" class="lang-btn">{t['lang_switch']}</a>
        </div>
    </div>
    <div class="breadcrumb">
        <a href="https://broadbandhk.com/">{t['home']}</a> &gt;
        <a href="https://broadbandhk.com/pages/travel/index.html">{t['travel']}</a> &gt;
        <span>{display_name}</span>
    </div>
    <div class="hero">
        <h1>{t['h1']}</h1>
        <p>{t['subtitle']}</p>
        <div class="stats">
            <div class="stat"><div class="stat-num">{flag}</div><div class="stat-label">{country}</div></div>
            <div class="stat"><div class="stat-num">{"低至半價" if is_zh else "Up to 50% Off"}</div><div class="stat-label">{"限時優惠" if is_zh else "Limited Deals"}</div></div>
            <div class="stat"><div class="stat-num">{"免費取消" if is_zh else "Free Cancel"}</div><div class="stat-label">{"彈性預訂" if is_zh else "Flexible"}</div></div>
        </div>
    </div>
    <div class="container">
        <a href="{aff_url}" class="cta-main" target="_blank" rel="noopener noreferrer nofollow">{t['browse_all']}</a>

        {generate_hotel_cards(en_name, aff_url, is_zh)}

        <a href="{aff_url}" class="cta-main" style="margin-top:10px;" target="_blank" rel="noopener noreferrer nofollow">{"查看更多酒店優惠 →" if is_zh else "View More Hotel Deals →"}</a>

        <div class="info-section">
            <h2>{t['faq_title']}</h2>
            {faq_html}
        </div>

        <div class="info-section">
            <h2>{t['other_cities']}</h2>
            <div class="city-chips">
{other_cities_html}            </div>
        </div>
    </div>
    <div class="disclaimer">{t['disclaimer']}</div>
    <div class="footer">
        <p>&copy; 2026 SpeedNet Travel | <a href="https://broadbandhk.com/">broadbandhk.com</a></p>
    </div>
</body>
</html>"""
    return html


def generate_index_page(lang="zh"):
    is_zh = lang == "zh"

    t = {
        "title": "全球酒店住宿推介 | 即時格價比較 - SpeedNet Travel" if is_zh else "Worldwide Hotel Deals | Price Comparison - SpeedNet Travel",
        "h1": "全球酒店住宿推介" if is_zh else "Worldwide Hotel Deals",
        "subtitle": "涵蓋全球45+個熱門城市，即時比較酒店價錢，幫你搵到最抵住宿優惠。" if is_zh else "Compare hotel prices across 45+ popular cities worldwide. Find the best deals instantly.",
        "lang_switch": "English" if is_zh else "中文",
        "lang_url": "index-en.html" if is_zh else "index.html",
    }

    regions = {
        "asia": ("亞洲熱門城市" if is_zh else "Popular Cities in Asia", []),
        "middleeast": ("中東" if is_zh else "Middle East", []),
        "europe": ("歐洲熱門城市" if is_zh else "Popular Cities in Europe", []),
        "americas": ("美洲熱門城市" if is_zh else "Popular Cities in Americas", []),
        "oceania": ("大洋洲" if is_zh else "Oceania", []),
    }

    for city in CITIES:
        region = city[7]
        regions[region][1].append(city)

    sections_html = ""
    for region_key, (region_name, cities) in regions.items():
        if not cities:
            continue
        chips = ""
        for c in cities:
            page_name = f"travel-{c[3].lower().replace(' ', '-')}-hotels{'-en' if not is_zh else ''}.html"
            display = c[2] if is_zh else c[3]
            chips += f'                <a href="{page_name}" class="city-chip"><span class="flag">{c[6]}</span> {display}</a>\n'

        sections_html += f"""
        <div class="info-section">
            <h2>{region_name}</h2>
            <div class="city-chips">
{chips}            </div>
        </div>
"""

    html = f"""<!DOCTYPE html>
<html lang="{"zh-Hant-HK" if is_zh else "en"}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t['title']}</title>
    <meta name="description" content="{t['subtitle']}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://broadbandhk.com/pages/travel/{"index" if is_zh else "index-en"}.html">
    <link rel="alternate" hreflang="zh" href="https://broadbandhk.com/pages/travel/index.html">
    <link rel="alternate" hreflang="en" href="https://broadbandhk.com/pages/travel/index-en.html">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #333; line-height: 1.6; background: #f5f6fa; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 20px; display: flex; align-items: center; justify-content: space-between; }}
        .header a {{ color: white; text-decoration: none; font-size: 1.3em; font-weight: bold; }}
        .header-nav a {{ color: rgba(255,255,255,0.85); text-decoration: none; margin-left: 15px; font-size: 0.9em; }}
        .lang-btn {{ background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 15px; }}
        .hero {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: white; padding: 60px 20px; text-align: center; }}
        .hero h1 {{ font-size: 2.2em; margin-bottom: 12px; }}
        .hero p {{ opacity: 0.85; font-size: 1.05em; max-width: 600px; margin: 0 auto; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 30px 20px; }}
        .info-section {{ background: white; border-radius: 12px; padding: 28px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }}
        .info-section h2 {{ font-size: 1.3em; margin-bottom: 15px; border-left: 4px solid #667eea; padding-left: 12px; }}
        .city-chips {{ display: flex; gap: 10px; flex-wrap: wrap; }}
        .city-chip {{ display: inline-block; background: white; border: 1px solid #ddd; padding: 12px 20px; border-radius: 25px; text-decoration: none; color: #333; font-size: 0.92em; transition: all 0.2s; }}
        .city-chip:hover {{ border-color: #667eea; color: #667eea; background: #f0f0ff; transform: translateY(-2px); }}
        .city-chip .flag {{ margin-right: 6px; }}
        .footer {{ background: #1a1a2e; color: #a0aec0; padding: 30px 20px; text-align: center; font-size: 0.85em; margin-top: 30px; }}
        .footer a {{ color: #667eea; text-decoration: none; }}
        @media (max-width: 768px) {{ .hero h1 {{ font-size: 1.5em; }} }}
    </style>
</head>
<body>
    <div class="header">
        <a href="https://broadbandhk.com/">SpeedNet Travel</a>
        <div class="header-nav">
            <a href="https://broadbandhk.com/">{"寬頻比較" if is_zh else "Broadband"}</a>
            <a href="https://broadbandhk.com/pages/travel/{t['lang_url']}" class="lang-btn">{t['lang_switch']}</a>
        </div>
    </div>
    <div class="hero">
        <h1>{t['h1']}</h1>
        <p>{t['subtitle']}</p>
    </div>
    <div class="container">
{sections_html}
    </div>
    <div class="footer">
        <p>&copy; 2026 SpeedNet Travel | <a href="https://broadbandhk.com/">broadbandhk.com</a></p>
    </div>
</body>
</html>"""
    return html


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate index pages
    for lang in ["zh", "en"]:
        suffix = "" if lang == "zh" else "-en"
        filename = f"{OUTPUT_DIR}/index{suffix}.html"
        html = generate_index_page(lang)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Generated: {filename}")

    # Generate city pages
    for city in CITIES:
        en_name = city[3]
        slug = en_name.lower().replace(" ", "-")

        for lang in ["zh", "en"]:
            suffix = "" if lang == "zh" else "-en"
            filename = f"{OUTPUT_DIR}/travel-{slug}-hotels{suffix}.html"
            html = generate_city_page(city, lang)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Generated: {filename}")

    total = 2 + len(CITIES) * 2
    print(f"\nDone! Generated {total} pages ({len(CITIES)} cities x 2 languages + 2 index pages)")


if __name__ == "__main__":
    main()
