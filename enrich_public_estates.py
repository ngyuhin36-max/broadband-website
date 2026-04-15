# -*- coding: utf-8 -*-
"""Enrich BroadbandHK public estate pages with verified data."""
import re
from pathlib import Path

PAGES = Path(r"C:/Users/tonyng/Desktop/Claude_Code/BROADBANDHK/pages")

# Each estate: file, zh, en, district_sub, mtr, year, blocks, units, designer_dev, design, history_src_url
ESTATES = [
    {
        "file": "wah-fu-(i)-estate.html", "zh": "華富(一)邨", "zh_short": "華富邨",
        "en": "Wah Fu (I) Estate", "area": "南區 · 華富",
        "mtr": "港鐵南港島綫華富站（規劃中）；現時依靠巴士接駁香港仔、灣仔",
        "year": "1967 – 1969 年分三期落成",
        "blocks": "12 座（5 座 17-21 層長型 + 7 座 10-15 層長型）",
        "units": "約 4,800 伙",
        "dev": "香港屋宇建設委員會 / 香港房屋委員會（公屋邨）",
        "design": "舊長型 + 香港首批雙塔式/雙井型大廈（華興樓、華生樓、華泰樓、華昌樓）",
        "history": "華富邨由前房屋署署長廖本懷規劃，1967 年首期入伙，被譽為香港首個「公屋新市鎮」，擁有商場、街市、巴士總站等自給自足社區配套。華興樓及華昌樓更係香港首批雙塔式公屋設計。屋邨已納入重建計劃，預計由 2027 年起分階段清拆重建。",
        "wiki": "https://zh.wikipedia.org/zh-hk/%E8%8F%AF%E5%AF%8C%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1321348400445",
        "hero_stats": [("12","座"),("4,800","單位"),("1967-69","落成"),("舊長型+雙塔","設計")],
    },
    {
        "file": "shek-kip-mei-estate.html", "zh": "石硤尾邨",
        "en": "Shek Kip Mei Estate", "area": "深水埗區 · 石硤尾",
        "mtr": "港鐵石硤尾站（觀塘綫）步行 3-8 分鐘",
        "year": "1954 年首期；1973、1977-84 年重建；2007-2019 年再重建",
        "blocks": "22 座（分 8 期）",
        "units": "約 10,600 伙",
        "dev": "香港房屋委員會（公屋邨）",
        "design": "非標準設計／和諧式／舊長型混合；第 41 座美荷樓（舊 H 型徙置大廈）已列二級歷史建築",
        "history": "石硤尾邨是香港第一條公共屋邨，源於 1953 年石硤尾木屋區大火後政府興建嘅徙置區，開啟香港公共房屋歷史。原徙置大廈除第 41 座美荷樓（現活化為青年旅舍）外已全部拆卸重建，現時 8 期共 22 座新廈陸續於 2007-2019 年落成，提供約 10,600 個單位。",
        "wiki": "https://zh.wikipedia.org/zh-hk/%E7%9F%B3%E7%A1%A4%E5%B0%BE%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1321348400469",
        "hero_stats": [("22","座"),("10,600","單位"),("1954-2019","分期落成"),("石硤尾站","最近港鐵")],
    },
    {
        "file": "tai-hang-tung-estate.html", "zh": "大坑東邨",
        "en": "Tai Hang Tung Estate", "area": "深水埗區 · 石硤尾",
        "mtr": "港鐵石硤尾站（觀塘綫）／又一城 九龍塘站步行可達",
        "year": "1983 – 2002 年分階段重建落成",
        "blocks": "9 座",
        "units": "約 2,100 伙",
        "dev": "香港房屋委員會（公屋邨）",
        "design": "相連長型第一款 + 新長型 + 小單位大廈",
        "history": "大坑東邨源於 1955 年嘅徙置區，原址為 1953 年大坑東寮屋區。重建工程於 1979 年展開，1983-2002 年分階段落成現時 9 座大廈，包括東海樓、東輝樓、東成樓、東裕樓、東滿樓、東旺樓等。東海樓等係房委會首批相連第一型大廈，僅 11 層。",
        "wiki": "https://zh-yue.wikipedia.org/wiki/%E5%A4%A7%E5%9D%91%E6%9D%B1%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1321348400362",
        "hero_stats": [("9","座"),("2,100","單位"),("1983-2002","重建落成"),("石硤尾","所在地")],
    },
    {
        "file": "so-uk-estate.html", "zh": "蘇屋邨",
        "en": "So Uk Estate", "area": "深水埗區 · 長沙灣",
        "mtr": "港鐵長沙灣站（荃灣綫）步行 5-10 分鐘",
        "year": "原邨 1960-1963；重建後 2016（第一期）、2019（第二期）",
        "blocks": "14 座（非標準設計）",
        "units": "約 6,985 伙",
        "dev": "香港房屋委員會（公屋邨）",
        "design": "非標準設計大廈（21-41 層），以花卉命名：蘭花樓、壽菊樓、牡丹樓、金松樓、綠柳樓、櫻桃樓、茶花樓等",
        "history": "蘇屋邨原邨由香港屋宇建設委員會於 1960-1963 年興建，曾是香港最大公共屋邨。舊邨 2009 年起清拆重建，新蘇屋邨第一期 7 座於 2016 年 9 月入伙，第二期 7 座於 2019 年 2 月入伙，合共 14 座非標準設計大廈 6,985 個單位，容納約 19,500 人。",
        "wiki": "https://zh.wikipedia.org/zh-hk/%E8%98%87%E5%B1%8B%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1475118454624",
        "hero_stats": [("14","座"),("6,985","單位"),("2016/2019","重建落成"),("長沙灣站","最近港鐵")],
    },
    {
        "file": "butterfly-estate.html", "zh": "蝴蝶邨",
        "en": "Butterfly Estate", "area": "屯門區 · 蝴蝶灣",
        "mtr": "輕鐵蝴蝶站（505、507、610、614、615 綫）步行 1-3 分鐘",
        "year": "1983 年入伙",
        "blocks": "6 座（結構上為 3 幢 Y 字形雙連大廈）",
        "units": "約 2,784 伙（所有單位面積均為 24.93 平方米）",
        "dev": "香港房屋委員會（公屋邨）",
        "design": "Y 字形雙連大廈（＞—＜ 形），香港唯一採用梯級型大廈嘅公共屋邨",
        "history": "蝴蝶邨位於屯門蝴蝶灣，1983 年由原蝴蝶邨計劃嘅第 2、4、6 期發展而成（第 1、3 期改為湖景邨，第 5 期改為居屋兆山苑）。6 座住宅配對成「蝶舞－蝶影」、「蝶翎－蝶心」、「蝶聚－蝶意」共 3 組 Y 字形雙連大廈，形狀與後期 X 型非標準設計相似，係香港唯一梯級型大廈公共屋邨。",
        "wiki": "https://zh.wikipedia.org/wiki/%E8%9D%B4%E8%9D%B6%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1321348400491",
        "hero_stats": [("6","座"),("2,784","單位"),("1983","入伙"),("蝴蝶站","輕鐵")],
    },
    {
        "file": "tai-hing-estate.html", "zh": "大興邨",
        "en": "Tai Hing Estate", "area": "屯門區 · 大興",
        "mtr": "輕鐵大興（北）站、大興（南）站步行 1-3 分鐘",
        "year": "第一期 1977 年；第二期 1979 年入伙",
        "blocks": "7 座（6 座 29 層十字型 + 1 座 7 層長型）",
        "units": "約 4,900 伙",
        "dev": "香港房屋委員會（公屋邨）",
        "design": "十字型大廈（6 座 29 層）+ 長型大廈（1 座 7 層）",
        "history": "大興邨係屯門區第二個公共屋邨，分兩期發展：第一期 1977 年入伙，第二期 1979 年入伙，合共 7 座建築物（6 座 29 層高十字型樓宇加上 1 座 7 層高長型大廈）。大廈以「興」字命名：興昌樓、興泰樓、興盛樓、興平樓、興偉樓、興民樓、興耀樓。",
        "wiki": "https://zh.wikipedia.org/zh-hk/%E5%A4%A7%E8%88%88%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1321348400417",
        "hero_stats": [("7","座"),("4,900","單位"),("1977-79","入伙"),("大興站","輕鐵")],
    },
    {
        "file": "mei-tung-estate.html", "zh": "美東邨",
        "en": "Mei Tung Estate", "area": "九龍城區 · 東頭",
        "mtr": "港鐵樂富站（觀塘綫）步行 6-10 分鐘",
        "year": "美東樓 1974；美寶樓 1983；美仁樓 2010；美德樓 2014",
        "blocks": "4 座",
        "units": "約 1,800 伙（美東樓 + 美寶樓共 665 伙，另加美仁樓、美德樓）",
        "dev": "香港房屋委員會（公屋邨）",
        "design": "舊長型（美東樓）+ 雙塔式（美寶樓）+ 非標準設計（美仁樓、美德樓），橫跨房委會四代設計，被公屋迷譽為「跳格」樓宇史見證",
        "history": "美東邨位於九龍城區東頭，1974 年美東樓首期落成（原編號第 6 座），1983 年美寶樓加入，其後收回培民村、博愛村平房區地皮，於 2010、2014 年加建美仁樓及美德樓。美東樓及美寶樓已納入重建計劃，預計 2028 年前後清拆，新美東邨將提供 2,860 個單位。",
        "wiki": "https://zh.wikipedia.org/zh-hk/%E7%BE%8E%E6%9D%B1%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1321348400518",
        "hero_stats": [("4","座"),("1,800","單位"),("1974-2014","分期落成"),("樂富站","最近港鐵")],
    },
    {
        "file": "shun-tin-estate.html", "zh": "順天邨",
        "en": "Shun Tin Estate", "area": "觀塘區 · 茶寮坳",
        "mtr": "港鐵彩虹站（觀塘綫）／九龍灣站，巴士或小巴接駁",
        "year": "1981 – 1983 年分期入伙",
        "blocks": "11 座",
        "units": "約 6,000 伙",
        "dev": "香港房屋委員會（公屋邨）",
        "design": "I 型 / 雙塔式（19-24 層）",
        "history": "順天邨位於觀塘區茶寮坳，由房委會於 1975 年起北鄰觀塘山坡興建，分三期發展，首兩期共 8 座 19-24 層高 I 型或雙塔式大廈，1981 年首批居民入伙。大廈以「天」字命名：天權樓、天琴樓、天平樓、天樞樓等，屬於香港早期半山上依山而建公屋代表。",
        "wiki": "https://zh.wikipedia.org/zh-hk/%E9%A0%86%E5%A4%A9%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1321348400486",
        "hero_stats": [("11","座"),("6,000","單位"),("1981-83","入伙"),("彩虹/九龍灣","最近港鐵")],
    },
    {
        "file": "oi-man-estate.html", "zh": "愛民邨",
        "en": "Oi Man Estate", "area": "九龍城區 · 何文田",
        "mtr": "港鐵何文田站（屯馬綫、觀塘綫）步行 8-12 分鐘",
        "year": "1974 – 1975 年分期入伙",
        "blocks": "12 座",
        "units": "約 6,300 伙（容納約 17,200 人）",
        "dev": "前香港屋宇建設委員會（房委會改組前最後一個屋邨）",
        "design": "舊長型 + 雙塔式，設有特色井字型中央庭園",
        "history": "愛民邨是前香港屋宇建設委員會改組為房屋委員會之前最後一個興建嘅屋邨，1962-63 年規劃、1970 年動工、1973-1975 年陸續落成，12 座大廈（如衛民樓、敦民樓、嘉民樓、禮民樓、保民樓、建民樓、德民樓等）以「民」字命名。屬於香港第一代大型公共屋邨，設有井字形庭園、商場、街市、幼稚園及 3 座「菇亭」熟食中心。",
        "wiki": "https://zh.wikipedia.org/zh-hk/%E6%84%9B%E6%B0%91%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1321348400453",
        "hero_stats": [("12","座"),("6,300","單位"),("1974-75","入伙"),("何文田站","最近港鐵")],
    },
    {
        "file": "lai-on-estate.html", "zh": "麗安邨",
        "en": "Lai On Estate", "area": "深水埗區 · 長沙灣",
        "mtr": "港鐵長沙灣站（荃灣綫）步行 5-8 分鐘",
        "year": "1993 年入伙",
        "blocks": "5 座",
        "units": "約 2,130 伙",
        "dev": "香港房屋委員會（公屋邨）",
        "design": "Y4 型非標準／和諧 1 型過渡期設計",
        "history": "麗安邨位於深水埗荔枝角道 420 號，1989 年 11 月動工，1993 年入伙，共 5 座樓宇：麗德樓（第 1 座）、麗福樓（第 2 座）、麗榮樓（第 3 座）、麗正樓（第 4 座）、麗平樓（第 5 座）。毗鄰麗閣邨及西九龍中心，交通及生活配套完善。",
        "wiki": "https://zh.wikipedia.org/zh-hk/%E9%BA%97%E5%AE%89%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1321348400457",
        "hero_stats": [("5","座"),("2,130","單位"),("1993","入伙"),("長沙灣站","最近港鐵")],
    },
    {
        "file": "cho-yiu-chuen.html", "zh": "祖堯邨",
        "en": "Cho Yiu Chuen", "area": "葵青區 · 荔景山",
        "mtr": "港鐵荔景站（荃灣綫、東涌綫）步行 8-15 分鐘（上斜）",
        "year": "1976 – 1981 年分三期落成",
        "blocks": "13 座（含啟真樓、啟光樓、啟廉樓、啟恆樓、啟勉樓、啟謙樓、啟敬樓、松齡舍等）",
        "units": "約 2,532 伙",
        "dev": "香港房屋協會（房協屋邨，非房委會公屋）",
        "design": "非標準設計；啟敬樓 38 層為 1981 年落成時全球最高公屋建築",
        "history": "祖堯邨由香港房屋協會發展，1976 至 1981 年分三期落成，位於葵涌荔景山麗祖路、念祖街及榮祖街。第一期（啟真、啟光、啟廉樓）12 層、第二期（啟恆、啟勉、啟謙樓）6-13 層、第三期啟敬樓 38 層係當年全球最高公共屋邨建築。全邨 2,532 伙，容納約 16,000 人，並設長者專用嘅松齡舍。",
        "wiki": "https://zh.wikipedia.org/wiki/%E7%A5%96%E5%A0%AF%E9%82%A8",
        "ha": "https://www.hkhs.com/tc/housing_archive/id/12",
        "hero_stats": [("13","座"),("2,532","單位"),("1976-81","落成"),("荔景站","最近港鐵")],
    },
    {
        "file": "lai-tak-tsuen.html", "zh": "勵德邨",
        "en": "Lai Tak Tsuen", "area": "灣仔區 · 大坑",
        "mtr": "港鐵天后站（港島綫）／銅鑼灣站，巴士接駁大坑道",
        "year": "1975 – 1976 年落成",
        "blocks": "8 座（1-4 座圓筒型；5-8 座長方型）",
        "units": "約 2,468 伙",
        "dev": "香港房屋協會（房協屋邨）",
        "design": "香港唯一圓筒形（雙圓筒）公共屋邨，1-4 座為 27 層圓筒型；5-8 座為 28 層長方型，每層 17 伙",
        "history": "勵德邨由房協興建，原定 1972 年落成，因斜坡山泥傾瀉延期至 1975-1976 年分批入伙，位於灣仔區大坑道東面半山。1-4 座採用香港獨有嘅雙圓筒設計，打破傳統公屋長方形制式，令更多單位享維港景，成為遊客及攝影愛好者打卡熱點。屋邨以已故房協創辦人鄔勵德 (Michael Wright) 命名。",
        "wiki": "https://zh-yue.wikipedia.org/wiki/%E5%8B%B5%E5%BE%B7%E9%82%A8",
        "ha": "https://www.hkhs.com/tc/housing_archive/id/22",
        "hero_stats": [("8","座"),("2,468","單位"),("1975-76","落成"),("雙圓筒","獨特設計")],
    },
    {
        "file": "wah-kwai-estate.html", "zh": "華貴邨",
        "en": "Wah Kwai Estate", "area": "南區 · 華富／田灣",
        "mtr": "港鐵香港大學站 / 規劃中南港島綫華富站；巴士接駁香港仔",
        "year": "1990 年 10 月起入伙",
        "blocks": "6 座",
        "units": "約 3,716 伙（當中 452 伙原本未出售）",
        "dev": "香港房屋委員會（公屋邨）",
        "design": "Y3 型／Y4 型和諧式過渡期大廈，單位實用面積 208-598 呎",
        "history": "華貴邨位於香港島南區華貴道 3 號，鄰近華富邨，1990 年 10 月入伙，共 6 座大廈：華泰樓、華康樓、華孝樓、華禮樓、華信樓、華悌樓（以「孝悌忠信禮義廉恥」為名）。屋邨依山而建，景觀開揚，可遠眺博寮海峽及南丫島。",
        "wiki": "https://zh.wikipedia.org/zh-hk/%E8%8F%AF%E8%B2%B4%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1321348400451",
        "hero_stats": [("6","座"),("3,716","單位"),("1990","入伙"),("南區華富","位置")],
    },
    {
        "file": "wo-che-estate.html", "zh": "禾輋邨",
        "en": "Wo Che Estate", "area": "沙田區 · 沙田市中心",
        "mtr": "港鐵沙田站、大圍站（東鐵綫）步行 5-10 分鐘",
        "year": "1977、1978、1980 年分期落成；2003 年景和樓加建",
        "blocks": "13 座",
        "units": "約 6,500 伙",
        "dev": "香港房屋委員會（公屋邨）",
        "design": "房委會舊長型／雙塔式標準設計；2003 年景和樓為和諧式補建",
        "history": "禾輋邨係沙田區第二個落成嘅公共屋邨，1977 年首批樓宇落成，其後 1978、1980 年再增建，2003 年加建景和樓令總數增至 13 座。所有大廈皆以「和」字命名，如泰和樓、欣和樓、富和樓、景和樓、民和樓、德和樓、福和樓、和安樓、和滿樓等，鄰近沙田市中心、新城市廣場、沙田大會堂，交通及購物配套極為便利。",
        "wiki": "https://zh.wikipedia.org/zh-hk/%E7%A6%BE%E8%BC%8B%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1321348400482",
        "hero_stats": [("13","座"),("6,500","單位"),("1977-2003","分期落成"),("沙田站","最近港鐵")],
    },
    {
        "file": "sha-kok-estate.html", "zh": "沙角邨",
        "en": "Sha Kok Estate", "area": "沙田區 · 沙田圍",
        "mtr": "港鐵沙田圍站（屯馬綫）步行 3-6 分鐘",
        "year": "1980 – 1982 年分期入伙",
        "blocks": "7 座",
        "units": "約 3,900 伙",
        "dev": "香港房屋委員會（公屋邨）",
        "design": "罕有「長型連座」設計（I 型、Y 型混合）",
        "history": "沙角邨位於沙田城河東沙田圍填海地上，1980 年落成，是沙田區第三個公共屋邨，採用比較罕有嘅「長型連座」設計，共 7 座大廈：雲雀樓、鷺鳥樓、金鶯樓、銀鷗樓、杜鵑樓、美麗樓（愉城苑後改名）、翠鳳樓等，以雀鳥命名。第二期 4 座 16 層高、530 個單位曾於 1980 年 1 月撥作居屋愉城苑。",
        "wiki": "https://zh.wikipedia.org/zh-hk/%E6%B2%99%E8%A7%92%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1321348400464",
        "hero_stats": [("7","座"),("3,900","單位"),("1980-82","入伙"),("沙田圍站","最近港鐵")],
    },
    {
        "file": "lei-muk-shue-estate.html", "zh": "梨木樹邨",
        "en": "Lei Muk Shue Estate", "area": "荃灣區 · 上葵涌",
        "mtr": "港鐵大窩口站（荃灣綫）／葵興站，巴士小巴接駁（上斜）",
        "year": "原邨 1975 入伙；第三、四期重建 2005 年落成",
        "blocks": "合共 19 座（梨木樹邨 + 梨木樹（一）邨 + 梨木樹（二）邨）",
        "units": "容納約 27,400 人",
        "dev": "香港房屋委員會（公屋邨）",
        "design": "舊長型（原邨）+ 新和諧式（榕、翠、樂、儉、康樹樓）+ 非標準設計",
        "history": "梨木樹邨位於荃灣區東部上葵涌，分三個子邨：梨木樹（一）邨、梨木樹（二）邨、梨木樹邨（第 3-4 期），合共 19 座。第一代原邨第二期 1-6 座於 1975 年 6 月入伙；第一期 7-14 座隨後落成。原 9-12 座 2002 年起清拆重建，2005 年 3 月落成 5 座新和諧式大廈（榕、翠、樂、儉、康樹樓），由林頌恩建築師有限公司設計。",
        "wiki": "https://zh-yue.wikipedia.org/wiki/%E6%A2%A8%E6%9C%A8%E6%A8%B9%E9%82%A8",
        "ha": "https://www.housingauthority.gov.hk/tc/global-elements/estate-locator/detail.html?propId=1&id=1321348400467",
        "hero_stats": [("19","座"),("27,400","居民"),("1975-2005","分期落成"),("大窩口站","最近港鐵")],
    },
]


def build_info_table(e):
    return f"""<tr><td>中文名稱</td><td>{e['zh']}</td></tr>
<tr><td>英文名稱</td><td>{e['en']}</td></tr>
<tr><td>屋邨類型</td><td>公共屋邨（租住單位）</td></tr>
<tr><td>所在地區</td><td>{e['area']}</td></tr>
<tr><td>最近港鐵</td><td>{e['mtr']}</td></tr>
<tr><td>落成年份</td><td>{e['year']}</td></tr>
<tr><td>總座數</td><td>{e['blocks']}</td></tr>
<tr><td>總單位數</td><td>{e['units']}</td></tr>
<tr><td>發展商 / 管理</td><td>{e['dev']}</td></tr>
<tr><td>設計類型</td><td>{e['design']}</td></tr>
<tr><td>寬頻基建</td><td>光纖／銅線混合（視大廈年代），HKBN、HGC、3HK 覆蓋</td></tr>
<tr><td>裝機時間</td><td>一般 2-5 個工作天</td></tr>"""


def process(e):
    fp = PAGES / e["file"]
    if not fp.exists():
        print(f"MISSING: {e['file']}")
        return False
    s = fp.read_text(encoding="utf-8")
    zh = e["zh"]
    short = e.get("zh_short", zh)

    # Title
    new_title = f"{zh} 寬頻月費比較｜{e['area'].split(' · ')[1] if ' · ' in e['area'] else e['area']} {e['blocks'].split('（')[0]}{e['units'].split('（')[0]} 公共屋邨 - BroadbandHK"
    s = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", s, count=1, flags=re.S)

    # Meta description
    new_desc = (f"{zh}（{e['en']}）係{e['area'].replace(' · ','')}嘅公共屋邨，{e['year']}，"
                f"{e['blocks']}合共{e['units']}。設計類型：{e['design'].split('；')[0]}。"
                f"支援 HKBN 香港寬頻、HGC 環球全域電訊、3HK 和記電訊 覆蓋，光纖月費 $98 起。"
                f"WhatsApp 5228 7541 免費格價。")
    s = re.sub(r'(<meta name="description" content=")[^"]*(")',
               lambda m: m.group(1) + new_desc.replace('"',"'") + m.group(2), s, count=1)

    # Robots
    s = s.replace('<meta name="robots" content="noindex, follow">',
                  '<meta name="robots" content="index, follow">')

    # Hero stats
    stats_html = "\n".join(f'<div><span class="num">{n}</span><span class="lbl">{l}</span></div>' for n,l in e["hero_stats"])
    s = re.sub(r'<div class="hero-stats">.*?</div>\s*</section>',
               f'<div class="hero-stats">\n{stats_html}\n</div>\n</section>',
               s, count=1, flags=re.S)

    # Info-table: replace inner rows
    new_rows = build_info_table(e)
    s = re.sub(r'(<table class="info-table">)(.*?)(</table>)',
               lambda m: m.group(1) + "\n" + new_rows + "\n" + m.group(3),
               s, count=1, flags=re.S)

    # Replace the paragraph after info-table (history + source) — find the <p> immediately after </table>
    history_block = (f'<p style="margin-top:14px;color:#556;font-size:.95em"><strong>🏛️ 屋邨歷史：</strong>{e["history"]}</p>\n'
                     f'<p style="margin-top:10px;color:#556;font-size:.85em">📚 資料來源：'
                     f'<a href="{e["wiki"]}" target="_blank" rel="noopener">維基百科</a>、'
                     f'<a href="{e["ha"]}" target="_blank" rel="noopener">房屋署</a>。各座寬頻覆蓋以 ISP 官方確認為準。</p>')
    # Remove existing <p>...</p> immediately after </table> up to </div>
    s = re.sub(r'(</table>)\s*(<p[^>]*>.*?</p>\s*)+(\s*</div>)',
               lambda m: m.group(1) + "\n" + history_block + "\n" + m.group(3),
               s, count=1, flags=re.S)

    # Remove the fake "1000M 實測速度" FAQ item if exists
    s = re.sub(r'<div class="faq-item"><h3>[^<]*1000M[^<]*實際速度[^<]*</h3><p>[^<]*</p></div>',
               f'<div class="faq-item"><h3>{zh}係邊年落成？有咩特色？</h3><p>{e["history"][:120]}</p></div>',
               s, count=1)

    # Also strip any "1000M 實測速度" table row if somehow still present
    s = re.sub(r'<tr><td>1000M 實測速度</td><td>[^<]*</td></tr>\s*', '', s)

    fp.write_text(s, encoding="utf-8")
    print(f"OK: {e['file']}")
    return True


if __name__ == "__main__":
    done = 0
    for e in ESTATES:
        if process(e):
            done += 1
    print(f"\nTotal processed: {done}/{len(ESTATES)}")
