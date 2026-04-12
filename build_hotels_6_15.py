import json
from pathlib import Path
import importlib.util

# Reuse render function from build_top5_hotels.py
spec = importlib.util.spec_from_file_location("top5", "build_top5_hotels.py")
top5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(top5)

DATA = {
"hyatt-regency-tst": {
  "name": "香港尖沙咀凱悅酒店 Hyatt Regency TST",
  "en": "Hyatt Regency Hong Kong, Tsim Sha Tsui",
  "address_zh": "香港九龍尖沙咀彌敦道18號K11購物藝術館3樓",
  "address_en": "18 Hanoi Road, Tsim Sha Tsui, Kowloon, Hong Kong",
  "lat": 22.2983, "lng": 114.1727,
  "official": "https://www.hyatt.com/hyatt-regency/hkgrt-hyatt-regency-hong-kong-tsim-sha-tsui",
  "phone": "+852 2311 1234",
  "opened": "2009年",
  "rooms": 381,
  "district": "尖沙咀",
  "mtr": "港鐵尖沙咀站 D2 出口步行 1 分鐘，直達酒店",
  "intro": "香港尖沙咀凱悅酒店（Hyatt Regency Hong Kong, Tsim Sha Tsui）位於尖沙咀核心地段彌敦道K11購物藝術館上蓋，2009年開業，擁有 381 間客房。酒店由新世界發展與凱悅集團合作，地理位置極為便利，出港鐵尖沙咀站即達，係商務與購物旅客首選。",
  "history": "凱悅酒店原址位於重建前嘅凱悅中心（1969-2006），2006年結業後新世界於現址重建，2009年重開成為今日嘅凱悅尖沙咀。酒店與 K11 購物藝術館同座，設計融入現代藝術元素。",
  "facilities": [
    "9 樓戶外恆溫泳池及日光甲板",
    "24 小時健身中心",
    "凱悅尊貴貴賓廊",
    "會議及宴會廳（最大可容納 400 人）",
    "商務中心"
  ],
  "restaurants": [
    "Hugo's — 歐陸扒房，獲《米芝蓮指南》推薦",
    "Chin Chin Bar — 美式酒吧",
    "The Chinese Restaurant — 粵菜",
    "Café — 全日自助餐"
  ],
  "rooms_info": "381 間客房及套房，面積由 37 平方米（Hyatt Regency King）至 160 平方米（Presidential Suite）。提供 King／Twin 床型，部分房間可賞維港景或城市景。",
  "price_range": "Hyatt Regency Room HK$1,680 起 · Harbour View HK$2,800 起 · Presidential Suite HK$18,000 起",
  "nearby": [
    "K11 購物藝術館（同座）",
    "海港城（步行 10 分鐘）",
    "星光大道（步行 8 分鐘）",
    "半島酒店 The Lobby（步行 5 分鐘）",
    "尖沙咀天星碼頭（步行 10 分鐘）"
  ],
  "tips": "凱悅尖沙咀地鐵出口直達係最大賣點，適合帶大行李嘅商務或過境旅客。與 K11 購物藝術館相連，想買嘢食嘢非常方便。Hugo's 扒房嘅烤羊架係招牌菜。",
  "faq": [
    ["凱悅尖沙咀點去？", "港鐵尖沙咀站 D2 出口直達酒店大堂，無需過馬路。機場快綫九龍站轉免費接駁巴士 K3 綫到尖沙咀站旁邊，總車程約 30 分鐘。"],
    ["凱悅尖沙咀同 K11 有關係？", "有。酒店位於 K11 購物藝術館上蓋（3-24樓），由新世界發展興建，與 K11 Art Mall 共用建築。住客可直接下樓去商場用餐購物。"],
    ["凱悅尖沙咀幾錢一晚？", "Hyatt Regency Room HK$1,680 起、海景房 HK$2,800 起、Presidential Suite HK$18,000 起。建議 Trip.com／Klook／Agoda 比較至抵。"],
    ["凱悅尖沙咀有泳池嗎？", "有。9 樓戶外恆溫泳池全年開放，水溫 28°C，配有日光甲板及池邊餐飲服務，只限住客免費使用。"],
    ["凱悅尖沙咀 check-in 時間？", "Check-in：下午 3:00；Check-out：中午 12:00。World of Hyatt 會員可享免費 late check-out 至下午 2:00（視乎房況）。"],
    ["凱悅尖沙咀附近有咩食？", "同座 K11 購物藝術館 3-5 樓有 30+ 食肆，酒店步行 5-10 分鐘到半島酒店 The Lobby 下午茶、重慶大廈咖喱、海港城餐廳。"]
  ]
},
"the-murray": {
  "name": "香港美利酒店 The Murray",
  "en": "The Murray, Hong Kong, a Niccolo Hotel",
  "address_zh": "香港中環紅棉路22號",
  "address_en": "22 Cotton Tree Drive, Central, Hong Kong",
  "lat": 22.2799, "lng": 114.1632,
  "official": "https://www.niccolohotels.com/en/hotels/hong_kong/central/the_murray",
  "phone": "+852 3141 8888",
  "opened": "2018年1月",
  "rooms": 336,
  "district": "中環",
  "mtr": "港鐵金鐘站 C1 出口步行約 8 分鐘；中環站 J2 出口步行約 10 分鐘",
  "intro": "香港美利酒店（The Murray, Hong Kong, a Niccolo Hotel）位於中環紅棉路22號，由建於1969年嘅政府美利大廈活化改建，2018年1月開業。酒店由獲獎建築師 Foster + Partners 操刀翻新，保留原大廈標誌性嘅圓拱窗設計，係香港少有嘅活化保育酒店。",
  "history": "美利大廈建於1969年，原為政府辦公大樓，由著名建築師 Ron Phillips 設計，標誌性圓拱窗可降低熱負荷。2013年政府招標活化，馬會信託以 HK$25 億中標，委託 Foster + Partners 翻新。2018年1月以嘉佩樂 Niccolo 品牌開業。",
  "facilities": [
    "25 米戶外恆溫泳池及日光甲板",
    "The Murray Spa 水療中心",
    "24 小時健身中心",
    "會議廳、行政貴賓廊",
    "Mrs Pound 零售店"
  ],
  "restaurants": [
    "Guo Fu Lou 國福樓 — 粵菜 fine dining",
    "Murray Lane — 雞尾酒吧",
    "Popinjays — 25樓屋頂餐廳、360° 海港及山頂景",
    "The Tai Pan — 全日餐廳"
  ],
  "rooms_info": "336 間客房及套房，面積由 48 平方米（Deluxe Room）至 303 平方米（Presidential Suite）。保留原建築圓拱窗，房間採光充足。配備 Nespresso、TOTO 智能廁板、Frette 床品。",
  "price_range": "Deluxe Room HK$2,800 起 · Harbour View HK$4,800 起 · Presidential Suite HK$35,000 起",
  "nearby": [
    "香港公園（步行 2 分鐘）",
    "太古廣場（步行 5 分鐘）",
    "中環半山自動扶梯（步行 8 分鐘）",
    "PMQ 元創方（步行 12 分鐘）",
    "大館文化中心（步行 10 分鐘）"
  ],
  "tips": "Popinjays 屋頂餐廳可賞中環及維港雙景，落日時段特別靚，建議預約窗邊位。酒店地理位置較金鐘中環兩邊地鐵站都要步行 8-10 分鐘，建議搭的士或利用中環半山自動扶梯。",
  "faq": [
    ["美利酒店有咩歷史？", "酒店前身係1969年政府美利大廈，由 Ron Phillips 設計，以圓拱窗降溫聞名。2013年政府活化招標，馬會以 HK$25 億中標，委託 Foster + Partners 翻新，2018年1月以 Niccolo 品牌重開。"],
    ["美利酒店 Niccolo 係咩品牌？", "Niccolo 係馬會集團（Marco Polo）旗下奢華品牌，2015年推出，目前全球 5 間酒店，包括成都、長沙、重慶、西九龍及香港美利。"],
    ["美利酒店點去？", "港鐵金鐘站 C1 出口沿紅棉路行斜路上約 8 分鐘；中環站 J2 出口步行約 10 分鐘。建議搭的士或由太古廣場經有蓋行人通道前往。"],
    ["美利酒店幾錢一晚？", "Deluxe Room HK$2,800 起、Harbour View 海景房 HK$4,800 起、Presidential Suite HK$35,000 起。Niccolo 會員可享額外優惠。"],
    ["Popinjays 屋頂餐廳點預約？", "Popinjays 位於 25 樓頂層，可網上或電話（+852 3141 8888）預約，下午茶 HK$438／位、晚餐人均 HK$1,200-1,800。窗邊 360° 景位非常搶手。"],
    ["美利酒店附近有咩景點？", "步行 2 分鐘到香港公園（內設茶具文物館、溫室、觀鳥園）；5 分鐘到太古廣場；8 分鐘中環半山自動扶梯；12 分鐘 PMQ 元創方。非常適合文化遊客。"]
  ]
},
"w-hong-kong": {
  "name": "香港W酒店 W Hong Kong",
  "en": "W Hong Kong",
  "address_zh": "香港九龍柯士甸道西1號環球貿易廣場",
  "address_en": "1 Austin Road West, Kowloon Station, Hong Kong",
  "lat": 22.3045, "lng": 114.1602,
  "official": "https://www.marriott.com/hotels/travel/hkgwh-w-hong-kong",
  "phone": "+852 3717 2222",
  "opened": "2008年8月",
  "rooms": 393,
  "district": "西九龍",
  "mtr": "港鐵九龍站 C1/D1 出口經商場 MTR 層步行 2 分鐘",
  "intro": "香港W酒店（W Hong Kong）位於九龍西 Elements 圓方商場上蓋，2008年8月開業，係萬豪集團 W Hotels 旗下亞太區旗艦之一，擁有 393 間客房。以頂層 76 樓 WET 戶外無邊際泳池（全港最高戶外泳池）聞名，設計潮流年輕，係年輕 Staycation 族群熱門選擇。",
  "history": "W Hong Kong 由新鴻基地產發展，入住環球貿易廣場（ICC）及 Elements 商場同一建築群。2008年8月開業時為亞洲首間 W Hotel（與首爾同月開業）。2020年進行客房翻新，加入更多 Instagram 打卡元素。",
  "facilities": [
    "WET 76樓戶外無邊際泳池（全港最高戶外泳池）",
    "FIT 24小時健身中心",
    "Bliss Spa 水療中心",
    "WHATEVER/WHENEVER 24小時禮賓",
    "會議廳、行政貴賓廊"
  ],
  "restaurants": [
    "Sing Yin 星逸 — 米芝蓮一星粵菜",
    "Kitchen — 全日自助餐、海景",
    "WOOBAR — 雞尾酒吧、DJ 音樂",
    "Sun Bar — 76樓泳池酒吧"
  ],
  "rooms_info": "393 間客房及套房，面積由 37 平方米（Wonderful Room）至 235 平方米（Extreme Wow Suite）。設計年輕前衛，色彩大膽，部分套房設圓形浴缸。70% 房間擁維港或城市景。",
  "price_range": "Wonderful Room HK$2,200 起 · Spectacular Room HK$3,200 起 · Extreme Wow Suite HK$28,000 起",
  "nearby": [
    "Elements 圓方商場（同座）",
    "機場快綫九龍站（同座）",
    "西九龍文化區 M+／故宮文化博物館（步行 15 分鐘）",
    "天際 100 觀景台（同座 ICC 100樓）",
    "高鐵西九龍站（步行 8 分鐘）"
  ],
  "tips": "W酒店 76 樓 WET 無邊際泳池係全港最高戶外泳池，設日光甲板及酒吧，係 Instagram 打卡熱點。星逸米芝蓮一星粵菜比同級餐廳抵，午市點心套餐約 HK$388-488／位。酒店年輕潮流風格，特別適合年輕情侶及朋友 Staycation。",
  "faq": [
    ["W酒店泳池點樣？", "76 樓 WET 戶外無邊際泳池係全港最高戶外泳池，水溫 28°C，設日光甲板、Sun Bar 池邊酒吧、躺椅。只限住客免費使用，開放時間 6:30-22:00。打卡最佳位為泳池邊望維港。"],
    ["W酒店點去機場？", "機場快綫九龍站與酒店同座 ICC，步行 2 分鐘直達。搭機場快綫到機場約 22 分鐘，HK$105。亦可搭 A21／E21／E23 機場巴士。"],
    ["W酒店適合 Staycation 嗎？", "非常適合。酒店年輕潮流風格，頂層泳池打卡、WOOBAR DJ 音樂、Kitchen 海景自助餐，適合情侶、姊妹、朋友入住。平日 Staycation 套餐約 HK$2,500-3,500／晚包早餐。"],
    ["W酒店幾錢一晚？", "Wonderful Room HK$2,200 起、Spectacular Room HK$3,200 起、Extreme Wow Suite HK$28,000 起。旺季加 40-50%，Marriott Bonvoy 會員可享額外 5-15% 折扣。"],
    ["星逸粵菜幾星？點預約？", "星逸（Sing Yin）為米芝蓮一星粵菜，需提早 1-2 週網上或電話預約。午市點心套餐 HK$388-488／位、晚市人均 HK$800-1,500。"],
    ["W酒店同 Ritz-Carlton 點揀？", "兩間都位於西九龍 ICC 同一建築群，Ritz-Carlton 較奢華商務（102-118 樓）、W 較年輕潮流（76 樓以下）。Ritz 價錢約貴 30-50%，W 更抵 Staycation。"]
  ]
},
"dorsett-mongkok": {
  "name": "香港旺角帝盛酒店 Dorsett Mongkok",
  "en": "Dorsett Mongkok, Hong Kong",
  "address_zh": "香港九龍深水埗欽州街西88號",
  "address_en": "88 Tai Kok Tsui Road, Kowloon, Hong Kong",
  "lat": 22.3175, "lng": 114.1632,
  "official": "https://www.mongkok.dorsetthotels.com",
  "phone": "+852 3987 2288",
  "opened": "2014年",
  "rooms": 285,
  "district": "旺角/大角咀",
  "mtr": "港鐵奧運站 D 出口步行 3 分鐘；港鐵旺角站步行 15 分鐘",
  "intro": "香港旺角帝盛酒店（Dorsett Mongkok, Hong Kong）位於大角咀欽州街，2014年開業，擁有 285 間客房，係帝盛酒店集團（遠東發展旗下）旗下中檔 4 星級酒店。地理位置近奧運站，步行 15 分鐘到旺角購物區，性價比高。",
  "history": "旺角帝盛 2014 年開業，由遠東發展集團興建及營運。帝盛集團在港共有 5 間酒店（銅鑼灣、灣仔、旺角、觀塘、荃灣），主打中價優質住宿。",
  "facilities": [
    "頂層健身中心及景觀泳池",
    "商務中心、會議室",
    "24 小時禮賓部",
    "免費 WiFi、免費手機（Handy 智能手機）"
  ],
  "restaurants": [
    "Grand Café — 全日自助餐、中西融合",
    "The Bar — 大堂酒吧"
  ],
  "rooms_info": "285 間客房，面積由 25 平方米（Superior Room）至 60 平方米（Suite）。房間簡潔現代，全部設免費 WiFi、42 吋液晶電視、Handy 智能手機（可免費上網打電話）。",
  "price_range": "Superior Room HK$780 起 · Deluxe Room HK$980 起 · Suite HK$1,800 起",
  "nearby": [
    "朗豪坊（步行 15 分鐘）",
    "女人街、波鞋街（步行 15 分鐘）",
    "奧海城（步行 5 分鐘）",
    "通菜街金魚街（步行 18 分鐘）",
    "西九龍文化區（的士 10 分鐘）"
  ],
  "tips": "旺角帝盛地點較偏向大角咀，距奧運站較近（3 分鐘），搭 2 個站去旺角購物。最大賣點係每間房都配免費 Handy 智能手機，全程免費打電話上網，特別適合外地遊客。Grand Café 自助晚餐約 HK$388／位，性價比高。",
  "faq": [
    ["旺角帝盛位於邊度？", "地址係九龍大角咀欽州街西88號，接近奧運站而非旺角站。港鐵奧運站 D 出口步行 3 分鐘直達。雖然叫「旺角」帝盛但實際在大角咀。"],
    ["帝盛酒店有幾多間？", "帝盛集團在港共 5 間酒店：帝盛銅鑼灣、帝盛灣仔、帝盛旺角、帝盛觀塘、帝盛荃灣西（中文名 Silka 絲麗）。屬於中檔 4 星級品牌。"],
    ["旺角帝盛有免費手機？", "有。每間客房配一部 Handy 智能手機，住客可免費使用：本地及國際通話、4G 上網、酒店 app 指南。特別適合外地遊客，唔使再買 SIM card。"],
    ["旺角帝盛幾錢一晚？", "Superior Room HK$780 起、Deluxe Room HK$980 起、Suite HK$1,800 起。屬於中檔價位，Trip.com／Klook／Agoda 格價非常抵。"],
    ["旺角帝盛有泳池嗎？", "有。頂層景觀泳池（約 28 米），水溫 28°C，設日光甲板，只限住客使用，開放 6:30-21:30。面積較細但景觀不錯。"],
    ["旺角帝盛適合親子嗎？", "適合。房間可加床（部分房型），酒店有家庭套房（60 平方米），距離奧海城商場步行 5 分鐘（內設大型兒童設施）。預算有限嘅家庭可以考慮。"]
  ]
},
"crowne-plaza-cwb": {
  "name": "香港銅鑼灣皇冠假日酒店 Crowne Plaza CWB",
  "en": "Crowne Plaza Hong Kong Causeway Bay",
  "address_zh": "香港銅鑼灣禮頓道8號",
  "address_en": "8 Leighton Road, Causeway Bay, Hong Kong",
  "lat": 22.2775, "lng": 114.1839,
  "official": "https://www.ihg.com/crowneplaza/hotels/cn/zh/hong-kong/hkgcy",
  "phone": "+852 3980 3980",
  "opened": "2011年7月",
  "rooms": 263,
  "district": "銅鑼灣",
  "mtr": "港鐵銅鑼灣站 F1 出口步行約 5 分鐘；港鐵天后站步行約 8 分鐘",
  "intro": "香港銅鑼灣皇冠假日酒店（Crowne Plaza Hong Kong Causeway Bay）位於銅鑼灣禮頓道，2011年開業，擁有 263 間客房，係 IHG 洲際集團 Crowne Plaza 品牌喺港首間酒店。地理位置極佳，步行 5 分鐘到時代廣場、崇光百貨，係購物及商務客熱門選擇。",
  "history": "銅鑼灣皇冠假日由華地建築發展，2011年7月開業。酒店位於銅鑼灣商業核心邊緣，設計以現代都會風格為主，設有頂層景觀酒吧 Club @28。",
  "facilities": [
    "Club @28 頂層泳池及酒吧（28 樓）",
    "健身中心 24 小時開放",
    "商務中心、會議廳",
    "行政貴賓廊（Club Lounge）"
  ],
  "restaurants": [
    "Kudos — 全日自助餐、開放式廚房",
    "Tai Pan — 粵菜餐廳",
    "Club @28 — 頂層酒吧、維港景"
  ],
  "rooms_info": "263 間客房及套房，面積由 28 平方米（Standard Room）至 110 平方米（Presidential Suite）。房間配備 Smart TV、Nespresso、iHome Dock，部分房可賞跑馬地馬場或城市景。",
  "price_range": "Standard Room HK$1,582 起 · Club Room HK$2,400 起 · Suite HK$6,800 起",
  "nearby": [
    "時代廣場（步行 8 分鐘）",
    "崇光百貨（步行 10 分鐘）",
    "跑馬地馬場（步行 10 分鐘）",
    "利園區（步行 3 分鐘）",
    "維多利亞公園（步行 12 分鐘）"
  ],
  "tips": "Club @28 頂層泳池酒吧係打卡熱點，可賞跑馬地馬場同城市景，落日時段特別靚。酒店位置稍偏離銅鑼灣核心（近禮頓山），步行 5-10 分鐘到時代廣場。IHG One Rewards 會員可享 early check-in 及 late check-out。",
  "faq": [
    ["銅鑼灣皇冠假日點去？", "港鐵銅鑼灣站 F1 出口沿禮頓道步行約 5 分鐘；天后站步行 8 分鐘。位於禮頓道同波斯富街交界，近跑馬地馬場。"],
    ["Club @28 頂層泳池幾時開？", "Club @28 位於 28 樓，戶外泳池及酒吧開放時間 6:30-22:00（酒吧至 00:00）。住客免費使用，非住客需預訂 Day Pass。"],
    ["銅鑼灣皇冠假日幾錢？", "Standard Room HK$1,582 起、Club Room（含貴賓廊）HK$2,400 起、Suite HK$6,800 起。旺季加 30-50%，IHG 會員額外 10-15% 折扣。"],
    ["銅鑼灣皇冠假日 check-in 時間？", "Check-in：下午 3:00；Check-out：中午 12:00。IHG One Rewards Platinum／Diamond 會員可享免費 late check-out 至下午 4:00（視乎房況）。"],
    ["附近有咩食有咩買？", "步行 3 分鐘到利園區（The Lee Gardens）有高級餐廳及品牌店；8 分鐘到時代廣場食肆；10 分鐘崇光百貨地庫超市。亦可步行 15 分鐘去大坑食米芝蓮街頭小食。"],
    ["銅鑼灣皇冠假日適合商務嗎？", "適合。設 24 小時商務中心、14 間會議室（最大可容納 200 人）、行政貴賓廊、高速 WiFi。距離香港會議展覽中心搭的士約 10 分鐘、HK$50-70。"]
  ]
},
"bridal-tea-house-hotel": {
  "name": "百家好世酒店 Bridal Tea House Hotel",
  "en": "Bridal Tea House Hotel",
  "address_zh": "香港多個地點（太子、紅磡、北角、銅鑼灣、灣仔、九龍城、佐敦等）",
  "address_en": "Multiple locations in Hong Kong",
  "lat": 22.3193, "lng": 114.1694,
  "official": "https://www.bthhotel.com",
  "phone": "+852 3127 8888",
  "opened": "2003年（首間）",
  "rooms": 1500,
  "district": "多區",
  "mtr": "各分店近港鐵站，一般步行 3-8 分鐘",
  "intro": "百家好世酒店（Bridal Tea House Hotel）係香港本地連鎖 3 星級酒店品牌，2003年開業，目前全港有 13 間分店，合共超過 1,500 間客房，遍及太子、紅磡、北角、銅鑼灣、灣仔、九龍城、佐敦、荃灣等區。主打中低價位，適合預算有限嘅旅客及商務客。",
  "history": "百家好世由本地企業家譚炳文於2003年創立，原址為太子分店。品牌名源自粵語「百家」「好世界」，寓意平實人家嘅好旅居。集團旗下亦有奧斯卡酒店（Oscar Hotel）等副品牌。",
  "facilities": [
    "24 小時前台",
    "免費 WiFi",
    "商務中心（部分分店）",
    "自助洗衣設備（部分分店）",
    "禁煙樓層"
  ],
  "restaurants": [
    "各分店設小型早餐區",
    "部分分店鄰近 24 小時茶餐廳及便利店"
  ],
  "rooms_info": "約 1,500 間客房，面積由 10 平方米（Economy Room）至 25 平方米（Family Room）。房間精簡但齊備，設空調、免費 WiFi、LCD 電視、小型浴室。部分房型為「無窗房」，價錢較低。",
  "price_range": "Economy Room HK$380 起 · Standard Room HK$480 起 · Family Room HK$780 起",
  "nearby": [
    "各分店都近港鐵站及鬧市",
    "太子店：步行 5 分鐘到旺角女人街",
    "紅磡店：近紅磡火車站",
    "銅鑼灣店：步行 3 分鐘到時代廣場",
    "佐敦店：近廟街夜市"
  ],
  "tips": "百家好世屬於經濟型連鎖，房間普遍較細（約 10-15 平方米），有啲房型無窗。預訂前請留意：1) 有無窗（顯示「內望」即係無窗）；2) 床型（雙人床或兩張單人床）；3) 具體分店地址。預算有限或短暫過境嘅旅客非常適合。",
  "faq": [
    ["百家好世有幾多間分店？", "全港 13 間分店：太子、紅磡、北角、銅鑼灣、灣仔、九龍城、佐敦、荃灣、旺角、筲箕灣、西環、葵涌、香港仔等。總客房超過 1,500 間。"],
    ["百家好世點樣揀分店？", "按行程揀：購物去太子／旺角店（近女人街）；觀光去佐敦／尖沙咀店；近機場揀荃灣店；近迪士尼揀荃灣／葵涌店。每間分店都近港鐵站，步行 3-8 分鐘。"],
    ["百家好世幾錢一晚？", "Economy Room HK$380 起（無窗）、Standard Room HK$480 起、Family Room HK$780 起。旺季（聖誕、農曆年）加 40-80%，平日最抵。"],
    ["百家好世房間有幾大？", "房間面積由 10 平方米（Economy）至 25 平方米（Family Room）。絕大部分房型較細，預訂時請留意面積及是否有窗。如要大房可揀「豪華房」或「家庭房」。"],
    ["百家好世有冇早餐？", "部分分店提供簡易自助早餐（另加 HK$80-120／位），部分分店需自費外出用餐。預訂時請留意 package 是否含早餐。附近多有茶餐廳同便利店。"],
    ["百家好世可以住幾多人？", "Economy／Standard Room 一般 2 人入住；Family Room 可住 3-4 人。如要加床需提前通知並另加費用（約 HK$150-250／張）。"]
  ]
},
"auberge-discovery-bay": {
  "name": "愉景灣酒店 Auberge Discovery Bay",
  "en": "Auberge Discovery Bay Hong Kong",
  "address_zh": "香港大嶼山愉景灣海澄湖畔路88號",
  "address_en": "88 Siena Avenue, Discovery Bay, Lantau Island, Hong Kong",
  "lat": 22.2947, "lng": 114.0147,
  "official": "https://www.aubergediscoverybay.com",
  "phone": "+852 2295 8288",
  "opened": "2009年",
  "rooms": 325,
  "district": "大嶼山/愉景灣",
  "mtr": "由中環 3 號碼頭搭愉景灣渡輪約 25 分鐘，再搭免費接駁巴士 5 分鐘",
  "intro": "愉景灣酒店（Auberge Discovery Bay Hong Kong）位於大嶼山愉景灣，2009年開業，擁有 325 間客房，係愉景灣渡假社區內嘅 5 星級度假酒店。背山面海、坐擁沙灘及棕櫚林景觀，適合 Staycation 及遠離煩囂嘅週末度假。酒店由 HKR International（愉景灣發展商）興建及營運。",
  "history": "愉景灣係由香港興業於1970年代發展嘅獨立社區，愉景灣酒店2009年開業，原為社區會所升級改造。酒店同毗鄰嘅 Auberge Residence（服務式住宅）同屬 Auberge 品牌。",
  "facilities": [
    "私人沙灘（愉景灣大白灣沙灘）",
    "戶外恆溫泳池（兩個，成人池及兒童池）",
    "Spa 及健身中心",
    "網球場、自行車租賃",
    "免費渡輪穿梭服務往中環"
  ],
  "restaurants": [
    "Fire — 法式扒房、海景",
    "Café bord de Mer — 全日自助餐、沙灘景",
    "Lighthouse Terrace — 池畔酒吧",
    "M 21 — 義大利菜"
  ],
  "rooms_info": "325 間客房及套房，面積由 36 平方米（Deluxe Room）至 130 平方米（Suite）。全部房間設露台，可賞海景、沙灘景或花園景。配備 Smart TV、Nespresso、深泡浴缸。",
  "price_range": "Deluxe Room HK$1,980 起 · Ocean View HK$2,880 起 · Suite HK$8,800 起",
  "nearby": [
    "愉景灣大白灣沙灘（酒店即出）",
    "愉景灣廣場（步行 5 分鐘）",
    "迪士尼樂園（的士 15 分鐘）",
    "梅窩（搭村巴 30 分鐘）",
    "機場（的士 30 分鐘、HK$280-350）"
  ],
  "tips": "由中環 3 號碼頭搭愉景灣渡輪係最主要交通方式，每 15-30 分鐘一班，船程 25 分鐘，船費 HK$46（24 小時運作）。愉景灣內無公共交通，一律靠免費接駁巴士。酒店適合帶小朋友、想遠離市區煩囂、週末放鬆嘅旅客。",
  "faq": [
    ["愉景灣酒店點去？", "由中環 3 號碼頭搭愉景灣渡輪 25 分鐘到愉景灣碼頭，然後搭酒店免費接駁巴士 5 分鐘到酒店。渡輪每 15-30 分鐘一班、HK$46／程，24 小時運作。"],
    ["愉景灣酒店有沙灘嗎？", "有。酒店緊貼愉景灣大白灣沙灘（Tai Pak Beach），住客免費使用。設更衣室、淋浴、遮陽傘及躺椅租借。沙灘水質清澈，適合親子玩水。"],
    ["愉景灣酒店點去迪士尼？", "由酒店搭的士約 15 分鐘到迪士尼樂園（HK$180-220），或搭愉景灣免費接駁巴士到欣澳站再搭迪士尼綫地鐵（約 30 分鐘）。"],
    ["愉景灣酒店適合親子嗎？", "非常適合。設兒童泳池、私人沙灘、兒童俱樂部、兒童餐單、BB 床、家庭套房。距迪士尼僅 15 分鐘車程，可安排一日迪士尼遊再返酒店休息。"],
    ["愉景灣酒店幾錢一晚？", "Deluxe Room HK$1,980 起、Ocean View 海景房 HK$2,880 起、Suite HK$8,800 起。Staycation 套餐（含早餐及晚餐自助餐）約 HK$2,800-3,800／晚。"],
    ["愉景灣酒店可以帶寵物嗎？", "部分房型歡迎寵物（需預訂寵物友善房 Pet Friendly Room），需額外付清潔費 HK$300-500／晚。愉景灣社區係全港少有嘅寵物友善社區，有專屬狗公園。"]
  ]
},
"grand-hyatt-hong-kong": {
  "name": "香港君悅酒店 Grand Hyatt Hong Kong",
  "en": "Grand Hyatt Hong Kong",
  "address_zh": "香港灣仔港灣道1號",
  "address_en": "1 Harbour Road, Wan Chai, Hong Kong",
  "lat": 22.2817, "lng": 114.1731,
  "official": "https://www.hyatt.com/grand-hyatt/hkggh-grand-hyatt-hong-kong",
  "phone": "+852 2588 1234",
  "opened": "1989年",
  "rooms": 542,
  "district": "灣仔",
  "mtr": "港鐵灣仔站 A1 出口經有蓋行人天橋步行約 8 分鐘；金鐘站 A1 出口步行 12 分鐘",
  "intro": "香港君悅酒店（Grand Hyatt Hong Kong）位於灣仔會議展覽中心旁，1989年開業，擁有 542 間客房，係凱悅集團 Grand Hyatt 品牌在港旗艦酒店。酒店為新世界中心重建前嘅姊妹物業，由新鴻基地產發展，設有全港最大酒店戶外泳池（50 米），係政府高官、明星及商務旅客首選。",
  "history": "君悅酒店1989年開業，由新鴻基地產及合和實業合作興建，與隔鄰會議展覽中心同步發展。1997年香港回歸慶典、2005年世貿部長級會議等重要活動均以君悅為主要接待酒店。",
  "facilities": [
    "50 米戶外恆溫泳池（全港最大酒店泳池）",
    "戶外網球場、花園綠化 11,000 平方米",
    "Plateau Spa 水療中心",
    "24 小時健身中心",
    "Grand Club 行政貴賓廊",
    "大型會議及宴會廳（最大容納 1,200 人）"
  ],
  "restaurants": [
    "One Harbour Road 港灣壹號 — 粵菜，獲米芝蓮推薦",
    "Grissini — 意大利菜",
    "Kaetsu 華粵 — 日本料理",
    "Grand Cafe — 全日自助餐",
    "Champagne Bar — 香檳酒吧、現場爵士樂",
    "Tiffin — 下午茶自助餐"
  ],
  "rooms_info": "542 間客房及套房，面積由 42 平方米（Grand Deluxe Room）至 281 平方米（Presidential Suite）。2017-2019年進行大型翻新，保留經典東方元素，全部房間均可賞維港或城市景。",
  "price_range": "Grand Deluxe Room HK$2,400 起 · Harbour View HK$3,800 起 · Presidential Suite HK$58,000 起",
  "nearby": [
    "香港會議展覽中心（步行 3 分鐘）",
    "金紫荊廣場（步行 5 分鐘）",
    "灣仔渡輪碼頭（步行 3 分鐘，往尖沙咀）",
    "太古廣場（步行 15 分鐘）",
    "利東街（步行 12 分鐘）"
  ],
  "tips": "君悅 50 米戶外泳池配 11,000 平方米花園係全港酒店之冠，設日光甲板、泳池餐廳、兒童池。Tiffin 下午茶自助餐人均 HK$398-488，香港三大經典酒店下午茶之一。港灣壹號粵菜米芝蓮推薦，適合招呼客人。",
  "faq": [
    ["君悅酒店泳池有幾大？", "50 米戶外恆溫泳池係全港最大酒店泳池，配 11,000 平方米花園綠化、兒童池、網球場、日光甲板、泳池餐廳。只限住客免費使用，開放 6:30-22:00。"],
    ["君悅酒店點去會展？", "酒店同香港會議展覽中心有行人天橋直接連通，步行 3 分鐘。會展期間酒店客滿率極高，建議提早 2-3 個月預訂。"],
    ["君悅酒店 Tiffin 下午茶點訂？", "Tiffin 位於酒店大堂，下午茶自助餐時段：週一至五 3:15-5:30、週末 3:00-5:30。人均 HK$398-488，香檳升級加 HK$188／位。需網上或電話（+852 2584 7722）預約。"],
    ["君悅酒店幾錢一晚？", "Grand Deluxe Room HK$2,400 起、Harbour View 海景房 HK$3,800 起、Presidential Suite HK$58,000 起。旺季（會展期、聖誕、農曆年）加 50-100%。"],
    ["君悅酒店同君綽／君逸差別？", "Grand Hyatt（君悅）係凱悅最高端品牌；Hyatt Regency（凱悅／君綽）係主流商務品牌；Andaz／Park Hyatt 係精品品牌。君悅灣仔為旗艦，價位最高。"],
    ["君悅酒店適合商務會議嗎？", "非常適合。28 間會議廳，最大 Grand Ballroom 可容納 1,200 人，亦係亞洲最大酒店宴會廳之一。商務中心 24 小時開放，近會展及金融區。"]
  ]
},
"marriott-ocean-park": {
  "name": "香港海洋公園萬豪酒店 Marriott Ocean Park",
  "en": "Hong Kong Ocean Park Marriott Hotel",
  "address_zh": "香港南區黃竹坑南朗山路180號",
  "address_en": "180 Wong Chuk Hang Road, Aberdeen, Hong Kong",
  "lat": 22.2482, "lng": 114.1720,
  "official": "https://www.marriott.com/hotels/travel/hkgms-hong-kong-ocean-park-marriott-hotel",
  "phone": "+852 3555 1888",
  "opened": "2018年11月",
  "rooms": 471,
  "district": "南區/黃竹坑",
  "mtr": "港鐵海洋公園站 B 出口步行 5 分鐘；酒店提供免費接駁巴士",
  "intro": "香港海洋公園萬豪酒店（Hong Kong Ocean Park Marriott Hotel）位於南區黃竹坑南朗山腳，2018年11月開業，擁有 471 間客房，係海洋公園度假區嘅官方合作酒店，主題以海洋保育為靈感，係香港首間海洋主題酒店。",
  "history": "海洋公園萬豪由海洋公園公司興建、萬豪集團營運，係海洋公園度假區三間官方酒店之一（其他為富麗敦海洋公園酒店 Fullerton）。2018年11月開業，配合海洋公園業務多元化發展。",
  "facilities": [
    "海洋主題大堂（大型水族館展示 5,000 條魚）",
    "戶外恆溫泳池（兒童水上樂園區）",
    "24 小時健身中心",
    "會議廳、宴會廳",
    "免費穿梭巴士往中環／金鐘／海洋公園入口"
  ],
  "restaurants": [
    "Pacific — 全日自助餐（海洋主題）",
    "Feast — 午市自助、海鮮為主",
    "The Lounge — 大堂酒廊、下午茶"
  ],
  "rooms_info": "471 間客房，面積由 35 平方米（Deluxe Room）至 110 平方米（Suite）。部分房型設海洋主題裝飾（海洋套房內設大型水族館）。客房配備 Smart TV、Nespresso、BVLGARI 沐浴用品。",
  "price_range": "Deluxe Room HK$2,200 起 · Ocean View HK$2,800 起 · Ocean Suite HK$6,800 起（內設水族館）",
  "nearby": [
    "海洋公園（步行 5 分鐘）",
    "港鐵海洋公園站（步行 5 分鐘）",
    "黃竹坑藝術區（步行 10 分鐘）",
    "南區大街小巷（的士 10 分鐘到香港仔）",
    "赤柱廣場（巴士 30 分鐘）"
  ],
  "tips": "海洋套房（Ocean Suite）內設大型水族館，打卡熱點，但價錢較高（HK$6,800 起）。酒店與海洋公園有套票優惠，包住宿 + 門票通常較單買抵 15-25%。免費接駁巴士往返中環／金鐘，方便觀光。",
  "faq": [
    ["海洋公園萬豪點去海洋公園？", "酒店步行 5 分鐘到海洋公園正門；亦有免費穿梭巴士。港鐵海洋公園站 B 出口即到酒店。"],
    ["海洋套房有咩特別？", "Ocean Suite 內設大型觀賞水族館，連通客房及浴室，飼有多種熱帶魚，係酒店獨有賣點。價錢 HK$6,800 起，面積 110 平方米。打卡熱度極高。"],
    ["海洋公園萬豪有優惠套票？", "有。酒店與海洋公園推出「住宿 + 門票」套票，含 1 晚住宿 + 2 天樂園門票 + 自助早餐，約 HK$3,800-5,500／房（雙人）。比單買抵 15-25%。"],
    ["海洋公園萬豪幾錢一晚？", "Deluxe Room HK$2,200 起、Ocean View 海景房 HK$2,800 起、Ocean Suite 水族館套房 HK$6,800 起。親子家庭建議揀含門票套票更抵。"],
    ["海洋公園萬豪適合親子嗎？", "非常適合。酒店本身係海洋主題（大堂水族館、海洋套房），毗鄰海洋公園，設兒童泳池、Kids Club、家庭套房、BB 床、兒童 menu。"],
    ["海洋公園萬豪點去中環？", "免費穿梭巴士往返中環／金鐘，車程 20-25 分鐘。亦可搭港鐵南港島綫海洋公園站到金鐘，車程 5 分鐘；再轉荃灣綫去中環或尖沙咀。"]
  ]
},
"hotel-icon": {
  "name": "唯港薈 Hotel ICON",
  "en": "Hotel ICON",
  "address_zh": "香港九龍尖沙咀東部科學館道17號",
  "address_en": "17 Science Museum Road, Tsim Sha Tsui East, Kowloon, Hong Kong",
  "lat": 22.3018, "lng": 114.1788,
  "official": "https://www.hotel-icon.com",
  "phone": "+852 3400 1000",
  "opened": "2011年9月",
  "rooms": 262,
  "district": "尖沙咀東",
  "mtr": "港鐵尖東站 P2 出口步行約 5 分鐘；紅磡站步行 8 分鐘",
  "intro": "唯港薈（Hotel ICON）位於尖沙咀東部科學館道，2011年9月開業，擁有 262 間客房，係香港理工大學教學酒店，由學生實習營運，屬於 4 星級設計型酒店。由 Rocco Design Architects 羅時暐設計，大堂設香港最大室內垂直花園（由 Patrick Blanc 創作），係設計酒店迷必訪之作。",
  "history": "唯港薈由香港理工大學興建，作為酒店及旅遊業學院嘅教學基地，讓學生在真實酒店環境實習。2011年9月開業，由 Rocco Design Architects 操刀，花園由法國植物藝術家 Patrick Blanc 創作，擁有超過 8,000 株植物。",
  "facilities": [
    "戶外無邊際泳池（28 米、可賞維港景）",
    "The Pool Bar 池畔酒吧",
    "Angsana Spa（泰式水療品牌）",
    "24 小時健身中心",
    "大堂垂直花園（Patrick Blanc 作品）"
  ],
  "restaurants": [
    "Above & Beyond 天外天 — 米芝蓮一星粵菜、頂樓維港景",
    "The Market — 全日自助餐、開放式廚房",
    "GREEN — 純素食概念",
    "The Lounge — 下午茶"
  ],
  "rooms_info": "262 間客房及套房，面積由 35 平方米（Superior Room）至 200 平方米（Presidential Suite）。由國際設計師 Conran & Partners 設計，房間採北歐簡約風格，配備 Smart TV、Nespresso、免費 mini bar（部分房型）。",
  "price_range": "Superior Room HK$1,480 起 · Harbour View HK$2,380 起 · Suite HK$5,800 起",
  "nearby": [
    "香港科學館（步行 3 分鐘）",
    "香港歷史博物館（步行 3 分鐘）",
    "紅磡體育館（步行 8 分鐘）",
    "K11 MUSEA（步行 10 分鐘）",
    "尖沙咀天星碼頭（步行 15 分鐘）"
  ],
  "tips": "唯港薈由理工大學學生實習營運，服務態度特別真誠貼心。Above & Beyond 天外天位於頂樓，米芝蓮一星粵菜配 270° 維港景，晚市人均 HK$800-1,500。大堂 Patrick Blanc 垂直花園係打卡必到。部分房型含免費 mini bar，性價比高。",
  "faq": [
    ["唯港薈係咩酒店？", "唯港薈（Hotel ICON）係香港理工大學旗下教學酒店，由學生實習營運，4 星級設計型酒店。2011年開業，由 Rocco 設計，大堂有 Patrick Blanc 垂直花園。"],
    ["唯港薈有咩特別設計？", "大堂設香港最大室內垂直花園（超過 8,000 株植物，Patrick Blanc 創作）；頂層天外天餐廳由 Terry Farrell 設計、270° 維港景；客房由 Conran & Partners 設計。整體係設計酒店迷必訪。"],
    ["唯港薈地址同交通？", "地址：九龍尖沙咀東部科學館道17號。港鐵尖東站 P2 出口沿科學館道步行 5 分鐘；紅磡站經行人天橋步行 8 分鐘。酒店設免費穿梭巴士往返尖沙咀天星碼頭。"],
    ["天外天粵菜幾星？", "Above & Beyond 天外天位於酒店 28 樓，米芝蓮一星粵菜餐廳，擁有 270° 維港景。午市點心套餐 HK$388-488／位、晚市人均 HK$800-1,500。需提早 1-2 週預約。"],
    ["唯港薈幾錢一晚？", "Superior Room HK$1,480 起、Harbour View 海景房 HK$2,380 起、Suite HK$5,800 起。部分房型含免費 mini bar 及自助早餐，性價比係尖沙咀 4 星之冠。"],
    ["唯港薈泳池點樣？", "28 米戶外無邊際泳池位於酒店 9 樓，水溫 28°C，可賞維港景。設 The Pool Bar 池畔酒吧、日光甲板。只限住客免費使用，開放 6:30-22:00。"]
  ]
}
}

for slug,d in DATA.items():
    Path(f'pages/hotels/{slug}.html').write_text(top5.render(slug,d),encoding='utf-8')
    print('ok',slug)
