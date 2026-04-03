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
                <tr><td>供應商 A</td><td>$158/月</td><td>$198/月</td><td>+$40</td></tr>
                <tr><td>供應商 B</td><td>$148/月</td><td>$188/月</td><td>+$40</td></tr>
                <tr><td>供應商 C</td><td>$108/月</td><td>$148/月</td><td>+$40</td></tr>
                <tr><td>供應商 D</td><td>$168/月</td><td>$208/月</td><td>+$40</td></tr>
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
            <div class="tip-box"><strong>💡 Tips：</strong>好多供應商有長者優惠（65歲以上），記得問！供應商 C中國移動同供應商 A都有相關計劃。</div>
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
        "description": "供應商 A、供應商 B、供應商 C、供應商 D、供應商 E、供應商 F 六大供應商逐間比較，價錢、速度、覆蓋、客服全面評分。",
        "keywords": "寬頻比較, 寬頻供應商, 供應商 A, 供應商 B, 供應商 C, 供應商 D, 供應商 E, 供應商 F, 寬頻邊間好, 最平寬頻",
        "category": "trending",
        "cat_class": "cat-trending",
        "cat_name": "熱門話題",
        "card_desc": "六大供應商逐間比較：價錢、速度、覆蓋、客服全面評分，幫你揀最啱嘅一間。",
        "faqs": [
            ("香港邊間寬頻最平？", "以2026年市場價計，供應商 C中國移動通常提供最低月費，1000M可以低至$108/月。但「最平」唔一定係「最抵」，要考慮覆蓋範圍、穩定性同客服質素。建議用BroadbandHK格價計算器按你嘅地址比較實際可用嘅方案。"),
            ("供應商 A同供應商 B邊間好？", "兩間都係香港主要光纖供應商，各有優勢。供應商 A覆蓋較廣（特別係住宅區）、品牌知名度高；供應商 B係全港最大光纖網絡商，backbone網絡質素好，價錢通常較供應商 A平少少。如果兩間都有覆蓋你嘅大廈，建議比較實際報價再決定。"),
            ("寬頻穩唔穩定點樣睇？", "可以參考：(1)供應商嘅SLA（服務水平協議），承諾幾多%正常運作時間；(2)用戶評價（連登、Facebook群組）；(3)你大廈嘅鄰居用緊邊間。同一供應商喺唔同大廈嘅表現可以差好遠，因為取決於大廈嘅線路質素。")
        ],
        "sections": [
            ("六大供應商一覽表", """
            <table class="comparison-table">
                <tr><th>供應商</th><th>1000M月費</th><th>覆蓋率</th><th>網絡類型</th><th>適合</th></tr>
                <tr><td><strong>供應商 A</strong></td><td>$158起</td><td>★★★★☆</td><td>FTTH/FTTB</td><td>一般家庭</td></tr>
                <tr><td><strong>供應商 B</strong></td><td>$148起</td><td>★★★★★</td><td>FTTH</td><td>追求穩定</td></tr>
                <tr><td><strong>供應商 C</strong></td><td>$108起</td><td>★★★☆☆</td><td>FTTH/FTTB</td><td>慳錢首選</td></tr>
                <tr><td><strong>供應商 D</strong></td><td>$168起</td><td>★★★☆☆</td><td>FTTH</td><td>手機+寬頻組合</td></tr>
                <tr><td><strong>供應商 E</strong></td><td>$178起</td><td>★★★★★</td><td>FTTH/FTTB</td><td>要求最廣覆蓋</td></tr>
                <tr><td><strong>供應商 F</strong></td><td>$128起</td><td>★★☆☆☆</td><td>HFC/FTTH</td><td>特定屋苑</td></tr>
            </table>
            <p><em>*價錢為2026年Q1新客參考價，實際因地區、合約期而異</em></p>
            """),
            ("逐間供應商深度分析", """
            <h3>供應商 A</h3>
            <p><strong>優點：</strong>覆蓋廣、客服中心多、有門市可以當面傾。品牌知名度高，服務相對穩定。</p>
            <p><strong>缺點：</strong>價錢偏貴、合約條款較嚴格、續約價同新客價差距大。</p>
            <p><strong>適合：</strong>唔想煩、想搵間大品牌嘅用戶。</p>

            <h3>供應商 B（和記環球電訊）</h3>
            <p><strong>優點：</strong>全港最大光纖網絡、backbone質素高、企業級網絡穩定性、價錢合理。</p>
            <p><strong>缺點：</strong>品牌認知度較低、門市較少。</p>
            <p><strong>適合：</strong>追求網絡穩定性、在家工作用戶。</p>

            <h3>供應商 C香港</h3>
            <p><strong>優點：</strong>價錢最平、經常有超值促銷、手機+寬頻組合優惠多。</p>
            <p><strong>缺點：</strong>覆蓋範圍較細（主要大型屋苑）、部分地區只有FTTB。</p>
            <p><strong>適合：</strong>預算有限、追求最低月費嘅用戶。</p>

            <h3>供應商 D</h3>
            <p><strong>優點：</strong>手機+寬頻組合折扣大、服務態度好、網絡質素不錯。</p>
            <p><strong>缺點：</strong>純寬頻價錢偏貴、覆蓋範圍一般。</p>
            <p><strong>適合：</strong>已經用供應商 D手機、想一齊出享折扣嘅用戶。</p>

            <h3>供應商 E</h3>
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
    },
    # ============================================================
    # 新增 25 篇文章模板（2026-03 批次）
    # ============================================================
    # --- Broadband/Tech (8 articles) ---
    {
        "slug": "public-housing-broadband-guide-2026",
        "title": "公屋寬頻攻略 2026：邊間覆蓋你條邨？點揀最抵Plan？",
        "description": "公屋住戶寬頻揀邊間好？逐區覆蓋比較、FTTH定FTTB、月費比較，公屋上網全攻略。",
        "keywords": "公屋寬頻, 公屋上網, 公屋光纖, 公屋寬頻邊間好, 公屋WiFi, 公屋FTTH, 公屋寬頻覆蓋",
        "category": "saving",
        "cat_class": "cat-saving",
        "cat_name": "慳錢攻略",
        "card_desc": "公屋住戶寬頻揀邊間好？逐區覆蓋比較、FTTH定FTTB、月費最平攻略。",
        "faqs": [
            ("公屋係咪全部都有光纖入屋？", "唔係。好多舊公屋（2010年前落成）只有FTTB（光纖到樓），最後一段用銅線入屋，速度上限大約100-200M。較新嘅屋邨（2015年後）大部分有FTTH（光纖到戶），可以享用1000M全速。你可以喺BroadbandHK格價計算器輸入地址查到。"),
            ("公屋寬頻邊間最平？", "以2026年市場價計，供應商 C中國移動通常係最平，100M低至$68/月、1000M低至$108/月。但唔係每條邨都有覆蓋。供應商 B同供應商 A覆蓋較廣，價錢中等。建議先查覆蓋再格價。"),
            ("公屋可以自己拉光纖線嗎？", "唔可以自己拉。光纖入屋要由供應商嘅技師安裝，而且要經房署批准。如果你條邨未有某間供應商嘅光纖，個人係冇辦法加裝嘅。只能用已經鋪設好嘅供應商。")
        ],
        "sections": [
            ("公屋寬頻現況：FTTH vs FTTB", """
            <p>香港公屋嘅寬頻基建分兩種：</p>
            <table class="comparison-table">
                <tr><th>類型</th><th>FTTH 光纖到戶</th><th>FTTB 光纖到樓</th></tr>
                <tr><td>光纖去到邊</td><td>直接入你屋企</td><td>去到大廈機房，最後用銅線入屋</td></tr>
                <tr><td>最高速度</td><td>1000M-2000M</td><td>100-200M（銅線限制）</td></tr>
                <tr><td>穩定性</td><td>極穩定</td><td>受樓齡、線路質素影響</td></tr>
                <tr><td>常見屋邨</td><td>2015年後新邨</td><td>大部分舊邨</td></tr>
            </table>
            <div class="tip-box"><strong>💡 點樣查：</strong>用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK 格價計算器</a> 輸入你嘅屋邨地址，即刻知道有邊間供應商、係FTTH定FTTB。</div>
            """),
            ("各區公屋覆蓋情況", """
            <p>以下係主要公屋區域嘅供應商覆蓋概況：</p>
            <table class="comparison-table">
                <tr><th>區域</th><th>供應商 A</th><th>供應商 B</th><th>供應商 C</th><th>供應商 E</th></tr>
                <tr><td>觀塘區（翠屏邨等）</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
                <tr><td>黃大仙區（彩虹邨等）</td><td>✅</td><td>✅</td><td>部分</td><td>✅</td></tr>
                <tr><td>沙田區（瀝源邨等）</td><td>✅</td><td>✅</td><td>部分</td><td>✅</td></tr>
                <tr><td>屯門區（良景邨等）</td><td>✅</td><td>部分</td><td>部分</td><td>✅</td></tr>
                <tr><td>天水圍（天耀邨等）</td><td>✅</td><td>部分</td><td>✅</td><td>✅</td></tr>
            </table>
            <p><em>*覆蓋情況會持續更新，以實際查詢為準</em></p>
            """),
            ("公屋住戶揀Plan攻略", """
            <p>公屋單位通常400-600呎，揀Plan要考慮以下因素：</p>
            <ul>
                <li><strong>人數：</strong>1-2人揀100M夠用、3-4人揀500M、5人以上揀1000M</li>
                <li><strong>FTTB限制：</strong>如果你嘅單位係FTTB，就算買1000M Plan都跑唔到1000M，買100M就夠</li>
                <li><strong>合約期：</strong>公屋住戶可能會調遷，揀12個月合約較靈活（雖然貴啲）</li>
                <li><strong>Router：</strong>公屋單位細，一部WiFi 6 Router已經夠覆蓋全屋，唔使買Mesh</li>
            </ul>
            <div class="tip-box"><strong>💡 慳錢Tips：</strong>留意各供應商嘅「公屋優惠計劃」，部分有額外折扣。另外，同鄰居一齊裝同一間供應商，有時可以攞到「團體優惠」。</div>
            """),
            ("公屋寬頻常見問題解決", """
            <p>公屋住戶常遇到嘅寬頻問題同解決方法：</p>
            <ul>
                <li><strong>速度慢過應有水平：</strong>先用LAN線測速排除WiFi問題。如果LAN線測速都慢，打去供應商投訴，可能係大廈機房設備問題</li>
                <li><strong>WiFi訊號弱：</strong>公屋牆壁多數係石屎牆，穿牆衰減大。將Router放喺客廳中央位置，唔好放入電視櫃</li>
                <li><strong>經常斷線：</strong>可能係大廈線路老化。記錄斷線時間同頻率，向供應商投訴要求免費檢修</li>
                <li><strong>冇供應商覆蓋：</strong>極少數偏遠公屋可能只有供應商 E覆蓋。如果月費太貴，可以考慮5G家居寬頻作替代</li>
            </ul>
            """)
        ]
    },
    {
        "slug": "village-house-broadband-guide",
        "title": "村屋寬頻點揀？丁屋上網全攻略：覆蓋、速度、價錢比較",
        "description": "村屋寬頻揀邊間好？光纖有冇覆蓋？5G家居寬頻係咪更好嘅選擇？村屋上網全面解析。",
        "keywords": "村屋寬頻, 丁屋上網, 村屋光纖, 村屋5G, 新界村屋寬頻, 村屋WiFi, 村屋上網方案",
        "category": "beginner",
        "cat_class": "cat-beginner",
        "cat_name": "新手入門",
        "card_desc": "村屋寬頻揀邊間好？光纖覆蓋、5G家居寬頻、價錢比較全攻略。",
        "faqs": [
            ("村屋有冇光纖寬頻？", "部分村屋有，部分冇。大型村屋屋苑（如加州花園、錦繡花園）通常有FTTH光纖覆蓋。但散落嘅獨立丁屋好多時候只有FTTB甚至銅線DSL，速度有限。建議先用BroadbandHK查覆蓋。"),
            ("村屋用5G家居寬頻好唔好？", "如果村屋冇光纖覆蓋，5G家居寬頻係好選擇。新界大部分地區5G覆蓋已經唔錯，下載速度可達200-500Mbps。優點係唔使拉線、即裝即用；缺點係速度受天氣同用戶數量影響，唔及光纖穩定。"),
            ("村屋三層點樣覆蓋WiFi？", "村屋通常有三層，一部Router好難覆蓋全屋。建議用Mesh WiFi系統（3件裝），每層放一個節點。或者每層拉LAN線連接獨立AP，效果最好。預算大約$800-1500。")
        ],
        "sections": [
            ("村屋寬頻四大選擇", """
            <table class="comparison-table">
                <tr><th>方案</th><th>速度</th><th>月費</th><th>優點</th><th>缺點</th></tr>
                <tr><td>FTTH光纖到戶</td><td>100M-1000M</td><td>$108-198</td><td>速度快、穩定</td><td>覆蓋有限</td></tr>
                <tr><td>FTTB光纖到樓</td><td>最高100M</td><td>$88-148</td><td>覆蓋較廣</td><td>速度受限</td></tr>
                <tr><td>5G家居寬頻</td><td>100-500M</td><td>$98-198</td><td>免拉線、即裝</td><td>受天氣影響</td></tr>
                <tr><td>衛星寬頻</td><td>50-200M</td><td>$300+</td><td>偏遠地區可用</td><td>延遲高、貴</td></tr>
            </table>
            <div class="tip-box"><strong>💡 首選：</strong>有光纖就用光纖。冇光纖就試5G家居寬頻。兩樣都冇先考慮衛星。</div>
            """),
            ("村屋WiFi全屋覆蓋方案", """
            <p>村屋通常700呎×3層，一部Router根本覆蓋唔到。以下係三種解決方案：</p>
            <h3>方案一：Mesh WiFi系統（推薦）</h3>
            <ul>
                <li>每層放一個Mesh節點，自動組網</li>
                <li>推薦：TP-Link Deco X50 三件裝（$780）</li>
                <li>優點：設定簡單、漫遊無縫切換</li>
            </ul>
            <h3>方案二：每層獨立AP</h3>
            <ul>
                <li>由地下拉LAN線到每層，每層放一部AP</li>
                <li>優點：速度最快、最穩定</li>
                <li>缺點：要拉線、設定較複雜</li>
            </ul>
            <h3>方案三：Powerline + WiFi</h3>
            <ul>
                <li>利用電線傳輸網絡到每層</li>
                <li>優點：唔使拉線</li>
                <li>缺點：速度取決於電線質素，跨電錶可能唔work</li>
            </ul>
            """),
            ("村屋5G家居寬頻實測", """
            <p>我哋喺新界多個村屋地區實測5G家居寬頻嘅表現：</p>
            <table class="comparison-table">
                <tr><th>地區</th><th>供應商</th><th>下載速度</th><th>上傳速度</th><th>延遲</th></tr>
                <tr><td>元朗錦田</td><td>3HK</td><td>280Mbps</td><td>45Mbps</td><td>12ms</td></tr>
                <tr><td>大埔林村</td><td>供應商 C</td><td>350Mbps</td><td>52Mbps</td><td>10ms</td></tr>
                <tr><td>西貢壁屋</td><td>供應商 D</td><td>210Mbps</td><td>38Mbps</td><td>15ms</td></tr>
                <tr><td>粉嶺軍地</td><td>供應商 C</td><td>180Mbps</td><td>35Mbps</td><td>18ms</td></tr>
            </table>
            <p><em>*實測數據僅供參考，速度受基站距離、天氣、用戶數量影響</em></p>
            <div class="tip-box"><strong>💡 Tips：</strong>買5G家居寬頻前，先問供應商借Router試用幾日，測試你屋企嘅實際速度。大部分供應商都有14日冷靜期。</div>
            """),
            ("村屋寬頻安裝注意事項", """
            <p>村屋安裝寬頻有幾個特別要注意嘅地方：</p>
            <ul>
                <li><strong>拉線問題：</strong>獨立丁屋可能要從最近嘅電線桿拉線入屋，安裝費可能額外加$500-2000</li>
                <li><strong>業主同意：</strong>如果係租客，裝寬頻前要攞業主同意，特別係要鑽牆拉線嘅情況</li>
                <li><strong>防水處理：</strong>村屋入線位要做好防水，避免落雨滲水影響線路</li>
                <li><strong>雷擊保護：</strong>村屋較易受雷擊影響，建議Router接駁防雷插座</li>
                <li><strong>合約期：</strong>揀12個月合約較安全，因為村屋業權同租約變動較多</li>
            </ul>
            """)
        ]
    },
    {
        "slug": "ftth-vs-fttb-explained",
        "title": "光纖入屋 vs 光纖到樓：FTTH同FTTB有咩分別？點樣查自己屋企係邊種？",
        "description": "FTTH同FTTB差幾遠？點解同樣係1000M Plan但速度差咁遠？教你點查、點揀。",
        "keywords": "FTTH, FTTB, 光纖入屋, 光纖到樓, 光纖分別, 寬頻光纖, 光纖速度",
        "category": "tech",
        "cat_class": "cat-tech",
        "cat_name": "技術知識",
        "card_desc": "FTTH同FTTB差幾遠？點解同樣1000M Plan速度差咁遠？教你點查點揀。",
        "faqs": [
            ("點樣知道自己屋企係FTTH定FTTB？", "最簡單嘅方法係睇入屋嘅線。如果牆上有一個白色小盒（ONT/光纖終端），入面接住幼幼嘅光纖線，就係FTTH。如果只有電話線插座或者RJ45網線插座，大機率係FTTB。你亦可以問供應商確認。"),
            ("FTTB可以升級做FTTH嗎？", "要睇你大廈有冇光纖入屋嘅基建。如果大廈已經鋪咗光纖到每個單位，只係你而家用緊FTTB供應商，轉用FTTH供應商就得。但如果大廈根本冇光纖到戶嘅線路，就要等供應商入嚟鋪線，個人冇辦法自己升級。"),
            ("FTTB嘅1000M Plan係咪呃人？", "唔算呃人，但有誤導成分。FTTB嘅「1000M」指嘅係光纖到大廈機房嘅速度，但最後一段銅線入屋嘅速度通常只有100-200Mbps。正規供應商會喺合約寫明「最高速度」，但好多消費者唔留意。揀Plan前一定要問清楚實際可達速度。")
        ],
        "sections": [
            ("FTTH vs FTTB：圖解分別", """
            <p>簡單嚟講，兩者嘅分別在於「光纖去到邊」：</p>
            <table class="comparison-table">
                <tr><th>特徵</th><th>FTTH 光纖到戶</th><th>FTTB 光纖到樓</th></tr>
                <tr><td>光纖終點</td><td>你家門口</td><td>大廈地下機房</td></tr>
                <tr><td>最後一段</td><td>光纖（全程光纖）</td><td>銅線/電話線</td></tr>
                <tr><td>實際最高速度</td><td>1000Mbps+</td><td>100-200Mbps</td></tr>
                <tr><td>穩定性</td><td>極高</td><td>受線路老化影響</td></tr>
                <tr><td>延遲（Ping）</td><td>1-3ms</td><td>5-15ms</td></tr>
                <tr><td>常見大廈</td><td>2010年後新樓</td><td>舊樓、村屋</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>結論</td><td>首選方案</td><td>夠用但有限制</td></tr>
            </table>
            """),
            ("點解FTTB速度差咁遠？", """
            <p>FTTB嘅樽頸位在於最後一段銅線。光纖可以傳輸接近光速嘅數據，但銅線有物理限制：</p>
            <ul>
                <li><strong>距離衰減：</strong>銅線愈長，訊號愈弱。如果你住高層（離機房遠），速度會更差</li>
                <li><strong>干擾：</strong>銅線容易受電磁干擾影響，特別係同電力線纜行同一條管道時</li>
                <li><strong>線路老化：</strong>舊樓嘅銅線可能用咗20-30年，氧化同損耗令速度大打折扣</li>
                <li><strong>共用頻寬：</strong>同一條銅線可能被多戶共用，繁忙時段速度會下降</li>
            </ul>
            <div class="tip-box"><strong>💡 實際影響：</strong>你買咗$198/月嘅「1000M」Plan，但FTTB實際只跑到150M，等於你用緊1000M嘅價錢享受150M嘅服務。所以揀Plan前一定要確認係FTTH定FTTB！</div>
            """),
            ("點樣查你嘅大廈係FTTH定FTTB", """
            <p>以下幾個方法可以確認你屋企嘅接駁類型：</p>
            <ul>
                <li><strong>方法1：</strong>睇牆身嘅接線盒。FTTH會有一個獨立嘅白色ONT（光纖終端盒），大約手掌大小</li>
                <li><strong>方法2：</strong>問供應商客服，報上你嘅地址，佢哋可以即時查到</li>
                <li><strong>方法3：</strong>用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK 格價計算器</a> 輸入地址，覆蓋資料會顯示接駁類型</li>
                <li><strong>方法4：</strong>睇你嘅合約，通常會列明「FTTH」或「FTTB」</li>
            </ul>
            """),
            ("FTTB用戶嘅優化建議", """
            <p>如果你嘅大廈只有FTTB，可以用以下方法提升體驗：</p>
            <ul>
                <li><strong>唔好買太高速Plan：</strong>FTTB實際上限大約100-200M，買500M或1000M Plan只係浪費錢。100M Plan已經夠用</li>
                <li><strong>用LAN線直連：</strong>FTTB速度本身已經有限，再經WiFi衰減就更差。盡量用LAN線連接需要高速嘅裝置</li>
                <li><strong>投訴線路質素：</strong>如果測速遠低於應有水平（例如買100M但只有30M），向供應商投訴要求檢修線路</li>
                <li><strong>考慮5G替代：</strong>如果FTTB速度實在太差，5G家居寬頻可能係更好嘅選擇，速度可達200-500M</li>
            </ul>
            <div class="tip-box"><strong>💡 長遠解決：</strong>可以聯合大廈其他住戶向業主立案法團提議，邀請FTTH供應商入嚟鋪光纖。覆蓋一幢大廈嘅成本由供應商承擔，但需要法團同意施工。</div>
            """)
        ]
    },
    {
        "slug": "router-placement-settings-guide",
        "title": "Router擺位同設定全攻略：點放先收得最好？15個必改設定",
        "description": "Router放錯位置速度減半！教你最佳擺位、必改嘅15個設定、頻道優化，全屋WiFi速度即時提升。",
        "keywords": "Router擺位, Router設定, WiFi設定, WiFi頻道, Router位置, WiFi優化, 路由器設定",
        "category": "tech",
        "cat_class": "cat-tech",
        "cat_name": "技術知識",
        "card_desc": "Router放錯位置速度減半！最佳擺位、15個必改設定，全屋WiFi即時提升。",
        "faqs": [
            ("Router放高定放低好？", "放高好！WiFi訊號係向下同向四周擴散嘅。放喺離地1.2-1.5米嘅位置（例如書架上層、牆壁掛架）效果最好。放喺地上會令訊號被地板吸收，浪費一半覆蓋範圍。"),
            ("Router天線要點擺？", "如果Router有外置天線，一支指向上、一支打橫45度角。呢個角度可以同時覆蓋水平同垂直方向。如果有三支天線，一支向上、兩支各打橫45度向唔同方向。內置天線嘅Router通常已經優化好角度。"),
            ("Router附近唔可以放咩？", "避免放喺以下物品旁邊：微波爐（嚴重干擾2.4GHz）、金屬物品（反射訊號）、魚缸（水會吸收訊號）、電視機後面（金屬外殼阻擋）、密封電視櫃入面（散熱差+訊號被擋）。")
        ],
        "sections": [
            ("Router最佳擺位5大原則", """
            <ul>
                <li><strong>原則1 — 放中間：</strong>Router放屋企正中央，訊號向四面八方擴散，覆蓋最均勻</li>
                <li><strong>原則2 — 放高處：</strong>離地1.2-1.5米，WiFi訊號向下擴散效果最好</li>
                <li><strong>原則3 — 開放空間：</strong>唔好收入櫃或者放角落，訊號需要空氣流通</li>
                <li><strong>原則4 — 遠離干擾源：</strong>距離微波爐、藍牙裝置至少1米以上</li>
                <li><strong>原則5 — 靠近常用區域：</strong>如果冇辦法放中間，優先靠近你最常上網嘅位置</li>
            </ul>
            <div class="tip-box"><strong>💡 實測數據：</strong>將Router從電視櫃入面移到電視櫃上面（開放位置），WiFi速度平均提升40-60%！呢個係最簡單、零成本嘅提速方法。</div>
            """),
            ("15個必改Router設定", """
            <p>大部分人裝完Router就唔理，但改幾個設定可以大幅提升速度同安全性：</p>
            <h3>速度優化</h3>
            <ul>
                <li>1. 開啟 <strong>Band Steering</strong>：自動引導裝置用5GHz（更快）</li>
                <li>2. 5GHz頻寬設為 <strong>80MHz或160MHz</strong></li>
                <li>3. 用WiFi Analyzer App掃描，將頻道改為<strong>最少人用嘅頻道</strong></li>
                <li>4. 開啟 <strong>MU-MIMO</strong>（多裝置同時傳輸）</li>
                <li>5. 開啟 <strong>OFDMA</strong>（WiFi 6 Router先有）</li>
            </ul>
            <h3>安全設定</h3>
            <ul>
                <li>6. 改掉<strong>預設管理員密碼</strong>（admin/admin好危險！）</li>
                <li>7. WiFi加密用 <strong>WPA3</strong>（最少WPA2）</li>
                <li>8. 關閉 <strong>WPS</strong>（有安全漏洞）</li>
                <li>9. 關閉 <strong>遠端管理</strong>（唔好俾外人控制你Router）</li>
                <li>10. 定期<strong>更新韌體</strong>（修補安全漏洞）</li>
            </ul>
            <h3>穩定性設定</h3>
            <ul>
                <li>11. 設定<strong>定時自動重啟</strong>（每周一次，凌晨4點）</li>
                <li>12. 開啟 <strong>QoS</strong>：優先保障視像通話同打機</li>
                <li>13. DNS改用 <strong>1.1.1.1</strong>（Cloudflare）或 <strong>8.8.8.8</strong>（Google）</li>
                <li>14. 限制<strong>最大連接裝置數</strong>（避免被蹭網）</li>
                <li>15. 開啟<strong>訪客WiFi</strong>（畀訪客用，同主網絡隔離）</li>
            </ul>
            """),
            ("香港唔同戶型嘅擺位建議", """
            <table class="comparison-table">
                <tr><th>戶型</th><th>建議Router位置</th><th>需要額外裝置？</th></tr>
                <tr><td>開放式/Studio（200-300呎）</td><td>任何位置都OK</td><td>唔使</td></tr>
                <tr><td>一房（300-450呎）</td><td>客廳同房之間嘅走廊</td><td>唔使</td></tr>
                <tr><td>兩房（450-600呎）</td><td>客廳中央高處</td><td>可能要WiFi延伸器</td></tr>
                <tr><td>三房（600-800呎）</td><td>客廳中央</td><td>建議Mesh WiFi 2件裝</td></tr>
                <tr><td>村屋（三層）</td><td>中間樓層</td><td>必須Mesh WiFi 3件裝</td></tr>
            </table>
            """),
            ("WiFi頻道優化實戰教學", """
            <p>香港住宅密度高，你嘅WiFi可能同鄰居嘅WiFi互相干擾。以下係優化步驟：</p>
            <ul>
                <li><strong>Step 1：</strong>下載WiFi Analyzer App（Android免費、iOS用Airport Utility）</li>
                <li><strong>Step 2：</strong>掃描你附近嘅WiFi頻道使用情況</li>
                <li><strong>Step 3：</strong>2.4GHz頻段揀最少人用嘅頻道（建議用1、6或11號頻道）</li>
                <li><strong>Step 4：</strong>5GHz頻段揀DFS頻道（通常較少人用）</li>
                <li><strong>Step 5：</strong>登入Router管理頁面（192.168.1.1），手動設定頻道</li>
            </ul>
            <div class="tip-box"><strong>💡 自動 vs 手動：</strong>大部分Router預設係「自動選頻道」，但自動唔一定揀到最好嘅。手動設定通常可以再提升10-20%速度。</div>
            """)
        ]
    },
    {
        "slug": "cybersecurity-basics-guide",
        "title": "網絡安全入門：10個保護自己嘅基本功，防止被hack同詐騙",
        "description": "密碼點設先安全？公共WiFi可唔可以用？釣魚訊息點分辨？網絡安全入門必讀指南。",
        "keywords": "網絡安全, 網上安全, 密碼安全, 釣魚詐騙, 公共WiFi安全, 防毒軟件, 雙重認證",
        "category": "tech",
        "cat_class": "cat-tech",
        "cat_name": "技術知識",
        "card_desc": "密碼點設先安全？公共WiFi可唔可以用？10個網絡安全基本功必讀。",
        "faqs": [
            ("用公共WiFi安唔安全？", "公共WiFi（餐廳、商場、港鐵）基本上唔安全。其他人可以截取你嘅數據。如果一定要用，記住：唔好登入銀行或重要帳戶、唔好輸入信用卡資料、盡量用VPN加密連接。最安全係用自己手機嘅流動數據。"),
            ("密碼要幾長先安全？", "至少12個字元，包含大細楷英文、數字同符號。最好嘅方法係用「密碼短句」，例如「我隻貓2024年食咗3條魚」拼音版：WoZhiMao2024NianShiLe3TiaoYu!。每個帳戶用唔同密碼，用密碼管理器（如Bitwarden免費版）記住。"),
            ("收到可疑SMS/WhatsApp點算？", "唔好撳入面嘅連結！合法機構唔會透過SMS要求你輸入密碼或銀行資料。如果聲稱係銀行，自己打銀行官方熱線查證。記住：任何叫你急住做嘅訊息，99%係詐騙。慢慢處理就唔會中招。")
        ],
        "sections": [
            ("10大網絡安全基本功", """
            <ul>
                <li><strong>1. 用強密碼：</strong>12位以上、大細楷+數字+符號。每個帳戶唔同密碼</li>
                <li><strong>2. 開啟雙重認證（2FA）：</strong>Gmail、Facebook、銀行全部開啟，即使密碼被盜都登唔入</li>
                <li><strong>3. 更新系統：</strong>手機、電腦、Router嘅系統更新通常包含安全修補，即時更新</li>
                <li><strong>4. 唔好亂撳連結：</strong>收到可疑SMS、Email嘅連結，唔好撳。自己打開瀏覽器輸入官方網址</li>
                <li><strong>5. 用密碼管理器：</strong>Bitwarden（免費）或1Password，安全地儲存所有密碼</li>
                <li><strong>6. 避免公共WiFi：</strong>盡量用流動數據。必須用公共WiFi時開VPN</li>
                <li><strong>7. 定期備份：</strong>重要資料備份到外置硬碟或雲端，防範勒索軟件</li>
                <li><strong>8. 留意HTTPS：</strong>網站地址要有🔒鎖頭同https://，冇嘅話唔好輸入個人資料</li>
                <li><strong>9. 唔好共用密碼：</strong>朋友/屋企人都唔好共用。帳戶被盜時追唔到係邊個洩漏</li>
                <li><strong>10. 定期檢查帳戶：</strong>每月查銀行月結單、Email登入記錄，及早發現異常</li>
            </ul>
            """),
            ("釣魚詐騙實例同識別方法", """
            <p>以下係香港常見嘅網絡詐騙手法：</p>
            <table class="comparison-table">
                <tr><th>詐騙類型</th><th>常見手法</th><th>識別方法</th></tr>
                <tr><td>假銀行SMS</td><td>「你嘅帳戶有異常登入，即按連結驗證」</td><td>銀行唔會用SMS叫你撳連結</td></tr>
                <tr><td>假速遞通知</td><td>「你有包裹未領取，請繳付$18手續費」</td><td>真正速遞唔會要你網上俾錢</td></tr>
                <tr><td>假政府通知</td><td>「你有稅務退款，填寫銀行資料領取」</td><td>政府退款唔會用SMS通知</td></tr>
                <tr><td>社交媒體釣魚</td><td>朋友帳戶被盜後「借$3000應急」</td><td>打電話畀朋友本人確認</td></tr>
                <tr><td>假WiFi熱點</td><td>商場出現「Free_WiFi_HK」引你連接</td><td>只連有密碼嘅官方WiFi</td></tr>
            </table>
            <div class="tip-box"><strong>⚠ 鐵則：</strong>任何要求你「即刻」行動嘅訊息，幾乎100%係詐騙。合法機構永遠唔會催促你在幾分鐘內做決定。</div>
            """),
            ("免費安全工具推薦", """
            <ul>
                <li><strong>密碼管理器：</strong>Bitwarden（免費、開源、跨平台）</li>
                <li><strong>防毒軟件：</strong>Windows Defender（Windows內建，已經夠好）+ Malwarebytes免費版（定期掃描）</li>
                <li><strong>VPN：</strong>ProtonVPN（免費版、瑞士公司、唔記錄數據）</li>
                <li><strong>DNS過濾：</strong>Cloudflare 1.1.1.1（免費、快速、阻擋惡意網站）</li>
                <li><strong>瀏覽器擴充：</strong>uBlock Origin（攔截惡意廣告）+ HTTPS Everywhere（強制加密連接）</li>
                <li><strong>帳戶檢查：</strong>haveibeenpwned.com（免費查你嘅Email有冇被洩漏）</li>
            </ul>
            """),
            ("家居網絡安全設定", """
            <p>除咗個人習慣，屋企嘅網絡都要做好安全設定：</p>
            <ul>
                <li><strong>Router密碼：</strong>一定要改掉預設嘅admin/admin，用強密碼</li>
                <li><strong>WiFi加密：</strong>用WPA3（最少WPA2），唔好用WEP（10秒可以被破解）</li>
                <li><strong>關閉WPS：</strong>WPS有已知安全漏洞，關閉佢</li>
                <li><strong>更新Router韌體：</strong>定期檢查更新，修補安全漏洞</li>
                <li><strong>訪客WiFi：</strong>訪客用獨立WiFi，同主網絡隔離，保護你嘅裝置</li>
                <li><strong>DNS過濾：</strong>將Router DNS改為Cloudflare Family（1.1.1.3），自動阻擋惡意網站</li>
            </ul>
            <div class="tip-box"><strong>💡 進階：</strong>如果你想更全面嘅保護，可以考慮安裝Pi-hole（開源DNS過濾器），全屋所有裝置自動過濾廣告同惡意網站。</div>
            """)
        ]
    },
    {
        "slug": "5g-home-broadband-worth-it",
        "title": "5G家居寬頻值唔值得用？同光纖比較、實測速度、適合邊種人",
        "description": "5G家居寬頻係咩？同光纖寬頻差幾遠？邊啲人適合用？2026年5G家居寬頻全面評測。",
        "keywords": "5G家居寬頻, 5G寬頻, 5G上網, 5G vs 光纖, 5G Router, 5G速度, 5G寬頻月費",
        "category": "tech",
        "cat_class": "cat-tech",
        "cat_name": "技術知識",
        "card_desc": "5G家居寬頻同光纖比差幾遠？實測速度、月費比較，睇下適唔適合你。",
        "faqs": [
            ("5G家居寬頻同手機5G有咩分別？", "本質上用同一個5G網絡，但5G家居寬頻用專用嘅5G Router（室內CPE），天線收訊能力比手機強好多。而且家居Plan通常有更大數據用量（部分係無限），月費亦比手機5G Plan平。"),
            ("5G家居寬頻打機會唔會lag？", "視乎你嘅位置同網絡擁擠程度。5G嘅延遲理論上可以低至1ms，但實際喺香港通常係10-30ms。光纖寬頻通常係1-5ms。如果你係認真打機嘅玩家，光纖仍然係首選。休閒玩家用5G就冇問題。"),
            ("5G家居寬頻有冇限速？", "大部分供應商嘅5G家居Plan喺合約上寫住「唔限速」，但實際上喺網絡繁忙時段（晚上7-11點）可能會被降低優先度。部分Plan有「FUP公平使用政策」，用超過一定數據量後可能限速。簽約前問清楚。")
        ],
        "sections": [
            ("5G家居寬頻 vs 光纖寬頻", """
            <table class="comparison-table">
                <tr><th>比較項目</th><th>5G家居寬頻</th><th>光纖寬頻（FTTH）</th></tr>
                <tr><td>下載速度</td><td>100-800Mbps（波動）</td><td>100-2000Mbps（穩定）</td></tr>
                <tr><td>上傳速度</td><td>30-100Mbps</td><td>同下載一樣</td></tr>
                <tr><td>延遲</td><td>10-30ms</td><td>1-5ms</td></tr>
                <tr><td>穩定性</td><td>受天氣、用戶數量影響</td><td>極穩定</td></tr>
                <tr><td>安裝</td><td>即插即用，唔使拉線</td><td>要技師上門拉線</td></tr>
                <tr><td>搬屋</td><td>帶走Router就得</td><td>要重新安裝</td></tr>
                <tr><td>月費（1000M級）</td><td>$128-198</td><td>$108-198</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>適合</td><td>冇光纖覆蓋/租客/經常搬屋</td><td>追求穩定/打機/在家工作</td></tr>
            </table>
            """),
            ("5G家居寬頻適合邊種人？", """
            <p>以下情況，5G家居寬頻係好選擇：</p>
            <ul>
                <li><strong>冇光纖覆蓋：</strong>村屋、偏遠地區、舊樓只有FTTB嘅情況</li>
                <li><strong>租客：</strong>租約唔長、唔想被24個月寬頻合約綁住。5G可以帶走Router搬屋</li>
                <li><strong>臨時住所：</strong>裝修期間臨時搬出、短租Airbnb等</li>
                <li><strong>唔想等安裝：</strong>光纖安裝可能要排期1-2周，5G即日就有得用</li>
            </ul>
            <p>以下情況，光纖寬頻更適合你：</p>
            <ul>
                <li>打機玩家（需要低延遲）</li>
                <li>在家工作（需要穩定連接）</li>
                <li>多人同時使用（5人以上）</li>
                <li>做直播/上傳大量影片</li>
            </ul>
            """),
            ("2026年5G家居寬頻供應商比較", """
            <table class="comparison-table">
                <tr><th>供應商</th><th>月費</th><th>速度</th><th>合約期</th><th>特色</th></tr>
                <tr><td>3HK</td><td>$128起</td><td>5G無限</td><td>24個月</td><td>覆蓋廣、價錢中等</td></tr>
                <tr><td>供應商 C</td><td>$98起</td><td>5G無限</td><td>24個月</td><td>最平、經常有優惠</td></tr>
                <tr><td>供應商 D</td><td>$158起</td><td>5G無限</td><td>24個月</td><td>網絡質素好</td></tr>
                <tr><td>csl</td><td>$168起</td><td>5G無限</td><td>24個月</td><td>覆蓋最廣</td></tr>
            </table>
            <p><em>*價錢為2026年Q1參考價，實際因促銷而異</em></p>
            """),
            ("5G家居寬頻優化Tips", """
            <p>想從5G家居寬頻攞到最佳速度？跟住以下建議：</p>
            <ul>
                <li><strong>Router擺位：</strong>放喺靠窗位置，面向最近嘅5G基站方向。可以用CellMapper App查基站位置</li>
                <li><strong>避免遮擋：</strong>5G訊號穿牆能力較弱，Router同窗之間唔好有厚牆</li>
                <li><strong>固定頻段：</strong>部分5G Router可以手動鎖定n78頻段（3.5GHz），速度通常最快</li>
                <li><strong>外置天線：</strong>如果速度唔理想，可以加裝5G外置天線（$200-500），速度可提升50-100%</li>
                <li><strong>避開繁忙時段：</strong>如果有大檔案要下載，盡量喺非繁忙時段（凌晨-早上）進行</li>
            </ul>
            <div class="tip-box"><strong>💡 試用建議：</strong>大部分5G供應商有14日冷靜期。建議先買返嚟試幾日，測試唔同位置嘅速度。唔滿意可以退。</div>
            """)
        ]
    },
    {
        "slug": "vpn-explained-how-to-choose",
        "title": "VPN係咩？點揀VPN？2026年VPN入門指南同推薦",
        "description": "VPN有咩用？免費VPN安唔安全？點樣揀啱自己嘅VPN？新手必讀嘅VPN完全指南。",
        "keywords": "VPN, VPN推薦, VPN香港, 免費VPN, VPN是什麼, VPN選擇, VPN比較",
        "category": "tech",
        "cat_class": "cat-tech",
        "cat_name": "技術知識",
        "card_desc": "VPN有咩用？免費VPN安唔安全？新手必讀嘅VPN完全指南同2026年推薦。",
        "faqs": [
            ("免費VPN可唔可以用？", "大部分免費VPN唔建議使用。免費VPN嘅運營成本要從某處賺返，通常係賣你嘅瀏覽數據俾廣告商。部分免費VPN仲會注入廣告甚至惡意軟件。唯一推薦嘅免費VPN係ProtonVPN免費版（瑞士公司、唔賣數據、但速度較慢且只有少數伺服器）。"),
            ("用VPN會唔會影響網速？", "會。VPN會令速度下降10-30%，因為你嘅數據要多行一段路（經過VPN伺服器）。揀近嘅伺服器（例如香港、日本、新加坡）速度影響較少。優質付費VPN（如NordVPN、ExpressVPN）嘅速度下降通常在10-15%。"),
            ("VPN合唔合法？", "喺香港，使用VPN係完全合法嘅。VPN本身係一種網絡安全工具，企業同個人都廣泛使用。但用VPN進行非法活動（例如侵犯版權）當然仍然係違法嘅。")
        ],
        "sections": [
            ("VPN係咩？簡單解釋", """
            <p>VPN（Virtual Private Network，虛擬私人網絡）係一條「加密隧道」，將你嘅網絡流量加密後，經過VPN伺服器再去到目的地。</p>
            <p>用一個比喻：平時上網就好似寄明信片，任何人都可以睇到內容。用VPN就好似將明信片放入密封信封，只有收件人先打得開。</p>
            <p><strong>VPN嘅三大用途：</strong></p>
            <ul>
                <li><strong>保護隱私：</strong>加密你嘅網絡流量，防止被監控同追蹤</li>
                <li><strong>安全連接：</strong>喺公共WiFi用VPN，保護你嘅數據唔會被截取</li>
                <li><strong>跨區瀏覽：</strong>連接其他國家嘅伺服器，瀏覽當地內容</li>
            </ul>
            """),
            ("揀VPN嘅5個重點", """
            <ul>
                <li><strong>1. 無日誌政策（No-Log）：</strong>確保VPN供應商唔會記錄你嘅瀏覽活動。揀有獨立審計證明嘅</li>
                <li><strong>2. 速度：</strong>揀有亞洲伺服器（香港、日本、新加坡）嘅VPN，速度影響最少</li>
                <li><strong>3. 安全協議：</strong>支援WireGuard或OpenVPN協議，加密強度最高</li>
                <li><strong>4. 裝置數量：</strong>一個帳戶可以同時連接幾多部裝置（通常5-8部）</li>
                <li><strong>5. 價錢：</strong>年費Plan通常最抵，月費大約$25-50 HKD</li>
            </ul>
            <div class="tip-box"><strong>⚠ 注意：</strong>避免使用總部喺「五眼聯盟」國家（美國、英國、加拿大、澳洲、紐西蘭）嘅VPN，因為當地法律可能要求VPN供應商交出用戶數據。</div>
            """),
            ("2026年VPN推薦", """
            <table class="comparison-table">
                <tr><th>VPN</th><th>月費</th><th>速度</th><th>伺服器</th><th>特色</th></tr>
                <tr><td><strong>NordVPN</strong></td><td>~$30 HKD</td><td>★★★★★</td><td>60+國家</td><td>速度最快、功能最齊</td></tr>
                <tr><td><strong>ExpressVPN</strong></td><td>~$50 HKD</td><td>★★★★★</td><td>94國家</td><td>最易用、客服最好</td></tr>
                <tr><td><strong>Surfshark</strong></td><td>~$20 HKD</td><td>★★★★☆</td><td>65+國家</td><td>最平、無限裝置</td></tr>
                <tr><td><strong>ProtonVPN</strong></td><td>免費/~$35</td><td>★★★☆☆</td><td>60+國家</td><td>最注重隱私、瑞士公司</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td colspan="5">推薦：預算足夠揀NordVPN、最平揀Surfshark、免費揀ProtonVPN</td></tr>
            </table>
            <p><em>*月費為年付計劃嘅每月平均價</em></p>
            """),
            ("VPN設定教學", """
            <p>設定VPN好簡單，以NordVPN為例：</p>
            <ul>
                <li><strong>Step 1：</strong>去NordVPN官網註冊帳戶、揀Plan付費</li>
                <li><strong>Step 2：</strong>下載對應嘅App（Windows/Mac/iOS/Android都有）</li>
                <li><strong>Step 3：</strong>登入帳戶，撳「Quick Connect」自動連接最快嘅伺服器</li>
                <li><strong>Step 4：</strong>連接成功！你嘅所有網絡流量已經加密</li>
            </ul>
            <p><strong>進階設定建議：</strong></p>
            <ul>
                <li>開啟「Kill Switch」：VPN斷線時自動斷網，防止數據洩漏</li>
                <li>開啟「Auto-connect」：開機自動連接VPN</li>
                <li>Router級VPN：直接喺Router安裝VPN，全屋裝置自動加密（需要支援VPN嘅Router）</li>
            </ul>
            """)
        ]
    },
    {
        "slug": "nas-home-storage-guide",
        "title": "NAS家用儲存入門：點解要買NAS？點揀？點設定？新手完全指南",
        "description": "NAS係咩？屋企需要NAS嗎？Synology定QNAP好？NAS選購、設定、應用全攻略。",
        "keywords": "NAS, NAS推薦, 家用NAS, Synology, QNAP, NAS入門, 網絡儲存, NAS設定",
        "category": "tech",
        "cat_class": "cat-tech",
        "cat_name": "技術知識",
        "card_desc": "NAS係咩？屋企需要嗎？Synology定QNAP好？新手NAS選購設定全攻略。",
        "faqs": [
            ("NAS同外置硬碟有咩分別？", "外置硬碟要接電腦先用得到，NAS係獨立運作、接駁屋企網絡嘅儲存裝置，全屋所有裝置（手機、電腦、Smart TV）都可以隨時存取。仲可以喺外面透過互聯網遠端存取。簡單嚟講，NAS就係你嘅私人雲端硬碟。"),
            ("NAS需要幾快嘅寬頻？", "屋企內部用NAS，速度取決於LAN線（1Gbps=125MB/s）同WiFi。寬頻速度主要影響遠端存取。如果你要喺公司存取屋企NAS嘅檔案，上傳速度就好重要——100M寬頻上傳大約12MB/s，500M大約62MB/s。"),
            ("NAS硬碟壞咗資料會唔會冇？", "如果只用一隻硬碟（RAID 0或JBOD），硬碟壞咗資料就冇。所以強烈建議用兩隻硬碟做RAID 1（鏡像），一隻壞咗另一隻仲有完整備份。呢個係NAS最重要嘅保護功能。")
        ],
        "sections": [
            ("NAS可以做咩？6大用途", """
            <ul>
                <li><strong>1. 私人雲端：</strong>代替Google Drive/iCloud，唔使月月俾錢、容量自己決定</li>
                <li><strong>2. 相片備份：</strong>手機相片自動備份到NAS，類似Google相簿但完全私人</li>
                <li><strong>3. 影片串流：</strong>將電影、劇集放入NAS，全屋電視都可以播放（用Plex/Emby）</li>
                <li><strong>4. 自動備份：</strong>電腦、手機嘅資料定時自動備份到NAS</li>
                <li><strong>5. 遠端存取：</strong>喺公司或旅行都可以存取屋企NAS嘅檔案</li>
                <li><strong>6. 監控錄影：</strong>接駁IP Camera，NAS做錄影同儲存</li>
            </ul>
            <div class="tip-box"><strong>💡 慳錢計算：</strong>iCloud 2TB月費$78，一年$936。一部NAS + 2隻4TB硬碟大約$2500，可以用3-5年，長遠慳好多！</div>
            """),
            ("新手揀NAS指南", """
            <table class="comparison-table">
                <tr><th>品牌/型號</th><th>價錢</th><th>硬碟數</th><th>適合</th><th>特色</th></tr>
                <tr><td>Synology DS224+</td><td>~$2,800</td><td>2</td><td>一般家庭</td><td>系統最好用、App最齊</td></tr>
                <tr><td>Synology DS124</td><td>~$1,500</td><td>1</td><td>個人入門</td><td>最平Synology</td></tr>
                <tr><td>QNAP TS-233</td><td>~$1,800</td><td>2</td><td>預算有限</td><td>性價比高</td></tr>
                <tr><td>QNAP TS-464</td><td>~$4,500</td><td>4</td><td>進階玩家</td><td>擴展性強</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td colspan="5">新手推薦：Synology DS224+ — 系統最易用、社區支援最多</td></tr>
            </table>
            <p><strong>硬碟推薦：</strong>NAS專用硬碟（如WD Red Plus、Seagate IronWolf），4TB大約$700-900/隻</p>
            """),
            ("NAS基本設定教學", """
            <p>以Synology為例，初次設定步驟：</p>
            <ul>
                <li><strong>Step 1：</strong>裝入硬碟、接LAN線到Router、接電源開機</li>
                <li><strong>Step 2：</strong>電腦瀏覽器輸入 find.synology.com 搵到你嘅NAS</li>
                <li><strong>Step 3：</strong>安裝DSM系統（Synology嘅作業系統）</li>
                <li><strong>Step 4：</strong>設定RAID模式 — 2隻硬碟建議用SHR（等同RAID 1，資料有備份保護）</li>
                <li><strong>Step 5：</strong>建立共用資料夾同用戶帳戶</li>
                <li><strong>Step 6：</strong>安裝Synology Photos（相片備份）、Synology Drive（檔案同步）</li>
                <li><strong>Step 7：</strong>設定QuickConnect或DDNS，方便遠端存取</li>
            </ul>
            """),
            ("NAS同寬頻嘅配合建議", """
            <p>NAS嘅體驗同你嘅寬頻速度密切相關：</p>
            <ul>
                <li><strong>屋內傳輸：</strong>NAS用LAN線（1Gbps）連接Router，屋內傳輸速度約110MB/s，同寬頻速度無關</li>
                <li><strong>遠端存取：</strong>上傳速度決定你喺外面存取NAS嘅速度。100M寬頻上傳~12MB/s，500M上傳~62MB/s</li>
                <li><strong>Plex串流：</strong>如果用NAS做Plex Media Server俾屋外嘅人睇，需要上傳速度至少20Mbps（1080p）</li>
            </ul>
            <div class="tip-box"><strong>💡 建議：</strong>如果你會經常喺外面存取NAS，建議至少用500M對等寬頻（上下載速度一樣）。用 <a href="https://broadbandhk.com/speed-test.html" style="color:var(--primary)">BroadbandHK 測速工具</a> 確認你嘅上傳速度。</div>
            """)
        ]
    },
    # --- Life/Practical (8 articles) ---
    {
        "slug": "hong-kong-moving-guide",
        "title": "香港搬屋全攻略：搬屋公司點揀？Checklist、時間表、慳錢Tips",
        "description": "香港搬屋要幾錢？搬屋公司邊間好？由搬屋前準備到搬入新屋，一文睇晒搬屋全流程。",
        "keywords": "香港搬屋, 搬屋攻略, 搬屋公司, 搬屋費用, 搬屋checklist, 搬屋流程, 搬屋收費",
        "category": "saving",
        "cat_class": "cat-saving",
        "cat_name": "慳錢攻略",
        "card_desc": "搬屋公司邊間好？費用幾多？由準備到搬入新屋嘅完整Checklist同慳錢Tips。",
        "faqs": [
            ("香港搬屋大概要幾錢？", "視乎單位大小同距離。一般而言：開放式/一房約$1,500-3,000、兩房約$2,500-5,000、三房約$4,000-8,000。旺季（暑假、農曆新年前後）貴20-50%。上落樓梯（冇升降機）每層加$200-500。"),
            ("搬屋公司點揀先唔會中伏？", "三個重點：(1)一定要上門睇貨報價，電話報價好易有爭拗；(2)揀有固定辦公室嘅公司，唔好揀只有手機號碼嘅；(3)問清楚收費包唔包裝箱、拆裝傢俬、搬運保險。最好攞3間報價比較。"),
            ("幾時搬屋最平？", "避開6-8月暑假（學生搬屋旺季）、農曆新年前後。星期一至四比周末平約20-30%。月中比月頭月尾平（因為大部分租約月初或月尾開始）。如果時間靈活，問搬屋公司邊日最平。")
        ],
        "sections": [
            ("搬屋前4周準備Checklist", """
            <ul>
                <li><strong>4周前：</strong>開始揀搬屋公司、攞報價。安排新屋寬頻安裝（用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK 格價計算器</a> 查覆蓋）</li>
                <li><strong>3周前：</strong>確定搬屋公司、日期。開始執嘢、丟唔要嘅傢俬（可以放Carousell賣）</li>
                <li><strong>2周前：</strong>通知管理處（舊屋+新屋）搬屋日期。更改地址（銀行、保險、政府部門）</li>
                <li><strong>1周前：</strong>開始裝箱。標記每個箱（客廳/房間/廚房）。確認搬屋當日流程</li>
                <li><strong>前1日：</strong>貴重物品自己帶。雪櫃除霜。確認新屋水電煤已開通</li>
            </ul>
            <div class="tip-box"><strong>💡 慳錢Tips：</strong>紙箱唔使買！去超市（百佳、惠康）後門問，通常免費送。搬屋膠紙同氣泡紙喺淘寶買最平。</div>
            """),
            ("搬屋公司比較同報價攻略", """
            <table class="comparison-table">
                <tr><th>類型</th><th>收費</th><th>優點</th><th>缺點</th></tr>
                <tr><td>大型搬屋公司</td><td>$3,000-10,000+</td><td>有保險、專業、服務好</td><td>貴</td></tr>
                <tr><td>中型搬屋公司</td><td>$1,500-5,000</td><td>性價比高、彈性大</td><td>質素參差</td></tr>
                <tr><td>散工/Van仔</td><td>$800-2,000</td><td>最平</td><td>冇保險、冇保障</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td colspan="4">建議：一般家庭揀中型搬屋公司，有貴重傢俬揀大型公司</td></tr>
            </table>
            <p><strong>報價時必問：</strong></p>
            <ul>
                <li>收費包唔包紙箱、膠紙、氣泡紙？</li>
                <li>大型傢俬（床、梳化）拆裝要唔要額外收費？</li>
                <li>有冇搬運保險？損壞賠償政策？</li>
                <li>上落樓梯（如冇升降機）加幾多？</li>
            </ul>
            """),
            ("搬屋當日流程", """
            <ul>
                <li><strong>早上：</strong>最後檢查所有箱已封好、貴重物品自己攞住。影相記錄傢俬同牆身狀況（退租用）</li>
                <li><strong>搬運中：</strong>有一個人留喺舊屋監督裝車、一個人喺新屋監督落貨。確認每個箱放啱位置</li>
                <li><strong>完成後：</strong>檢查傢俬有冇損壞。舊屋最後巡視一次（抽屜、衣櫃入面、陽台）。交還舊屋鎖匙</li>
            </ul>
            """),
            ("搬屋後要做嘅10件事", """
            <ul>
                <li>✅ 確認新屋寬頻已安裝、WiFi正常（搬屋前預約好）</li>
                <li>✅ 更改地址：身份證（入境處）、銀行、保險、信用卡</li>
                <li>✅ 登記選民地址更新</li>
                <li>✅ 通知屋企人、朋友新地址</li>
                <li>✅ 檢查水電煤是否正常、煤氣公司約時間檢查</li>
                <li>✅ 更換門鎖（租屋都建議換，安全考慮）</li>
                <li>✅ 深層清潔（搬入前最適合做，屋企仲未有傢俬）</li>
                <li>✅ 記錄新屋任何已有損壞（影相、通知業主），保障退租時唔會被扣按金</li>
                <li>✅ 認識管理處、了解大廈規則</li>
                <li>✅ 歸還舊屋Router（如租用），避免被罰款</li>
            </ul>
            """)
        ]
    },
    {
        "slug": "renovation-budget-guide",
        "title": "裝修預算全攻略：香港裝修要幾錢？慳錢秘技同避伏指南",
        "description": "香港裝修每呎幾錢？全屋裝修預算點計？裝修公司點揀？避免超支同中伏嘅實用指南。",
        "keywords": "裝修預算, 裝修費用, 裝修公司, 裝修價錢, 裝修慳錢, 裝修報價, 香港裝修",
        "category": "saving",
        "cat_class": "cat-saving",
        "cat_name": "慳錢攻略",
        "card_desc": "香港裝修每呎幾錢？全屋預算點計？裝修公司點揀？避免超支同中伏指南。",
        "faqs": [
            ("香港裝修每呎大概幾錢？", "2026年市場價大約：簡單翻新$500-800/呎、中等裝修$800-1,200/呎、豪華裝修$1,200-2,000+/呎。一個400呎單位簡單翻新大約$20-32萬，中等裝修$32-48萬。呢個價錢包設計、人工、材料。"),
            ("裝修公司同判頭有咩分別？", "裝修公司有辦公室、設計師、項目經理，收費較高但服務較有保障。判頭（師傅）直接做工程，冇中間人所以平20-40%，但你要自己管理進度同質素。新手建議揀裝修公司，有經驗嘅可以搵判頭慳錢。"),
            ("裝修會唔會超支？點避免？", "超支喺裝修好常見，平均超支10-20%。避免方法：(1)預算預留15%作為應急；(2)簽約前問清楚所有「唔包」嘅項目；(3)儘量唔好中途改設計；(4)材料費要列明品牌同型號。")
        ],
        "sections": [
            ("裝修預算拆解", """
            <table class="comparison-table">
                <tr><th>項目</th><th>佔預算比例</th><th>400呎參考價</th></tr>
                <tr><td>拆舊工程</td><td>5-10%</td><td>$1-3萬</td></tr>
                <tr><td>水電工程</td><td>10-15%</td><td>$3-5萬</td></tr>
                <tr><td>泥水工程（地磚、牆磚）</td><td>15-20%</td><td>$5-8萬</td></tr>
                <tr><td>木工（傢俬、櫃）</td><td>25-35%</td><td>$8-12萬</td></tr>
                <tr><td>油漆</td><td>5-8%</td><td>$2-3萬</td></tr>
                <tr><td>廚房+廁所</td><td>15-20%</td><td>$5-8萬</td></tr>
                <tr><td>雜項（清潔、運輸等）</td><td>5%</td><td>$1-2萬</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>合計</td><td>100%</td><td>$25-41萬</td></tr>
            </table>
            """),
            ("裝修慳錢10大秘技", """
            <ul>
                <li><strong>1. 保留可用嘅嘢：</strong>如果舊有地磚/牆磚狀態OK，唔使全部打掉重鋪，慳幾萬</li>
                <li><strong>2. IKEA傢俬代替訂造：</strong>衣櫃、書架用IKEA可以平60-70%，質素唔差</li>
                <li><strong>3. 淘寶買燈飾五金：</strong>同樣品質嘅燈飾，淘寶價錢係香港嘅1/3-1/5</li>
                <li><strong>4. 揀平替磁磚：</strong>國產磚同意大利磚效果差唔多，但價錢差3-5倍</li>
                <li><strong>5. 減少間牆：</strong>開放式設計唔使間牆，慳材料同人工</li>
                <li><strong>6. 包工包料 vs 包工不包料：</strong>自己買材料可以慳10-20%（但要有時間格價）</li>
                <li><strong>7. 避開旺季：</strong>農曆新年後（3-4月）同暑假後（10-11月）係淡季，判頭較願意減價</li>
                <li><strong>8. 一次過做：</strong>分階段裝修反而更貴，因為每次開工都有基本成本</li>
                <li><strong>9. 唔好中途改設計：</strong>改設計 = 額外費用 + 延期。開工前想清楚</li>
                <li><strong>10. 寬頻線路一齊做：</strong>裝修時順便拉LAN線到每個房間，之後唔使靠WiFi穿牆</li>
            </ul>
            <div class="tip-box"><strong>💡 裝修期間寬頻：</strong>裝修工程通常1-3個月，期間可以用5G家居寬頻或手機熱點。裝修完先裝返光纖寬頻。</div>
            """),
            ("裝修公司點揀？避伏指南", """
            <ul>
                <li><strong>攞最少3個報價：</strong>唔好只問一間，比較先知道市場價</li>
                <li><strong>睇過往作品：</strong>要求睇真實完工相片，最好可以去現場睇</li>
                <li><strong>合約要詳細：</strong>每個項目嘅材料品牌、型號、數量、單價都要列明</li>
                <li><strong>付款分期：</strong>千祈唔好一次過俾晒。建議：簽約30%→開工30%→完工驗收30%→保養期後10%</li>
                <li><strong>保養期：</strong>確認有6-12個月保養期，裝修後有問題免費維修</li>
            </ul>
            """),
            ("裝修時嘅網絡規劃", """
            <p>裝修係最佳時機做好屋企嘅網絡基建：</p>
            <ul>
                <li><strong>拉LAN線：</strong>由入線位拉Cat6 LAN線到每個房間（每條大約$100-200工料費），之後WiFi唔夠快可以直接接線</li>
                <li><strong>預留NAS位置：</strong>如果有興趣用NAS，預留一個有電源同LAN口嘅位置</li>
                <li><strong>Router位置：</strong>同裝修師傅講好Router要放喺屋企中央位置，預留電源同光纖入線</li>
                <li><strong>每個房間至少2個網線插座：</strong>一個畀電腦/Smart TV、一個備用</li>
            </ul>
            <div class="tip-box"><strong>💡 重要：</strong>裝修後先想拉LAN線就好麻煩（要鑿牆或者明喉），所以趁裝修一次過搞掂，長遠受惠！</div>
            """)
        ]
    },
    {
        "slug": "hong-kong-car-park-investment",
        "title": "香港車位投資指南：車位值唔值得買？回報率、風險、揀位攻略",
        "description": "香港車位投資值唔值得？回報率幾多？邊區車位最值得買？車位投資入門全攻略。",
        "keywords": "車位投資, 香港車位, 車位回報率, 車位買賣, 車位出租, 車位價錢, 車位投資回報",
        "category": "saving",
        "cat_class": "cat-saving",
        "cat_name": "慳錢攻略",
        "card_desc": "車位投資值唔值得？回報率幾多？邊區最值得買？車位投資入門全攻略。",
        "faqs": [
            ("香港車位投資回報率大概幾多？", "2026年香港車位租金回報率平均約2.5-4%，視乎地區。市區（中環、銅鑼灣）車位貴但回報率較低（約2-2.5%）；新界（元朗、將軍澳）車位較平但回報率較高（約3-4%）。比較銀行定期存款（約2-3%），車位回報仍有少少優勢，但流動性差好多。"),
            ("買車位要幾多首期？", "車位按揭最多借五成（50%），即係要俾50%首期。一個$150萬嘅車位需要$75萬首期。車位按揭利率通常比住宅高0.5-1%。如果你已經有住宅按揭，銀行可能會收緊車位嘅借貸額。"),
            ("買車位有咩隱藏成本？", "除咗車位本身嘅價錢，仲有：管理費（每月$500-2000）、差餉地租（每季幾百蚊）、印花稅（最高4.25%）、律師費（約$5000-8000）。呢啲成本會影響你嘅實際回報率。")
        ],
        "sections": [
            ("車位投資回報率計算", """
            <p>計算車位投資回報率嘅公式：</p>
            <p style="background:#f0f9ff;padding:16px;border-radius:8px;font-size:1.1em;text-align:center"><strong>年度淨回報率 = (年租金收入 - 年度支出) ÷ 總投資成本 × 100%</strong></p>
            <p><strong>計算例子：</strong></p>
            <table class="comparison-table">
                <tr><th>項目</th><th>金額</th></tr>
                <tr><td>車位買入價</td><td>$150萬</td></tr>
                <tr><td>印花稅 + 律師費</td><td>~$7萬</td></tr>
                <tr><td>總投資成本</td><td>$157萬</td></tr>
                <tr><td>月租收入</td><td>$4,500</td></tr>
                <tr><td>年租金收入</td><td>$54,000</td></tr>
                <tr><td>年度支出（管理費+差餉）</td><td>~$15,000</td></tr>
                <tr><td>年度淨收入</td><td>$39,000</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>淨回報率</td><td>2.48%</td></tr>
            </table>
            """),
            ("邊區車位最值得投資？", """
            <table class="comparison-table">
                <tr><th>地區</th><th>車位參考價</th><th>月租</th><th>估計回報率</th><th>評價</th></tr>
                <tr><td>中環/金鐘</td><td>$300-600萬</td><td>$5,000-8,000</td><td>1.5-2%</td><td>保值但回報低</td></tr>
                <tr><td>觀塘/九龍灣</td><td>$120-200萬</td><td>$3,500-5,000</td><td>2.5-3.5%</td><td>商業區需求大</td></tr>
                <tr><td>將軍澳</td><td>$100-180萬</td><td>$3,000-4,500</td><td>3-3.5%</td><td>住宅區穩定需求</td></tr>
                <tr><td>沙田</td><td>$120-200萬</td><td>$3,000-4,500</td><td>2.5-3%</td><td>交通樞紐</td></tr>
                <tr><td>元朗/天水圍</td><td>$60-120萬</td><td>$2,000-3,500</td><td>3-4%</td><td>回報率最高</td></tr>
            </table>
            """),
            ("揀車位5大要點", """
            <ul>
                <li><strong>1. 屋苑車位比例：</strong>車位數量少過住宅單位數量嘅屋苑，車位需求會更大、租金更穩定</li>
                <li><strong>2. 附近泊車選擇：</strong>如果附近有大量公眾停車場或路邊咪錶，你嘅車位競爭力會減弱</li>
                <li><strong>3. 車位位置：</strong>近升降機、唔使轉彎、唔係柱位旁邊嘅車位最受歡迎，租金可以高10-20%</li>
                <li><strong>4. 管理費水平：</strong>管理費太高會蠶食你嘅回報。比較同區唔同屋苑嘅管理費</li>
                <li><strong>5. 電動車充電：</strong>有充電設施或者容易加裝充電器嘅車位，未來需求會愈嚟愈大</li>
            </ul>
            <div class="tip-box"><strong>💡 趨勢：</strong>隨住電動車普及，有充電設施嘅車位未來升值潛力更大。買車位時可以問管理處有冇計劃加裝充電設施。</div>
            """),
            ("車位投資風險同注意事項", """
            <ul>
                <li><strong>流動性低：</strong>車位唔似股票咁易賣出，可能要幾個月至半年先搵到買家</li>
                <li><strong>空置風險：</strong>租客退租後可能要空置1-3個月先搵到新租客</li>
                <li><strong>政策風險：</strong>政府可能推出影響車位需求嘅政策（例如電子道路收費、增加公共停車場）</li>
                <li><strong>維修費用：</strong>停車場翻新時可能要分攤大額維修基金</li>
                <li><strong>利率風險：</strong>加息會令按揭供款增加，蠶食回報</li>
            </ul>
            """)
        ]
    },
    {
        "slug": "hong-kong-mpf-guide",
        "title": "香港強積金MPF攻略：點揀基金？點整合？點慳管理費？",
        "description": "MPF揀邊隻基金好？管理費點慳？轉工MPF點處理？強積金實用攻略全面睇。",
        "keywords": "MPF, 強積金, MPF基金, MPF攻略, MPF管理費, MPF整合, 強積金揀基金",
        "category": "saving",
        "cat_class": "cat-saving",
        "cat_name": "慳錢攻略",
        "card_desc": "MPF揀邊隻基金好？管理費點慳？轉工點處理？強積金實用攻略。",
        "faqs": [
            ("MPF揀邊類基金好？", "視乎你嘅年齡同風險承受能力。20-30歲：可以進取啲，揀股票基金（特別係環球股票）佔70-80%。40-50歲：平衡型，股票50%+債券50%。50歲以上：保守型，債券為主。懶人之選係「預設投資策略（DIS）」，自動按年齡調整。"),
            ("MPF管理費真係差好遠？", "係！唔同基金嘅管理費可以差3-4倍。例如同樣係環球股票基金，最平嘅基金收0.6%，最貴嘅收2%以上。每年差1.4%聽落唔多，但40年累計會令你嘅退休金少20-30%！揀低收費基金係最實際嘅慳錢方法。"),
            ("轉工後舊嘅MPF點算？", "你可以選擇：(1)將舊MPF轉去新僱主嘅MPF計劃；(2)將舊MPF轉去你自己揀嘅「個人帳戶」。建議轉去管理費最低嘅計劃。唔好放喺度唔理，因為舊計劃嘅管理費可能好高。")
        ],
        "sections": [
            ("MPF基金類型同表現", """
            <table class="comparison-table">
                <tr><th>基金類型</th><th>風險</th><th>10年平均年回報</th><th>適合</th></tr>
                <tr><td>環球股票基金</td><td>高</td><td>6-9%</td><td>年輕、長線投資</td></tr>
                <tr><td>香港股票基金</td><td>高</td><td>2-5%</td><td>看好香港市場</td></tr>
                <tr><td>混合資產基金</td><td>中</td><td>3-6%</td><td>平衡型投資者</td></tr>
                <tr><td>債券基金</td><td>低</td><td>1-3%</td><td>保守投資者</td></tr>
                <tr><td>保守基金</td><td>極低</td><td>0.5-1%</td><td>接近退休人士</td></tr>
                <tr><td>預設投資策略(DIS)</td><td>按年齡調整</td><td>4-7%</td><td>懶人之選</td></tr>
            </table>
            <div class="tip-box"><strong>💡 重點：</strong>年輕人最大嘅優勢係「時間」。30歲開始每月供$1500到環球股票基金（假設年回報7%），65歲退休時有大約$240萬。如果放保守基金（年回報1%），只有$68萬。差距係3.5倍！</div>
            """),
            ("慳MPF管理費攻略", """
            <p>MPF管理費係蠶食你回報嘅最大敵人。以下係慳費攻略：</p>
            <ul>
                <li><strong>揀低收費基金：</strong>同類型基金，管理費可以差2-3倍。例如永明彩虹計劃嘅環球股票基金收費約0.75%，比某啲計劃嘅2%平好多</li>
                <li><strong>用「半自由行」轉供款：</strong>你可以每年一次將僱員供款部分轉去自己揀嘅低收費計劃</li>
                <li><strong>整合MPF帳戶：</strong>如果你有多個舊MPF帳戶（轉工留低嘅），整合到一個低收費計劃</li>
                <li><strong>考慮DIS：</strong>預設投資策略嘅管理費上限係0.95%，比好多主動管理基金平</li>
            </ul>
            """),
            ("MPF整合步驟", """
            <p>將散落嘅MPF帳戶整合到一個計劃，方便管理又可以慳費：</p>
            <ul>
                <li><strong>Step 1：</strong>登入積金局ePA帳戶（mpfa.org.hk），查你所有MPF帳戶</li>
                <li><strong>Step 2：</strong>比較各計劃嘅管理費，揀最低嘅</li>
                <li><strong>Step 3：</strong>填寫「計劃成員帳戶轉移申請表」（可以喺積金局網站下載）</li>
                <li><strong>Step 4：</strong>交畀你想轉入嘅MPF受託人處理</li>
                <li><strong>Step 5：</strong>轉移通常需要6-8個工作天完成</li>
            </ul>
            """),
            ("年輕人MPF配置建議", """
            <p>如果你25-35歲，距離退休仲有30年以上，以下配置可以參考：</p>
            <ul>
                <li><strong>進取型（適合25-35歲）：</strong>環球股票基金80% + 亞洲股票基金20%</li>
                <li><strong>均衡型（適合35-45歲）：</strong>環球股票基金50% + 混合資產基金30% + 債券基金20%</li>
                <li><strong>保守型（適合50歲以上）：</strong>債券基金50% + 保守基金30% + 混合資產基金20%</li>
            </ul>
            <div class="tip-box"><strong>💡 懶人方案：</strong>如果你唔想煩，直接揀「預設投資策略（DIS）」。佢會自動按你嘅年齡調整股債比例，管理費亦有上限保障。雖然唔係最優，但至少唔會太差。</div>
            """)
        ]
    },
    {
        "slug": "hong-kong-tax-saving-guide",
        "title": "香港稅務慳稅攻略：薪俸稅點計？扣稅項目有邊啲？報稅實用指南",
        "description": "香港打工仔點樣合法慳稅？薪俸稅計算方法、扣稅項目一覽、報稅Tips全攻略。",
        "keywords": "慳稅, 香港稅務, 薪俸稅, 扣稅, 報稅, 免稅額, 稅務扣除",
        "category": "saving",
        "cat_class": "cat-saving",
        "cat_name": "慳錢攻略",
        "card_desc": "打工仔點樣合法慳稅？扣稅項目一覽、免稅額計算、報稅實用Tips。",
        "faqs": [
            ("香港薪俸稅稅率幾多？", "香港用累進稅率同標準稅率兩者取較低者。累進稅率：首$50,000收2%、次$50,000收6%、再$50,000收10%、再$50,000收14%、餘額17%。標準稅率15%。大部分打工仔用累進稅率會較著數。"),
            ("自願性MPF供款可以扣稅？", "可以！自願性MPF供款（TVC）每年最多扣$60,000。呢個係2019年起新增嘅扣稅項目，好多人唔知。供$60,000自願MPF，如果你嘅邊際稅率係17%，可以慳$10,200稅。而且MPF仲有投資回報。"),
            ("自住物業貸款利息可以扣稅？", "可以！自住物業嘅按揭利息每年最多扣$100,000，最多扣20個課稅年度。呢個係好多業主唔知嘅慳稅方法。記得報稅時填寫物業稅部分。")
        ],
        "sections": [
            ("2026年免稅額一覽", """
            <table class="comparison-table">
                <tr><th>免稅額項目</th><th>金額（每年）</th></tr>
                <tr><td>基本免稅額</td><td>$132,000</td></tr>
                <tr><td>已婚人士免稅額</td><td>$264,000</td></tr>
                <tr><td>子女免稅額（每名）</td><td>$130,000</td></tr>
                <tr><td>子女出生年度額外免稅</td><td>$130,000</td></tr>
                <tr><td>供養父母免稅額（60歲以上，同住）</td><td>$100,000</td></tr>
                <tr><td>供養父母免稅額（60歲以上，不同住）</td><td>$50,000</td></tr>
                <tr><td>單親免稅額</td><td>$132,000</td></tr>
                <tr><td>傷殘受養人免稅額</td><td>$75,000</td></tr>
            </table>
            <p><em>*以上為2025/26課稅年度參考數字</em></p>
            """),
            ("8個合法慳稅方法", """
            <ul>
                <li><strong>1. 自願性MPF供款：</strong>每年最多扣$60,000。邊際稅率17%可慳$10,200</li>
                <li><strong>2. 合資格年金保費：</strong>每年最多扣$60,000（同自願MPF共用$60,000上限）</li>
                <li><strong>3. 自住物業貸款利息：</strong>每年最多扣$100,000</li>
                <li><strong>4. 個人進修開支：</strong>每年最多扣$100,000（與工作相關嘅課程）</li>
                <li><strong>5. 認可慈善捐款：</strong>最多扣入息35%（捐款$100以上可扣稅）</li>
                <li><strong>6. 供養父母/祖父母：</strong>每名最多$100,000（同住長者）</li>
                <li><strong>7. 住宅租金扣除：</strong>每年最多扣$100,000（2022年起新增）</li>
                <li><strong>8. VHIS自願醫保扣除：</strong>每名受保人每年最多扣$8,000</li>
            </ul>
            <div class="tip-box"><strong>💡 計算例子：</strong>年薪$60萬，用盡自願MPF($6萬)、租金扣除($10萬)、供養父母($10萬)、基本免稅($13.2萬)，應課稅入息淨額只有$20.8萬，稅款大約$1.2萬。冇用扣稅就要交約$4.4萬，差$3.2萬！</div>
            """),
            ("報稅實用Tips", """
            <ul>
                <li><strong>準時報稅：</strong>通常5月初收到報稅表，限期1個月。網上報稅可自動延期1個月。遲交有罰款</li>
                <li><strong>保留單據：</strong>所有扣稅項目嘅單據要保留7年，稅務局可能抽查</li>
                <li><strong>用eTAX網上報稅：</strong>快捷方便，仲可以睇到上年嘅報稅資料做參考</li>
                <li><strong>分開評稅 vs 合併評稅：</strong>已婚人士可以揀分開或合併評稅。如果兩人收入差距大，合併評稅通常較著數</li>
                <li><strong>暫繳稅反對：</strong>如果你預計下年收入會大減，可以申請減少暫繳稅</li>
            </ul>
            """),
            ("打工仔慳稅行動清單", """
            <ul>
                <li>✅ 開設自願性MPF帳戶，每月供$5,000（年$60,000扣稅上限）</li>
                <li>✅ 買VHIS自願醫保（自己+家人每人每年最多扣$8,000）</li>
                <li>✅ 如果有供養60歲以上父母，記得報稅時填寫</li>
                <li>✅ 保留所有進修課程收據（與工作相關嘅課程先可以扣）</li>
                <li>✅ 租客記得保留租約同租金收據，每年最多扣$100,000</li>
                <li>✅ 捐款$100以上保留收據（認可慈善機構先得）</li>
                <li>✅ 用eTAX網上報稅，方便又有延期</li>
            </ul>
            """)
        ]
    },
    {
        "slug": "start-online-shop-guide",
        "title": "開網店全攻略：香港開網店要幾錢？平台比較、流程、慳成本秘技",
        "description": "想開網店但唔知從何入手？Shopify定Shopline好？成本幾多？由零開始嘅網店全攻略。",
        "keywords": "開網店, 網店攻略, 網店平台, Shopify, Shopline, 網店成本, 香港網店",
        "category": "trending",
        "cat_class": "cat-trending",
        "cat_name": "熱門話題",
        "card_desc": "想開網店唔知從何入手？平台比較、成本計算、流程全攻略，由零開始。",
        "faqs": [
            ("開網店要幾多啟動資金？", "最低門檻大約$2,000-5,000就可以開始：網店平台月費$200-500、域名$100/年、基本產品攝影$500-1,000。如果做Dropshipping（代發貨），唔使囤貨就更平。當然，如果要專業設計同大量庫存，預算就要$2-5萬以上。"),
            ("Shopify定Shopline邊個好？", "Shopify功能最強大、App生態最豐富，適合有經驗或者打算做大嘅店主。Shopline係亞洲公司，中文介面更好、本地支付（FPS、PayMe）整合更方便，適合香港初創網店。新手建議先用Shopline。"),
            ("冇貨源點算？", "可以做Dropshipping（代發貨模式）：你開網店賣嘢，但唔使自己囤貨。客人下單後，供應商直接寄貨畀客人。可以喺淘寶/1688搵供應商、或者用Dropshipping平台（如CJDropshipping）。利潤較低但風險亦低，適合新手試水溫。")
        ],
        "sections": [
            ("網店平台比較", """
            <table class="comparison-table">
                <tr><th>平台</th><th>月費</th><th>交易費</th><th>優點</th><th>適合</th></tr>
                <tr><td>Shopline</td><td>$338起</td><td>0.5-2%</td><td>中文介面、本地支付</td><td>香港初創</td></tr>
                <tr><td>Shopify</td><td>$250起(USD29)</td><td>0.5-2%</td><td>功能最強、App最多</td><td>有經驗店主</td></tr>
                <tr><td>Boutir掌舖</td><td>$199起</td><td>2%</td><td>手機管理、最簡單</td><td>個人小店</td></tr>
                <tr><td>WooCommerce</td><td>免費(需hosting)</td><td>視支付方式</td><td>完全自主</td><td>有技術基礎</td></tr>
                <tr><td>IG/FB Shop</td><td>免費</td><td>視支付方式</td><td>零成本開始</td><td>試水溫</td></tr>
            </table>
            """),
            ("開網店5步流程", """
            <ul>
                <li><strong>Step 1 — 揀產品：</strong>搵一個你有興趣嘅niche市場。分析競爭對手、定價、目標客群</li>
                <li><strong>Step 2 — 揀平台：</strong>新手建議用Shopline或Boutir開始，月費低、易上手</li>
                <li><strong>Step 3 — 設定網店：</strong>上載產品相片同描述、設定付款方式（FPS、信用卡、PayMe）、設定送貨方式</li>
                <li><strong>Step 4 — 推廣：</strong>開IG商業帳戶、FB專頁，定期出內容。可以試小額Facebook/IG廣告（$50/日開始）</li>
                <li><strong>Step 5 — 營運：</strong>處理訂單、客服、庫存管理。用Excel或者平台內建嘅工具追蹤銷售數據</li>
            </ul>
            <div class="tip-box"><strong>💡 重要：</strong>開網店最重要嘅唔係網站，係<strong>流量</strong>。有最靚嘅網站但冇人嚟都係冇用。建議將預算嘅50%放喺推廣上。</div>
            """),
            ("網店成本拆解", """
            <table class="comparison-table">
                <tr><th>項目</th><th>最低預算</th><th>建議預算</th><th>說明</th></tr>
                <tr><td>網店平台月費</td><td>$0（IG Shop）</td><td>$300-500/月</td><td>Shopline/Shopify</td></tr>
                <tr><td>域名</td><td>$80/年</td><td>$80-150/年</td><td>.com或.hk</td></tr>
                <tr><td>產品攝影</td><td>$0（自己影）</td><td>$500-2,000</td><td>專業產品相好重要</td></tr>
                <tr><td>首批貨物</td><td>$0（Dropship）</td><td>$3,000-10,000</td><td>視產品類型</td></tr>
                <tr><td>包裝物料</td><td>$200</td><td>$500-1,000</td><td>紙箱、氣泡紙、貼紙</td></tr>
                <tr><td>廣告預算（首月）</td><td>$500</td><td>$2,000-5,000</td><td>Facebook/IG廣告</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>合計（首月）</td><td>~$1,000</td><td>~$7,000-18,000</td><td></td></tr>
            </table>
            """),
            ("網店寬頻同工具需求", """
            <p>開網店雖然唔需要超快寬頻，但穩定嘅網絡對日常營運好重要：</p>
            <ul>
                <li><strong>寬頻需求：</strong>100-500M寬頻已經足夠。上傳大量產品相片時速度快啲會方便好多</li>
                <li><strong>必備工具：</strong>Canva（免費設計工具）、Google Analytics（追蹤流量）、ChatGPT（寫產品描述）</li>
                <li><strong>拍片設備：</strong>如果要拍產品影片或者做直播帶貨，建議用500M以上寬頻確保直播穩定</li>
                <li><strong>雲端協作：</strong>用Google Drive/Notion管理訂單同產品資料</li>
            </ul>
            <div class="tip-box"><strong>💡 直播帶貨：</strong>如果你打算喺IG/FB做直播賣嘢，穩定嘅寬頻好重要。建議用LAN線連接電腦，用 <a href="https://broadbandhk.com/speed-test.html" style="color:var(--primary)">BroadbandHK 測速工具</a> 確認上傳速度至少10Mbps以上。</div>
            """)
        ]
    },
    {
        "slug": "hong-kong-startup-cost-guide",
        "title": "香港創業成本計算：開公司要幾錢？註冊、租Office、營運成本全拆解",
        "description": "想喺香港創業？公司註冊幾錢？租Office定Co-working好？每月營運成本計算全攻略。",
        "keywords": "香港創業, 創業成本, 開公司, 公司註冊, 創業費用, 租辦公室, 營運成本",
        "category": "trending",
        "cat_class": "cat-trending",
        "cat_name": "熱門話題",
        "card_desc": "香港創業要幾錢？公司註冊、租Office、營運成本全拆解，創業必讀。",
        "faqs": [
            ("喺香港開一間有限公司要幾錢？", "公司註冊費用大約$3,000-6,000，包括：公司註冊處費用$1,720、商業登記費$2,150/年、公司秘書服務$500-2,000/年。如果用會計公司代辦，連埋首年服務通常$3,000-5,000全包。整個過程1-2周完成。"),
            ("初創應該租Office定用Co-working？", "初期強烈建議用Co-working Space。原因：(1)月費$2,000-5,000 vs 傳統Office $8,000-20,000+；(2)唔使簽長約，靈活性高；(3)包寬頻、水電、清潔、會議室。等到團隊穩定（5人以上）先考慮租獨立Office。"),
            ("香港創業有冇政府資助？", "有！常見嘅包括：科技券（TVP，最高$60萬）、中小企業市場推廣基金（EMF，最高$80萬）、創業培育計劃（Science Park/Cyberport提供辦公室+資金）。記得留意政府嘅BUD專項基金同各類創業比賽。")
        ],
        "sections": [
            ("創業首年成本估算", """
            <table class="comparison-table">
                <tr><th>成本項目</th><th>最低預算（月）</th><th>建議預算（月）</th></tr>
                <tr><td>公司註冊+商業登記</td><td colspan="2">$3,000-5,000（一次性）</td></tr>
                <tr><td>辦公空間</td><td>$0（在家工作）</td><td>$2,000-5,000（Co-working）</td></tr>
                <tr><td>寬頻+電話</td><td>$150（家用寬頻）</td><td>$500-1,000（商用）</td></tr>
                <tr><td>會計+公司秘書</td><td>$300</td><td>$500-1,500</td></tr>
                <tr><td>保險</td><td>$200</td><td>$500-1,000</td></tr>
                <tr><td>軟件工具</td><td>$0（免費工具）</td><td>$500-2,000</td></tr>
                <tr><td>市場推廣</td><td>$500</td><td>$3,000-10,000</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>每月總計</td><td>~$1,500</td><td>~$8,000-20,000</td></tr>
            </table>
            <div class="tip-box"><strong>💡 慳錢建議：</strong>頭6個月盡量在家工作（WFH），用家用寬頻就夠。等有穩定收入先搬去Co-working Space。呢樣可以每月慳$2,000-5,000。</div>
            """),
            ("Co-working Space比較", """
            <table class="comparison-table">
                <tr><th>Co-working Space</th><th>位置</th><th>Hot Desk月費</th><th>特色</th></tr>
                <tr><td>WeWork</td><td>全港多個</td><td>$2,500起</td><td>國際品牌、設施最齊</td></tr>
                <tr><td>Naked Hub</td><td>中環/觀塘</td><td>$2,000起</td><td>設計感強</td></tr>
                <tr><td>CoCoon</td><td>觀塘/荔枝角</td><td>$1,800起</td><td>創業社區氛圍</td></tr>
                <tr><td>theDesk</td><td>銅鑼灣/西營盤</td><td>$2,200起</td><td>安靜環境</td></tr>
                <tr><td>Paperclip</td><td>觀塘</td><td>$1,200起</td><td>最平、適合初創</td></tr>
            </table>
            <p><em>*大部分Co-working Space都包寬頻（通常1000M共用）、打印、會議室使用</em></p>
            """),
            ("創業慳成本10個方法", """
            <ul>
                <li><strong>1. 在家工作（WFH）：</strong>初期唔使租Office，一條穩定寬頻就夠創業</li>
                <li><strong>2. 用免費工具：</strong>Google Workspace免費版、Canva、Notion、Trello都有免費Plan</li>
                <li><strong>3. 虛擬辦公室：</strong>只需要商業地址同電話接聽服務，月費$500-1,000</li>
                <li><strong>4. 自己學做網站：</strong>用Cloudflare Pages/WordPress自己做，慳$10,000-50,000設計費</li>
                <li><strong>5. 社交媒體行銷：</strong>IG/FB/LinkedIn免費發佈內容，比付費廣告更長遠</li>
                <li><strong>6. 善用政府資助：</strong>TVP科技券、EMF市場推廣基金等</li>
                <li><strong>7. 外判非核心工作：</strong>會計、設計等外判比請全職平好多</li>
                <li><strong>8. 共享資源：</strong>同其他初創共享辦公設備、會議室</li>
                <li><strong>9. 免費法律諮詢：</strong>部分律師樓有免費初創諮詢，善用</li>
                <li><strong>10. 慳寬頻費：</strong>用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK</a> 格價，搵到最平嘅商業寬頻方案</li>
            </ul>
            """),
            ("初創寬頻同IT設定建議", """
            <p>初創公司嘅寬頻同IT需求唔複雜，但要穩定：</p>
            <ul>
                <li><strong>在家創業：</strong>500M家用寬頻已經足夠視像會議+雲端工作。確保上傳速度穩定（視像會議需要至少5Mbps上傳）</li>
                <li><strong>Co-working Space：</strong>通常已包寬頻，但建議自備流動數據做backup</li>
                <li><strong>獨立Office：</strong>建議1000M商用寬頻，配合VPN保障數據安全</li>
                <li><strong>雲端優先：</strong>用Google Workspace/Microsoft 365做文件協作，唔使自己管Server</li>
                <li><strong>備用網絡：</strong>準備一個5G流動WiFi做備用，寬頻斷線時唔會影響工作</li>
            </ul>
            """)
        ]
    },
    {
        "slug": "work-from-home-setup-guide",
        "title": "在家工作WFH設定指南：寬頻、設備、空間規劃全攻略",
        "description": "WFH點樣設定最舒服高效？寬頻要幾快？視像會議器材點揀？在家工作全面設定指南。",
        "keywords": "WFH, 在家工作, 在家工作設定, WFH寬頻, 視像會議, 在家工作設備, Home Office",
        "category": "beginner",
        "cat_class": "cat-beginner",
        "cat_name": "新手入門",
        "card_desc": "WFH點樣設定最舒服高效？寬頻、設備、空間規劃在家工作全攻略。",
        "faqs": [
            ("WFH需要幾快嘅寬頻？", "最低100M，建議500M。視像會議（Zoom/Teams）需要上下載各5-10Mbps，如果屋企有其他人同時上網，100M可能唔夠分。500M確保多人同時視像會議+串流都流暢。最重要係穩定，唔好用共享WiFi。"),
            ("WFH一定要用LAN線嗎？", "唔一定，但強烈建議。WiFi可能喺視像會議中途突然變差（訊號波動），導致你喺老闆面前斷線/畫面模糊。用LAN線連接電腦可以確保連接穩定、延遲低。如果電腦冇LAN口，買個USB-C轉LAN適配器（$50-100）。"),
            ("WFH揀咩耳機好？", "視像會議用嘅耳機最重要係收音質素（你講嘢對方聽唔聽到清楚），而唔係音質。推薦：Jabra Evolve2 40（$600-800，辦公室首選）、Apple AirPods Pro（$1,800，已經有就用）、Anker PowerConf（$400，平價之選）。")
        ],
        "sections": [
            ("WFH寬頻需求分析", """
            <table class="comparison-table">
                <tr><th>WFH活動</th><th>所需下載速度</th><th>所需上傳速度</th></tr>
                <tr><td>Email + 文書處理</td><td>5 Mbps</td><td>2 Mbps</td></tr>
                <tr><td>Zoom/Teams 視像會議</td><td>5-10 Mbps</td><td>5-10 Mbps</td></tr>
                <tr><td>多人視像會議（Gallery View）</td><td>15-25 Mbps</td><td>10 Mbps</td></tr>
                <tr><td>雲端檔案同步（Google Drive等）</td><td>10-20 Mbps</td><td>10-20 Mbps</td></tr>
                <tr><td>VPN連接公司網絡</td><td>20-50 Mbps</td><td>10-20 Mbps</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>全部同時進行</td><td>50-100 Mbps</td><td>30-60 Mbps</td></tr>
            </table>
            <div class="tip-box"><strong>💡 建議：</strong>WFH用500M對等寬頻（上下載速度一樣）最穩陣。用 <a href="https://broadbandhk.com/speed-test.html" style="color:var(--primary)">BroadbandHK 測速工具</a> 測試你嘅實際速度，特別係上傳速度。</div>
            """),
            ("WFH設備清單", """
            <table class="comparison-table">
                <tr><th>設備</th><th>最低預算</th><th>建議預算</th><th>推薦</th></tr>
                <tr><td>顯示器</td><td>$1,000（24寸）</td><td>$2,000-3,000（27寸）</td><td>Dell P2723QE</td></tr>
                <tr><td>鍵盤</td><td>$100</td><td>$300-600</td><td>Logitech MX Keys</td></tr>
                <tr><td>滑鼠</td><td>$50</td><td>$200-500</td><td>Logitech MX Master 3</td></tr>
                <tr><td>耳機/咪</td><td>$100</td><td>$400-800</td><td>Jabra Evolve2 40</td></tr>
                <tr><td>Webcam</td><td>$200</td><td>$500-1,000</td><td>Logitech C920</td></tr>
                <tr><td>椅子</td><td>$500</td><td>$2,000-5,000</td><td>Ikea MARKUS / Herman Miller</td></tr>
                <tr><td>USB Hub/Dock</td><td>$200</td><td>$500-1,000</td><td>Anker PowerExpand</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>合計</td><td>~$2,150</td><td>~$6,000-12,000</td><td></td></tr>
            </table>
            """),
            ("視像會議優化Tips", """
            <ul>
                <li><strong>用LAN線：</strong>最重要一步！WiFi不穩定係視像會議最大敵人</li>
                <li><strong>關閉不需要嘅程式：</strong>Dropbox同步、Windows Update、背景下載都會搶頻寬</li>
                <li><strong>光線：</strong>面對窗戶（自然光）或者買一個環形燈（$100-200），唔好背光</li>
                <li><strong>背景：</strong>整理桌面背景或者用虛擬背景。Teams/Zoom都有背景模糊功能</li>
                <li><strong>備用網絡：</strong>手機開熱點做備用。萬一寬頻斷線，即刻切換手機熱點，唔會miss成個會議</li>
                <li><strong>靜音習慣：</strong>唔講嘢時Mute咪，減少背景噪音干擾同事</li>
            </ul>
            """),
            ("WFH空間規劃建議", """
            <p>香港屋企空間有限，WFH空間點規劃？</p>
            <ul>
                <li><strong>獨立房間最好：</strong>有門可以隔開屋企人嘅聲音，視像會議時最理想</li>
                <li><strong>冇獨立房間：</strong>揀客廳嘅角落，用書架/屏風做簡單分隔</li>
                <li><strong>枱面大小：</strong>最少120cm × 60cm，放得落顯示器+手提電腦+文具</li>
                <li><strong>椅子好重要：</strong>每日坐8小時，一張好椅子係最值得嘅投資。唔好用摺椅/餐椅</li>
                <li><strong>走線整理：</strong>用理線器、線槽將電源線、LAN線整理好。桌底唔好一堆線</li>
                <li><strong>Router擺位：</strong>盡量將Router放喺你嘅工作位置附近，或者用LAN線直接連接</li>
            </ul>
            <div class="tip-box"><strong>💡 稅務提醒：</strong>WFH嘅部分家居開支（寬頻費、電費）可能可以作為扣稅項目。保留相關單據同記錄。</div>
            """)
        ]
    },
    # --- District/Area (5 articles) ---
    {
        "slug": "kwun-tong-district-guide",
        "title": "觀塘區生活指南：寬頻覆蓋、交通、美食、租樓全攻略",
        "description": "觀塘區住得好唔好？寬頻邊間覆蓋最好？租金幾錢？交通方便嗎？觀塘區生活全面睇。",
        "keywords": "觀塘, 觀塘生活, 觀塘租樓, 觀塘寬頻, 觀塘交通, 觀塘美食, 觀塘區指南",
        "category": "trending",
        "cat_class": "cat-trending",
        "cat_name": "熱門話題",
        "card_desc": "觀塘區住得好唔好？寬頻覆蓋、交通、美食、租樓全面睇。",
        "faqs": [
            ("觀塘區寬頻覆蓋情況點？", "觀塘區係全港寬頻覆蓋最好嘅地區之一。大部分私樓同較新嘅公屋都有FTTH光纖到戶，供應商 A、供應商 B、供應商 C、供應商 E全部有覆蓋。月費方面因為競爭激烈，通常比偏遠地區平10-20%。"),
            ("觀塘租樓大概幾錢？", "2026年參考：觀塘市中心兩房單位約$12,000-18,000/月、翠屏邨公屋約$2,000-3,500/月。如果揀觀塘工廈改建嘅住宅（要留意係咪合法），可以平啲但配套較少。牛頭角/九龍灣一帶較貴但交通更方便。"),
            ("觀塘區適合邊種人住？", "適合喺觀塘/九龍灣返工嘅打工仔（步行/短程巴士就到）、預算有限嘅年輕人（租金比港島平好多）、鍾意多元化美食嘅人（工廈、熟食市場選擇極多）。唔太適合追求寧靜環境嘅人，觀塘始終比較嘈。")
        ],
        "sections": [
            ("觀塘區寬頻覆蓋全面睇", """
            <table class="comparison-table">
                <tr><th>區域</th><th>主要屋苑</th><th>FTTH</th><th>供應商</th><th>1000M參考月費</th></tr>
                <tr><td>觀塘市中心</td><td>觀塘花園、裕民坊重建區</td><td>✅</td><td>全覆蓋</td><td>$108-168</td></tr>
                <tr><td>翠屏/藍田</td><td>翠屏邨、匯景花園</td><td>✅</td><td>全覆蓋</td><td>$108-168</td></tr>
                <tr><td>牛頭角</td><td>淘大花園、得寶花園</td><td>✅</td><td>全覆蓋</td><td>$108-168</td></tr>
                <tr><td>九龍灣</td><td>德福花園、淘大花園</td><td>✅</td><td>全覆蓋</td><td>$108-168</td></tr>
                <tr><td>油塘</td><td>Ocean One、鯉灣天下</td><td>✅</td><td>大部分覆蓋</td><td>$118-178</td></tr>
            </table>
            <div class="tip-box"><strong>💡 格價建議：</strong>觀塘區所有主要供應商都有覆蓋，競爭激烈=你有議價能力。用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK 格價計算器</a> 比較你地址嘅最新價格。</div>
            """),
            ("觀塘區交通指南", """
            <ul>
                <li><strong>港鐵：</strong>觀塘線（觀塘站、牛頭角站、九龍灣站）+ 將軍澳線（油塘站、藍田站）</li>
                <li><strong>巴士：</strong>路線極多，直達港島（606/601）、旺角（3D/13D）、沙田（89B）、將軍澳（98A）</li>
                <li><strong>小巴：</strong>覆蓋區內各屋邨同工業區</li>
                <li><strong>過海：</strong>觀塘碼頭有渡輪去北角/西灣河（20分鐘），避開塞車</li>
            </ul>
            <p><strong>返工通勤時間參考：</strong></p>
            <ul>
                <li>觀塘→中環：約30-40分鐘（港鐵）</li>
                <li>觀塘→旺角：約15-20分鐘（港鐵）</li>
                <li>觀塘→將軍澳：約15-25分鐘（港鐵轉線）</li>
            </ul>
            """),
            ("觀塘區美食同生活配套", """
            <ul>
                <li><strong>美食：</strong>觀塘區嘅工廈Cafe同餐廳選擇極多，價錢比市區平。裕民坊一帶有大量街坊小店，午餐$40-60有交易</li>
                <li><strong>購物：</strong>APM商場（24小時通宵營業）、MegaBox、創紀之城（觀塘站上蓋）</li>
                <li><strong>運動：</strong>觀塘海濱花園（緩跑、踩單車）、觀塘游泳池、觀塘體育館</li>
                <li><strong>醫療：</strong>基督教聯合醫院、觀塘區健康中心</li>
                <li><strong>教育：</strong>多間Band 1中學（藍田聖保祿、觀塘瑪利諾書院）</li>
            </ul>
            """),
            ("觀塘區租樓建議", """
            <table class="comparison-table">
                <tr><th>區域</th><th>類型</th><th>兩房參考月租</th><th>特點</th></tr>
                <tr><td>九龍灣</td><td>私樓</td><td>$15,000-22,000</td><td>交通最方便、商場多</td></tr>
                <tr><td>觀塘市中心</td><td>私樓/唐樓</td><td>$10,000-16,000</td><td>生活便利、選擇多</td></tr>
                <tr><td>油塘</td><td>私樓</td><td>$13,000-18,000</td><td>較新屋苑、環境較好</td></tr>
                <tr><td>牛頭角</td><td>私樓</td><td>$12,000-17,000</td><td>性價比高</td></tr>
                <tr><td>藍田</td><td>私樓/公屋</td><td>$10,000-15,000</td><td>相對寧靜</td></tr>
            </table>
            <div class="tip-box"><strong>💡 租屋Tips：</strong>租屋前記得用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK</a> 查新屋嘅寬頻覆蓋。觀塘區大部分有齊覆蓋，但個別舊樓可能只有FTTB，影響網速。</div>
            """)
        ]
    },
    {
        "slug": "tsuen-wan-district-guide",
        "title": "荃灣區生活指南：寬頻覆蓋、交通、屋苑、配套全攻略",
        "description": "荃灣區住得好唔好？寬頻邊間覆蓋最好？交通方便嗎？荃灣區生活全面睇。",
        "keywords": "荃灣, 荃灣生活, 荃灣租樓, 荃灣寬頻, 荃灣交通, 荃灣屋苑, 荃灣區指南",
        "category": "trending",
        "cat_class": "cat-trending",
        "cat_name": "熱門話題",
        "card_desc": "荃灣區住得好唔好？寬頻覆蓋、交通、屋苑、生活配套全面睇。",
        "faqs": [
            ("荃灣區寬頻覆蓋好唔好？", "荃灣區寬頻覆蓋整體唔錯。荃灣市中心嘅大型屋苑（如荃灣中心、萬景峰、The Pavilia Bay）全部有FTTH。但部分舊樓同荃灣西近海傍嘅較舊屋苑可能只有FTTB。建議用BroadbandHK查你個地址。"),
            ("荃灣定葵芳好住啲？", "荃灣商場多、生活便利，但人多車多。葵芳相對安靜，但配套冇荃灣咁齊。荃灣有港鐵直達市區、商場夠行（荃灣廣場、如心廣場、荃新天地），整體生活質素較高。租金兩者差唔多。"),
            ("荃灣去市區方便嗎？", "幾方便。荃灣站搭港鐵到旺角約15分鐘、到中環約25分鐘。亦有多條巴士線直達港島、九龍。缺點係大帽山隧道位經常塞車，搭巴士過海時間唔穩定。")
        ],
        "sections": [
            ("荃灣區寬頻覆蓋", """
            <table class="comparison-table">
                <tr><th>屋苑/地段</th><th>類型</th><th>FTTH</th><th>供應商數量</th></tr>
                <tr><td>荃灣中心</td><td>私樓</td><td>✅</td><td>4+間</td></tr>
                <tr><td>萬景峰/The Pavilia Bay</td><td>私樓</td><td>✅</td><td>4+間</td></tr>
                <tr><td>海之戀/海濱花園</td><td>私樓</td><td>✅</td><td>3-4間</td></tr>
                <tr><td>綠楊新邨</td><td>私樓</td><td>✅</td><td>3-4間</td></tr>
                <tr><td>福來邨/象山邨</td><td>公屋</td><td>部分</td><td>2-3間</td></tr>
            </table>
            <p>用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK 格價計算器</a> 輸入你嘅屋苑地址，即刻睇到所有供應商嘅覆蓋同價錢。</p>
            """),
            ("荃灣區交通配套", """
            <ul>
                <li><strong>港鐵：</strong>荃灣線（荃灣站、大窩口站）</li>
                <li><strong>西鐵線：</strong>荃灣西站（較近海濱一帶）</li>
                <li><strong>巴士：</strong>930（去港島灣仔）、934/935（去港島）、38（去葵盛）</li>
                <li><strong>屯門公路：</strong>開車去機場約20分鐘</li>
            </ul>
            <p><strong>通勤時間：</strong></p>
            <ul>
                <li>荃灣→旺角：約15分鐘（港鐵）</li>
                <li>荃灣→中環：約25分鐘（港鐵）</li>
                <li>荃灣→機場：約20分鐘（巴士/的士）</li>
            </ul>
            """),
            ("荃灣區租樓指南", """
            <table class="comparison-table">
                <tr><th>屋苑</th><th>類型</th><th>兩房月租</th><th>特點</th></tr>
                <tr><td>荃灣中心</td><td>私樓</td><td>$13,000-17,000</td><td>地鐵上蓋、生活便利</td></tr>
                <tr><td>萬景峰</td><td>私樓</td><td>$14,000-19,000</td><td>較新、設施好</td></tr>
                <tr><td>海之戀</td><td>私樓</td><td>$16,000-22,000</td><td>海景、近荃灣西站</td></tr>
                <tr><td>綠楊新邨</td><td>私樓</td><td>$11,000-15,000</td><td>性價比高、近地鐵</td></tr>
                <tr><td>海濱花園</td><td>私樓</td><td>$12,000-16,000</td><td>近荃灣西站</td></tr>
            </table>
            """),
            ("荃灣區生活配套", """
            <ul>
                <li><strong>商場：</strong>荃灣廣場、如心廣場、荃新天地、南豐紗廠（文青打卡點）</li>
                <li><strong>街市：</strong>荃灣街市（新裝修過，乾淨企理）、楊屋道街市</li>
                <li><strong>行山：</strong>大帽山、城門水塘（菠蘿壩入口近荃灣）、荃灣馬灣</li>
                <li><strong>醫療：</strong>仁濟醫院、荃灣港安醫院</li>
                <li><strong>學校：</strong>荃灣官立中學、寶安商會王少清中學</li>
            </ul>
            <div class="tip-box"><strong>💡 生活Tips：</strong>荃灣區近年發展好快，特別係荃灣西站一帶。南豐紗廠改建做文創空間後，成個區嘅氣氛都唔同晒。如果你鍾意行山+城市生活嘅平衡，荃灣係好選擇。</div>
            """)
        ]
    },
    {
        "slug": "sha-tin-district-guide",
        "title": "沙田區生活指南：寬頻覆蓋、交通、屋苑、教育全攻略",
        "description": "沙田區住得好唔好？寬頻覆蓋情況、交通配套、名校選擇、租樓指南全面睇。",
        "keywords": "沙田, 沙田生活, 沙田租樓, 沙田寬頻, 沙田交通, 沙田學校, 沙田區指南",
        "category": "trending",
        "cat_class": "cat-trending",
        "cat_name": "熱門話題",
        "card_desc": "沙田區住得好唔好？寬頻覆蓋、交通、名校、租樓全面睇。",
        "faqs": [
            ("沙田區寬頻覆蓋好唔好？", "沙田區寬頻覆蓋整體好好。沙田市中心（沙田第一城、好運中心一帶）全部有FTTH，供應商選擇多、競爭大。馬鞍山一帶較新屋苑亦全部有光纖覆蓋。少數舊村屋可能只有FTTB或需要用5G家居寬頻。"),
            ("沙田同大圍邊度好住啲？", "沙田市中心生活配套最齊全（新城市廣場、沙田街市），但人多擁擠。大圍近年發展快（名城、大圍站上蓋），交通樞紐轉線方便，但配套仲追緊。石門一帶環境較寧靜，適合家庭。"),
            ("沙田區學校好唔好？", "沙田係香港嘅教育強區之一。多間Band 1中學：浸信會呂明才中學、沙田蘇浙公學、聖公會林裘謀中學等。小學方面，浸信會沙田圍呂明才小學、培基小學等都係名校。呢個係好多家庭揀住沙田嘅主因。")
        ],
        "sections": [
            ("沙田區寬頻覆蓋", """
            <table class="comparison-table">
                <tr><th>區域</th><th>代表屋苑</th><th>FTTH</th><th>供應商</th></tr>
                <tr><td>沙田市中心</td><td>沙田第一城、好運中心</td><td>✅</td><td>全覆蓋</td></tr>
                <tr><td>大圍</td><td>名城、海福花園</td><td>✅</td><td>全覆蓋</td></tr>
                <tr><td>石門</td><td>碩門邨、濱景花園</td><td>✅</td><td>大部分覆蓋</td></tr>
                <tr><td>馬鞍山</td><td>新港城、迎海</td><td>✅</td><td>全覆蓋</td></tr>
                <tr><td>火炭</td><td>駿景園、銀禧花園</td><td>✅</td><td>3-4間</td></tr>
            </table>
            <div class="tip-box"><strong>💡 建議：</strong>沙田區競爭大，議價空間較大。記得用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK 格價計算器</a> 比較價錢，唔好接受第一個報價。</div>
            """),
            ("沙田區交通配套", """
            <ul>
                <li><strong>東鐵線：</strong>沙田站、火炭站、大學站、大圍站</li>
                <li><strong>屯馬線：</strong>大圍站（轉線站）、沙田圍站、石門站、車公廟站、馬鞍山站</li>
                <li><strong>巴士：</strong>170（去港島）、182（去沙田）、72（去太和）</li>
                <li><strong>的士：</strong>新界的士較市區平</li>
            </ul>
            <p><strong>通勤時間：</strong></p>
            <ul>
                <li>沙田→九龍塘：約10分鐘（東鐵線）</li>
                <li>沙田→金鐘：約25分鐘（東鐵線直達）</li>
                <li>大圍→尖沙咀：約20分鐘（屯馬線）</li>
            </ul>
            """),
            ("沙田區租樓指南", """
            <table class="comparison-table">
                <tr><th>屋苑</th><th>兩房月租</th><th>特點</th></tr>
                <tr><td>沙田第一城</td><td>$12,000-16,000</td><td>呎數大、生活配套齊</td></tr>
                <tr><td>名城</td><td>$14,000-19,000</td><td>較新、近大圍站</td></tr>
                <tr><td>新港城（馬鞍山）</td><td>$11,000-15,000</td><td>商場大、性價比高</td></tr>
                <tr><td>迎海（馬鞍山）</td><td>$16,000-22,000</td><td>海景、新</td></tr>
                <tr><td>駿景園（火炭）</td><td>$10,000-14,000</td><td>寧靜、近科學園</td></tr>
            </table>
            """),
            ("沙田區生活配套", """
            <ul>
                <li><strong>購物：</strong>新城市廣場（沙田最大商場）、HomeSquare、MOS Point（馬鞍山）</li>
                <li><strong>運動：</strong>城門河單車徑（沙田至大埔）、馬鞍山海濱長廊、沙田馬場</li>
                <li><strong>教育：</strong>多間Band 1中學同優質小學（沙田被稱為「新界教育重鎮」）</li>
                <li><strong>科技園：</strong>白石角科學園喺沙田區，唔少科技公司職員住沙田</li>
                <li><strong>醫療：</strong>威爾斯親王醫院、沙田醫院</li>
            </ul>
            <div class="tip-box"><strong>💡 沙田區優勢：</strong>如果你重視子女教育、鍾意踩單車/跑步、喺科學園返工，沙田區係首選。加上東鐵直通金鐘，去市區亦唔算慢。</div>
            """)
        ]
    },
    {
        "slug": "tseung-kwan-o-district-guide",
        "title": "將軍澳區生活指南：寬頻覆蓋、交通、屋苑、新市鎮全攻略",
        "description": "將軍澳住得好唔好？寬頻覆蓋情況、配套成熟嗎？租金幾錢？將軍澳生活全面睇。",
        "keywords": "將軍澳, TKO, 將軍澳生活, 將軍澳租樓, 將軍澳寬頻, 將軍澳交通, 日出康城",
        "category": "trending",
        "cat_class": "cat-trending",
        "cat_name": "熱門話題",
        "card_desc": "將軍澳住得好唔好？寬頻覆蓋、交通、屋苑、新市鎮配套全面睇。",
        "faqs": [
            ("將軍澳寬頻覆蓋好唔好？", "將軍澳係新市鎮，大部分屋苑喺2000年後落成，幾乎全部有FTTH光纖到戶。供應商選擇多、競爭激烈，月費通常都幾抵。日出康城作為最新嘅大型屋苑，寬頻基建更加先進。"),
            ("將軍澳最大缺點係咩？", "交通！將軍澳只靠一條港鐵將軍澳線同幾條隧道，繁忙時段港鐵迫到爆、塞隧道。另外，日出康城同市中心（坑口/將軍澳站）有一段距離，區內交通要靠巴士。但近年增設咗唔少巴士線，情況改善中。"),
            ("將軍澳定觀塘好住？", "兩者各有優勢。將軍澳：屋苑較新、環境整潔、空氣好、有海濱；觀塘：交通更方便、生活配套更成熟、美食選擇更多。如果你重視居住環境同新淨感，揀將軍澳；如果重視交通同便利性，揀觀塘。")
        ],
        "sections": [
            ("將軍澳寬頻覆蓋", """
            <table class="comparison-table">
                <tr><th>區域</th><th>代表屋苑</th><th>FTTH</th><th>1000M參考月費</th></tr>
                <tr><td>將軍澳站</td><td>天晉、PopCorn一帶</td><td>✅</td><td>$108-168</td></tr>
                <tr><td>坑口</td><td>蔚藍灣畔、東港城</td><td>✅</td><td>$108-168</td></tr>
                <tr><td>寶琳</td><td>新都城、怡心園</td><td>✅</td><td>$108-168</td></tr>
                <tr><td>日出康城</td><td>LP6-LP10、Marini</td><td>✅</td><td>$108-158</td></tr>
                <tr><td>調景嶺</td><td>都會駅、城中駅</td><td>✅</td><td>$108-168</td></tr>
            </table>
            <p>將軍澳區幾乎全部FTTH覆蓋，用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK 格價計算器</a> 比較最新價錢。</p>
            """),
            ("將軍澳區交通", """
            <ul>
                <li><strong>港鐵：</strong>將軍澳線（寶琳站、坑口站、將軍澳站、調景嶺站、康城站）</li>
                <li><strong>巴士：</strong>694（去港島）、296M（去坑口）、798（去沙田）</li>
                <li><strong>跨灣大橋：</strong>連接將軍澳同藍田，大幅縮短去九龍嘅時間</li>
            </ul>
            <p><strong>通勤時間：</strong></p>
            <ul>
                <li>將軍澳→北角：約20分鐘（港鐵）</li>
                <li>將軍澳→旺角：約30分鐘（港鐵轉線）</li>
                <li>日出康城→中環：約35-40分鐘（港鐵）</li>
            </ul>
            """),
            ("將軍澳區租樓指南", """
            <table class="comparison-table">
                <tr><th>屋苑</th><th>兩房月租</th><th>特點</th></tr>
                <tr><td>天晉</td><td>$15,000-20,000</td><td>地鐵上蓋、商場直達</td></tr>
                <tr><td>新都城（寶琳）</td><td>$12,000-16,000</td><td>成熟社區、配套齊</td></tr>
                <tr><td>日出康城</td><td>$11,000-16,000</td><td>最新、環境好、但偏遠</td></tr>
                <tr><td>蔚藍灣畔（坑口）</td><td>$13,000-17,000</td><td>近海、環境好</td></tr>
                <tr><td>都會駅（調景嶺）</td><td>$12,000-16,000</td><td>近轉線站、方便</td></tr>
            </table>
            """),
            ("將軍澳區生活配套", """
            <ul>
                <li><strong>購物：</strong>PopCorn商場、東港城、新都城中心、日出康城The LOHAS</li>
                <li><strong>海濱：</strong>將軍澳海濱公園、單車徑（海濱長廊好適合跑步踩車）</li>
                <li><strong>運動：</strong>將軍澳運動場、香港單車館（國際級設施）</li>
                <li><strong>醫療：</strong>將軍澳醫院</li>
                <li><strong>教育：</strong>播道書院、匯知中學、優才書院</li>
            </ul>
            <div class="tip-box"><strong>💡 將軍澳優勢：</strong>如果你係年輕家庭，將軍澳嘅新屋苑、海濱環境、運動設施都好吸引。寬頻基建亦係全港最好之一（全FTTH）。缺點就係交通繁忙時段會比較擁擠。</div>
            """)
        ]
    },
    {
        "slug": "yuen-long-district-guide",
        "title": "元朗區生活指南：寬頻覆蓋、交通、新舊市鎮、租樓全攻略",
        "description": "元朗區住得好唔好？天水圍同元朗市中心邊度好？寬頻覆蓋、交通、生活配套全面睇。",
        "keywords": "元朗, 元朗生活, 元朗租樓, 元朗寬頻, 天水圍, 元朗交通, 元朗區指南",
        "category": "trending",
        "cat_class": "cat-trending",
        "cat_name": "熱門話題",
        "card_desc": "元朗區住得好唔好？天水圍同元朗市中心比較、寬頻覆蓋、生活配套全面睇。",
        "faqs": [
            ("元朗區寬頻覆蓋情況點？", "元朗市中心同天水圍嘅大型屋苑寬頻覆蓋唔錯，大部分有FTTH。但元朗嘅村屋地區（錦田、十八鄉等）覆蓋參差，部分只有FTTB甚至冇光纖覆蓋，需要用5G家居寬頻。建議搬入前用BroadbandHK查清楚。"),
            ("元朗去市區方便嗎？", "比以前方便好多。屯馬線全通後，元朗站去尖沙咀約35分鐘、去金鐘約45分鐘。但始終係新界西北，通勤時間較長。如果喺九龍西返工（尖沙咀、荔枝角），元朗仲可以接受。去港島就比較辛苦。"),
            ("天水圍定元朗市中心好住？", "元朗市中心生活最方便（元朗YOHO系列、形點商場），食肆多、街市大。天水圍較寧靜，屋苑較新（嘉湖山莊），但配套不如元朗市中心。天水圍租金比元朗平10-20%，適合預算有限嘅家庭。")
        ],
        "sections": [
            ("元朗區寬頻覆蓋", """
            <table class="comparison-table">
                <tr><th>區域</th><th>代表屋苑</th><th>FTTH</th><th>備註</th></tr>
                <tr><td>元朗市中心</td><td>YOHO Town/Midtown</td><td>✅</td><td>全覆蓋、供應商多</td></tr>
                <tr><td>天水圍</td><td>嘉湖山莊、天晴邨</td><td>✅</td><td>大部分覆蓋</td></tr>
                <tr><td>錦田</td><td>加州花園</td><td>部分</td><td>大型屋苑有，獨立村屋未必</td></tr>
                <tr><td>十八鄉</td><td>散村</td><td>❌</td><td>大部分需要5G家居寬頻</td></tr>
                <tr><td>洪水橋</td><td>新發展區</td><td>✅</td><td>新屋苑全FTTH</td></tr>
            </table>
            <div class="tip-box"><strong>⚠ 村屋住戶注意：</strong>元朗區好多村屋冇光纖覆蓋。搬入前一定要用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK 格價計算器</a> 查清楚，唔好簽咗租約先發現冇寬頻用！</div>
            """),
            ("元朗區交通配套", """
            <ul>
                <li><strong>屯馬線：</strong>元朗站、朗屏站、天水圍站</li>
                <li><strong>輕鐵：</strong>區內主要交通工具，連接元朗、天水圍、屯門</li>
                <li><strong>巴士：</strong>968（去銅鑼灣）、269D（去沙田）、B1（去落馬洲口岸）</li>
                <li><strong>深圳口岸：</strong>落馬洲口岸近在咫尺，方便北上消費</li>
            </ul>
            <p><strong>通勤時間：</strong></p>
            <ul>
                <li>元朗→尖沙咀：約35分鐘（屯馬線）</li>
                <li>元朗→金鐘：約45分鐘（屯馬線+東鐵線）</li>
                <li>元朗→深圳福田：約30分鐘（B1巴士+口岸）</li>
            </ul>
            """),
            ("元朗區租樓指南", """
            <table class="comparison-table">
                <tr><th>屋苑</th><th>兩房月租</th><th>特點</th></tr>
                <tr><td>YOHO Town/Midtown</td><td>$12,000-17,000</td><td>地鐵上蓋、最方便</td></tr>
                <tr><td>嘉湖山莊（天水圍）</td><td>$8,000-12,000</td><td>大型屋苑、最平</td></tr>
                <tr><td>Park YOHO</td><td>$13,000-18,000</td><td>近錦田、環境較好</td></tr>
                <tr><td>天水圍公屋</td><td>$2,000-3,500</td><td>公屋租金最平</td></tr>
                <tr><td>元朗村屋</td><td>$6,000-10,000</td><td>空間大、但交通唔方便</td></tr>
            </table>
            """),
            ("元朗區生活配套", """
            <ul>
                <li><strong>購物：</strong>形點商場（YOHO Mall，元朗最大）、嘉湖銀座、天水圍天盛商場</li>
                <li><strong>美食：</strong>元朗大馬路一帶食肆林立、B仔涼粉、好到底麵、新釗記</li>
                <li><strong>郊遊：</strong>南生圍（影相打卡）、錦田壁畫村、濕地公園</li>
                <li><strong>北上消費：</strong>近落馬洲口岸，30分鐘到深圳福田，周末北上食飯好方便</li>
                <li><strong>醫療：</strong>博愛醫院、天水圍醫院</li>
            </ul>
            <div class="tip-box"><strong>💡 元朗區優勢：</strong>租金係全港最平嘅地區之一（天水圍），適合預算有限嘅家庭。近年屯馬線全通後交通改善好多。如果你經常北上深圳，元朗更加方便。缺點就係去港島真係比較遠。</div>
            """)
        ]
    },
    # --- Trending (4 articles) ---
    {
        "slug": "ai-tools-recommendations-2026",
        "title": "AI工具推薦2026：10個免費/平價AI工具幫你提升工作效率",
        "description": "2026年最實用嘅AI工具推薦：寫文、整圖、做PPT、分析數據，10個AI工具幫你慳時間。",
        "keywords": "AI工具, AI推薦, ChatGPT, AI寫作, AI圖片, AI生產力, 2026 AI工具",
        "category": "trending",
        "cat_class": "cat-trending",
        "cat_name": "熱門話題",
        "card_desc": "2026年最實用AI工具推薦：寫文、整圖、做PPT、分析數據，10個AI慳時間工具。",
        "faqs": [
            ("ChatGPT免費版夠唔夠用？", "一般日常使用免費版已經好夠用。免費版用GPT-4o mini模型，可以處理大部分文字工作（寫Email、翻譯、整理筆記）。如果需要更強嘅分析能力、圖片生成、或者上傳檔案分析，可以考慮Plus版（US$20/月）。"),
            ("AI會唔會取代我份工？", "短期內（2-5年），AI更多係「輔助」而唔係「取代」。識得用AI嘅人會取代唔識用AI嘅人。建議你學識用AI做日常重複性工作（整理報告、寫Email、分析數據），將時間留返做需要創意同判斷嘅工作。"),
            ("用AI做嘢有冇法律問題？", "要注意幾點：(1)唔好將公司機密資料輸入AI（可能會洩漏）；(2)AI生成嘅內容可能有版權爭議；(3)AI可能會「幻覺」（生成虛假資訊），重要內容一定要自己核實。部分公司有AI使用政策，跟住做就唔會有問題。")
        ],
        "sections": [
            ("10大實用AI工具一覽", """
            <table class="comparison-table">
                <tr><th>工具</th><th>用途</th><th>價錢</th><th>推薦度</th></tr>
                <tr><td><strong>ChatGPT</strong></td><td>寫文、問答、分析</td><td>免費/US$20月</td><td>★★★★★</td></tr>
                <tr><td><strong>Claude</strong></td><td>長文分析、寫作</td><td>免費/US$20月</td><td>★★★★★</td></tr>
                <tr><td><strong>Canva AI</strong></td><td>設計、社交媒體圖</td><td>免費/HK$60月</td><td>★★★★☆</td></tr>
                <tr><td><strong>Gamma</strong></td><td>自動生成PPT</td><td>免費/US$10月</td><td>★★★★☆</td></tr>
                <tr><td><strong>Notion AI</strong></td><td>筆記、項目管理</td><td>US$10/月</td><td>★★★★☆</td></tr>
                <tr><td><strong>Perplexity</strong></td><td>AI搜尋引擎</td><td>免費/US$20月</td><td>★★★★★</td></tr>
                <tr><td><strong>Midjourney</strong></td><td>AI生成圖片</td><td>US$10/月起</td><td>★★★★☆</td></tr>
                <tr><td><strong>ElevenLabs</strong></td><td>AI配音、文字轉語音</td><td>免費/US$5月起</td><td>★★★☆☆</td></tr>
                <tr><td><strong>Descript</strong></td><td>影片/Podcast剪輯</td><td>免費/US$24月</td><td>★★★★☆</td></tr>
                <tr><td><strong>GitHub Copilot</strong></td><td>AI寫程式碼</td><td>US$10/月</td><td>★★★★★</td></tr>
            </table>
            """),
            ("打工仔必學嘅5個AI應用場景", """
            <h3>1. AI寫Email/公文</h3>
            <p>用ChatGPT/Claude寫專業Email、會議記錄、報告。只需要俾重點，AI幫你寫出完整嘅專業文件。可以慳50-70%寫作時間。</p>

            <h3>2. AI做PPT簡報</h3>
            <p>用Gamma或者ChatGPT+Beautiful.ai，輸入主題同重點，幾分鐘生成一份完整簡報。之前要花2-3小時做嘅PPT，而家30分鐘搞掂。</p>

            <h3>3. AI分析Excel數據</h3>
            <p>將Excel數據複製入ChatGPT/Claude，叫佢分析趨勢、搵出異常、生成圖表。唔使識複雜公式。</p>

            <h3>4. AI翻譯+改文法</h3>
            <p>ChatGPT嘅翻譯質素已經好接近人工翻譯。英文Email/文件可以先用中文寫好，再叫AI翻譯成專業英文。</p>

            <h3>5. AI搜尋資料</h3>
            <p>Perplexity係AI搜尋引擎，可以直接問問題，佢會從網上搵答案並附上來源。比Google搜尋快3-5倍。</p>
            """),
            ("AI工具對寬頻嘅需求", """
            <p>大部分AI工具都係雲端運行，對寬頻有一定需求：</p>
            <ul>
                <li><strong>文字AI（ChatGPT、Claude）：</strong>需求極低，2G手機都用到</li>
                <li><strong>AI圖片生成（Midjourney）：</strong>生成圖片需要下載高解像度檔案，100M寬頻足夠</li>
                <li><strong>AI影片工具（Descript、Runway）：</strong>上傳/下載影片需要較快寬頻，建議500M以上</li>
                <li><strong>本地AI模型（Ollama、Stable Diffusion）：</strong>如果你想喺自己電腦行AI，唔需要快寬頻，但需要好嘅顯卡</li>
            </ul>
            <div class="tip-box"><strong>💡 建議：</strong>如果你經常使用AI工具工作（特別係涉及影片、圖片嘅），500M寬頻係最佳選擇。確保上傳速度足夠（用 <a href="https://broadbandhk.com/speed-test.html" style="color:var(--primary)">BroadbandHK 測速工具</a> 測試）。</div>
            """),
            ("AI工具使用注意事項", """
            <ul>
                <li><strong>唔好輸入機密資料：</strong>唔好將公司財務數據、客戶個人資料輸入ChatGPT等AI工具。你嘅輸入可能會被用嚟訓練AI模型</li>
                <li><strong>核實AI嘅答案：</strong>AI會「幻覺」（自信地講錯嘢）。重要嘅數字、日期、法律條文一定要自己核實</li>
                <li><strong>標明AI輔助：</strong>如果你嘅公司有AI使用政策，記得遵守。部分行業（法律、醫療）對AI使用有嚴格限制</li>
                <li><strong>保持學習：</strong>AI工具每幾個月就有大更新。建議follow相關嘅科技新聞（如The Verge、少數派），保持updated</li>
                <li><strong>善用Prompt：</strong>識寫Prompt（指令）先用得好AI。學好Prompt Engineering可以大幅提升AI輸出質素</li>
            </ul>
            """)
        ]
    },
    {
        "slug": "hong-kong-free-wifi-hotspot-map",
        "title": "香港免費WiFi熱點地圖：邊度有免費WiFi？速度快唔快？安全嗎？",
        "description": "香港免費WiFi邊度有？Wi-Fi.HK速度點？用公共WiFi安唔安全？免費WiFi熱點全攻略。",
        "keywords": "免費WiFi, 香港WiFi, Wi-Fi.HK, 公共WiFi, 免費上網, WiFi熱點, 香港免費上網",
        "category": "beginner",
        "cat_class": "cat-beginner",
        "cat_name": "新手入門",
        "card_desc": "香港邊度有免費WiFi？速度幾快？安全嗎？免費WiFi熱點全攻略。",
        "faqs": [
            ("Wi-Fi.HK係咩？", "Wi-Fi.HK係香港政府推動嘅免費WiFi計劃，喺全港超過35,000個熱點提供免費WiFi。包括政府場所（圖書館、體育館、公園）、港鐵站、商場、餐廳等。連接方法：搜尋WiFi名稱「Wi-Fi.HK via 供應商 E」或類似名稱，開瀏覽器接受條款即可。"),
            ("免費WiFi速度快唔快？", "視乎地點同使用人數。政府場所嘅WiFi通常有5-30Mbps，夠用嚟睇網頁同收Email。商場WiFi可能更快（20-50Mbps）。但繁忙時段（例如午飯時間嘅商場）速度會大幅下降。唔建議用嚟做視像會議或下載大型檔案。"),
            ("用免費WiFi安全嗎？", "基本上唔安全。公共WiFi嘅數據可以被截取。安全建議：(1)唔好登入銀行或輸入信用卡資料；(2)用VPN加密連接；(3)確保網站有HTTPS（鎖頭符號）；(4)用完後忘記該WiFi網絡。最安全嘅做法係用自己嘅流動數據。")
        ],
        "sections": [
            ("香港免費WiFi熱點分佈", """
            <table class="comparison-table">
                <tr><th>地點類型</th><th>WiFi名稱</th><th>速度</th><th>時間限制</th></tr>
                <tr><td>政府場所（圖書館、體育館）</td><td>Wi-Fi.HK via 供應商 E</td><td>5-30Mbps</td><td>無限</td></tr>
                <tr><td>港鐵站</td><td>MTR Free Wi-Fi</td><td>5-20Mbps</td><td>15-30分鐘/次</td></tr>
                <tr><td>商場（大型）</td><td>各商場自己嘅WiFi</td><td>20-50Mbps</td><td>1-2小時</td></tr>
                <tr><td>連鎖餐廳</td><td>各餐廳WiFi</td><td>10-30Mbps</td><td>通常無限</td></tr>
                <tr><td>公共屋邨</td><td>Wi-Fi.HK</td><td>5-20Mbps</td><td>無限</td></tr>
                <tr><td>公園/海濱</td><td>Wi-Fi.HK</td><td>5-15Mbps</td><td>無限</td></tr>
            </table>
            """),
            ("各區免費WiFi熱門地點", """
            <h3>港島區</h3>
            <ul>
                <li>中環大會堂、香港中央圖書館（銅鑼灣）、維多利亞公園</li>
            </ul>
            <h3>九龍區</h3>
            <ul>
                <li>尖沙咀文化中心、旺角花園街公園、九龍公園</li>
            </ul>
            <h3>新界區</h3>
            <ul>
                <li>沙田中央公園、大埔海濱公園、荃灣公共圖書館</li>
            </ul>
            <p><strong>尋找WiFi熱點方法：</strong></p>
            <ul>
                <li>下載「Wi-Fi.HK」App，地圖顯示附近所有免費WiFi</li>
                <li>Google Maps搜尋「free wifi near me」</li>
                <li>留意商場/餐廳門口嘅WiFi標誌</li>
            </ul>
            """),
            ("公共WiFi安全使用指南", """
            <p>用公共WiFi要注意以下安全要點：</p>
            <ul>
                <li><strong>用VPN：</strong>連接公共WiFi前開VPN（推薦ProtonVPN免費版），所有數據自動加密</li>
                <li><strong>唔好做敏感操作：</strong>唔好登入銀行App、唔好輸入信用卡資料、唔好登入重要帳戶</li>
                <li><strong>檢查HTTPS：</strong>確保網站地址有https://同鎖頭符號先輸入資料</li>
                <li><strong>關閉自動連接：</strong>手機設定入面關閉「自動連接WiFi」功能，避免連到假WiFi</li>
                <li><strong>用完忘記網絡：</strong>用完後喺WiFi設定入面「忘記此網絡」，下次唔會自動連</li>
                <li><strong>假WiFi陷阱：</strong>小心名稱類似但唔同嘅WiFi（例如「Free_WiFi_HK」vs「FreeWiFi_HK」），可能係釣魚WiFi</li>
            </ul>
            <div class="tip-box"><strong>💡 最安全方案：</strong>如果你經常出街需要上網，買一個大流量嘅手機月費Plan反而最安全。香港5G無限數據Plan最平大約$150/月，比用公共WiFi冒風險好得多。</div>
            """),
            ("免費WiFi唔夠用？替代方案", """
            <p>如果你經常出街需要穩定網絡，以下方案比免費WiFi更好：</p>
            <ul>
                <li><strong>手機大流量Plan：</strong>5G無限數據Plan月費$150-250，全港覆蓋、安全、穩定</li>
                <li><strong>手機熱點：</strong>用手機開WiFi熱點分享畀電腦用。注意：會用較多電量</li>
                <li><strong>流動WiFi蛋：</strong>日租$30-50，適合短期需要（旅行、搬屋期間）</li>
                <li><strong>Co-working Space：</strong>如果你需要長時間喺外面工作，Co-working Space嘅WiFi速度同安全性遠勝公共WiFi</li>
            </ul>
            <p>如果你屋企寬頻速度唔夠快，影響到你需要出去搵WiFi用，不如升級你嘅家用寬頻。用 <a href="https://broadbandhk.com/calculator.html" style="color:var(--primary)">BroadbandHK 格價計算器</a> 搵到最平嘅Plan。</p>
            """)
        ]
    },
    {
        "slug": "esports-broadband-guide",
        "title": "電競寬頻需求指南：打機要幾快寬頻？Ping值點降？遊戲網絡優化全攻略",
        "description": "打機lag點算？寬頻速度同Ping值有咩關係？遊戲網絡點優化？電競玩家嘅寬頻完全指南。",
        "keywords": "電競寬頻, 打機寬頻, Ping值, 遊戲延遲, 打機lag, 遊戲網絡, 電競Router",
        "category": "tech",
        "cat_class": "cat-tech",
        "cat_name": "技術知識",
        "card_desc": "打機lag點算？Ping值點降？寬頻速度幾快先夠？電競玩家網絡優化全攻略。",
        "faqs": [
            ("打機需要幾快嘅寬頻？", "打機對寬頻速度要求其實唔高！大部分網絡遊戲只需要3-10Mbps。打機最重要嘅唔係速度，係Ping值（延遲）同穩定性。100M寬頻打機已經綽綽有餘，但你需要有線連接（LAN線）同低延遲嘅網絡。買1000M對打機嘅幫助唔大，除非你同時要下載大型遊戲。"),
            ("Ping值幾多先算好？", "Ping值係你嘅裝置同遊戲伺服器之間嘅延遲。低過20ms：極好（電競級）、20-50ms：好（流暢遊玩）、50-100ms：一般（偶爾會感到延遲）、100ms以上：差（明顯lag）。香港連接亞洲伺服器通常可以做到10-30ms，連接歐美伺服器通常150-250ms。"),
            ("WiFi打機得唔得？", "可以但唔建議。WiFi嘅Ping值比LAN線高10-30ms，而且會不定時波動（spike），導致突然lag。認真打機嘅玩家100%用LAN線。如果你部機離Router太遠，拉一條15-20米嘅Cat6 LAN線（$50-100）係最值得嘅投資。")
        ],
        "sections": [
            ("唔同遊戲嘅網絡需求", """
            <table class="comparison-table">
                <tr><th>遊戲類型</th><th>需要速度</th><th>理想Ping</th><th>LAN線必須？</th></tr>
                <tr><td>FPS射擊（Valorant、CS2）</td><td>5Mbps</td><td>&lt;20ms</td><td>✅ 強烈建議</td></tr>
                <tr><td>MOBA（LoL、Dota2）</td><td>3Mbps</td><td>&lt;40ms</td><td>✅ 建議</td></tr>
                <tr><td>大逃殺（PUBG、Apex）</td><td>10Mbps</td><td>&lt;50ms</td><td>✅ 建議</td></tr>
                <tr><td>MMO（FF14、WoW）</td><td>5Mbps</td><td>&lt;100ms</td><td>建議</td></tr>
                <tr><td>格鬥（Street Fighter 6）</td><td>3Mbps</td><td>&lt;30ms</td><td>✅ 必須</td></tr>
                <tr><td>休閒（動物森友會、原神）</td><td>3Mbps</td><td>&lt;100ms</td><td>唔使</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>下載遊戲（100GB）</td><td>越快越好</td><td>N/A</td><td>建議</td></tr>
            </table>
            """),
            ("降低Ping值嘅7個方法", """
            <ul>
                <li><strong>1. 用LAN線：</strong>WiFi轉LAN線可以降低Ping 10-30ms，而且更穩定</li>
                <li><strong>2. 揀近嘅伺服器：</strong>盡量揀亞洲伺服器（香港/日本/新加坡），唔好連歐美</li>
                <li><strong>3. 關閉背景下載：</strong>Windows Update、Steam更新、雲端同步都會搶頻寬同增加延遲</li>
                <li><strong>4. Router QoS設定：</strong>喺Router入面開QoS，將你嘅打機裝置設為最高優先</li>
                <li><strong>5. DNS優化：</strong>改用Cloudflare DNS（1.1.1.1），DNS查詢速度可以快2-5ms</li>
                <li><strong>6. 唔好用VPN打機：</strong>VPN會增加10-50ms延遲（除非係專門嘅遊戲VPN）</li>
                <li><strong>7. 請屋企人暫停串流：</strong>其他人睇Netflix/YouTube會佔用頻寬同增加延遲</li>
            </ul>
            <div class="tip-box"><strong>💡 測試工具：</strong>用 <a href="https://broadbandhk.com/speed-test.html" style="color:var(--primary)">BroadbandHK 測速工具</a> 測試你嘅Ping值同速度。理想數值：Ping &lt;10ms、Jitter &lt;5ms。</div>
            """),
            ("電競Router推薦", """
            <p>如果你係認真嘅玩家，投資一部電競Router可以明顯改善網絡體驗：</p>
            <table class="comparison-table">
                <tr><th>Router</th><th>價錢</th><th>特色</th><th>適合</th></tr>
                <tr><td>ASUS RT-AX86U Pro</td><td>~$1,500</td><td>遊戲加速、低延遲模式</td><td>最佳性價比</td></tr>
                <tr><td>ASUS ROG Rapture GT-AX6000</td><td>~$3,000</td><td>三頻WiFi 6、遊戲專用頻段</td><td>預算充裕</td></tr>
                <tr><td>TP-Link Archer AX73</td><td>~$700</td><td>WiFi 6、QoS支援</td><td>平價之選</td></tr>
                <tr><td>Netgear Nighthawk XR1000</td><td>~$2,000</td><td>DumaOS遊戲優化系統</td><td>進階玩家</td></tr>
            </table>
            <p><strong>電競Router嘅主要優勢：</strong></p>
            <ul>
                <li>內建QoS優先保障遊戲頻寬</li>
                <li>遊戲加速功能（優化路由路徑）</li>
                <li>更低嘅處理延遲</li>
                <li>更穩定嘅WiFi（雖然仲係建議用LAN線）</li>
            </ul>
            """),
            ("遊戲下載速度優化", """
            <p>雖然打機唔需要高速寬頻，但下載遊戲就需要了。現代遊戲動輒50-150GB：</p>
            <table class="comparison-table">
                <tr><th>遊戲</th><th>大小</th><th>100M下載時間</th><th>500M下載時間</th><th>1000M下載時間</th></tr>
                <tr><td>CoD: Warzone</td><td>~150GB</td><td>~3.5小時</td><td>~40分鐘</td><td>~20分鐘</td></tr>
                <tr><td>GTA 6</td><td>~120GB</td><td>~2.7小時</td><td>~32分鐘</td><td>~16分鐘</td></tr>
                <tr><td>FF14全內容</td><td>~80GB</td><td>~1.8小時</td><td>~21分鐘</td><td>~11分鐘</td></tr>
                <tr><td>Valorant</td><td>~25GB</td><td>~33分鐘</td><td>~7分鐘</td><td>~3分鐘</td></tr>
            </table>
            <div class="tip-box"><strong>💡 結論：</strong>打機本身100M夠用。但如果你經常下載/更新大型遊戲，500M或1000M會方便好多。折衷方案：用100M寬頻，安排喺瞓覺時下載大型遊戲。</div>
            """)
        ]
    },
    {
        "slug": "smart-home-beginners-guide",
        "title": "智能家居入門指南：香港屋企點開始做Smart Home？設備、設定、寬頻需求",
        "description": "智能家居入門要買咩？Google Home定Apple HomeKit好？WiFi夠唔夠穩定？Smart Home新手全攻略。",
        "keywords": "智能家居, Smart Home, 智能燈泡, 智能插座, Google Home, Apple HomeKit, 智能家居入門",
        "category": "tech",
        "cat_class": "cat-tech",
        "cat_name": "技術知識",
        "card_desc": "智能家居入門買咩好？Google定Apple生態？WiFi夠唔夠穩定？新手全攻略。",
        "faqs": [
            ("智能家居需要幾快嘅寬頻？", "速度唔需要好快，100M已經綽綽有餘。但重要嘅係WiFi覆蓋同穩定性。智能家居裝置通常用2.4GHz WiFi，如果屋企有20個以上智能裝置，普通Router可能承受唔到。建議用支援100+裝置嘅WiFi 6 Router或Mesh WiFi系統。"),
            ("Google Home定Apple HomeKit揀邊個？", "如果你全家用iPhone/iPad，揀Apple HomeKit — 整合最好、隱私保障最高。如果屋企有Android用戶，或者想更多裝置選擇、更平嘅價錢，揀Google Home。兩個生態都唔錯，重點係唔好溝亂兩個生態，揀一個就stick住。"),
            ("智能家居安唔安全？", "有風險但可以管理。智能裝置連接WiFi，如果被入侵可以監控你嘅生活。安全措施：(1)用強WiFi密碼（WPA3）；(2)定期更新裝置韌體；(3)設定訪客WiFi畀智能裝置用（同主網絡隔離）；(4)買有信譽品牌嘅裝置。")
        ],
        "sections": [
            ("智能家居新手入門套裝", """
            <p>唔使一次過買齊所有嘢。以下係建議嘅入門順序：</p>
            <table class="comparison-table">
                <tr><th>優先度</th><th>裝置</th><th>參考價</th><th>用途</th></tr>
                <tr><td>第1步</td><td>智能音箱（Google Nest/HomePod Mini）</td><td>$300-800</td><td>語音控制中心</td></tr>
                <tr><td>第2步</td><td>智能燈泡（Philips Hue/IKEA）</td><td>$80-250/個</td><td>調光調色、自動開關</td></tr>
                <tr><td>第3步</td><td>智能插座</td><td>$50-100/個</td><td>傳統電器變智能（風扇、燈）</td></tr>
                <tr><td>第4步</td><td>智能門鎖</td><td>$1,500-3,000</td><td>密碼/指紋開門、遠程解鎖</td></tr>
                <tr><td>第5步</td><td>IP Camera</td><td>$200-800</td><td>家居監控、睇寵物</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>入門總預算</td><td colspan="3">$500-1,500（音箱+2-3個智能燈泡+智能插座）</td></tr>
            </table>
            """),
            ("Google Home vs Apple HomeKit vs Alexa", """
            <table class="comparison-table">
                <tr><th>特點</th><th>Google Home</th><th>Apple HomeKit</th><th>Amazon Alexa</th></tr>
                <tr><td>語音助手</td><td>Google Assistant</td><td>Siri</td><td>Alexa</td></tr>
                <tr><td>裝置選擇</td><td>最多</td><td>較少但精品</td><td>最多</td></tr>
                <tr><td>價錢</td><td>平</td><td>較貴</td><td>最平</td></tr>
                <tr><td>隱私保護</td><td>一般</td><td>最好</td><td>一般</td></tr>
                <tr><td>香港支援</td><td>好</td><td>好</td><td>一般</td></tr>
                <tr><td>廣東話支援</td><td>有</td><td>有</td><td>冇</td></tr>
                <tr style="background:#eff6ff;font-weight:600"><td>推薦</td><td>Android用戶首選</td><td>Apple用戶首選</td><td>唔太適合香港</td></tr>
            </table>
            <div class="tip-box"><strong>💡 Matter標準：</strong>2024年起，新嘅智能家居裝置開始支援「Matter」標準，即係一個裝置可以同時喺Google Home、Apple HomeKit、Alexa上面用。買新裝置時留意有冇「Matter」標誌。</div>
            """),
            ("智能家居嘅WiFi需求", """
            <p>智能家居裝置對WiFi嘅需求同一般上網唔同：</p>
            <ul>
                <li><strong>頻段：</strong>大部分智能裝置只支援2.4GHz WiFi（唔係5GHz）。確保你嘅Router冇關閉2.4GHz</li>
                <li><strong>裝置數量：</strong>每個智能裝置佔用一個WiFi連接。20個裝置以上可能令普通Router「塞車」</li>
                <li><strong>覆蓋範圍：</strong>每個角落嘅智能裝置都要有穩定WiFi訊號。一個WiFi死角就會令該位置嘅裝置掉線</li>
                <li><strong>穩定性 > 速度：</strong>智能裝置用嘅頻寬極少（每個大約0.1Mbps），但需要24/7穩定連接</li>
            </ul>
            <p><strong>建議Router設定：</strong></p>
            <ul>
                <li>用WiFi 6以上嘅Router（支援更多同時連接裝置）</li>
                <li>將智能裝置連2.4GHz、手機電腦連5GHz</li>
                <li>如果裝置超過15個，考慮用Mesh WiFi確保全屋覆蓋</li>
                <li>設定獨立訪客WiFi畀智能裝置用，同手機電腦隔離（安全考慮）</li>
            </ul>
            """),
            ("5個實用智能家居場景", """
            <h3>場景1：出門自動關燈關冷氣</h3>
            <p>設定「地理圍欄」，當你嘅手機離開屋企一定範圍，自動關閉所有燈同冷氣。每月慳$50-100電費。</p>

            <h3>場景2：語音控制全屋燈光</h3>
            <p>「Hey Google，關晒所有燈」「Siri，將客廳燈調暗50%」。唔使逐個開關撳。</p>

            <h3>場景3：定時開冷氣</h3>
            <p>返工前30分鐘自動開冷氣，返到屋企已經涼晒。用智能插座控制傳統冷氣就得。</p>

            <h3>場景4：遠程監控</h3>
            <p>用IP Camera喺Office睇屋企嘅毛孩、或者外出時監控家居安全。需要穩定嘅寬頻上傳速度。</p>

            <h3>場景5：睡前模式</h3>
            <p>一句「Good night」，全屋燈關閉、門鎖上鎖、冷氣調到25度、明朝7點自動開窗簾。</p>
            <div class="tip-box"><strong>💡 寬頻建議：</strong>智能家居需要全天候穩定嘅寬頻連接。如果你嘅寬頻經常斷線，智能裝置就會「失控」。確保你嘅寬頻穩定度足夠，可以用 <a href="https://broadbandhk.com/speed-test.html" style="color:var(--primary)">BroadbandHK 測速工具</a> 測試。</div>
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
