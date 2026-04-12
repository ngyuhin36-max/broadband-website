"""Add real GEO optimizations to HKhotel.html and HKhotel-en.html:
1. TravelAgency LocalBusiness schema with full contact + HK areaServed
2. Place schema listing all 18 HK districts with coordinates
3. hasMap link to Google Maps
4. Additional geo meta: ISO-3166 region codes, timezone
5. TouristDestination schema for Hong Kong with attractions
"""
import json, re
from pathlib import Path

# 18 HK districts with centroids (lat, lng, en, zh)
HK_DISTRICTS = [
    ("Central and Western","中西區",22.2820,114.1500),
    ("Wan Chai","灣仔區",22.2777,114.1750),
    ("Eastern","東區",22.2845,114.2170),
    ("Southern","南區",22.2483,114.1543),
    ("Yau Tsim Mong","油尖旺區",22.3130,114.1700),
    ("Sham Shui Po","深水埗區",22.3302,114.1622),
    ("Kowloon City","九龍城區",22.3276,114.1880),
    ("Wong Tai Sin","黃大仙區",22.3419,114.1939),
    ("Kwun Tong","觀塘區",22.3137,114.2259),
    ("Tsuen Wan","荃灣區",22.3722,114.1114),
    ("Kwai Tsing","葵青區",22.3600,114.1200),
    ("Tuen Mun","屯門區",22.3907,113.9753),
    ("Yuen Long","元朗區",22.4430,114.0320),
    ("Tai Po","大埔區",22.4499,114.1649),
    ("Sha Tin","沙田區",22.3815,114.1880),
    ("Sai Kung","西貢區",22.3810,114.2700),
    ("North","北區",22.5000,114.1450),
    ("Islands","離島區",22.2617,113.9427),
]

def build_geo_schemas(lang):
    is_zh = lang == "zh"
    url = "https://broadbandhk.com/pages/HKhotel.html" if is_zh else "https://broadbandhk.com/pages/HKhotel-en.html"
    name = "香港酒店推介格價比較" if is_zh else "Hong Kong Hotels Price Comparison"
    description = "2026 香港全區 730 間酒店格價比較平台" if is_zh else "2026 Hong Kong 730 hotels price comparison platform"
    gmap_query = "https://www.google.com/maps/place/Hong+Kong"

    # TravelAgency LocalBusiness — covers all HK districts as areaServed
    travel = {
        "@context":"https://schema.org",
        "@type":"TravelAgency",
        "name": name,
        "description": description,
        "url": url,
        "image": "https://broadbandhk.com/og-image.png",
        "priceRange": "HK$300 - HK$8,000+",
        "address": {
            "@type":"PostalAddress",
            "addressLocality": "Hong Kong" if not is_zh else "香港",
            "addressRegion":"HK",
            "addressCountry":"HK"
        },
        "geo":{"@type":"GeoCoordinates","latitude":22.3193,"longitude":114.1694},
        "hasMap": gmap_query,
        "areaServed": [
            {"@type":"AdministrativeArea","name":(zh if is_zh else en),
             "geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lng}}
            for en,zh,lat,lng in HK_DISTRICTS
        ],
        "serviceArea": {
            "@type":"GeoShape",
            "box":"22.15,113.82 22.57,114.44"
        },
        "knowsAbout":[
            ("Hong Kong hotels" if not is_zh else "香港酒店"),
            ("Staycation" if not is_zh else "Staycation"),
            ("Hotel price comparison" if not is_zh else "酒店格價"),
            ("Harbour view hotels" if not is_zh else "維港海景酒店"),
            ("Family hotels" if not is_zh else "親子酒店"),
        ]
    }

    # TouristDestination — Hong Kong attractions context
    dest = {
        "@context":"https://schema.org",
        "@type":"TouristDestination",
        "name": "Hong Kong" if not is_zh else "香港",
        "url": url,
        "geo":{"@type":"GeoCoordinates","latitude":22.3193,"longitude":114.1694},
        "touristType":[
            "Business traveller" if not is_zh else "商務旅客",
            "Family" if not is_zh else "親子家庭",
            "Couple" if not is_zh else "情侶",
            "Backpacker" if not is_zh else "背包客",
            "Luxury traveller" if not is_zh else "豪華旅客",
        ],
        "includesAttraction":[
            {"@type":"TouristAttraction","name":("Victoria Harbour" if not is_zh else "維多利亞港"),
             "geo":{"@type":"GeoCoordinates","latitude":22.2910,"longitude":114.1700}},
            {"@type":"TouristAttraction","name":("Victoria Peak" if not is_zh else "太平山頂"),
             "geo":{"@type":"GeoCoordinates","latitude":22.2710,"longitude":114.1498}},
            {"@type":"TouristAttraction","name":("Hong Kong Disneyland" if not is_zh else "香港迪士尼樂園"),
             "geo":{"@type":"GeoCoordinates","latitude":22.3131,"longitude":114.0410}},
            {"@type":"TouristAttraction","name":("Ocean Park" if not is_zh else "海洋公園"),
             "geo":{"@type":"GeoCoordinates","latitude":22.2464,"longitude":114.1751}},
            {"@type":"TouristAttraction","name":("Tsim Sha Tsui Promenade" if not is_zh else "尖沙咀海濱長廊"),
             "geo":{"@type":"GeoCoordinates","latitude":22.2941,"longitude":114.1736}},
            {"@type":"TouristAttraction","name":("The Peak Tram" if not is_zh else "山頂纜車"),
             "geo":{"@type":"GeoCoordinates","latitude":22.2783,"longitude":114.1567}},
            {"@type":"TouristAttraction","name":("Avenue of Stars" if not is_zh else "星光大道"),
             "geo":{"@type":"GeoCoordinates","latitude":22.2935,"longitude":114.1730}},
            {"@type":"TouristAttraction","name":("Lan Kwai Fong" if not is_zh else "蘭桂坊"),
             "geo":{"@type":"GeoCoordinates","latitude":22.2810,"longitude":114.1548}},
        ],
        "subjectOf":{"@type":"WebPage","url":url}
    }

    # Place schema with containsPlace (18 districts)
    hk_place = {
        "@context":"https://schema.org",
        "@type":"City",
        "name":"Hong Kong","alternateName":"香港",
        "geo":{"@type":"GeoCoordinates","latitude":22.3193,"longitude":114.1694},
        "containedInPlace":{"@type":"Country","name":"China","identifier":"CN"},
        "containsPlace":[
            {"@type":"AdministrativeArea","name":(zh if is_zh else en),
             "geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lng}}
            for en,zh,lat,lng in HK_DISTRICTS
        ],
    }

    # Fix stray syntax error — remove trailing brace bug
    import json as J
    # Use string dumping while fixing; TouristDestination has a stray ')' above — fix:
    return travel, dest, hk_place

for lang, path in [("zh","pages/HKhotel.html"),("en","pages/HKhotel-en.html")]:
    # Rebuild manually (can't json-dump the broken dict).
    travel, dest, hk_place = build_geo_schemas(lang)
    p = Path(path)
    s = p.read_text(encoding="utf-8")

    # Build JSON-LD blocks as strings
    def jdump(d): return json.dumps(d, ensure_ascii=False)
    new_blocks = (
        '    <script type="application/ld+json">' + jdump(travel) + '</script>\n'
        '    <script type="application/ld+json">' + jdump(hk_place) + '</script>\n'
        '    <script type="application/ld+json">' + jdump(dest) + '</script>\n'
    )

    # Add additional geo meta (ISO codes + timezone)
    extra_meta = (
        '    <meta name="geo.country" content="HK">\n'
        '    <meta name="geo.region" content="HK">\n'
        '    <meta name="country" content="Hong Kong">\n'
        '    <meta name="DC.coverage.spatial" content="Hong Kong SAR">\n'
        '    <meta name="timezone" content="Asia/Hong_Kong">\n'
        '    <meta name="distribution" content="global">\n'
        '    <meta name="target" content="all">\n'
    )

    # Insert extra_meta right after existing ICBM meta
    s = re.sub(
        r'(<meta name="ICBM" content="[^"]+">\n)',
        lambda m: m.group(1) + extra_meta, s, count=1)

    # Insert new schemas right before first <style>
    s = re.sub(r'(\s*<style>)', r'\n' + new_blocks + r'\1', s, count=1)

    p.write_text(s, encoding="utf-8")
    print(f"{path} GEO boosted: TravelAgency + City containsPlace(18) + TouristDestination")
