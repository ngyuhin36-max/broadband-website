"""Optimize pages/trains.html SEO/GEO (zh only — no en version exists)."""
import re, json
from pathlib import Path

# XRL destinations from West Kowloon Station with coords + distance info
DESTS = [
    ("Shenzhen North","深圳北",22.6101,114.0293,"14 min","HK$75 起","14 分鐘"),
    ("Futian","福田",22.5360,114.0553,"23 min","HK$90 起","23 分鐘"),
    ("Guangzhou South","廣州南",23.0014,113.2681,"47 min","HK$215 起","47 分鐘"),
    ("Guangzhou East","廣州東",23.1531,113.3220,"75 min","HK$220 起","75 分鐘"),
    ("Zhuhai","珠海",22.2686,113.5769,"105 min","HK$240 起","105 分鐘"),
    ("Changsha South","長沙南",28.1507,113.0656,"200 min","HK$580 起","3 小時 20 分鐘"),
    ("Wuhan","武漢",30.5936,114.3053,"4h 10m","HK$720 起","4 小時 10 分鐘"),
    ("Xiamen North","廈門北",24.5945,118.0290,"5h 10m","HK$720 起","5 小時 10 分鐘"),
    ("Hangzhou East","杭州東",30.2946,120.2121,"7h","HK$975 起","7 小時"),
    ("Shanghai Hongqiao","上海虹橋",31.1940,121.3246,"8h","HK$1,071 起","8 小時"),
    ("Beijing West","北京西",39.8946,116.3227,"9h","HK$1,239 起","9 小時"),
]

def jdump(d): return json.dumps(d, ensure_ascii=False)

url = "https://broadbandhk.com/pages/trains.html"

travel = {
    "@context":"https://schema.org","@type":"TravelAgency",
    "name":"香港高鐵訂票格價比較",
    "description":"2026 香港西九龍高鐵站出發中國高鐵即時訂票格價比較",
    "url":url,
    "image":"https://broadbandhk.com/og-image.png",
    "priceRange":"HK$75 - HK$1,500+",
    "address":{"@type":"PostalAddress","addressLocality":"西九龍","addressRegion":"香港","addressCountry":"HK"},
    "geo":{"@type":"GeoCoordinates","latitude":22.3044,"longitude":114.1666},
    "hasMap":"https://www.google.com/maps/place/West+Kowloon+Station",
    "areaServed":[
        {"@type":"TrainStation","name":zh,"alternateName":en,
         "geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lng}}
        for en,zh,lat,lng,_,_,_ in DESTS
    ],
    "knowsAbout":["香港高鐵","廣深港高鐵","西九龍站","中國高鐵","高鐵訂票","Trip.com 高鐵"]
}

breadcrumb = {
    "@context":"https://schema.org","@type":"BreadcrumbList",
    "itemListElement":[
        {"@type":"ListItem","position":1,"name":"首頁","item":"https://broadbandhk.com/"},
        {"@type":"ListItem","position":2,"name":"高鐵訂票","item":url}
    ]}

# FAQ - long-tail train questions
faqs = [
    ("西九龍高鐵搭車點帶證件？","內地客用回鄉證；香港人用回鄉證或護照；外國人用護照。西九龍站設一地兩檢，喺西九龍站內完成香港出境 + 內地入境。護照／證件要帶去閘機掃描。"),
    ("高鐵二等座／一等座／商務座點揀？","二等座 2+3 排列，HK$75-1,239（最抵、90% 旅客選）。一等座 2+2 寬座，+30-50% 價錢。商務座類似飛機頭等艙，+100-200% 但可躺、有獨立屏幕。短程（深圳／廣州）二等座夠用，長程（上海／北京）可考慮升等。"),
    ("高鐵訂票邊度買最方便？","Trip.com 最方便（繁中介面、HK$ 扣款、免紙本）。12306 官方 App 需要內地手機號；香港地鐵售票機需要現場排隊；第三方代訂收手續費。建議 Trip.com 網上訂後直接用車票二維碼入閘。"),
    ("高鐵要提早幾耐訂？","內地高鐵一般提早 15 日公開售票。熱門時段（春運／國慶／五一／暑假）建議開票即訂（0時 00 開賣）。廣深線一般即日預訂有位。",),
    ("西九龍去深圳北最快幾耐？","14 分鐘，HK$75 起。比搭港鐵（東鐵線到羅湖過關再轉深圳地鐵）快 30-40 分鐘，但貴少少。建議選繁忙時間坐高鐵省時。"),
    ("高鐵可以退票／改簽嗎？","開車前 48 小時以上：免費退票 / 改簽；48 小時內：5-20% 手續費；開車後：不可退票但可改簽同日其他班次（需同站）。Trip.com 代處理退改，約 30 分鐘內完成。"),
    ("高鐵行李限制？","免費手提 20kg 成人 / 10kg 兒童，尺寸不限（但要塞得入行李架）。超重或大型物品需另付寄存費。寵物、危險品、鋒利物品禁帶。液體 100ml 以下 OK。"),
    ("香港去澳門可以搭高鐵嗎？","冇直達高鐵。流程：西九龍 → 珠海站 (105 分鐘、HK$240) → 拱北口岸步行過關 → 澳門關閘。全程約 2.5-3 小時。或者考慮港珠澳大橋巴士（直達 40 分鐘、HK$65），通常更快。"),
    ("高鐵 vs 飛機點揀？","廣州／深圳（< 3 小時）：高鐵贏（無安檢等候）。上海／北京（8-9 小時）：飛機贏（2-3 小時飛行）。長沙／武漢／廈門（4-6 小時）：視乎價錢，高鐵可慳 HK$500-1,000 但時間多一倍。"),
    ("高鐵即日來回深圳可行嗎？","完全可行。14 分鐘到深圳北 / 23 分鐘到福田。朝早 8:00 出發，深圳玩到晚上 10 點返香港。香港買一程，深圳買返程（或直接買來回票）。親子一日遊首選。"),
]
faq = {
    "@context":"https://schema.org","@type":"FAQPage",
    "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]
}

dest = {
    "@context":"https://schema.org","@type":"TouristDestination",
    "name":"香港西九龍高鐵站",
    "alternateName":"West Kowloon Station (XRL)",
    "url":url,
    "geo":{"@type":"GeoCoordinates","latitude":22.3044,"longitude":114.1666},
    "includesAttraction":[
        {"@type":"TrainStation","name":zh,
         "geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lng}}
        for en,zh,lat,lng,_,_,_ in DESTS
    ],
    "touristType":["商務","親子","情侶","背包客"]
}

# Apply
p = Path("pages/trains.html")
s = p.read_text(encoding="utf-8")

# Trim keywords
new_kw = "香港高鐵訂票,西九龍高鐵,高鐵格價2026,香港去深圳高鐵,香港去廣州高鐵,香港去上海高鐵,香港去北京高鐵,香港去珠海高鐵,香港去長沙高鐵,深圳北高鐵,福田高鐵,廣州南高鐵,高鐵二等座,高鐵一等座,高鐵商務座,高鐵退票改簽,高鐵行李限制,西九龍站,高鐵vs飛機,高鐵即日來回深圳,珠海去澳門,Trip.com高鐵訂票,Hong Kong XRL,Hong Kong to Shenzhen train,Hong Kong to Guangzhou train"
s = re.sub(r'<meta name="keywords" content="[^"]+">',
           f'<meta name="keywords" content="{new_kw}">', s, count=1)

# Add GEO meta
extra = (
    '    <meta name="geo.country" content="HK">\n'
    '    <meta name="DC.coverage.spatial" content="West Kowloon Station, Hong Kong">\n'
    '    <meta name="timezone" content="Asia/Hong_Kong">\n'
    '    <meta name="distribution" content="global">\n'
)
if 'geo.country' not in s:
    s = re.sub(r'(<meta name="ICBM"[^>]+>\n)',
               lambda m: m.group(1) + extra, s, count=1)

# Add schemas
new_blocks = (
    f'    <script type="application/ld+json">{jdump(travel)}</script>\n'
    f'    <script type="application/ld+json">{jdump(breadcrumb)}</script>\n'
    f'    <script type="application/ld+json">{jdump(faq)}</script>\n'
    f'    <script type="application/ld+json">{jdump(dest)}</script>\n'
)
s = re.sub(r'(\s*<style>)', r'\n' + new_blocks + r'\1', s, count=1)

p.write_text(s, encoding="utf-8")
print("trains.html optimized")
ctx = '"@context"'
print(f"  schemas: {s.count(ctx)}, hreflang: {s.count('hreflang=')}")
