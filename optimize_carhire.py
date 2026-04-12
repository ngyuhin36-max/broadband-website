"""Optimize pages/carhire.html + pages/carhire-en.html SEO/GEO."""
import re, json
from pathlib import Path

# Popular HK self-drive destinations (country + coords + en/zh)
DESTS = [
    ("Okinawa","沖繩",26.3344,127.8056,"JP"),
    ("Osaka","大阪",34.6937,135.5023,"JP"),
    ("Hokkaido","北海道",43.0618,141.3545,"JP"),
    ("Tokyo","東京",35.6762,139.6503,"JP"),
    ("Fukuoka","福岡",33.5904,130.4017,"JP"),
    ("Jeju","濟州島",33.4890,126.4983,"KR"),
    ("Seoul","首爾",37.5665,126.9780,"KR"),
    ("Taipei","台北",25.0330,121.5654,"TW"),
    ("Kaohsiung","高雄",22.6273,120.3014,"TW"),
    ("Hualien","花蓮",23.9871,121.6014,"TW"),
    ("Bangkok","曼谷",13.7563,100.5018,"TH"),
    ("Los Angeles","洛杉磯",34.0522,-118.2437,"US"),
    ("California","加州",36.7783,-119.4179,"US"),
    ("Iceland","冰島",64.9631,-19.0208,"IS"),
    ("Australia","澳洲",-25.2744,133.7751,"AU"),
]

def jdump(d): return json.dumps(d, ensure_ascii=False)

def build(is_zh):
    url = "https://broadbandhk.com/pages/carhire.html" if is_zh else "https://broadbandhk.com/pages/carhire-en.html"
    alt = "https://broadbandhk.com/pages/carhire-en.html" if is_zh else "https://broadbandhk.com/pages/carhire.html"
    name = "香港人全球租車格價比較" if is_zh else "Global Car Rental Price Comparison from Hong Kong"
    desc = "2026 全球 200+ 國家自駕遊即時租車格價比較" if is_zh else "2026 Instant car rental price comparison across 200+ countries"

    travel = {
        "@context":"https://schema.org","@type":"AutoRental",
        "name":name,"description":desc,"url":url,
        "image":"https://broadbandhk.com/og-image.png",
        "priceRange":"HK$145 - HK$800+",
        "address":{"@type":"PostalAddress","addressLocality":"Hong Kong","addressCountry":"HK"},
        "geo":{"@type":"GeoCoordinates","latitude":22.3193,"longitude":114.1694},
        "hasMap":"https://www.google.com/maps/place/Hong+Kong",
        "areaServed":[
            {"@type":"Place","name":(zh if is_zh else en),
             "geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lng}}
            for en,zh,lat,lng,cc in DESTS
        ],
        "knowsAbout":(
            ["自駕遊","國際駕照","租車保險","Hertz","Avis","Budget","Times 租車","日本自駕"]
            if is_zh else
            ["Self-drive","International Driving Permit","Car rental insurance","Hertz","Avis","Budget","Times Car","Japan self-drive"]
        )
    }
    breadcrumb = {
        "@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"首頁" if is_zh else "Home","item":"https://broadbandhk.com/"},
            {"@type":"ListItem","position":2,"name":"全球租車" if is_zh else "Global Car Rental","item":url}
        ]}
    faqs_zh = [
        ("香港人去日本自駕要咩證件？","1) 香港駕駛執照（正本）；2) 國際駕駛許可證 IDP（運輸署申請 HK$80，10 日辦妥）；3) 護照。日本唔認香港駕照中文翻譯，必須要 IDP。韓國亦同。"),
        ("IDP 國際駕照點申請？","運輸署所有牌照事務處均可辦理。帶香港駕照正本、身份證、護照副本、1 張照片、HK$80 費用。可 24 小時內取證。有效期 1 年。網上預約 https://www.gov.hk/idp。"),
        ("租車保險點揀？全險還係基本？","基本：CDW 碰撞險（自負額 HK$3,000-10,000）。**強烈建議加 Super CDW / LDW 全險**（約每日 HK$80-150，自負額變 $0）。如果唔熟當地駕駛規則，絕對要買全險。信用卡自帶租車險覆蓋範圍有限。"),
        ("沖繩租車邊間最抵？","Times Car / Toyota Rent a Car / OTS 本地租車最抵（細車 HK$145-250/日）。建議機場取車／還車慳時間。Trip.com／Klook 平台經常有 10-20% 網上優惠。"),
        ("北海道冬天租車安全嗎？","12月-3月有雪，**必須揀四驅車（4WD）+ 冬季輪胎（Snow Tire）**，加價約 HK$50-100/日。新手建議避冬季或跟團。可先喺札幌／函館市內試開，再上高速公路。"),
        ("租車油費計算：滿油還還是預付？","**建議「滿油取車滿油還車」**（Full to Full）。預付油費（Pre-paid）表面平但實際平均貴 20-30%，因為還車剩嘅油冇得退。留意 ETC 電子收費卡另計費用。"),
        ("日本 ETC 卡點搞？","部分租車公司 ETC 卡免費借、通行費月尾結算（日圓）。租車時主動要求「ETC カード」。高速公路通行費可慳時間（唔使排隊人手收費）。"),
        ("租車可以異地還車嗎？","**甲借乙還（One-way Rental）**可以，但通常加異地還車費 HK$200-800。日本本島內一般 HK$300-500；跨島（九州→北海道）不行。Trip.com／Klook 可以篩選異地還車選項。"),
        ("新手第一次海外自駕應該揀邊度？","推薦順序：**台灣（左軚、中文路牌、駕駛習慣相近）> 日本沖繩（小島、少高速）> 日本大阪／京都 > 韓國濟州島 > 北海道**。美國／歐洲建議有經驗後再嘗試。"),
        ("租車邊個平台格價最好？","建議同時開 3 個：1) **Trip.com**（新用戶常有 8-15% off）；2) **Klook**（經常有 Staycation 套票）；3) **DiscoverCars**（歐美車型選擇多）。同一車同一日可差 20-40%。")
    ]
    faqs_en = [
        ("What documents do Hong Kong travellers need to drive in Japan?","1) HK driving licence (original); 2) International Driving Permit (IDP, apply at HK Transport Dept for HK$80, 10 days processing); 3) Passport. Japan doesn't accept the Chinese translation of HK licences — the IDP is mandatory. Same for Korea."),
        ("How do I apply for an IDP in Hong Kong?","Any HK Transport Department licensing office. Bring HK licence original, HKID, passport copy, 1 photo, HK$80. Issued within 24 hours, valid 1 year. Book online at https://www.gov.hk/idp."),
        ("Basic insurance or full cover?","Basic CDW (deductible HK$3,000-10,000). Strongly recommend upgrading to Super CDW / LDW full cover (~HK$80-150/day, deductible becomes $0). Credit card rental insurance has limited coverage — full cover is essential for unfamiliar traffic."),
        ("Cheapest car rental in Okinawa?","Times Car / Toyota Rent a Car / OTS local firms are cheapest (compact HK$145-250/day). Pick up / drop off at airport saves time. Trip.com / Klook platforms often offer 10-20% discounts."),
        ("Is it safe to drive in Hokkaido in winter?","Dec-Mar snow. 4WD + winter/snow tyres are essential (+HK$50-100/day). Newcomers should avoid winter or join a tour. Practice in Sapporo / Hakodate city first before highways."),
        ("Full-tank or prepaid fuel — which to pick?","Recommend Full to Full. Prepaid fuel looks cheaper but averages 20-30% more because unused fuel isn't refunded. ETC tolls are billed separately."),
        ("How does ETC work in Japan?","Some rental companies lend ETC cards free; toll charges settled monthly in JPY. Ask for 'ETC カード' at pickup. Saves time vs cash lanes on highways."),
        ("Can I do one-way rental?","Yes (One-way Rental) — usually HK$200-800 extra fee. Within Japan main island HK$300-500; cross-island (Kyushu→Hokkaido) often not allowed. Filter 'one-way' on Trip.com / Klook."),
        ("Best first-time self-drive destination for Hongkongers?","Recommended order: Taiwan (left-hand drive, Chinese signs, familiar habits) > Okinawa (small island, few highways) > Osaka/Kyoto > Jeju Island > Hokkaido. US/Europe — try after experience."),
        ("Which car rental platform is cheapest?","Open 3 tabs: 1) Trip.com (new user 8-15% off); 2) Klook (bundle deals); 3) DiscoverCars (wider US/EU options). Same car same day can vary 20-40%.")
    ]
    faq_items = faqs_zh if is_zh else faqs_en
    faq = {
        "@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq_items]
    }
    dest = {
        "@context":"https://schema.org","@type":"TouristDestination",
        "name":"Global Self-Drive Destinations" if not is_zh else "全球自駕遊目的地",
        "url":url,
        "geo":{"@type":"GeoCoordinates","latitude":22.3193,"longitude":114.1694},
        "includesAttraction":[
            {"@type":"Place","name":(zh if is_zh else en),
             "geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lng}}
            for en,zh,lat,lng,cc in DESTS
        ],
        "touristType":["Family","Couple","Honeymoon","Adventure","Backpacker"] if not is_zh else ["親子","情侶","蜜月","冒險","背包客"]
    }
    return travel, breadcrumb, faq, dest

for lang, path in [("zh","pages/carhire.html"),("en","pages/carhire-en.html")]:
    is_zh = lang == "zh"
    p = Path(path); s = p.read_text(encoding="utf-8")

    if is_zh:
        new_kw = "租車格價2026,自駕遊,日本租車,沖繩租車,大阪租車,北海道租車,北海道冬天租車,濟州島租車,台灣租車,冰島環島,Hertz,Avis,Budget,Times 租車,Toyota Rent a Car,國際駕照,IDP,租車保險,全險 CDW,日本 ETC,甲借乙還,異地還車,新手自駕,親子自駕遊,蜜月自駕,Trip.com 租車,加州1號公路"
    else:
        new_kw = "car rental 2026,self drive,Japan car rental,Okinawa car rental,Osaka car rental,Hokkaido car rental,Jeju car rental,Taiwan car rental,Iceland self drive,Hertz,Avis,Budget,Times Car,Toyota Rent a Car,international driving permit,IDP,car rental insurance,CDW full cover,ETC Japan,one way rental,first time self drive,family road trip,honeymoon road trip,Trip.com car rental,California Highway 1"
    s = re.sub(r'<meta name="keywords" content="[^"]+">',
               f'<meta name="keywords" content="{new_kw}">', s, count=1)

    extra = (
        '    <meta name="geo.country" content="HK">\n'
        '    <meta name="DC.coverage.spatial" content="Global (200+ countries)">\n'
        '    <meta name="timezone" content="Asia/Hong_Kong">\n'
        '    <meta name="distribution" content="global">\n'
    )
    if 'geo.country' not in s:
        s = re.sub(r'(<meta name="ICBM"[^>]+>\n)',
                   lambda m: m.group(1) + extra, s, count=1)

    travel, breadcrumb, faq, dest = build(is_zh)
    new_blocks = (
        f'    <script type="application/ld+json">{jdump(travel)}</script>\n'
        f'    <script type="application/ld+json">{jdump(breadcrumb)}</script>\n'
        f'    <script type="application/ld+json">{jdump(faq)}</script>\n'
        f'    <script type="application/ld+json">{jdump(dest)}</script>\n'
    )
    s = re.sub(r'(\s*<style>)', r'\n' + new_blocks + r'\1', s, count=1)

    p.write_text(s, encoding="utf-8")
    ctx = '"@context"'
    print(f"{path}: schemas={s.count(ctx)} hreflang={s.count('hreflang=')}")
