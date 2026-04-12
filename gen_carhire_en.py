"""Generate carhire-en.html by replacing all Chinese text"""
with open("C:/Users/tonyng/Desktop/Claude_Code/BROADBANDHK/pages/carhire-en.html","r",encoding="utf-8") as f:
    h = f.read()

# Sort by length desc to avoid partial match
t = [
    ('lang="zh-Hant-HK"','lang="en"'),
    ('租車格價2026｜全球200+國家自駕遊．沖繩大阪北海道濟州｜HK$145起/日｜Trip.com租車比較','Car Rental 2026 | Self-Drive 200+ Countries · Okinawa Osaka Hokkaido Jeju | From HK$145/day'),
    ('2026年租車格價比較！全球200+國家、10,000+城市自駕遊。沖繩租車HK$145起/日、大阪HK$212起、北海道HK$175起、濟州島HK$150起。Hertz、Avis、Budget、Times即時比價。新用戶8%折扣。','2026 car rental comparison! 200+ countries. Okinawa HK$145/day, Osaka HK$212, Hokkaido HK$175, Jeju HK$150. Compare Hertz, Avis, Budget, Times. New users 8% off.'),
    ('carhire.html','carhire-en.html'),
    ('hreflang="zh-Hant-HK" href="https://broadbandhk.com/pages/carhire-en.html"','hreflang="zh-Hant-HK" href="https://broadbandhk.com/pages/carhire.html"'),
    ('hreflang="x-default" href="https://broadbandhk.com/pages/carhire-en.html"','hreflang="x-default" href="https://broadbandhk.com/pages/carhire.html"'),
    ('"language" content="zh-Hant-HK"','"language" content="en"'),
    ('"og:locale" content="zh_HK"','"og:locale" content="en_US"'),
    ('"og:locale:alternate" content="en_US"','"og:locale:alternate" content="zh_HK"'),
    ('"inLanguage": "zh-HK"','"inLanguage": "en"'),
    ('租車格價2026｜全球自駕遊｜沖繩大阪北海道HK$145起/日','Car Rental 2026 | Global Self-Drive | Okinawa Osaka Hokkaido From HK$145/day'),
    ('全球200+國家租車比價。沖繩HK$145起、大阪HK$212起。Hertz/Avis/Budget即時格價。新用戶8%折扣。','Compare 200+ countries. Okinawa HK$145, Osaka HK$212. Hertz/Avis/Budget. New users 8% off.'),
    ('租車格價2026｜全球自駕遊比較','Car Rental 2026 | Global Self-Drive Comparison'),
    ('全球200+國家、10,000+城市租車即時格價比較。','Compare car rental across 200+ countries, 10,000+ cities.'),
    # Nav
    ('酒店格價','Hotels'), ('機票格價','Flights'), ('高鐵訂票','Trains'), ('租車自駕','Car Rental'),
    ('首頁','Home'), ('租車格價','Car Rental'),
    # Hero
    ('租車格價2026｜全球自駕遊比較','Car Rental 2026 | Global Self-Drive'),
    ('覆蓋全球200+國家、10,000+城市。比較Hertz、Avis、Budget、Times等頂級租車品牌，即時格價搵最抵自駕遊方案。新用戶享8%折扣。','Compare across 200+ countries, 10,000+ cities. Hertz, Avis, Budget, Times instant comparison. New users get 8% discount.'),
    ('國家覆蓋','Countries'), ('每日租金','Per Day'), ('免費取消','Free Cancel'), ('彈性預訂','Flexible'),
    ('搜尋全球租車 →','Search Car Rentals Worldwide →'), ('搜尋更多租車目的地 →','Search More Destinations →'), ('搜尋','Search'),
    # Section titles
    ('日本自駕遊（最受歡迎）','Japan Self-Drive (Most Popular)'), ('韓國自駕遊','South Korea Self-Drive'),
    ('台灣及東南亞自駕遊','Taiwan & Southeast Asia'), ('歐美自駕遊','Europe & Americas'),
    # Dest cards
    ('沖繩自駕遊','Okinawa Self-Drive'), ('那霸機場取車，自駕遊美麗海水族館、古宇利大橋、萬座毛、美國村。沖繩沒有鐵路，租車是最佳交通方式。','Naha Airport pickup. Drive to Churaumi Aquarium, Kouri Bridge, Cape Manzamo, American Village. No railway — car is essential.'),
    ('北海道自駕遊','Hokkaido Self-Drive'), ('新千歲機場取車，自駕遊富良野薰衣草田、美瑛青池、小樽運河、洞爺湖。夏天花海冬天雪景。','New Chitose Airport. Furano lavender, Biei Blue Pond, Otaru Canal, Lake Toya. Summer flowers, winter snow.'),
    ('大阪/京都自駕遊','Osaka/Kyoto Self-Drive'), ('關西機場取車，自駕遊京都嵐山、奈良東大寺、有馬溫泉、白濱。適合關西深度遊。','Kansai Airport. Kyoto Arashiyama, Nara Todai-ji, Arima Onsen, Shirahama. Deep Kansai exploration.'),
    ('東京/箱根自駕遊','Tokyo/Hakone Self-Drive'), ('成田機場取車，自駕遊箱根溫泉、富士山河口湖、輕井澤、伊豆半島。東京市區不建議開車。','Narita Airport. Hakone onsen, Mt Fuji Kawaguchi, Karuizawa, Izu Peninsula. Avoid central Tokyo driving.'),
    ('福岡/九州自駕遊','Fukuoka/Kyushu Self-Drive'), ('福岡機場取車，自駕遊由布院溫泉、阿蘇火山、別府地獄溫泉、熊本城。九州溫泉之旅首選。','Fukuoka Airport. Yufuin Onsen, Mt Aso, Beppu Hell Springs, Kumamoto Castle. Best onsen road trip.'),
    ('濟州島自駕遊','Jeju Island Self-Drive'), ('濟州機場取車，環島自駕遊城山日出峰、牛島、中文觀光區、漢拏山。濟州島環島一圈約3小時。','Jeju Airport. Island loop: Seongsan Ilchulbong, Udo, Jungmun, Hallasan. Full loop ~3 hours.'),
    ('高雄/墾丁自駕遊','Kaohsiung/Kenting Self-Drive'), ('高雄機場取車，自駕遊墾丁國家公園、旗津海岸、屏東海生館。南台灣陽光海岸之旅。','Kaohsiung Airport. Kenting National Park, Cijin Coast, Pingtung Aquarium. Southern Taiwan sun coast.'),
    ('台北/花蓮自駕遊','Taipei/Hualien Self-Drive'), ('桃園機場取車，自駕遊太魯閣峽谷、清水斷崖、九份老街、宜蘭。東海岸壯麗風景。','Taoyuan Airport. Taroko Gorge, Qingshui Cliffs, Jiufen, Yilan. Spectacular east coast.'),
    ('曼谷自駕遊','Bangkok Self-Drive'), ('素萬那普機場取車，自駕遊華欣、芭堤雅、考艾國家公園。泰國高速公路路況良好。','Suvarnabhumi Airport. Hua Hin, Pattaya, Khao Yai National Park. Thailand highways in good condition.'),
    ('洛杉磯/加州1號公路','LA / California Highway 1'), ('LAX機場取車，自駕加州1號公路（Big Sur）、聖塔芭芭拉、三藩市金門大橋。全球最經典自駕路線之一。','LAX pickup. Pacific Coast Highway (Big Sur), Santa Barbara, SF Golden Gate. One of the world\'s most iconic drives.'),
    ('冰島環島自駕','Iceland Ring Road'), ('凱夫拉維克機場取車，環島自駕遊黃金圈、藍湖溫泉、冰川、北極光。Ring Road全長1,322公里。','Keflavik Airport. Ring Road: Golden Circle, Blue Lagoon, glaciers, Northern Lights. Full loop 1,322km.'),
    # Tags
    ('那霸機場','Naha Airport'), ('右軚駕駛','Drive on Left'), ('免國際車牌','IDP Required'), ('最受歡迎','Most Popular'),
    ('新千歲機場','New Chitose'), ('冬天需雪胎','Snow Tyres Winter'), ('風景公路','Scenic Routes'),
    ('關西機場','Kansai Airport'), ('高速公路ETC','Highway ETC'), ('京阪神','Kansai Region'),
    ('成田機場','Narita Airport'), ('富士山','Mt Fuji'), ('溫泉之旅','Hot Springs'),
    ('福岡機場','Fukuoka Airport'), ('溫泉巡禮','Onsen Tour'), ('美食之旅','Food Trip'),
    ('濟州機場','Jeju Airport'), ('環島自駕','Island Loop'),
    ('高雄機場','Kaohsiung Airport'), ('墾丁海灘','Kenting Beach'), ('夜市美食','Night Markets'),
    ('桃園機場','Taoyuan Airport'), ('太魯閣','Taroko Gorge'), ('蘇花公路','Suhua Highway'),
    ('素萬那普機場','Suvarnabhumi'), ('華欣','Hua Hin'), ('考艾','Khao Yai'),
    ('LAX機場','LAX Airport'), ('左軚駕駛','Drive on Right'), ('加州1號公路','PCH Highway 1'), ('經典路線','Iconic Route'),
    ('凱夫拉維克機場','Keflavik Airport'), ('極光','Northern Lights'),
    # Price labels
    ('每日租金低至','Daily rate from'), ('起/日（含保險）','/day (incl. insurance)'),
    # Tips
    ('租車自駕攻略','Car Rental Tips'),
    ('國際駕照','International Driving Permit'), ('日本及韓國接受香港駕照+國際駕駛許可證（IDP）。美國大部分州接受香港駕照。建議出發前在運輸署辦理IDP（HK$80）。','Japan & Korea accept HK licence + IDP. Most US states accept HK licence. Get IDP from Transport Dept (HK$80).'),
    ('保險必買','Insurance Essential'), ('基本保險（CDW）通常已含在租金內。建議加購全險（Full Cover），每日約HK$50-100，萬一發生意外可免自付額。','Basic CDW usually included. Add Full Cover (~HK$50-100/day) to reduce excess to zero.'),
    ('提早預訂更平','Book Early, Save More'), ('提前2-4星期預訂通常比到場租車便宜30-50%。旺季（暑假、聖誕）建議提前1個月訂。Trip.com可免費取消。','2-4 weeks ahead is 30-50% cheaper. Peak season book 1 month early. Trip.com offers free cancellation.'),
    ('日本ETC卡','Japan ETC Card'), ('日本高速公路需要ETC卡（電子收費），租車時可一併租用。外國旅客可用Expressway Pass享折扣。','Japan highways need ETC card. Rent with your car. Tourists can use Expressway Pass for discounts.'),
    ('甲借乙還','One-Way Rental'), ('Trip.com支援異地還車（甲借乙還），但會收取額外費用。同城市不同門店還車通常免費。','Trip.com supports one-way. Same city different branch usually free. Different cities HK$200-1,000.'),
    ('油費及還車','Fuel & Return'), ('大部分租車需在還車前加滿油（Full-to-Full）。日本油價約HK$10/公升，比香港便宜。還車時保留油站收據。','Most are Full-to-Full. Japan fuel ~HK$10/litre. Keep fuel receipt when returning.'),
    # Brands
    ('合作租車品牌','Partner Car Rental Brands'), ('和運租車（台灣）','Ho Ing (Taiwan)'),
    # Price table
    ('熱門目的地租車價格一覽','Car Rental Price Overview'),
    ('目的地','Destination'), ('小型車/日','Compact/day'), ('SUV/日','SUV/day'), ('駕駛方向','Driving Side'), ('需國際駕照','IDP Needed?'),
    ('🇯🇵 沖繩','🇯🇵 Okinawa'), ('🇯🇵 北海道','🇯🇵 Hokkaido'), ('🇯🇵 大阪','🇯🇵 Osaka'),
    ('🇰🇷 濟州島','🇰🇷 Jeju'), ('🇹🇼 高雄','🇹🇼 Kaohsiung'), ('🇹🇭 曼谷','🇹🇭 Bangkok'),
    ('🇺🇸 洛杉磯','🇺🇸 Los Angeles'), ('🇮🇸 冰島','🇮🇸 Iceland'),
    ('右軚（靠左行）','Left (RHD)'), ('左軚（靠左行）','Left (RHD)'), ('左軚（靠右行）','Right (LHD)'), ('右軚（靠右行）','Right (LHD)'),
    ('需IDP','Yes'), ('HK駕照可用','HK Licence OK'),
    ('起','from'),
    ('* 價格僅供參考，實際價格視乎日期、車型及租車公司。點擊「搜尋」查看 Trip.com 最新價格。','* Prices for reference. Click "Search" for latest Trip.com prices.'),
    # Guide article
    ('自駕遊目的地攻略','Self-Drive Destination Guide'),
    ('沖繩自駕 — 香港人至愛','Okinawa — Hong Kong\'s Favourite'),
    ('沖繩是香港人最喜歡的自駕目的地，沒有鐵路系統令租車成為必須。那霸機場有多間租車公司（Times、Toyota、Nippon），取車非常方便。沖繩公路路況極佳，速限50-80km/h，適合新手。建議行程：美麗海水族館→古宇利島→萬座毛→美國村→那霸國際通。注意日本靠左行駛，香港人習慣右軚所以適應快。需在出發前準備國際駕駛許可證（IDP），運輸署辦理只需HK$80。',
     'Okinawa is HK\'s top self-drive spot. No railway makes rental essential. Naha Airport has Times, Toyota, Nippon — easy pickup. Roads are excellent, 50-80km/h limits, beginner-friendly. Route: Churaumi → Kouri Island → Manzamo → American Village → Kokusai Street. Japan drives left — HK drivers adapt fast with RHD. Get IDP from Transport Dept, HK$80.'),
    ('北海道自駕 — 風景公路','Hokkaido — Scenic Road Trip'),
    ('北海道是日本最適合自駕的地方，公路寬闊車少風景壯麗。夏天（6-8月）薰衣草田、花田，秋天（9-10月）紅葉，冬天（12-3月）雪景。冬天租車必須指定雪胎（Snow Tire），大部分租車公司冬季自動提供。推薦路線：新千歲→富良野→美瑛→旭川→小樽→札幌，約5天行程。',
     'Hokkaido has Japan\'s best driving — wide roads, little traffic, stunning views. Summer (Jun-Aug) lavender, autumn (Sep-Oct) foliage, winter (Dec-Mar) snow. Winter requires snow tyres (provided automatically). Route: Chitose → Furano → Biei → Asahikawa → Otaru → Sapporo, ~5 days.'),
    ('濟州島環島 — 最輕鬆自駕','Jeju Island — Easiest Self-Drive'),
    ('濟州島環島一圈僅約3小時，是最輕鬆的自駕目的地。濟州機場取車非常方便，韓國靠右行駛與大部分國家相同。推薦景點：城山日出峰、牛島（需搭渡輪）、中文觀光區、漢拏山。注意韓國高速公路收費需用Hi-pass或現金。',
     'Jeju\'s full loop is only ~3 hours — the most relaxed self-drive. Easy Jeju Airport pickup, Korea drives right like most countries. Top spots: Seongsan, Udo (ferry), Jungmun, Hallasan. Korean highways use Hi-pass or cash tolls.'),
    ('加州1號公路 — 全球最經典','California Hwy 1 — World\'s Most Iconic'),
    ('加州1號公路（Pacific Coast Highway）是全球最經典自駕路線之一，從洛杉磯到三藩市沿太平洋海岸行駛約650公里。必停景點：Big Sur、蒙特雷、赫斯特城堡、聖塔芭芭拉。建議用3-5天完成，沿途住宿。美國靠右行駛，加油站自助，高速公路大部分免費。',
     'PCH is one of the world\'s most iconic drives, 650km LA to SF along the Pacific. Must-stop: Big Sur, Monterey, Hearst Castle, Santa Barbara. Allow 3-5 days. US drives right, self-service gas, most highways toll-free.'),
    # FAQ
    ('租車常見問題','Car Rental FAQs'),
    ('Q: 香港人在日本租車需要什麼文件？','Q: What documents do I need to rent in Japan?'),
    ('需要：(1) 有效香港駕照 (2) 國際駕駛許可證IDP（運輸署辦理HK$80）(3) 護照 (4) 信用卡（用於押金）。注意日本不接受中國駕照。IDP有效期1年。','You need: (1) Valid HK licence (2) IDP from Transport Dept, HK$80 (3) Passport (4) Credit card for deposit. Japan doesn\'t accept Chinese licences. IDP valid 1 year.'),
    ('Q: 日本租車大約幾錢一日？','Q: How much is car rental in Japan per day?'),
    ('小型車（如Toyota Vitz）約HK$145-212/日，SUV約HK$280-350/日，7人車約HK$350-500/日。含基本保險（CDW）。高速公路收費另計，建議租ETC卡。油費約HK$10/公升。','Compact (e.g. Toyota Vitz) HK$145-212/day, SUV HK$280-350/day, 7-seater HK$350-500/day. Incl. CDW. Highway tolls extra — rent ETC card. Fuel ~HK$10/litre.'),
    ('Q: 租車保險點揀？','Q: Which car rental insurance should I get?'),
    ('基本保險（CDW/LDW）通常已含在租金。建議加購全險（Full Cover/Super CDW），每日約HK$50-100，可將自付額降至0。Trip.com部分套餐已含全險，預訂時留意。','Basic CDW/LDW usually included. Add Full Cover/Super CDW (~HK$50-100/day) to reduce excess to zero. Some Trip.com packages include full cover.'),
    ('Q: 甲借乙還（異地還車）會額外收費嗎？','Q: Is one-way rental (different drop-off) extra?'),
    ('同城市不同門店通常免費。不同城市（如大阪借東京還）會收取異地還車費，約HK$200-1,000視乎距離。建議預訂時先確認費用。','Same city different branch usually free. Different cities (e.g. Osaka pickup, Tokyo drop-off) charge HK$200-1,000 by distance. Confirm when booking.'),
    ('Q: 冬天在北海道租車安全嗎？','Q: Is it safe to drive in Hokkaido in winter?'),
    ('安全但需注意：(1) 必須使用雪胎（租車公司冬季自動提供）(2) 避免夜間駕駛 (3) 減速慢行 (4) 預留更多行車時間。北海道公路除雪效率高，主要公路全年暢通。','Safe with precautions: (1) Snow tyres mandatory (auto-provided winter) (2) Avoid night driving (3) Reduce speed (4) Allow extra time. Hokkaido snow clearing is efficient, main roads clear year-round.'),
    ('Q: 濟州島租車需要國際駕照嗎？','Q: Do I need an IDP for Jeju Island?'),
    ('需要。香港駕照+IDP（國際駕駛許可證）即可在韓國租車。濟州機場有多間租車公司，取車方便。韓國靠右行駛。注意韓國酒駕零容忍，血液酒精濃度0.03%即違法。','Yes. HK licence + IDP works in Korea. Easy Jeju Airport pickup. Korea drives right. Zero tolerance for drink driving — 0.03% BAC is illegal.'),
    ('Q: 租車可以免費取消嗎？','Q: Can I cancel for free?'),
    ('Trip.com大部分租車訂單支持免費取消（取車前48小時）。預訂時留意「免費取消」標籤。部分特價訂單可能不可退改，預訂前確認條款。','Most Trip.com rentals offer free cancel 48hr before pickup. Look for "Free Cancellation" tag. Some discounted bookings may be non-refundable.'),
    ('Q: 新用戶有優惠嗎？','Q: Any new user discounts?'),
    ('有！Trip.com新用戶首次租車可領取8%優惠券，有效期15天。另外，已在Trip.com訂機票或酒店的用戶可享專屬租車折扣。','Yes! New users get 8% coupon valid 15 days. Users who booked flights/hotels get exclusive car rental discounts.'),
    # Disclaimer
    ('以上資料只供參考，實際價格以預訂平台為準。本頁面包含聯盟推廣連結，透過連結預訂我們可能獲得佣金，不影響你的價格。','Information is for reference only. Actual prices subject to booking platform. This page contains affiliate links — booking may earn us a commission at no extra cost to you.'),
    # Add language toggle
    ('<a href="https://broadbandhk.com/pages/carhire-en.html">租車自駕</a>','<a href="https://broadbandhk.com/pages/carhire-en.html">Car Rental</a><a href="https://broadbandhk.com/pages/carhire.html" style="background:rgba(255,255,255,0.2);padding:4px 12px;border-radius:15px;">中文</a>'),
]
t.sort(key=lambda x: len(x[0]), reverse=True)
for old, new in t:
    h = h.replace(old, new)
with open("C:/Users/tonyng/Desktop/Claude_Code/BROADBANDHK/pages/carhire-en.html","w",encoding="utf-8") as f:
    f.write(h)
print("Done")
