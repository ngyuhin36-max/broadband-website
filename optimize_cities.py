"""Wave 1: Optimize 12 city main hotel pages (6 cities x 2 languages).
- Remove all fake aggregateRating from Hotel schema
- Add BreadcrumbList schema
- Add FAQPage schema (city-specific, 6 Q&A)
- Add TravelAgency + TouristDestination schema
- Add geo meta (country / timezone)
"""
import re, json
from pathlib import Path

CITIES = {
    "BJ": {"zh": "北京", "en": "Beijing", "lat": 39.9042, "lng": 116.4074, "tz": "Asia/Shanghai", "country":"CN"},
    "GZ": {"zh": "廣州", "en": "Guangzhou", "lat": 23.1291, "lng": 113.2644, "tz": "Asia/Shanghai", "country":"CN"},
    "KH": {"zh": "高雄", "en": "Kaohsiung", "lat": 22.6273, "lng": 120.3014, "tz": "Asia/Taipei", "country":"TW"},
    "MO": {"zh": "澳門", "en": "Macau", "lat": 22.1987, "lng": 113.5439, "tz": "Asia/Macau", "country":"MO"},
    "SH": {"zh": "上海", "en": "Shanghai", "lat": 31.2304, "lng": 121.4737, "tz": "Asia/Shanghai", "country":"CN"},
    "TP": {"zh": "台北", "en": "Taipei", "lat": 25.0330, "lng": 121.5654, "tz": "Asia/Taipei", "country":"TW"},
}

# City-specific FAQs (zh + en) and attractions
CITY_CONTENT = {
    "BJ": {
        "faq_zh":[
            ("北京酒店平均幾錢一晚？","2026北京酒店價格：經濟型(如家/漢庭/7天) RMB¥200-400；3星商務 ¥400-800；4星 ¥800-1500；5星豪華(麗思/文華/寶格麗) ¥2000-8000+。黃金周(5月1日/10月1日)及春節加價 40-80%。"),
            ("北京邊間酒店近故宮？","步行可達：東方君悅(王府井)、北京飯店、麗思卡爾頓、柏悅、華爾道夫。地鐵1號線可直達天安門東站，再步行5分鐘入故宮。"),
            ("北京親子酒店推薦？","北京環球影城度假酒店、首旅諾金度假酒店(海洋世界)、北京環球大酒店(環球度假區)、六旗北京(家庭套房)、奧林匹克森林公園凱悅。"),
            ("北京機場酒店揀邊間？","步行/免費穿梭：首都機場希爾頓(T3 步行10分鐘)、北京首都機場希爾頓花園、昆泰酒店。大興機場近：北京大興希爾頓花園、洲際大興機場。"),
            ("北京商務出差住邊？","CBD 區：北京國貿大酒店、柏悅、凱賓斯基、麗思、東方君悅。金融街：金融街威斯汀、金融街麗思、北京金融街洲際。中關村：香格里拉、萬豪。"),
            ("北京長城附近有酒店嗎？","慕田峪長城附近：慕田峪小園(民宿)、石林苑度假村。八達嶺：八達嶺溫泉度假酒店。金山嶺：金山嶺溫泉度假村。建議租車或酒店專車前往。"),
        ],
        "faq_en":[
            ("How much does a Beijing hotel cost per night in 2026?","Budget chains (Home Inn, Hanting, 7 Days) RMB¥200-400; 3-star business ¥400-800; 4-star ¥800-1500; 5-star luxury (Ritz-Carlton, Bulgari, Mandarin) ¥2000-8000+. Golden Week (May 1, Oct 1) and CNY add 40-80%."),
            ("Which Beijing hotels are close to the Forbidden City?","Walking distance: Grand Hyatt (Wangfujing), Beijing Hotel, Ritz-Carlton, Park Hyatt, Waldorf Astoria. Metro Line 1 to Tiananmen East + 5 min walk."),
            ("Which Beijing hotels are best for families?","Universal Beijing Resort Hotel, NUO Resort (Aquarium), Universal Grand Hotel, Hyatt Regency Wangjing, Hyatt Regency Olympic Park Beijing."),
            ("Best Beijing airport hotels?","Capital Airport: Hilton Beijing Capital Airport (10-min walk T3), Hilton Garden Inn Airport. Daxing Airport: Hilton Garden Inn Daxing, InterContinental Daxing."),
            ("Where to stay in Beijing for business?","CBD: China World, Park Hyatt, Kempinski, Ritz-Carlton. Financial Street: Westin, Ritz, InterContinental. Zhongguancun: Shangri-La, Marriott."),
            ("Any hotels near the Great Wall?","Mutianyu: Brickyard Retreat. Badaling: Badaling Resort. Jinshanling: Jinshanling Hot Spring Resort. Rent a car or arrange hotel transfer."),
        ],
        "attractions":[("Forbidden City","故宮",39.9163,116.3972),("Great Wall - Badaling","八達嶺長城",40.3587,116.0132),("Tiananmen Square","天安門廣場",39.9055,116.3976),("Temple of Heaven","天壇",39.8822,116.4064),("Summer Palace","頤和園",39.9999,116.2755)],
    },
    "GZ": {
        "faq_zh":[
            ("廣州酒店平均幾錢一晚？","廣州酒店：經濟型 ¥200-400；3星商務 ¥400-700；4星 ¥700-1500；5星豪華(四季/文華/花園/WHotel) ¥1500-5000+。廣交會(4月15日/10月15日)加價 30-60%。"),
            ("廣州邊間酒店近沙面/上下九？","沙面島：白天鵝賓館(老牌5星)、嶺南會館(古典)。上下九：廣東大廈、全季上下九、7天連鎖。地鐵1/6號線沙面站直達。"),
            ("廣州塔附近酒店推薦？","四季酒店(珠江新城)、WHotel廣州、香格里拉、文華東方、麗思卡爾頓、廣州塔凱旋門。珠江新城CBD集中，夜景絕佳。"),
            ("廣交會住邊區最方便？","琶洲會展中心旁：琶洲萬豪、廣州希爾頓逸林琶洲、皇冠假日琶洲。廣交會免費穿梭巴士覆蓋主要商務酒店。"),
            ("廣州機場酒店揀邊間？","白雲機場旁：白雲機場鉑爾曼(T1直通)、白雲國際會議中心、華盛達等。搭機場快線約35分鐘到市區。"),
            ("廣州親子酒店推薦？","長隆酒店(夜賞熊貓)、長隆熊貓酒店、長隆鱷魚公園酒店、長隆迎賓館、保利皇冠假日(近長隆海洋王國)。"),
        ],
        "faq_en":[
            ("How much does a Guangzhou hotel cost per night?","Budget ¥200-400; 3-star ¥400-700; 4-star ¥700-1500; 5-star (Four Seasons, Mandarin, Garden, W) ¥1500-5000+. Canton Fair (Apr 15, Oct 15) adds 30-60%."),
            ("Hotels near Shamian Island / Shangxiajiu?","Shamian: White Swan Hotel (classic 5-star), Lingnan Club. Shangxiajiu: Guangdong Hotel, Ji Hotel, 7 Days. Metro Line 1/6 Shamian Station."),
            ("Hotels near Canton Tower?","Four Seasons Guangzhou (Pearl River), W Guangzhou, Shangri-La, Mandarin, Ritz-Carlton Guangzhou. Zhujiang New Town CBD with night skyline views."),
            ("Where to stay for Canton Fair?","Pazhou Expo area: Marriott Pazhou, DoubleTree Pazhou, Crowne Plaza Pazhou. Free shuttles to main business hotels."),
            ("Best Guangzhou airport hotels?","Baiyun Airport: Pullman Baiyun Airport (directly connected T1), Baiyun International Convention Centre. Airport Express 35 min to city."),
            ("Family hotels in Guangzhou?","Chimelong Hotel (pandas at night), Chimelong Panda Hotel, Chimelong Crocodile Hotel, Poly Crowne Plaza (near Chimelong Ocean Kingdom)."),
        ],
        "attractions":[("Canton Tower","廣州塔",23.1065,113.3180),("Shamian Island","沙面島",23.1070,113.2413),("Chimelong","長隆度假區",23.0047,113.3299),("Yuexiu Park","越秀公園",23.1378,113.2640),("Pearl River","珠江新城",23.1200,113.3250)],
    },
    "KH": {
        "faq_zh":[
            ("高雄酒店平均幾錢一晚？","高雄酒店：經濟 NT$800-1500；3星 NT$1500-3000；4星 NT$3000-5000；5星豪華(國賓/漢來/85大樓) NT$5000-12000+。春節/暑假加 30-50%。"),
            ("高雄邊間酒店近愛河/駁二？","愛河旁：高雄國賓大飯店、城市商旅愛河館、康橋商旅愛河館。駁二特區：摩西文旅、承億文旅高雄館、城市商旅駁二館。"),
            ("高雄85大樓住宿推薦？","君鴻國際酒店(85大樓39-85樓)、85大樓Sky樓、高雄萬豪酒店(近85大樓)。擁有全台最高景觀，可俯瞰高雄港。"),
            ("西子灣/旗津住邊？","西子灣：高雄西子灣沙灘會館、海琉秘境。旗津：旗津千禧海景飯店、旗津鯛魚燒民宿。步行或輪渡至景點。"),
            ("高雄親子酒店推薦？","承億文旅高雄館(親子主題)、義大天悅飯店(義大遊樂世界)、義大皇冠假日、夢時代旁的福容大飯店、麗尊酒店。"),
            ("高雄機場/左營高鐵站住哪？","小港機場：福華大飯店、小港機場格上租車。左營高鐵站：翰品酒店、禧樂商務、城市商旅高雄站前館。"),
        ],
        "faq_en":[
            ("How much does a Kaohsiung hotel cost?","Budget NT$800-1500; 3-star NT$1500-3000; 4-star NT$3000-5000; 5-star (Ambassador, Grand Hi-Lai, 85 Tower) NT$5000-12000+. CNY/summer adds 30-50%."),
            ("Hotels near Love River / Pier-2?","Love River: Ambassador Kaohsiung, City Suites Love River, Kingdom Hotel Love River. Pier-2: Moxy, Hotel Tai, City Suites Pier-2."),
            ("85 Sky Tower hotel options?","Grand Hi-Lai Hotel, 85 Sky Tower Hotel (floors 39-85), Kaohsiung Marriott. Tallest views in Taiwan overlooking Kaohsiung Harbour."),
            ("Sizihwan / Cijin hotels?","Sizihwan: Hotel Cozzi Sizihwan, The Lees Hotel. Cijin: Formosa Cijin Hotel, Cijin Taiyaki B&B. Walking / ferry to attractions."),
            ("Family hotels in Kaohsiung?","Hotel Dua (kids theme floor), E-Da Skylark Hotel (E-Da Theme Park), E-Da Royal Hotel, Fullon Hotel (Dream Mall), Royal Kaohsiung."),
            ("Kaohsiung airport / HSR Zuoying hotels?","Siaogang Airport: Howard Plaza, car-rental hotels. Zuoying HSR: Han-Hsien, Kindness Hotel, City Suites Kaohsiung Station."),
        ],
        "attractions":[("Love River","愛河",22.6270,120.2940),("85 Sky Tower","高雄85大樓",22.6115,120.3013),("Sizihwan","西子灣",22.6268,120.2649),("Pier-2","駁二藝術特區",22.6201,120.2800),("Dream Mall","夢時代",22.5957,120.3078)],
    },
    "MO": {
        "faq_zh":[
            ("澳門酒店平均幾錢一晚？","澳門酒店：3星 MOP$500-1000；4星 MOP$1000-2500；5星豪華(永利/新濠/四季) MOP$2500-8000+。週末加 30-80%。週日至週四平日最抵。"),
            ("澳門邊間酒店近大三巴？","議事亭前地步行：十六浦索菲特、澳門葡京(老牌)、萊斯酒店、澳門四季名薈。大三巴步行10分鐘內。"),
            ("澳門路氹度假區住邊？","澳門銀河綜合度假城(JW萬豪/悅榕莊/麗思)、威尼斯人、新濠影匯/天幕/龍馬、永利皇宮、新葡京、巴黎人、倫敦人。每間都有賭場+購物+秀。"),
            ("澳門親子酒店推薦？","威尼斯人(大運河)、新濠天地(水舞間)、新濠影匯(8字摩天輪)、巴黎人(艾菲爾鐵塔)、倫敦人(雙層巴士)、銀河(人造沙灘)、大倉酒店(日本主題)。"),
            ("澳門機場酒店哪家好？","麗世酒店(氹仔機場)、澳門麗思、威斯汀度假酒店(黑沙灣)、澳門銀河。機場搭免費穿梭巴士到主要酒店15-20分鐘。"),
            ("澳門港澳碼頭/橫琴口岸近邊？","港澳碼頭旁：十六浦、美高梅、永利。橫琴口岸：銀河、金沙城中心、新濠影匯。均有免費穿梭巴士覆蓋全澳門。"),
        ],
        "faq_en":[
            ("How much does a Macau hotel cost?","3-star MOP$500-1000; 4-star MOP$1000-2500; 5-star luxury (Wynn, Melco, Four Seasons) MOP$2500-8000+. Weekends add 30-80%. Sun-Thu weekdays cheapest."),
            ("Hotels near Ruins of St. Paul's?","Senado Square walkable: Sofitel Ponte 16, Grand Lisboa (classic), Rocks Hotel, Four Seasons Macao. St. Paul's within 10 min walk."),
            ("Cotai Strip resort hotels?","Galaxy (JW Marriott / Banyan Tree / Ritz-Carlton), Venetian, Studio City / Morpheus / Dragon, Wynn Palace, Grand Lisboa Palace, Parisian, Londoner. Each has casino+mall+shows."),
            ("Family hotels in Macau?","Venetian (Grand Canal), City of Dreams (House of Dancing Water), Studio City (8-shaped Ferris wheel), Parisian (Eiffel Tower), Londoner (double-decker), Galaxy (artificial beach), Okura Macau (Japanese theme)."),
            ("Macau airport hotels?","Regency Art Hotel Taipa (near airport), Ritz-Carlton Macau, Grand Coloane Beach Resort, Galaxy. Free shuttle buses to major hotels 15-20 min."),
            ("Near ferry terminal / Hengqin border?","Outer Harbour Ferry: Ponte 16, MGM, Wynn. Hengqin Border: Galaxy, Sands Cotai Central, Studio City. All offer free shuttles citywide."),
        ],
        "attractions":[("Ruins of St. Paul's","大三巴",22.1975,113.5407),("Senado Square","議事亭前地",22.1937,113.5407),("Venetian Macao","威尼斯人",22.1469,113.5621),("Macau Tower","澳門旅遊塔",22.1763,113.5390),("A-Ma Temple","媽閣廟",22.1864,113.5323)],
    },
    "SH": {
        "faq_zh":[
            ("上海酒店平均幾錢一晚？","上海酒店：經濟型(如家/漢庭) ¥300-500；3星商務 ¥500-1000；4星 ¥1000-2500；5星豪華(外灘華爾道夫/半島/寶格麗/和平飯店) ¥2500-10000+。"),
            ("上海邊間酒店近外灘？","外灘邊：外灘華爾道夫、和平飯店、半島、W酒店外灘、費爾蒙和平飯店、浦西萬怡。地鐵2/10號線南京東路站步行5分鐘。"),
            ("上海迪士尼住哪方便？","迪士尼度假區酒店：上海迪士尼樂園酒店、玩具總動員酒店(2023新)。度假區外：浦東文華、南匯萬麗、上海浦東嘉里大酒店。"),
            ("上海親子酒店推薦？","上海迪士尼酒店、玩具總動員、海昌海洋公園酒店(水族館景)、東方綠舟溫泉、月湖雕塑公園酒店、歡樂谷瑪雅酒店。"),
            ("陸家嘴/浦東商務酒店揀邊間？","四季酒店(浦東)、金茂君悅、柏悅、麗思卡爾頓、浦東香格里拉、麗華東方。金茂大廈/環球金融中心/上海中心直通。"),
            ("上海機場酒店揀邊間？","虹橋機場：虹橋元一希爾頓、萬豪虹橋、浦西洲際。浦東機場：浦東機場華美達、浦東機場凱悅(T1直通)、空港大酒店。"),
        ],
        "faq_en":[
            ("How much does a Shanghai hotel cost?","Budget (Home Inn/Hanting) ¥300-500; 3-star ¥500-1000; 4-star ¥1000-2500; 5-star luxury (Waldorf Bund, Peninsula, Bulgari, Fairmont Peace) ¥2500-10000+."),
            ("Hotels near The Bund?","Bund-side: Waldorf Astoria, Fairmont Peace Hotel, Peninsula, W The Bund, Indigo Bund. Metro 2/10 Nanjing East Road Station 5 min walk."),
            ("Where to stay for Shanghai Disney?","Resort: Shanghai Disneyland Hotel, Toy Story Hotel (2023 new). Nearby: Mandarin Pudong, Renaissance Nanhui, Kerry Pudong."),
            ("Family hotels in Shanghai?","Shanghai Disneyland Hotel, Toy Story Hotel, Haichang Ocean Park Hotel (aquarium views), Oriental Green Boat Resort, Moon Lake Sculpture Park Hotel."),
            ("Lujiazui / Pudong business hotels?","Four Seasons Pudong, Grand Hyatt Jin Mao, Park Hyatt (SWFC), Ritz-Carlton Pudong, Shangri-La Pudong, Mandarin Oriental. Direct connections to Jin Mao/SWFC/Shanghai Tower."),
            ("Shanghai airport hotels?","Hongqiao: Hilton Hongqiao, Marriott Hongqiao, InterContinental Puxi. Pudong: Ramada Pudong, Hyatt Pudong Airport (T1 direct), Airport Hotel."),
        ],
        "attractions":[("The Bund","外灘",31.2398,121.4907),("Oriental Pearl Tower","東方明珠",31.2397,121.4994),("Shanghai Disneyland","上海迪士尼",31.1436,121.6575),("Yuyuan","豫園",31.2268,121.4920),("Nanjing Road","南京路",31.2352,121.4750)],
    },
    "TP": {
        "faq_zh":[
            ("台北酒店平均幾錢一晚？","台北酒店：背包客棧 NT$800-1500；3星 NT$1500-3000；4星 NT$3000-5500；5星豪華(文華東方/君悅/W/寒舍艾麗) NT$5500-15000+。過年/寒暑假加 30-60%。"),
            ("台北邊間酒店近台北101/信義區？","信義區：台北W酒店、寒舍艾麗、寒舍艾美、君悅(101步行5分鐘)、文華東方(敦化北路)、君品酒店(京站)。"),
            ("台北車站/西門町住邊？","台北車站：凱撒大飯店、君品、洛碁、天成。西門町：絲柏汽車旅館、町・草休閒旅店、美麗信、艾瑞斯商旅。"),
            ("台北夜市附近住哪好？","士林夜市：台北美麗信、圓山飯店、士林夜旅館。饒河街夜市：君品、大地酒店。寧夏夜市：凱薩、城市商旅南西館。"),
            ("台北機場酒店揀邊間？","桃園機場：大溪笠復威斯汀、諾富特桃園機場。松山機場(市內)：松山機場旁大地酒店、台北萬怡。建議選桃園機場快線台北站酒店。"),
            ("台北親子酒店推薦？","台北圓山大飯店(溜滑梯房)、豪麗邸(主題家庭房)、北投春天酒店(溫泉)、陽明山中國麗緻、劍湖山王子飯店、北投老爺會館。"),
        ],
        "faq_en":[
            ("How much does a Taipei hotel cost?","Hostels NT$800-1500; 3-star NT$1500-3000; 4-star NT$3000-5500; 5-star (Mandarin, Hyatt, W, Sherwood, Le Meridien) NT$5500-15000+. CNY/holidays add 30-60%."),
            ("Hotels near Taipei 101 / Xinyi?","Xinyi: W Taipei, Sherwood, Le Meridien, Grand Hyatt (5-min walk to 101), Mandarin Oriental (Dunhua), Palais de Chine."),
            ("Taipei Main Station / Ximending hotels?","Main Station: Caesar Park, Palais de Chine, Cosmos, Cosmos Creation. Ximending: Cypress Hotel, Chaiin Hotel, Miramar Garden, Hotel Éclat."),
            ("Hotels near night markets?","Shilin: Miramar Garden, Grand Hotel, Shilin Night Inn. Raohe: Palais de Chine, The Gaia Hotel. Ningxia: Caesar Park, City Suites Nanxi."),
            ("Taipei airport hotels?","Taoyuan Airport: Novotel Taipei Taoyuan, The Westin Taoyuan. Songshan (in-city): The Gaia Taipei, Courtyard Taipei. Choose hotels near HSR Taipei Station for convenience."),
            ("Family hotels in Taipei?","Grand Hotel Taipei (slide rooms), Hualis Hotel (theme family rooms), Spring City Resort Beitou (hot spring), Chinese Culture Hotel (Yangmingshan), Janfusun Prince, Villa 32 Beitou."),
        ],
        "attractions":[("Taipei 101","台北101",25.0336,121.5645),("Shilin Night Market","士林夜市",25.0879,121.5239),("National Palace Museum","故宮博物院",25.1024,121.5484),("Ximending","西門町",25.0421,121.5068),("Chiang Kai-shek Memorial","中正紀念堂",25.0367,121.5210)],
    },
}

def build_geo(city, lang):
    c = CITIES[city]; content = CITY_CONTENT[city]
    is_zh = lang == "zh"
    url = f"https://broadbandhk.com/pages/{city}hotel{'-en' if not is_zh else ''}.html"
    alt_url = f"https://broadbandhk.com/pages/{city}hotel{'' if not is_zh else '-en'}.html"
    loc = c["zh"] if is_zh else c["en"]
    cname = f"{loc}酒店推介格價比較" if is_zh else f"{c['en']} Hotels Price Comparison"

    travel = {
        "@context":"https://schema.org","@type":"TravelAgency",
        "name": cname,
        "description": f"2026 {loc}酒店格價比較平台" if is_zh else f"2026 {c['en']} hotels price comparison platform",
        "url": url, "image":"https://broadbandhk.com/og-image.png",
        "priceRange":"varied",
        "address":{"@type":"PostalAddress","addressLocality":loc,"addressCountry":c["country"]},
        "geo":{"@type":"GeoCoordinates","latitude":c["lat"],"longitude":c["lng"]},
        "hasMap": f"https://www.google.com/maps/place/{loc}",
        "areaServed":{"@type":"City","name":loc,"geo":{"@type":"GeoCoordinates","latitude":c["lat"],"longitude":c["lng"]}},
    }
    dest = {
        "@context":"https://schema.org","@type":"TouristDestination",
        "name": loc, "url": url,
        "geo":{"@type":"GeoCoordinates","latitude":c["lat"],"longitude":c["lng"]},
        "touristType":["Business","Family","Couple","Luxury","Backpacker"] if not is_zh else ["商務","親子","情侶","豪華","背包客"],
        "includesAttraction":[
            {"@type":"TouristAttraction","name":(zh if is_zh else en),
             "geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lng}}
            for en,zh,lat,lng in content["attractions"]
        ],
        "subjectOf":{"@type":"WebPage","url":url}
    }
    breadcrumb = {
        "@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"首頁" if is_zh else "Home","item":"https://broadbandhk.com/"},
            {"@type":"ListItem","position":2,"name":"旅遊酒店" if is_zh else "Travel Hotels","item":url},
            {"@type":"ListItem","position":3,"name":f"{loc}酒店" if is_zh else f"{c['en']} Hotels"}
        ]}
    faq_items = content["faq_zh"] if is_zh else content["faq_en"]
    faq = {
        "@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
            for q,a in faq_items
        ]}
    return travel, dest, breadcrumb, faq, alt_url

def jdump(d): return json.dumps(d, ensure_ascii=False)

for city in CITIES:
    for lang in ("zh","en"):
        suf = "" if lang == "zh" else "-en"
        p = Path(f"pages/{city}hotel{suf}.html")
        if not p.exists(): continue
        s = p.read_text(encoding="utf-8")

        # Remove fake aggregateRating
        s = re.sub(r',"aggregateRating":\{"@type":"AggregateRating"[^}]+\}', '', s)

        travel, dest, breadcrumb, faq, alt_url = build_geo(city, lang)
        new_blocks = (
            f'    <script type="application/ld+json">{jdump(travel)}</script>\n'
            f'    <script type="application/ld+json">{jdump(breadcrumb)}</script>\n'
            f'    <script type="application/ld+json">{jdump(faq)}</script>\n'
            f'    <script type="application/ld+json">{jdump(dest)}</script>\n'
        )

        # Add extra GEO meta after ICBM (or after geo.position)
        c = CITIES[city]
        extra = (
            f'    <meta name="geo.country" content="{c["country"]}">\n'
            f'    <meta name="DC.coverage.spatial" content="{c["en"]}">\n'
            f'    <meta name="timezone" content="{c["tz"]}">\n'
            f'    <link rel="alternate" hreflang="{"en" if lang == "zh" else "zh-Hant-HK"}" href="{alt_url}">\n'
        )
        # Inject after ICBM meta
        s = re.sub(r'(<meta name="ICBM"[^>]+>\n)',
                   lambda m: m.group(1) + extra, s, count=1)

        # Inject new schemas before <style>
        s = re.sub(r'(\s*<style>)', r'\n' + new_blocks + r'\1', s, count=1)

        p.write_text(s, encoding="utf-8")
        print(f"optimized {city}hotel{suf}.html")
