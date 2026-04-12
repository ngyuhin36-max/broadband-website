"""Optimize pages/flights.html and pages/flights-en.html with:
- Trimmed keywords
- TravelAgency + TouristDestination (multi-destination) + BreadcrumbList + FAQPage schemas
- Additional geo meta
- hreflang already exists
"""
import re, json
from pathlib import Path

# Popular HK flight destinations with coords
DESTINATIONS = [
    ("Tokyo","東京",35.6762,139.6503,"JP","¥"),
    ("Osaka","大阪",34.6937,135.5023,"JP","¥"),
    ("Seoul","首爾",37.5665,126.9780,"KR","₩"),
    ("Bangkok","曼谷",13.7563,100.5018,"TH","฿"),
    ("Taipei","台北",25.0330,121.5654,"TW","NT$"),
    ("Singapore","新加坡",1.3521,103.8198,"SG","S$"),
    ("London","倫敦",51.5074,-0.1278,"GB","£"),
    ("New York","紐約",40.7128,-74.0060,"US","$"),
    ("Okinawa","沖繩",26.3344,127.8056,"JP","¥"),
    ("Fukuoka","福岡",33.5904,130.4017,"JP","¥"),
    ("Busan","釜山",35.1796,129.0756,"KR","₩"),
    ("Bali","峇里島",-8.3405,115.0920,"ID","Rp"),
    ("Paris","巴黎",48.8566,2.3522,"FR","€"),
    ("Ho Chi Minh City","胡志明市",10.8231,106.6297,"VN","₫"),
    ("Shanghai","上海",31.2304,121.4737,"CN","¥"),
]

def jdump(d): return json.dumps(d, ensure_ascii=False)

def build_schemas(is_zh):
    url = "https://broadbandhk.com/pages/flights.html" if is_zh else "https://broadbandhk.com/pages/flights-en.html"
    alt_url = "https://broadbandhk.com/pages/flights-en.html" if is_zh else "https://broadbandhk.com/pages/flights.html"
    name = "香港機票格價比較" if is_zh else "Hong Kong Flight Price Comparison"
    desc = "2026 香港出發機票格價比較，640+ 航空公司即時比較" if is_zh else "2026 Hong Kong flight price comparison — 640+ airlines instant comparison"

    travel = {
        "@context":"https://schema.org","@type":"TravelAgency",
        "name":name,"description":desc,"url":url,
        "image":"https://broadbandhk.com/og-image.png",
        "priceRange":"HK$880 - HK$25,000+",
        "address":{"@type":"PostalAddress","addressLocality":"Hong Kong","addressCountry":"HK"},
        "geo":{"@type":"GeoCoordinates","latitude":22.3193,"longitude":114.1694},
        "hasMap":"https://www.google.com/maps/place/Hong+Kong+International+Airport",
        "areaServed":[
            {"@type":"City","name":(zh if is_zh else en),
             "geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lng}}
            for en,zh,lat,lng,cc,cur in DESTINATIONS
        ],
        "knowsAbout":[
            ("香港機票" if is_zh else "Hong Kong flights"),
            ("廉航" if is_zh else "Budget airlines"),
            ("國泰航空" if is_zh else "Cathay Pacific"),
            ("HK Express"),("樂桃航空" if is_zh else "Peach Aviation"),
        ]
    }

    breadcrumb = {
        "@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"首頁" if is_zh else "Home","item":"https://broadbandhk.com/"},
            {"@type":"ListItem","position":2,"name":"機票格價" if is_zh else "Flight Deals","item":url}
        ]}

    # FAQ - long-tail flight queries
    faq_zh = [
        ("香港飛日本機票最平幾多錢？","廉航(HK Express/樂桃/Jetstar)東京來回低至 HK$1,280；大阪 HK$1,180；沖繩 HK$1,080；福岡 HK$1,280。黃金週/櫻花季(3-4月)/楓葉季(10-11月)加價 40-80%。淡季(6月/11月/2月)最抵。"),
        ("香港機票幾時買最平？","3-5 月、10-11 月為平價期。平機票 tips：1) 提早 6-12 週訂；2) 星期二、三、四出發；3) 紅眼航班／早機較平；4) 用無痕模式搜尋；5) Google Flights／Skyscanner／Trip.com 多平台格價。"),
        ("HK Express 行李收費幾多錢？","手提行李 7kg 免費；寄艙行李 20kg 約 HK$180-280、25kg HK$230-350、30kg HK$280-420。網上預訂比機場付款平 30-50%。"),
        ("直航 vs 轉機邊個抵？","直航快但貴；轉機平 20-50%。短程 3-5 小時建議直航；長程 8+ 小時（歐洲／美洲）轉機可慳 HK$2,000-5,000。留意至少 2 小時轉機時間。"),
        ("國泰 vs HK Express 點揀？","國泰：全服務、行李／餐／選位包含、可改期。HK Express：廉航、低票價但附加費多、行李改期另收。短程（日本/韓國/台灣）揀 HK Express 慳錢；長程（歐美）揀國泰舒適。"),
        ("香港飛歐洲最抵邊條航線？","轉機最平：卡塔爾航空（杜哈轉機）、阿聯酋（杜拜）、泰航（曼谷）。直航：國泰／維珍。巴黎／倫敦來回 HK$4,500-8,000（轉機），直航加 HK$2,000-3,000。"),
        ("紅眼航班值得搭嗎？","紅眼（深夜出發）比日間平 20-40%。優點：多一日玩、機場人少、過關快。缺點：瞓唔夠、的士貴。適合短程（日本/韓國/台灣）。長程建議日間出發。"),
        ("機票同住宿一齊訂會唔會平啲？","Trip.com／Klook／Expedia 嘅「機票+酒店套票」可慳 15-25%。適合行程靈活 + 住 3-4 星酒店嘅旅客。豪華酒店（5 星）分開訂通常更抵。"),
        ("櫻花季日本機票點樣搶？","2026 櫻花季（3月下旬-4月初）最熱門。建議：1) 9 月前開始睇；2) 訂 JAL/ANA/國泰直航；3) 避開京都奈良黃金週；4) 福岡／沖繩較平。建議 6 個月前鎖票。"),
        ("機票改期／退票政策？","廉航（HK Express/樂桃）：通常唔可以退，改期收 HK$300-800+差價。國泰/JAL 等全服務：Economy Flex 可退改（加 HK$2,000-5,000）。建議買旅遊保險保障。"),
    ]
    faq_en = [
        ("What's the cheapest Hong Kong to Japan flight in 2026?","Budget (HK Express/Peach/Jetstar): Tokyo return from HK$1,280; Osaka HK$1,180; Okinawa HK$1,080; Fukuoka HK$1,280. Peak (Golden Week / cherry blossom Mar-Apr / autumn leaves Oct-Nov) adds 40-80%. Off-peak (Jun/Nov/Feb) is cheapest."),
        ("When is the best time to book a Hong Kong flight?","Mar-May and Oct-Nov typically cheapest. Tips: 1) Book 6-12 weeks ahead; 2) Tue/Wed/Thu departures; 3) Red-eye / early-morning flights; 4) Use incognito mode; 5) Compare Google Flights / Skyscanner / Trip.com."),
        ("How much are HK Express baggage fees?","Cabin 7kg free. Checked 20kg approx HK$180-280, 25kg HK$230-350, 30kg HK$280-420. Pre-booking online saves 30-50% vs airport counter."),
        ("Direct flight vs connecting — which is better?","Direct is faster but pricier; connecting can save 20-50%. For 3-5h short-haul go direct. Long-haul 8+h (Europe/Americas) connecting saves HK$2,000-5,000. Allow 2+h layover."),
        ("Cathay Pacific vs HK Express — which to choose?","Cathay: full-service, baggage/meal/seat included, flexible changes. HK Express: budget, low fares but many add-ons. Short-haul (JP/KR/TW) go HK Express to save; long-haul (EU/US) go Cathay for comfort."),
        ("Cheapest HK to Europe route?","Connecting cheapest: Qatar (Doha), Emirates (Dubai), Thai Air (Bangkok). Direct: Cathay / Virgin. Paris/London return HK$4,500-8,000 connecting; +HK$2,000-3,000 for direct."),
        ("Are red-eye flights worth it?","Red-eyes (late-night) save 20-40% vs daytime. Pros: extra day to explore, empty airport, fast immigration. Cons: less sleep, pricier taxi. Good for short-haul (JP/KR/TW); long-haul prefer daytime."),
        ("Is a flight + hotel bundle cheaper?","Trip.com / Klook / Expedia bundles save 15-25%. Best for flexible itinerary + 3-4 star hotels. Luxury (5-star) hotels: usually cheaper booked separately."),
        ("How do I book cherry-blossom-season flights to Japan?","2026 sakura season (late Mar - early Apr) is peak. Tips: 1) Start watching Sep onwards; 2) Book JAL/ANA/Cathay direct; 3) Avoid Kyoto/Nara during Golden Week; 4) Fukuoka/Okinawa cheaper. Lock in 6 months ahead."),
        ("Flight change / refund policy?","Budget (HK Express/Peach): usually non-refundable; change fee HK$300-800 + fare difference. Full-service (Cathay/JAL) Economy Flex: refundable/changeable for HK$2,000-5,000 extra. Always buy travel insurance."),
    ]
    faq_items = faq_zh if is_zh else faq_en
    faq = {
        "@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
            for q,a in faq_items
        ]}

    dest = {
        "@context":"https://schema.org","@type":"TouristDestination",
        "name":"Hong Kong International Airport" if not is_zh else "香港國際機場",
        "url":url,
        "geo":{"@type":"GeoCoordinates","latitude":22.3080,"longitude":113.9185},
        "includesAttraction":[
            {"@type":"Place","name":(zh if is_zh else en),
             "geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lng}}
            for en,zh,lat,lng,cc,cur in DESTINATIONS
        ],
        "touristType":["Business","Family","Couple","Backpacker","Solo"] if not is_zh else ["商務","親子","情侶","背包客","單人旅遊"]
    }
    return travel, breadcrumb, faq, dest

for lang, path in [("zh","pages/flights.html"),("en","pages/flights-en.html")]:
    is_zh = lang == "zh"
    p = Path(path); s = p.read_text(encoding="utf-8")

    # Trim keywords
    if is_zh:
        new_kw = "香港機票格價,平機票,機票格價2026,香港飛東京,香港飛大阪,香港飛首爾,香港飛曼谷,香港飛台北,香港飛新加坡,香港飛倫敦,香港飛紐約,國泰航空,HK Express,樂桃航空,香港快運,廉航機票,廉航行李費,紅眼航班,直航,轉機,機票幾時買,買平機票秘技,櫻花機票,楓葉季機票,蜜月機票,親子機票,HK to Tokyo,HK to Osaka,Cathay Pacific,HK Express deals"
    else:
        new_kw = "Hong Kong flight deals 2026,cheap flights Hong Kong,HK to Tokyo flights,HK to Osaka flights,HK to Seoul flights,HK to Bangkok flights,HK to Taipei flights,HK to Singapore flights,HK to London flights,HK to New York flights,Cathay Pacific deals,HK Express deals,HK Express baggage fees,Peach Aviation,budget airline Hong Kong,red eye flights,cherry blossom flights,when to book flights HK,connecting flights cheap,direct flights Hong Kong,Hong Kong airport,HKIA flights,family travel flights,honeymoon flights Hong Kong"
    s = re.sub(r'<meta name="keywords" content="[^"]+">',
               f'<meta name="keywords" content="{new_kw}">', s, count=1)

    # Add GEO meta (if not already present)
    extra = (
        '    <meta name="geo.country" content="HK">\n'
        '    <meta name="DC.coverage.spatial" content="Hong Kong International Airport (HKG)">\n'
        '    <meta name="timezone" content="Asia/Hong_Kong">\n'
        '    <meta name="distribution" content="global">\n'
    )
    if 'name="geo.country"' not in s:
        s = re.sub(r'(<meta name="ICBM"[^>]+>\n)',
                   lambda m: m.group(1) + extra, s, count=1)

    # Add new schemas before <style>
    travel, breadcrumb, faq, dest = build_schemas(is_zh)
    new_blocks = (
        f'    <script type="application/ld+json">{jdump(travel)}</script>\n'
        f'    <script type="application/ld+json">{jdump(breadcrumb)}</script>\n'
        f'    <script type="application/ld+json">{jdump(faq)}</script>\n'
        f'    <script type="application/ld+json">{jdump(dest)}</script>\n'
    )
    s = re.sub(r'(\s*<style>)', r'\n' + new_blocks + r'\1', s, count=1)

    p.write_text(s, encoding="utf-8")
    print(f"optimized {path}")
    print(f"  schemas:", s.count('"@context"'), "hreflang:", s.count('hreflang='))
