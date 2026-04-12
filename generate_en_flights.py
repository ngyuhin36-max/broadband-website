"""
Generate English version of flights.html → flights-en.html
"""

with open("C:/Users/tonyng/Desktop/Claude_Code/BROADBANDHK/pages/flights.html", "r", encoding="utf-8") as f:
    html = f.read()

# Language tag
html = html.replace('lang="zh-Hant-HK"', 'lang="en"', 1)

# URLs
html = html.replace('flights.html', 'flights-en.html')
html = html.replace('hreflang="zh-Hant-HK" href="https://broadbandhk.com/pages/flights-en.html"', 'hreflang="zh-Hant-HK" href="https://broadbandhk.com/pages/flights.html"')
html = html.replace('hreflang="x-default" href="https://broadbandhk.com/pages/flights-en.html"', 'hreflang="en" href="https://broadbandhk.com/pages/flights-en.html"')

# Meta
html = html.replace('"inLanguage": "zh-HK"', '"inLanguage": "en"')
html = html.replace('"og:locale" content="zh_HK"', '"og:locale" content="en_US"')
html = html.replace('"language" content="zh-Hant-HK"', '"language" content="en"')

translations = [
    # Title & Meta
    ('機票格價2026｜香港飛東京HK$1,280起．大阪．首爾．曼谷．國泰HK Express樂桃｜640+航空公司比較',
     'Flight Deals 2026 | Hong Kong to Tokyo HK$1,280 · Osaka · Seoul · Bangkok · Cathay Pacific HK Express | 640+ Airlines'),
    ('2026香港機票格價！東京來回HK$1,280起、大阪HK$1,180起、首爾HK$1,380起、曼谷HK$880起。國泰航空、HK Express、樂桃、日航640+航空公司即時比較。廉航行李費攻略、買平機票秘技一覽。',
     '2026 Hong Kong flight deals! Tokyo return HK$1,280, Osaka HK$1,180, Seoul HK$1,380, Bangkok HK$880. Compare 640+ airlines: Cathay Pacific, HK Express, Peach, JAL. Budget airline baggage fees &amp; cheap flight tips.'),
    ('香港出發：東京HK$1,280、大阪HK$1,180、首爾HK$1,380、曼谷HK$880起。國泰/HK Express/樂桃即時格價。',
     'From Hong Kong: Tokyo HK$1,280, Osaka HK$1,180, Seoul HK$1,380, Bangkok HK$880. Cathay/HK Express/Peach instant comparison.'),

    # Navigation
    ('寬頻比較', 'Broadband'),
    ('酒店格價', 'Hotels'),
    ('機票格價', 'Flights'),
    ('首頁', 'Home'),

    # Add language toggle
    ('<a href="https://broadbandhk.com/pages/flights-en.html" class="lang-btn">English</a>',
     '<a href="https://broadbandhk.com/pages/flights.html" class="lang-btn">中文</a>'),

    # Hero
    ('機票格價2026｜香港出發平機票', 'Flight Deals 2026 | Cheap Flights from Hong Kong'),
    ('比較640+航空公司機票價錢，覆蓋全球熱門航線。國泰、HK Express、樂桃、星宇、虎航即時格價，幫你搵到最平機票。',
     'Compare 640+ airlines covering all popular routes worldwide. Cathay Pacific, HK Express, Peach, STARLUX, Tigerair — find the cheapest flights instantly.'),
    ('航空公司', 'Airlines'),
    ('全球覆蓋', 'Worldwide'),
    ('國家', 'Countries'),
    ('即時格價', 'Live Prices'),
    ('含稅總價', 'Tax Included'),

    # CTA
    ('搜尋全球機票 →', 'Search All Flights →'),
    ('搜尋更多航線機票 →', 'Search More Flight Routes →'),
    ('搜尋', 'Search'),

    # Section titles
    ('日本航線', 'Japan Routes'),
    ('韓國航線', 'South Korea Routes'),
    ('東南亞航線', 'Southeast Asia Routes'),
    ('台灣及中國航線', 'Taiwan & China Routes'),
    ('歐美長途航線', 'Long-Haul Europe & Americas'),

    # Route cards
    ('香港 → 東京', 'Hong Kong → Tokyo'),
    ('香港 → 大阪', 'Hong Kong → Osaka'),
    ('香港 → 沖繩', 'Hong Kong → Okinawa'),
    ('香港 → 福岡', 'Hong Kong → Fukuoka'),
    ('香港 → 首爾', 'Hong Kong → Seoul'),
    ('香港 → 釜山', 'Hong Kong → Busan'),
    ('香港 → 曼谷', 'Hong Kong → Bangkok'),
    ('香港 → 新加坡', 'Hong Kong → Singapore'),
    ('香港 → 峇里島', 'Hong Kong → Bali'),
    ('香港 → 越南（胡志明市）', 'Hong Kong → Vietnam (Ho Chi Minh City)'),
    ('香港 → 台北', 'Hong Kong → Taipei'),
    ('香港 → 上海', 'Hong Kong → Shanghai'),
    ('香港 → 倫敦', 'Hong Kong → London'),
    ('香港 → 巴黎', 'Hong Kong → Paris'),
    ('香港 → 紐約', 'Hong Kong → New York'),

    # Route descriptions
    ('成田/羽田機場，飛行約4小時。新宿、淺草、秋葉原等熱門景點。日圓低水旅遊性價比極高。',
     'Narita/Haneda Airport, ~4hr flight. Shinjuku, Asakusa, Akihabara. Weak yen makes Japan travel great value.'),
    ('關西機場，飛行約3.5小時。道頓堀美食、環球影城、心齋橋購物。',
     'Kansai Airport, ~3.5hr flight. Dotonbori food, Universal Studios, Shinsaibashi shopping.'),
    ('那霸機場，飛行約2.5小時。美麗海水族館、國際通、浮潛天堂。',
     'Naha Airport, ~2.5hr flight. Churaumi Aquarium, Kokusai Street, snorkeling paradise.'),
    ('福岡機場，飛行約3小時。博多拉麵、太宰府天滿宮、溫泉。',
     'Fukuoka Airport, ~3hr flight. Hakata ramen, Dazaifu shrine, hot springs.'),
    ('仁川機場，飛行約3.5小時。明洞購物、弘大文青、景福宮韓服體驗。K-pop聖地。',
     'Incheon Airport, ~3.5hr flight. Myeongdong shopping, Hongdae indie scene, Gyeongbokgung hanbok. K-pop pilgrimage.'),
    ('金海機場，飛行約3小時。海雲台海灘、甘川文化村、海鮮市場。',
     'Gimhae Airport, ~3hr flight. Haeundae Beach, Gamcheon Culture Village, seafood market.'),
    ('素萬那普機場，飛行約2.5小時。大皇宮、Chatuchak市集、按摩SPA、街頭美食。',
     'Suvarnabhumi Airport, ~2.5hr flight. Grand Palace, Chatuchak Market, massage & spa, street food.'),
    ('樟宜機場，飛行約3.5小時。濱海灣金沙、環球影城、牛車水美食。',
     'Changi Airport, ~3.5hr flight. Marina Bay Sands, Universal Studios, Chinatown food.'),
    ('伍拉賴機場，飛行約4.5小時。烏布梯田、海神廟、衝浪、Villa度假。',
     'Ngurah Rai Airport, ~4.5hr flight. Ubud rice terraces, Tanah Lot, surfing, villa retreats.'),
    ('新山一機場，飛行約2.5小時。法式殖民建築、越南河粉、咖啡文化。',
     'Tan Son Nhat Airport, ~2.5hr flight. French colonial architecture, pho, coffee culture.'),
    ('桃園機場，飛行約1.5小時。夜市美食、九份、101觀景台。短途首選。',
     'Taoyuan Airport, ~1.5hr flight. Night market food, Jiufen, Taipei 101. Best short-haul trip.'),
    ('浦東/虹橋機場，飛行約2.5小時。外灘夜景、迪士尼、南京路步行街。',
     'Pudong/Hongqiao Airport, ~2.5hr flight. The Bund, Disneyland, Nanjing Road.'),
    ('希斯路機場，飛行約12小時。大英博物館、白金漢宮、西區劇院。',
     'Heathrow Airport, ~12hr flight. British Museum, Buckingham Palace, West End theatre.'),
    ('戴高樂機場，飛行約12小時。鐵塔、羅浮宮、香榭麗舍大道。浪漫之都。',
     'CDG Airport, ~12hr flight. Eiffel Tower, Louvre, Champs-Élysées. City of Romance.'),
    ('JFK機場，飛行約16小時。自由神像、時代廣場、中央公園、百老匯。',
     'JFK Airport, ~16hr flight. Statue of Liberty, Times Square, Central Park, Broadway.'),

    # Airlines
    ('來回機票低至', 'Return from'),
    ('經濟艙含稅', 'Economy incl. tax'),
    ('國泰航空', 'Cathay Pacific'),
    ('日本航空', 'Japan Airlines'),
    ('全日空', 'ANA'),
    ('大韓航空', 'Korean Air'),
    ('韓亞航空', 'Asiana Airlines'),
    ('釜山航空', 'Air Busan'),
    ('新加坡航空', 'Singapore Airlines'),
    ('泰國航空', 'Thai Airways'),
    ('泰獅航', 'Thai Lion Air'),
    ('印尼鷹航', 'Garuda Indonesia'),
    ('越南航空', 'Vietnam Airlines'),
    ('中華航空', 'China Airlines'),
    ('長榮航空', 'EVA Air'),
    ('星宇航空', 'STARLUX'),
    ('東方航空', 'China Eastern'),
    ('春秋航空', 'Spring Airlines'),
    ('英國航空', 'British Airways'),
    ('維珍航空', 'Virgin Atlantic'),
    ('法國航空', 'Air France'),
    ('聯合航空', 'United Airlines'),
    ('樂桃航空', 'Peach Aviation'),
    ('虎航', 'Tigerair'),
    ('酷航', 'Scoot'),
    ('亞洲航空', 'AirAsia'),
    ('香港快運', 'HK Express'),

    # Tips section
    ('買平機票攻略', 'How to Find Cheap Flights'),
    ('週二三最平', 'Tue/Wed Cheapest'),
    ('航空公司通常在週二、三推出促銷，機票價格比週五六日平20-30%。',
     'Airlines typically launch promotions on Tue/Wed, with prices 20-30% cheaper than weekends.'),
    ('提早1-3個月', 'Book 1-3 Months Early'),
    ('短途航線提早4-6星期、長途提早2-3個月預訂通常有最佳價格。',
     'Short-haul: book 4-6 weeks ahead. Long-haul: 2-3 months. This usually gets the best prices.'),
    ('善用格價工具', 'Use Price Comparison'),
    ('Trip.com 提供價格趨勢及預測功能，設定提醒可在降價時即時通知。',
     'Trip.com offers price trends and prediction tools. Set alerts to get notified when prices drop.'),
    ('紅眼航班更平', 'Red-eye Flights Cheaper'),
    ('凌晨出發的航班通常較便宜，適合想慳錢的旅客。到達後直接開始行程。',
     'Early morning flights are usually cheaper. Arrive and start your trip right away.'),
    ('轉機可慳更多', 'Connecting Flights Save More'),
    ('直飛方便但較貴，願意轉機一次可慳高達40%。留意轉機時間至少2小時。',
     'Direct flights are convenient but pricier. One connection can save up to 40%. Allow at least 2hr layover.'),
    ('廉航 vs 傳統', 'Budget vs Full-Service'),
    ('HK Express、樂桃等廉航票價平但要另付行李費。連行李計算後比較才準確。',
     'HK Express, Peach offer lower fares but charge for baggage. Compare total cost including luggage.'),

    # Airlines section
    ('香港出發主要航空公司', 'Major Airlines from Hong Kong'),
    ('傳統航空（含行李及餐飲）', 'Full-Service Airlines (incl. baggage & meals)'),
    ('廉價航空（基本票價較平）', 'Budget Airlines (lower base fares)'),

    # FAQ section headers
    ('機票常見問題', 'Flight FAQs'),
    ('航線專屬格價問題', 'Route-Specific Price FAQs'),

    # FAQ questions
    ('Q: 香港飛東京最平幾錢？', 'Q: What\'s the cheapest flight from Hong Kong to Tokyo?'),
    ('Q: HK Express同國泰航空邊間抵？', 'Q: HK Express vs Cathay Pacific — which is cheaper?'),
    ('Q: 幾時買機票最平？', 'Q: When is the cheapest time to buy flights?'),
    ('Q: 香港飛曼谷幾耐？', 'Q: How long is the flight from Hong Kong to Bangkok?'),
    ('Q: 機票可以免費取消嗎？', 'Q: Can I cancel flights for free?'),
    ('Q: 香港飛首爾最平航空公司？', 'Q: Cheapest airline from Hong Kong to Seoul?'),
    ('Q: 廉航行李費幾錢？', 'Q: How much are budget airline baggage fees?'),
    ('Q: 香港飛大阪最平幾錢？邊間航空公司最抵？', 'Q: Cheapest Hong Kong to Osaka flights? Best airline?'),
    ('Q: 香港飛沖繩有直航嗎？', 'Q: Are there direct flights from Hong Kong to Okinawa?'),
    ('Q: 香港飛新加坡邊間航空公司好？', 'Q: Best airline from Hong Kong to Singapore?'),
    ('Q: 香港飛台北最平幾時？', 'Q: When are Hong Kong to Taipei flights cheapest?'),
    ('Q: 國泰航空同HK Express飛日本邊間好？', 'Q: Cathay Pacific vs HK Express to Japan — which is better?'),
    ('Q: 香港飛倫敦最平幾錢？要飛幾耐？', 'Q: Cheapest Hong Kong to London flights? How long?'),

    # FAQ answers
    ('香港飛東京來回經濟艙含稅約HK$1,280起。HK Express廉航促銷時可低至HK$980。建議提早4-6星期預訂，避開日本黃金週及暑假旺季。週二三出發通常最平。',
     'Hong Kong to Tokyo return economy from HK$1,280 incl. tax. HK Express sales can go as low as HK$980. Book 4-6 weeks early, avoid Golden Week and summer peak. Tue/Wed departures are cheapest.'),
    ('HK Express基本票價較平，但不含行李及餐飲。如需寄艙行李20kg（約HK$200-300），加上去後未必比國泰平。短途1-2天旅行揀HK Express，長途帶多行李揀國泰。',
     'HK Express has lower base fares but excludes baggage and meals. Adding 20kg checked bag (HK$200-300) may close the gap with Cathay. Choose HK Express for 1-2 day trips, Cathay for longer trips with more luggage.'),
    ('短途（日韓泰）：出發前4-6星期。長途（歐美）：出發前2-3個月。每年1月、5月及9月是航空公司大促銷季節。週二三下午經常有限時特價。',
     'Short-haul (Japan/Korea/Thailand): 4-6 weeks before. Long-haul (Europe/US): 2-3 months. Jan, May, Sep are major airline sale seasons. Tue/Wed afternoons often have flash deals.'),
    ('香港直飛曼谷約2.5小時，是香港人最受歡迎的短途目的地之一。來回含稅約HK$880起。泰獅航、HK Express經常有促銷低至HK$600。',
     'Direct flight ~2.5 hours, one of the most popular short-haul destinations for HK travellers. Return from HK$880. Thai Lion Air & HK Express often have promos as low as HK$600.'),
    ('視乎票種。傳統航空的彈性票通常可免費改期或取消。廉航基本票不可退改，需加購「彈性退改」選項（約HK$100-200）。Trip.com部分機票提供「免費取消」標籤。',
     'Depends on fare type. Full-service flexible fares usually allow free changes/cancellation. Budget basic fares are non-refundable — add "flexible rebooking" option (~HK$100-200). Some Trip.com fares offer "Free Cancellation".'),
    ('HK Express及釜山航空通常提供最平價格，來回約HK$1,180起。國泰及大韓航空含行李餐飲約HK$2,000起。促銷期間HK Express可低至HK$800。',
     'HK Express and Air Busan offer the lowest prices, return from HK$1,180. Cathay and Korean Air with baggage/meals from HK$2,000. HK Express sales can go as low as HK$800.'),
    ('HK Express寄艙行李20kg約HK$200-350（視航線），手提行李7kg免費。樂桃行李約HK$180-280。建議預訂時即加購行李，機場櫃台加購會貴50%以上。',
     'HK Express checked 20kg: HK$200-350 (varies by route), carry-on 7kg free. Peach baggage: HK$180-280. Add baggage at booking — airport counter is 50%+ more expensive.'),
    ('香港飛大阪（關西機場）來回含稅約HK$1,180起。HK Express及樂桃航空是最平選擇，促銷時可低至HK$880。國泰航空含行李餐飲約HK$1,800起。飛行約3.5小時，建議提早4-6星期預訂。',
     'HK to Osaka (Kansai) return from HK$1,180 incl. tax. HK Express and Peach are cheapest, sales as low as HK$880. Cathay with baggage/meals from HK$1,800. ~3.5hr flight, book 4-6 weeks early.'),
    ('有！HK Express及樂桃航空提供香港直飛沖繩（那霸機場）航線，飛行約2.5小時。來回含稅約HK$980起。沖繩是日本最近的度假勝地，適合3-4天短途海島遊。',
     'Yes! HK Express and Peach offer direct flights to Okinawa (Naha), ~2.5 hours. Return from HK$980 incl. tax. Okinawa is the closest Japanese resort — perfect for 3-4 day beach trips.'),
    ('新加坡航空服務質素最高但價格較貴（約HK$1,800起）。國泰航空性價比好（約HK$1,400起）。酷航（Scoot）是廉航選擇，含稅約HK$1,080起但不含行李。飛行約3.5小時。',
     'Singapore Airlines has the best service but costs more (from HK$1,800). Cathay offers good value (from HK$1,400). Scoot is the budget option (from HK$1,080 but no baggage). ~3.5hr flight.'),
    ('香港飛台北是最短途國際航線（1.5小時），來回HK$780起。平日（週二至四）比週末平30%。避開農曆新年、端午及中秋假期。4月底至5月初及10月至11月是台灣旅遊最佳季節。',
     'HK to Taipei is the shortest international route (1.5hr), return from HK$780. Weekdays (Tue-Thu) are 30% cheaper. Avoid CNY, Dragon Boat, Mid-Autumn. Late Apr-May and Oct-Nov are best seasons.'),
    ('國泰航空含23kg寄艙行李+機上餐飲+選位，東京來回約HK$2,200起。HK Express基本票HK$1,280起但要加行李（HK$200-350）及餐飲。如果帶20kg行李，兩者差價僅約HK$300-500，國泰體驗好好多。輕裝出行2-3天選HK Express，正常旅行選國泰。',
     'Cathay includes 23kg baggage + meals + seat selection, Tokyo return from HK$2,200. HK Express base fare HK$1,280 plus baggage (HK$200-350). With 20kg luggage, the gap is only HK$300-500 — Cathay is much better value. Light 2-3 day trips: HK Express. Normal trips: Cathay.'),
    ('國泰航空直飛倫敦希斯路約12小時，來回含稅HK$4,280起。經杜拜轉機（阿聯酋航空）約HK$3,500起但耗時18-20小時。英國航空直飛約HK$4,500起。建議提早2-3個月預訂，暑假及聖誕是最貴時段。',
     'Cathay direct to Heathrow ~12hr, return from HK$4,280. Via Dubai (Emirates) from HK$3,500 but 18-20hr total. British Airways direct from HK$4,500. Book 2-3 months early. Summer and Christmas are peak pricing.'),

    # Route guide article
    ('香港出發航線攻略', 'Hong Kong Flight Route Guide'),
    ('日本航線 — 香港人至愛目的地', 'Japan — Hong Kong\'s Favourite Destination'),
    ('韓國航線 — K-pop及美食天堂', 'South Korea — K-pop & Food Paradise'),
    ('東南亞航線 — 短途平價首選', 'Southeast Asia — Best Budget Short-Haul'),
    ('台灣航線 — 最短途最方便', 'Taiwan — Shortest & Most Convenient'),
    ('歐美長途航線 — 提早預訂至關重要', 'Europe & Americas — Book Early, Save Big'),

    # Price table
    ('香港出發機票價格一覽表', 'Hong Kong Flight Price Overview'),
    ('目的地', 'Destination'),
    ('飛行時間', 'Flight Time'),
    ('廉航價格', 'Budget Airline'),
    ('傳統航空', 'Full-Service'),
    ('最佳預訂時間', 'Best Booking Time'),
    ('小時', 'hr'),
    ('星期前', ' weeks early'),
    ('個月前', ' months early'),
    ('* 價格為來回經濟艙含稅參考價，實際價格視乎日期及航空公司。點擊「搜尋」查看 Trip.com 最新價格。',
     '* Prices are return economy incl. tax for reference. Actual prices vary by date and airline. Click "Search" for latest Trip.com prices.'),

    # Disclaimer & Footer
    ('以上資料只供參考，實際價格以預訂平台為準。本頁面包含聯盟推廣連結，透過連結預訂我們可能獲得佣金，不影響你的價格。',
     'Information is for reference only. Actual prices are subject to the booking platform. This page contains affiliate links — booking through these links may earn us a commission at no extra cost to you.'),
]

for zh, en in translations:
    html = html.replace(zh, en)

with open("C:/Users/tonyng/Desktop/Claude_Code/BROADBANDHK/pages/flights-en.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Generated flights-en.html successfully!")
