import re
from pathlib import Path
p = Path("pages/HKhotel-en.html")
s = p.read_text(encoding="utf-8")

s = s.replace(
    '<title>Hong Kong Hotels 2026 | 451 Hotels Price Comparison · Peninsula · W Hotel · Sheraton</title>',
    '<title>Hong Kong Hotels 2026 | 730 Hotels Compared from HK$380 · Tsim Sha Tsui · Causeway Bay · Staycation & Family</title>')
s = re.sub(r'<meta name="description" content="[^"]+">',
    '<meta name="description" content="2026 Hong Kong Hotels Guide · 730 hotels compared instantly: budget stays from HK$380, 4-star from HK$800, 5-star luxury from HK$2,200. Tsim Sha Tsui / Causeway Bay / Central / Wan Chai / Mongkok / Disney / Airport. Staycation, family, couples, business, pet-friendly, Instagram-worthy picks. Compare Trip.com, Klook and Agoda in one click.">',
    s, count=1)
new_kw = 'Hong Kong hotels 2026,Hong Kong hotel deals,Hong Kong staycation,Hong Kong family hotel,Hong Kong couples hotel,Hong Kong harbour view hotel,Tsim Sha Tsui hotel,Causeway Bay hotel,Central Hong Kong hotel,Wan Chai hotel,Mongkok hotel,Disney Hong Kong hotel,Hong Kong airport hotel,Discovery Bay hotel,budget hotel Hong Kong,5 star hotel Hong Kong,4 star hotel Hong Kong,Peninsula Hong Kong,Mandarin Oriental,Ritz-Carlton HK,Four Seasons HK,W Hong Kong,Rosewood HK,Grand Hyatt HK,pet friendly hotel HK,Hong Kong day use hotel,Hong Kong hotel pool,Hong Kong hotel breakfast'
s = re.sub(r'<meta name="keywords" content="[^"]+">',
           f'<meta name="keywords" content="{new_kw}">', s, count=1)
s = re.sub(r'<meta property="og:title" content="[^"]+">',
           '<meta property="og:title" content="Hong Kong Hotels 2026 | 730 Hotels Compared · Peninsula · Rosewood · W Hotel">', s, count=1)
s = re.sub(r'<meta property="og:description" content="[^"]+">',
           '<meta property="og:description" content="2026 Hong Kong 730 hotels - luxury to budget, all districts, staycation family harbour view picks. Compare Trip.com, Klook, Agoda in one click.">', s, count=1)

s = s.replace('Top Hong Kong Hotels 2026 | 451 Hotels Price Comparison',
              'Top Hong Kong Hotels 2026 | 730 Hotels Price Comparison')
s = s.replace('2026 Hong Kong 451 hotels price comparison covering Tsim Sha Tsui, Causeway Bay, Wan Chai, Mongkok.',
              '2026 Hong Kong 730 real hotels price comparison covering all 18 districts.')
s = s.replace('"name": "Hong Kong Hotels\u6392\u884c\u699c2026"',
              '"name": "Hong Kong Hotels Top Picks 2026"')
s = s.replace('"description": "2026\u5e74\u9999\u6e2fHighly Popular\u9152\u5e97\u6392\u884c\u699c"',
              '"description": "Hong Kong\'s most popular hotels in 2026"')

name_map = {
    "\u9999\u6e2f\u534a\u5cf6\u9152\u5e97 The Peninsula Hong Kong": "The Peninsula Hong Kong",
    "\u9999\u6e2f\u6587\u83ef\u6771\u65b9\u9152\u5e97 Mandarin Oriental Hong Kong": "Mandarin Oriental, Hong Kong",
    "\u9999\u6e2f\u9e97\u601d\u5361\u723e\u9813\u9152\u5e97 The Ritz-Carlton Hong Kong": "The Ritz-Carlton, Hong Kong",
    "Tsim Sha Tsui\u51f1\u60a6\u9152\u5e97 Hyatt Regency Tsim Sha Tsui": "Hyatt Regency Hong Kong, Tsim Sha Tsui",
    "\u9999\u6e2f\u7f8e\u5229\u9152\u5e97 The Murray Hong Kong": "The Murray, Hong Kong",
    "\u9999\u6e2fW\u9152\u5e97 W Hong Kong": "W Hong Kong",
    "Mongkok\u5e1d\u76db\u9152\u5e97 Dorsett Mongkok": "Dorsett Mongkok, Hong Kong",
    "Causeway Bay\u7687\u51a0\u5047\u65e5\u9152\u5e97 Crowne Plaza Causeway Bay": "Crowne Plaza Hong Kong Causeway Bay",
    "\u7d05\u8336\u9928\u9152\u5e97 Bridal Tea House Hotel": "Bridal Tea House Hotel",
    "\u9999\u6e2f\u6109\u666f\u7063\u9152\u5e97 Auberge Discovery Bay": "Auberge Discovery Bay Hong Kong",
    "\u9999\u6e2f\u56db\u5b63\u9152\u5e97 Four Seasons Hotel Hong Kong": "Four Seasons Hotel Hong Kong",
    "\u9999\u6e2f\u541b\u60a6\u9152\u5e97 Grand Hyatt Hong Kong": "Grand Hyatt Hong Kong",
    "\u9999\u6e2f\u7470\u9e97\u9152\u5e97 Rosewood Hong Kong": "Rosewood Hong Kong",
    "\u9999\u6e2fOcean Park\u842c\u8c6a\u9152\u5e97 Marriott Ocean Park": "Hong Kong Ocean Park Marriott Hotel",
    "\u552f\u6e2f\u85c8 Hotel ICON": "Hotel ICON",
}
for zh, en in name_map.items():
    s = s.replace(f'"name":"{zh}"', f'"name":"{en}"')

addr_map = {
    "\u68b3\u58eb\u5df4\u5229\u9053": "Salisbury Road",
    "\u5e72\u8afe\u9053\u4e2d5\u865f": "5 Connaught Road Central",
    "\u67ef\u58eb\u7538\u9053\u897f1\u865f": "1 Austin Road West",
    "\u6cb3\u5167\u9053\u0031\u0038\u865f": "18 Hanoi Road",
    "\u7d05\u68c9\u8def22\u865f": "22 Cotton Tree Drive",
    "\u8354\u679d\u89d2\u9053\u0038\u0038\u865f": "88 Lai Chi Kok Road",
    "\u79ae\u9813\u9053\u0038\u865f": "8 Leighton Road",
    "\u767d\u52a0\u58eb\u8857\u0034\u0035\u865f": "45 Parkes Street",
    "\u6109\u666f\u7063\u9053\u0038\u0038\u865f": "88 Siena Avenue",
    "\u91d1\u878d\u8857\u0038\u865f": "8 Finance Street",
    "\u6e2f\u7063\u9053\u0031\u865f": "1 Harbour Road",
    "\u68b3\u58eb\u5df4\u5229\u9053\u0031\u0038\u865f": "18 Salisbury Road",
    "Ocean Park\u9053180\u865f": "180 Wong Chuk Hang Road",
    "\u79d1\u5b78\u9928\u9053\u0031\u0037\u865f": "17 Science Museum Road",
    "\u9ec3\u7af9\u5751": "Wong Chuk Hang",
    "TST East": "Tsim Sha Tsui East"
}
for zh, en in addr_map.items():
    s = s.replace(f'"streetAddress":"{zh}"', f'"streetAddress":"{en}"')
    s = s.replace(f'"addressLocality":"{zh}"', f'"addressLocality":"{en}"')

s = re.sub(r',"aggregateRating":\{"@type":"AggregateRating","bestRating":"10","worstRating":"1","ratingValue":"[^"]+","reviewCount":"\d+"\}', '', s)

old = '    </script>\n\n    <style>'
new_blocks = '''    </script>

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type":"ListItem","position":1,"name":"Home","item":"https://broadbandhk.com/"},
            {"@type":"ListItem","position":2,"name":"Travel Hotels","item":"https://broadbandhk.com/pages/HKhotel-en.html"},
            {"@type":"ListItem","position":3,"name":"Hong Kong Hotels"}
        ]
    }
    </script>

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type":"Question","name":"How much does a Hong Kong hotel cost per night in 2026?","acceptedAnswer":{"@type":"Answer","text":"Prices span a wide range. Budget guesthouses run HK$300-800/night; 3-star business hotels HK$700-1,500; 4-star HK$1,200-2,500; 5-star luxury HK$2,500-8,000+. Peak periods (Christmas, Chinese New Year, fireworks nights) typically add 40-100% - book 4-8 weeks in advance."}},
            {"@type":"Question","name":"Which are the cheapest hotels in Hong Kong?","acceptedAnswer":{"@type":"Answer","text":"Under HK$500/night: Bridal Tea House Hotel (13 branches citywide), Panda Hotel (Tsuen Wan), Maple Leaf Hotel (Wan Chai), Dorsett Mongkok economy rooms. HK$500-800: Empire Hotel, Silka Tsuen Wan, Rosedale Hotel. Always compare Trip.com, Klook and Agoda - the same hotel can vary 15-30%."}},
            {"@type":"Question","name":"What are the best Hong Kong staycation hotels?","acceptedAnswer":{"@type":"Answer","text":"Top weekday staycation picks: Kerry Hotel (Hung Hom, private beach), Nina Hotel Tsuen Wan West (free shuttle bus), Ocean Park Marriott (aquarium-themed suites), Auberge Discovery Bay (family resort). Weekend rates often add 30-50%; Sunday-Monday stays are typically much better value."}},
            {"@type":"Question","name":"Which Hong Kong hotels are best for families?","acceptedAnswer":{"@type":"Answer","text":"Family favourites: Hong Kong Disneyland Hotel / Explorers Lodge / Hollywood Hotel (3 at Disney), Ocean Park Marriott (ocean-themed suites), Auberge Discovery Bay (private beach), Kerry Hotel (Kids Club), Four Seasons (family pool + Kids For All Seasons)."}},
            {"@type":"Question","name":"Which hotel should I pick in Tsim Sha Tsui?","acceptedAnswer":{"@type":"Answer","text":"Classic Tsim Sha Tsui picks: The Peninsula (the 1928 landmark), Rosewood (2019 new at Victoria Dockside), Mandarin Oriental, Sheraton (next to Peninsula), Hyatt Regency (MTR-connected), Hotel ICON (award-winning design hotel). Harbour View rooms face Victoria Harbour."}},
            {"@type":"Question","name":"Which airport hotels are closest?","acceptedAnswer":{"@type":"Answer","text":"Walking distance: Regal Airport Hotel (3-min covered walkway directly to departure hall). 5-10 min by shuttle: Regala Skycity Hotel (opened 2022), Four Points by Sheraton Tung Chung, Novotel Citygate. Many offer Day Use (6 hours from HK$380) - perfect for long layovers."}},
            {"@type":"Question","name":"Which Hong Kong hotels have the best harbour views?","acceptedAnswer":{"@type":"Answer","text":"Tsim Sha Tsui waterfront: The Peninsula, Rosewood, InterContinental Grand Stanford. Wan Chai: Grand Hyatt, Conrad (Admiralty). West Kowloon: W Hotel (76F infinity pool), Ritz-Carlton (118F Ozone, world\'s highest bar). Harbour View rooms typically add 30-50% on base rate."}},
            {"@type":"Question","name":"Do Hong Kong hotels offer Day Use?","acceptedAnswer":{"@type":"Answer","text":"Yes - hotels offering day-use packages include Regal Airport (6 hours from HK$380), Regala Skycity, Four Points Tung Chung, Hotel ICON, Crowne Plaza Causeway Bay and New World Millennium. Search Day Use filter on Trip.com. Great for long layovers or delays."}},
            {"@type":"Question","name":"Which Hong Kong hotels are pet-friendly?","acceptedAnswer":{"@type":"Answer","text":"Pet-friendly: Auberge Discovery Bay (whole DB community is pet-friendly), The Warrick (Tung Chung), selected Ovolo properties. Book the Pet Friendly Room when reserving; extra cleaning fee HK$300-500/night. Always confirm current policy with the hotel directly."}},
            {"@type":"Question","name":"Trip.com vs Klook vs Agoda - which is cheapest?","acceptedAnswer":{"@type":"Answer","text":"The same hotel on the same night can differ 15-30% across the three. Trip.com has the widest inventory; Klook often bundles staycation packages (incl. breakfast or buffet); Agoda Secret Deals occasionally win on flash sales. Open all three tabs and compare before you book."}}
        ]
    }
    </script>

    <style>'''
s = s.replace(old, new_blocks)

p.write_text(s, encoding="utf-8")
print("HKhotel-en.html optimized")
print("schemas:", s.count('"@context"'))
print("hreflang:", s.count('hreflang='))
print("aggregateRating:", s.count('aggregateRating'))
