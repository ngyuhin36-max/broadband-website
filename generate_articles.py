#!/usr/bin/env python3
"""
BroadbandHK 高質量文章批量生成器
產出針對高搜尋量關鍵字嘅 SEO 文章
每篇文章都有完整 Schema.org、OG Tags、內部連結

用法：python generate_articles.py
"""

import os
import datetime

TODAY = datetime.date.today().strftime("%Y-%m-%d")
YEAR = datetime.date.today().strftime("%Y")
OUTPUT_DIR = "kb"

# ============================================================
# 文章定義：每篇針對一個高搜尋量關鍵字
# ============================================================
ARTICLES = [
    {
        "slug": "moving-checklist-2026",
        "title": f"{YEAR} 搬屋全攻略：搬屋前後 Checklist 完整版",
        "desc": f"{YEAR}年最完整搬屋 checklist！搬屋前、搬屋中、搬屋後要做嘅所有嘢，包括寬頻、水電煤、地址更改、搬屋公司揀選全部幫你列晒。",
        "keywords": "搬屋checklist, 搬屋攻略, 搬屋清單, 搬屋注意事項, 搬屋準備, 搬屋公司",
        "category": "生活攻略",
        "color": "#f97316",
        "content": f"""
            <p>搬屋係人生大事之一，要處理嘅嘢多到數唔晒。BroadbandHK 幫你整理咗一份最完整嘅搬屋 Checklist，由搬屋前一個月到搬入新屋之後，每一步都幫你諗好晒。</p>

            <h2>搬屋前 4 星期</h2>
            <ul>
                <li><strong>揀搬屋公司</strong> — 搵至少 3 間報價比較，記得問清楚有冇隱藏收費（樓梯費、大件傢俬費、泊車費）</li>
                <li><strong>斷捨離</strong> — 搬屋前係最好嘅清理時機，唔需要嘅嘢可以放上 Carousell 賣或者捐出去</li>
                <li><strong>通知寬頻公司</strong> — 提早安排新屋嘅寬頻安裝，避免搬入去冇網用。<a href="../moving.html" style="color:#2563eb;font-weight:600;">用 BroadbandHK 搬屋小幫手即刻查詢 →</a></li>
                <li><strong>學校通知</strong> — 如果有小朋友，要通知學校更改地址</li>
                <li><strong>寵物安排</strong> — 搬屋當日最好搵人幫手照顧寵物</li>
            </ul>

            <h2>搬屋前 2 星期</h2>
            <ul>
                <li><strong>水電煤轉名/過戶</strong> — 聯絡中電/港燈、煤氣公司、水務署安排截數同開新戶</li>
                <li><strong>地址更改</strong> — 銀行、信用卡、保險、政府（選民登記、車牌地址）、管理處</li>
                <li><strong>執包裝材料</strong> — 紙箱、氣泡紙、封箱膠紙、標記筆</li>
                <li><strong>貴重物品</strong> — 首飾、證件、現金自己帶，唔好交搬屋公司</li>
                <li><strong>影相記錄</strong> — 影低所有傢俬嘅位置，方便新屋擺位</li>
            </ul>

            <h2>搬屋前 1 星期</h2>
            <ul>
                <li><strong>確認搬屋公司</strong> — 再打電話確認時間、價錢、車輛大小</li>
                <li><strong>準備新屋</strong> — 如果可以，提早清潔新屋、量度傢俬位置</li>
                <li><strong>通知管理處</strong> — 新舊屋苑都要通知管理處，預約搬屋用升降機</li>
                <li><strong>冰箱清理</strong> — 搬屋前 2 日開始清雪櫃，避免食物浪費</li>
            </ul>

            <h2>搬屋當日</h2>
            <ul>
                <li><strong>最後檢查</strong> — 逐間房檢查，抽屜、櫃頂、露台都要睇</li>
                <li><strong>水電煤截數</strong> — 影低所有錶數，用手機影相做記錄</li>
                <li><strong>鎖匙交收</strong> — 舊屋鎖匙交返業主/代理</li>
                <li><strong>新屋驗收</strong> — 入伙前檢查水喉、電掣、窗戶有冇問題</li>
            </ul>

            <h2>搬屋後 1 星期</h2>
            <ul>
                <li><strong>寬頻安裝</strong> — 如果提早安排，搬入即有網用。<a href="https://api.whatsapp.com/send?phone=85252287541&text=你好，我剛搬屋想查詢寬頻安裝" style="color:#2563eb;font-weight:600;">WhatsApp BroadbandHK 即日安排 →</a></li>
                <li><strong>傢俬歸位</strong> — 大型傢俬先定位，再處理細件</li>
                <li><strong>鄰居打招呼</strong> — 尤其住唐樓或舊區，同鄰居建立好關係好重要</li>
                <li><strong>更新地址</strong> — 檢查有冇漏咗邊間公司/機構未更新地址</li>
            </ul>

            <div class="tip-box">
                <strong>BroadbandHK 貼士：</strong>搬屋最容易忘記嘅就係寬頻！好多人搬入新屋先發現冇網用，要等幾日先裝到。建議搬屋前至少 2 星期聯絡 BroadbandHK，我哋可以安排搬入當日就有網用。
            </div>
"""
    },
    {
        "slug": "home-wifi-setup-guide",
        "title": f"屋企 WiFi 全攻略：點樣設定先最快最穩？",
        "desc": "WiFi 慢唔一定係寬頻問題！教你正確擺放 Router 位置、設定最佳頻道、解決 WiFi 死角，全屋上網都暢順。",
        "keywords": "WiFi設定, Router位置, WiFi慢, WiFi死角, WiFi優化, 屋企WiFi",
        "category": "技術教室",
        "color": "#8b5cf6",
        "content": """
            <p>你有冇試過明明裝咗 1000M 寬頻，但屋企上網仲係好慢？問題可能唔係寬頻唔夠快，而係你嘅 WiFi 設定同 Router 擺位出咗問題。</p>

            <h2>Router 擺放位置 — 最影響 WiFi 速度嘅因素</h2>

            <h3>最佳位置</h3>
            <ul>
                <li><strong>屋企正中間</strong> — WiFi 訊號向四面八方擴散，擺正中間覆蓋最廣</li>
                <li><strong>離地 1-2 米</strong> — 放喺書櫃頂或者掛牆，唔好放地下</li>
                <li><strong>空曠位置</strong> — 避免放入櫃、電視後面或者角落</li>
            </ul>

            <h3>避開嘅位置</h3>
            <ul>
                <li><strong>廚房附近</strong> — 微波爐會干擾 WiFi 2.4GHz 頻道</li>
                <li><strong>金屬物件旁邊</strong> — 鏡、金屬櫃會反射同阻擋訊號</li>
                <li><strong>牆角/密閉空間</strong> — 訊號被牆壁吸收，覆蓋大減</li>
                <li><strong>地下</strong> — 訊號向下擴散嘅效率最差</li>
            </ul>

            <h2>2.4GHz vs 5GHz — 你應該用邊個？</h2>

            <table class="comparison-table">
                <tr>
                    <th>特性</th>
                    <th>2.4GHz</th>
                    <th>5GHz</th>
                </tr>
                <tr>
                    <td>速度</td>
                    <td>較慢（最高 ~300Mbps）</td>
                    <td>較快（最高 ~1,700Mbps）</td>
                </tr>
                <tr>
                    <td>覆蓋範圍</td>
                    <td>較遠、穿牆力強</td>
                    <td>較近、穿牆力弱</td>
                </tr>
                <tr>
                    <td>適合</td>
                    <td>遠距離、智能家電</td>
                    <td>近距離、打機、睇片</td>
                </tr>
                <tr>
                    <td>干擾</td>
                    <td>多（鄰居WiFi、微波爐）</td>
                    <td>少</td>
                </tr>
            </table>

            <div class="tip-box">
                <strong>BroadbandHK 建議：</strong>如果你 Router 支援雙頻，將常用裝置（手機、電腦）連 5GHz，智能燈泡、掃地機器人等連 2.4GHz。
            </div>

            <h2>WiFi 死角點解決？</h2>
            <ul>
                <li><strong>Mesh WiFi 系統</strong> — 最有效嘅方案，用 2-3 個節點覆蓋全屋。適合 800 呎以上單位</li>
                <li><strong>WiFi Extender</strong> — 平價選擇，但速度會減半。適合單一死角位</li>
                <li><strong>Powerline Adapter</strong> — 用家中電線傳輸網絡，穿牆力最強。適合舊樓厚牆</li>
                <li><strong>拉 LAN 線</strong> — 最穩定嘅方案，適合打機/WFH 嘅固定位置</li>
            </ul>

            <h2>即學即用：3 步提升 WiFi 速度</h2>
            <ol>
                <li><strong>重啟 Router</strong> — 最簡單有效，每個月重啟一次可以清除快取同記憶體洩漏</li>
                <li><strong>更改 WiFi 頻道</strong> — 用 WiFi Analyzer app 搵最少人用嘅頻道，避開鄰居干擾</li>
                <li><strong>更新 Router 韌體</strong> — 廠商會定期修復 bug 同提升速度，記得定期更新</li>
            </ol>

            <div class="tip-box">
                <strong>仲係慢？</strong>可能真係你嘅寬頻唔夠用。<a href="../speed-test.html" style="color:#2563eb;font-weight:600;">用 BroadbandHK 速度測試即刻檢查 →</a>
            </div>
"""
    },
    {
        "slug": "wfh-internet-tips",
        "title": f"{YEAR} 在家工作上網攻略：Zoom 唔再斷線",
        "desc": f"WFH 上網慢、Zoom 斷線、VPN 連唔到？教你用最少錢解決在家工作所有上網問題，提升工作效率。",
        "keywords": "WFH上網, 在家工作寬頻, Zoom斷線, VPN慢, 在家工作WiFi, 遙距工作上網",
        "category": "生活攻略",
        "color": "#3b82f6",
        "content": f"""
            <p>越來越多香港公司實行混合辦公模式，在家工作已經成為日常。但 WFH 最令人頭痛嘅，就係上網問題 — Zoom 開會斷線、VPN 慢到死、同事 share screen 睇唔到⋯⋯</p>

            <h2>WFH 需要幾多 M 寬頻？</h2>

            <table class="comparison-table">
                <tr>
                    <th>工作類型</th>
                    <th>最低網速</th>
                    <th>建議網速</th>
                </tr>
                <tr>
                    <td>文書處理 + Email</td>
                    <td>10M</td>
                    <td>50M</td>
                </tr>
                <tr>
                    <td>Zoom/Teams 視像會議</td>
                    <td>25M</td>
                    <td>100M</td>
                </tr>
                <tr>
                    <td>Share Screen + 多人會議</td>
                    <td>50M</td>
                    <td>200M</td>
                </tr>
                <tr>
                    <td>VPN 連公司網絡</td>
                    <td>50M</td>
                    <td>200M</td>
                </tr>
                <tr>
                    <td>設計/剪片/大檔案傳輸</td>
                    <td>200M</td>
                    <td>500M-1000M</td>
                </tr>
                <tr>
                    <td>程式開發（Git push/pull）</td>
                    <td>50M</td>
                    <td>200M</td>
                </tr>
            </table>

            <div class="tip-box">
                <strong>注意：</strong>以上係一個人嘅需求。如果你同屋企人同時上網（例如你開 Zoom，小朋友睇 YouTube），需要將數字加倍。一家四口 WFH + 上網，建議至少 500M。
            </div>

            <h2>Zoom 斷線 5 大原因同解決方法</h2>
            <ol>
                <li><strong>WiFi 訊號弱</strong> — 坐近 Router 或者用 LAN 線直駁電腦</li>
                <li><strong>頻寬唔夠</strong> — 開會時請屋企人暫停睇 Netflix/YouTube</li>
                <li><strong>Router 過熱</strong> — 夏天 Router 容易過熱降速，放喺通風位置</li>
                <li><strong>背景程式佔頻寬</strong> — 關閉 OneDrive/Dropbox 自動同步</li>
                <li><strong>寬頻本身慢</strong> — <a href="../speed-test.html" style="color:#2563eb;font-weight:600;">即刻測試你嘅網速 →</a></li>
            </ol>

            <h2>VPN 慢嘅解決方案</h2>
            <ul>
                <li><strong>揀近嘅 VPN 伺服器</strong> — 連香港或者新加坡，唔好連美國</li>
                <li><strong>改用 WireGuard 協議</strong> — 比 OpenVPN 快 30-50%</li>
                <li><strong>分流設定</strong> — 只將公司流量行 VPN，其他正常上網</li>
                <li><strong>升級寬頻</strong> — VPN 會將速度降低 20-40%，如果底速唔夠就會好明顯</li>
            </ul>

            <h2>WFH 最佳網絡設定</h2>
            <ul>
                <li>工作電腦盡量用 <strong>LAN 線直駁 Router</strong>，比 WiFi 穩定好多</li>
                <li>將 Router 放喺 <strong>工作枱附近</strong></li>
                <li>開會前 <strong>關閉雲端同步</strong>（OneDrive、Google Drive、iCloud）</li>
                <li>如果同事多人同時開會，考慮 <strong>錯開時間</strong> 或者 <strong>關閉鏡頭</strong> 慳頻寬</li>
            </ul>

            <div class="tip-box">
                <strong>BroadbandHK 建議：</strong>WFH 用家最少需要 100M 寬頻。如果你成日要開視像會議 + 用 VPN，建議升級到 500M。<a href="https://api.whatsapp.com/send?phone=85252287541&text=你好，我在家工作想查詢適合嘅寬頻方案" style="color:#2563eb;font-weight:600;">WhatsApp 查詢最適合你嘅方案 →</a>
            </div>
"""
    },
    {
        "slug": "parental-control-setup",
        "title": "小朋友上網安全：家長控制設定完全指南",
        "desc": "教你喺 Router、手機、電腦設定家長控制，限制上網時間、過濾不良內容、監控上網活動。保護小朋友安全上網。",
        "keywords": "家長控制, 小朋友上網安全, 兒童上網, 限制上網時間, 過濾網站, Router家長控制",
        "category": "家長指南",
        "color": "#10b981",
        "content": """
            <p>香港小朋友平均每日上網超過 3 小時，接觸到不良內容嘅風險越來越高。作為家長，與其完全禁止上網，不如學識點樣設定「安全網」，畀小朋友安全地使用互聯網。</p>

            <h2>方法一：Router 層面設定（最有效）</h2>
            <p>喺 Router 設定家長控制，可以一次過管理屋企所有裝置，小朋友點都避唔開。</p>

            <h3>設定步驟</h3>
            <ol>
                <li>打開瀏覽器，輸入 <strong>192.168.1.1</strong>（或 Router 底部標示嘅地址）</li>
                <li>登入管理頁面（預設帳號密碼通常印喺 Router 底部）</li>
                <li>搵到 <strong>「Parental Control」</strong> 或 <strong>「家長控制」</strong> 選項</li>
                <li>新增小朋友嘅裝置（用 MAC 地址識別）</li>
                <li>設定上網時間限制（例如：22:00 後禁止上網）</li>
                <li>啟用網站過濾（封鎖不良內容分類）</li>
            </ol>

            <h2>方法二：裝置層面設定</h2>

            <h3>iPhone / iPad</h3>
            <ol>
                <li>設定 → 螢幕使用時間 → 開啟</li>
                <li>設定「停用時間」（例如 21:00-07:00）</li>
                <li>App 限制 → 限制社交媒體、遊戲每日使用時間</li>
                <li>內容與私隱限制 → 封鎖成人網站</li>
            </ol>

            <h3>Android</h3>
            <ol>
                <li>安裝 Google Family Link app</li>
                <li>建立小朋友嘅 Google 帳戶</li>
                <li>設定每日屏幕時間上限</li>
                <li>管理可以安裝嘅 App</li>
                <li>查看位置同上網報告</li>
            </ol>

            <h2>方法三：DNS 過濾（零成本）</h2>
            <p>將 Router 嘅 DNS 改為家庭安全 DNS，自動過濾不良網站：</p>
            <ul>
                <li><strong>Cloudflare Family</strong> — 1.1.1.3（封鎖惡意軟件 + 成人內容）</li>
                <li><strong>OpenDNS Family</strong> — 208.67.222.123</li>
                <li><strong>CleanBrowsing</strong> — 185.228.168.168</li>
            </ul>

            <div class="tip-box">
                <strong>設定方法：</strong>Router 管理頁面 → WAN/Internet 設定 → 將 DNS 改為以上任何一組 → 儲存 → 重啟 Router。全屋所有裝置即刻生效。
            </div>

            <h2>唔同年齡嘅上網建議</h2>

            <table class="comparison-table">
                <tr>
                    <th>年齡</th>
                    <th>每日上網時間</th>
                    <th>建議設定</th>
                </tr>
                <tr>
                    <td>3-6 歲</td>
                    <td>最多 1 小時</td>
                    <td>只允許教育 App，全程陪伴</td>
                </tr>
                <tr>
                    <td>7-12 歲</td>
                    <td>最多 2 小時</td>
                    <td>DNS 過濾 + 時間限制 + App 白名單</td>
                </tr>
                <tr>
                    <td>13-17 歲</td>
                    <td>視乎需要</td>
                    <td>DNS 過濾 + 定期檢查 + 開放溝通</td>
                </tr>
            </table>

            <div class="tip-box">
                <strong>BroadbandHK 提醒：</strong>技術手段只係輔助，最重要嘅係同小朋友建立信任同溝通。教佢哋點樣分辨好壞資訊，比封鎖更加有效。
            </div>
"""
    },
    {
        "slug": "broadband-renewal-negotiation",
        "title": f"{YEAR} 寬頻續約議價攻略：教你 3 步拎到最低價",
        "desc": f"寬頻合約到期唔好急住續！教你點樣用 3 步議價策略，拎到比新客更平嘅月費。附 {YEAR} 年最新市場行情參考。",
        "keywords": "寬頻續約, 寬頻議價, 寬頻減價, 合約到期, 寬頻轉台, 寬頻慳錢",
        "category": "慳錢攻略",
        "color": "#eab308",
        "content": f"""
            <p>寬頻合約到期，係你最有議價能力嘅時刻。因為寬頻公司留住一個舊客嘅成本，遠低過搵一個新客。只要你識得點傾，絕對可以拎到比原價平好多嘅月費。</p>

            <h2>第一步：知道自己嘅底牌</h2>
            <p>議價之前，你需要準備以下資料：</p>
            <ul>
                <li><strong>你現有嘅合約月費</strong> — 睇清楚每月畀幾多</li>
                <li><strong>合約到期日</strong> — 過咗到期日你就係「自由身」，隨時可以走。<a href="../reminder.html" style="color:#2563eb;font-weight:600;">用合約到期提醒工具 →</a></li>
                <li><strong>市場行情</strong> — 其他供應商同類計劃嘅價錢</li>
                <li><strong>你嘅用量</strong> — 你真正需要幾多 M？100M 定 500M 定 1000M？</li>
            </ul>

            <h2>第二步：三步議價法</h2>

            <h3>Step 1：表示想「取消」而唔係「續約」</h3>
            <p>打電話去寬頻公司，講你想<strong>取消服務</strong>，唔係續約。佢哋通常會即刻轉你去「客戶挽留組」— 呢個先係有權畀你優惠嘅部門。</p>

            <h3>Step 2：講出你嘅替代選擇</h3>
            <p>同客服講：「我已經查過其他供應商嘅價錢，佢哋 500M 月費只要 $1XX，仲免安裝費送 Router。如果你哋冇更好嘅方案，我就會轉。」</p>
            <p>重點：唔需要講邊間，只需要令對方知道你有選擇。</p>

            <h3>Step 3：唔好即刻答應</h3>
            <p>客服畀你嘅第一個 offer 通常唔係最好。你可以講：「我考慮下先，聽日覆你。」掛線之後，通常幾日內佢哋會再打畀你，畀一個更好嘅 offer。</p>

            <div class="tip-box">
                <strong>秘技：</strong>如果你真係唔想自己傾，可以直接 <a href="https://api.whatsapp.com/send?phone=85252287541&text=你好，我想查詢寬頻續約有冇更好嘅方案" style="color:#2563eb;font-weight:600;">WhatsApp BroadbandHK</a>，我哋免費幫你比較同配對最啱嘅方案，唔使自己逐間打電話傾。
            </div>

            <h2>第三步：知道幾時走</h2>
            <p>如果傾極都傾唔到好價錢，就真係轉。唔好因為怕煩而繼續畀貴月費。</p>
            <ul>
                <li>轉台嘅安裝費通常新供應商會包</li>
                <li>大部分情況下當日申請，翌日就可以安裝</li>
                <li>Router 通常都係免費送</li>
            </ul>

            <h2>{YEAR} 年寬頻月費參考範圍</h2>

            <table class="comparison-table">
                <tr>
                    <th>速度</th>
                    <th>合理月費範圍</th>
                    <th>太貴嘅指標</th>
                </tr>
                <tr>
                    <td>100M</td>
                    <td>$78 - $128</td>
                    <td>超過 $150</td>
                </tr>
                <tr>
                    <td>500M</td>
                    <td>$128 - $178</td>
                    <td>超過 $200</td>
                </tr>
                <tr>
                    <td>1000M</td>
                    <td>$178 - $248</td>
                    <td>超過 $280</td>
                </tr>
            </table>

            <p>如果你而家嘅月費超過「太貴指標」，就一定要行動。每個月慳 $50，一年就係 $600。</p>
"""
    },
]


def generate_article(article):
    """Generate a single KB article HTML file."""
    slug = article["slug"]
    title = article["title"]
    desc = article["desc"]
    keywords = article["keywords"]
    category = article["category"]
    color = article["color"]
    content = article["content"]

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — BroadbandHK 寬頻專家</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://broadbandhk.com/kb/{slug}.html">

    <script async src="https://www.googletagmanager.com/gtag/js?id=G-23EZE5P385"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-23EZE5P385');
        gtag('config', 'AW-959473638');
    </script>

    <meta property="og:type" content="article">
    <meta property="og:url" content="https://broadbandhk.com/kb/{slug}.html">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:locale" content="zh_HK">
    <meta property="og:image" content="https://broadbandhk.com/og-image.png">
    <meta property="og:site_name" content="BroadbandHK 寬頻專家">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="https://broadbandhk.com/og-image.png">

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "datePublished": "{TODAY}",
        "dateModified": "{TODAY}",
        "author": {{"@type": "Organization", "name": "BroadbandHK 寬頻專家"}},
        "publisher": {{"@type": "Organization", "name": "BroadbandHK 寬頻專家"}},
        "mainEntityOfPage": {{"@type": "WebPage", "@id": "https://broadbandhk.com/kb/{slug}.html"}}
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
        .kb-article ul, .kb-article ol {{ margin: 16px 0; padding-left: 24px; }}
        .kb-article li {{ color: var(--gray); margin-bottom: 8px; line-height: 1.8; }}
        .kb-date {{ color: var(--gray); font-size: 0.85rem; margin-bottom: 20px; }}
        .tip-box {{ background: #fef3c7; border-left: 4px solid var(--accent); padding: 20px 24px; border-radius: 0 8px 8px 0; margin: 24px 0; }}
        .tip-box strong {{ color: var(--dark); }}
        .comparison-table {{ width: 100%; border-collapse: collapse; margin: 24px 0; }}
        .comparison-table th, .comparison-table td {{ padding: 14px 16px; text-align: center; border-bottom: 1px solid #e2e8f0; font-size: 0.95rem; }}
        .comparison-table th {{ background: var(--primary); color: var(--white); font-weight: 700; }}
        .comparison-table tr:nth-child(even) {{ background: var(--light); }}
        .related-articles {{ margin-top: 48px; padding: 32px; background: var(--light); border-radius: var(--radius); }}
        .related-articles h3 {{ font-size: 1.2rem; margin-bottom: 16px; }}
        .related-articles a {{ display: block; color: var(--primary); text-decoration: none; padding: 8px 0; font-weight: 500; }}
        .related-articles a:hover {{ text-decoration: underline; }}
        .back-link {{ display: inline-block; margin-top: 32px; color: var(--primary); text-decoration: none; font-weight: 700; }}
        @media (max-width: 768px) {{ .kb-article {{ padding: 28px 20px; }} .kb-hero h1 {{ font-size: 1.8rem; }} }}
    </style>
</head>
<body>

<nav class="navbar">
    <div class="container nav-container">
        <a href="../index.html" class="logo">⚡ BroadbandHK</a>
        <ul class="nav-links">
            <li><a href="../index.html#plans">寬頻方案</a></li>
            <li><a href="../blog.html">攻略文章</a></li>
            <li><a href="../partner.html">合作夥伴</a></li>
            <li><a href="../index.html#contact">聯絡我們</a></li>
        </ul>
        <a href="https://api.whatsapp.com/send?phone=85252287541" class="btn btn-small">WhatsApp 查詢</a>
    </div>
</nav>

<section class="kb-hero">
    <div class="container">
        <div class="kb-breadcrumb"><a href="../index.html">首頁</a> &gt; <a href="../blog.html">攻略文章</a> &gt; {category}</div>
        <h1>{title}</h1>
        <p>{desc[:80]}...</p>
    </div>
</section>

<section class="kb-content">
    <div class="container">
        <div class="kb-article">
            <p class="kb-date">{TODAY} · {category}</p>
            {content}

            <div class="related-articles">
                <h3>相關文章</h3>
                <a href="moving-broadband-guide.html">搬屋寬頻安排全攻略</a>
                <a href="broadband-hidden-fees.html">寬頻隱藏收費大揭秘</a>
                <a href="router-guide.html">Router 選購終極指南</a>
                <a href="wifi-dead-zones-fix.html">WiFi 死角完全解決方案</a>
            </div>

            <a href="../blog.html" class="back-link">← 返回全部文章</a>
        </div>
    </div>
</section>

<section class="cta" style="text-align:center;padding:60px 0;background:linear-gradient(135deg,#0f172a,#1e3a5f);">
    <div class="container">
        <h2 style="color:#fff;font-size:1.8rem;margin-bottom:12px;">寬頻嘅嘢，問 BroadbandHK 就得</h2>
        <p style="color:rgba(255,255,255,0.7);margin-bottom:24px;">免費寬頻顧問，幫你搵最適合嘅方案</p>
        <a href="https://api.whatsapp.com/send?phone=85252287541&text=你好，我想查詢寬頻方案" class="btn btn-primary btn-large" style="background:#22c55e;">WhatsApp 免費查詢</a>
    </div>
</section>

<footer class="footer">
    <div class="container">
        <div class="footer-bottom">
            &copy; {YEAR} BroadbandHK 寬頻專家. All rights reserved. | <a href="../index.html" style="color:rgba(255,255,255,0.6);">返回首頁</a>
        </div>
    </div>
</footer>

</body>
</html>"""
    return html


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    generated = []
    for article in ARTICLES:
        filepath = os.path.join(OUTPUT_DIR, f"{article['slug']}.html")
        html = generate_article(article)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        generated.append(article)
        print(f"  OK {filepath}")

    print(f"\n共生成 {len(generated)} 篇文章")
    print("下一步：git add kb/ && git commit && git push")


if __name__ == "__main__":
    main()
