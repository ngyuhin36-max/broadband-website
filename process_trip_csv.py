"""
Process Trip.com CSV data and generate hotel list HTML
for travel-hotel-deals.html
"""
import csv

AFF_URL = "https://tw.trip.com/hotels/list?city=58&display=%E9%A6%99%E6%B8%AF&optionId=58&optionType=City&optionName=%E9%A6%99%E6%B8%AF&Allianceid=8067382&SID=305319575&trip_sub1=&trip_sub3=D15325011"

# Hotels already in the page (don't duplicate)
EXISTING = {
    "香港半島酒店", "香港文華東方酒店", "香港麗思卡爾頓酒店",
    "尖沙咀凱悅酒店", "香港美利酒店", "香港W酒店",
    "旺角帝盛酒店", "銅鑼灣皇冠假日酒店", "紅茶館酒店",
    "香港愉景灣酒店", "香港四季酒店", "香港君悅酒店",
    "香港瑰麗酒店", "香港海洋公園萬豪酒店", "唯港薈",
    "香港皇悅卓越酒店", "荃灣西如心酒店", "香港喜來登酒店",
    "麗豪航天城酒店", "香港悅來酒店", "香港灣仔帝盛酒店",
    "合和酒店", "香港珀麗酒店", "香港灣仔皇悅酒店",
    "香港楓葉旅館", "尖沙咀帝苑酒店", "香港銅鑼灣皇悅酒店",
    "香港港麗酒店", "香港嘉里酒店", "香港迪士尼樂園酒店",
    "千禧新世界香港飯店", "香港帝京酒店", "香港東涌福朋喜來登飯店",
    "香港富豪機場酒店", "灣景國際", "旭逸雅捷酒店",
    "迪士尼好萊塢飯店", "香港荃灣帝盛酒店",
    # Also match Trip.com naming variants
    "香港灣仔帝盛飯店", "荃灣西如心飯店", "香港皇悅卓越飯店",
    "香港灣仔皇悅飯店", "香港楓葉旅館", "香港喜來登飯店",
    "合和飯店", "香港悅來飯店", "香港荃灣帝盛飯店",
    "千禧新世界香港飯店", "香港君悅飯店", "香港珀麗飯店",
    "麗豪航天城飯店", "香港東湧福朋喜來登飯店",
    "迪士尼好萊塢飯店", "香港銅鑼灣皇悅飯店",
    "尖沙咀帝苑飯店", "旭逸雅捷飯店",
}

def is_existing(name):
    for e in EXISTING:
        if e in name or name in e:
            return True
    return False

def main():
    hotels = []
    seen = set()

    with open("C:/Users/tonyng/Downloads/tw.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["hotelName"].strip()
            if not name or name in seen:
                continue
            seen.add(name)

            if is_existing(name):
                continue

            price = row.get("sale", "").replace("HKD", "").replace(",", "").strip()
            orig = row.get("delete", "").replace("HKD", "").replace(",", "").strip()

            if not price:
                continue

            hotels.append({"name": name, "price": int(price), "orig": int(orig) if orig else 0})

    print(f"New hotels to add: {len(hotels)}")

    # Generate compact hotel list HTML
    html_parts = []
    html_parts.append("""
            <!-- === Trip.com Full Hotel Directory (auto-generated from CSV) === -->
            <div class="faq-section" style="margin-top:40px;">
                <h2>更多香港酒店（Trip.com 全部酒店目錄）</h2>
                <p style="color:#666;font-size:0.9em;margin-bottom:20px;">以下酒店全部可在 Trip.com 預訂，點擊即可查看詳情及最新價格。</p>
                <div style="overflow-x:auto;">
                    <table style="width:100%;border-collapse:collapse;font-size:0.85em;">
                        <thead>
                            <tr style="background:#667eea;color:white;">
                                <th style="padding:10px;text-align:left;border-radius:8px 0 0 0;">酒店名稱</th>
                                <th style="padding:10px;text-align:center;">優惠價</th>
                                <th style="padding:10px;text-align:center;">原價</th>
                                <th style="padding:10px;text-align:center;border-radius:0 8px 0 0;">預訂</th>
                            </tr>
                        </thead>
                        <tbody>""")

    for i, h in enumerate(hotels):
        bg = ' style="background:#fafafa;"' if i % 2 == 1 else ""
        orig_html = f"<s style='color:#999;'>HK${h['orig']:,}</s>" if h["orig"] else "-"
        html_parts.append(f"""
                            <tr{bg}>
                                <td style="padding:8px 10px;font-weight:500;">{h['name']}</td>
                                <td style="padding:8px 10px;text-align:center;color:#ff4757;font-weight:bold;">HK${h['price']:,}</td>
                                <td style="padding:8px 10px;text-align:center;">{orig_html}</td>
                                <td style="padding:8px 10px;text-align:center;"><a href="{AFF_URL}" target="_blank" rel="noopener noreferrer nofollow" style="background:#287DFA;color:white;padding:4px 12px;border-radius:4px;text-decoration:none;font-size:0.85em;">格價</a></td>
                            </tr>""")

    html_parts.append("""
                        </tbody>
                    </table>
                </div>
                <p style="color:#888;font-size:0.78em;margin-top:10px;">* 價格僅供參考，實際價格視乎入住日期。點擊「格價」查看 Trip.com 最新優惠。</p>
            </div>""")

    output = "\n".join(html_parts)

    with open("C:/Users/tonyng/Desktop/Claude_Code/BROADBANDHK/trip_hotels_table.html", "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Generated HTML with {len(hotels)} hotels -> trip_hotels_table.html")

if __name__ == "__main__":
    main()
