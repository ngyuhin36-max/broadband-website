// ===== Mobile Menu =====
function toggleMobileMenu() {
    document.getElementById('navLinks').classList.toggle('open');
    document.querySelector('.hamburger').classList.toggle('active');
}
document.querySelectorAll('.nav-dropdown > a').forEach(function(link) {
    link.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            e.preventDefault();
            this.parentElement.classList.toggle('open');
        }
    });
});

// ===== Hero Carousel =====
let currentSlide = 0;
const totalSlides = 3;
let autoSlideInterval;

function updateSlide() {
    document.getElementById('heroSlides').style.transform = `translateX(-${currentSlide * 100}%)`;
    document.querySelectorAll('.carousel-dot').forEach((dot, i) => {
        dot.classList.toggle('active', i === currentSlide);
    });
}

function moveSlide(dir) {
    currentSlide = (currentSlide + dir + totalSlides) % totalSlides;
    updateSlide();
    resetAutoSlide();
}

function goToSlide(index) {
    currentSlide = index;
    updateSlide();
    resetAutoSlide();
}

function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    autoSlideInterval = setInterval(() => moveSlide(1), 5000);
}

autoSlideInterval = setInterval(() => moveSlide(1), 5000);

// ===== Navbar Scroll Effect =====
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.boxShadow = '0 4px 24px rgba(0,0,0,0.2)';
    } else {
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.15)';
    }
});

// ===== AI ChatBot =====
(function() {
    const PLANS = {
        basic: { name: '基本版', speed: '100Mbps', price: '$98/月', people: '1-2人', use: '上網、串流、社交媒體' },
        advanced: { name: '進階版', speed: '500Mbps', price: '$158/月', people: '3-4人', use: '家庭、在家工作、4K串流' },
        premium: { name: '極速版', speed: '1000Mbps', price: '$228/月', people: '5人以上', use: '重度使用、打機、直播' }
    };

    const MENU = {
        main: {
            text: '你好！我係 BroadbandHK 寬頻顧問 👋\n有咩可以幫到你？',
            options: [
                { label: '📋 邊個計劃適合我？', action: 'recommend' },
                { label: '💰 月費幾錢？', action: 'pricing' },
                { label: '🏠 我要搬屋轉寬頻', action: 'moving' },
                { label: '⚡ 安裝要等幾耐？', action: 'install' },
                { label: '❓ 其他問題', action: 'other' }
            ]
        },
        recommend: {
            text: '想幫你搵最適合嘅計劃！你屋企有幾多人用 WiFi？',
            options: [
                { label: '1-2 人', action: 'rec_basic' },
                { label: '3-4 人', action: 'rec_advanced' },
                { label: '5 人或以上', action: 'rec_premium' }
            ]
        },
        rec_basic: {
            text: '推薦你 <b>基本版 100Mbps</b> 💡\n\n✅ 月費：<b>$98/月</b>\n✅ 速度：100Mbps\n✅ 免安裝費\n✅ 送 Wi-Fi Router\n\n1-2 人日常上網、睇片、社交媒體絕對夠用！',
            options: [
                { label: '✅ 我想申請', action: 'apply_basic' },
                { label: '🔄 睇其他計劃', action: 'pricing' },
                { label: '↩️ 返回主選單', action: 'main' }
            ]
        },
        rec_advanced: {
            text: '推薦你 <b>進階版 500Mbps</b> 🚀\n\n✅ 月費：<b>$158/月</b>\n✅ 速度：500Mbps\n✅ 免安裝費\n✅ 送 Wi-Fi Router\n\n3-4 人家庭、在家工作、4K 串流都好流暢！',
            options: [
                { label: '✅ 我想申請', action: 'apply_advanced' },
                { label: '🔄 睇其他計劃', action: 'pricing' },
                { label: '↩️ 返回主選單', action: 'main' }
            ]
        },
        rec_premium: {
            text: '推薦你 <b>極速版 1000Mbps</b> ⚡\n\n✅ 月費：<b>$228/月</b>\n✅ 速度：1000Mbps（1G 極速）\n✅ 免安裝費\n✅ 送 Wi-Fi Router\n\n5 人以上、打機、直播、多裝置同時用都冇問題！',
            options: [
                { label: '✅ 我想申請', action: 'apply_premium' },
                { label: '🔄 睇其他計劃', action: 'pricing' },
                { label: '↩️ 返回主選單', action: 'main' }
            ]
        },
        pricing: {
            text: '我哋有 3 個計劃：\n\n💡 <b>基本版 100M — $98/月</b>\n　 適合 1-2 人\n\n🚀 <b>進階版 500M — $158/月</b>\n　 適合 3-4 人家庭\n\n⚡ <b>極速版 1000M — $228/月</b>\n　 適合 5 人以上\n\n全部免安裝費 + 送 Wi-Fi Router！',
            options: [
                { label: '📋 幫我推薦', action: 'recommend' },
                { label: '✅ 我想申請', action: 'apply' },
                { label: '💼 商業寬頻？', action: 'business' },
                { label: '↩️ 返回主選單', action: 'main' }
            ]
        },
        moving: {
            text: '搬屋轉寬頻？我哋幫到你！🏠\n\n✅ 新居最快<b>翌日安裝</b>\n✅ 免安裝費\n✅ 送新 Wi-Fi Router\n✅ 月費低至 $98\n\n搬屋係轉寬頻嘅最佳時機，可能慳到每月過百蚊！\n\n📖 <a href="moving.html" style="color:#2563eb">搬屋入伙小幫手</a>',
            options: [
                { label: '✅ 查詢搬屋寬頻', action: 'apply_moving' },
                { label: '📋 幫我推薦計劃', action: 'recommend' },
                { label: '↩️ 返回主選單', action: 'main' }
            ]
        },
        install: {
            text: '安裝流程好簡單！⚡\n\n1️⃣ WhatsApp 查詢 + 確認地址\n2️⃣ 我哋安排師傅\n3️⃣ <b>最快翌日安裝</b>\n4️⃣ 即裝即用！\n\n⏰ 一般 1-3 個工作天完成\n💰 免安裝費\n📦 送 Wi-Fi Router',
            options: [
                { label: '✅ 我想申請', action: 'apply' },
                { label: '↩️ 返回主選單', action: 'main' }
            ]
        },
        business: {
            text: '我哋有商業寬頻計劃！💼\n\n適合辦公室、商鋪、中小企。\n\n✅ 專線光纖，穩定可靠\n✅ 覆蓋全港 1,648 個商業物業\n✅ 專人跟進售後\n\n📖 <a href="pages/business.html" style="color:#2563eb">睇商業寬頻詳情</a>',
            options: [
                { label: '✅ 查詢商業寬頻', action: 'apply_biz' },
                { label: '↩️ 返回主選單', action: 'main' }
            ]
        },
        other: {
            text: '你可以問我：\n\n📡 寬頻覆蓋範圍\n📄 合約期幾長\n🔧 售後服務\n💳 付款方式\n\n或者直接 WhatsApp 我哋，真人為你解答！',
            options: [
                { label: '📡 覆蓋範圍', action: 'coverage' },
                { label: '📄 合約問題', action: 'contract' },
                { label: '💬 WhatsApp 真人客服', action: 'whatsapp' },
                { label: '↩️ 返回主選單', action: 'main' }
            ]
        },
        coverage: {
            text: '我哋覆蓋<b>全港 18 區</b>！🇭🇰\n\n包括：觀塘、沙田、將軍澳、荃灣、屯門、元朗、大埔、深水埗、九龍城、油尖旺、灣仔、中西區、東區等。\n\n公屋、私樓、居屋、村屋都有覆蓋。\n\n唔確定你嘅地址有冇覆蓋？WhatsApp 我哋查詢！',
            options: [
                { label: '✅ 查詢我嘅地址', action: 'apply' },
                { label: '↩️ 返回主選單', action: 'main' }
            ]
        },
        contract: {
            text: '合約詳情 📄\n\n⏰ 合約期：<b>24 個月</b>\n💰 月費固定，唔會加價\n🚫 合約期內取消需付餘下月費\n✅ 到期後可續約或轉計劃\n\n💡 提示：合約到期前 1-2 個月記得比較市場價！\n\n📖 <a href="kb/contract-expiry.html" style="color:#2563eb">合約期滿攻略</a>',
            options: [
                { label: '✅ 我想申請', action: 'apply' },
                { label: '↩️ 返回主選單', action: 'main' }
            ]
        },
        apply: {
            text: '太好了！🎉 即刻 WhatsApp 我哋，專人幫你跟進：',
            wa: { text: '你好，我想申請寬頻服務', label: 'WhatsApp 即時申請' },
            options: [{ label: '↩️ 返回主選單', action: 'main' }]
        },
        apply_basic: {
            text: '好！即刻幫你安排 <b>基本版 100M ($98/月)</b> 🎉',
            wa: { text: '你好，我想申請基本版 100M 寬頻（$98/月）', label: 'WhatsApp 申請基本版' },
            options: [{ label: '↩️ 返回主選單', action: 'main' }]
        },
        apply_advanced: {
            text: '好！即刻幫你安排 <b>進階版 500M ($158/月)</b> 🎉',
            wa: { text: '你好，我想申請進階版 500M 寬頻（$158/月）', label: 'WhatsApp 申請進階版' },
            options: [{ label: '↩️ 返回主選單', action: 'main' }]
        },
        apply_premium: {
            text: '好！即刻幫你安排 <b>極速版 1000M ($228/月)</b> 🎉',
            wa: { text: '你好，我想申請極速版 1000M 寬頻（$228/月）', label: 'WhatsApp 申請極速版' },
            options: [{ label: '↩️ 返回主選單', action: 'main' }]
        },
        apply_moving: {
            text: '好！即刻幫你安排搬屋寬頻 🏠🎉',
            wa: { text: '你好，我準備搬屋，想查詢新居寬頻安裝', label: 'WhatsApp 查詢搬屋寬頻' },
            options: [{ label: '↩️ 返回主選單', action: 'main' }]
        },
        apply_biz: {
            text: '好！即刻幫你安排商業寬頻 💼🎉',
            wa: { text: '你好，我想查詢商業寬頻服務', label: 'WhatsApp 查詢商業寬頻' },
            options: [{ label: '↩️ 返回主選單', action: 'main' }]
        },
        whatsapp: {
            text: '即刻聯絡真人客服！😊',
            wa: { text: '你好，我想查詢寬頻服務', label: 'WhatsApp 聯絡客服' },
            options: [{ label: '↩️ 返回主選單', action: 'main' }]
        }
    };

    // Create chat button
    const btn = document.createElement('button');
    btn.className = 'chatbot-btn';
    btn.innerHTML = '💬<div class="badge">1</div>';
    btn.setAttribute('aria-label', 'AI 寬頻顧問');
    document.body.appendChild(btn);

    // Create chat window
    const win = document.createElement('div');
    win.className = 'chatbot-window';
    win.innerHTML = `
        <div class="chatbot-header">
            <div class="chatbot-avatar">👩</div>
            <div class="chatbot-header-text">
                <h4>寬頻顧問小幫手</h4>
                <span>24 小時在線 · 即時回覆</span>
            </div>
            <button class="chatbot-close">&times;</button>
        </div>
        <div class="chatbot-messages" id="chatMessages"></div>
    `;
    document.body.appendChild(win);

    const messagesEl = win.querySelector('#chatMessages');
    let isOpen = false;

    function toggleChat() {
        isOpen = !isOpen;
        win.classList.toggle('open', isOpen);
        if (isOpen) {
            btn.querySelector('.badge').style.display = 'none';
        }
    }

    btn.addEventListener('click', toggleChat);
    win.querySelector('.chatbot-close').addEventListener('click', toggleChat);

    function addBotMsg(html, options, wa) {
        const msg = document.createElement('div');
        msg.className = 'chat-msg chat-bot';
        let content = html.replace(/\n/g, '<br>');

        if (wa) {
            content += `<br><a href="https://api.whatsapp.com/send?phone=85252287541&text=${encodeURIComponent(wa.text)}" target="_blank" class="chat-wa-btn">📱 ${wa.label}</a>`;
        }

        if (options && options.length > 0) {
            content += '<div class="chat-options">';
            options.forEach(opt => {
                content += `<button class="chat-option-btn" data-action="${opt.action}">${opt.label}</button>`;
            });
            content += '</div>';
        }

        msg.innerHTML = content;
        messagesEl.appendChild(msg);
        messagesEl.scrollTop = messagesEl.scrollHeight;

        msg.querySelectorAll('.chat-option-btn').forEach(b => {
            b.addEventListener('click', function() {
                const action = this.getAttribute('data-action');
                addUserMsg(this.textContent);
                setTimeout(() => showMenu(action), 300);
            });
        });
    }

    function addUserMsg(text) {
        const msg = document.createElement('div');
        msg.className = 'chat-msg chat-user';
        msg.textContent = text;
        messagesEl.appendChild(msg);
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    function showMenu(key) {
        const menu = MENU[key];
        if (!menu) return;
        addBotMsg(menu.text, menu.options, menu.wa);
    }

    setTimeout(() => showMenu('main'), 500);
})();

// ===== Estate Search =====
function updateSearchLink() {
    var input = document.getElementById('estateInput');
    var btn = document.getElementById('estateSearchBtn');
    var estate = input ? input.value.trim() : '';
    if (btn) {
        btn.href = 'https://api.whatsapp.com/send?phone=85252287541&text=' + encodeURIComponent('你好，我想查詢「' + (estate || '我的屋苑') + '」嘅寬頻覆蓋同方案');
    }
}
(function() {
    var input = document.getElementById('estateInput');
    if (input) {
        input.addEventListener('input', updateSearchLink);
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('estateSearchBtn').click();
            }
        });
    }
})();

// ===== Service Worker =====
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js');
}
