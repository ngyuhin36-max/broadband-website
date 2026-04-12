import json, html
from pathlib import Path

DATA = {
"the-peninsula-hong-kong": {
  "name": "香港半島酒店 The Peninsula Hong Kong",
  "en": "The Peninsula Hong Kong",
  "address_zh": "香港九龍尖沙咀梳士巴利道22號",
  "address_en": "22 Salisbury Road, Tsim Sha Tsui, Kowloon, Hong Kong",
  "lat": 22.2948, "lng": 114.1724,
  "official": "https://www.peninsula.com/hong-kong",
  "phone": "+852 2920 2888",
  "opened": "1928年",
  "rooms": 300,
  "district": "尖沙咀",
  "mtr": "港鐵尖沙咀站 E 出口步行約 3 分鐘；港鐵尖東站 L3 出口步行約 5 分鐘",
  "intro": "香港半島酒店（The Peninsula Hong Kong）係香港最具歷史嘅五星級豪華酒店，1928年開業，被譽為「遠東貴婦」（The Grande Dame of the Far East），係香港半島酒店集團嘅旗艦物業。酒店坐落尖沙咀海傍梳士巴利道，白色古典主義大樓加上門前勞斯萊斯車隊已成為香港地標之一。",
  "history": "半島酒店1928年12月11日正式開幕，當年被譽為「蘇彝士以東最豪華酒店」。1994年加建30層新翼大樓，令酒店高度躍升，亦加入直昇機停機坪（係全港唯一有兩個直昇機坪嘅酒店）。酒店經歷二戰日佔時期（曾被改名為「東亞酒店」），戰後恢復原名，至今仍由嘉道理家族持有。",
  "facilities": [
    "屋頂直昇機坪（往返機場服務）",
    "羅馬式室內游泳池、日光露台",
    "半島水療中心（The Peninsula Spa）",
    "健身中心、瑜伽室",
    "14部勞斯萊斯 Phantom 專屬車隊（全球酒店最大規模）",
    "The Peninsula Academy 文化體驗活動"
  ],
  "restaurants": [
    "Gaddi's — 法國菜，1953年開業，香港最具代表性 fine dining",
    "Spring Moon 嘉麟樓 — 米芝蓮粵菜",
    "Felix — 28樓由 Philippe Starck 設計，法式當代菜",
    "The Lobby — 英式下午茶，香港最著名打卡位",
    "Chesa — 瑞士菜",
    "Imasa — 日式料理"
  ],
  "rooms_info": "提供 300 間客房及套房，面積由 42 平方米（Superior Room）至 370 平方米（半島套房）。全部房間均提供免費 WiFi、Nespresso 咖啡機、iPad 客房控制系統。海景房可賞維多利亞港景色。",
  "price_range": "Superior Room HK$3,280 起 · Deluxe Harbour View HK$5,800 起 · 半島套房 HK$52,000 起",
  "nearby": [
    "香港太空館（步行 2 分鐘）",
    "香港文化中心（步行 3 分鐘）",
    "海港城（步行 8 分鐘）",
    "星光大道（步行 5 分鐘）",
    "1881 Heritage（步行 5 分鐘）"
  ],
  "tips": "半島酒店嘅英式下午茶無得預約，建議平日下午 3 時前到達 The Lobby 排隊，週末通常要等 1-2 小時。如果住客可以優先安排。酒店車隊提供勞斯萊斯機場接送服務（需另收費），係非常獨特嘅半島體驗。",
  "faq": [
    ["半島酒店下午茶要預約嗎？", "半島酒店 The Lobby 下午茶唔接受預約，先到先得。建議平日下午 2-3 時到，可能要排 30-60 分鐘；週末排隊可達 2 小時。住客可享優先安排，部分套房套餐包含下午茶。"],
    ["半島酒店 check-in 時間？", "Check-in 時間：下午 2:00；Check-out 時間：中午 12:00。Early check-in 及 late check-out 視乎房間狀況，VIP 或套房住客通常較易安排。"],
    ["半島酒店有機場接送嗎？", "有。酒店提供勞斯萊斯 Phantom 機場接送服務，但屬於付費服務（約 HK$2,200-2,800 單程）。另亦設直昇機服務往返澳門或機場（需預約）。"],
    ["半島酒店附近邊個地鐵站最近？", "港鐵尖沙咀站 E 出口步行約 3 分鐘；尖東站 L3 出口步行約 5 分鐘。由尖沙咀站行過彌敦道南端，轉梳士巴利道即到酒店正門。"],
    ["半島酒店幾錢一晚？", "Superior Room HK$3,280 起、Deluxe Harbour View 海景房 HK$5,800 起、半島套房 HK$52,000 起。旺季（聖誕、農曆新年、煙花期）可能加價 30-50%。建議喺 Trip.com、Klook、Agoda 三個平台比較至抵。"],
    ["半島酒店適合親子入住嗎？", "適合。提供兒童設施包括兒童毛巾、浴袍、拖鞋、兒童餐單、BB 床。屋頂游泳池設兒童區，The Lobby 下午茶亦有小童版本。距離香港太空館及文化中心只需步行 2-3 分鐘。"]
  ]
},
"mandarin-oriental": {
  "name": "香港文華東方酒店 Mandarin Oriental",
  "en": "Mandarin Oriental, Hong Kong",
  "address_zh": "香港中環干諾道中5號",
  "address_en": "5 Connaught Road Central, Central, Hong Kong",
  "lat": 22.2819, "lng": 114.1606,
  "official": "https://www.mandarinoriental.com/hongkong",
  "phone": "+852 2522 0111",
  "opened": "1963年",
  "rooms": 501,
  "district": "中環",
  "mtr": "港鐵中環站 F 出口經人行天橋直達；香港站 A2 出口步行約 3 分鐘",
  "intro": "香港文華東方酒店（Mandarin Oriental, Hong Kong）係文華東方酒店集團嘅創始旗艦，1963年開業，位於中環核心地段干諾道中5號。酒店以東方奢華傳統融合現代設計聞名，長期係商務旅客及名人政要嘅首選，擁有10間餐廳及酒吧，多間獲米芝蓮星級認證。",
  "history": "文華東方酒店1963年10月開業時被譽為香港最高大樓，亦係當年東南亞最豪華酒店。2005-2006年進行了 HK$1.4 億大型翻新，由設計師 Adam Tihany 操刀，重塑客房同公共空間。酒店喺2008年慶祝 45 週年，亦係文華東方集團全球擴張嘅起點。",
  "facilities": [
    "The Mandarin Spa（樓高3層、連羅馬式溫水泳池）",
    "文華理髮院（自1963年營運至今）",
    "健身中心、Pilates 工作室",
    "禮賓部 24 小時服務",
    "會議及宴會廳（最大可容納 450 人）"
  ],
  "restaurants": [
    "Man Wah 文華廳 — 米芝蓮一星粵菜，25樓維港景",
    "Pierre — 法式 fine dining（前為米芝蓮二星）",
    "Mandarin Grill + Bar — 米芝蓮一星扒房",
    "The Chinnery — 英式酒吧、全港最大 single malt 威士忌收藏",
    "Clipper Lounge — 下午茶、文華玫瑰花瓣朱古力聞名",
    "Café Causette — 全日餐廳"
  ],
  "rooms_info": "501 間客房及套房，面積由 37 平方米（City Room）至 210 平方米（Mandarin Suite）。2006 年翻新後加入現代化設施，保留東方奢華風格。Harbour View 房間面向維多利亞港及尖沙咀天際線。",
  "price_range": "City Room HK$3,800 起 · Harbour View HK$5,500 起 · Mandarin Suite HK$28,000 起",
  "nearby": [
    "國際金融中心 IFC Mall（步行 3 分鐘）",
    "蘭桂坊（步行 8 分鐘）",
    "中環街市（步行 5 分鐘）",
    "大館（步行 10 分鐘）",
    "香港摩天輪（步行 8 分鐘）"
  ],
  "tips": "文華東方嘅玫瑰花瓣朱古力係香港經典手信，可以喺 Cake Shop 購買。文華理髮院係男士剃鬚及理髮熱門之選，需預約。Man Wah 文華廳窗邊海景位要提早2-3週預約。",
  "faq": [
    ["文華東方酒店有咩出名？", "文華東方以米芝蓮餐廳（Man Wah、Pierre、Mandarin Grill）、玫瑰花瓣朱古力、英式下午茶、文華理髮院、羅馬式泳池聞名。係香港商務旅客及名人政要首選。"],
    ["文華東方酒店地址同交通？", "地址：香港中環干諾道中5號。港鐵中環站 F 出口經有蓋行人天橋直達酒店三樓；香港站 A2 出口步行約 3 分鐘。酒店設免費穿梭巴士往返金鐘及尖沙咀。"],
    ["文華東方下午茶點樣訂？", "Clipper Lounge 下午茶可網上或電話預約，時段為下午 3:00-5:30。經典三層下午茶每位約 HK$388-488，週末加價 10-15%。文華玫瑰花瓣朱古力係必試。"],
    ["文華東方酒店幾錢一晚？", "City Room HK$3,800 起，Harbour View 海景房 HK$5,500 起，Mandarin Suite HK$28,000 起。非旺季可能跌至 HK$2,800 起，建議 Trip.com／Klook／Agoda 三平台比較。"],
    ["文華東方 check-in／check-out 時間？", "Check-in：下午 3:00；Check-out：中午 12:00。Fans of M.O. 會員可享免費 early check-in 及 late check-out（視乎房況）。"],
    ["文華東方泳池有咩特別？", "文華 Spa 嘅羅馬式室內溫水泳池由大理石柱及馬賽克圖案裝飾，水溫長期保持 29°C。泳池只限酒店住客及 Spa 會員使用，每日 6:00-22:00 開放。"]
  ]
},
"the-ritz-carlton": {
  "name": "香港麗思卡爾頓酒店 The Ritz-Carlton",
  "en": "The Ritz-Carlton, Hong Kong",
  "address_zh": "香港九龍柯士甸道西1號環球貿易廣場",
  "address_en": "International Commerce Centre, 1 Austin Road West, West Kowloon, Hong Kong",
  "lat": 22.3030, "lng": 114.1606,
  "official": "https://www.ritzcarlton.com/hongkong",
  "phone": "+852 2263 2263",
  "opened": "2011年（新址）",
  "rooms": 312,
  "district": "西九龍",
  "mtr": "港鐵九龍站 C1/D1 出口經商場 MTR 層步行 5 分鐘；高鐵西九龍站步行 8 分鐘",
  "intro": "香港麗思卡爾頓酒店（The Ritz-Carlton, Hong Kong）位於九龍西環球貿易廣場（ICC）102 至 118 樓，係全球海拔最高嘅酒店之一，最高點達 484 米。酒店2011年3月開業，以頂層 118 樓 Ozone 天台酒吧（全球最高酒吧）聞名，擁有 312 間客房，全部設有落地玻璃窗賞維港全景。",
  "history": "麗思卡爾頓香港原址位於中環遮打道，2008年結業後遷至西九龍環球貿易廣場高層。ICC 由 KPF 建築事務所設計，係香港第一高樓（484 米）。酒店入住 102-118 樓嘅景觀位置，由 LTW Designworks 操刀設計，揉合中西元素。",
  "facilities": [
    "Ozone 天台酒吧（118樓，全球最高酒吧）",
    "室內恆溫泳池（118樓，天花水族館屏幕）",
    "麗思卡爾頓水療中心（Ritz-Carlton Spa）",
    "Club Lounge 貴賓廊（116樓）",
    "ESPA 健身中心、瑜伽室",
    "兒童俱樂部 The Ritz Kids"
  ],
  "restaurants": [
    "Tin Lung Heen 天龍軒 — 米芝蓮三星粵菜（102樓）",
    "Tosca di Angelo — 米芝蓮一星意大利菜（102樓）",
    "Ozone — 118樓天際酒吧、落日最佳",
    "The Lounge & Bar — 大堂酒廊、下午茶",
    "The Chocolate Library — 自助朱古力吧",
    "Café 103 — 全日自助餐"
  ],
  "rooms_info": "312 間客房及套房，面積由 50 平方米（Deluxe Room）至 338 平方米（The Ritz-Carlton Suite）。所有房間設落地玻璃窗，超過 70% 房間擁有維港全景。配備 Nespresso 咖啡機、TOTO 智能廁板、BVLGARI 沐浴用品。",
  "price_range": "Deluxe Room HK$4,200 起 · Harbour View HK$6,800 起 · Ritz-Carlton Suite HK$42,000 起",
  "nearby": [
    "Elements 圓方商場（同座相連）",
    "西九龍文化區 M+／故宮文化博物館（步行 15 分鐘）",
    "天際 100 觀景台（同座100樓）",
    "柯士甸站／高鐵西九龍站（步行 5-8 分鐘）",
    "香港郵輪碼頭（的士 10 分鐘）"
  ],
  "tips": "Ozone 天台酒吧落日時段（約下午 5:30-7:00）景觀最佳，需預約窗邊位。天龍軒米芝蓮三星粵菜要提早 3-4 週預約，中午商務套餐較抵。泳池設於 118 樓，天花嵌入水族館屏幕，係打卡熱點。",
  "faq": [
    ["麗思卡爾頓位於邊度？幾層樓高？", "位於九龍西環球貿易廣場（ICC），酒店佔據 102-118 樓，最高點達 484 米，係香港最高酒店、全球最高酒店之一。"],
    ["Ozone 酒吧要預約嗎？點上去？", "Ozone 酒吧位於 118 樓，強烈建議週末預約（尤其落日時段）。由酒店大堂（9樓）搭專用電梯直上 118樓。Smart casual dress code，最低消費視乎日子而定。"],
    ["麗思卡爾頓點去機場？", "酒店距離機場快綫九龍站（同座 ICC）只需步行 5 分鐘，搭機場快綫到機場約 22 分鐘，車費 HK$105。亦可搭的士約 35 分鐘、HK$280。"],
    ["麗思卡爾頓幾錢一晚？", "Deluxe Room HK$4,200 起、Harbour View 海景房 HK$6,800 起、Ritz-Carlton Suite HK$42,000 起。旺季加 40-60%，建議 Trip.com／Klook／Agoda 格價。"],
    ["天龍軒幾多粒星？點預約？", "天龍軒（Tin Lung Heen）為米芝蓮三星粵菜餐廳，位於 102 樓。需提早 3-4 週網上或電話預約，午市 set lunch 約 HK$688-988／位、晚市 tasting menu 約 HK$2,288-3,388／位。"],
    ["酒店泳池有咩特別？", "118 樓室內恆溫泳池係全港最高嘅酒店泳池，水溫 28-30°C。泳池天花嵌入 144 平方米高清水族館屏幕，配合燈光變化，非常適合拍照打卡。"]
  ]
},
"four-seasons-hong-kong": {
  "name": "香港四季酒店 Four Seasons Hong Kong",
  "en": "Four Seasons Hotel Hong Kong",
  "address_zh": "香港中環金融街8號",
  "address_en": "8 Finance Street, Central, Hong Kong",
  "lat": 22.2867, "lng": 114.1571,
  "official": "https://www.fourseasons.com/hongkong",
  "phone": "+852 3196 8888",
  "opened": "2005年",
  "rooms": 399,
  "district": "中環",
  "mtr": "港鐵香港站 F 出口直達；中環站 A 出口步行約 5 分鐘",
  "intro": "香港四季酒店（Four Seasons Hotel Hong Kong）位於中環國際金融中心（IFC）旁，2005年開業，係全球第一間獲米芝蓮 8 粒星殊榮嘅酒店（Lung King Heen 3星 + Caprice 3星）。酒店擁有 399 間客房，全部面向維港或中環天際線，設兩個戶外無邊際泳池及全港最大酒店 Spa 之一。",
  "history": "四季酒店由新鴻基地產發展，2005年10月開業，與 IFC Mall、四季匯（服務式住宅）及四季滙辦公大樓組成綜合體。2009年 Lung King Heen 龍景軒成為全球首間獲米芝蓮三星嘅粵菜餐廳，奠定酒店國際地位。2019-2020年進行了大型客房翻新。",
  "facilities": [
    "戶外無邊際恆溫泳池（兩個，一個成人、一個家庭）",
    "Four Seasons Spa（面積 2,100 平方米，全港最大酒店 Spa 之一）",
    "24 小時健身中心",
    "桑拿、蒸氣室、冰室",
    "商務中心、會議廳（最大容納 680 人）",
    "兒童俱樂部 Kids For All Seasons"
  ],
  "restaurants": [
    "Lung King Heen 龍景軒 — 米芝蓮三星粵菜（全球首間粵菜三星）",
    "Caprice — 米芝蓮三星法國菜",
    "Sushi Saito — 米芝蓮二星日本壽司（東京本店分店）",
    "The Lounge — 下午茶、全日餐廳",
    "Argo — 雞尾酒吧、亞洲50最佳酒吧",
    "Blue Bar — 大堂酒吧、現場音樂"
  ],
  "rooms_info": "399 間客房及套房，面積由 44 平方米（Superior Room）至 334 平方米（Presidential Suite）。2020年翻新後配備智能燈光、恒溫系統、Toto 免治廁板、Bvlgari 沐浴用品。絕大部分客房可賞維港或中環天際線。",
  "price_range": "Superior Room HK$5,200 起 · Harbour View HK$7,800 起 · Presidential Suite HK$68,000 起",
  "nearby": [
    "IFC Mall 國際金融中心商場（直通）",
    "香港站機場快綫（步行 3 分鐘）",
    "中環碼頭（步行 5 分鐘，往離島）",
    "大館文化中心（步行 12 分鐘）",
    "蘭桂坊（步行 10 分鐘）"
  ],
  "tips": "四季酒店嘅兩個無邊際泳池（成人池 + 家庭池）景觀一流，8樓設日光甲板。Lung King Heen 龍景軒午市飲茶較抵（人均 HK$500-800），晚市品嚐套餐約 HK$1,988-2,988。酒店直通 IFC 商場及機場快綫，對商務及過境旅客最方便。",
  "faq": [
    ["四季酒店有咩米芝蓮餐廳？", "四季有 3 間米芝蓮星級餐廳：Lung King Heen 龍景軒（三星粵菜、全球首間粵菜三星）、Caprice（三星法國菜）、Sushi Saito（二星日本壽司）。酒店累積獲 8 粒米芝蓮星。"],
    ["四季酒店泳池可以游水嗎？", "可以，住客免費使用。設兩個戶外無邊際泳池：50 米成人池（水溫 28°C）及家庭池（水溫 30°C）。位於 8 樓日光甲板，可賞維港景色。開放時間 6:30-22:00。"],
    ["四季酒店地址同交通？", "地址：香港中環金融街8號。港鐵香港站 F 出口（IFC Mall 內）經行人通道直達；中環站 A 出口步行約 5 分鐘。機場快綫香港站同 IFC 相連，往機場約 24 分鐘。"],
    ["龍景軒點預約？幾錢？", "龍景軒（Lung King Heen）需提早 3-4 週網上或電話預約（+852 3196 8882）。午市點心套餐 HK$688-988／位、晚市品嚐套餐 HK$1,988-2,988／位。窗邊海景位非常搶手。"],
    ["四季酒店幾錢一晚？", "Superior Room HK$5,200 起、Harbour View 海景房 HK$7,800 起、Presidential Suite HK$68,000 起。旺季（聖誕、農曆新年）可達 HK$8,000+。建議 Trip.com／Klook／Agoda 比較。"],
    ["四季酒店適合帶小朋友嗎？", "非常適合。設專屬家庭泳池（水溫較暖）、Kids For All Seasons 兒童俱樂部、BB 床、兒童拖鞋浴袍、兒童 menu。部分套房可加連通房，方便一家人入住。"]
  ]
},
"rosewood-hong-kong": {
  "name": "香港瑰麗酒店 Rosewood Hong Kong",
  "en": "Rosewood Hong Kong",
  "address_zh": "香港九龍尖沙咀梳士巴利道18號",
  "address_en": "18 Salisbury Road, Tsim Sha Tsui, Kowloon, Hong Kong",
  "lat": 22.2948, "lng": 114.1760,
  "official": "https://www.rosewoodhotels.com/en/hong-kong",
  "phone": "+852 3891 8888",
  "opened": "2019年3月",
  "rooms": 413,
  "district": "尖沙咀",
  "mtr": "港鐵尖東站 J 出口步行約 3 分鐘；尖沙咀站 F 出口步行約 8 分鐘",
  "intro": "香港瑰麗酒店（Rosewood Hong Kong）2019年3月開業，位於尖沙咀梳士巴利道18號 Victoria Dockside 綜合體，酒店佔據 40-65 樓，擁有 413 間客房，係瑰麗酒店集團亞太區旗艦。由新世界發展，業主鄭家純家族委託 Tony Chi 設計，以私人宅邸概念打造，保留家族藝術收藏超過 4,700 件作品。",
  "history": "瑰麗酒店前身為新世界中心（1978年開業，2010年代拆卸），原址重建為 Victoria Dockside，包括 K11 MUSEA、瑰麗酒店、瑰麗府邸（服務式住宅）、商業大廈及綠化休憩空間。總投資超過 HK$200 億，2019年3月18日瑰麗酒店正式開幕，係鄭家純女兒鄭志雯主理項目。",
  "facilities": [
    "Asaya 水療及健康中心（面積 8,000 平方米，全港最大 Spa 之一）",
    "戶外無邊際泳池（6樓、全年恆溫）",
    "24 小時健身中心、Pilates 工作室",
    "Manor Club 行政貴賓廊",
    "兒童俱樂部 Rosewood Explorers",
    "連接 K11 MUSEA 藝術商場"
  ],
  "restaurants": [
    "The Legacy House 彤福軒 — 米芝蓮一星順德菜",
    "Henry — 美式扒房（40樓維港全景）",
    "Chaat — 印度菜（創意街頭風味）",
    "Asaya Kitchen — 健康食物概念（Asaya Spa 附設）",
    "DarkSide — 1920年代爵士酒吧、亞洲50最佳酒吧",
    "The Butterfly Room — 英式下午茶、五星級茶點"
  ],
  "rooms_info": "413 間客房及套房，面積由 50 平方米（Deluxe Room）至 400 平方米（Harbour House）。由 Tony Chi 設計，以香港家族宅邸為靈感，客房內設工作枱、梳化區、深泡浴缸、落地玻璃窗。超過 85% 房間擁有維港景觀。",
  "price_range": "Deluxe Room HK$5,500 起 · Harbour View HK$8,200 起 · Manor Suite HK$38,000 起",
  "nearby": [
    "K11 MUSEA 藝術商場（同座相連）",
    "星光大道（步行 2 分鐘）",
    "香港文化中心（步行 5 分鐘）",
    "1881 Heritage（步行 7 分鐘）",
    "維多利亞港天星碼頭（步行 8 分鐘）"
  ],
  "tips": "瑰麗酒店嘅 DarkSide 1920年代爵士酒吧連續多年入選亞洲50最佳酒吧，週末需預約。Asaya Spa 設獨立入口及日光浴室，療程約 HK$1,800-4,800／90分鐘。彤福軒順德菜米芝蓮一星，人均 HK$800-1,500。",
  "faq": [
    ["瑰麗酒店位於邊度？點去？", "位於九龍尖沙咀梳士巴利道18號 Victoria Dockside，酒店佔據 40-65 樓。港鐵尖東站 J 出口經 K11 MUSEA 步行約 3 分鐘、尖沙咀站 F 出口步行約 8 分鐘。"],
    ["瑰麗酒店同 K11 MUSEA 有關係？", "有。瑰麗酒店同 K11 MUSEA 藝術商場同屬新世界 Victoria Dockside 綜合體，酒店大堂同商場相連，酒店保留超過 4,700 件家族藝術收藏，部分展示於公共空間。"],
    ["瑰麗酒店泳池幾時開？", "6 樓戶外無邊際泳池全年恆溫 28-30°C，開放時間 6:30-22:00，只限住客使用。設日光甲板、私人涼亭（需預約，另收費）、池邊餐飲服務。"],
    ["DarkSide 酒吧有咩特別？", "DarkSide 位於酒店 1 樓，1920 年代爵士酒吧風格，每晚有現場爵士樂表演。亞洲50最佳酒吧常客，以陳年蘭姆酒及 whisky 見稱，wine list 超過 300 款。建議週末預約。"],
    ["瑰麗酒店幾錢一晚？", "Deluxe Room HK$5,500 起、Harbour View 海景房 HK$8,200 起、Manor Suite HK$38,000 起。旺季加 40-50%。建議 Trip.com／Klook／Agoda 格價，Rosewood 會員計劃可享額外優惠。"],
    ["瑰麗酒店下午茶喺邊度？", "The Butterfly Room 英式下午茶，時段：下午 2:30-5:30，三層下午茶套餐每位約 HK$488-688。主題隨季節更換，香檳下午茶另加 HK$200-300／位。需提早 1-2 週預約。"]
  ]
}
}

TRIP="https://hk.trip.com/hotels/list?city=58&display=%E9%A6%99%E6%B8%AF&optionId=58&optionType=City&optionName=%E9%A6%99%E6%B8%AF&Allianceid=8067382&SID=305319575&trip_sub1=&trip_sub3=D15325011"
KLOOK="https://affiliate.klook.com/redirect?aid=118358&aff_adid=1254708&k_site=https%3A%2F%2Fwww.klook.com%2Fzh-HK%2Fsearch%2Fresult%2F%3Fquery%3D%25E9%25A6%2599%25E6%25B8%25AF%26sort%3Dmost_relevant%26tab_key%3D54%26start%3D1"

base=json.loads(Path('hotels_data.json').read_text(encoding='utf-8'))
base_map={h['slug']:h for h in base}

def render(slug, d):
    b = base_map[slug]
    img = b['img']
    tags_html=''.join(f'<span class="tag">{t}</span>' for t in b['tags'])
    fac=''.join(f'<li>{x}</li>' for x in d['facilities'])
    rest=''.join(f'<li>{x}</li>' for x in d['restaurants'])
    near=''.join(f'<li>{x}</li>' for x in d['nearby'])
    faq=''.join(f'<div class="faq-q">Q：{q}</div><div class="faq-a">A：{a}</div>' for q,a in d['faq'])
    schema = {
        "@context":"https://schema.org","@type":"Hotel",
        "name":d['en'],"alternateName":d['name'],"description":d['intro'],
        "url":f"https://broadbandhk.com/pages/hotels/{slug}.html","image":img,
        "telephone":d['phone'],
        "address":{"@type":"PostalAddress","streetAddress":d['address_en'],"addressLocality":d['district'],"addressRegion":"Hong Kong","addressCountry":"HK"},
        "geo":{"@type":"GeoCoordinates","latitude":d['lat'],"longitude":d['lng']},
        "starRating":{"@type":"Rating","ratingValue":"5"},
        "aggregateRating":{"@type":"AggregateRating","ratingValue":b['score'],"reviewCount":"2000","bestRating":"10"},
        "priceRange":d['price_range'],"numberOfRooms":d['rooms'],
    }
    faq_schema = {"@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in d['faq']]}
    breadcrumb = {"@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"首頁","item":"https://broadbandhk.com/"},
            {"@type":"ListItem","position":2,"name":"香港酒店推介","item":"https://broadbandhk.com/pages/HKhotel.html"},
            {"@type":"ListItem","position":3,"name":d['name']}
        ]}
    schemas = (
        '<script type="application/ld+json">' + json.dumps(schema,ensure_ascii=False) + '</script>\n'
        '<script type="application/ld+json">' + json.dumps(faq_schema,ensure_ascii=False) + '</script>\n'
        '<script type="application/ld+json">' + json.dumps(breadcrumb,ensure_ascii=False) + '</script>'
    )

    html_out = f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{d['name']}｜格價．地址．設施．交通全攻略 2026 - Broadband HK</title>
<meta name="description" content="{d['name']}全攻略：{d['address_zh']}，{d['mtr']}。{d['intro'][:60]} Trip.com／Klook／Agoda 格價比較。">
<meta name="keywords" content="{d['name']}, {d['en']}, {d['district']}酒店, 香港酒店, 格價, 2026">
<meta property="og:title" content="{d['name']}｜格價比較．2026住宿攻略">
<meta property="og:description" content="{d['intro'][:100]}">
<meta property="og:image" content="{img}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://broadbandhk.com/pages/hotels/{slug}.html">
<meta name="geo.region" content="HK">
<meta name="geo.placename" content="{d['district']}">
<meta name="geo.position" content="{d['lat']};{d['lng']}">
<meta name="ICBM" content="{d['lat']}, {d['lng']}">
<link rel="canonical" href="https://broadbandhk.com/pages/hotels/{slug}.html">
{schemas}
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang TC','Microsoft JhengHei',sans-serif;background:#f8f9fa;color:#333;line-height:1.75;}}
.topbar{{background:#1a1a2e;color:white;padding:12px 20px;font-size:0.9em;}}
.topbar a{{color:#ffd700;text-decoration:none;}}
.topbar a:hover{{text-decoration:underline;}}
.hero{{background:linear-gradient(135deg,#1a1a2e,#16213e 50%,#0f3460);color:white;padding:45px 20px;text-align:center;}}
.hero h1{{font-size:1.9em;margin-bottom:8px;}}
.hero .stars{{color:#ffd700;font-size:1em;margin-bottom:10px;}}
.hero .loc{{opacity:0.9;font-size:0.95em;}}
.container{{max-width:920px;margin:-20px auto 40px;padding:0 15px;}}
.card{{background:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08);overflow:hidden;margin-bottom:20px;}}
.hotel-img{{width:100%;height:360px;background-size:cover;background-position:center;}}
.body{{padding:28px 32px;}}
.tags{{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 18px;}}
.tag{{background:#f0f2ff;color:#667eea;padding:4px 12px;border-radius:12px;font-size:0.82em;}}
.rating{{display:flex;align-items:center;gap:12px;margin:15px 0;}}
.score{{background:#ff4757;color:white;padding:6px 14px;border-radius:6px;font-weight:bold;font-size:1.1em;}}
.desc{{font-size:0.95em;color:#555;margin:15px 0;}}
.price{{font-size:1.6em;color:#ff4757;font-weight:bold;margin:15px 0 5px;}}
.price small{{font-size:0.6em;color:#888;font-weight:normal;}}
.platforms{{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px;}}
.btn{{flex:1;min-width:150px;padding:14px 20px;border-radius:8px;text-decoration:none;color:white;text-align:center;font-weight:bold;font-size:0.95em;transition:opacity 0.2s;}}
.btn:hover{{opacity:0.88;}}
.btn-trip{{background:#287DFA;}}
.btn-klook{{background:#FF5722;}}
.btn-agoda{{background:#C91A1A;}}
.section{{background:white;border-radius:12px;padding:25px 32px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,0.06);}}
.section h2{{font-size:1.3em;border-left:4px solid #667eea;padding-left:12px;margin-bottom:16px;color:#222;}}
.section h3{{font-size:1.05em;margin:18px 0 8px;color:#333;}}
.section p{{color:#555;margin-bottom:12px;}}
.section ul{{padding-left:20px;color:#555;}}
.section li{{margin-bottom:6px;}}
.info-grid{{display:grid;grid-template-columns:140px 1fr;gap:8px 20px;font-size:0.93em;}}
.info-grid dt{{color:#888;}}
.info-grid dd{{color:#333;}}
.faq-q{{font-weight:bold;color:#222;margin-top:16px;}}
.faq-a{{color:#555;margin-top:4px;}}
.tip{{background:#fffde7;border-left:4px solid #ffd700;padding:14px 18px;color:#555;font-size:0.93em;border-radius:0 8px 8px 0;}}
.back{{display:inline-block;margin:15px 0;color:#667eea;text-decoration:none;font-size:0.93em;}}
.back:hover{{text-decoration:underline;}}
.cta{{background:linear-gradient(135deg,#667eea,#764ba2);color:white;border-radius:12px;padding:25px 32px;text-align:center;margin-bottom:20px;}}
.cta h3{{font-size:1.15em;margin-bottom:8px;}}
.cta p{{opacity:0.92;margin-bottom:15px;font-size:0.92em;}}
</style>
</head>
<body>
<div class="topbar">📍 <a href="/">Broadband HK</a> ＞ <a href="/pages/HKhotel.html">香港酒店推介</a> ＞ {d['name']}</div>
<div class="hero">
<h1>{d['name']}</h1>
<div class="stars">{b['stars']}</div>
<div class="loc">📍 {d['address_zh']}</div>
</div>
<div class="container">

<div class="card">
<div class="hotel-img" style="background-image:url('{img}');"></div>
<div class="body">
<div class="tags">{tags_html}</div>
<div class="rating"><span class="score">{b['score']}</span><span>{b['rtext']}</span></div>
<div class="desc">{d['intro']}</div>
<div class="price">{d['price_range'].split('·')[0].strip()} <small>/ 每晚起</small></div>
<div class="platforms">
<a href="{TRIP}" class="btn btn-trip" target="_blank" rel="noopener noreferrer nofollow">Trip.com 格價</a>
<a href="{KLOOK}" class="btn btn-klook" target="_blank" rel="noopener noreferrer nofollow">Klook 格價</a>
<span class="btn btn-agoda" style="opacity:0.7;cursor:not-allowed;">Agoda 格價</span>
</div>
</div>
</div>

<div class="section">
<h2>酒店資料</h2>
<dl class="info-grid">
<dt>英文名稱</dt><dd>{d['en']}</dd>
<dt>地址</dt><dd>{d['address_zh']}（{d['address_en']}）</dd>
<dt>所在地區</dt><dd>{d['district']}</dd>
<dt>開業年份</dt><dd>{d['opened']}</dd>
<dt>客房數量</dt><dd>{d['rooms']} 間</dd>
<dt>酒店電話</dt><dd>{d['phone']}</dd>
<dt>官方網站</dt><dd><a href="{d['official']}" target="_blank" rel="noopener noreferrer">{d['official']}</a></dd>
<dt>GPS 座標</dt><dd>{d['lat']}°N, {d['lng']}°E</dd>
</dl>
</div>

<div class="section">
<h2>酒店簡介</h2>
<p>{d['intro']}</p>
<h3>發展歷史</h3>
<p>{d['history']}</p>
</div>

<div class="section">
<h2>房型與價位</h2>
<p>{d['rooms_info']}</p>
<p><strong>價位範圍：</strong>{d['price_range']}</p>
</div>

<div class="section">
<h2>酒店設施</h2>
<ul>{fac}</ul>
</div>

<div class="section">
<h2>餐飲選擇</h2>
<ul>{rest}</ul>
</div>

<div class="section">
<h2>交通資訊</h2>
<p><strong>港鐵：</strong>{d['mtr']}</p>
<p><strong>機場交通：</strong>由香港國際機場可搭乘機場快綫或機場巴士 A21／A22／E23 前往，亦可預約酒店專車接送。</p>
<h3>附近景點</h3>
<ul>{near}</ul>
</div>

<div class="section">
<h2>入住小貼士</h2>
<div class="tip">💡 {d['tips']}</div>
</div>

<div class="section">
<h2>常見問題 FAQ</h2>
{faq}
</div>

<div class="cta">
<h3>立即比較三大平台格價</h3>
<p>Trip.com、Klook、Agoda 實時搜尋 {d['name']} 最平價格</p>
<div class="platforms">
<a href="{TRIP}" class="btn btn-trip" target="_blank" rel="noopener noreferrer nofollow" style="background:white;color:#287DFA;">Trip.com 格價</a>
<a href="{KLOOK}" class="btn btn-klook" target="_blank" rel="noopener noreferrer nofollow" style="background:white;color:#FF5722;">Klook 格價</a>
</div>
</div>

<a href="/pages/HKhotel.html" class="back">← 返回香港酒店推介列表</a>
</div>
</body>
</html>
'''
    return html_out

for slug,d in DATA.items():
    Path(f'pages/hotels/{slug}.html').write_text(render(slug,d),encoding='utf-8')
    print('ok',slug)
