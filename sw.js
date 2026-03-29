const CACHE_NAME = 'broadbandhk-v1';
const PRECACHE_URLS = [
  '/',
  '/style.css',
  '/calculator.html',
  '/speed-test.html',
  '/licenses.html',
  '/shops.html',
  '/blog.html',
  '/og-image.png'
];

// Install — 預載核心資源
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

// Activate — 清理舊 cache
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fetch — Network first, fallback to cache
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then(response => {
        // 成功取得網絡回應，更新 cache
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      })
      .catch(() => {
        // 離線時用 cache
        return caches.match(event.request);
      })
  );
});
