# -*- coding: utf-8 -*-
"""Batch fix 13 luxury mid-levels/peak pages."""
import os, re, sys

ROOT = r"C:/Users/tonyng/Desktop/Claude_Code/BROADBANDHK/pages"

# Data dictionary: (filename, title, desc_content, keywords, sub_line, stats_4tuple, table_rows_list, intro_para, sources_html)
# stats_4tuple: [(num,lbl),(num,lbl),(num,lbl),(num,lbl)]
# table_rows_list: list of (label, value) -- will replace the whole tr block

DATA = [
    {
        "file": "twelve-peaks.html",
        "cn": "千溪", "en": "Twelve Peaks",
        "title_tail": "山頂加列山道 12幢獨立洋房 新世界發展 - BroadbandHK",
        "desc": "【2026最新】千溪 Twelve Peaks 寬頻方案比較：山頂加列山道12號，新世界發展，12幢獨立洋房每幢設私人升降機及泳池，實用約3,600-4,800呎。曾連續兩年稱冠亞洲十大超級豪宅。光纖入屋，支援 HKBN、HGC。100M $98 / 500M $158 / 1000M $228。WhatsApp 5228 7541。",
        "keywords": "千溪寬頻,Twelve Peaks broadband,加列山道寬頻,山頂洋房寬頻,新世界豪宅",
        "sub": "山頂 · 加列山道 12 號 · 12 幢獨立洋房 · 新世界發展",
        "stats": [("12","獨立洋房"),("3,600+","呎實用"),("$98","月費起"),("2-4天","上門安裝")],
        "rows": [
            ("中文名稱","千溪"),
            ("英文名稱","Twelve Peaks"),
            ("所在地區","山頂 · 加列山道 12 號"),
            ("最近交通","山頂纜車、15 號巴士"),
            ("項目組成","12 幢獨立洋房（每幢設私人升降機、泳池、花園、車位）"),
            ("實用面積","約 3,600 - 4,800 平方呎，房間數 3 - 6 間"),
            ("私家花園","約 1,802 - 4,478 平方呎"),
            ("發展商","新世界發展（New World Development）"),
            ("豪宅地位","2014、2015 連續兩年登「亞洲十大超級豪宅」榜首；首幢洋房曾以 8.19 億成交、呎價 18.8 萬破紀錄"),
            ("寬頻基建","光纖入屋 FTTH"),
            ("裝機時間","2-4 個工作天（洋房需預約）"),
        ],
        "intro": "千溪由新世界發展在山頂加列山道興建，2012 年落成。12 幢獨立洋房各擁私人升降機、泳池、花園，住戶為頂級富豪。項目連續兩年登亞洲十大超級豪宅榜首，為山頂核心豪宅代表作之一。",
        "sources": '<a href="https://richitt.com/twelve-peaks/" target="_blank" rel="noopener">覓至房</a>、<a href="https://hk.centanet.com/estate/en/Twelve-Peaks/2-SYBPWWPEWE" target="_blank" rel="noopener">中原地產</a>',
    },
    {
        "file": "bowen-place.html",
        "cn": "寶雲閣", "en": "Bowen Place",
        "title_tail": "中半山寶雲道 1座39伙 1989年 - BroadbandHK",
        "desc": "【2026最新】寶雲閣 Bowen Place 寬頻方案比較：中半山寶雲道 11A，1 座 39 伙，1989 年 2 月入伙，發展商 Vee Success Ltd.。實用 1,445-2,325 呎，設室外泳池及健身室。光纖入屋，支援 HKBN、HGC。100M $98 / 500M $158 / 1000M $228。WhatsApp 5228 7541。",
        "keywords": "寶雲閣寬頻,Bowen Place broadband,寶雲道寬頻,中半山豪宅寬頻",
        "sub": "中半山 · 寶雲道 11A · 1座 · 39伙 · 1989 年落成",
        "stats": [("1","座數"),("39","總單位"),("1989","落成年份"),("$98","月費起")],
        "rows": [
            ("中文名稱","寶雲閣"),
            ("英文名稱","Bowen Place"),
            ("所在地區","中半山 · 寶雲道 11A"),
            ("最近港鐵","金鐘站（港島綫、荃灣綫）"),
            ("落成年份","1989 年 2 月"),
            ("座數 / 單位","1 座 · 39 伙"),
            ("實用面積","1,445 - 2,325 平方呎"),
            ("發展商","Vee Success Ltd."),
            ("會所設施","健身室、室外游泳池"),
            ("校網","小學 11 校網，中學中西區校網"),
            ("寬頻基建","光纖入屋 FTTH"),
            ("裝機時間","1-3 個工作天"),
        ],
        "intro": "寶雲閣位於中半山寶雲道 11A，單幢 39 伙，1989 年落成，毗鄰多國領事館及加拿大國際學校、香港猶太國際學校，屬傳統中半山豪宅區。",
        "sources": '<a href="https://www.oneday.com.hk/en_US/buildings/bowen-place/" target="_blank" rel="noopener">OneDay 搵地</a>、<a href="https://www.28hse.com/en/estate/detail/bowen-place-813" target="_blank" rel="noopener">28Hse</a>',
    },
    {
        "file": "tregunter.html",
        "cn": "地利根德閣", "en": "Tregunter",
        "title_tail": "中半山地利根德里14號 3座317伙 - BroadbandHK",
        "desc": "【2026最新】地利根德閣 Tregunter 寬頻方案比較：中半山地利根德里14號，3座合共317伙。1、2座1981年落成，3座1993年落成高達66層。實用1,547-6,507呎。支援 HKBN、HGC。100M $98 / 500M $158 / 1000M $228。WhatsApp 5228 7541。",
        "keywords": "地利根德閣寬頻,Tregunter broadband,地利根德里寬頻,中半山豪宅,HKBN Tregunter",
        "sub": "中半山 · 地利根德里 14 號 · 3座 · 317伙 · 1981/1993 落成",
        "stats": [("3","座數"),("317","總單位"),("66","最高層數"),("$98","月費起")],
        "rows": [
            ("中文名稱","地利根德閣"),
            ("英文名稱","Tregunter"),
            ("所在地區","中半山 · 地利根德里 14 號"),
            ("最近港鐵","中環站、金鐘站（港島綫、荃灣綫）"),
            ("落成年份","第 1、2 座 1981 年；第 3 座 1993 年"),
            ("座數 / 單位","3 座 · 317 伙（第1座33層、第2座32層、每層2伙共130伙；第3座66層、每層4伙共187伙）"),
            ("實用面積","1,547 - 6,507 平方呎"),
            ("豪宅地位","中半山地標之一，住戶多為跨國企業高層及名流"),
            ("寬頻基建","光纖入屋 FTTH"),
            ("裝機時間","1-3 個工作天"),
        ],
        "intro": "地利根德閣位於中半山地利根德里，由 3 座高層住宅組成共 317 伙，其中第 3 座高達 66 層，曾為香港最高住宅樓宇之一。坐擁維港及山景，為中半山傳統豪宅屋苑代表。",
        "sources": '<a href="https://zh-yue.wikipedia.org/wiki/%E5%9C%B0%E5%88%A9%E6%A0%B9%E5%BE%B7%E9%96%A3" target="_blank" rel="noopener">維基百科</a>、<a href="https://hk.centanet.com/estate/en/Tregunter/2-TZHNZHLAHM" target="_blank" rel="noopener">中原地產</a>',
    },
    {
        "file": "clovelly-court.html",
        "cn": "嘉富麗苑", "en": "Clovelly Court",
        "title_tail": "中半山梅道12號 2座240伙 新世界 - BroadbandHK",
        "desc": "【2026最新】嘉富麗苑 Clovelly Court 寬頻方案比較：中半山梅道 12 號，2 座 240 伙，1994 年入伙，新世界發展。實用 1,562-2,348 呎，每層3伙。會所設網球場、泳池、健身室。光纖入屋，支援 HKBN、HGC。100M $98 / 500M $158 / 1000M $228。WhatsApp 5228 7541。",
        "keywords": "嘉富麗苑寬頻,Clovelly Court broadband,梅道寬頻,中半山豪宅,新世界",
        "sub": "中半山 · 梅道 12 號 · 2座 · 240伙 · 1994 年 · 新世界發展",
        "stats": [("2","座數"),("240","總單位"),("1994","入伙年份"),("$98","月費起")],
        "rows": [
            ("中文名稱","嘉富麗苑"),
            ("英文名稱","Clovelly Court"),
            ("所在地區","中半山 · 梅道 12 號"),
            ("最近港鐵","中環站、金鐘站（港島綫、荃灣綫）"),
            ("落成年份","1994 年 3 月"),
            ("座數 / 單位","2 座 · 240 伙（每層 3 伙）"),
            ("實用面積","1,562 - 2,348 平方呎"),
            ("間格","3 房為主；6 樓以上設大型橢圓形陽台"),
            ("發展商","新世界發展（New World Development）"),
            ("會所設施","網球場、游泳池、健身室"),
            ("校網","小學 11 校網，中學中西區校網"),
            ("寬頻基建","光纖入屋 FTTH"),
            ("裝機時間","1-3 個工作天"),
        ],
        "intro": "嘉富麗苑位於中半山梅道 12 號，由新世界發展興建，1994 年入伙。2 座共 240 伙，每層 3 伙，高層戶配大型橢圓形陽台，景觀開揚。屬 11 校網，為中半山老牌大型豪宅屋苑。",
        "sources": '<a href="https://www.oneday.com.hk/en_US/buildings/clovelly-court/" target="_blank" rel="noopener">OneDay 搵地</a>、<a href="https://hk.centanet.com/estate/en/Clovelly-Court/2-TZHNTHDXHM" target="_blank" rel="noopener">中原地產</a>',
    },
    {
        "file": "century-tower-i.html",
        "cn": "世紀大廈", "en": "Century Tower",
        "title_tail": "中半山地利根德里1A 2座82伙 - BroadbandHK",
        "desc": "【2026最新】世紀大廈 Century Tower 寬頻方案比較：中半山地利根德里 1A，2 座 82 伙。第1座1971年、圓筒型35層、每層2伙；第2座1992年、22層每層1伙。發展商置地/嘉里。實用 1,129-4,172 呎。光纖入屋。100M $98 / 500M $158 / 1000M $228。WhatsApp 5228 7541。",
        "keywords": "世紀大廈寬頻,Century Tower broadband,地利根德里,中半山豪宅",
        "sub": "中半山 · 地利根德里 1A · 2座 · 82伙 · 1971/1992 落成 · 置地/嘉里",
        "stats": [("2","座數"),("82","總單位"),("1971","第一座落成"),("$98","月費起")],
        "rows": [
            ("中文名稱","世紀大廈"),
            ("英文名稱","Century Tower"),
            ("所在地區","中半山 · 地利根德里 1A"),
            ("最近港鐵","中環站、金鐘站（港島綫、荃灣綫）"),
            ("座數 / 單位","2 座 · 82 伙"),
            ("第 1 座","1971 年落成，35 層圓筒型設計，每層 2 伙共 60 伙"),
            ("第 2 座","1992 年落成，22 層，每層 1 伙共 22 伙（4 房 3 套間隔）"),
            ("實用面積","1,129 - 4,172 平方呎"),
            ("發展商","第 1 座：香港置地；第 2 座：嘉里建設"),
            ("寬頻基建","光纖入屋 FTTH"),
            ("裝機時間","1-3 個工作天"),
        ],
        "intro": "世紀大廈由兩座性質迥異的住宅組成：第 1 座為 1971 年香港置地興建之圓筒型地標；第 2 座為 1992 年嘉里建設發展、每層 1 伙之豪宅，單位面積達 4,172 呎。兩座同處中半山地利根德里 1A，為中半山老牌豪宅。",
        "sources": '<a href="https://zh.wikipedia.org/zh-hk/%E4%B8%96%E7%B4%80%E5%A4%A7%E5%BB%88" target="_blank" rel="noopener">維基百科</a>、<a href="https://hk.centanet.com/estate/en/Century-Tower/2-SKPBGPWXPA" target="_blank" rel="noopener">中原地產</a>',
    },
    {
        "file": "po-shan-mansions.html",
        "cn": "寶城大廈", "en": "Po Shan Mansions",
        "title_tail": "西半山寶珊道14-16號 2座77伙 - BroadbandHK",
        "desc": "【2026最新】寶城大廈 Po Shan Mansions 寬頻方案比較：西半山寶珊道 14-16 號，2 座 77 伙，1965 年 12 月入伙。4 房大單位為主，實用 2,410-4,820 呎。光纖入屋，支援 HKBN、HGC。100M $98 / 500M $158 / 1000M $228。WhatsApp 5228 7541 免費格價。",
        "keywords": "寶城大廈寬頻,Po Shan Mansions broadband,寶珊道寬頻,西半山豪宅",
        "sub": "西半山 · 寶珊道 14-16 號 · 2座 · 77伙 · 1965 年落成",
        "stats": [("2","座數"),("77","總單位"),("1965","入伙年份"),("$98","月費起")],
        "rows": [
            ("中文名稱","寶城大廈"),
            ("英文名稱","Po Shan Mansions"),
            ("所在地區","西半山 · 寶珊道 14-16 號"),
            ("最近港鐵","香港大學站（港島綫）"),
            ("落成年份","1965 年 12 月"),
            ("座數 / 單位","2 座 · 77 伙"),
            ("實用面積","2,410 - 4,820 平方呎"),
            ("間格","4 房大單位為主"),
            ("校網","小學 11 校網，中學中西區"),
            ("寬頻基建","光纖入屋 FTTH"),
            ("裝機時間","1-3 個工作天"),
        ],
        "intro": "寶城大廈位於西半山寶珊道 14-16 號，1965 年入伙，2 座合共 77 伙，全屬 4 房大宅格局，實用最高 4,820 呎，為西半山傳統低密度豪宅之一。",
        "sources": '<a href="https://www.oneday.com.hk/en_US/buildings/po-shan-mansions/" target="_blank" rel="noopener">OneDay 搵地</a>、<a href="https://hk.centanet.com/estate/en/Po-Shan-Mansions" target="_blank" rel="noopener">中原地產</a>',
    },
    {
        "file": "magazine-gap-tower.html",
        "cn": "馬己仙峽大廈", "en": "Magazine Gap Towers",
        "title_tail": "中半山馬己仙峽道15號 24伙 1967 - BroadbandHK",
        "desc": "【2026最新】馬己仙峽大廈 Magazine Gap Towers 寬頻方案比較：中半山馬己仙峽道 15 號，1 座 12 層 24 伙，每層 2 伙，1967 年落成。屬馬己仙峽道傳統名人豪宅地段。光纖入屋。100M $98 / 500M $158 / 1000M $228。WhatsApp 5228 7541。",
        "keywords": "馬己仙峽大廈寬頻,Magazine Gap Towers broadband,馬己仙峽道寬頻,中半山豪宅",
        "sub": "中半山 · 馬己仙峽道 15 號 · 1座 · 24伙 · 1967 年",
        "stats": [("1","座數"),("24","總單位"),("1967","落成年份"),("$98","月費起")],
        "rows": [
            ("中文名稱","馬己仙峽大廈"),
            ("英文名稱","Magazine Gap Towers"),
            ("所在地區","中半山 · 馬己仙峽道 15 號"),
            ("最近港鐵","金鐘站（港島綫、荃灣綫）"),
            ("落成年份","1967 年"),
            ("座數 / 單位","1 座 · 12 層 · 每層 2 伙 · 共 24 伙"),
            ("地段特色","馬己仙峽道一帶為傳統名人豪宅地段"),
            ("寬頻基建","光纖入屋 FTTH"),
            ("裝機時間","1-3 個工作天"),
        ],
        "intro": "馬己仙峽大廈位於中半山馬己仙峽道 15 號，1967 年落成，樓高 12 層每層 2 伙，共 24 伙，低密度佈局令私隱度極高。馬己仙峽道自開埠至今為名人豪宅雲集之地。",
        "sources": '<a href="https://zh.wikipedia.org/zh-hk/%E9%A6%AC%E5%B7%B1%E4%BB%99%E5%B3%BD%E9%81%93" target="_blank" rel="noopener">維基百科</a>、<a href="https://hk.centanet.com/estate/en/Magazine-Gap-Towers/1-TSSHTHDXHM" target="_blank" rel="noopener">中原地產</a>',
    },
    {
        "file": "severn-8.html",
        "cn": "倚巒", "en": "Severn 8",
        "title_tail": "山頂施勳道 22幢洋房 新鴻基2005 - BroadbandHK",
        "desc": "【2026最新】倚巒 Severn 8 寬頻方案比較：山頂施勳道，新鴻基地產發展，2005年落成，22幢洋房分3期、實用 2,363-3,752 呎、3-4 房。2008 曾以 2.84 億、呎價 5.6 萬破亞洲洋房紀錄。光纖入屋。100M $98 / 500M $158 / 1000M $228。WhatsApp 5228 7541。",
        "keywords": "倚巒寬頻,Severn 8 broadband,施勳道寬頻,山頂洋房,新鴻基豪宅",
        "sub": "山頂 · 施勳道 · 22 幢洋房（3 期）· 新鴻基 · 2005 年",
        "stats": [("22","總洋房"),("3","期數"),("2005","落成年份"),("$98","月費起")],
        "rows": [
            ("中文名稱","倚巒"),
            ("英文名稱","Severn 8"),
            ("所在地區","山頂 · 施勳道"),
            ("最近交通","山頂纜車、15 號巴士"),
            ("落成年份","2005 年"),
            ("項目組成","22 幢獨立洋房（分 3 期）"),
            ("實用面積","2,363 - 3,752 平方呎（3-4 房）"),
            ("海拔","約 400 米，坐擁維港無敵景"),
            ("發展商","新鴻基地產（Sun Hung Kai Properties）"),
            ("豪宅紀錄","2008 年 1 幢洋房以 2.84 億、呎價約 5.6 萬成交，曾創亞洲洋房呎價紀錄"),
            ("寬頻基建","光纖入屋 FTTH"),
            ("裝機時間","2-4 個工作天（洋房需預約）"),
        ],
        "intro": "倚巒由新鴻基地產於 2000 年以 4.9 億投得地皮，2005 年落成。22 幢獨立洋房坐落山頂施勳道海拔 400 米，施勳道自開埠以來為山頂名人豪宅雲集之地。項目屢創香港及亞洲豪宅呎價新高。",
        "sources": '<a href="https://zh.wikipedia.org/zh-hk/%E5%80%9A%E5%B7%92" target="_blank" rel="noopener">維基百科</a>、<a href="https://hk.centanet.com/estate/en/Severn-8/2-SYPPWPPEPE" target="_blank" rel="noopener">中原地產</a>',
    },
    {
        "file": "grenville-house.html",
        "cn": "嘉慧園", "en": "Grenville House",
        "title_tail": "中半山馬己仙峽道3號 5座120伙 - BroadbandHK",
        "desc": "【2026最新】嘉慧園 Grenville House 寬頻方案比較：中半山馬己仙峽道 3 號，5 座弧形排列共 120 伙，1971 年落成。每座 12 層、每層 2 伙，實用 3,073-3,366 呎。光纖入屋，支援 HKBN、HGC。100M $98 / 500M $158 / 1000M $228。WhatsApp 5228 7541。",
        "keywords": "嘉慧園寬頻,Grenville House broadband,馬己仙峽道,中半山豪宅",
        "sub": "中半山 · 馬己仙峽道 3 號 · 5座 · 120伙 · 1971 年",
        "stats": [("5","座數"),("120","總單位"),("1971","落成年份"),("$98","月費起")],
        "rows": [
            ("中文名稱","嘉慧園"),
            ("英文名稱","Grenville House"),
            ("所在地區","中半山 · 馬己仙峽道 3 號"),
            ("最近港鐵","金鐘站（港島綫、荃灣綫）"),
            ("落成年份","1971 年"),
            ("座數 / 單位","5 座 · 12 層 · 每層 2 伙 · 共 120 伙（弧形排列）"),
            ("實用面積","3,073 - 3,366 平方呎"),
            ("單位特色","樓底高，大窗，景觀開揚"),
            ("寬頻基建","光纖入屋 FTTH"),
            ("裝機時間","1-3 個工作天"),
        ],
        "intro": "嘉慧園位於中半山馬己仙峽道 3 號，1971 年落成，5 座弧形排列共 120 伙。每伙實用逾 3,000 呎，樓底高、大窗大廳，屬中半山老牌大宅。馬己仙峽道為傳統名人豪宅地段。",
        "sources": '<a href="https://www.oneday.com.hk/en_US/buildings/grenville-house/" target="_blank" rel="noopener">OneDay 搵地</a>、<a href="https://hk.centanet.com/estate/en/Grenville-House/2-OSUUURCXRQ" target="_blank" rel="noopener">中原地產</a>',
    },
    {
        "file": "parkview-court.html",
        "cn": "恆柏園", "en": "Park View Court",
        "title_tail": "西半山列堤頓道1號 2座136伙 - BroadbandHK",
        "desc": "【2026最新】恆柏園 Park View Court 寬頻方案比較：西半山列堤頓道 1 號，2 座 136 伙。實用 1,266-2,680 呎，屬西半山傳統豪宅屋苑。光纖入屋，支援 HKBN、HGC。100M $98 / 500M $158 / 1000M $228。WhatsApp 5228 7541 免費格價。",
        "keywords": "恆柏園寬頻,Park View Court broadband,列堤頓道寬頻,西半山豪宅",
        "sub": "西半山 · 列堤頓道 1 號 · 2座 · 136伙",
        "stats": [("2","座數"),("136","總單位"),("2,680","最大實用呎"),("$98","月費起")],
        "rows": [
            ("中文名稱","恆柏園"),
            ("英文名稱","Park View Court"),
            ("所在地區","西半山 · 列堤頓道 1 號"),
            ("最近港鐵","香港大學站（港島綫）"),
            ("座數 / 單位","2 座 · 136 伙"),
            ("實用面積","1,266 - 2,680 平方呎"),
            ("校網","小學 11 校網"),
            ("寬頻基建","光纖入屋 FTTH"),
            ("裝機時間","1-3 個工作天"),
        ],
        "intro": "恆柏園位於西半山列堤頓道 1 號，2 座共 136 伙，實用最大達 2,680 呎。鄰近香港大學及羅便臣道一帶，為西半山傳統中大型豪宅屋苑。",
        "sources": '<a href="https://www.oneday.com.hk/en_US/buildings/park-view-court/" target="_blank" rel="noopener">OneDay 搵地</a>、<a href="https://www.28hse.com/en/estate/detail/park-view-court-442" target="_blank" rel="noopener">28Hse</a>',
    },
    {
        "file": "tavistock-(tower-t3).html",
        "cn": "騰皇居", "en": "Tavistock",
        "title_tail": "中半山地利根德里10號 1座98伙 信和 - BroadbandHK",
        "desc": "【2026最新】騰皇居 Tavistock 寬頻方案比較：中半山地利根德里 10 號，信和置業發展，1999 年入伙，1 座 98 伙，實用 1,221-5,254 呎。會所設施齊備。光纖入屋，支援 HKBN、HGC。100M $98 / 500M $158 / 1000M $228。WhatsApp 5228 7541。",
        "keywords": "騰皇居寬頻,Tavistock broadband,地利根德里,中半山豪宅,信和",
        "sub": "中半山 · 地利根德里 10 號 · 1座 · 98伙 · 1999 年 · 信和置業",
        "stats": [("1","座數"),("98","總單位"),("1999","入伙年份"),("$98","月費起")],
        "rows": [
            ("中文名稱","騰皇居"),
            ("英文名稱","Tavistock"),
            ("所在地區","中半山 · 地利根德里 10 號"),
            ("最近港鐵","中環站、金鐘站（港島綫、荃灣綫）"),
            ("落成年份","1999 年 5 月"),
            ("座數 / 單位","1 座 · 98 伙"),
            ("實用面積","1,221 - 5,254 平方呎"),
            ("發展商","信和置業（Sino Land）"),
            ("會所設施","泳池、健身室、兒童及體育設施、餐飲"),
            ("入場門檻","近年呎價約 4 萬起、入場約 6,000 萬"),
            ("寬頻基建","光纖入屋 FTTH"),
            ("裝機時間","1-3 個工作天"),
        ],
        "intro": "騰皇居由信和置業發展，1999 年落成，位於中半山地利根德里 10 號。單幢 98 伙，實用最大 5,254 呎，會所設施齊全，屬中半山一線豪宅。",
        "sources": '<a href="https://www.squarefoot.com.hk/estate/detail/tavistock-785" target="_blank" rel="noopener">Squarefoot</a>、<a href="https://www.oneday.com.hk/en_US/buildings/tavistock/" target="_blank" rel="noopener">OneDay 搵地</a>',
    },
    {
        "file": "strawberry-hill.html",
        "cn": "紅梅閣", "en": "Strawberry Hill",
        "title_tail": "山頂 48幢洋房 1976 - BroadbandHK",
        "desc": "【2026最新】紅梅閣 Strawberry Hill 寬頻方案比較：山頂區分 2 期共 48 幢洋房，1976 年落成，3-4 房連壁爐獨立廳，多數單位附花園或庭院，鄰近山頂學校。光纖入屋。100M $98 / 500M $158 / 1000M $228。WhatsApp 5228 7541。",
        "keywords": "紅梅閣寬頻,Strawberry Hill broadband,山頂洋房寬頻,山頂豪宅",
        "sub": "山頂 · 2 期 · 48 幢洋房 · 1976 年落成",
        "stats": [("2","期數"),("48","總洋房"),("1976","落成年份"),("$98","月費起")],
        "rows": [
            ("中文名稱","紅梅閣"),
            ("英文名稱","Strawberry Hill"),
            ("所在地區","山頂區"),
            ("最近交通","山頂纜車、15 號巴士"),
            ("落成年份","1976 年（分 2 期）"),
            ("項目組成","48 幢獨立洋房"),
            ("間格","3 - 4 房，獨立廳、飯廳，設壁爐"),
            ("單位特色","多數附花園或庭院"),
            ("鄰近設施","山頂學校、山頂廣場超級市場"),
            ("寬頻基建","光纖入屋 FTTH"),
            ("裝機時間","2-4 個工作天（洋房需預約）"),
        ],
        "intro": "紅梅閣位於山頂區，分 2 期共 48 幢洋房，1976 年落成，屬山頂傳統洋房屋苑。單位設獨立廳、飯廳及壁爐，大多配有花園或庭院，鄰近山頂學校，配套完善。",
        "sources": '<a href="https://www.oneday.com.hk/en_US/buildings/strawberry-hill/" target="_blank" rel="noopener">OneDay 搵地</a>、<a href="https://www.midland.com.hk/en/estate/Hong-Kong-Island-%E5%B1%B1%E9%A0%82-Strawberry-Hill-E000000215" target="_blank" rel="noopener">美聯物業</a>',
    },
    {
        "file": "1-plantation-road.html",
        "cn": "種植道1號", "en": "1 Plantation Road",
        "title_tail": "山頂 20幢洋房 九廣鐵路/會德豐 - BroadbandHK",
        "desc": "【2026最新】種植道1號 1 Plantation Road 寬頻方案比較：山頂低密度 20 幢獨立洋房，實用 4,600-7,500 呎，連私人升降機及車庫。九廣鐵路持有、會德豐負責發展銷售，PEAK COLLECTION 系列。光纖入屋。100M $98 / 500M $158 / 1000M $228。WhatsApp 5228 7541。",
        "keywords": "種植道1號寬頻,1 Plantation Road broadband,山頂洋房寬頻,會德豐豪宅",
        "sub": "山頂 · 種植道 1 號 · 20 幢獨立洋房 · 九廣鐵路/會德豐",
        "stats": [("20","總洋房"),("4,600+","呎實用"),("3","期數"),("$98","月費起")],
        "rows": [
            ("中文名稱","種植道 1 號"),
            ("英文名稱","1 Plantation Road"),
            ("所在地區","山頂 · 種植道 1 號"),
            ("最近交通","山頂纜車、15 號巴士"),
            ("項目組成","20 幢獨立洋房（分 3 期）"),
            ("實用面積","約 4,600 - 7,500 平方呎"),
            ("單位特色","每幢設私人升降機及車庫"),
            ("持有 / 發展","九廣鐵路公司（KCRC, 0004.HK）持有，會德豐地產發展及銷售"),
            ("銷售策略","1、2、3、5、6 號 5 幢招標出售（5,600-6,200 呎），其餘 15 幢長線出租"),
            ("系列","PEAK COLLECTION"),
            ("寬頻基建","光纖入屋 FTTH"),
            ("裝機時間","2-4 個工作天（洋房需預約）"),
        ],
        "intro": "種植道 1 號為山頂低密度超級豪宅項目，由九廣鐵路持有，會德豐地產發展及銷售，20 幢獨立洋房每幢設私人升降機及車庫，實用 4,600-7,500 呎。屬 PEAK COLLECTION 系列，首期首幢洋房曾以 5.58 億成交。",
        "sources": '<a href="https://www.okay.com/en/building/1-plantation-road/2398" target="_blank" rel="noopener">OKAY.com</a>、<a href="https://www.oneday.com.hk/en_US/buildings/1-plantation-road/" target="_blank" rel="noopener">OneDay 搵地</a>',
    },
]


def build_table_rows(rows):
    return "\n".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows)


def patch(entry):
    path = os.path.join(ROOT, entry["file"])
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    cn = entry["cn"]; en = entry["en"]
    # 1) robots noindex -> index
    html = html.replace('<meta name="robots" content="noindex, follow">',
                        '<meta name="robots" content="index, follow">')

    # 2) Replace <title>
    html = re.sub(r"<title>.*?</title>",
                  f"<title>{cn} {en} 寬頻月費比較｜{entry['title_tail']}</title>",
                  html, count=1, flags=re.S)

    # 3) Replace meta description
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{entry["desc"]}">',
                  html, count=1)

    # 4) Replace meta keywords
    html = re.sub(r'<meta name="keywords" content="[^"]*">',
                  f'<meta name="keywords" content="{entry["keywords"]}">',
                  html, count=1)

    # 5) Replace hero section (sub line + stats)
    s = entry["stats"]
    new_stats = (
        f'<div class="hero-stats">\n'
        f'<div><span class="num">{s[0][0]}</span><span class="lbl">{s[0][1]}</span></div>\n'
        f'<div><span class="num">{s[1][0]}</span><span class="lbl">{s[1][1]}</span></div>\n'
        f'<div><span class="num">{s[2][0]}</span><span class="lbl">{s[2][1]}</span></div>\n'
        f'<div><span class="num">{s[3][0]}</span><span class="lbl">{s[3][1]}</span></div>\n'
        f'</div>'
    )
    html = re.sub(
        r'<section class="hero">\s*<h1>.*?</h1>\s*<p class="sub">.*?</p>\s*<div class="hero-stats">.*?</div>\s*</section>',
        f'<section class="hero">\n<h1>{cn} {en} 寬頻月費比較</h1>\n<p class="sub">{entry["sub"]}</p>\n{new_stats}\n</section>',
        html, count=1, flags=re.S
    )

    # 6) Replace info table (the first table.info-table and the following <p> intro + add sources)
    new_table = build_table_rows(entry["rows"])
    sources_html = f'<p style="margin-top:10px;color:#556;font-size:.85em">📚 資料來源：{entry["sources"]}。</p>'
    new_intro = f'<p style="margin-top:14px;color:#556;font-size:.95em">{entry["intro"]}</p>\n{sources_html}'
    html = re.sub(
        r'<table class="info-table">.*?</table>\s*<p style="margin-top:14px[^>]*>.*?</p>',
        f'<table class="info-table">\n{new_table}\n</table>\n{new_intro}',
        html, count=1, flags=re.S
    )

    # 7) Remove bogus '1000M 實測速度' FAQ answer -> replace with theoretical
    html = re.sub(
        r'<div class="faq-item"><h3>[^<]*?嘅 1000M 寬頻實際速度有幾快？</h3><p>根據用戶實測[^<]*?</p></div>',
        f'<div class="faq-item"><h3>{cn} 1000M 寬頻理論速度？</h3><p>1000M 光纖理論下載速度為 1 Gbps (1000 Mbps)。實際速度受路由器效能、線材、Wi-Fi 訊號、連線裝置數目影響，建議搭配 Wi-Fi 6/6E 路由器並以網線直駁電腦量測最高速度。</p></div>',
        html, count=1
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK {entry['file']}")


for e in DATA:
    try:
        patch(e)
    except Exception as ex:
        print(f"ERR {e['file']}: {ex}")
