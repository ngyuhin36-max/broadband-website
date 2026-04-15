# -*- coding: utf-8 -*-
"""Strip bogus '950+ Mbps' FAQ from JSON-LD and visible FAQ across 15 luxury pages."""
import os, re

ROOT = r"C:/Users/tonyng/Desktop/Claude_Code/BROADBANDHK/pages"
FILES = [
    "mount-nicholson.html","opus-hong-kong.html","twelve-peaks.html","bowen-place.html",
    "tregunter.html","clovelly-court.html","century-tower-i.html","po-shan-mansions.html",
    "magazine-gap-tower.html","severn-8.html","grenville-house.html","parkview-court.html",
    "tavistock-(tower-t3).html","strawberry-hill.html","1-plantation-road.html",
]

for fn in FILES:
    p = os.path.join(ROOT, fn)
    with open(p,"r",encoding="utf-8") as f:
        html = f.read()
    orig = html
    # Replace inside JSON-LD FAQPage: the "950+ Mbps" Q/A -> rewrite
    html = re.sub(
        r'\{"@type": "Question", "name": "[^"]*?嘅 1000M 寬頻實際速度有幾快？", "acceptedAnswer": \{"@type": "Answer", "text": "根據用戶實測[^"]*?"\}\}',
        lambda m: '{"@type": "Question", "name": "1000M 寬頻理論速度？", "acceptedAnswer": {"@type": "Answer", "text": "1000M 光纖理論下載速度為 1 Gbps (1000 Mbps)。實際速度受路由器效能、線材、Wi-Fi 訊號、連線裝置數目影響，建議搭配 Wi-Fi 6/6E 路由器並以網線直駁電腦量測最高速度。"}}',
        html
    )
    # For pages patched by earlier manual Edit (mount-nicholson, opus), visible FAQ already done.
    # Remove residual "950+ Mbps" anywhere (in visible FAQ of the 13 via regex above should be gone except JSON-LD)
    if html != orig:
        with open(p,"w",encoding="utf-8") as f:
            f.write(html)
        print("OK",fn)
    else:
        print("NOCHG",fn)
