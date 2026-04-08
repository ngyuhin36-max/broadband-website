/**
 * Template Engine — 修正下載、尺寸選擇、手機縮放、iframe優化
 * 自動注入到所有模板，與 template-enhancer.js 兼容
 */
(function () {
    'use strict';

    // ── 尺寸預設 ──
    var SIZES = [
        { id: 'ig-post', w: 1080, h: 1080, label: 'IG 帖文 (1080×1080)' },
        { id: 'ig-story', w: 1080, h: 1920, label: 'IG Story (1080×1920)' },
        { id: 'fb-post', w: 1200, h: 630, label: 'FB 帖文 (1200×630)' },
        { id: 'fb-cover', w: 820, h: 312, label: 'FB 封面 (820×312)' },
        { id: 'linkedin', w: 1200, h: 627, label: 'LinkedIn (1200×627)' },
        { id: 'twitter', w: 1200, h: 675, label: 'Twitter/X (1200×675)' },
        { id: 'pinterest', w: 1000, h: 1500, label: 'Pinterest (1000×1500)' },
        { id: 'yt-thumb', w: 1280, h: 720, label: 'YT 縮圖 (1280×720)' }
    ];

    var currentSize = SIZES[0]; // default IG Post

    // ── 注入 CSS ──
    var style = document.createElement('style');
    style.textContent =
        /* 手機縮放容器 */
        '.te-scale-wrap{transform-origin:top center;margin:0 auto;}' +
        /* 尺寸選擇器 */
        '.te-size-select{padding:8px 12px;border:2px solid #e0e0e0;border-radius:8px;font-size:13px;' +
        'font-family:inherit;font-weight:600;cursor:pointer;background:#fff;color:#333;min-width:180px}' +
        '.te-size-select:focus{border-color:#6366f1;outline:none}' +
        /* 尺寸標籤 */
        '.te-size-label{font-size:12px;color:#94a3b8;font-weight:600;text-align:center;margin-top:8px}' +
        /* iframe 模式 */
        'body.te-iframe .instructions{display:none}' +
        'body.te-iframe{padding:15px !important}' +
        /* 手機優化 */
        '@media(max-width:768px){' +
        '  body{padding:10px !important}' +
        '  .toolbar{padding:12px 15px !important;gap:10px !important;justify-content:center}' +
        '  .toolbar label{font-size:12px}' +
        '  .toolbar input[type="color"]{width:40px;height:32px}' +
        '  .btn-download{padding:10px 18px !important;font-size:14px !important}' +
        '  .instructions{font-size:13px;padding:10px 15px;margin-bottom:12px}' +
        '  .te-size-select{min-width:140px;font-size:12px;padding:6px 8px}' +
        '}' +
        /* 下載中提示 */
        '.te-downloading{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);' +
        'display:flex;align-items:center;justify-content:center;z-index:9999}' +
        '.te-downloading-box{background:#fff;padding:30px 50px;border-radius:16px;text-align:center;' +
        'box-shadow:0 10px 40px rgba(0,0,0,0.2)}' +
        '.te-downloading-box h3{margin:0 0 8px;font-size:18px;color:#1e293b}' +
        '.te-downloading-box p{margin:0;font-size:14px;color:#64748b}';
    document.head.appendChild(style);

    // ── iframe 偵測 ──
    try {
        if (window.self !== window.top) {
            document.body.classList.add('te-iframe');
        }
    } catch (e) {
        document.body.classList.add('te-iframe');
    }

    // ── 初始化 ──
    function init() {
        var toolbar = document.querySelector('.toolbar');
        var card = document.getElementById('card');
        var templateWrap = document.getElementById('template');
        if (!toolbar || !card) return;

        // 加入尺寸選擇器
        addSizeSelector(toolbar);

        // 手機自動縮放
        setupResponsiveScale(card, templateWrap);

        // 覆寫下載函數
        overrideDownload(card);
    }

    // ── 尺寸選擇器 ──
    function addSizeSelector(toolbar) {
        var container = document.createElement('div');
        container.style.cssText = 'display:flex;flex-direction:column;align-items:flex-start';

        var label = document.createElement('label');
        label.textContent = '下載尺寸';
        label.style.cssText = 'font-size:14px;color:#666;font-weight:600;margin-bottom:4px';

        var select = document.createElement('select');
        select.className = 'te-size-select';
        select.id = 'teSizeSelect';

        for (var i = 0; i < SIZES.length; i++) {
            var opt = document.createElement('option');
            opt.value = i;
            opt.textContent = SIZES[i].label;
            select.appendChild(opt);
        }

        select.onchange = function () {
            currentSize = SIZES[parseInt(this.value)];
        };

        container.appendChild(label);
        container.appendChild(select);

        // 插入到 download 按鈕之前
        var dlBtn = toolbar.querySelector('.btn-download');
        if (dlBtn) toolbar.insertBefore(container, dlBtn);
        else toolbar.appendChild(container);
    }

    // ── 手機縮放 ──
    function setupResponsiveScale(card, templateWrap) {
        var target = templateWrap || card;

        function applyScale() {
            var cardW = card.offsetWidth;
            var viewW = window.innerWidth - 20; // 留 padding
            if (viewW < cardW) {
                var scale = viewW / cardW;
                target.style.transform = 'scale(' + scale + ')';
                target.style.transformOrigin = 'top center';
                // 修正高度，避免留白
                target.style.marginBottom = -(card.offsetHeight * (1 - scale)) + 'px';
            } else {
                target.style.transform = '';
                target.style.marginBottom = '';
            }
        }

        applyScale();
        window.addEventListener('resize', applyScale);
    }

    // ── 覆寫下載函數 ──
    function overrideDownload(card) {
        // 統一下載函數 — 截取 #card，輸出所選尺寸
        function enhancedDownload() {
            // 清除文字選取和 focus
            if (document.activeElement) document.activeElement.blur();
            window.getSelection && window.getSelection().removeAllRanges && window.getSelection().removeAllRanges();

            // 取消所有圖片選取框（enhancer 的）
            var selected = document.querySelectorAll('.te-img-wrapper.selected');
            selected.forEach(function (w) { w.classList.remove('selected'); });

            // 顯示下載中提示
            var overlay = document.createElement('div');
            overlay.className = 'te-downloading';
            overlay.innerHTML = '<div class="te-downloading-box"><h3>正在生成圖片...</h3><p>' +
                currentSize.w + ' x ' + currentSize.h + ' px</p></div>';
            document.body.appendChild(overlay);

            // 暫時移除縮放（確保截圖準確）
            var templateWrap = document.getElementById('template');
            var origTransform = templateWrap ? templateWrap.style.transform : '';
            var origMargin = templateWrap ? templateWrap.style.marginBottom : '';
            if (templateWrap) {
                templateWrap.style.transform = '';
                templateWrap.style.marginBottom = '';
            }

            // 用 html2canvas 截取 #card
            html2canvas(card, {
                scale: 2,
                useCORS: true,
                backgroundColor: null,
                width: card.offsetWidth,
                height: card.offsetHeight
            }).then(function (capturedCanvas) {
                var targetW = currentSize.w;
                var targetH = currentSize.h;
                var cardW = card.offsetWidth;
                var cardH = card.offsetHeight;

                var finalCanvas;

                // 如果尺寸同 card 一樣，直接用
                if (targetW === cardW && targetH === cardH) {
                    finalCanvas = capturedCanvas;
                } else {
                    // 建立目標尺寸 canvas
                    finalCanvas = document.createElement('canvas');
                    finalCanvas.width = targetW * 2;  // scale:2
                    finalCanvas.height = targetH * 2;
                    var ctx = finalCanvas.getContext('2d');

                    // 取 card 背景色填充
                    var bgColor = getCardBackgroundColor(card);
                    ctx.fillStyle = bgColor;
                    ctx.fillRect(0, 0, finalCanvas.width, finalCanvas.height);

                    // 計算縮放比例（fit inside）
                    var scaleX = (targetW * 2) / capturedCanvas.width;
                    var scaleY = (targetH * 2) / capturedCanvas.height;
                    var fitScale = Math.min(scaleX, scaleY, 1); // 唔放大，只縮小或原尺寸

                    var drawW = capturedCanvas.width * fitScale;
                    var drawH = capturedCanvas.height * fitScale;
                    var offsetX = (finalCanvas.width - drawW) / 2;
                    var offsetY = (finalCanvas.height - drawH) / 2;

                    ctx.drawImage(capturedCanvas, offsetX, offsetY, drawW, drawH);
                }

                // 下載
                var a = document.createElement('a');
                var title = document.title.replace(/Template \d+ - /, '').replace(/\s+/g, '-').toLowerCase();
                a.download = title + '-' + currentSize.id + '.png';
                a.href = finalCanvas.toDataURL('image/png');
                a.click();

                // 移除提示
                overlay.remove();

                // 恢復縮放
                if (templateWrap) {
                    templateWrap.style.transform = origTransform;
                    templateWrap.style.marginBottom = origMargin;
                }
            }).catch(function (err) {
                overlay.remove();
                if (templateWrap) {
                    templateWrap.style.transform = origTransform;
                    templateWrap.style.marginBottom = origMargin;
                }
                alert('下載失敗，請重試。');
                console.error(err);
            });
        }

        // 覆寫全局下載函數
        window.downloadPNG = enhancedDownload;
        window.dl = enhancedDownload;

        // 替換 download 按鈕的 onclick
        var dlBtns = document.querySelectorAll('.btn-download');
        dlBtns.forEach(function (btn) {
            btn.onclick = function (e) {
                e.preventDefault();
                enhancedDownload();
            };
        });
    }

    // ── 提取 card 背景色 ──
    function getCardBackgroundColor(card) {
        var bg = card.style.background || card.style.backgroundColor || '';
        // 如果係漸變，提取第一個顏色
        var gradMatch = bg.match(/#[0-9a-fA-F]{3,8}/);
        if (gradMatch) return gradMatch[0];
        // 如果係 rgb
        var rgbMatch = bg.match(/rgb\([^)]+\)/);
        if (rgbMatch) return rgbMatch[0];
        // 用 computed style
        var computed = window.getComputedStyle(card).backgroundColor;
        if (computed && computed !== 'rgba(0, 0, 0, 0)') return computed;
        return '#ffffff';
    }

    // ── 啟動 ──
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
