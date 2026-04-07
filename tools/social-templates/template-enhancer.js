/**
 * Template Enhancer — 為所有模板加入圖片上傳、拖動、縮放功能
 * 自動注入到 toolbar，與 html2canvas 下載兼容
 */
(function() {
    'use strict';

    const STYLE = document.createElement('style');
    STYLE.textContent = `
        .img-upload-btn{padding:12px 20px;border:2px dashed #c084fc;border-radius:10px;background:rgba(192,132,252,0.08);
            color:#7c3aed;font-size:14px;font-weight:700;cursor:pointer;font-family:inherit;transition:all 0.2s;display:flex;align-items:center;gap:6px}
        .img-upload-btn:hover{background:rgba(192,132,252,0.15);border-color:#7c3aed}
        .te-img-wrapper{position:absolute;cursor:move;z-index:50;user-select:none;touch-action:none}
        .te-img-wrapper img{display:block;width:100%;height:100%;object-fit:contain;pointer-events:none}
        .te-img-wrapper.selected{outline:2px dashed #7c3aed;outline-offset:2px}
        .te-img-controls{position:absolute;top:-40px;left:50%;transform:translateX(-50%);display:none;gap:6px;
            background:#fff;padding:6px 10px;border-radius:10px;box-shadow:0 2px 12px rgba(0,0,0,0.15);white-space:nowrap}
        .te-img-wrapper.selected .te-img-controls{display:flex}
        .te-ctrl-btn{width:30px;height:30px;border:1px solid #e2e8f0;border-radius:8px;background:#fff;
            font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.15s}
        .te-ctrl-btn:hover{background:#f1f5f9}
        .te-ctrl-btn.danger:hover{background:#fee2e2;color:#ef4444}
        .te-resize-handle{position:absolute;bottom:-6px;right:-6px;width:16px;height:16px;background:#7c3aed;
            border-radius:4px;cursor:nwse-resize;z-index:51;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,0.2)}
        .te-img-wrapper:not(.selected) .te-resize-handle{display:none}
        .te-img-count{font-size:12px;color:#94a3b8;margin-left:4px}
    `;
    document.head.appendChild(STYLE);

    let imgCount = 0;

    function init() {
        const toolbar = document.querySelector('.toolbar');
        if (!toolbar) return;

        // Add upload button
        const uploadBtn = document.createElement('button');
        uploadBtn.className = 'img-upload-btn';
        uploadBtn.innerHTML = '📷 加入圖片 <span class="te-img-count" id="teImgCount"></span>';
        uploadBtn.type = 'button';
        uploadBtn.onclick = () => fileInput.click();

        // Insert before download button
        const dlBtn = toolbar.querySelector('.btn-download');
        if (dlBtn) toolbar.insertBefore(uploadBtn, dlBtn);
        else toolbar.appendChild(uploadBtn);

        // Hidden file input
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.multiple = true;
        fileInput.style.display = 'none';
        fileInput.onchange = (e) => handleFiles(e.target.files);
        document.body.appendChild(fileInput);

        // Click card to deselect all images
        const card = document.getElementById('card');
        if (card) {
            card.addEventListener('click', (e) => {
                if (!e.target.closest('.te-img-wrapper')) {
                    document.querySelectorAll('.te-img-wrapper.selected').forEach(w => w.classList.remove('selected'));
                }
            });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            const selected = document.querySelector('.te-img-wrapper.selected');
            if (!selected) return;
            const step = e.shiftKey ? 10 : 1;
            switch(e.key) {
                case 'Delete':
                case 'Backspace':
                    if (document.activeElement.isContentEditable) return;
                    e.preventDefault();
                    removeImage(selected);
                    break;
                case 'ArrowUp': e.preventDefault(); selected.style.top = (parseInt(selected.style.top) - step) + 'px'; break;
                case 'ArrowDown': e.preventDefault(); selected.style.top = (parseInt(selected.style.top) + step) + 'px'; break;
                case 'ArrowLeft': e.preventDefault(); selected.style.left = (parseInt(selected.style.left) - step) + 'px'; break;
                case 'ArrowRight': e.preventDefault(); selected.style.left = (parseInt(selected.style.left) + step) + 'px'; break;
                case '[': // Make smaller
                    e.preventDefault();
                    resizeBy(selected, -20);
                    break;
                case ']': // Make bigger
                    e.preventDefault();
                    resizeBy(selected, 20);
                    break;
            }
        });
    }

    function handleFiles(files) {
        Array.from(files).forEach(file => {
            if (!file.type.startsWith('image/')) return;
            const reader = new FileReader();
            reader.onload = (e) => addImageToCanvas(e.target.result);
            reader.readAsDataURL(file);
        });
    }

    function addImageToCanvas(dataUrl) {
        const card = document.getElementById('card');
        if (!card) return;

        // Make card position relative if not already
        const cardStyle = getComputedStyle(card);
        if (cardStyle.position === 'static') card.style.position = 'relative';

        imgCount++;
        updateCount();

        const wrapper = document.createElement('div');
        wrapper.className = 'te-img-wrapper';
        wrapper.style.cssText = 'left:100px;top:100px;width:300px;height:300px;';

        const img = document.createElement('img');
        img.src = dataUrl;

        // Controls bar
        const controls = document.createElement('div');
        controls.className = 'te-img-controls';
        controls.innerHTML = `
            <button class="te-ctrl-btn" title="縮小 [" data-action="smaller">−</button>
            <button class="te-ctrl-btn" title="放大 ]" data-action="bigger">+</button>
            <button class="te-ctrl-btn" title="上移一層" data-action="forward">↑</button>
            <button class="te-ctrl-btn" title="下移一層" data-action="backward">↓</button>
            <button class="te-ctrl-btn" title="圓形切換" data-action="circle">○</button>
            <button class="te-ctrl-btn" title="透明度" data-action="opacity">◐</button>
            <button class="te-ctrl-btn danger" title="刪除 Delete" data-action="delete">✕</button>
        `;

        // Resize handle
        const resizeHandle = document.createElement('div');
        resizeHandle.className = 'te-resize-handle';

        wrapper.appendChild(img);
        wrapper.appendChild(controls);
        wrapper.appendChild(resizeHandle);
        card.appendChild(wrapper);

        // Select on click
        wrapper.addEventListener('mousedown', (e) => {
            if (e.target.closest('.te-img-controls') || e.target.closest('.te-resize-handle')) return;
            e.stopPropagation();
            document.querySelectorAll('.te-img-wrapper.selected').forEach(w => w.classList.remove('selected'));
            wrapper.classList.add('selected');
        });

        // Drag
        setupDrag(wrapper, card);

        // Resize handle
        setupResize(resizeHandle, wrapper);

        // Control buttons
        controls.addEventListener('click', (e) => {
            const btn = e.target.closest('[data-action]');
            if (!btn) return;
            e.stopPropagation();
            const action = btn.dataset.action;
            switch(action) {
                case 'smaller': resizeBy(wrapper, -30); break;
                case 'bigger': resizeBy(wrapper, 30); break;
                case 'forward':
                    const nextZ = parseInt(wrapper.style.zIndex || 50) + 1;
                    wrapper.style.zIndex = nextZ;
                    break;
                case 'backward':
                    const prevZ = Math.max(1, parseInt(wrapper.style.zIndex || 50) - 1);
                    wrapper.style.zIndex = prevZ;
                    break;
                case 'circle':
                    const isCircle = img.style.borderRadius === '50%';
                    img.style.borderRadius = isCircle ? '0' : '50%';
                    btn.textContent = isCircle ? '○' : '□';
                    break;
                case 'opacity':
                    const cur = parseFloat(wrapper.style.opacity || 1);
                    wrapper.style.opacity = cur <= 0.3 ? 1 : (cur - 0.2).toFixed(1);
                    break;
                case 'delete':
                    removeImage(wrapper);
                    break;
            }
        });

        // Auto select
        document.querySelectorAll('.te-img-wrapper.selected').forEach(w => w.classList.remove('selected'));
        wrapper.classList.add('selected');
    }

    function setupDrag(wrapper, card) {
        let startX, startY, startLeft, startTop, dragging = false;

        wrapper.addEventListener('mousedown', (e) => {
            if (e.target.closest('.te-img-controls') || e.target.closest('.te-resize-handle')) return;
            e.preventDefault();
            dragging = true;
            startX = e.clientX;
            startY = e.clientY;
            startLeft = parseInt(wrapper.style.left) || 0;
            startTop = parseInt(wrapper.style.top) || 0;
        });

        document.addEventListener('mousemove', (e) => {
            if (!dragging) return;
            wrapper.style.left = (startLeft + e.clientX - startX) + 'px';
            wrapper.style.top = (startTop + e.clientY - startY) + 'px';
        });

        document.addEventListener('mouseup', () => { dragging = false; });

        // Touch support
        wrapper.addEventListener('touchstart', (e) => {
            if (e.target.closest('.te-img-controls') || e.target.closest('.te-resize-handle')) return;
            const t = e.touches[0];
            dragging = true;
            startX = t.clientX;
            startY = t.clientY;
            startLeft = parseInt(wrapper.style.left) || 0;
            startTop = parseInt(wrapper.style.top) || 0;
        }, { passive: true });

        document.addEventListener('touchmove', (e) => {
            if (!dragging) return;
            const t = e.touches[0];
            wrapper.style.left = (startLeft + t.clientX - startX) + 'px';
            wrapper.style.top = (startTop + t.clientY - startY) + 'px';
        }, { passive: true });

        document.addEventListener('touchend', () => { dragging = false; });
    }

    function setupResize(handle, wrapper) {
        let startX, startY, startW, startH, resizing = false;

        handle.addEventListener('mousedown', (e) => {
            e.preventDefault();
            e.stopPropagation();
            resizing = true;
            startX = e.clientX;
            startY = e.clientY;
            startW = parseInt(wrapper.style.width) || wrapper.offsetWidth;
            startH = parseInt(wrapper.style.height) || wrapper.offsetHeight;
        });

        document.addEventListener('mousemove', (e) => {
            if (!resizing) return;
            const dx = e.clientX - startX;
            const newW = Math.max(50, startW + dx);
            const newH = Math.max(50, startH + dx); // keep aspect ratio
            wrapper.style.width = newW + 'px';
            wrapper.style.height = newH + 'px';
        });

        document.addEventListener('mouseup', () => { resizing = false; });
    }

    function resizeBy(wrapper, delta) {
        const w = parseInt(wrapper.style.width) || wrapper.offsetWidth;
        const h = parseInt(wrapper.style.height) || wrapper.offsetHeight;
        const nw = Math.max(50, w + delta);
        const nh = Math.max(50, h + delta);
        wrapper.style.width = nw + 'px';
        wrapper.style.height = nh + 'px';
    }

    function removeImage(wrapper) {
        wrapper.remove();
        imgCount--;
        updateCount();
    }

    function updateCount() {
        const el = document.getElementById('teImgCount');
        if (el) el.textContent = imgCount > 0 ? `(${imgCount})` : '';
    }

    // Auto-init when DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
