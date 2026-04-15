# -*- coding: utf-8 -*-
"""Enrich commercial tower pages with real data. Idempotent replacement of
template blocks on 15 iconic HK commercial buildings.
"""
import os, re, sys

PAGES = os.path.join(os.path.dirname(__file__), 'pages')

# Each entry provides substitution data for one tower.
TOWERS = [
    {
        'file': 'central-plaza.html',
        'zh': '中環廣場', 'en': 'Central Plaza', 'short': '中環廣場',
        'slug': 'central-plaza',
        'title': '中環廣場 Central Plaza 商業寬頻比較｜灣仔 78 層甲級寫字樓 - BroadbandHK',
        'desc': '中環廣場 (Central Plaza)：灣仔港灣道 18 號，1992 年落成，78 層 / 374 米甲級寫字樓，距會展站 / 灣仔站步行約 3-5 分鐘。支援 HKBN Enterprise、PCCW Commercial、HGC Business 企業光纖，提供 SLA、靜態 IP、MPLS 專線。WhatsApp 5228 7541 免費格價。',
        'kw': '中環廣場商業寬頻,Central Plaza broadband,灣仔甲廈寬頻,HKBN Enterprise 中環廣場,PCCW Commercial,靜態 IP,SLA 專線',
        'addr': '香港灣仔港灣道 18 號',
        'lat': '22.2838', 'lng': '114.1738',
        'district': '灣仔區 · 灣仔核心商業區',
        'completed': '1992 年 8 月',
        'floors': '78 層',
        'height': '374 米（樓頂天線連塔 374m）',
        'architect': 'Dennis Lau & Ng Chun Man 建築師事務所',
        'developer': '新世界發展、恆基、合和、黃廷芳家族等財團',
        'ownership': '分層業權（原由財團合資發展，多戶持有）',
        'tenants': 'BNP Paribas、信安保險、中銀國際、英皇娛樂、香港 JEBSEN、各專業服務公司',
        'mtr': '會展站（東鐵線過海段）約 300 米；灣仔站（港島線）步行約 5 分鐘',
        'rent': 'HK$45 - $75 / 呎 / 月（甲級寫字樓）',
        'wiki': 'https://en.wikipedia.org/wiki/Central_Plaza_(Hong_Kong)',
        'src2_url': 'https://www.cbdofficehk.com/central-plaza',
        'src2_name': 'CBD Office HK',
        'hero_sub': '灣仔 · 港灣道 18 號 · 78 層甲級寫字樓 · 1992 年落成 · 374 米',
        'stat1_num': '78', 'stat1_lbl': '層甲廈',
        'stat2_num': '0.3km', 'stat2_lbl': '至會展站',
        'stat3_num': '4+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '374m', 'stat4_lbl': '建築高度',
        'class': '甲級商業寫字樓（非住宅）',
        'history': '中環廣場 1992 年落成時為全港最高建築，三角形平面及粉紅、金、銀玻璃幕牆極具辨識度，至今仍是灣仔商業區地標之一，樓頂 Rainbow Lightning 報時燈為香港著名夜景。',
    },
    {
        'file': 'hopewell-centre.html',
        'zh': '合和中心', 'en': 'Hopewell Centre', 'short': '合和中心',
        'slug': 'hopewell-centre',
        'title': '合和中心 Hopewell Centre 商業寬頻比較｜灣仔 64 層圓筒形寫字樓 - BroadbandHK',
        'desc': '合和中心 (Hopewell Centre)：灣仔皇后大道東 183 號，1980 年落成，64 層圓筒形商業寫字樓，距灣仔站約 450 米。支援 HKBN Enterprise、PCCW Commercial、HGC Business、中信 CPC 企業光纖，提供 SLA、靜態 IP。WhatsApp 5228 7541 免費格價。',
        'kw': '合和中心商業寬頻,Hopewell Centre broadband,灣仔寫字樓寬頻,HKBN Enterprise,PCCW Commercial,SLA 專線',
        'addr': '香港灣仔皇后大道東 183 號',
        'lat': '22.2750', 'lng': '114.1722',
        'district': '灣仔區 · 灣仔',
        'completed': '1980 年',
        'floors': '64 層',
        'height': '216 米',
        'architect': '甘銘建築師（Gordon Wu 合和實業主理設計）',
        'developer': '合和實業 Hopewell Holdings',
        'ownership': '單一業權（合和實業持有出租）',
        'tenants': '合和集團總部、中小企辦公室、律師行、工程顧問、國際義工組織等；頂層設 62/F 旋轉餐廳',
        'mtr': '灣仔站（港島線）步行約 6 分鐘（450 米），經皇后大道東步行系統',
        'rent': 'HK$38 - $52 / 呎 / 月',
        'wiki': 'https://en.wikipedia.org/wiki/Hopewell_Centre_(Hong_Kong)',
        'src2_url': 'https://www.midlandici.com.hk/en/building/WAC-Wan-Chai-Hopewell-Centre/B000020128',
        'src2_name': 'Midland IC&I',
        'hero_sub': '灣仔 · 皇后大道東 183 號 · 64 層圓筒形甲廈 · 1980 年落成 · 216 米',
        'stat1_num': '64', 'stat1_lbl': '層商廈',
        'stat2_num': '450m', 'stat2_lbl': '至灣仔站',
        'stat3_num': '4+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '216m', 'stat4_lbl': '建築高度',
        'class': '商業寫字樓（非住宅，圓筒形設計）',
        'history': '合和中心 1980 年落成時為香港最高建築，由合和實業主席胡應湘主導興建，是香港首幢圓形摩天大樓，象徵灣仔 80 年代商業發展。頂層 62 樓設旋轉餐廳，辦公樓層集中於 16-60 樓。',
    },
    {
        'file': 'times-square.html',
        'zh': '時代廣場', 'en': 'Times Square', 'short': '時代廣場',
        'slug': 'times-square',
        'title': '時代廣場 Times Square 商業寬頻比較｜銅鑼灣 Tower 1/2 甲級寫字樓 - BroadbandHK',
        'desc': '時代廣場 (Times Square)：銅鑼灣勿地臣街 1 號，1994 年落成，一座 46 層（Tower 1）+ 二座 36 層（Tower 2）甲級寫字樓，直達銅鑼灣站 A 出口。支援 HKBN Enterprise、PCCW Commercial、HGC Business 企業光纖，提供 SLA、靜態 IP。WhatsApp 5228 7541 免費格價。',
        'kw': '時代廣場商業寬頻,Times Square broadband,銅鑼灣寫字樓寬頻,HKBN Enterprise,PCCW Commercial,Wharf 寫字樓',
        'addr': '香港銅鑼灣勿地臣街 1 號',
        'lat': '22.2800', 'lng': '114.1826',
        'district': '灣仔區 · 銅鑼灣核心商業 / 零售區',
        'completed': '1994 年 4 月',
        'floors': 'Tower 1：46 層；Tower 2：36 層（合共 59 層辦公樓面）',
        'height': 'Tower 1 約 199 米；Tower 2 約 172 米',
        'architect': 'Wong &amp; Ouyang (HK) Ltd.',
        'developer': '九龍倉集團 The Wharf (Holdings)',
        'ownership': '單一業權（九倉持有並出租）',
        'tenants': 'PCCW、滙豐私人銀行、法資律師行、跨國時尚品牌亞太辦公室等；商場樓層為 LCX、Lane Crawford、Apple Store 等零售旗艦',
        'mtr': '銅鑼灣站（港島線）A 出口直達（地下連接）',
        'rent': 'HK$60 - $95 / 呎 / 月（甲級寫字樓）',
        'wiki': 'https://en.wikipedia.org/wiki/Times_Square_(Hong_Kong)',
        'src2_url': 'https://www.cbdofficehk.com/times-square',
        'src2_name': 'CBD Office HK',
        'hero_sub': '銅鑼灣 · 勿地臣街 1 號 · Tower 1 46 層 + Tower 2 36 層 · 1994 年落成',
        'stat1_num': '46+36', 'stat1_lbl': '層雙座甲廈',
        'stat2_num': '0km', 'stat2_lbl': '直達銅鑼灣站',
        'stat3_num': '4+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '980k', 'stat4_lbl': '呎寫字樓面積',
        'class': '甲級商業寫字樓 + 零售商場綜合體',
        'history': '時代廣場 1994 年由九倉發展，是香港首個「垂直購物中心」概念，底層 16 層為高端商場、上層兩座辦公大樓提供接近 980,000 呎寫字樓面積，至今仍是銅鑼灣核心商業地標。',
    },
    {
        'file': 'lippo-centre.html',
        'zh': '力寶中心', 'en': 'Lippo Centre', 'short': '力寶中心',
        'slug': 'lippo-centre',
        'title': '力寶中心 Lippo Centre 商業寬頻比較｜金鐘 46/42 層雙子甲廈 - BroadbandHK',
        'desc': '力寶中心 (Lippo Centre)：金鐘金鐘道 89 號，1988 年落成，Tower 1（46 層）+ Tower 2（42 層）雙子甲級寫字樓，毗鄰金鐘站。原名 Bond Centre。支援 HKBN Enterprise、PCCW Commercial、HGC Business 企業光纖，提供 SLA、靜態 IP、MPLS。WhatsApp 5228 7541 免費格價。',
        'kw': '力寶中心商業寬頻,Lippo Centre broadband,金鐘寫字樓寬頻,HKBN Enterprise,PCCW Commercial,Bond Centre',
        'addr': '香港金鐘金鐘道 89 號',
        'lat': '22.2795', 'lng': '114.1644',
        'district': '中西區 · 金鐘核心商業區',
        'completed': '1988 年',
        'floors': 'Tower 1：46 層（186 米）；Tower 2：42 層（172 米）',
        'height': 'Tower 1 186 米；Tower 2 172 米',
        'architect': 'Paul Rudolph（美國建築大師）',
        'developer': '原 Bond Corporation；1988 年後由力寶集團 Lippo Group 接手',
        'ownership': '分層業權（多單位出售 / 出租）',
        'tenants': '力寶集團、多間律師行、金融公司、領事館、中小企辦公室',
        'mtr': '金鐘站（荃灣線 / 港島線 / 南港島線 / 東鐵線過海段）B 出口直達',
        'rent': 'HK$55 - $80 / 呎 / 月（甲級）',
        'wiki': 'https://en.wikipedia.org/wiki/Lippo_Centre_(Hong_Kong)',
        'src2_url': 'https://www.cbdofficehk.com/lippo-centre',
        'src2_name': 'CBD Office HK',
        'hero_sub': '金鐘 · 金鐘道 89 號 · 46 層 + 42 層雙子甲廈 · 1988 年落成',
        'stat1_num': '46+42', 'stat1_lbl': '層雙子塔',
        'stat2_num': '0km', 'stat2_lbl': '直達金鐘站',
        'stat3_num': '4+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '186m', 'stat4_lbl': 'Tower 1 高度',
        'class': '甲級商業寫字樓（雙子塔，非住宅）',
        'history': '力寶中心 1988 年落成，原名 Bond Centre，由美國建築大師 Paul Rudolph 設計，以獨特「樹熊攀樹」形雙子塔聞名。1988 年 Bond Corporation 陷財困後，力寶集團接手並改名 Lippo Centre，成為金鐘商業地標之一。',
    },
    {
        'file': 'bank-of-china-tower.html',
        'zh': '中銀大廈', 'en': 'Bank of China Tower', 'short': '中銀大廈',
        'slug': 'bank-of-china-tower',
        'title': '中銀大廈 Bank of China Tower 商業寬頻比較｜中環 72 層貝聿銘設計甲廈 - BroadbandHK',
        'desc': '中銀大廈 (Bank of China Tower)：中環花園道 1 號，1990 年落成，貝聿銘設計，72 層 / 367 米甲級寫字樓，毗鄰中環站 / 金鐘站。支援 HKBN Enterprise、PCCW Commercial、HGC Business、中信 CPC 等企業光纖，提供 SLA、靜態 IP、MPLS 金融級專線。WhatsApp 5228 7541 免費格價。',
        'kw': '中銀大廈商業寬頻,Bank of China Tower broadband,中環寫字樓寬頻,HKBN Enterprise,PCCW Commercial,貝聿銘',
        'addr': '香港中環花園道 1 號',
        'lat': '22.2790', 'lng': '114.1616',
        'district': '中西區 · 中環 / 金鐘交界核心商業區',
        'completed': '1990 年 5 月正式啟用（1989 年竣工）',
        'floors': '72 層',
        'height': '367.4 米（連天線 367m；至頂樓 315m）',
        'architect': '貝聿銘 I. M. Pei（Pei Cobb Freed &amp; Partners）',
        'developer': '中國銀行（香港）— 由中銀集團持有自用',
        'ownership': '單一業權（中銀自用及招租部分樓層）',
        'tenants': '中國銀行（香港）總行、中銀國際、各國駐港商務辦事處、跨國律師行、私人銀行',
        'mtr': '中環站 J2 出口步行約 5 分鐘；金鐘站 B 出口步行約 5 分鐘',
        'rent': 'HK$95 - $150 / 呎 / 月（頂級甲廈）',
        'wiki': 'https://en.wikipedia.org/wiki/Bank_of_China_Tower_(Hong_Kong)',
        'src2_url': 'https://bochk.com/m/en/aboutus/corpprofile/boctower.html',
        'src2_name': '中銀官網',
        'hero_sub': '中環 · 花園道 1 號 · 貝聿銘設計 · 72 層 / 367 米 · 1990 年啟用',
        'stat1_num': '72', 'stat1_lbl': '層甲廈',
        'stat2_num': '0.4km', 'stat2_lbl': '至中環站',
        'stat3_num': '5+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '367m', 'stat4_lbl': '建築高度',
        'class': '頂級甲級商業寫字樓（銀行總部自用 + 出租）',
        'history': '中銀大廈 1990 年啟用，由貝聿銘大師設計，以「竹節拔高」棱柱造型及鑽石形玻璃幕牆成為香港地標。落成時為亞洲最高、全球第五高建築，現為中國銀行（香港）總行。',
    },
    {
        'file': 'citic-tower.html',
        'zh': '中信大廈', 'en': 'CITIC Tower', 'short': '中信大廈',
        'slug': 'citic-tower',
        'title': '中信大廈 CITIC Tower 商業寬頻比較｜金鐘添美道 1 號 33 層甲廈 - BroadbandHK',
        'desc': '中信大廈 (CITIC Tower)：金鐘添美道 1 號，1997 年落成，33 層 / 126 米甲級寫字樓，經天橋直達金鐘站。支援 HKBN Enterprise、PCCW Commercial、HGC Business、中信國際電訊 CPC 企業光纖，提供 SLA、靜態 IP、MPLS 專線。WhatsApp 5228 7541 免費格價。',
        'kw': '中信大廈商業寬頻,CITIC Tower broadband,金鐘寫字樓寬頻,HKBN Enterprise,PCCW Commercial,中信 CPC',
        'addr': '香港金鐘添美道 1 號',
        'lat': '22.2819', 'lng': '114.1641',
        'district': '中西區 · 金鐘核心商業區',
        'completed': '1997 年',
        'floors': '33 層',
        'height': '126 米（413 呎）',
        'architect': 'Ng Chun Man &amp; Associates Architects &amp; Engineers',
        'developer': '中信泰富（現中信股份）CITIC Pacific / CITIC Limited',
        'ownership': '單一業權（中信自用及出租）',
        'tenants': '中信股份總部、中信國際電訊 CPC、各金融 / 法律專業服務公司',
        'mtr': '金鐘站 B / C 出口行人天橋直達（連接統一中心、海富中心）',
        'rent': 'HK$75 - $110 / 呎 / 月（甲級）',
        'wiki': 'https://en.wikipedia.org/wiki/CITIC_Tower',
        'src2_url': 'https://property.jll.com.hk/en/office-lease/hong-kong/admiralty/citic-tower-hkg-p-0003iv',
        'src2_name': 'JLL 仲量聯行',
        'hero_sub': '金鐘 · 添美道 1 號 · 33 層甲級寫字樓 · 1997 年落成 · 中信集團總部',
        'stat1_num': '33', 'stat1_lbl': '層甲廈',
        'stat2_num': '0km', 'stat2_lbl': '天橋直達金鐘站',
        'stat3_num': '5+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '126m', 'stat4_lbl': '建築高度',
        'class': '甲級商業寫字樓（CBD Grade A）',
        'history': '中信大廈 1997 年落成，由中信泰富快速興建作為集團總部，面向維港景觀開揚。底層連接金鐘行人天橋網絡，可直達海富中心、統一中心、金鐘站及添馬政府總部，為金鐘甲廈代表之一。',
    },
    {
        'file': 'cheung-kong-center.html',
        'zh': '長江集團中心', 'en': 'Cheung Kong Center', 'short': '長江中心',
        'slug': 'cheung-kong-center',
        'title': '長江集團中心 Cheung Kong Center 商業寬頻比較｜中環 70 層甲廈 - BroadbandHK',
        'desc': '長江集團中心 (Cheung Kong Center)：中環皇后大道中 2 號，1999 年落成，César Pelli 設計，70 層 / 283 米甲級寫字樓，毗鄰中環站。支援 HKBN Enterprise、PCCW Commercial、HGC Business 企業光纖，提供 SLA、靜態 IP、MPLS 專線。WhatsApp 5228 7541 免費格價。',
        'kw': '長江集團中心商業寬頻,Cheung Kong Center broadband,中環寫字樓寬頻,HKBN Enterprise,長江中心,PCCW Commercial',
        'addr': '香港中環皇后大道中 2 號',
        'lat': '22.2802', 'lng': '114.1614',
        'district': '中西區 · 中環核心商業區',
        'completed': '1999 年',
        'floors': '70 層（7-70/F 為甲級寫字樓，五層地下停車場）',
        'height': '283 米（928 呎）',
        'architect': 'César Pelli（Pelli Clarke Pelli Architects）',
        'developer': '長江實業 / 和記黃埔（現長和系 CK Hutchison）',
        'ownership': '單一業權（長和自用及出租）',
        'tenants': '長和系總部、Bloomberg、Barclays、Blackstone、Goldman Sachs（部分）、BlackRock、Franklin Templeton 等跨國金融機構',
        'mtr': '中環站 J2 / K 出口步行約 4 分鐘；金鐘站 B 出口步行約 7 分鐘',
        'rent': 'HK$100 - $170 / 呎 / 月（頂級甲廈）',
        'wiki': 'https://en.wikipedia.org/wiki/Cheung_Kong_Center',
        'src2_url': 'https://www.savviprop.com/cheung-kong-center',
        'src2_name': 'SAVVI 商廈',
        'hero_sub': '中環 · 皇后大道中 2 號 · 70 層甲級寫字樓 · 1999 年落成 · 長和系總部',
        'stat1_num': '70', 'stat1_lbl': '層甲廈',
        'stat2_num': '0.3km', 'stat2_lbl': '至中環站',
        'stat3_num': '5+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '283m', 'stat4_lbl': '建築高度',
        'class': '頂級甲級商業寫字樓（非住宅）',
        'history': '長江集團中心 1999 年由 César Pelli 設計落成，位處中環「金三角」（鄰匯豐、中銀、渣打總行）。70 層全甲級寫字樓面積逾 126 萬呎，為長和系總部及多間國際金融機構香港辦事處所在。',
    },
    {
        'file': 'exchange-square.html',
        'zh': '交易廣場', 'en': 'Exchange Square', 'short': '交易廣場',
        'slug': 'exchange-square',
        'title': '交易廣場 Exchange Square 商業寬頻比較｜中環置地三座甲廈 - BroadbandHK',
        'desc': '交易廣場 (Exchange Square)：中環康樂廣場 8 號，一 / 二座 1985 年、三座 1988 年落成，52 / 51 / 33 層甲級寫字樓，直達香港站 / 中環站。支援 HKBN Enterprise、PCCW Commercial、HGC Business 企業光纖，提供 SLA、靜態 IP、MPLS。WhatsApp 5228 7541 免費格價。',
        'kw': '交易廣場商業寬頻,Exchange Square broadband,中環置地甲廈,港交所寫字樓,HKBN Enterprise,PCCW Commercial',
        'addr': '香港中環康樂廣場 8 號',
        'lat': '22.2849', 'lng': '114.1585',
        'district': '中西區 · 中環核心金融區',
        'completed': 'One / Two Exchange Square：1985 年；Three Exchange Square：1988 年',
        'floors': 'One：52 層；Two：51 層；Three：33 層',
        'height': 'One / Two 各 188 米；Three 144 米',
        'architect': 'Palmer and Turner（巴馬丹拿）',
        'developer': '置地公司 Hongkong Land',
        'ownership': '單一業權（置地持有出租；港交所 HKEX 2025 年購入 9 層作永久總部）',
        'tenants': '香港交易所（HKEX）、各大投行、基金、律師行；底層為中環巴士總站',
        'mtr': '中環站 A 出口經行人天橋步行約 4 分鐘；香港站 E1 出口步行約 3 分鐘',
        'rent': 'HK$105 - $165 / 呎 / 月（頂級甲廈）',
        'wiki': 'https://en.wikipedia.org/wiki/Exchange_Square_(Hong_Kong)',
        'src2_url': 'https://www.cbdofficehk.com/exchange-square',
        'src2_name': 'CBD Office HK',
        'hero_sub': '中環 · 康樂廣場 8 號 · 三座甲級寫字樓 · 1985-1988 年落成 · HKEX 所在',
        'stat1_num': '52', 'stat1_lbl': '層（One Exchange）',
        'stat2_num': '0.3km', 'stat2_lbl': '至中環 / 香港站',
        'stat3_num': '5+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '188m', 'stat4_lbl': 'One / Two 高度',
        'class': '頂級甲級商業寫字樓（三座綜合體，非住宅）',
        'history': '交易廣場 1985 年由置地發展落成，三座高層甲廈曾為香港聯合交易所及前港交所總部所在。2025 年 HKEX 再購入 9 層作永久總部。綜合地下中環巴士總站，連接中環 / 香港站行人天橋系統。',
    },
    {
        'file': 'chater-house.html',
        'zh': '遮打大廈', 'en': 'Chater House', 'short': '遮打大廈',
        'slug': 'chater-house',
        'title': '遮打大廈 Chater House 商業寬頻比較｜中環康樂廣場 30 層甲廈 - BroadbandHK',
        'desc': '遮打大廈 (Chater House)：中環干諾道中 8 號，2002 年落成，KPF 設計，30 層甲級寫字樓，毗鄰中環站 / 香港站。支援 HKBN Enterprise、PCCW Commercial、HGC Business 企業光纖，提供 SLA、靜態 IP、MPLS 專線。WhatsApp 5228 7541 免費格價。',
        'kw': '遮打大廈商業寬頻,Chater House broadband,中環置地甲廈,JP Morgan 寫字樓,HKBN Enterprise',
        'addr': '香港中環干諾道中 8 號',
        'lat': '22.2828', 'lng': '114.1596',
        'district': '中西區 · 中環核心金融區',
        'completed': '2002 年',
        'floors': '30 層寫字樓 + 3 層商場 + 3 層地庫',
        'height': '約 170 米',
        'architect': 'Kohn Pedersen Fox (KPF)',
        'developer': '置地公司 Hongkong Land',
        'ownership': '單一業權（置地持有出租）',
        'tenants': 'JP Morgan（主要租戶）、多間跨國投行及私人銀行；商場層為 Armani / Bulgari 旗艦店',
        'mtr': '中環站 K 出口行人天橋直達；香港站 E2 出口步行約 5 分鐘',
        'rent': 'HK$120 - $180 / 呎 / 月（頂級甲廈）',
        'wiki': 'https://en.wikipedia.org/wiki/Chater_House',
        'src2_url': 'https://www.hkland.com/en/properties/hong-kong/chater-house',
        'src2_name': '置地官網 Hongkong Land',
        'hero_sub': '中環 · 干諾道中 8 號 · 30 層甲級寫字樓 · 2002 年落成 · KPF 設計',
        'stat1_num': '30', 'stat1_lbl': '層甲廈',
        'stat2_num': '0km', 'stat2_lbl': '天橋直達中環站',
        'stat3_num': '5+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '474k', 'stat4_lbl': '呎淨寫字樓面積',
        'class': '頂級甲級商業寫字樓（JP Morgan 總部所在）',
        'history': '遮打大廈 2002 年由置地發展，KPF 設計，原址為香港會所及太古大廈。落成後即由 JP Morgan 作亞洲總部，並連接中環置地行人天橋系統（Landmark、Prince\'s、Alexandra House 互通）。',
    },
    {
        'file': 'jardine-house.html',
        'zh': '怡和大廈', 'en': 'Jardine House', 'short': '怡和大廈',
        'slug': 'jardine-house',
        'title': '怡和大廈 Jardine House 商業寬頻比較｜中環 52 層圓窗甲廈 - BroadbandHK',
        'desc': '怡和大廈 (Jardine House)：中環康樂廣場 1 號，1973 年落成，52 層 / 179 米甲級寫字樓，以圓窗聞名，毗鄰中環站 / 香港站。支援 HKBN Enterprise、PCCW Commercial、HGC Business 企業光纖，提供 SLA、靜態 IP、MPLS。WhatsApp 5228 7541 免費格價。',
        'kw': '怡和大廈商業寬頻,Jardine House broadband,中環置地甲廈,康樂大廈,HKBN Enterprise',
        'addr': '香港中環康樂廣場 1 號',
        'lat': '22.2850', 'lng': '114.1591',
        'district': '中西區 · 中環核心金融區',
        'completed': '1973 年',
        'floors': '52 層（46 層寫字樓：3-48/F）',
        'height': '178.5 米',
        'architect': 'Palmer and Turner（巴馬丹拿）',
        'developer': '置地公司 Hongkong Land（原名 Connaught Centre 康樂大廈，1989 年改名怡和大廈）',
        'ownership': '單一業權（置地持有出租）',
        'tenants': '怡和集團、多間會計師行、律師行、跨國企業亞太辦公室',
        'mtr': '中環站 A 出口行人天橋直達；香港站 E1 出口步行約 2 分鐘',
        'rent': 'HK$90 - $140 / 呎 / 月（甲級）',
        'wiki': 'https://en.wikipedia.org/wiki/Jardine_House',
        'src2_url': 'https://www.cbdofficehk.com/jardine-house',
        'src2_name': 'CBD Office HK',
        'hero_sub': '中環 · 康樂廣場 1 號 · 52 層圓窗甲廈 · 1973 年落成 · 香港首幢摩天大樓',
        'stat1_num': '52', 'stat1_lbl': '層甲廈',
        'stat2_num': '0km', 'stat2_lbl': '天橋直達中環站',
        'stat3_num': '5+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '696k', 'stat4_lbl': '呎寫字樓面積',
        'class': '甲級商業寫字樓（香港首幢真正摩天大樓）',
        'history': '怡和大廈 1973 年落成時為亞洲最高建築，原名「康樂大廈 Connaught Centre」，1989 年 1 月改名怡和大廈。其 1,748 個直徑 1.75 米圓窗為港島標誌，連接中環行人天橋系統核心。',
    },
    {
        'file': 'world-wide-house.html',
        'zh': '環球大廈', 'en': 'World-Wide House', 'short': '環球大廈',
        'slug': 'world-wide-house',
        'title': '環球大廈 World-Wide House 商業寬頻比較｜中環德輔道中 32 層甲廈 - BroadbandHK',
        'desc': '環球大廈 (World-Wide House)：中環德輔道中 19 號，32 層商業寫字樓，毗鄰中環站（經行人天橋直達）。支援 HKBN Enterprise、PCCW Commercial、HGC Business 企業光纖，提供 SLA、靜態 IP。WhatsApp 5228 7541 免費格價。',
        'kw': '環球大廈商業寬頻,World-Wide House broadband,中環寫字樓寬頻,HKBN Enterprise,PCCW Commercial',
        'addr': '香港中環德輔道中 19 號',
        'lat': '22.2832', 'lng': '114.1583',
        'district': '中西區 · 中環核心商業區',
        'completed': '1980 年',
        'floors': '32 層（23 層寫字樓：4-27/F + 4 層零售 G-3/F）',
        'height': '約 130 米',
        'architect': 'Palmer and Turner（巴馬丹拿）',
        'developer': '信和置業 / 尖沙咀置業集團（原由 World-Wide Shipping 環球航運發展）',
        'ownership': '分層業權（多戶持有出租）',
        'tenants': '中小企辦公室、貿易公司、律師 / 會計事務所、外幣兌換店、旅行社；底層商場為菲律賓 / 印尼族裔聚腳地',
        'mtr': '中環站 A 出口行人天橋直達（連接置地廣場、太子大廈、遮打大廈）',
        'rent': 'HK$45 - $75 / 呎 / 月（甲乙級）',
        'wiki': 'https://en.wikipedia.org/wiki/World-Wide_House',
        'src2_url': 'https://property.jll.com.hk/en/office-lease/hong-kong/central/world-wide-house-hkg-p-000kq5',
        'src2_name': 'JLL 仲量聯行',
        'hero_sub': '中環 · 德輔道中 19 號 · 32 層商業寫字樓 · 1980 年落成 · 天橋直達中環站',
        'stat1_num': '32', 'stat1_lbl': '層商廈',
        'stat2_num': '0km', 'stat2_lbl': '天橋直達中環站',
        'stat3_num': '4+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '23', 'stat4_lbl': '層寫字樓',
        'class': '商業寫字樓 + 零售商場綜合體',
        'history': '環球大廈 1980 年落成，位於中環舊郵政總局及舊環球大廈原址，是中環首批連接行人天橋網絡嘅商廈之一。業權分散，租金較置地系甲廈親民，吸引中小企及貿易公司。',
    },
    {
        'file': 'hysan-place.html',
        'zh': '希慎廣場', 'en': 'Hysan Place', 'short': '希慎廣場',
        'slug': 'hysan-place',
        'title': '希慎廣場 Hysan Place 商業寬頻比較｜銅鑼灣 40 層綠建甲廈 - BroadbandHK',
        'desc': '希慎廣場 (Hysan Place)：銅鑼灣軒尼詩道 500 號，2012 年落成，KPF 設計，40 層甲級寫字樓 + 商場綜合體，直達銅鑼灣站 F 出口。支援 HKBN Enterprise、PCCW Commercial、HGC Business 企業光纖，提供 SLA、靜態 IP。WhatsApp 5228 7541 免費格價。',
        'kw': '希慎廣場商業寬頻,Hysan Place broadband,銅鑼灣寫字樓寬頻,HKBN Enterprise,PCCW Commercial,希慎興業',
        'addr': '香港銅鑼灣軒尼詩道 500 號',
        'lat': '22.2796', 'lng': '114.1818',
        'district': '灣仔區 · 銅鑼灣核心商業 / 零售區',
        'completed': '2012 年 8 月',
        'floors': '40 層（15 層寫字樓 + 17 層商場 + 停車場 / 機房）',
        'height': '約 230 米',
        'architect': 'Kohn Pedersen Fox (KPF)',
        'developer': '希慎興業 Hysan Development',
        'ownership': '單一業權（希慎持有自用 + 出租）',
        'tenants': '希慎興業總部、Facebook / Meta 香港辦公室、法資 / 日資企業亞太辦公室、Apple Store、誠品書店（商場層）',
        'mtr': '銅鑼灣站（港島線）F 出口直達',
        'rent': 'HK$70 - $110 / 呎 / 月（甲級）',
        'wiki': 'https://en.wikipedia.org/wiki/Hysan_Place',
        'src2_url': 'https://www.hysan.com.hk/portfolio/hysan-place/',
        'src2_name': '希慎興業官網',
        'hero_sub': '銅鑼灣 · 軒尼詩道 500 號 · 40 層甲級寫字樓 + 商場 · 2012 年落成',
        'stat1_num': '40', 'stat1_lbl': '層甲廈',
        'stat2_num': '0km', 'stat2_lbl': '直達銅鑼灣站',
        'stat3_num': '5+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '710k', 'stat4_lbl': '呎總樓面',
        'class': '甲級商業寫字樓 + 零售商場綜合體（LEED Platinum 綠建）',
        'history': '希慎廣場 2012 年由希慎興業於原興利中心 Hennessy Centre 原址重建落成，KPF 設計，獲 LEED Platinum 及香港首個 BEAM Plus Platinum 認證。為銅鑼灣首個港鐵直達嘅綠色甲廈。',
    },
    {
        'file': 'admiralty-centre.html',
        'zh': '海富中心', 'en': 'Admiralty Centre', 'short': '海富中心',
        'slug': 'admiralty-centre',
        'title': '海富中心 Admiralty Centre 商業寬頻比較｜金鐘 Tower 1 / 2 甲廈 - BroadbandHK',
        'desc': '海富中心 (Admiralty Centre)：金鐘夏慤道 18 號，1980 年落成，Tower 1（32 層甲廈）+ Tower 2（26 層），直達金鐘站。支援 HKBN Enterprise、PCCW Commercial、HGC Business 企業光纖，提供 SLA、靜態 IP、MPLS 專線。WhatsApp 5228 7541 免費格價。',
        'kw': '海富中心商業寬頻,Admiralty Centre broadband,金鐘寫字樓寬頻,HKBN Enterprise,PCCW Commercial',
        'addr': '香港金鐘夏慤道 18 號',
        'lat': '22.2795', 'lng': '114.1649',
        'district': '中西區 · 金鐘核心商業區',
        'completed': '1980 年',
        'floors': 'Tower 1：32 層；Tower 2：26 層（+ 3 層商場）',
        'height': 'Tower 1 約 117 米；Tower 2 約 100 米',
        'architect': 'Leigh &amp; Orange 利安顧問',
        'developer': '長江實業 Cheung Kong Holdings（港鐵為地主 Landlord，地面為金鐘站上蓋）',
        'ownership': '分層業權（多戶持有出租）',
        'tenants': '保險公司、律師行、旅行社、政府部門辦公室、中小企',
        'mtr': '金鐘站 A / C / D 出口直達（地下及商場層連接）',
        'rent': 'HK$48 - $72 / 呎 / 月',
        'wiki': 'https://en.wikipedia.org/wiki/Admiralty_Centre',
        'src2_url': 'https://www.cbdofficehk.com/admiralty-centre',
        'src2_name': 'CBD Office HK',
        'hero_sub': '金鐘 · 夏慤道 18 號 · Tower 1 32 層 + Tower 2 26 層 · 1980 年落成 · 金鐘站上蓋',
        'stat1_num': '32+26', 'stat1_lbl': '層雙座',
        'stat2_num': '0km', 'stat2_lbl': '金鐘站上蓋',
        'stat3_num': '4+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '58', 'stat4_lbl': '合共樓層',
        'class': '商業寫字樓（甲級 Tower 1 + 商場綜合體）',
        'history': '海富中心 1980 年由長江實業發展，為金鐘站上蓋物業之一，樓下設金鐘（海富）巴士總站，並連接中信大廈、統一中心行人天橋網絡。為金鐘最早嘅商業綜合體之一。',
    },
    {
        'file': 'united-centre.html',
        'zh': '統一中心', 'en': 'United Centre', 'short': '統一中心',
        'slug': 'united-centre',
        'title': '統一中心 United Centre 商業寬頻比較｜金鐘金鐘道 95 號 33 層甲廈 - BroadbandHK',
        'desc': '統一中心 (United Centre)：金鐘金鐘道 95 號，1981 年落成，33 層寫字樓，行人天橋直達金鐘站。總樓面約 554,000 呎。支援 HKBN Enterprise、PCCW Commercial、HGC Business 企業光纖，提供 SLA、靜態 IP、MPLS 專線。WhatsApp 5228 7541 免費格價。',
        'kw': '統一中心商業寬頻,United Centre broadband,金鐘寫字樓寬頻,HKBN Enterprise,PCCW Commercial',
        'addr': '香港金鐘金鐘道 95 號',
        'lat': '22.2797', 'lng': '114.1642',
        'district': '中西區 · 金鐘核心商業區',
        'completed': '1981 年',
        'floors': '33 層寫字樓（2-6, 8-35/F）+ 1 層零售 + 1 層停車場',
        'height': '約 150 米',
        'architect': 'Palmer and Turner（巴馬丹拿）',
        'developer': '長江實業 / 和記黃埔合作發展',
        'ownership': '分層業權（多戶持有出租）',
        'tenants': '領事館、貿易公司、律師 / 會計行、中小企、保險公司',
        'mtr': '金鐘站 F 出口行人天橋直達（連接力寶中心、太古廣場、中信大廈）',
        'rent': 'HK$52 - $78 / 呎 / 月',
        'wiki': 'https://en.wikipedia.org/wiki/United_Centre',
        'src2_url': 'https://property.jll.com.hk/en/office-lease/hong-kong/admiralty/united-centre-hkg-p-000jxm',
        'src2_name': 'JLL 仲量聯行',
        'hero_sub': '金鐘 · 金鐘道 95 號 · 33 層寫字樓 · 1981 年落成 · 天橋直達金鐘站',
        'stat1_num': '33', 'stat1_lbl': '層寫字樓',
        'stat2_num': '0km', 'stat2_lbl': '天橋直達金鐘站',
        'stat3_num': '4+', 'stat3_lbl': '間 ISP 覆蓋',
        'stat4_num': '554k', 'stat4_lbl': '呎總樓面',
        'class': '商業寫字樓（甲乙級）',
        'history': '統一中心 1981 年落成，為金鐘早期商業綜合體之一，行人天橋連接太古廣場、力寶中心、中信大廈及金鐘站，形成金鐘 24 小時商業動線，至今仍吸引中小企、律師行及多國領事館進駐。',
    },
]

def build_head(t):
    """Return dict of replacements keyed on original strings in template."""
    return {
        'title': t['title'],
        'desc': t['desc'],
        'kw': t['kw'],
        'zh': t['zh'], 'en': t['en'],
        'slug': t['slug'],
        'lat': t['lat'], 'lng': t['lng'],
    }

def enrich(file, t):
    path = os.path.join(PAGES, file)
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()

    zh = t['zh']; en = t['en']; slug = t['slug']
    desc = t['desc']; kw = t['kw']; title = t['title']
    addr = t['addr']; lat = t['lat']; lng = t['lng']
    district = t['district']; completed = t['completed']
    floors = t['floors']; height = t['height']; architect = t['architect']
    developer = t['developer']; ownership = t['ownership']
    tenants = t['tenants']; mtr = t['mtr']; rent = t['rent']
    wiki = t['wiki']; src2_url = t['src2_url']; src2_name = t['src2_name']
    cls = t['class']; history = t['history']
    hero_sub = t['hero_sub']
    s1n = t['stat1_num']; s1l = t['stat1_lbl']
    s2n = t['stat2_num']; s2l = t['stat2_lbl']
    s3n = t['stat3_num']; s3l = t['stat3_lbl']
    s4n = t['stat4_num']; s4l = t['stat4_lbl']

    # 1. Title
    s = re.sub(
        r'<title>[^<]*</title>',
        f"<title>{title}</title>",
        s, count=1
    )
    # 2. Description
    s = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{desc}">',
        s, count=1
    )
    # 3. Keywords
    s = re.sub(
        r'<meta name="keywords" content="[^"]*">',
        f'<meta name="keywords" content="{kw}">',
        s, count=1
    )
    # 4. robots
    s = s.replace('<meta name="robots" content="noindex, follow">',
                  '<meta name="robots" content="index, follow">')
    # 5. geo position
    s = re.sub(r'<meta name="geo.position" content="[^"]*">',
               f'<meta name="geo.position" content="{lat};{lng}">', s)
    s = re.sub(r'<meta name="ICBM" content="[^"]*">',
               f'<meta name="ICBM" content="{lat}, {lng}">', s)
    # 6. og:title / og:description
    s = re.sub(r'<meta property="og:title" content="[^"]*">',
               f'<meta property="og:title" content="{title}">', s)
    s = re.sub(r'<meta property="og:description" content="[^"]*">',
               f'<meta property="og:description" content="{desc}">', s)

    # 7. Schema Place JSON-LD
    place_json = (
        '{"@context":"https://schema.org","@type":"Place",'
        f'"name":"{zh} {en}",'
        f'"address":{{"@type":"PostalAddress","streetAddress":"{addr}","addressLocality":"香港","addressRegion":"香港","addressCountry":"HK"}},'
        f'"geo":{{"@type":"GeoCoordinates","latitude":"{lat}","longitude":"{lng}"}},'
        f'"description":"{zh}（{en}）位於{addr}，{completed}落成，{floors}，{cls}。最近港鐵：{mtr}。"}}'
    )
    s = re.sub(
        r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "Place"[^<]*</script>',
        f'<script type="application/ld+json">{place_json}</script>',
        s, count=1
    )

    # 8. LocalBusiness
    lb_json = (
        '{"@context":"https://schema.org","@type":"LocalBusiness",'
        f'"name":"BroadbandHK - {zh}商業寬頻服務",'
        f'"description":"{zh} {en} 商業寬頻及企業專線比較，支援 HKBN Enterprise、PCCW Commercial、HGC Business 等，提供 SLA / 靜態 IP / MPLS。",'
        f'"url":"https://broadbandhk.com/pages/{slug}.html",'
        '"telephone":"+852-5228-7541",'
        f'"areaServed":{{"@type":"Place","name":"{zh} {en}"}},'
        '"priceRange":"HK$238 - HK$1888"}'
    )
    s = re.sub(
        r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "LocalBusiness"[^<]*</script>',
        f'<script type="application/ld+json">{lb_json}</script>',
        s, count=1
    )

    # 9. Breadcrumb
    bc_json = (
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"主頁","item":"https://broadbandhk.com/"},'
        '{"@type":"ListItem","position":2,"name":"屋苑寬頻","item":"https://broadbandhk.com/pages/"},'
        f'{{"@type":"ListItem","position":3,"name":"{zh} {en}","item":"https://broadbandhk.com/pages/{slug}.html"}}]}}'
    )
    s = re.sub(
        r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "BreadcrumbList"[^<]*</script>',
        f'<script type="application/ld+json">{bc_json}</script>',
        s, count=1
    )

    # 10. FAQ JSON
    faq_json = (
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        f'{{"@type":"Question","name":"{zh}係住宅定商廈？","acceptedAnswer":{{"@type":"Answer","text":"{zh}（{en}）係{cls}，{completed}落成，{floors}，位於{addr}。租戶包括：{tenants}。"}}}},'
        f'{{"@type":"Question","name":"{zh}點搭車去？","acceptedAnswer":{{"@type":"Answer","text":"最近港鐵：{mtr}。"}}}},'
        f'{{"@type":"Question","name":"{zh}有邊幾間商業寬頻供應商？","acceptedAnswer":{{"@type":"Answer","text":"{zh}獲 HKBN Enterprise、PCCW / HKT Commercial、HGC Business、中信國際電訊 CPC 等主要 ISP 覆蓋，支援企業光纖、MPLS、Cloud Connect、靜態 IP 及 SLA 保證。"}}}},'
        f'{{"@type":"Question","name":"{zh}裝商業寬頻要等幾耐？","acceptedAnswer":{{"@type":"Answer","text":"商業寬頻因需大廈管理處協調接線，一般需 5-10 個工作天（視乎 ISP 同樓層）。如單位曾接駁可縮短至 3-5 天。"}}}},'
        f'{{"@type":"Question","name":"{zh}辦公室商業寬頻月費大約幾多？","acceptedAnswer":{{"@type":"Answer","text":"基本商業 500M 約 $388-$588/月；1000M 企業光纖連 SLA + 靜態 IP 約 $888-$1,888/月；MPLS / 專線另報價。"}}}}'
        ']}'
    )
    s = re.sub(
        r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage"[^<]*</script>',
        f'<script type="application/ld+json">{faq_json}</script>',
        s, count=1
    )

    # 11. Breadcrumb HTML
    s = re.sub(
        r'<div class="breadcrumb">\s*<a href="/">主頁</a> › <a href="/pages/">屋苑寬頻</a> › <strong>[^<]*</strong>\s*</div>',
        f'<div class="breadcrumb">\n<a href="/">主頁</a> › <a href="/pages/">屋苑寬頻</a> › <strong>{zh} {en}</strong>\n</div>',
        s, count=1
    )

    # 12. Hero section
    hero_new = (
        '<section class="hero">\n'
        f'<h1>{zh} {en} 商業寬頻比較</h1>\n'
        f'<p class="sub">{hero_sub}</p>\n'
        '<div class="hero-stats">\n'
        f'<div><span class="num">{s1n}</span><span class="lbl">{s1l}</span></div>\n'
        f'<div><span class="num">{s2n}</span><span class="lbl">{s2l}</span></div>\n'
        f'<div><span class="num">{s3n}</span><span class="lbl">{s3l}</span></div>\n'
        f'<div><span class="num">{s4n}</span><span class="lbl">{s4l}</span></div>\n'
        '</div>\n'
        '</section>'
    )
    s = re.sub(
        r'<section class="hero">.*?</section>',
        lambda m: hero_new,
        s, count=1, flags=re.DOTALL
    )

    # 13. Info card (building data)
    info_new = (
        '<div class="card">\n'
        f'<h2>🏢 {zh} 大廈資料</h2>\n'
        '<table class="info-table">\n'
        f'<tr><td>中文名稱</td><td>{zh}</td></tr>\n'
        f'<tr><td>英文名稱</td><td>{en}</td></tr>\n'
        f'<tr><td>地址</td><td>{t["addr"]}</td></tr>\n'
        f'<tr><td>所在地區</td><td>{t["district"]}</td></tr>\n'
        f'<tr><td>大廈類別</td><td>{t["class"]}</td></tr>\n'
        f'<tr><td>落成年份</td><td>{t["completed"]}</td></tr>\n'
        f'<tr><td>總樓層</td><td>{t["floors"]}</td></tr>\n'
        f'<tr><td>建築高度</td><td>{t["height"]}</td></tr>\n'
        f'<tr><td>建築師</td><td>{t["architect"]}</td></tr>\n'
        f'<tr><td>發展商 / 業主</td><td>{t["developer"]}</td></tr>\n'
        f'<tr><td>業權結構</td><td>{t["ownership"]}</td></tr>\n'
        f'<tr><td>典型租戶</td><td>{t["tenants"]}</td></tr>\n'
        f'<tr><td>最近港鐵</td><td>{t["mtr"]}</td></tr>\n'
        f'<tr><td>寫字樓租金參考</td><td>{t["rent"]}</td></tr>\n'
        '<tr><td>寬頻基建</td><td>商業級光纖入樓（FTTB），支援企業專線、SLA、靜態 IP、MPLS</td></tr>\n'
        '<tr><td>裝機時間</td><td>商業寬頻一般 5-10 個工作天</td></tr>\n'
        '</table>\n'
        f'<p style="margin-top:14px;color:#556;font-size:.9em">{t["history"]}</p>\n'
        f'<p style="margin-top:10px;color:#556;font-size:.85em">📚 資料來源：<a href="{t["wiki"]}" target="_blank" rel="noopener">維基百科</a>、<a href="{t["src2_url"]}" target="_blank" rel="noopener">{t["src2_name"]}</a>。資料以各 ISP 官方確認為準。</p>\n'
        '</div>'
    )
    s = re.sub(
        r'<div class="card">\s*<h2>🏢[^<]*屋苑資料</h2>.*?</div>\s*(?=<div class="card">\s*<h2>📡)',
        info_new + '\n\n',
        s, count=1, flags=re.DOTALL
    )

    # 14. ISP card
    isp_new = (
        '<div class="card">\n'
        f'<h2>📡 {zh} 商業寬頻供應商</h2>\n'
        f'<p>作為 {t["district"].split("·")[-1].strip()} 甲廈，{zh} 獲多間主要 ISP 提供企業級寬頻：</p>\n'
        '<ul class="operators-list">\n'
        '<li>📶 <strong>HKBN Enterprise Solutions</strong><br><span style="font-size:.85em;color:#667">企業光纖 + Cloud Connect + SLA</span></li>\n'
        '<li>📶 <strong>PCCW / HKT Commercial</strong><br><span style="font-size:.85em;color:#667">核心網覆蓋，金融 / 專業服務專線</span></li>\n'
        '<li>📶 <strong>HGC 環球全域電訊 Business</strong><br><span style="font-size:.85em;color:#667">MPLS、跨境專線、數據中心互連</span></li>\n'
        '<li>📶 <strong>中信國際電訊 CPC</strong><br><span style="font-size:.85em;color:#667">TrueCONNECT MPLS + 靜態 IP</span></li>\n'
        '<li>📶 <strong>3HK Business / SmarTone Business</strong><br><span style="font-size:.85em;color:#667">企業光纖 + 5G 備援</span></li>\n'
        '</ul>\n'
        f'<p style="margin-top:12px;color:#667;font-size:.88em">⚠️ 由於 {zh} 各樓層 ISP 覆蓋或有差異，建議 WhatsApp 提供樓層 + 單位資料，我哋查實際覆蓋再報價。</p>\n'
        '</div>'
    )
    s = re.sub(
        r'<div class="card">\s*<h2>📡[^<]*寬頻供應商覆蓋</h2>.*?</div>\s*(?=<div class="card">\s*<h2>💰)',
        isp_new + '\n\n',
        s, count=1, flags=re.DOTALL
    )

    # 15. Plans - replace residential plans with commercial plans
    plans_new = (
        '<div class="card">\n'
        f'<h2>💰 {zh} 商業寬頻月費計劃</h2>\n'
        f'<p>BroadbandHK 為 {zh} 租戶提供企業光纖方案（月費僅供參考，以實際單位評估為準）：</p>\n'
        '<div class="plans-grid">\n'
        '            <div class="plan-card">\n'
        '                <div class="plan-name">500M 商業光纖</div>\n'
        '                <div class="plan-price">$388<span>/月起</span></div>\n'
        '                <p class="plan-target">中小企辦公室、基本商業應用</p>\n'
        '                <ul class="plan-features">\n'
        '                    <li>500Mbps 對等商業光纖</li>\n'
        '                    <li>商用級 Router</li>\n'
        '                    <li>基本 SLA 支援</li>\n'
        '                    <li>24 / 36 個月合約</li>\n'
        '                </ul>\n'
        f'                <a href="https://wa.me/85252287541?text=你好，我喺{zh}返工，想查詢 500M 商業寬頻" class="cta-btn whatsapp">WhatsApp 查詢</a>\n'
        '            </div>\n'
        '            <div class="plan-card popular">\n'
        '                <div class="plan-name">1000M 企業光纖 + SLA</div>\n'
        '                <div class="plan-price">$888<span>/月起</span></div>\n'
        '                <p class="plan-target">企業辦公、金融 / 專業服務、靜態 IP</p>\n'
        '                <ul class="plan-features">\n'
        '                    <li>1Gbps 對等企業光纖</li>\n'
        '                    <li>SLA 99.9% 可用性保證</li>\n'
        '                    <li>靜態 IP（1-5 個）</li>\n'
        '                    <li>24x7 企業客戶支援</li>\n'
        '                </ul>\n'
        f'                <a href="https://wa.me/85252287541?text=你好，我喺{zh}返工，想查詢 1000M 企業光纖 + SLA" class="cta-btn whatsapp">WhatsApp 查詢</a>\n'
        '            </div>\n'
        '            <div class="plan-card">\n'
        '                <div class="plan-name">MPLS / Cloud Connect 專線</div>\n'
        '                <div class="plan-price">報價<span>/月</span></div>\n'
        '                <p class="plan-target">跨境專線、多 Office 互連、Cloud 直連</p>\n'
        '                <ul class="plan-features">\n'
        '                    <li>MPLS VPN / SD-WAN</li>\n'
        '                    <li>AWS / Azure / GCP 直連</li>\n'
        '                    <li>SLA 99.99%</li>\n'
        '                    <li>靜態 IP Block / BGP</li>\n'
        '                </ul>\n'
        f'                <a href="https://wa.me/85252287541?text=你好，我喺{zh}返工，想查詢 MPLS 專線" class="cta-btn whatsapp">WhatsApp 查詢</a>\n'
        '            </div></div>\n'
        '<p style="text-align:center;margin-top:16px;color:#667;font-size:.88em">全部商業計劃：企業級 SLA 支援 · 靜態 IP 可加配 · 按需選 24 / 36 個月合約</p>\n'
        '</div>'
    )
    s = re.sub(
        r'<div class="card">\s*<h2>💰[^<]*寬頻月費計劃</h2>.*?</div>\s*(?=<div class="card">\s*<h2>❓)',
        plans_new + '\n\n',
        s, count=1, flags=re.DOTALL
    )

    # 16. FAQ HTML
    faq_html_new = (
        '<div class="card">\n'
        f'<h2>❓ {zh} 商業寬頻常見問題</h2>\n'
        f'<div class="faq-item"><h3>{zh}係住宅定商廈？</h3><p>{zh}（{en}）係 <strong>{t["class"]}</strong>，{t["completed"]}落成，{t["floors"]}，位於{t["addr"]}。租戶主要為：{t["tenants"]}。</p></div>\n'
        f'<div class="faq-item"><h3>{zh}點搭車去？</h3><p>最近港鐵：{t["mtr"]}。</p></div>\n'
        f'<div class="faq-item"><h3>{zh}有邊幾間商業寬頻供應商？</h3><p>{zh} 獲 HKBN Enterprise、PCCW / HKT Commercial、HGC Business、中信國際電訊 CPC、3HK Business 等主要 ISP 覆蓋，支援企業光纖、MPLS、Cloud Connect、靜態 IP 及 SLA 保證。</p></div>\n'
        f'<div class="faq-item"><h3>{zh}裝商業寬頻要等幾耐？</h3><p>商業寬頻因需大廈管理處協調接線，一般需 5-10 個工作天。如單位曾經接駁，重裝時間可縮短至 3-5 天。</p></div>\n'
        f'<div class="faq-item"><h3>{zh}辦公室商業寬頻月費大約幾多？</h3><p>基本商業 500M 約 $388-$588/月；1000M 企業光纖連 SLA + 靜態 IP 約 $888-$1,888/月；MPLS 專線 / Cloud Connect 另按方案報價。可 WhatsApp 5228 7541 提供樓層資料獲實際報價。</p></div>\n'
        '</div>'
    )
    s = re.sub(
        r'<div class="card">\s*<h2>❓[^<]*寬頻常見問題</h2>.*?</div>\s*(?=<div class="card">\s*<h2>📍)',
        faq_html_new + '\n\n',
        s, count=1, flags=re.DOTALL
    )

    # 17. Final CTA WhatsApp link context
    s = re.sub(
        r'你好，我住' + re.escape(zh) + r'，想查詢寬頻優惠',
        f'你好，我喺{zh}返工，想查詢商業寬頻優惠',
        s
    )
    s = re.sub(
        r'你好，我住[^，]*，想查詢寬頻優惠',
        f'你好，我喺{zh}返工，想查詢商業寬頻優惠',
        s
    )

    # 18. Final CTA heading
    s = re.sub(
        r'<h2>📞 即刻查 [^<]* 寬頻優惠</h2>',
        f'<h2>📞 即刻查 {zh} 商業寬頻優惠</h2>',
        s
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)
    return True


def main():
    results = []
    for t in TOWERS:
        try:
            enrich(t['file'], t)
            results.append((t['file'], 'OK'))
        except Exception as e:
            results.append((t['file'], f'ERR: {e}'))
    for r in results:
        print(r)

if __name__ == '__main__':
    main()
