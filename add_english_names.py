"""
Add English hotel names to the Trip.com directory table in HKhotel-en.html
Uses known chain name mappings + common translation patterns
"""
import re

# Known hotel chain Chinese → English mappings
CHAIN_MAP = {
    "香港喜來登飯店": "Sheraton Hong Kong Hotel & Towers",
    "荃灣西如心飯店": "Nina Hotel Tsuen Wan West",
    "香港皇悅卓越飯店（銅鑼灣店）": "Empire Prestige Causeway Bay",
    "香港灣仔帝盛飯店": "Dorsett Wanchai Hong Kong",
    "香港灣仔皇悅飯店": "Empire Hotel Hong Kong - Wan Chai",
    "香港楓葉旅館（尖沙咀地鐵站店近C2口）": "Maple Leaf Hotel (TST MTR C2 Exit)",
    "香港港島海逸君綽飯店": "Harbour Grand Hong Kong",
    "合和飯店": "Hopewell Hotel",
    "香港悅來飯店": "Panda Hotel",
    "香港荃灣帝盛飯店": "Dorsett Tsuen Wan",
    "香港君悅飯店": "Grand Hyatt Hong Kong",
    "香港百利飯店": "Park Hotel Hong Kong",
    "雅高宜必思香港中上環飯店": "ibis Hong Kong Central & Sheung Wan",
    "星寓": "Star Studios",
    "香港東湧福朋喜來登飯店": "Four Points by Sheraton Tung Chung",
    "香港銅鑼灣智選假日飯店": "Holiday Inn Express Causeway Bay",
    "香港逸東飯店（朗廷飯店集團旗下）": "Eaton HK (Langham Group)",
    "香港恆豐飯店": "Prudential Hotel",
    "香港灣仔睿景飯店": "Hotel Ease Wan Chai",
    "千禧新世界香港飯店": "New World Millennium Hong Kong Hotel",
    "聚居": "Juji Hotel",
    "香港金域假日飯店": "Holiday Inn Golden Mile",
    "香港北角海逸飯店": "Harbour Plaza North Point",
    "香港康得思飯店（朗廷飯店集團旗下）": "Cordis Hong Kong (Langham Group)",
    "麗豪航天城飯店（富豪飯店集團旗下）": "Regala Skycity Hotel (Regal Hotels)",
    "香港皇悅卓越飯店（尖沙咀店）": "Empire Prestige Tsim Sha Tsui",
    "香港頤庭飯店（銅鑼灣店）": "Eco Tree Hotel Causeway Bay",
    "富豪香港飯店": "Regal Hongkong Hotel",
    "香港百樂飯店": "Park Lane Hong Kong",
    "旭逸雅捷飯店·荃灣": "Hotel Ease Access Tsuen Wan",
    "如心銅鑼灣海景飯店": "L'hotel Causeway Bay Harbour View",
    "香港珀麗飯店": "Rosedale Hotel Hong Kong",
    "尖沙咀帝苑飯店": "The Royal Garden Hong Kong",
    "香港海景嘉福洲際飯店": "InterContinental Grand Stanford Hong Kong",
    "香港柏寧鉑爾曼飯店": "The Park Lane Hong Kong, a Pullman Hotel",
    "香港沙田凱悅飯店": "Hyatt Regency Hong Kong Sha Tin",
    "香港帝京飯店": "Royal Plaza Hotel",
    "紅茶館飯店（大角咀店）": "Bridal Tea House Tai Kok Tsui",
    "香港九龍諾富特飯店": "Novotel Hong Kong Nathan Road Kowloon",
    "香港城景國際": "The Cityview",
    "紅茶館飯店（佐敦店）": "Bridal Tea House Jordan",
    "紅茶館飯店（紅磡機利士南路店）": "Bridal Tea House Hung Hom",
    "香港尖沙咀凱悅飯店": "Hyatt Regency Tsim Sha Tsui",
    "香港美利酒店": "The Murray Hong Kong",
    "如心艾朗飯店": "L'hotel elan",
    "香港朗廷飯店": "The Langham Hong Kong",
    "香港彌敦飯店": "Nathan Hotel",
    "香港天一飯店喜利店（尖沙咀地鐵站店近C2口）": "Day One Hotel Tsim Sha Tsui",
    "香港盛庭LIVING飯店公寓（近何文田站B1口）": "iclub LIVING Ho Man Tin",
    "香港東隅": "East Hong Kong",
    "東南樓藝術飯店": "Tung Nam Lou Art Hotel",
    "香港基督教青年會（港青）": "YMCA of Hong Kong",
    "粵海181飯店": "Guangdong Hotel 181",
    "香港TUVE飯店": "TUVE Hotel",
    "香港富薈旺角飯店": "iclub Mong Kok Hotel",
    "Page148, 晉致飯店": "Page148, Hotel & Co",
    "香港君立飯店": "Kimberley Hotel",
    "香港太子飯店-馬哥孛羅": "Prince Hotel Marco Polo",
    "海星旅館": "Starfish Hostel",
    "香港東湧世茂喜來登飯店": "Sheraton Tung Chung",
    "香港六國飯店": "Gloucester Luk Kwok Hong Kong",
    "香港普特曼飯店": "Putman Hotel Hong Kong",
    "迪士尼好萊塢飯店": "Disney's Hollywood Hotel",
    "香港港麗飯店": "Conrad Hong Kong",
    "香港半島酒店": "The Peninsula Hong Kong",
    "香港文華東方酒店": "Mandarin Oriental Hong Kong",
    "香港麗思卡爾頓酒店": "The Ritz-Carlton Hong Kong",
    "香港W酒店": "W Hong Kong",
    "香港四季酒店": "Four Seasons Hotel Hong Kong",
    "香港瑰麗酒店": "Rosewood Hong Kong",
    "香港嘉里酒店": "Kerry Hotel Hong Kong",
    "唯港薈": "Hotel ICON",
    "香港銅鑼灣皇悅飯店": "Empire Hotel Causeway Bay",
    "灣景國際-香港中華基督教青年會": "The Harbourview - YMCA",
    "灣景國際": "The Harbourview",
    "旺角帝盛飯店": "Dorsett Mongkok",
    "香港數碼港艾美飯店": "Le Meridien Cyberport",
    "香港洲際飯店": "InterContinental Hong Kong",
    "香港愉景灣酒店": "Auberge Discovery Bay",
    "迪士尼探索家度假飯店": "Disney Explorers Lodge",
    "香港迪士尼樂園飯店": "Hong Kong Disneyland Hotel",
    "香港富豪機場飯店": "Regal Airport Hotel",
    "南灣如心飯店": "L'hotel Island South",
    "香港夢卓恩飯店（雅高集團旗下）": "MGallery The Silveri (Accor)",
    "香港維港凱悅尚萃飯店": "Hyatt Centric Victoria Harbour",
    "香港觀塘帝盛飯店": "Dorsett Kwun Tong",
    "香港朗廷": "The Langham Hong Kong",
    "香港沙田萬怡飯店": "Courtyard by Marriott Sha Tin",
    "香港尖沙咀皇悅飯店": "Empire Hotel TST",
    "香港如心海景飯店暨會議中心": "L'hotel Nina et Convention Centre",
    "馬哥孛羅香港飯店": "Marco Polo Hongkong Hotel",
    "香港海洋公園萬豪飯店": "Hong Kong Ocean Park Marriott",
    "香港麗豪飯店": "Regal Riverside Hotel",
    "九龍香格里拉": "Kowloon Shangri-La",
    "香港嘉湖海逸飯店": "Harbour Plaza Resort City",
    "香港天際萬豪飯店": "SkyCity Marriott Hotel",
    "紅茶館飯店（紅磡溫思勞街店）": "Bridal Tea House Hung Hom Winslow",
    "香港九龍東皇冠假日飯店": "Crowne Plaza Kowloon East",
    "香港九龍東智選假日飯店": "Holiday Inn Express Kowloon East",
    "旭逸雅捷飯店·旺角": "Hotel Ease Access Mongkok",
    "富豪九龍飯店": "Regal Kowloon Hotel",
    "富薈上環飯店": "iclub Sheung Wan Hotel",
    "富薈馬頭圍飯店": "iclub Ma Tau Wai Hotel",
    "富薈灣仔飯店": "iclub Wan Chai Hotel",
    "富薈炮台山飯店": "iclub Fortress Hill Hotel",
    "香港銅鑼灣維景飯店": "Metropark Hotel Causeway Bay",
    "九龍維景飯店": "Metropark Hotel Kowloon",
    "香港悅品海景飯店（荃灣）": "Hotel COZi Harbour View",
    "香港帝盛飯店": "Dorsett Hong Kong",
    "旭逸飯店·荃灣": "Hotel Ease Tsuen Wan",
    "香港遨凱飯店": "The Arca Hotel",
    "香港港島英迪格飯店": "Hotel Indigo Hong Kong Island",
    "香港JW萬豪飯店": "JW Marriott Hong Kong",
    "香港萬麗海景飯店": "Renaissance Harbour View Hotel",
    "香港美利THE MURRAY": "The Murray Hong Kong",
    "香港置地文華東方飯店": "The Landmark Mandarin Oriental",
    "香港柏寧飯店": "The Park Lane Hong Kong",
    "香港奕居": "The Upper House",
    "香港文華東方飯店": "Mandarin Oriental Hong Kong",
    "深圳羅湖戴斯精選溫德姆飯店": "Days Hotel Luohu Shenzhen",
}

# Common pattern translations for remaining names
PATTERNS = [
    ("飯店", "Hotel"),
    ("酒店", "Hotel"),
    ("旅館", "Inn"),
    ("旅舍", "Hostel"),
    ("公寓", "Apartment"),
    ("賓館", "Guesthouse"),
    ("度假村", "Resort"),
    ("度假飯店", "Resort Hotel"),
    ("民宿", "B&B"),
    ("青年旅舍", "Youth Hostel"),
    ("香港", "Hong Kong "),
    ("尖沙咀", "Tsim Sha Tsui "),
    ("銅鑼灣", "Causeway Bay "),
    ("旺角", "Mongkok "),
    ("灣仔", "Wan Chai "),
    ("荃灣", "Tsuen Wan "),
    ("深圳", "Shenzhen "),
]

def get_english_name(zh_name):
    """Get English name for a Chinese hotel name"""
    # Check exact match first
    if zh_name in CHAIN_MAP:
        return CHAIN_MAP[zh_name]
    # Check partial match
    for key, val in CHAIN_MAP.items():
        if key in zh_name or zh_name in key:
            return val
    return None

with open("C:/Users/tonyng/Desktop/Claude_Code/BROADBANDHK/pages/HKhotel-en.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find all hotel names in the directory table and add English names
# Pattern: <td style="padding:8px 10px;font-weight:500;">CHINESE_NAME</td>
pattern = r'(<td style="padding:8px 10px;font-weight:500;">)(.*?)(</td>)'

def replace_name(match):
    prefix = match.group(1)
    zh_name = match.group(2)
    suffix = match.group(3)
    en_name = get_english_name(zh_name)
    if en_name:
        return f'{prefix}{zh_name}<br><small style="color:#667eea;font-weight:normal;">{en_name}</small>{suffix}'
    return match.group(0)

new_html = re.sub(pattern, replace_name, html)

# Count how many were translated
import re as re2
originals = re2.findall(pattern, html)
translated = sum(1 for m in originals if get_english_name(m[1]))

with open("C:/Users/tonyng/Desktop/Claude_Code/BROADBANDHK/pages/HKhotel-en.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"Total hotels in table: {len(originals)}")
print(f"English names added: {translated}")
print(f"Remaining Chinese only: {len(originals) - translated}")
