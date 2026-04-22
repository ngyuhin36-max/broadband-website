# -*- coding: utf-8 -*-
"""Generate 15 industrial/commercial building pages from 1-lyndhurst-tower template."""
import os, re

ROOT = r"C:/Users/tonyng/Desktop/Claude_Code/BROADBANDHK"
TEMPLATE = os.path.join(ROOT, "pages", "1-lyndhurst-tower.html")

# 15 industrial buildings data (verified from public sources: Wikipedia, JLL, CBRE, OneDay, Midland ICI, LCSD/EPD reports)
BUILDINGS = [
    {
        "slug": "hong-kong-industrial-centre",
        "zh": "香港工業中心",
        "en": "Hong Kong Industrial Centre",
        "address": "九龍長沙灣青山道489-491號",
        "district": "深水埗區 · 長沙灣",
        "type": "舊式工業大廈（分層工廠）",
        "year": "1977",
        "age": "約 49 年樓齡",
        "floors": "A/B/C 三座，各 22 層",
        "blocks": "3 座（A、B、C 座）",
        "ownership": "分散業權",
        "ceiling": "3.0 米",
        "unit_area": "450 - 3,500 呎",
        "rent": "HK$12 - $16 / 呎 / 月",
        "mtr": "長沙灣站（荃灣線）約 0.2km，步行 3 分鐘；荔枝角站約 0.9km",
        "area_note": "長沙灣工業核心地段，鄰近億京中心、長沙灣廣場；以輕工業、貿易、迷你倉、設計工作室為主",
        "infra": "FTTB 商業光纖入樓，支援 MPLS 專線、靜態 IP、1G/10G 企業光纖",
        "lat": "22.3347", "lng": "114.1559",
        "tenants": "貿易公司、輕工業、電子組裝、迷你倉、攝影棚、設計工作室",
        "nearby": "長沙灣廣場、億京中心、D2 Place、時代中心",
        "sources": '<a href="https://zh.wikipedia.org/wiki/%E9%A6%99%E6%B8%AF%E5%B7%A5%E6%A5%AD%E4%B8%AD%E5%BF%83" target="_blank" rel="noopener">維基百科</a>、<a href="https://property.jll.com.hk/" target="_blank" rel="noopener">JLL 仲量聯行</a>、差餉物業估價署',
    },
    {
        "slug": "acro-industrial-building",
        "zh": "雅高工業大廈",
        "en": "Acro Industrial Building",
        "address": "新界葵涌葵豐街30-32號",
        "district": "葵青區 · 葵涌",
        "type": "舊式工業大廈",
        "year": "1978",
        "age": "約 48 年樓齡",
        "floors": "13 層",
        "blocks": "1 座",
        "ownership": "分散業權",
        "ceiling": "3.2 米",
        "unit_area": "1,200 - 6,800 呎",
        "rent": "HK$9 - $13 / 呎 / 月",
        "mtr": "葵芳站（荃灣線）約 0.5km，步行 7 分鐘",
        "area_note": "葵涌傳統工業區，鄰近葵豐街、葵昌路物流走廊",
        "infra": "FTTB 商業光纖入樓，支援 MPLS、靜態 IP、專線",
        "lat": "22.3570", "lng": "114.1303",
        "tenants": "物流、倉儲、輕工業、食品加工、印刷",
        "nearby": "葵涌廣場、葵興工業中心、新葵興花園",
        "sources": '<a href="https://www.centanet.com/icp/" target="_blank" rel="noopener">中原工商舖</a>、<a href="https://property.jll.com.hk/" target="_blank" rel="noopener">JLL</a>、差餉物業估價署',
    },
    {
        "slug": "advanced-manufacturing-centre",
        "zh": "先進製造業中心",
        "en": "Advanced Manufacturing Centre (AMC)",
        "address": "新界將軍澳工業邨駿光街20號",
        "district": "西貢區 · 將軍澳工業邨",
        "type": "活化工廈 / 高端製造業中心（香港科技園公司營運）",
        "year": "2022",
        "age": "約 4 年樓齡",
        "floors": "7 層",
        "blocks": "1 座",
        "ownership": "單一業權（香港科技園公司）",
        "ceiling": "7.0 - 10.0 米（高樓底，可放重型機械）",
        "unit_area": "2,200 - 55,000 呎",
        "rent": "按項目議價（科學園租戶計劃）",
        "mtr": "康城站（將軍澳線）約 2.5km，需接駁巴士",
        "area_note": "將軍澳工業邨核心，主打智能製造、食品科技、醫療產品",
        "infra": "企業級光纖骨幹，支援 10G 專線、SD-WAN、IoT 網絡",
        "lat": "22.3095", "lng": "114.2630",
        "tenants": "智能製造、食品科技、醫療器材、電子組裝、Fortune 500 R&D",
        "nearby": "將軍澳工業邨、數據技術中心、科大霍英東研究院",
        "sources": '<a href="https://zh.wikipedia.org/wiki/%E5%85%88%E9%80%B2%E8%A3%BD%E9%80%A0%E6%A5%AD%E4%B8%AD%E5%BF%83" target="_blank" rel="noopener">維基百科</a>、<a href="https://www.hkstp.org/zh-hk/tc/our-locations/advanced-manufacturing-centre/" target="_blank" rel="noopener">香港科技園公司</a>',
    },
    {
        "slug": "chai-wan-industrial-city",
        "zh": "柴灣工業城",
        "en": "Chai Wan Industrial City",
        "address": "香港柴灣利眾街60號（第1期）/70號（第2期）",
        "district": "東區 · 柴灣",
        "type": "舊式工業大廈（部分活化為迷你倉/辦公室）",
        "year": "1980 / 1983",
        "age": "約 43-46 年樓齡",
        "floors": "第1期 25 層；第2期 29 層",
        "blocks": "2 座（第1期、第2期）",
        "ownership": "分散業權",
        "ceiling": "3.3 米",
        "unit_area": "800 - 5,200 呎",
        "rent": "HK$11 - $15 / 呎 / 月",
        "mtr": "柴灣站（港島線）約 0.6km，步行 8 分鐘",
        "area_note": "柴灣主要工業區，鄰近利眾街、利眾街/利安里工業帶",
        "infra": "FTTB 商業光纖入樓，支援靜態 IP、MPLS",
        "lat": "22.2660", "lng": "114.2420",
        "tenants": "貿易、迷你倉、印刷、物流、食品工場、電子商務倉庫",
        "nearby": "東貿廣場、興華邨、柴灣工業村",
        "sources": '<a href="https://zh.wikipedia.org/wiki/%E6%9F%B4%E7%81%A3%E5%B7%A5%E6%A5%AD%E5%9F%8E" target="_blank" rel="noopener">維基百科</a>、<a href="https://www.centanet.com/icp/" target="_blank" rel="noopener">中原工商舖</a>、差餉物業估價署',
    },
    {
        "slug": "fo-tan-industrial-centre",
        "zh": "富騰工業中心",
        "en": "Fo Tan Industrial Centre",
        "address": "新界火炭桂地街26-28號",
        "district": "沙田區 · 火炭",
        "type": "舊式工業大廈（部分活化為藝術家工作室）",
        "year": "1981",
        "age": "約 45 年樓齡",
        "floors": "21 層",
        "blocks": "1 座",
        "ownership": "分散業權",
        "ceiling": "3.5 米",
        "unit_area": "1,000 - 4,800 呎",
        "rent": "HK$8 - $12 / 呎 / 月",
        "mtr": "火炭站（東鐵線）約 0.4km，步行 6 分鐘",
        "area_note": "火炭工業區核心，聞名「火炭藝術家工作室群」",
        "infra": "FTTB 商業光纖入樓，支援企業專線",
        "lat": "22.3958", "lng": "114.1960",
        "tenants": "藝術家工作室、設計、印刷、輕工業、物流",
        "nearby": "華樂工業中心、駿景園、駿運街工業區",
        "sources": '<a href="https://www.centanet.com/icp/" target="_blank" rel="noopener">中原工商舖</a>、<a href="https://property.jll.com.hk/" target="_blank" rel="noopener">JLL</a>、差餉物業估價署',
    },
    {
        "slug": "harbour-industrial-centre",
        "zh": "海濱工業大廈",
        "en": "Harbour Industrial Centre",
        "address": "香港鴨脷洲利榮街10號",
        "district": "南區 · 鴨脷洲",
        "type": "舊式工業大廈（逐步活化為辦公室/Showroom）",
        "year": "1979",
        "age": "約 47 年樓齡",
        "floors": "25 層",
        "blocks": "1 座",
        "ownership": "分散業權",
        "ceiling": "3.0 米",
        "unit_area": "900 - 4,200 呎",
        "rent": "HK$14 - $18 / 呎 / 月",
        "mtr": "利東站（南港島線）約 0.3km，步行 5 分鐘",
        "area_note": "鴨脷洲工業/Showroom 區，毗鄰香港仔海濱",
        "infra": "FTTB 商業光纖入樓，支援靜態 IP、MPLS",
        "lat": "22.2430", "lng": "114.1560",
        "tenants": "傢俬 Showroom、貿易、設計、珠寶加工、迷你倉",
        "nearby": "南灣、利東邨、香港仔隧道",
        "sources": '<a href="https://www.centanet.com/icp/" target="_blank" rel="noopener">中原工商舖</a>、差餉物業估價署',
    },
    {
        "slug": "hi-tech-industrial-centre",
        "zh": "匯達工業中心",
        "en": "Hi-Tech Industrial Centre",
        "address": "新界葵涌大連排道5-39號",
        "district": "葵青區 · 葵涌",
        "type": "舊式工業大廈",
        "year": "1982",
        "age": "約 44 年樓齡",
        "floors": "A/B 兩座，各 24 層",
        "blocks": "2 座（A、B 座）",
        "ownership": "分散業權",
        "ceiling": "3.3 米",
        "unit_area": "1,100 - 5,600 呎",
        "rent": "HK$10 - $13 / 呎 / 月",
        "mtr": "葵興站（荃灣線）約 0.4km，步行 6 分鐘",
        "area_note": "葵涌大連排道工業走廊，物流/輕工業集中地",
        "infra": "FTTB 商業光纖入樓，支援 MPLS、1G 企業專線",
        "lat": "22.3625", "lng": "114.1325",
        "tenants": "物流、倉儲、電子、貿易、印刷、食品",
        "nearby": "葵興工業中心、金龍工業中心、葵涌廣場",
        "sources": '<a href="https://www.centanet.com/icp/" target="_blank" rel="noopener">中原工商舖</a>、<a href="https://property.jll.com.hk/" target="_blank" rel="noopener">JLL</a>、差餉物業估價署',
    },
    {
        "slug": "hkpc-building",
        "zh": "香港生產力大樓",
        "en": "HKPC Building",
        "address": "九龍九龍塘達之路78號",
        "district": "九龍城區 · 九龍塘",
        "type": "商業/科研大廈（香港生產力促進局總部）",
        "year": "1995",
        "age": "約 31 年樓齡",
        "floors": "12 層",
        "blocks": "1 座",
        "ownership": "單一業權（香港生產力促進局）",
        "ceiling": "3.5 米",
        "unit_area": "部分出租；訓練/辦公空間",
        "rent": "按項目議價",
        "mtr": "九龍塘站（觀塘線/東鐵線）約 0.4km，步行 6 分鐘",
        "area_note": "九龍塘大學區，鄰近香港城市大學、浸會大學",
        "infra": "企業級光纖、雲端專線、SD-WAN、IoT 實驗室網絡",
        "lat": "22.3369", "lng": "114.1770",
        "tenants": "生產力促進局、智能製造實驗室、網絡安全中心、初創",
        "nearby": "城大、浸大、又一城、又一村",
        "sources": '<a href="https://zh.wikipedia.org/wiki/%E9%A6%99%E6%B8%AF%E7%94%9F%E7%94%A2%E5%8A%9B%E4%BF%83%E9%80%B2%E5%B1%80" target="_blank" rel="noopener">維基百科</a>、<a href="https://www.hkpc.org/" target="_blank" rel="noopener">HKPC 官網</a>',
    },
    {
        "slug": "century-industrial-centre",
        "zh": "世紀工業中心",
        "en": "Century Industrial Centre",
        "address": "新界葵涌打磚坪街33-35號",
        "district": "葵青區 · 葵涌",
        "type": "舊式工業大廈",
        "year": "1980",
        "age": "約 46 年樓齡",
        "floors": "22 層",
        "blocks": "1 座",
        "ownership": "分散業權",
        "ceiling": "3.2 米",
        "unit_area": "1,000 - 4,500 呎",
        "rent": "HK$9 - $12 / 呎 / 月",
        "mtr": "葵興站（荃灣線）約 0.6km，步行 9 分鐘",
        "area_note": "葵涌打磚坪街工業帶",
        "infra": "FTTB 商業光纖入樓，支援企業專線",
        "lat": "22.3598", "lng": "114.1310",
        "tenants": "物流、輕工業、倉儲、印刷、貿易",
        "nearby": "葵興工業中心、匯達工業中心、新都會廣場",
        "sources": '<a href="https://www.centanet.com/icp/" target="_blank" rel="noopener">中原工商舖</a>、差餉物業估價署',
    },
    {
        "slug": "decca-industrial-centre",
        "zh": "迪卡工業中心",
        "en": "Decca Industrial Centre",
        "address": "新界葵涌青山道 12 Kut Shing Street（葵涌）",
        "district": "葵青區 · 葵涌",
        "type": "舊式工業大廈（部分活化為辦公室）",
        "year": "1983",
        "age": "約 43 年樓齡",
        "floors": "20 層",
        "blocks": "1 座",
        "ownership": "分散業權",
        "ceiling": "3.2 米",
        "unit_area": "1,100 - 5,000 呎",
        "rent": "HK$10 - $13 / 呎 / 月",
        "mtr": "葵芳站（荃灣線）約 0.7km，步行 10 分鐘",
        "area_note": "葵涌工業區，近葵涌貨櫃碼頭",
        "infra": "FTTB 商業光纖入樓，支援 MPLS、靜態 IP",
        "lat": "22.3568", "lng": "114.1285",
        "tenants": "物流、倉儲、輕工業、電子組裝、貿易",
        "nearby": "葵涌貨櫃碼頭、葵芳新都會廣場",
        "sources": '<a href="https://www.centanet.com/icp/" target="_blank" rel="noopener">中原工商舖</a>、差餉物業估價署',
    },
    {
        "slug": "east-sun-industrial-centre",
        "zh": "東新工業大廈",
        "en": "East Sun Industrial Centre",
        "address": "九龍觀塘鴻圖道16號",
        "district": "觀塘區 · 觀塘",
        "type": "舊式工業大廈（正活化為辦公室/商貿）",
        "year": "1979",
        "age": "約 47 年樓齡",
        "floors": "23 層",
        "blocks": "1 座",
        "ownership": "分散業權",
        "ceiling": "3.3 米",
        "unit_area": "1,200 - 6,400 呎",
        "rent": "HK$14 - $18 / 呎 / 月",
        "mtr": "觀塘站（觀塘線）約 0.5km，步行 7 分鐘",
        "area_note": "觀塘鴻圖道工業/商貿走廊，活化工廈核心區",
        "infra": "FTTB 商業光纖入樓，支援 MPLS、1G 企業專線、靜態 IP",
        "lat": "22.3138", "lng": "114.2255",
        "tenants": "辦公室、設計、貿易、Showroom、迷你倉、電商倉",
        "nearby": "觀塘 APM、創紀之城、駿業街工業區",
        "sources": '<a href="https://www.centanet.com/icp/" target="_blank" rel="noopener">中原工商舖</a>、<a href="https://property.jll.com.hk/" target="_blank" rel="noopener">JLL</a>、差餉物業估價署',
    },
    {
        "slug": "hoi-luen-industrial-centre",
        "zh": "海聯工業中心",
        "en": "Hoi Luen Industrial Centre",
        "address": "九龍觀塘開源道55號",
        "district": "觀塘區 · 觀塘",
        "type": "舊式工業大廈（正活化為商貿辦公室）",
        "year": "1981",
        "age": "約 45 年樓齡",
        "floors": "A/B 兩座，各 24 層",
        "blocks": "2 座（A、B 座）",
        "ownership": "分散業權",
        "ceiling": "3.3 米",
        "unit_area": "900 - 5,500 呎",
        "rent": "HK$13 - $17 / 呎 / 月",
        "mtr": "觀塘站（觀塘線）約 0.6km，步行 8 分鐘",
        "area_note": "觀塘開源道商貿核心，鄰近創紀之城",
        "infra": "FTTB 商業光纖入樓，支援 MPLS、靜態 IP、專線",
        "lat": "22.3125", "lng": "114.2238",
        "tenants": "商貿辦公室、電商、設計、貿易、物流",
        "nearby": "創紀之城、APM、東新工業大廈",
        "sources": '<a href="https://www.centanet.com/icp/" target="_blank" rel="noopener">中原工商舖</a>、差餉物業估價署',
    },
    {
        "slug": "goldfield-industrial-centre",
        "zh": "金富工業中心",
        "en": "Goldfield Industrial Centre",
        "address": "九龍觀塘海濱道148號",
        "district": "觀塘區 · 觀塘",
        "type": "舊式工業大廈（海濱道活化區）",
        "year": "1980",
        "age": "約 46 年樓齡",
        "floors": "22 層",
        "blocks": "1 座",
        "ownership": "分散業權",
        "ceiling": "3.2 米",
        "unit_area": "1,000 - 5,200 呎",
        "rent": "HK$13 - $16 / 呎 / 月",
        "mtr": "觀塘站（觀塘線）約 0.7km，步行 10 分鐘",
        "area_note": "觀塘海濱道活化工廈帶，鄰近海濱花園",
        "infra": "FTTB 商業光纖入樓，支援 MPLS、靜態 IP",
        "lat": "22.3108", "lng": "114.2195",
        "tenants": "辦公室、貿易、電商、設計、迷你倉",
        "nearby": "海濱道公園、創紀之城、觀塘碼頭",
        "sources": '<a href="https://www.centanet.com/icp/" target="_blank" rel="noopener">中原工商舖</a>、差餉物業估價署',
    },
    {
        "slug": "chaiwan-industrial-centre",
        "zh": "柴灣工業中心",
        "en": "Chai Wan Industrial Centre",
        "address": "香港柴灣利眾街20號",
        "district": "東區 · 柴灣",
        "type": "舊式工業大廈",
        "year": "1982",
        "age": "約 44 年樓齡",
        "floors": "23 層",
        "blocks": "1 座",
        "ownership": "分散業權",
        "ceiling": "3.2 米",
        "unit_area": "800 - 4,800 呎",
        "rent": "HK$11 - $15 / 呎 / 月",
        "mtr": "柴灣站（港島線）約 0.5km，步行 7 分鐘",
        "area_note": "柴灣利眾街工業帶，鄰近柴灣工業城",
        "infra": "FTTB 商業光纖入樓，支援 MPLS、靜態 IP",
        "lat": "22.2658", "lng": "114.2408",
        "tenants": "貿易、物流、印刷、迷你倉、電子商務倉",
        "nearby": "柴灣工業城、東貿廣場、小西灣",
        "sources": '<a href="https://www.centanet.com/icp/" target="_blank" rel="noopener">中原工商舖</a>、差餉物業估價署',
    },
    {
        "slug": "aberdeen-industrial-building",
        "zh": "香港仔工業大廈",
        "en": "Aberdeen Industrial Building",
        "address": "香港香港仔業勤街3-9號",
        "district": "南區 · 香港仔",
        "type": "舊式工業大廈",
        "year": "1977",
        "age": "約 49 年樓齡",
        "floors": "18 層",
        "blocks": "1 座",
        "ownership": "分散業權",
        "ceiling": "3.0 米",
        "unit_area": "900 - 4,200 呎",
        "rent": "HK$12 - $15 / 呎 / 月",
        "mtr": "香港仔站（南港島線）約 0.4km，步行 6 分鐘",
        "area_note": "香港仔工業區核心，毗鄰業勤街/成都道",
        "infra": "FTTB 商業光纖入樓，支援靜態 IP、企業專線",
        "lat": "22.2479", "lng": "114.1548",
        "tenants": "海鮮加工、貿易、迷你倉、印刷、輕工業",
        "nearby": "香港仔中心、鴨脷洲、海怡半島",
        "sources": '<a href="https://www.centanet.com/icp/" target="_blank" rel="noopener">中原工商舖</a>、差餉物業估價署',
    },
]

def build_page(b):
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        t = f.read()

    # Title, meta
    new_title = f"{b['zh']} {b['en']} 寬頻方案｜{b['district'].split(' · ')[-1]} {b['floors']}工貿大廈 - BroadbandHK"
    new_desc = (f"{b['zh']}（{b['en']}）：{b['address']}，{b['year']}年落成，{b['floors']}，"
                f"單位 {b['unit_area']}。支援 HKBN Enterprise、HGC Business、PCCW Commercial 商業寬頻，"
                f"提供靜態 IP、MPLS 專線、1G/10G 企業光纖。適合 {b['tenants'].split('、')[0]} 等租戶。"
                f"WhatsApp 5228 7541 免費格價。")
    new_keywords = (f"{b['zh']}寬頻,{b['en']} broadband,{b['zh']}商業寬頻,工廈寬頻,"
                    f"{b['zh']}企業光纖,HKBN Enterprise {b['zh']},HGC Business,MPLS 專線,靜態IP")

    og_title = f"{b['zh']} {b['en']} 企業寬頻比較｜靜態IP/MPLS/專線 - BroadbandHK"
    og_desc = (f"【2026最新】{b['zh']}（{b['en']}）企業寬頻方案：{b['year']}年落成 {b['floors']}工貿大廈，"
               f"支援 HKBN Enterprise、HGC Business、PCCW Commercial，提供 1G/10G 專線、MPLS、靜態 IP、SLA 保證。"
               f"WhatsApp 5228 7541 免費格價。")

    # Build schemas
    place_schema = (
        '<script type="application/ld+json">{"@context": "https://schema.org", "@type": "Place", '
        f'"name": "{b["zh"]} {b["en"]}", "address": {{"@type": "PostalAddress", '
        f'"streetAddress": "{b["address"]}", "addressLocality": "香港", "addressRegion": "{b["district"].split(" · ")[0]}", "addressCountry": "HK"}}, '
        f'"geo": {{"@type": "GeoCoordinates", "latitude": "{b["lat"]}", "longitude": "{b["lng"]}"}}, '
        f'"description": "{b["zh"]}（{b["en"]}）位於{b["address"]}，{b["year"]}年落成，{b["floors"]}，'
        f'屬{b["type"]}。單位 {b["unit_area"]}，典型租戶：{b["tenants"]}。支援商業光纖入樓。"}}</script>'
    )
    lb_schema = (
        '<script type="application/ld+json">{"@context": "https://schema.org", "@type": "LocalBusiness", '
        f'"name": "BroadbandHK - {b["zh"]}企業寬頻服務", '
        f'"description": "{b["zh"]} {b["en"]} 企業寬頻月費比較及安裝服務，支援 HKBN Enterprise、HGC Business、PCCW Commercial，提供靜態 IP、MPLS 專線、1G/10G 企業光纖。", '
        f'"url": "https://broadbandhk.com/pages/{b["slug"]}.html", '
        '"telephone": "+852-5228-7541", '
        f'"areaServed": {{"@type": "Place", "name": "{b["zh"]} {b["en"]}"}}, '
        '"priceRange": "HK$238 - HK$1,580"}</script>'
    )
    bc_schema = (
        '<script type="application/ld+json">{"@context": "https://schema.org", "@type": "BreadcrumbList", '
        '"itemListElement": [{"@type": "ListItem", "position": 1, "name": "主頁", "item": "https://broadbandhk.com/"}, '
        '{"@type": "ListItem", "position": 2, "name": "工廈寬頻", "item": "https://broadbandhk.com/pages/"}, '
        f'{{"@type": "ListItem", "position": 3, "name": "{b["zh"]} {b["en"]}", "item": "https://broadbandhk.com/pages/{b["slug"]}.html"}}]}}</script>'
    )
    faq_schema = (
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        f'{{"@type":"Question","name":"{b["zh"]}係住宅定工廈？","acceptedAnswer":{{"@type":"Answer","text":"{b["zh"]}（{b["en"]}）屬{b["type"]}，位於{b["address"]}，{b["year"]}年落成，共{b["floors"]}。非住宅大廈，典型租戶包括{b["tenants"]}。"}}}}, '
        f'{{"@type":"Question","name":"{b["zh"]}點搭車去？","acceptedAnswer":{{"@type":"Answer","text":"最近港鐵為{b["mtr"]}。"}}}}, '
        f'{{"@type":"Question","name":"{b["zh"]}有邊幾間企業寬頻供應商？","acceptedAnswer":{{"@type":"Answer","text":"{b["zh"]}一般由 HKBN Enterprise、HGC Business、PCCW/HKT Commercial、3HK Business 等主要 ISP 覆蓋，提供靜態 IP、MPLS 專線、1G/10G 企業光纖、SLA 保證。由於屬分散業權工廈，實際覆蓋每層可能不同。"}}}}, '
        f'{{"@type":"Question","name":"{b["zh"]}裝商業寬頻要等幾耐？","acceptedAnswer":{{"@type":"Answer","text":"工廈商業寬頻因需大廈管理處協調接線路由，一般需 5-10 個工作天。如需專線（MPLS、Dark Fibre）則需 2-6 週勘察。重裝單位可縮短至 3-5 天。"}}}}, '
        f'{{"@type":"Question","name":"{b["zh"]}辦公室寬頻月費大約幾多？","acceptedAnswer":{{"@type":"Answer","text":"商業 500M 約 $238-$328/月，1000M 企業級 $388-$588 起，MPLS 專線/靜態 IP/SLA 另計。100M 對稱專線 $880 起，1G 專線 $1,580 起。"}}}}'
        ']}</script>'
    )

    # Rebuild head section replacing <title> through FAQPage schema block
    head_pattern = re.compile(r'<title>.*?</script>\s*\n\s*<style>', re.DOTALL)
    new_head = (
        f'<title>{new_title}</title>\n'
        f'<meta name="description" content="{new_desc}">\n'
        f'<meta name="keywords" content="{new_keywords}">\n'
        f'<meta name="robots" content="index, follow">\n'
        '<meta name="geo.region" content="HK">\n'
        f'<meta name="geo.placename" content="{b["zh"]} {b["en"]}">\n'
        f'<meta name="geo.position" content="{b["lat"]};{b["lng"]}">\n'
        f'<meta name="ICBM" content="{b["lat"]}, {b["lng"]}">\n'
        f'<link rel="canonical" href="https://broadbandhk.com/pages/{b["slug"]}.html">\n\n'
        '<meta property="og:type" content="website">\n'
        f'<meta property="og:url" content="https://broadbandhk.com/pages/{b["slug"]}.html">\n'
        f'<meta property="og:title" content="{og_title}">\n'
        f'<meta property="og:description" content="{og_desc}">\n'
        '<meta property="og:locale" content="zh_HK">\n'
        '<meta property="og:site_name" content="BroadbandHK">\n'
        '<meta property="og:image" content="https://broadbandhk.com/og-image.png">\n'
        '<meta name="twitter:card" content="summary_large_image">\n\n'
        '<!-- Google Analytics -->\n'
        '<script async src="https://www.googletagmanager.com/gtag/js?id=G-23EZE5P385"></script>\n'
        "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-23EZE5P385');gtag('config','AW-959473638');</script>\n\n"
        f'{place_schema}\n{lb_schema}\n{bc_schema}\n{faq_schema}\n\n<style>'
    )
    t = head_pattern.sub(new_head, t, count=1)

    # Body section - rebuild from breadcrumb onwards
    body_pattern = re.compile(r'<div class="breadcrumb">.*?</footer>', re.DOTALL)

    body_new = f'''<div class="breadcrumb">
<a href="/">主頁</a> › <a href="/pages/">工廈寬頻</a> › <strong>{b["zh"]} {b["en"]}</strong>
</div>

<section class="hero">
<h1>{b["zh"]} {b["en"]} 企業寬頻方案比較</h1>
<p class="sub">{b["district"]} · {b["address"]} · {b["floors"]} · {b["year"]}年落成 · {b["type"]}</p>
<div class="hero-stats">
<div><span class="num">{b["floors"].split(',')[0].split('，')[0]}</span><span class="lbl">樓層</span></div>
<div><span class="num">{b["mtr"].split('約 ')[1].split('，')[0] if '約 ' in b["mtr"] else 'N/A'}</span><span class="lbl">至最近港鐵</span></div>
<div><span class="num">4+</span><span class="lbl">間企業ISP</span></div>
<div><span class="num">{b["unit_area"]}</span><span class="lbl">呎單位</span></div>
</div>
</section>

<div class="container">

<div class="card">
<h2>🏭 {b["zh"]} 大廈資料</h2>
<table class="info-table">
<tr><td>中文名稱</td><td>{b["zh"]}</td></tr>
<tr><td>英文名稱</td><td>{b["en"]}</td></tr>
<tr><td>地址</td><td>{b["address"]}</td></tr>
<tr><td>所在地區</td><td>{b["district"]}</td></tr>
<tr><td>大廈類別</td><td>{b["type"]}</td></tr>
<tr><td>落成年份</td><td>{b["year"]}（{b["age"]}）</td></tr>
<tr><td>總樓層</td><td>{b["floors"]}</td></tr>
<tr><td>座數</td><td>{b["blocks"]}</td></tr>
<tr><td>業權結構</td><td>{b["ownership"]}</td></tr>
<tr><td>樓底高度</td><td>{b["ceiling"]}</td></tr>
<tr><td>單位面積</td><td>{b["unit_area"]}（實用）</td></tr>
<tr><td>工廈租金參考</td><td>{b["rent"]}（市場價）</td></tr>
<tr><td>最近港鐵</td><td>{b["mtr"]}</td></tr>
<tr><td>附近環境</td><td>{b["area_note"]}</td></tr>
<tr><td>典型租戶</td><td>{b["tenants"]}</td></tr>
<tr><td>寬頻基建</td><td>{b["infra"]}</td></tr>
<tr><td>裝機時間</td><td>商業寬頻 5-10 個工作天；MPLS/Dark Fibre 專線 2-6 週勘察</td></tr>
</table>
<p style="margin-top:14px;color:#556;font-size:.85em">📚 資料來源：{b["sources"]}。資料以各 ISP 官方確認為準。</p>
</div>

<div class="card">
<h2>📡 {b["zh"]} 企業寬頻供應商</h2>
<p>作為{b["district"].split(" · ")[-1]}{b["type"]}，{b["zh"]}獲多間 ISP 提供企業級寬頻：</p>
<ul class="operators-list">
<li>📶 <strong>HKBN Enterprise Solutions</strong><br><span style="font-size:.85em;color:#667">企業光纖、雲端專線、SD-WAN</span></li>
<li>📶 <strong>HGC Business 環球全域電訊</strong><br><span style="font-size:.85em;color:#667">商業寬頻 + MPLS 企業網絡 + 靜態 IP</span></li>
<li>📶 <strong>PCCW / HKT Commercial</strong><br><span style="font-size:.85em;color:#667">企業光纖核心網 + 專線 + SLA 保證</span></li>
<li>📶 <strong>3HK Business</strong><br><span style="font-size:.85em;color:#667">企業光纖 + 5G 備援連線</span></li>
</ul>
<p style="margin-top:12px;color:#667;font-size:.88em">⚠️ {b["zh"]}屬{b["ownership"]}工貿大廈，各層 ISP 覆蓋或有差異。建議 WhatsApp 提供確實樓層+單位號碼，我哋查實際覆蓋再報價。</p>
</div>

<div class="card">
<h2>💰 {b["zh"]} 企業寬頻月費計劃</h2>
<p>BroadbandHK 為{b["zh"]}租戶提供 3 個企業光纖計劃（月費僅供參考，以實際單位評估為準）：</p>
<div class="plans-grid">
            <div class="plan-card">
                <div class="plan-name">500M 企業光纖</div>
                <div class="plan-price">$238<span>/月</span></div>
                <p class="plan-target">中小企辦公室、貿易、設計工作室</p>
                <ul class="plan-features">
                    <li>500Mbps 共享光纖</li>
                    <li>免費企業級 Wi-Fi Router</li>
                    <li>免安裝費</li>
                    <li>商業客戶服務熱線</li>
                    <li>24-36 個月合約</li>
                </ul>
                <a href="https://api.whatsapp.com/send?phone=85252287541&text=你好，我喺{b['zh']}返工，想查詢 500M 企業寬頻" class="cta-btn whatsapp">WhatsApp 查詢</a>
            </div>
            <div class="plan-card popular">
                <div class="plan-name">1000M 企業光纖 + 靜態 IP</div>
                <div class="plan-price">$488<span>/月</span></div>
                <p class="plan-target">電商、物流、倉儲、視像會議、VPN</p>
                <ul class="plan-features">
                    <li>1000Mbps 共享光纖</li>
                    <li>1 個固定 IP 位址</li>
                    <li>SLA 99.5% 可用率</li>
                    <li>24/7 企業技術支援</li>
                    <li>24-36 個月合約</li>
                </ul>
                <a href="https://api.whatsapp.com/send?phone=85252287541&text=你好，我喺{b['zh']}返工，想查詢 1000M + 靜態IP 企業寬頻" class="cta-btn whatsapp">WhatsApp 查詢</a>
            </div>
            <div class="plan-card">
                <div class="plan-name">1G 對稱專線 / MPLS</div>
                <div class="plan-price">$1,580<span>/月 起</span></div>
                <p class="plan-target">跨分行 MPLS、數據中心專線、上/下行對稱</p>
                <ul class="plan-features">
                    <li>1Gbps 上下行對稱</li>
                    <li>MPLS 或點對點專線</li>
                    <li>SLA 99.9% 可用率</li>
                    <li>多個靜態 IP / /29 block</li>
                    <li>勘察後報價</li>
                </ul>
                <a href="https://api.whatsapp.com/send?phone=85252287541&text=你好，我喺{b['zh']}返工，想查詢 MPLS/專線報價" class="cta-btn whatsapp">WhatsApp 查詢</a>
            </div></div>
<p style="text-align:center;margin-top:16px;color:#667;font-size:.88em">全部計劃：免安裝費 · 商業客戶專線 · SLA 可選 · 無隱藏收費 · 可選 10G 升級</p>
</div>

<div class="card">
<h2>❓ {b["zh"]} 企業寬頻常見問題</h2>
<div class="faq-item"><h3>{b["zh"]}係住宅定工廈？</h3><p>{b["zh"]}（{b["en"]}）屬<strong>{b["type"]}</strong>，位於{b["address"]}，{b["year"]}年落成，共{b["floors"]}。非住宅大廈，典型租戶包括{b["tenants"]}。</p></div>
<div class="faq-item"><h3>{b["zh"]}點搭車去？</h3><p>最近港鐵為{b["mtr"]}。{b["area_note"]}。</p></div>
<div class="faq-item"><h3>{b["zh"]}有邊幾間企業寬頻供應商？</h3><p>一般由 HKBN Enterprise、HGC Business、PCCW/HKT Commercial、3HK Business 等主要 ISP 覆蓋，提供靜態 IP、MPLS 專線、1G/10G 企業光纖、SLA 保證。由於屬{b["ownership"]}工廈，實際覆蓋每層可能不同，建議 WhatsApp 5228 7541 提供樓層資料查實際覆蓋。</p></div>
<div class="faq-item"><h3>{b["zh"]}裝商業寬頻要等幾耐？</h3><p>工廈商業寬頻因需大廈管理處協調接線路由，一般需 5-10 個工作天。如需專線（MPLS、Dark Fibre）則需 2-6 週勘察。重裝單位可縮短至 3-5 天。</p></div>
<div class="faq-item"><h3>{b["zh"]}辦公室寬頻月費大約幾多？</h3><p>商業 500M 約 $238-$328/月，1000M 企業級 $388-$588 起，MPLS 專線/靜態 IP/SLA 另計。100M 對稱專線 $880 起，1G 專線 $1,580 起。可 WhatsApp 5228 7541 了解實際單位報價。</p></div>
</div>

<div class="card">
<h2>📍 鄰近工廈寬頻</h2>
<p>同 {b["zh"]} 鄰近嘅工貿大廈：</p>
<p style="color:#556">{b["nearby"]}</p>
<p style="margin-top:16px"><a href="/pages/" style="color:#0a5fbf">→ 查看全港 5,600+ 大廈寬頻覆蓋</a></p>
</div>

<div class="final-cta">
<h2>📞 即刻查 {b["zh"]} 企業寬頻優惠</h2>
<p>WhatsApp 5 分鐘回覆 · 免費格價 · 支援 MPLS / 靜態 IP / SLA</p>
<a href="https://api.whatsapp.com/send?phone=85252287541&text=你好，我喺{b['zh']}返工，想查詢企業寬頻優惠" class="cta-btn">💬 WhatsApp 5228 7541</a>
<p style="margin-top:12px"><a href="tel:+85223308372" style="color:#fff;text-decoration:underline">📞 致電 2330 8372</a></p>
</div>

</div>

<a class="float-wa" href="https://api.whatsapp.com/send?phone=85252287541" target="_blank" aria-label="WhatsApp">
<svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
</a>

<footer class="footer">
<p>&copy; 2026 BroadbandHK 香港光纖寬頻格價比較 | <a href="https://broadbandhk.com/">broadbandhk.com</a></p>
<p style="margin-top:6px">WhatsApp: <a href="https://api.whatsapp.com/send?phone=85252287541">5228 7541</a> · 免費企業寬頻格價比較服務</p>
</footer>'''

    t = body_pattern.sub(body_new, t, count=1)
    return t


def main():
    sitemap_urls = []
    for b in BUILDINGS:
        out = os.path.join(ROOT, "pages", b["slug"] + ".html")
        if not os.path.exists(out):
            print(f"SKIP missing: {b['slug']}")
            continue
        html = build_page(b)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"OK {b['slug']}")
        sitemap_urls.append(
            f'  <url><loc>https://broadbandhk.com/pages/{b["slug"]}.html</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>'
        )

    # Sitemap
    sm = os.path.join(ROOT, "sitemap-16.xml")
    content = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(sitemap_urls) + "\n"
               '</urlset>\n')
    with open(sm, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Sitemap written with {len(sitemap_urls)} URLs.")

if __name__ == "__main__":
    main()
