"""
自動深度文章生成系統
每周自動生成 2 篇 SEO 優化嘅深度文章
自動發佈到網站、更新 blog.html、更新 sitemap
"""

import json
import os
import re
import random
import hashlib
from datetime import datetime, timezone, timedelta

HKT = timezone(timedelta(hours=8))
TODAY = datetime.now(HKT)
DATE_STR = TODAY.strftime("%Y-%m-%d")
DATE_DISPLAY = f"{TODAY.year} 年 {TODAY.month} 月 {TODAY.day} 日"
SITE_URL = "https://broadbandhk.com"
KB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "kb")
BLOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "blog.html")
SITEMAP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
PUBLISHED_LOG = os.path.join(os.path.dirname(__file__), "published_articles.json")


# ============================================================
# 文章模板庫 — 每篇都係獨特嘅深度內容
# ============================================================
ARTICLE_TEMPLATES = [
    {
        "slug": "broadband-speed-explained",
        "title": "100M、500M、1000M 寬頻速度有咩分別？實測話你知邊個最抵用",
        "description": "100M夠唔夠用？500M同1000M差幾遠？實測數據話你知唔同速度嘅真實體驗，幫你揀最適合嘅Plan。",
        "keywords": "寬頻速度比較, 100M寬頻, 500M寬頻, 1000M寬頻, 網速分別, 寬頻邊個速度好",
        "category": "beginner",
        "cat_class": "cat-beginner",
        "cat_name": "新手入門",
        "card_desc": "100M夠唔夠用？500M同1000M差幾遠？實測數據幫你揀最適合嘅Plan。",
        "faqs": [
            ("100M寬頻夠唔夠用？", "如果屋企只有1-2人上網，主要睇網頁、社交媒體同標清串流，100M基本夠用。但如果有3人以上同時用、或者要睇4K Netflix，建議至少500M。100M嘅實際下載速度大約12MB/秒，下載一套1GB嘅電影大約需要1分半鐘。"),
            ("500M同1000M體感差別大唔大？", "日常上網體感差別唔算太大，因為大部分網站同App嘅伺服器速度本身就有限制。但係下載大型檔案（遊戲、4K電影）時差別明顯：500M下載100GB遊戲大約要27分鐘，1000M只需13分鐘。如果屋企多人同時用，1000M嘅優勢會更明顯。"),
            ("點解我1000M寬頻測速只有500-600M？", "呢個好正常！WiFi本身有訊號衰減，穿牆後速度會大打折扣。要測到接近1000M，需要用LAN線直接連接Router。另外，舊款Router（唔支援WiFi 6）、舊電腦網卡都會限制速度。建議用5GHz WiFi頻段同埋WiFi 6以上嘅Router。")
        ],
        "sections": [
            ("速度 = 車道，唔係車速", """
            <p>好多人以為寬頻速度愈快，開網頁就愈快。但其實寬頻速度更似「車道闊度」——100M就好似一條單線行車道，1000M就好似十線高速公路。</p>
            <p>一個人用100M，好似一架車行單線路，暢通無阻；但如果全家4-5個人同時用，就好似5架車迫一條路，大家都慢咗。呢個時候1000M嘅優勢就出嚟——每個人都有自己嘅車道。</p>
            <div class="tip-box"><strong>💡 重點：</strong>寬頻速度主要影響「同時間幾多人/裝置可以流暢使用」，而唔係「單獨使用時有幾快」。</div>
            """),
            ("唔同速度嘅實際體驗比較", """
            <table class="comparison-table">
                <tr><th>使用場景</th><th>100M</th><th>500M</th><th>1000M</th></tr>
                <tr><td>睇 YouTube 1080p</td><td>✅ 流暢</td><td>✅ 流暢</td><td>✅ 流暢</td></tr>
                <tr><td>Netflix 4K</td><td>⚠ 1人OK</td><td>✅ 3人OK</td><td>✅ 5人以上</td></tr>
                <tr><td>Zoom 視像會議</td><td>✅ 1-2人</td><td>✅ 3-4人</td><td>✅ 全家開會</td></tr>
                <tr><td>下載 100GB 遊戲</td><td>⏱ 2.5小時</td><td>⏱ 27分鐘</td><td>⏱ 13分鐘</td></tr>
                <tr><td>多人同時打機+串流</td><td>❌ 會lag</td><td>✅ OK</td><td>✅ 完全冇問題</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>建議人數</td><td>1-2人</td><td>3-4人</td><td>5人以上</td></tr>
            </table>
            """),
            ("邊種速度最抵用？性價比分析", """
            <p>以2026年香港市場嚟講，<strong>500M 係性價比最高嘅選擇</strong>。原因：</p>
            <ul>
                <li><strong>價錢差距唔大：</strong>500M月費通常只比100M貴$20-40，但速度係5倍</li>
                <li><strong>夠用但唔浪費：</strong>適合大部分3-4人家庭嘅日常需求</li>
                <li><strong>1000M溢價較高：</strong>1000M月費通常比500M貴$50-100，但日常體感提升唔算明顯</li>
            </ul>
            <div class="tip-box"><strong>💡 揀Plan建議：</strong>1-2人住➡100M、3-4人住➡500M、5人以上/打機重度用戶/在家工作➡1000M。如果月費差距細過$30，直接揀高一級。</div>
            """),
            ("影響實際速度嘅隱藏因素", """
            <p>就算你裝咗1000M，以下因素都可能令你嘅實際體驗打折扣：</p>
            <ul>
                <li><strong>Router質素：</strong>ISP送嘅免費Router通常只支援WiFi 5，最高速度大約500-600Mbps。想發揮1000M全速，需要WiFi 6/6E Router</li>
                <li><strong>WiFi穿牆衰減：</strong>每穿一道牆，速度大約減半。如果Router放客廳，房間可能只有200-300M。解決方法：用Mesh WiFi系統</li>
                <li><strong>裝置限制：</strong>舊手機（iPhone 10以前）同舊電腦嘅網卡可能只支援WiFi 5，速度上限大約400-500Mbps</li>
                <li><strong>光纖到戶 vs 光纖到樓：</strong>FTTH（光纖到戶）速度穩定；FTTB（光纖到樓）最後一段用銅線，速度可能唔穩定</li>
            </ul>
            """)
        ]
    },
    {
        "slug": "broadband-contract-tips-2026",
        "title": "2026年寬頻續約攻略：點樣傾到最平月費？7個議價秘技",
        "description": "寬頻合約就快到期？教你7個議價秘技同續約攻略，幫你慳到最多！附真實議價對話範例。",
        "keywords": "寬頻續約, 寬頻議價, 寬頻合約到期, 寬頻減價, 寬頻轉台, 續約攻略, 寬頻平方案",
        "category": "saving",
        "cat_class": "cat-saving",
        "cat_name": "慳錢攻略",
        "card_desc": "寬頻合約就快到期？7個議價秘技幫你傾到最平月費，附真實對話範例。",
        "faqs": [
            ("寬頻合約到期唔續約會點？", "合約到期後通常會自動轉為「按月計劃」，月費會比合約價貴20-50%。所以一定要喺到期前1-2個月主動聯絡供應商議價或者轉台。千祈唔好等佢自動續約。"),
            ("幾時開始傾續約最好？", "最佳時機係合約到期前1-2個月。太早傾（3個月前）供應商未必肯俾最筍價；到期後先傾就已經蝕咗按月計嘅差價。建議喺到期前6-8周開始格價，到期前4周正式傾判。"),
            ("轉台真係會平啲？", "係！轉台通常比原供應商續約平10-30%，因為新客優惠永遠最筍。但要考慮轉台嘅安裝費（部分供應商免費）同埋轉換期間嘅斷網問題。如果原供應商肯Match新客價，留低其實最方便。")
        ],
        "sections": [
            ("點解續約價永遠貴過新客價？", """
            <p>呢個係電訊業嘅「公開秘密」——寬頻供應商永遠用最筍嘅價錢吸引新客，因為搶客比留客更重要。</p>
            <p>根據我哋嘅數據，<strong>同一供應商嘅續約價平均比新客價貴15-30%</strong>。舉個例子：</p>
            <table class="comparison-table">
                <tr><th>供應商</th><th>1000M 新客價</th><th>1000M 續約價</th><th>差價</th></tr>
                <tr><td>HKBN 香港寬頻</td><td>$158/月</td><td>$198/月</td><td>+$40</td></tr>
                <tr><td>HGC 環電</td><td>$148/月</td><td>$188/月</td><td>+$40</td></tr>
                <tr><td>CMHK 中國移動</td><td>$108/月</td><td>$148/月</td><td>+$40</td></tr>
                <tr><td>SmarTone</td><td>$168/月</td><td>$208/月</td><td>+$40</td></tr>
            </table>
            <p><em>*以上為2026年Q1市場參考價，實際價格因地區、合約期而異</em></p>
            <div class="tip-box"><strong>💡 關鍵：</strong>識得議價嘅客戶平均可以慳到$30-60/月，即每年慳$360-720！</div>
            """),
            ("7個實戰議價秘技", """
            <h3>秘技 1：格價先行</h3>
            <p>議價前，先去各大供應商網站睇最新新客價。呢啲價錢就係你嘅「彈藥」。推薦用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK 格價計算器</a> 快速比較。</p>

            <h3>秘技 2：表明轉台意向</h3>
            <p>打去客服時，唔好話「想續約」，要講「想取消服務」或「想了解轉台手續」。呢個時候你會被轉去「客戶挽留部」，佢哋有權批出更平嘅價錢。</p>

            <h3>秘技 3：用競爭對手嘅報價做籌碼</h3>
            <p>「我收到XX供應商嘅報價，同樣1000M只需要$XXX/月，如果你哋Match唔到呢個價錢，我就要轉台喇。」呢句說話係最強武器。</p>

            <h3>秘技 4：揀啱時間傾</h3>
            <p>月底（25-31號）係銷售團隊衝業績嘅時候，佢哋會更願意俾更好嘅價錢。星期一至三嘅下午通常人少，客服有更多時間同你傾。</p>

            <h3>秘技 5：要求「送」而唔係「減」</h3>
            <p>如果月費減唔到，可以要求免安裝費、送Router、送幾個月月費、免費升級速度等。呢啲對供應商嘅成本較低，佢哋更容易答應。</p>

            <h3>秘技 6：唔好即時答應</h3>
            <p>第一個報價永遠唔係最低價。聽完offer後講「我考慮下先」，通常幾日內佢哋會再打嚟俾更好嘅價。</p>

            <h3>秘技 7：善用「忠誠客戶」身份</h3>
            <p>如果你已經用咗同一供應商3年以上，可以話「我做咗你哋咁多年忠實客戶，我相信你哋可以俾到一個更好嘅價錢留住我。」呢個往往有額外折扣。</p>
            """),
            ("真實議價對話範例", """
            <div style="background:#f8fafc;border-radius:12px;padding:24px;margin:20px 0;border:1px solid #e2e8f0;">
            <p><strong>你：</strong>「你好，我嘅合約下個月到期，我想了解取消服務嘅手續。」</p>
            <p><strong>客服：</strong>（轉你去挽留部門）</p>
            <p><strong>挽留專員：</strong>「先生/小姐，我睇到你嘅合約就快到期。我可以幫你安排續約，而家有個優惠⋯⋯」</p>
            <p><strong>你：</strong>「唔該，我已經收到XX供應商嘅報價，同樣1000M只需$138/月，仲免安裝費。如果你哋Match唔到呢個價，我就轉台喇。」</p>
            <p><strong>挽留專員：</strong>「等我幫你睇下⋯⋯我可以幫你申請特別優惠價$148/月。」</p>
            <p><strong>你：</strong>「$148仲係貴過人哋嘅$138喎。你有冇其他優惠可以配合？例如免Router費或者送幾個月？」</p>
            <p><strong>挽留專員：</strong>「咁我幫你申請$148/月，另外免首3個月月費，即係平均$111/月。」</p>
            <p><strong>你：</strong>「好，咁我考慮下先，聽日覆你。」<em>（等佢再加碼）</em></p>
            </div>
            """),
            ("續約 vs 轉台 完整比較", """
            <table class="comparison-table">
                <tr><th>因素</th><th>續約（原供應商）</th><th>轉台（新供應商）</th></tr>
                <tr><td>月費</td><td>通常較貴</td><td>通常較平（新客價）</td></tr>
                <tr><td>安裝費</td><td>免費</td><td>$0-$680（睇供應商）</td></tr>
                <tr><td>斷網期</td><td>無</td><td>可能有1-3日</td></tr>
                <tr><td>麻煩程度</td><td>低</td><td>中（要安排安裝）</td></tr>
                <tr><td>合約期</td><td>通常24個月</td><td>通常24個月</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>最佳策略</td><td colspan="2">先拎新客價做參考 → 同原供應商議價 → 議唔成先轉台</td></tr>
            </table>
            """)
        ]
    },
    {
        "slug": "wifi-dead-zones-fix",
        "title": "WiFi死角點算？5個方法徹底解決屋企WiFi收唔到訊號",
        "description": "房間WiFi好弱？廁所完全收唔到？教你5個方法徹底解決WiFi死角問題，全屋訊號滿格。",
        "keywords": "WiFi死角, WiFi收唔到, WiFi訊號弱, Mesh WiFi, WiFi延伸器, 路由器擺位, WiFi穿牆",
        "category": "tech",
        "cat_class": "cat-tech",
        "cat_name": "技術知識",
        "card_desc": "房間WiFi好弱？廁所完全收唔到？5個方法徹底解決WiFi死角，全屋訊號滿格。",
        "faqs": [
            ("WiFi延伸器同Mesh WiFi有咩分別？", "WiFi延伸器係接收現有WiFi訊號再放大，速度通常會減半，而且切換時會斷線。Mesh WiFi係多個節點組成一個網絡，速度損失少、切換無縫。如果屋企大過600呎，強烈建議用Mesh WiFi。"),
            ("Router放邊度最好？", "最理想係放喺屋企正中間、離地1-1.5米高嘅位置。避免放喺角落、地上、金屬物品旁邊、或者微波爐附近。如果入線位喺門口，可以用長LAN線將Router移到更中央嘅位置。"),
            ("2.4GHz同5GHz WiFi揀邊個好？", "5GHz速度快但穿牆能力弱，適合喺Router附近使用；2.4GHz速度較慢但穿牆能力強，適合隔牆嘅房間。大部分Router會自動分配，但如果你喺Router旁邊，手動連5GHz會更快。")
        ],
        "sections": [
            ("點解屋企會有WiFi死角？", """
            <p>WiFi訊號本質上係無線電波，會被各種物理因素阻擋同吸收：</p>
            <ul>
                <li><strong>牆壁：</strong>每道磚牆會令訊號衰減40-50%，鋼筋混凝土牆更嚴重</li>
                <li><strong>距離：</strong>WiFi 訊號每遠離1米，強度就減少約6%</li>
                <li><strong>干擾：</strong>微波爐、藍牙裝置、鄰居嘅WiFi都會造成干擾</li>
                <li><strong>Router位置：</strong>放喺角落嘅Router只能覆蓋180度，浪費咗一半訊號</li>
            </ul>
            <p>典型香港住宅（400-700呎）通常有1-2個WiFi死角，最常見係主人房同廁所。</p>
            """),
            ("方法1：優化Router擺位（免費）", """
            <p>最簡單有效嘅方法，唔使花一蚊：</p>
            <ul>
                <li>將Router移到屋企<strong>最中央</strong>嘅位置</li>
                <li>放喺<strong>離地1-1.5米</strong>嘅架上（唔好放地上）</li>
                <li>遠離<strong>金屬物品</strong>同<strong>微波爐</strong></li>
                <li>Router天線（如有）指向<strong>不同方向</strong>（一支直、一支打橫）</li>
                <li>用App測試唔同位置嘅訊號強度，搵到最佳擺位</li>
            </ul>
            <div class="tip-box"><strong>💡 實測：</strong>單係將Router從門口角落移到客廳電視櫃上，主人房嘅WiFi速度可以由50Mbps提升到200Mbps以上！</div>
            """),
            ("方法2：升級WiFi 6/6E Router（$300-800）", """
            <p>如果你仲用緊ISP送嘅舊Router，升級係最值得嘅投資：</p>
            <table class="comparison-table">
                <tr><th>規格</th><th>WiFi 5（舊）</th><th>WiFi 6</th><th>WiFi 6E</th></tr>
                <tr><td>最高速度</td><td>~800Mbps</td><td>~1,200Mbps</td><td>~2,400Mbps</td></tr>
                <tr><td>多裝置表現</td><td>差</td><td>好</td><td>極好</td></tr>
                <tr><td>穿牆能力</td><td>一般</td><td>較好</td><td>好（6GHz穿牆弱）</td></tr>
                <tr><td>價錢</td><td>—</td><td>$300-500</td><td>$500-800</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>推薦</td><td>應該換</td><td>最佳性價比</td><td>預算充裕首選</td></tr>
            </table>
            """),
            ("方法3：安裝Mesh WiFi系統（$600-2000）", """
            <p>如果屋企大過500呎或者牆多，Mesh WiFi係終極解決方案：</p>
            <ul>
                <li><strong>原理：</strong>2-3個WiFi節點組成一個無縫網絡，全屋一個WiFi名</li>
                <li><strong>優勢：</strong>行到邊度都自動連接最近嘅節點，唔會斷線</li>
                <li><strong>適合：</strong>500呎以上、2房以上嘅住宅</li>
            </ul>
            <p>2026年推薦 Mesh WiFi 系統：</p>
            <ul>
                <li><strong>TP-Link Deco X50</strong>（$580/2件裝）— 性價比之王</li>
                <li><strong>ASUS ZenWiFi AX</strong>（$1,200/2件裝）— 功能最齊全</li>
                <li><strong>Google Nest WiFi Pro</strong>（$1,500/2件裝）— 最易設定</li>
            </ul>
            <div class="tip-box"><strong>💡 慳錢Tips：</strong>如果屋企只有一個死角位，用LAN線拉一部平嘅WiFi 6 Router做AP（接入點）模式，$300就搞掂，效果同Mesh差唔多！</div>
            """),
            ("方法4：用Powerline / MoCA 有線延伸（$200-500）", """
            <p>唔想拉LAN線、又唔想買Mesh？Powerline適配器利用屋企嘅電線傳輸網絡訊號：</p>
            <ul>
                <li>將一個接Router，另一個接WiFi死角嘅插座</li>
                <li>訊號通過電線傳輸，唔受牆壁影響</li>
                <li>速度可達200-500Mbps（取決於電線質素）</li>
                <li>注意：跨電錶可能唔work，同一電路效果最好</li>
            </ul>
            """),
            ("方法5：轉用5GHz + 頻道優化（免費）", """
            <p>香港住宅密度高，WiFi干擾係大問題。以下設定可以改善：</p>
            <ul>
                <li>登入Router管理頁面（通常 192.168.1.1）</li>
                <li>將5GHz頻道改為<strong>較少人用嘅頻道</strong>（用WiFi Analyzer App掃描）</li>
                <li>開啟<strong>Band Steering</strong>功能，自動引導裝置用5GHz</li>
                <li>將2.4GHz頻寬設為<strong>20MHz</strong>（減少同鄰居干擾）</li>
                <li>將5GHz頻寬設為<strong>80MHz或160MHz</strong>（增加速度）</li>
            </ul>
            """)
        ]
    },
    {
        "slug": "elderly-broadband-guide",
        "title": "長者上網入門：幫爸媽揀寬頻同設定WiFi嘅完整指南",
        "description": "點樣幫屋企長者揀啱寬頻？Router設定、WiFi連接、防詐騙全教學，子女必讀嘅孝順指南。",
        "keywords": "長者上網, 老人家寬頻, 長者WiFi設定, 長者智能手機上網, 長者防詐騙, 長者平板電腦",
        "category": "trending",
        "cat_class": "cat-trending",
        "cat_name": "熱門話題",
        "card_desc": "幫爸媽揀啱寬頻、設定WiFi、防網絡詐騙，子女必讀嘅孝順指南。",
        "faqs": [
            ("長者需要幾快嘅寬頻？", "一般長者主要用嚟視像通話、睇新聞同YouTube，100M已經綽綽有餘。如果同仔女同住，按全家人數揀速度。唔需要為長者單獨裝最快嘅Plan。"),
            ("點樣教長者連WiFi？", "最簡單嘅方法係幫佢哋設定好WiFi自動連接，之後就唔使理。你可以將WiFi密碼印出嚟貼喺Router旁邊，或者用QR Code，長者用手機掃一掃就連到。大部分手機連過一次之後都會自動記住。"),
            ("長者容易中網絡詐騙，點算？", "安裝瀏覽器嘅廣告攔截器、設定DNS過濾（如CleanBrowsing），同埋教佢哋一條鐵則：「任何叫你俾錢、俾密碼嘅訊息，一定要先問仔女」。定期幫佢哋檢查手機有冇裝到可疑App。")
        ],
        "sections": [
            ("長者上網需求分析", """
            <p>根據統計，香港65歲以上長者最常用嘅網絡功能：</p>
            <ul>
                <li><strong>WhatsApp/微信：</strong>同仔女朋友傾計、傳相（93%長者使用）</li>
                <li><strong>視像通話：</strong>見到個孫、同遠方親友傾偈（78%）</li>
                <li><strong>YouTube：</strong>睇新聞、粵曲、煮飯教學（71%）</li>
                <li><strong>睇新聞：</strong>東網、HK01、明報等（65%）</li>
                <li><strong>Facebook：</strong>睇朋友動態、睇群組（52%）</li>
            </ul>
            <p>以上所有用途，<strong>100M寬頻已經完全足夠</strong>。</p>
            """),
            ("幫長者揀Plan嘅4個重點", """
            <ul>
                <li><strong>揀最簡單嘅Plan：</strong>唔好揀包電話、包OTT嘅組合套餐，長者用唔到亦唔會用，純寬頻最好</li>
                <li><strong>合約期揀24個月：</strong>月費最平，長者通常唔會轉供應商</li>
                <li><strong>要有中文客服：</strong>萬一有問題，長者可以自己打去問</li>
                <li><strong>考慮寬頻+手機組合：</strong>部分供應商有「全家Plan」，一齊出可以慳更多</li>
            </ul>
            <div class="tip-box"><strong>💡 Tips：</strong>好多供應商有長者優惠（65歲以上），記得問！CMHK中國移動同HKBN都有相關計劃。</div>
            """),
            ("Router設定懶人包：一次搞掂", """
            <p>幫長者設定好以下嘢，之後佢哋就唔需要理Router：</p>
            <ul>
                <li><strong>WiFi名稱：</strong>改做簡單易記嘅名（例如「屋企WiFi」），唔好用預設嘅亂碼</li>
                <li><strong>WiFi密碼：</strong>設定簡單但安全嘅密碼（8位數字），印出嚟貼喺Router上</li>
                <li><strong>自動重啟：</strong>部分Router有定時自動重啟功能，設定每周重啟一次，保持穩定</li>
                <li><strong>訪客WiFi：</strong>可以唔開，減少長者困惑</li>
                <li><strong>QR Code連WiFi：</strong>去 qifi.org 生成WiFi QR Code，印出嚟，有客人嚟掃一掃就連到</li>
            </ul>
            """),
            ("防詐騙設定：保護長者上網安全", """
            <p>網絡詐騙係長者最大嘅威脅。以下設定可以大幅減低風險：</p>
            <ul>
                <li><strong>DNS過濾：</strong>將Router嘅DNS改為 CleanBrowsing（185.228.168.9），自動攔截釣魚網站</li>
                <li><strong>廣告攔截：</strong>喺長者手機安裝 Firefox + uBlock Origin，阻擋惡意廣告</li>
                <li><strong>來電過濾：</strong>開啟手機嘅「來電過濾」功能，攔截詐騙電話</li>
                <li><strong>定下規矩：</strong>同長者講清楚「任何叫你俾錢、俾密碼、裝App嘅，100%係騙人」</li>
                <li><strong>定期檢查：</strong>每個月幫長者檢查手機一次，睇下有冇裝到奇怪App</li>
            </ul>
            <div class="tip-box"><strong>⚠ 重要：</strong>將你嘅電話號碼設為長者手機嘅緊急聯絡人。教佢哋遇到任何可疑訊息，第一時間打俾你。</div>
            """)
        ]
    },
    {
        "slug": "broadband-for-youtubers",
        "title": "做YouTuber/直播主需要幾快寬頻？上傳速度、直播設定全攻略",
        "description": "想做YouTube、Twitch直播？上傳速度幾多先夠？OBS設定點調？YouTuber寬頻需求全面解析。",
        "keywords": "YouTuber寬頻, 直播寬頻, 上傳速度, OBS設定, Twitch直播, YouTube上傳, 串流寬頻需求",
        "category": "trending",
        "cat_class": "cat-trending",
        "cat_name": "熱門話題",
        "card_desc": "想做YouTube、Twitch直播？上傳速度幾多先夠？直播設定全攻略。",
        "faqs": [
            ("做YouTube需要幾快嘅上傳速度？", "上傳已剪輯好嘅影片，其實10Mbps上傳已經夠用，只係要等耐啲。但如果做直播，建議上傳速度至少20Mbps以上（720p直播需要約5Mbps，1080p需要約10Mbps，4K需要約35Mbps）。香港大部分光纖寬頻嘅上傳速度同下載一樣，所以100M以上基本冇問題。"),
            ("直播會唔會影響屋企其他人上網？", "會！直播需要持續佔用上傳頻寬。如果你用100M寬頻直播1080p（佔用約10M上傳），屋企其他人嘅上傳速度會受影響（例如視像通話可能會卡）。建議直播主至少用500M寬頻，或者喺Router設定QoS優先保障直播嘅頻寬。"),
            ("用WiFi直播定LAN線好？", "一定要用LAN線！WiFi嘅延遲同速度會波動，直播時一旦WiFi訊號波動就會掉幀甚至斷線。專業直播主100%用LAN線連接電腦。如果電腦冇LAN口，買個USB轉LAN適配器（$50-100）。")
        ],
        "sections": [
            ("唔同平台嘅寬頻需求", """
            <table class="comparison-table">
                <tr><th>平台/用途</th><th>最低上傳速度</th><th>建議上傳速度</th><th>建議寬頻</th></tr>
                <tr><td>YouTube 上傳影片</td><td>5 Mbps</td><td>20+ Mbps</td><td>100M</td></tr>
                <tr><td>YouTube 直播 720p</td><td>5 Mbps</td><td>10 Mbps</td><td>100M</td></tr>
                <tr><td>YouTube 直播 1080p</td><td>10 Mbps</td><td>20 Mbps</td><td>500M</td></tr>
                <tr><td>Twitch 直播</td><td>6 Mbps</td><td>15 Mbps</td><td>500M</td></tr>
                <tr><td>Facebook Live</td><td>4 Mbps</td><td>10 Mbps</td><td>100M</td></tr>
                <tr><td>IG Live</td><td>3 Mbps</td><td>8 Mbps</td><td>100M</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>直播+打機+屋企人用</td><td>30 Mbps</td><td>50+ Mbps</td><td>1000M</td></tr>
            </table>
            """),
            ("上傳時間計算器", """
            <p>影片上傳到YouTube要幾耐？以下係實際參考：</p>
            <table class="comparison-table">
                <tr><th>影片大小</th><th>100M寬頻</th><th>500M寬頻</th><th>1000M寬頻</th></tr>
                <tr><td>1GB（10分鐘1080p）</td><td>1.5分鐘</td><td>16秒</td><td>8秒</td></tr>
                <tr><td>5GB（30分鐘4K）</td><td>7分鐘</td><td>1.3分鐘</td><td>40秒</td></tr>
                <tr><td>20GB（1小時4K）</td><td>28分鐘</td><td>5.3分鐘</td><td>2.7分鐘</td></tr>
                <tr><td>50GB（長片4K）</td><td>70分鐘</td><td>14分鐘</td><td>7分鐘</td></tr>
            </table>
            <div class="tip-box"><strong>💡 Tips：</strong>YouTube上傳速度仲受YouTube伺服器限制，通常唔會用盡你嘅寬頻。實際上傳時間可能比上面多20-50%。</div>
            """),
            ("直播OBS最佳設定", """
            <p>用OBS直播時，正確嘅設定可以確保畫質流暢：</p>
            <h3>1080p 直播建議設定：</h3>
            <ul>
                <li><strong>輸出解像度：</strong>1920x1080</li>
                <li><strong>幀率：</strong>30fps（打機直播可用60fps）</li>
                <li><strong>Bitrate：</strong>4,500-6,000 Kbps</li>
                <li><strong>編碼器：</strong>NVENC（有Nvidia顯卡）或 x264</li>
                <li><strong>關鍵幀間隔：</strong>2秒</li>
            </ul>
            <h3>720p 直播建議設定（網速較慢時）：</h3>
            <ul>
                <li><strong>輸出解像度：</strong>1280x720</li>
                <li><strong>幀率：</strong>30fps</li>
                <li><strong>Bitrate：</strong>2,500-4,000 Kbps</li>
            </ul>
            <div class="tip-box"><strong>⚠ 注意：</strong>直播前記得用 <a href="https://broadbandhk.com/speed-test.html" style="color:var(--primary)">BroadbandHK 測速工具</a> 測試你嘅上傳速度。Bitrate唔好超過上傳速度嘅70%，留啲buffer確保穩定。</div>
            """),
            ("直播主嘅網絡優化清單", """
            <p>做直播前，跟住呢個Checklist確保網絡穩定：</p>
            <ul>
                <li>✅ 用<strong>LAN線</strong>連接電腦（唔好用WiFi）</li>
                <li>✅ 關閉電腦上所有<strong>雲端同步</strong>（Google Drive、Dropbox、OneDrive）</li>
                <li>✅ 請屋企人暫時<strong>唔好下載大型檔案</strong></li>
                <li>✅ 喺Router設定<strong>QoS</strong>，優先保障你部電腦嘅頻寬</li>
                <li>✅ 直播前30分鐘做一次<strong>速度測試</strong></li>
                <li>✅ 準備<strong>手機熱點</strong>做備用網絡（萬一寬頻斷線）</li>
                <li>✅ OBS設定<strong>自動重連</strong>功能（Settings > Advanced > Auto Reconnect）</li>
            </ul>
            """)
        ]
    },
    {
        "slug": "broadband-moving-checklist-2026",
        "title": "2026搬屋寬頻完整Checklist：搬屋前中後要做嘅15件事",
        "description": "搬屋要轉寬頻？由取消舊合約到新屋裝機，15個步驟幫你搬屋寬頻無縫過渡，唔會斷網。",
        "keywords": "搬屋寬頻, 搬屋轉寬頻, 搬屋上網, 寬頻搬遷, 搬屋checklist, 新屋裝寬頻",
        "category": "saving",
        "cat_class": "cat-saving",
        "cat_name": "慳錢攻略",
        "card_desc": "搬屋要轉寬頻？15個步驟幫你無縫過渡，由舊屋到新屋唔會斷網。",
        "faqs": [
            ("搬屋一定要轉寬頻供應商？", "唔一定。大部分供應商都提供「搬遷服務」，可以將現有合約搬去新地址。但要注意：(1)新地址要有該供應商嘅覆蓋；(2)搬遷可能有費用（$200-500）；(3)如果新地址嘅月費較高，可能要補差價。建議先問現有供應商嘅搬遷條件，再比較轉台嘅價錢。"),
            ("搬屋前幾耐要安排寬頻？", "建議搬屋前3-4周開始安排。步驟：(1)確認新地址嘅覆蓋同價錢；(2)預約搬入日前1-2日安裝；(3)搬屋日當日就有網用。旺季（暑假6-8月）安裝排期可能要等1-2周，更加要提早安排。"),
            ("搬屋期間冇網用點算？", "可以用手機開熱點暫時用住。如果需要穩定網絡（在家工作），可以租用流動WiFi蛋（日租$30-50）。另外，部分供應商可以安排舊屋同新屋嘅服務有幾日重疊，確保唔斷網。")
        ],
        "sections": [
            ("搬屋前4周：準備階段", """
            <p>提早準備可以避免搬屋後冇網用嘅窘境：</p>
            <ul>
                <li><strong>Step 1：</strong>查新地址嘅寬頻覆蓋 — 用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK 格價計算器</a> 查邊間有覆蓋</li>
                <li><strong>Step 2：</strong>聯絡現有供應商問搬遷條件（費用、是否有覆蓋、月費變動）</li>
                <li><strong>Step 3：</strong>格價！搬屋係轉台嘅最佳時機，因為你可以用「新客優惠」</li>
                <li><strong>Step 4：</strong>決定搬遷定轉台，盡早預約安裝日期</li>
                <li><strong>Step 5：</strong>確認現有合約嘅提早終止費（如有），計算轉台是否更著數</li>
            </ul>
            """),
            ("搬屋前1周：確認階段", """
            <ul>
                <li><strong>Step 6：</strong>確認新屋安裝日期同時間</li>
                <li><strong>Step 7：</strong>準備一條長LAN線（5-10米），方便技師測試</li>
                <li><strong>Step 8：</strong>記低你現有Router嘅WiFi名稱同密碼，新屋設定返一樣嘅名同密碼，所有裝置就會自動連接</li>
                <li><strong>Step 9：</strong>將現有Router嘅特殊設定截圖保存（Port Forward、DHCP、DNS等）</li>
            </ul>
            <div class="tip-box"><strong>💡 Pro Tip：</strong>喺新屋設定同舊屋一模一樣嘅WiFi名稱同密碼，所有手機、電腦、智能家居裝置都會自動連接，唔使逐個重新設定！</div>
            """),
            ("搬屋當日：安裝階段", """
            <ul>
                <li><strong>Step 10：</strong>確保有人喺新屋等技師上門</li>
                <li><strong>Step 11：</strong>叫技師將光纖入線拉到你想放Router嘅位置</li>
                <li><strong>Step 12：</strong>安裝完即場測速，確認速度正常（用LAN線測試）</li>
                <li><strong>Step 13：</strong>設定WiFi（用返舊屋嘅名同密碼）</li>
            </ul>
            """),
            ("搬屋後1周：善後階段", """
            <ul>
                <li><strong>Step 14：</strong>取消或確認舊屋嘅寬頻服務已終止（避免被雙重收費）</li>
                <li><strong>Step 15：</strong>歸還舊Router（如果係租用嘅，逾期歸還可能會被收$500-1000）</li>
            </ul>
            <table class="comparison-table">
                <tr><th>注意事項</th><th>詳情</th></tr>
                <tr><td>舊合約罰款</td><td>提早終止通常要賠剩餘月費嘅50%</td></tr>
                <tr><td>搬遷費</td><td>$0-$500（睇供應商同距離）</td></tr>
                <tr><td>新裝費</td><td>$0-$680（新客通常免費）</td></tr>
                <tr><td>Router歸還</td><td>30日內歸還，逾期罰$500-1000</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>慳錢秘技</td><td>合約到期前搬屋 = 最佳轉台時機，零罰款+新客優惠</td></tr>
            </table>
            """)
        ]
    },
    {
        "slug": "hong-kong-broadband-providers-comparison",
        "title": "2026年香港6大寬頻供應商全面比較：邊間最平？邊間最快？邊間最穩？",
        "description": "HKBN、HGC、CMHK、SmarTone、PCCW、i-Cable 六大供應商逐間比較，價錢、速度、覆蓋、客服全面評分。",
        "keywords": "香港寬頻比較, 寬頻供應商, HKBN, HGC, CMHK, SmarTone, PCCW, i-Cable, 寬頻邊間好, 最平寬頻",
        "category": "trending",
        "cat_class": "cat-trending",
        "cat_name": "熱門話題",
        "card_desc": "六大供應商逐間比較：價錢、速度、覆蓋、客服全面評分，幫你揀最啱嘅一間。",
        "faqs": [
            ("香港邊間寬頻最平？", "以2026年市場價計，CMHK中國移動通常提供最低月費，1000M可以低至$108/月。但「最平」唔一定係「最抵」，要考慮覆蓋範圍、穩定性同客服質素。建議用BroadbandHK格價計算器按你嘅地址比較實際可用嘅方案。"),
            ("HKBN同HGC邊間好？", "兩間都係香港主要光纖供應商，各有優勢。HKBN覆蓋較廣（特別係住宅區）、品牌知名度高；HGC係全港最大光纖網絡商，backbone網絡質素好，價錢通常較HKBN平少少。如果兩間都有覆蓋你嘅大廈，建議比較實際報價再決定。"),
            ("寬頻穩唔穩定點樣睇？", "可以參考：(1)供應商嘅SLA（服務水平協議），承諾幾多%正常運作時間；(2)用戶評價（連登、Facebook群組）；(3)你大廈嘅鄰居用緊邊間。同一供應商喺唔同大廈嘅表現可以差好遠，因為取決於大廈嘅線路質素。")
        ],
        "sections": [
            ("六大供應商一覽表", """
            <table class="comparison-table">
                <tr><th>供應商</th><th>1000M月費</th><th>覆蓋率</th><th>網絡類型</th><th>適合</th></tr>
                <tr><td><strong>HKBN 香港寬頻</strong></td><td>$158起</td><td>★★★★☆</td><td>FTTH/FTTB</td><td>一般家庭</td></tr>
                <tr><td><strong>HGC 環電</strong></td><td>$148起</td><td>★★★★★</td><td>FTTH</td><td>追求穩定</td></tr>
                <tr><td><strong>CMHK 中國移動</strong></td><td>$108起</td><td>★★★☆☆</td><td>FTTH/FTTB</td><td>慳錢首選</td></tr>
                <tr><td><strong>SmarTone</strong></td><td>$168起</td><td>★★★☆☆</td><td>FTTH</td><td>手機+寬頻組合</td></tr>
                <tr><td><strong>PCCW/網上行</strong></td><td>$178起</td><td>★★★★★</td><td>FTTH/FTTB</td><td>要求最廣覆蓋</td></tr>
                <tr><td><strong>i-Cable 有線</strong></td><td>$128起</td><td>★★☆☆☆</td><td>HFC/FTTH</td><td>特定屋苑</td></tr>
            </table>
            <p><em>*價錢為2026年Q1新客參考價，實際因地區、合約期而異</em></p>
            """),
            ("逐間供應商深度分析", """
            <h3>HKBN 香港寬頻</h3>
            <p><strong>優點：</strong>覆蓋廣、客服中心多、有門市可以當面傾。品牌知名度高，服務相對穩定。</p>
            <p><strong>缺點：</strong>價錢偏貴、合約條款較嚴格、續約價同新客價差距大。</p>
            <p><strong>適合：</strong>唔想煩、想搵間大品牌嘅用戶。</p>

            <h3>HGC 環電（和記環球電訊）</h3>
            <p><strong>優點：</strong>全港最大光纖網絡、backbone質素高、企業級網絡穩定性、價錢合理。</p>
            <p><strong>缺點：</strong>品牌認知度較低、門市較少。</p>
            <p><strong>適合：</strong>追求網絡穩定性、在家工作用戶。</p>

            <h3>CMHK 中國移動香港</h3>
            <p><strong>優點：</strong>價錢最平、經常有超值促銷、手機+寬頻組合優惠多。</p>
            <p><strong>缺點：</strong>覆蓋範圍較細（主要大型屋苑）、部分地區只有FTTB。</p>
            <p><strong>適合：</strong>預算有限、追求最低月費嘅用戶。</p>

            <h3>SmarTone</h3>
            <p><strong>優點：</strong>手機+寬頻組合折扣大、服務態度好、網絡質素不錯。</p>
            <p><strong>缺點：</strong>純寬頻價錢偏貴、覆蓋範圍一般。</p>
            <p><strong>適合：</strong>已經用SmarTone手機、想一齊出享折扣嘅用戶。</p>

            <h3>PCCW/網上行</h3>
            <p><strong>優點：</strong>覆蓋最廣（前電訊盈科）、幾乎全港都有、技術支援完善。</p>
            <p><strong>缺點：</strong>最貴、合約條款複雜、客服等候時間長。</p>
            <p><strong>適合：</strong>其他供應商冇覆蓋嘅地區、或者要求最穩定服務嘅用戶。</p>
            """),
            ("2026年揀供應商嘅建議", """
            <div class="tip-box"><strong>揀供應商4步曲：</strong><br>
            1️⃣ 用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK 格價計算器</a> 查你地址有邊間覆蓋<br>
            2️⃣ 比較有覆蓋嘅供應商嘅<strong>新客價</strong>（唔好睇官網定價）<br>
            3️⃣ 問你大廈嘅鄰居用緊邊間、穩唔穩定<br>
            4️⃣ 確認係<strong>FTTH（光纖到戶）</strong>定FTTB（光纖到樓），前者更好</div>
            """)
        ]
    },
    {
        "slug": "smart-tv-broadband-guide",
        "title": "Smart TV上網全攻略：Netflix、Disney+、YouTube需要幾多M寬頻？",
        "description": "Smart TV 上網點設定？串流平台需要幾多網速？4K HDR要幾快？全面Smart TV寬頻指南。",
        "keywords": "Smart TV上網, 電視寬頻, Netflix網速, Disney Plus網速, 4K串流, Smart TV WiFi, 串流速度需求",
        "category": "beginner",
        "cat_class": "cat-beginner",
        "cat_name": "新手入門",
        "card_desc": "Netflix、Disney+、YouTube需要幾多M？Smart TV上網設定同串流優化全攻略。",
        "faqs": [
            ("Smart TV用WiFi定LAN線好？", "如果可以拉LAN線，一定用LAN線 — 更穩定、唔會buffering。但如果Router離電視太遠，WiFi 5GHz都夠用（前提係中間唔好隔太多牆）。如果WiFi信號弱，考慮用Powerline或者Mesh WiFi延伸到電視附近。"),
            ("幾多M寬頻先夠睇4K Netflix？", "Netflix 4K建議至少25Mbps穩定連接。所以100M寬頻1-2人睇4K係夠嘅。但如果同時有人打機或下載，建議用500M。Disney+嘅4K需要約25Mbps，YouTube 4K需要約20Mbps。"),
            ("Smart TV WiFi成日斷線點算？", "常見原因：(1)Router太遠，5GHz訊號穿唔到牆；(2)電視WiFi模組較弱（比手機差）；(3)IP衝突。解決方法：將電視改用2.4GHz WiFi（穿牆力較強）、或者用Powerline/LAN線直接連接。")
        ],
        "sections": [
            ("各串流平台速度需求", """
            <table class="comparison-table">
                <tr><th>平台</th><th>SD標清</th><th>HD高清</th><th>4K Ultra HD</th><th>4K HDR</th></tr>
                <tr><td>Netflix</td><td>1 Mbps</td><td>5 Mbps</td><td>15 Mbps</td><td>25 Mbps</td></tr>
                <tr><td>Disney+</td><td>—</td><td>5 Mbps</td><td>25 Mbps</td><td>25 Mbps</td></tr>
                <tr><td>YouTube</td><td>1 Mbps</td><td>5 Mbps</td><td>20 Mbps</td><td>—</td></tr>
                <tr><td>Apple TV+</td><td>—</td><td>8 Mbps</td><td>25 Mbps</td><td>25 Mbps</td></tr>
                <tr><td>Viu / myTV</td><td>2 Mbps</td><td>5 Mbps</td><td>—</td><td>—</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>多人同時睇</td><td colspan="4">每人用緊嘅速度 × 人數 = 你需要嘅總速度</td></tr>
            </table>
            <div class="tip-box"><strong>💡 計算例子：</strong>2部電視同時睇Netflix 4K（25×2=50Mbps）+ 1個人打機（10Mbps）+ 1個人視像通話（5Mbps）= 需要65Mbps。100M寬頻剛剛夠，建議用500M更穩妥。</div>
            """),
            ("Smart TV WiFi設定優化", """
            <p>大部分Smart TV嘅WiFi接收能力比手機弱。以下設定可以改善串流體驗：</p>
            <ul>
                <li><strong>優先用5GHz：</strong>喺WiFi設定揀5GHz網絡（通常名字有「5G」字尾）</li>
                <li><strong>固定IP：</strong>喺Router入面為電視設定固定IP，避免IP衝突導致斷線</li>
                <li><strong>DNS設定：</strong>改用Google DNS（8.8.8.8）或Cloudflare DNS（1.1.1.1），可以加快串流連接速度</li>
                <li><strong>關閉快速啟動：</strong>部分電視嘅「快速啟動」功能會導致WiFi不穩定，關閉後會改善</li>
                <li><strong>定期重啟：</strong>每周重啟電視同Router一次，清除記憶體</li>
            </ul>
            """),
            ("唔同寬頻速度嘅串流體驗", """
            <table class="comparison-table">
                <tr><th>寬頻速度</th><th>可以做到</th><th>做唔到</th></tr>
                <tr><td><strong>100M</strong></td><td>1-2人同時4K串流、基本上網</td><td>多人同時4K + 打機</td></tr>
                <tr><td><strong>500M</strong></td><td>3-4人同時4K、同時下載、打機</td><td>好多人同時直播</td></tr>
                <tr><td><strong>1000M</strong></td><td>全家暢用、乜都得</td><td>基本上冇限制</td></tr>
            </table>
            """)
        ]
    },
    {
        "slug": "broadband-scam-prevention",
        "title": "小心寬頻銷售陷阱！7種常見手法同防騙指南",
        "description": "街頭推銷、電話促銷、虛假優惠⋯⋯教你識破7種寬頻銷售陷阱，簽約前必讀。",
        "keywords": "寬頻陷阱, 寬頻推銷, 寬頻詐騙, 寬頻合約陷阱, 寬頻隱藏費用, 寬頻銷售手法",
        "category": "saving",
        "cat_class": "cat-saving",
        "cat_name": "慳錢攻略",
        "card_desc": "街頭推銷、電話促銷、虛假優惠⋯⋯7種寬頻銷售陷阱大拆解，簽約前必讀！",
        "faqs": [
            ("街頭寬頻推銷可唔可信？", "唔係所有街頭推銷都係騙人，但要非常小心。常見問題包括：口頭承諾同合約內容唔同、隱藏月費、綁定唔需要嘅服務。建議喺街頭攞咗報價後，返屋企上網核實，唔好即場簽約。"),
            ("簽咗合約先發現被騙點算？", "根據香港法例，消費者有7日冷靜期（適用於上門或電話銷售）。喺冷靜期內可以免費取消。如果過咗冷靜期，可以向通訊事務管理局投訴，或者去消委會求助。"),
            ("點樣分辨真正嘅優惠？", "真正嘅優惠會白紙黑字寫清楚所有費用。如果推銷員避免回答「總共要俾幾多錢」、唔肯俾你帶合約走慢慢睇、或者催你「今日簽先有呢個價」，大機率有陷阱。")
        ],
        "sections": [
            ("陷阱1：「月費$78」嘅真相", """
            <p>你可能見過「極速寬頻月費只需$78！」嘅廣告。但實際上：</p>
            <ul>
                <li>$78只係<strong>頭6個月嘅優惠價</strong>，之後恢復$198/月</li>
                <li>或者$78係<strong>扣除所有回贈後嘅「平均月費」</strong>，實際每月要先俾$178</li>
                <li>或者$78係100M速度，你以為係1000M</li>
            </ul>
            <div class="tip-box"><strong>⚠ 自保方法：</strong>永遠問清楚「24個月合約總共要俾幾多錢？」呢個數字先係真正嘅成本。用總金額÷24個月 = 真實平均月費。</div>
            """),
            ("陷阱2：免費Router嘅隱藏成本", """
            <p>「免費送Router」聽落好吸引，但：</p>
            <ul>
                <li>大部分係<strong>租用</strong>唔係送：合約結束後要歸還，逾期歸還罰$500-1000</li>
                <li>送嘅Router通常係<strong>最低檔</strong>嘅型號，只支援WiFi 5，跑唔到你付費嘅1000M速度</li>
                <li>部分供應商會喺月費入面<strong>暗加$38-58 Router租費</strong></li>
            </ul>
            <p><strong>建議：</strong>自己買一部WiFi 6 Router（$300-500），長遠更抵用、速度更快。</p>
            """),
            ("陷阱3-7：更多常見手法", """
            <h3>陷阱3：自動續約條款</h3>
            <p>合約到期後自動轉為按月收費（通常貴20-50%），而且你唔主動取消就會一直收。</p>

            <h3>陷阱4：綁定增值服務</h3>
            <p>「免費試用3個月OTT串流服務」— 但3個月後自動收費$68/月，你可能忘記取消。</p>

            <h3>陷阱5：虛假網速</h3>
            <p>推銷「2000M」計劃，但2000M只係理論最高速度，實際上WiFi永遠跑唔到。唔好為虛標速度支付溢價。</p>

            <h3>陷阱6：電話冷call壓力銷售</h3>
            <p>「呢個優惠今日最後一日！」— 基本上永遠唔會係最後一日。如果真係好Deal，聽日都仲有。</p>

            <h3>陷阱7：安裝後加收費用</h3>
            <p>安裝時先話你知「你嘅大廈需要特別拉線，要加收$1000」。簽約前一定要確認所有安裝費用。</p>
            """),
            ("簽約前必問清單", """
            <p>喺簽任何寬頻合約之前，一定要問清楚以下問題：</p>
            <ul>
                <li>✅ 24個月合約<strong>總共要俾幾多錢</strong>？（唔好聽月費，要聽總數）</li>
                <li>✅ 安裝費幾多？有冇額外拉線費用？</li>
                <li>✅ Router係<strong>送定租</strong>？租嘅話月費幾多？</li>
                <li>✅ 有冇綁定其他服務？幾時開始收費？</li>
                <li>✅ 合約到期後月費會點？</li>
                <li>✅ 提早終止合約嘅罰款幾多？</li>
                <li>✅ 係FTTH（光纖到戶）定FTTB（光纖到樓）？</li>
                <li>✅ 可唔可以攞份合約副本返屋企睇清楚先簽？</li>
            </ul>
            """)
        ]
    }
]


def get_published():
    """讀取已發佈嘅文章列表"""
    if os.path.exists(PUBLISHED_LOG):
        with open(PUBLISHED_LOG, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_published(published):
    with open(PUBLISHED_LOG, "w", encoding="utf-8") as f:
        json.dump(published, f, ensure_ascii=False, indent=2)


def generate_html(article):
    """生成完整 HTML 頁面"""
    slug = article["slug"]
    title = article["title"]
    desc = article["description"]
    keywords = article["keywords"]

    # FAQ Schema
    faq_items = ""
    for i, (q, a) in enumerate(article["faqs"]):
        comma = "," if i < len(article["faqs"]) - 1 else ""
        faq_items += f"""
            {{
                "@type": "Question",
                "name": "{q}",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "{a}"
                }}
            }}{comma}"""

    # 文章內容
    sections_html = ""
    for heading, content in article["sections"]:
        sections_html += f"""
        <h2>{heading}</h2>
        {content}
        """

    # FAQ 顯示區
    faq_display = ""
    for q, a in article["faqs"]:
        faq_display += f"""
        <div style="margin-bottom:20px;">
            <h3 style="margin-bottom:8px;">{q}</h3>
            <p>{a}</p>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — BroadbandHK 知識庫</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{SITE_URL}/kb/{slug}.html">

    <script async src="https://www.googletagmanager.com/gtag/js?id=G-23EZE5P385"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-23EZE5P385');
    </script>

    <meta property="og:type" content="article">
    <meta property="og:url" content="{SITE_URL}/kb/{slug}.html">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{SITE_URL}/og-image.png">
    <meta property="og:locale" content="zh_HK">
    <meta property="og:site_name" content="BroadbandHK 寬頻格價比較">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{SITE_URL}/og-image.png">

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "datePublished": "{DATE_STR}",
        "dateModified": "{DATE_STR}",
        "author": {{"@type": "Organization", "name": "BroadbandHK 寬頻格價比較"}},
        "publisher": {{"@type": "Organization", "name": "BroadbandHK 寬頻格價比較"}},
        "mainEntityOfPage": {{"@type": "WebPage", "@id": "{SITE_URL}/kb/{slug}.html"}}
    }}
    </script>

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{faq_items}
        ]
    }}
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../style.css">
    <style>
        .kb-hero {{ padding: 140px 0 60px; text-align: center; background: linear-gradient(135deg, var(--primary-light) 0%, var(--white) 60%); }}
        .kb-hero h1 {{ font-size: 2.5rem; font-weight: 900; margin-bottom: 12px; }}
        .kb-hero p {{ font-size: 1.1rem; color: var(--gray); }}
        .kb-breadcrumb {{ padding: 20px 0 0; font-size: 0.9rem; color: var(--gray); }}
        .kb-breadcrumb a {{ color: var(--primary); text-decoration: none; }}
        .kb-content {{ padding: 60px 0; }}
        .kb-article {{ background: var(--white); border-radius: var(--radius); padding: 48px; margin-bottom: 40px; box-shadow: var(--shadow); max-width: 800px; margin: 0 auto; }}
        .kb-article h2 {{ font-size: 1.6rem; font-weight: 900; margin: 32px 0 16px; color: var(--dark); }}
        .kb-article h3 {{ font-size: 1.3rem; font-weight: 700; margin: 28px 0 12px; color: var(--dark); }}
        .kb-article p {{ color: var(--gray); font-size: 1rem; line-height: 1.9; margin-bottom: 16px; }}
        .kb-article ul {{ margin: 16px 0; padding-left: 24px; }}
        .kb-article li {{ color: var(--gray); margin-bottom: 8px; line-height: 1.8; }}
        .kb-date {{ color: var(--gray); font-size: 0.85rem; margin-bottom: 20px; }}
        .tip-box {{ background: #fef3c7; border-left: 4px solid var(--accent); padding: 20px 24px; border-radius: 0 8px 8px 0; margin: 24px 0; }}
        .tip-box strong {{ color: var(--dark); }}
        .comparison-table {{ width: 100%; border-collapse: collapse; margin: 24px 0; }}
        .comparison-table th, .comparison-table td {{ padding: 14px 16px; text-align: center; border-bottom: 1px solid #e2e8f0; font-size: 0.95rem; }}
        .comparison-table th {{ background: var(--primary); color: var(--white); font-weight: 700; }}
        .comparison-table tr:hover {{ background: #f8fafc; }}
        .related-links {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 30px; }}
        .related-links a {{ background: var(--primary-light); color: var(--primary); padding: 8px 16px; border-radius: 20px; text-decoration: none; font-size: 0.9rem; font-weight: 600; }}
        .cta-box {{ background: linear-gradient(135deg, var(--primary), #2563eb); color: white; padding: 30px; border-radius: 12px; text-align: center; margin: 40px 0; }}
        .cta-box a {{ color: white; background: #25D366; padding: 12px 30px; border-radius: 24px; text-decoration: none; font-weight: 700; display: inline-block; margin-top: 12px; }}
        @media (max-width: 768px) {{
            .kb-hero h1 {{ font-size: 1.6rem; }}
            .kb-article {{ padding: 24px 16px; }}
            .comparison-table {{ font-size: 0.8rem; }}
            .comparison-table th, .comparison-table td {{ padding: 8px 6px; }}
        }}
    </style>
</head>
<body>
    <section class="kb-hero">
        <div class="container">
            <div class="kb-breadcrumb"><a href="../index.html">主頁</a> &gt; <a href="../blog.html">知識庫</a> &gt; {title.split("：")[0] if "：" in title else title[:20]}</div>
            <h1>{title}</h1>
            <p>{desc}</p>
        </div>
    </section>

    <section class="kb-content">
        <div class="container">
            <article class="kb-article">
                <p class="kb-date">{DATE_DISPLAY} · BroadbandHK 編輯部</p>
                {sections_html}

                <h2>常見問題 FAQ</h2>
                {faq_display}

                <div class="cta-box">
                    <h3>想搵最適合你嘅寬頻Plan？</h3>
                    <p>用我哋嘅免費格價計算器，即刻比較各大供應商最新優惠！</p>
                    <a href="../calculator.html">免費格價比較 →</a>
                </div>

                <div class="related-links">
                    <a href="../blog.html">← 返回知識庫</a>
                    <a href="../calculator.html">格價計算器</a>
                    <a href="../speed-test.html">速度測試</a>
                </div>
            </article>
        </div>
    </section>
</body>
</html>"""

    return html


def update_blog_html(article):
    """將新文章加到 blog.html"""
    if not os.path.exists(BLOG_FILE):
        print(f"  WARNING: {BLOG_FILE} not found")
        return

    with open(BLOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    slug = article["slug"]
    cat_class = article["cat_class"]
    cat_name = article["cat_name"]
    card_desc = article["card_desc"]
    title = article["title"]

    # 檢查是否已經加過
    if slug in content:
        print(f"  Already in blog.html, skipping")
        return

    # 搵對應嘅 section
    category_map = {
        "trending": "trending",
        "beginner": "beginner",
        "saving": "saving",
        "tech": "tech",
        "district": "district"
    }
    section_id = category_map.get(article["category"], "trending")

    # 喺對應 section 嘅 article-grid 後面加新卡片
    marker = f'id="{section_id}">'
    if marker in content:
        # 搵到 article-grid 嘅開頭
        grid_marker = content.find('<div class="article-grid">', content.find(marker))
        if grid_marker > 0:
            insert_pos = grid_marker + len('<div class="article-grid">') + 1
            new_card = f"""
            <a href="kb/{slug}.html" class="article-card">
                <span class="card-category {cat_class}">{cat_name}</span>
                <h3>{title}</h3>
                <p>{card_desc}</p>
                <span class="card-date">{DATE_DISPLAY}</span>
            </a>"""
            content = content[:insert_pos] + new_card + content[insert_pos:]

            with open(BLOG_FILE, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Added to blog.html ({section_id} section)")


def update_sitemap(slug):
    """將新文章加到 sitemap"""
    # 搵最新嘅 sitemap 檔案
    sitemap_files = sorted([f for f in os.listdir(SITEMAP_DIR) if re.match(r"sitemap-\d+\.xml", f)])
    if not sitemap_files:
        print("  WARNING: No sitemap files found")
        return

    latest_sitemap = os.path.join(SITEMAP_DIR, sitemap_files[-1])
    url_entry = f"{SITE_URL}/kb/{slug}.html"

    with open(latest_sitemap, "r", encoding="utf-8") as f:
        content = f.read()

    if url_entry in content:
        print(f"  Already in sitemap")
        return

    new_entry = f"""  <url>
    <loc>{url_entry}</loc>
    <lastmod>{DATE_STR}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""

    content = content.replace("</urlset>", new_entry)

    with open(latest_sitemap, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Added to {sitemap_files[-1]}")


def main():
    print("=" * 60)
    print("Auto Article Generator")
    print(f"Date: {DATE_STR}")
    print("=" * 60)

    published = get_published()
    published_slugs = [p["slug"] for p in published]

    # 搵出未發佈嘅文章
    unpublished = [a for a in ARTICLE_TEMPLATES if a["slug"] not in published_slugs]

    if not unpublished:
        print("All articles have been published! Add more templates to continue.")
        return

    # 每次發佈 1 篇
    article = unpublished[0]
    slug = article["slug"]
    print(f"\nPublishing: {article['title']}")

    # 檢查是否已存在
    filepath = os.path.join(KB_DIR, f"{slug}.html")
    if os.path.exists(filepath):
        print(f"  File already exists: {filepath}")
    else:
        # 生成 HTML
        html = generate_html(article)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Created: kb/{slug}.html")

    # 更新 blog.html
    update_blog_html(article)

    # 更新 sitemap
    update_sitemap(slug)

    # 記錄已發佈
    published.append({
        "slug": slug,
        "title": article["title"],
        "date": DATE_STR
    })
    save_published(published)

    print(f"\nDone! Published 1 article.")
    print(f"Remaining in queue: {len(unpublished) - 1}")


if __name__ == "__main__":
    main()
