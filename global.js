// ===== SCROLL PROGRESS =====
const progressBar = document.querySelector('.progress-bar');

window.addEventListener('scroll', () => {
  const scrollTop = window.scrollY;
  const docHeight = document.body.scrollHeight - window.innerHeight;
  const progress = (scrollTop / docHeight) * 100;

  if (progressBar) progressBar.style.width = progress + "%";
});

// ===== COLOR SWITCH =====
const sections = document.querySelectorAll('section');

window.addEventListener('scroll', () => {
  let currentTheme = "light";

  sections.forEach(section => {
    const rect = section.getBoundingClientRect();

    if (rect.top <= window.innerHeight * 0.3 && rect.bottom >= 0) {
      if (section.classList.contains('dark-section') || section.classList.contains('hero')) {
        currentTheme = "dark";
      } else {
        currentTheme = "light";
      }
    }
  });

  if (progressBar) {
    if (currentTheme === "dark") {
      progressBar.classList.add('progress-dark');
      progressBar.classList.remove('progress-light');
    } else {
      progressBar.classList.add('progress-light');
      progressBar.classList.remove('progress-dark');
    }
  }
});

// ===== COOKIE CONSENT + TRACKING =====
(function () {
  var GA4_ID = 'G-E2MRR0GV9Q';
  var META_PIXEL_ID = '1639537617062408';
  var COOKIE_KEY = 'dlp56_cookie_consent';
  var trackingLoaded = false;

  // --- Cookie helpers ---
  function getConsent() {
    var match = document.cookie.match(new RegExp('(?:^|; )' + COOKIE_KEY + '=([^;]*)'));
    return match ? match[1] : null;
  }

  function setConsent(value) {
    var d = new Date();
    d.setTime(d.getTime() + 365 * 24 * 60 * 60 * 1000);
    document.cookie = COOKIE_KEY + '=' + value + ';expires=' + d.toUTCString() + ';path=/;SameSite=Lax';
  }

  // --- Load GA4 ---
  function loadGA4() {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
    document.head.appendChild(s);

    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA4_ID, { anonymize_ip: true });
  }

  // --- Load Meta Pixel ---
  function loadMetaPixel() {
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return;
      n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n;
      n.push = n; n.loaded = !0; n.version = '2.0';
      n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v;
      s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');

    window.fbq('init', META_PIXEL_ID);
    window.fbq('track', 'PageView');
  }

  // --- Load all tracking ---
  function loadTracking() {
    if (trackingLoaded) return;
    trackingLoaded = true;
    loadGA4();
    loadMetaPixel();
  }

  // --- Banner UI ---
  function showBanner() {
    var banner = document.createElement('div');
    banner.id = 'cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie consent');
    banner.innerHTML =
      '<div id="cookie-banner-inner">' +
        '<p>We use cookies to analyze site traffic and improve your experience. ' +
        '<a href="/privacy" style="color:#7ec8e3;text-decoration:underline;">Privacy Policy</a></p>' +
        '<div id="cookie-banner-btns">' +
          '<button id="cookie-accept" type="button">Accept</button>' +
          '<button id="cookie-reject" type="button">Reject</button>' +
        '</div>' +
      '</div>';

    // Styles
    var style = document.createElement('style');
    style.textContent =
      '#cookie-banner{position:fixed;bottom:0;left:0;right:0;z-index:9999;' +
        'background:rgba(15,38,51,0.97);color:rgba(255,255,255,0.92);' +
        'font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif;font-size:0.9rem;' +
        'padding:16px 20px;box-shadow:0 -4px 20px rgba(0,0,0,0.18);' +
        'animation:cbSlide .35s ease-out}' +
      '#cookie-banner-inner{max-width:1140px;margin:0 auto;display:flex;' +
        'align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap}' +
      '#cookie-banner p{margin:0;line-height:1.5;flex:1;min-width:200px}' +
      '#cookie-banner-btns{display:flex;gap:10px;flex-shrink:0}' +
      '#cookie-accept,#cookie-reject{border:none;border-radius:8px;padding:10px 22px;' +
        'font-weight:700;font-size:0.88rem;cursor:pointer;transition:opacity .2s}' +
      '#cookie-accept{background:#20a965;color:#fff}' +
      '#cookie-accept:hover{opacity:0.88}' +
      '#cookie-reject{background:rgba(255,255,255,0.14);color:rgba(255,255,255,0.88);' +
        'border:1px solid rgba(255,255,255,0.22)}' +
      '#cookie-reject:hover{opacity:0.78}' +
      '@keyframes cbSlide{from{transform:translateY(100%)}to{transform:translateY(0)}}' +
      '@media(max-width:600px){#cookie-banner-inner{flex-direction:column;text-align:center}' +
        '#cookie-banner-btns{width:100%;justify-content:center}}';
    document.head.appendChild(style);
    document.body.appendChild(banner);

    document.getElementById('cookie-accept').addEventListener('click', function () {
      setConsent('accepted');
      banner.remove();
      loadTracking();
    });

    document.getElementById('cookie-reject').addEventListener('click', function () {
      setConsent('rejected');
      banner.remove();
    });
  }

  // --- Init ---
  var consent = getConsent();
  if (consent === 'accepted') {
    loadTracking();
  } else if (consent !== 'rejected') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', showBanner);
    } else {
      showBanner();
    }
  }
})();

