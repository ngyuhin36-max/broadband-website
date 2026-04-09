"""
Real hotel data for major cities worldwide
Used by generate_travel_pages.py to create rich hotel listing pages
"""

# Format: { "CityEnglishName": [ (name_zh, name_en, stars, district_zh, district_en, rating, reviews, price_hkd, tags_zh, tags_en, img_url), ... ] }

HOTELS = {
    "Hong Kong": [], # Already has dedicated page travel-hotel-deals.html

    "Tokyo": [
        ("東京帝國酒店", "Imperial Hotel Tokyo", 5, "日比谷/銀座", "Hibiya/Ginza", 9.3, 4521, 2180, "歷史名酒店,銀座購物,皇居旁", "Historic,Ginza Shopping,Near Imperial Palace", "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=500&h=300&fit=crop"),
        ("東京安達仕酒店", "Andaz Tokyo Toranomon Hills", 5, "虎之門", "Toranomon", 9.4, 3102, 2680, "設計酒店,高層景觀,米芝蓮餐廳", "Design Hotel,High-rise Views,Michelin Dining", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("新宿格拉斯麗酒店", "Hotel Gracery Shinjuku", 4, "新宿", "Shinjuku", 8.7, 12450, 780, "哥斯拉主題,歌舞伎町,交通便利", "Godzilla Theme,Kabukicho,Convenient Transport", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
        ("淺草豪景酒店", "Asakusa View Hotel", 4, "淺草", "Asakusa", 8.5, 8932, 650, "晴空塔景觀,淺草寺旁,日式體驗", "Skytree Views,Near Senso-ji,Japanese Experience", "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=500&h=300&fit=crop"),
        ("東京站大都會酒店", "Hotel Metropolitan Tokyo", 4, "池袋", "Ikebukuro", 8.6, 7654, 720, "池袋站直達,購物方便,家庭友善", "Direct Station Access,Shopping,Family Friendly", "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=500&h=300&fit=crop"),
        ("東京灣希爾頓酒店", "Hilton Tokyo Bay", 4, "舞濱", "Maihama", 8.8, 9876, 950, "迪士尼官方酒店,海景房,親子首選", "Disney Official,Ocean View,Family Favorite", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
        ("上野三井花園酒店", "Mitsui Garden Hotel Ueno", 3, "上野", "Ueno", 8.4, 6543, 520, "上野公園旁,交通樞紐,性價比高", "Near Ueno Park,Transport Hub,Great Value", "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=500&h=300&fit=crop"),
        ("品川王子酒店", "Shinagawa Prince Hotel", 4, "品川", "Shinagawa", 8.2, 15678, 680, "水族館,IMAX電影院,新幹線站旁", "Aquarium,IMAX Cinema,Near Shinkansen", "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=500&h=300&fit=crop"),
        ("APA酒店新宿歌舞伎町塔", "APA Hotel Shinjuku Kabukicho Tower", 3, "新宿", "Shinjuku", 8.0, 21345, 420, "超值之選,新宿核心,大浴場", "Budget Pick,Central Shinjuku,Public Bath", "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500&h=300&fit=crop"),
        ("東京椿山莊酒店", "Hotel Chinzanso Tokyo", 5, "目白", "Mejiro", 9.5, 2345, 3200, "日式庭園,螢火蟲季節,奢華水療", "Japanese Garden,Firefly Season,Luxury Spa", "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500&h=300&fit=crop"),
    ],

    "Osaka": [
        ("大阪瑞吉酒店", "The St. Regis Osaka", 5, "中之島", "Nakanoshima", 9.4, 2890, 2580, "頂級奢華,河景,米芝蓮餐廳", "Ultra Luxury,River View,Michelin Dining", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("大阪萬豪都酒店", "Osaka Marriott Miyako Hotel", 5, "阿倍野", "Abeno", 9.2, 5432, 1880, "日本最高樓,360度景觀,天王寺旁", "Tallest Building,360° Views,Near Tennoji", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
        ("心齋橋大和皇家酒店", "Daiwa Roynet Shinsaibashi", 4, "心齋橋", "Shinsaibashi", 8.8, 9876, 680, "道頓堀步行3分鐘,購物天堂", "3min to Dotonbori,Shopping Paradise", "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=500&h=300&fit=crop"),
        ("難波東方酒店", "Namba Oriental Hotel", 4, "難波", "Namba", 8.6, 7654, 620, "難波站直達,美食集中地,交通便利", "Direct Namba Access,Food Hub,Convenient", "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=500&h=300&fit=crop"),
        ("大阪環球影城港口酒店", "Hotel Universal Port", 4, "此花區", "Konohana", 8.7, 11234, 850, "環球影城官方,主題房間,親子首選", "USJ Official,Themed Rooms,Family Pick", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
        ("大阪十字酒店", "Cross Hotel Osaka", 4, "心齋橋", "Shinsaibashi", 8.9, 6543, 750, "設計酒店,道頓堀旁,天台浴池", "Design Hotel,Near Dotonbori,Rooftop Bath", "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=500&h=300&fit=crop"),
        ("梅田阪急大酒店", "Hotel Hankyu Grand Osaka", 4, "梅田", "Umeda", 8.5, 8765, 720, "梅田站直達,百貨公司旁,商務首選", "Direct Umeda Station,Near Department Store", "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=500&h=300&fit=crop"),
        ("Super Hotel難波日本橋", "Super Hotel Namba Nihonbashi", 3, "日本橋", "Nihonbashi", 8.3, 13456, 380, "超值之選,黑門市場旁,溫泉浴池", "Budget Pick,Near Kuromon Market,Hot Spring", "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500&h=300&fit=crop"),
    ],

    "Kyoto": [
        ("京都麗思卡爾頓", "The Ritz-Carlton Kyoto", 5, "鴨川", "Kamogawa", 9.6, 1876, 4500, "鴨川河畔,日式奢華,米芝蓮餐廳", "Kamogawa Riverside,Japanese Luxury,Michelin", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("京都四季酒店", "Four Seasons Hotel Kyoto", 5, "東山", "Higashiyama", 9.5, 2345, 4200, "800年庭園,池泉回遊式,頂級體驗", "800yr Garden,Pond Garden,Premium Experience", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
        ("祇園賽萊斯廷酒店", "Hotel The Celestine Gion", 4, "祇園", "Gion", 9.0, 5432, 1280, "祇園核心,藝妓文化,傳統町家風", "Central Gion,Geisha Culture,Machiya Style", "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=500&h=300&fit=crop"),
        ("京都站三井花園酒店", "Mitsui Garden Kyoto Station", 4, "京都站", "Kyoto Stn", 8.7, 8765, 680, "京都站步行2分鐘,交通樞紐", "2min Kyoto Station,Transport Hub", "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=500&h=300&fit=crop"),
        ("河原町御池酒店", "Daiwa Roynet Kawaramachi", 4, "河原町", "Kawaramachi", 8.6, 6789, 620, "購物區核心,錦市場旁,美食天堂", "Shopping Center,Near Nishiki Market,Food Hub", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
        ("嵐山溫泉旅館", "Suiran Luxury Collection Arashiyama", 5, "嵐山", "Arashiyama", 9.4, 1234, 3800, "竹林旁,露天溫泉,日式旅館", "Near Bamboo Grove,Open-air Onsen,Ryokan", "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500&h=300&fit=crop"),
    ],

    "Seoul": [
        ("首爾四季酒店", "Four Seasons Hotel Seoul", 5, "光化門", "Gwanghwamun", 9.5, 3456, 2800, "景福宮旁,頂級奢華,城市景觀", "Near Gyeongbokgung,Top Luxury,City Views", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("首爾JW萬豪酒店", "JW Marriott Seoul", 5, "江南", "Gangnam", 9.3, 4567, 2200, "江南核心,購物便利,商務首選", "Central Gangnam,Shopping,Business Pick", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
        ("明洞樂天城市酒店", "Lotte City Hotel Myeongdong", 4, "明洞", "Myeongdong", 8.8, 12345, 780, "明洞購物街,免稅店旁,交通便利", "Myeongdong Shopping,Duty Free,Convenient", "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=500&h=300&fit=crop"),
        ("弘大L7酒店", "L7 Hongdae by Lotte", 4, "弘大", "Hongdae", 8.7, 9876, 650, "弘大文青區,夜生活豐富,屋頂泳池", "Hongdae Indie,Nightlife,Rooftop Pool", "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=500&h=300&fit=crop"),
        ("首爾東大門諾富特大使酒店", "Novotel Ambassador Dongdaemun", 4, "東大門", "Dongdaemun", 8.6, 8765, 620, "24小時購物,DDP旁,交通樞紐", "24hr Shopping,Near DDP,Transport Hub", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
        ("南山首爾塔萬怡酒店", "Courtyard by Marriott Namdaemun", 4, "南大門", "Namdaemun", 8.5, 7654, 580, "首爾塔景觀,南大門市場旁,超值", "Seoul Tower View,Near Market,Great Value", "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=500&h=300&fit=crop"),
        ("梨泰院漢密爾頓酒店", "Hamilton Hotel Itaewon", 3, "梨泰院", "Itaewon", 7.8, 15678, 380, "異國風情,酒吧街,經濟之選", "International Vibe,Bar Street,Budget Pick", "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500&h=300&fit=crop"),
        ("江南宜必思酒店", "Ibis Ambassador Gangnam", 3, "江南", "Gangnam", 8.2, 11234, 420, "江南站旁,COEX附近,性價比高", "Near Gangnam Stn,COEX Nearby,Great Value", "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=500&h=300&fit=crop"),
    ],

    "Bangkok": [
        ("曼谷文華東方酒店", "Mandarin Oriental Bangkok", 5, "河畔", "Riverside", 9.6, 3456, 2800, "湄南河畔,百年歷史,頂級奢華", "Chao Phraya River,Century-old,Top Luxury", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("曼谷暹羅凱賓斯基酒店", "Siam Kempinski Hotel Bangkok", 5, "暹羅", "Siam", 9.4, 4567, 2200, "暹羅商圈,花園泳池,購物天堂", "Siam District,Garden Pool,Shopping Paradise", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
        ("素坤逸萬豪酒店", "Bangkok Marriott Sukhumvit", 5, "素坤逸", "Sukhumvit", 9.1, 6789, 1580, "Thonglor區,屋頂酒吧,時尚地段", "Thonglor Area,Rooftop Bar,Trendy Location", "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=500&h=300&fit=crop"),
        ("曼谷素坤逸希爾頓酒店", "DoubleTree by Hilton Sukhumvit", 4, "素坤逸", "Sukhumvit", 8.7, 9876, 680, "BTS站旁,夜市附近,交通便利", "Near BTS,Night Market,Convenient", "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=500&h=300&fit=crop"),
        ("考山路巴迪小屋酒店", "Buddy Lodge Khaosan", 3, "考山路", "Khaosan", 8.0, 12345, 280, "背包客天堂,夜生活,超值之選", "Backpacker Hub,Nightlife,Budget Pick", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
        ("華欣洲際酒店", "InterContinental Hua Hin", 5, "華欣", "Hua Hin", 9.2, 3456, 1880, "海灘度假,無邊際泳池,SPA", "Beach Resort,Infinity Pool,Spa", "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500&h=300&fit=crop"),
        ("曼谷阿索克諾富特酒店", "Novotel Bangkok Asoke", 4, "阿索克", "Asoke", 8.5, 8765, 580, "MRT/BTS雙站,Terminal 21旁", "MRT/BTS Dual Station,Near Terminal 21", "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=500&h=300&fit=crop"),
        ("曼谷Chatrium河畔酒店", "Chatrium Hotel Riverside", 5, "河畔", "Riverside", 8.8, 7654, 880, "湄南河景,免費渡輪,家庭友善", "River View,Free Shuttle Boat,Family Friendly", "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=500&h=300&fit=crop"),
    ],

    "Singapore": [
        ("濱海灣金沙酒店", "Marina Bay Sands", 5, "濱海灣", "Marina Bay", 9.3, 25678, 3200, "無邊際泳池,地標酒店,賭場", "Infinity Pool,Iconic,Casino", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("萊佛士酒店", "Raffles Singapore", 5, "市中心", "City Centre", 9.6, 4567, 4500, "殖民地風格,Singapore Sling發源地", "Colonial Style,Home of Singapore Sling", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
        ("烏節路文華酒店", "Mandarin Orchard Singapore", 5, "烏節路", "Orchard Rd", 8.8, 12345, 1680, "烏節路購物區,交通便利,商務首選", "Orchard Shopping,Convenient,Business Pick", "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=500&h=300&fit=crop"),
        ("聖淘沙名勝世界節慶酒店", "Resorts World Sentosa Festive Hotel", 4, "聖淘沙", "Sentosa", 8.6, 9876, 1280, "環球影城旁,親子首選,海灘", "Near USS,Family Pick,Beach", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
        ("牛車水宜必思酒店", "Ibis Singapore on Bencoolen", 3, "武吉士", "Bugis", 8.2, 15678, 580, "牛車水美食,交通便利,超值之選", "Chinatown Food,Convenient,Budget Pick", "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500&h=300&fit=crop"),
        ("嘉佩樂酒店聖淘沙", "Capella Singapore Sentosa", 5, "聖淘沙", "Sentosa", 9.5, 2345, 4800, "Trump-Kim峰會場地,頂級度假村", "Trump-Kim Summit Venue,Premium Resort", "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500&h=300&fit=crop"),
    ],

    "Taipei": [
        ("台北文華東方酒店", "Mandarin Oriental Taipei", 5, "松山", "Songshan", 9.5, 3456, 3200, "頂級奢華,SPA,米芝蓮餐廳", "Top Luxury,Spa,Michelin Dining", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("台北W酒店", "W Taipei", 5, "信義區", "Xinyi", 9.2, 5678, 2680, "信義商圈,101旁,潮流設計", "Xinyi District,Near 101,Trendy Design", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
        ("西門町德立莊酒店", "Hotel Midtown Richardson Ximending", 4, "西門町", "Ximending", 8.7, 12345, 580, "西門町核心,夜市旁,交通便利", "Central Ximending,Night Market,Convenient", "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=500&h=300&fit=crop"),
        ("北投日勝生加賀屋", "Kagaya Taipei", 5, "北投", "Beitou", 9.3, 4567, 3800, "日式溫泉,懷石料理,頂級旅館", "Japanese Onsen,Kaiseki Cuisine,Premium Ryokan", "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500&h=300&fit=crop"),
        ("台北君悅酒店", "Grand Hyatt Taipei", 5, "信義區", "Xinyi", 9.0, 8765, 2180, "101腳下,會展旁,城市景觀", "At Foot of 101,Near TWTC,City Views", "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=500&h=300&fit=crop"),
        ("西門町宿之酒店", "Cho Hotel Ximending", 4, "西門町", "Ximending", 8.5, 9876, 480, "設計酒店,西門町步行區,超值", "Design Hotel,Ximending Walk,Great Value", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
    ],

    "London": [
        ("倫敦麗思酒店", "The Ritz London", 5, "皮卡迪利", "Piccadilly", 9.5, 3456, 5800, "英式下午茶,皇家級奢華", "Afternoon Tea,Royal Luxury", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("倫敦香格里拉酒店", "Shangri-La The Shard London", 5, "碎片大廈", "The Shard", 9.4, 4567, 3800, "全倫敦最高酒店,360度景觀", "London's Highest Hotel,360° Views", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
        ("倫敦希爾頓帕丁頓", "Hilton London Paddington", 4, "帕丁頓", "Paddington", 8.5, 12345, 1580, "希斯路快線,交通樞紐,海德公園旁", "Heathrow Express,Transport Hub,Near Hyde Park", "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=500&h=300&fit=crop"),
        ("Premier Inn倫敦市中心", "Premier Inn London City Centre", 3, "南華克", "Southwark", 8.2, 18765, 680, "經濟之選,泰晤士河畔,Borough Market旁", "Budget Pick,Thames Riverside,Near Borough Market", "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500&h=300&fit=crop"),
        ("倫敦柯芬園酒店", "The NoMad London Covent Garden", 5, "柯芬園", "Covent Garden", 9.3, 2345, 3200, "西區劇院,歷史建築,精品酒店", "West End Theatre,Historic Building,Boutique", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
    ],

    "Paris": [
        ("巴黎麗思酒店", "Ritz Paris", 5, "旺多姆廣場", "Place Vendôme", 9.7, 2345, 7800, "可可香奈兒故居,頂級奢華", "Coco Chanel's Home,Ultimate Luxury", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("巴黎半島酒店", "The Peninsula Paris", 5, "凱旋門", "Arc de Triomphe", 9.5, 3456, 5200, "凱旋門旁,屋頂餐廳,城市全景", "Near Arc de Triomphe,Rooftop Dining,City Panorama", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
        ("巴黎歌劇院諾富特", "Novotel Paris Opera", 4, "歌劇院", "Opéra", 8.6, 9876, 1380, "老佛爺旁,購物便利,交通便利", "Near Galeries Lafayette,Shopping,Convenient", "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=500&h=300&fit=crop"),
        ("巴黎北站宜必思", "Ibis Paris Gare du Nord", 3, "北站", "Gare du Nord", 7.8, 15678, 580, "歐洲之星旁,超值之選", "Near Eurostar,Budget Pick", "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500&h=300&fit=crop"),
        ("巴黎鐵塔景觀酒店", "Pullman Paris Tour Eiffel", 4, "鐵塔區", "Eiffel Tower", 8.8, 7654, 1880, "鐵塔景觀,塞納河旁,浪漫首選", "Eiffel Tower View,Near Seine,Romantic Pick", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
    ],

    "Dubai": [
        ("帆船酒店", "Burj Al Arab Jumeirah", 5, "朱美拉", "Jumeirah", 9.7, 4567, 8800, "全球最奢華酒店,海上地標", "World's Most Luxurious,Iconic Landmark", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("亞特蘭蒂斯棕櫚酒店", "Atlantis The Palm", 5, "棕櫚島", "Palm Jumeirah", 9.3, 12345, 3200, "水上樂園,海豚灣,親子首選", "Waterpark,Dolphin Bay,Family Pick", "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500&h=300&fit=crop"),
        ("杜拜JW萬豪侯爵酒店", "JW Marriott Marquis Dubai", 5, "商業灣", "Business Bay", 9.1, 8765, 1880, "全球最高酒店之一,雙子塔", "World's Tallest Hotel,Twin Towers", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
        ("杜拜碼頭希爾頓酒店", "Hilton Dubai Jumeirah", 5, "JBR海灘", "JBR Beach", 8.8, 6789, 1580, "海灘步行可達,JBR Walk旁", "Beach Access,JBR Walk Nearby", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
        ("杜拜市區宜必思", "Ibis One Central Dubai", 3, "市中心", "Downtown", 8.2, 11234, 480, "哈利法塔旁,Dubai Mall附近,超值", "Near Burj Khalifa,Near Dubai Mall,Budget", "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500&h=300&fit=crop"),
    ],

    "Phuket": [
        ("布吉悅榕庄", "Banyan Tree Phuket", 5, "拉古納", "Laguna", 9.4, 3456, 2800, "私人泳池別墅,瀉湖景觀,SPA", "Private Pool Villa,Lagoon View,Spa", "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500&h=300&fit=crop"),
        ("芭東海灘希爾頓", "Hilton Phuket Arcadia", 5, "卡倫海灘", "Karon Beach", 8.8, 8765, 1280, "海灘度假村,5個泳池,親子", "Beach Resort,5 Pools,Family", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
        ("芭東假日酒店", "Holiday Inn Patong", 4, "芭東", "Patong", 8.5, 12345, 680, "芭東海灘旁,夜生活,購物", "Patong Beach,Nightlife,Shopping", "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=500&h=300&fit=crop"),
        ("布吉卡塔海灘度假村", "Kata Beach Resort", 4, "卡塔", "Kata", 8.3, 9876, 480, "寧靜海灘,浮潛,家庭友善", "Quiet Beach,Snorkeling,Family Friendly", "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=500&h=300&fit=crop"),
    ],

    "Bali": [
        ("峇里島四季酒店", "Four Seasons Bali at Sayan", 5, "烏布", "Ubud", 9.6, 2345, 3800, "叢林河谷,梯田景觀,瑜伽", "Jungle Valley,Rice Terrace View,Yoga", "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500&h=300&fit=crop"),
        ("峇里島阿雅娜度假村", "AYANA Resort Bali", 5, "金巴蘭", "Jimbaran", 9.3, 6789, 2200, "岩石酒吧,無邊際泳池,海灘", "Rock Bar,Infinity Pool,Beach", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("水明漾W酒店", "W Bali Seminyak", 5, "水明漾", "Seminyak", 9.1, 5432, 1880, "潮流海灘,日落酒吧,設計酒店", "Trendy Beach,Sunset Bar,Design Hotel", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
        ("庫塔海灘遺產酒店", "Kuta Beach Heritage Hotel", 3, "庫塔", "Kuta", 8.2, 11234, 280, "庫塔海灘旁,衝浪,超值之選", "Kuta Beach,Surfing,Budget Pick", "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500&h=300&fit=crop"),
    ],

    "New York": [
        ("紐約瑞吉酒店", "The St. Regis New York", 5, "第五大道", "Fifth Avenue", 9.5, 3456, 5800, "第五大道地標,管家服務", "Fifth Ave Landmark,Butler Service", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("紐約時代廣場萬豪", "Marriott Marquis Times Square", 4, "時代廣場", "Times Square", 8.7, 15678, 2200, "時代廣場核心,百老匯劇院", "Central Times Square,Broadway Theatre", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
        ("紐約中央公園1酒店", "1 Hotel Central Park", 5, "中央公園", "Central Park", 9.2, 4567, 3800, "中央公園景觀,環保設計酒店", "Central Park Views,Eco-Design Hotel", "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=500&h=300&fit=crop"),
        ("Pod 51酒店", "Pod 51 Hotel", 3, "中城", "Midtown", 8.0, 18765, 680, "膠囊酒店概念,超值之選,交通便利", "Pod Concept,Budget Pick,Convenient", "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500&h=300&fit=crop"),
        ("布魯克林威廉斯堡酒店", "The William Vale Brooklyn", 5, "威廉斯堡", "Williamsburg", 9.1, 5432, 2800, "曼哈頓天際線景觀,屋頂泳池", "Manhattan Skyline Views,Rooftop Pool", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
    ],

    "Sydney": [
        ("悉尼柏悅酒店", "Park Hyatt Sydney", 5, "岩石區", "The Rocks", 9.6, 3456, 4800, "歌劇院對面,海港大橋景觀", "Opposite Opera House,Harbour Bridge Views", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("悉尼洲際酒店", "InterContinental Sydney", 5, "環形碼頭", "Circular Quay", 9.2, 6789, 2800, "環形碼頭旁,歌劇院步行可達", "Near Circular Quay,Walk to Opera House", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
        ("達令港諾富特酒店", "Novotel Darling Harbour", 4, "達令港", "Darling Harbour", 8.6, 9876, 1380, "達令港景觀,水族館旁,家庭友善", "Harbour Views,Near Aquarium,Family Friendly", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
        ("悉尼宜必思世界廣場", "Ibis Sydney World Square", 3, "市中心", "CBD", 8.0, 15678, 580, "市中心,中國城旁,超值之選", "CBD Location,Near Chinatown,Budget Pick", "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500&h=300&fit=crop"),
    ],

    "Kuala Lumpur": [
        ("吉隆坡文華東方", "Mandarin Oriental KL", 5, "KLCC", "KLCC", 9.3, 5678, 1580, "雙子塔旁,城市公園景觀", "Next to Petronas Towers,Park Views", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("武吉免登JW萬豪", "JW Marriott Bukit Bintang", 5, "武吉免登", "Bukit Bintang", 9.0, 8765, 980, "購物街核心,亞羅街夜市旁", "Shopping Hub,Near Jalan Alor Night Market", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
        ("吉隆坡希爾頓雙威酒店", "Hilton KL Sentral", 4, "中央車站", "KL Sentral", 8.7, 11234, 580, "交通樞紐,機場快線直達", "Transport Hub,Direct Airport Express", "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=500&h=300&fit=crop"),
        ("唐人街探索者旅舍", "BackHome KL Chinatown", 2, "唐人街", "Chinatown", 8.0, 6789, 120, "茨廠街旁,背包客首選,超值", "Near Petaling Street,Backpacker Pick,Budget", "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500&h=300&fit=crop"),
    ],

    "Maldives": [
        ("馬爾代夫瑞吉度假村", "The St. Regis Maldives", 5, "達阿魯環礁", "Dhaalu Atoll", 9.7, 1234, 8800, "水上別墅,私人泳池,管家服務", "Overwater Villa,Private Pool,Butler", "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500&h=300&fit=crop"),
        ("索尼娃富士度假村", "Soneva Fushi", 5, "巴阿環礁", "Baa Atoll", 9.8, 987, 12000, "赤腳奢華,天文台,有機餐廳", "Barefoot Luxury,Observatory,Organic Dining", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&h=300&fit=crop"),
        ("安娜塔拉吉哈瓦度假村", "Anantara Kihavah", 5, "巴阿環礁", "Baa Atoll", 9.6, 2345, 7800, "水下餐廳,海龜保育,天文台", "Underwater Restaurant,Turtle Conservation", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500&h=300&fit=crop"),
        ("康萊德馬爾代夫", "Conrad Maldives Rangali", 5, "南阿里環礁", "South Ari", 9.4, 4567, 5800, "全球首間水下餐廳,雙島度假村", "First Underwater Restaurant,Twin Island Resort", "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500&h=300&fit=crop"),
    ],
}
