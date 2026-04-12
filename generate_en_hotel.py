"""
Generate English version of HKhotel.html → HKhotel-en.html
Translates all Chinese text while keeping structure, CSS, and affiliate links intact.
"""

with open("C:/Users/tonyng/Desktop/Claude_Code/BROADBANDHK/pages/HKhotel.html", "r", encoding="utf-8") as f:
    html = f.read()

# --- HEAD section ---
html = html.replace('lang="zh-Hant-HK"', 'lang="en"', 1)

html = html.replace(
    '<title>香港酒店推介2026｜451間酒店格價比較．半島酒店／W Hotel／喜來登．尖沙咀銅鑼灣旺角</title>',
    '<title>Hong Kong Hotels 2026 | 451 Hotels Price Comparison · Peninsula · W Hotel · Sheraton · Tsim Sha Tsui</title>'
)

html = html.replace(
    'content="2026年香港酒店格價比較！451間酒店即時格價：半島酒店HK$3,280起、W Hotel HK$1,880起、喜來登HK$1,582起。尖沙咀、銅鑼灣、灣仔、旺角全區覆蓋。Staycation親子海景酒店一覽。"',
    'content="2026 Hong Kong hotel price comparison! 451 hotels: The Peninsula from HK$3,280, W Hotel from HK$1,880, Sheraton from HK$1,582. Tsim Sha Tsui, Causeway Bay, Wan Chai, Mongkok. Staycation, family &amp; harbour view hotels."'
)

html = html.replace('HKhotel.html', 'HKhotel-en.html')

# Keep one reference to the Chinese version for hreflang
html = html.replace(
    'hreflang="zh-Hant-HK" href="https://broadbandhk.com/pages/HKhotel-en.html"',
    'hreflang="zh-Hant-HK" href="https://broadbandhk.com/pages/HKhotel.html"'
)
html = html.replace(
    'hreflang="x-default" href="https://broadbandhk.com/pages/HKhotel-en.html"',
    'hreflang="en" href="https://broadbandhk.com/pages/HKhotel-en.html"'
)

html = html.replace('"inLanguage": "zh-HK"', '"inLanguage": "en"')
html = html.replace('"og:locale" content="zh_HK"', '"og:locale" content="en_US"')

# --- Navigation ---
translations = [
    ('SpeedNet Travel', 'SpeedNet Travel'),
    ('寬頻比較', 'Broadband'),
    ('酒店優惠', 'Hotel Deals'),
    ('首頁', 'Home'),
    ('旅遊酒店', 'Travel Hotels'),
    ('香港酒店推介', 'Hong Kong Hotels'),

    # Hero
    ('香港酒店住宿推介｜2026年精選排行榜', 'Best Hong Kong Hotels 2026 | Top Picks & Price Comparison'),
    ('我們精選了香港最受歡迎的酒店住宿，即時比較多個平台價錢，幫你搵到最抵住宿優惠。', 'We\'ve curated Hong Kong\'s most popular hotels with instant price comparison across platforms to help you find the best deals.'),
    ('間酒店', ' Hotels'),
    ('個格價平台', ' Booking Platforms'),
    ('限時優惠', 'Limited Deals'),
    ('搜尋酒店', 'Search Hotels'),

    # Sort bar
    ('間香港酒店（38間精選 + 413間目錄）', ' Hong Kong Hotels (38 Featured + 413 Directory)'),
    ('推薦排序', 'Recommended'),
    ('評分最高', 'Highest Rated'),
    ('價錢最低', 'Lowest Price'),
    ('最受歡迎', 'Most Popular'),

    # Hotel card labels
    ('5星級酒店', '5-Star Hotel'),
    ('4星級酒店', '4-Star Hotel'),
    ('3星級酒店', '3-Star Hotel'),
    ('2星級酒店', '2-Star Hotel'),
    ('每晚低至', 'From'),
    ('/ 每晚', '/ night'),
    ('Trip.com 格價', 'Compare on Trip.com'),
    ('立即預訂', 'Book Now'),
    ('卓越', 'Excellent'),
    ('極好', 'Very Good'),
    ('好', 'Good'),
    ('則評價', ' reviews'),

    # Badges
    ('TOP 推薦', 'TOP PICK'),
    ('潮人至愛', 'TRENDY'),
    ('性價比高', 'GREAT VALUE'),
    ('超值之選', 'BUDGET PICK'),
    ('Staycation', 'Staycation'),
    ('人氣之選', 'POPULAR'),
    ('新酒店', 'NEW'),
    ('高評分', 'TOP RATED'),
    ('海景推薦', 'SEA VIEW'),
    ('機場首選', 'AIRPORT'),
    ('極佳評分', 'TOP RATED'),
    ('旺角地標', 'MONGKOK'),
    ('維港海景', 'HARBOUR VIEW'),
    ('迪士尼', 'DISNEY'),
    ('超值', 'VALUE'),

    # Sidebar
    ('星級分佈', 'Star Rating'),
    ('住宿主題', 'Hotel Features'),
    ('熱門地區', 'Popular Areas'),
    ('游泳池', 'Swimming Pool'),
    ('親子住宿', 'Family Friendly'),
    ('五星奢華', '5-Star Luxury'),
    ('浴缸房', 'Bathtub Room'),
    ('健身室', 'Fitness Centre'),
    ('停車場', 'Parking'),
    ('全新開幕', 'Newly Opened'),
    ('海景房', 'Sea View'),
    ('尖沙咀', 'Tsim Sha Tsui'),
    ('銅鑼灣', 'Causeway Bay'),
    ('旺角', 'Mongkok'),
    ('中環', 'Central'),
    ('西九龍', 'West Kowloon'),
    ('大嶼山', 'Lantau Island'),

    # Trip.com Hotel Directory Table
    ('更多香港酒店（Trip.com 全部酒店目錄）', 'More Hong Kong Hotels (Full Trip.com Directory)'),
    ('以下酒店全部可在 Trip.com 預訂，點擊即可查看詳情及最新價格。', 'All hotels below are available on Trip.com. Click to view details and latest prices.'),
    ('酒店名稱', 'Hotel Name'),
    ('優惠價', 'Deal Price'),
    ('原價', 'Original'),
    ('預訂', 'Book'),
    ('格價', 'Compare'),
    ('* 價格僅供參考，實際價格視乎入住日期。點擊「格價」查看 Trip.com 最新優惠。', '* Prices are for reference only. Click "Compare" for the latest Trip.com deals.'),

    # Area Guide
    ('香港酒店地區攻略', 'Hong Kong Hotel Area Guide'),
    ('尖沙咀 — 旅客首選地段', 'Tsim Sha Tsui — Top Choice for Tourists'),
    ('銅鑼灣 — 購物天堂', 'Causeway Bay — Shopping Paradise'),
    ('灣仔 — 商務與美食集中地', 'Wan Chai — Business & Food Hub'),
    ('旺角 — 最地道的香港體驗', 'Mongkok — Authentic Hong Kong Experience'),
    ('荃灣 — 大房間高CP值', 'Tsuen Wan — Spacious Rooms, Great Value'),
    ('西九龍 — 新興高端區域', 'West Kowloon — Emerging Luxury District'),
    ('機場及大嶼山 — 轉機及度假', 'Airport & Lantau — Transit & Resort'),

    # Price table
    ('香港酒店價錢一覽表', 'Hong Kong Hotel Price Overview'),
    ('地區', 'Area'),
    ('推薦程度', 'Rating'),
    ('機場/大嶼山', 'Airport/Lantau'),
    ('* 價錢僅供參考，實際價格視乎入住日期及房型。建議點擊「Trip.com 格價」查看最新優惠。', '* Prices are for reference only. Click "Compare on Trip.com" for the latest deals.'),

    # Other cities
    ('其他熱門目的地', 'Other Popular Destinations'),
    ('東京酒店', 'Tokyo Hotels'),
    ('大阪酒店', 'Osaka Hotels'),
    ('京都酒店', 'Kyoto Hotels'),
    ('首爾酒店', 'Seoul Hotels'),
    ('曼谷酒店', 'Bangkok Hotels'),
    ('台北酒店', 'Taipei Hotels'),
    ('釜山酒店', 'Busan Hotels'),
    ('布吉酒店', 'Phuket Hotels'),

    # FAQ General
    ('香港酒店住宿常見問題', 'Hong Kong Hotel FAQs'),
    ('Q: 香港酒店邊區最抵住？', 'Q: Which area has the cheapest hotels in Hong Kong?'),
    ('旺角及佐敦一帶酒店性價比最高，3星酒店每晚HK$298起。尖沙咀及銅鑼灣價錢較高但位置便利，適合購物觀光。大嶼山及愉景灣適合Staycation度假。', 'Mongkok and Jordan offer the best value, with 3-star hotels from HK$298/night. Tsim Sha Tsui and Causeway Bay are pricier but more convenient for shopping. Lantau and Discovery Bay are ideal for staycations.'),
    ('Q: 香港Staycation邊間酒店最推薦？', 'Q: Which hotels are best for a Hong Kong staycation?'),
    ('親子推薦愉景灣酒店（有沙灘泳池）、情侶推薦W Hotel（天台泳池超靚）、奢華體驗推薦半島酒店。留意平日入住可慳高達40%。', 'For families: Auberge Discovery Bay (beach & pool). For couples: W Hotel (stunning rooftop pool). For luxury: The Peninsula. Weekday stays can save up to 40%.'),
    ('Q: 幾時訂香港酒店最平？', 'Q: When is the cheapest time to book Hong Kong hotels?'),
    ('一般而言，週二至四入住最平，週五六日及公眾假期最貴。提早2-3星期預訂通常有早鳥優惠。另外，每年1月及9月係淡季，酒店價錢相對較低。', 'Tuesday to Thursday stays are cheapest. Book 2-3 weeks early for early bird discounts. January and September are low season with lower prices.'),
    ('Q: 點樣比較唔同平台嘅酒店價錢？', 'Q: How to compare hotel prices across platforms?'),
    ('我哋已幫你整合Trip.com等主要平台嘅價錢。每間酒店都提供格價連結，一click即可比較，搵到最抵價格先預訂。', 'We\'ve integrated prices from Trip.com and other major platforms. Each hotel has a price comparison link — one click to compare and find the best deal.'),
    ('Q: 預訂酒店可以免費取消嗎？', 'Q: Can I get free cancellation on hotel bookings?'),
    ('大部分酒店提供免費取消選項，一般可於入住前24-72小時免費取消。預訂時留意「免費取消」標籤，確保行程有彈性。建議選擇有免費取消政策的房型。', 'Most hotels offer free cancellation, typically 24-72 hours before check-in. Look for the "Free Cancellation" tag when booking to ensure flexibility.'),

    # FAQ Hotel-specific
    ('熱門酒店格價問題', 'Popular Hotel Price FAQs'),
    ('Q: 香港半島酒店（The Peninsula）幾錢一晚？', 'Q: How much is The Peninsula Hong Kong per night?'),
    ('Q: 香港W酒店（W Hong Kong）住宿體驗如何？', 'Q: What\'s the W Hong Kong hotel experience like?'),
    ('Q: 香港麗思卡爾頓酒店（The Ritz-Carlton）值得住嗎？', 'Q: Is The Ritz-Carlton Hong Kong worth it?'),
    ('Q: 香港喜來登酒店（Sheraton Hong Kong）位置方便嗎？', 'Q: Is the Sheraton Hong Kong conveniently located?'),
    ('Q: 香港四季酒店（Four Seasons）同半島酒店邊間好？', 'Q: Four Seasons vs Peninsula Hong Kong — which is better?'),
    ('Q: 香港迪士尼樂園酒店同好萊塢飯店邊間抵？', 'Q: Disney\'s Hong Kong hotel vs Hollywood Hotel — which is cheaper?'),
    ('Q: 荃灣西如心酒店（Nina Hotel）性價比高嗎？', 'Q: Is Nina Hotel Tsuen Wan West good value?'),
    ('Q: 香港帝京酒店（Royal Plaza Hotel）在旺角邊度？', 'Q: Where is the Royal Plaza Hotel in Mongkok?'),
    ('Q: 香港機場附近有咩酒店推薦？', 'Q: Which hotels near Hong Kong Airport are recommended?'),
    ('Q: 香港維港海景酒店有邊幾間？', 'Q: Which Hong Kong hotels have Victoria Harbour views?'),

    # Footer
    ('以上資料只供參考，實際價格以預訂平台為準。本頁面包含聯盟推廣連結，透過連結預訂我們可能獲得佣金，不影響你的價格。', 'Information is for reference only. Actual prices are subject to the booking platform. This page contains affiliate links — booking through these links may earn us a commission at no extra cost to you.'),
    ('想知更多旅遊優惠？', 'Want more travel deals?'),
    ('WhatsApp 我哋，幫你搵最抵酒店同旅遊套票！', 'WhatsApp us for the best hotel and travel package deals!'),
    ('WhatsApp 查詢旅遊優惠', 'WhatsApp for Travel Deals'),
    ('全部目的地', 'All Destinations'),
]

for zh, en in translations:
    html = html.replace(zh, en)

# Write output
with open("C:/Users/tonyng/Desktop/Claude_Code/BROADBANDHK/pages/HKhotel-en.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Generated HKhotel-en.html successfully!")
