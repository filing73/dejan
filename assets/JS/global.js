// ===== SCROLL PROGRESS =====
const progressBar = document.querySelector('.progress-bar');

window.addEventListener('scroll', () => {
  if (!progressBar) return;

  const scrollTop = window.scrollY;
  const docHeight = document.body.scrollHeight - window.innerHeight;
  const progress = (scrollTop / docHeight) * 100;

  progressBar.style.width = progress + "%";
});

// ===== COLOR SWITCH =====
const sections = document.querySelectorAll('section');

window.addEventListener('scroll', () => {
  if (!progressBar) return;

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

  if (currentTheme === "dark") {
    progressBar.classList.add('progress-dark');
    progressBar.classList.remove('progress-light');
  } else {
    progressBar.classList.add('progress-light');
    progressBar.classList.remove('progress-dark');
  }
});

// ===== COOKIE CONSENT & TRACKING =====

// Check if user has already accepted cookies
function getCookieConsent() {
  const consent = localStorage.getItem('dlproject56_cookie_consent');
  return consent === 'accepted';
}

// Load GA4
function loadGA4() {
  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://www.googletagmanager.com/gtag/js?id=G-YFBTB98CGR';
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', 'G-YFBTB98CGR');
}

// Load Meta Pixel
function loadMetaPixel() {
  !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
  n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '953567734278264');
  fbq('track', 'PageView');
}

// Show cookie consent banner
function showCookieBanner() {
  const banner = document.createElement('div');
  banner.id = 'cookie-consent-banner';
  banner.innerHTML = `
    <div style="
      position: fixed;
      bottom: 20px;
      left: 20px;
      background: rgba(30, 30, 30, 0.95);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 20px;
      z-index: 9999;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: #fff;
      max-width: 380px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    ">
      <p style="margin: 0 0 16px 0; font-size: 14px; line-height: 1.6;">
        We use cookies and analytics to enhance your experience. Read our <a href="/privacy/" style="color: #667eea; text-decoration: none; font-weight: 500;">Privacy Policy</a>.
      </p>
      <div style="display: flex; gap: 12px;">
        <button id="cookie-reject" style="
          flex: 1;
          padding: 10px 16px;
          background: transparent;
          color: #fff;
          border: 1px solid rgba(255, 255, 255, 0.3);
          border-radius: 6px;
          cursor: pointer;
          font-size: 13px;
          font-weight: 500;
          transition: all 0.3s ease;
        " onmouseover="this.style.borderColor='rgba(255, 255, 255, 0.5)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.3)'">
          Reject
        </button>
        <button id="cookie-accept" style="
          flex: 1;
          padding: 10px 16px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: #fff;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          font-size: 13px;
          font-weight: 500;
          transition: all 0.3s ease;
        " onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">
          Accept
        </button>
      </div>
    </div>
  `;
  
  document.body.appendChild(banner);

  // Accept button
  document.getElementById('cookie-accept').addEventListener('click', () => {
    localStorage.setItem('dlproject56_cookie_consent', 'accepted');
    banner.remove();
    loadGA4();
    loadMetaPixel();
  });

  // Reject button
  document.getElementById('cookie-reject').addEventListener('click', () => {
    localStorage.setItem('dlproject56_cookie_consent', 'rejected');
    banner.remove();
  });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  const hasConsent = getCookieConsent();
  
  if (hasConsent) {
    // User already accepted - load tracking immediately
    loadGA4();
    loadMetaPixel();
  } else if (!localStorage.getItem('dlproject56_cookie_consent')) {
    // No decision made yet - show banner
    showCookieBanner();
  }
  // If rejected, do nothing
});

