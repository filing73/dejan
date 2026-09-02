/* Адвокат Бојана Ђаковић — site.js */
var LINA = { mode: 'demo', endpoint: '/ai-proxy.php' };

(function () {
  'use strict';
  var d = document, root = d.documentElement;
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ============ 1. ЋИРИЛИЦА ⇄ LATINICA ============ */
  var MAP = {
    'а':'a','б':'b','в':'v','г':'g','д':'d','ђ':'đ','е':'e','ж':'ž','з':'z','и':'i',
    'ј':'j','к':'k','л':'l','љ':'lj','м':'m','н':'n','њ':'nj','о':'o','п':'p','р':'r',
    'с':'s','т':'t','ћ':'ć','у':'u','ф':'f','х':'h','ц':'c','ч':'č','џ':'dž','ш':'š',
    'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Ђ':'Đ','Е':'E','Ж':'Ž','З':'Z','И':'I',
    'Ј':'J','К':'K','Л':'L','Љ':'Lj','М':'M','Н':'N','Њ':'Nj','О':'O','П':'P','Р':'R',
    'С':'S','Т':'T','Ћ':'Ć','У':'U','Ф':'F','Х':'H','Ц':'C','Ч':'Č','Џ':'Dž','Ш':'Š'
  };
  var DIG = { 'Љ': ['Lj', 'LJ'], 'Њ': ['Nj', 'NJ'], 'Џ': ['Dž', 'DŽ'] };
  var LOW = /[а-шђјљњћџ]/;

  function toLat(s) {
    var out = '', i, ch, m;
    for (i = 0; i < s.length; i++) {
      ch = s.charAt(i); m = MAP[ch];
      if (m === undefined) { out += ch; continue; }
      if (DIG[ch]) {
        var nx = s.charAt(i + 1);
        out += (nx && LOW.test(nx)) ? DIG[ch][0] : DIG[ch][1];
      } else out += m;
    }
    return out;
  }

  var ROOTS = ['.topbar', '#rail', '#ovl', '#glavni', '.foot', '.vz-foot', '#priv', '.sticky', '.lina-fab', '#lina'];
  var ATTRS = ['aria-label', 'placeholder', 'alt', 'title'];
  var CYR = /[Ѐ-џ]/;
  var texts = [], attrs = [], titleCyr = d.title, isLat = root.classList.contains('lat');

  function skip(el) { return !el || el.hasAttribute('data-lang-toggle') || el.closest('[data-lang-toggle]'); }

  function collect() {
    for (var r = 0; r < ROOTS.length; r++) {
      var root_ = d.querySelector(ROOTS[r]); if (!root_) continue;
      var w = d.createTreeWalker(root_, NodeFilter.SHOW_TEXT, null, false), n;
      while ((n = w.nextNode())) {
        var p = n.parentNode;
        if (!n.nodeValue || !CYR.test(n.nodeValue)) continue;
        if (!p || p.nodeName === 'SCRIPT' || p.nodeName === 'STYLE' || skip(p)) continue;
        texts.push([n, n.nodeValue]);
      }
      var els = root_.querySelectorAll('[aria-label],[placeholder],[alt],[title]');
      for (var i = 0; i < els.length; i++) {
        if (skip(els[i])) continue;
        for (var a = 0; a < ATTRS.length; a++) {
          var v = els[i].getAttribute(ATTRS[a]);
          if (v && CYR.test(v)) attrs.push([els[i], ATTRS[a], v]);
        }
      }
    }
  }

  function T(s) { return isLat ? toLat(s) : s; }

  function render() {
    var i;
    for (i = 0; i < texts.length; i++) texts[i][0].nodeValue = T(texts[i][1]);
    for (i = 0; i < attrs.length; i++) attrs[i][0].setAttribute(attrs[i][1], T(attrs[i][2]));
    d.title = T(titleCyr);
    root.lang = isLat ? 'sr-Latn' : 'sr-Cyrl';
    root.classList.toggle('lat', isLat);
    var b = d.querySelectorAll('[data-lang-toggle]');
    for (i = 0; i < b.length; i++) {
      b[i].textContent = isLat ? 'Ћир' : 'Lat';
      b[i].setAttribute('aria-label', isLat ? 'Пребаци на ћирилицу' : 'Пребаци на латиницу');
    }
    root.classList.add('ready');
  }

  collect();
  render();

  var toggles = d.querySelectorAll('[data-lang-toggle]');
  for (var t = 0; t < toggles.length; t++) {
    toggles[t].addEventListener('click', function () {
      isLat = !isLat;
      try { localStorage.setItem('pismo', isLat ? 'lat' : 'cir'); } catch (e) {}
      render();
    });
  }

  /* ============ 2. Година у футеру ============ */
  var god = d.getElementById('god');
  if (god) god.textContent = String(new Date().getFullYear());

  /* ============ 3. Reveal ============ */
  var rv = d.querySelectorAll('.rv');
  if (RM || !('IntersectionObserver' in window)) {
    for (var k = 0; k < rv.length; k++) rv[k].classList.add('in');
  } else {
    var ro = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); ro.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    for (var k2 = 0; k2 < rv.length; k2++) ro.observe(rv[k2]);
  }

  /* ============ 4. Rail: активна ставка + мека мембрана ============ */
  var rail = d.getElementById('rail');
  var links = rail ? rail.querySelectorAll('.rail-list a[data-sec]') : [];
  if (links.length && 'IntersectionObserver' in window) {
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        for (var i = 0; i < links.length; i++)
          links[i].classList.toggle('on', links[i].getAttribute('data-sec') === e.target.id);
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
    var secs = d.querySelectorAll('main section[id]');
    for (var s = 0; s < secs.length; s++) so.observe(secs[s]);
  }

  if (rail && !RM && matchMedia('(pointer:fine)').matches) {
    var items = rail.querySelectorAll('.rail-list a, .rail-list button'), raf = 0, my = 0;
    rail.addEventListener('mousemove', function (ev) {
      my = ev.clientY;
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        var rct = rail.getBoundingClientRect();
        rail.style.setProperty('--my', ((my - rct.top) / rct.height * 100).toFixed(2) + '%');
        for (var i = 0; i < items.length; i++) {
          var r = items[i].getBoundingClientRect(), dy = my - (r.top + r.height / 2);
          var f = Math.max(-1, Math.min(1, dy / 80));
          items[i].style.transform = 'translateY(' + (f * 2).toFixed(2) + 'px)';
        }
      });
    });
    rail.addEventListener('mouseenter', function () { rail.classList.add('hot'); });
    rail.addEventListener('mouseleave', function () {
      rail.classList.remove('hot');
      for (var i = 0; i < items.length; i++) items[i].style.transform = '';
    });
  }

  /* ============ 5. Full-screen мени ============ */
  var ovl = d.getElementById('ovl'), burger = d.getElementById('burger'),
      ovlClose = d.getElementById('ovlClose'), lastFocus = null;

  function trap(box) {
    return function (e) {
      if (e.key !== 'Tab') return;
      var f = box.querySelectorAll('a[href],button:not([disabled]),input,textarea,select,[tabindex]:not([tabindex="-1"])');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && d.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); }
    };
  }
  var ovlTrap = ovl ? trap(ovl) : null;

  function openOvl() {
    if (!ovl) return;
    lastFocus = d.activeElement;
    ovl.setAttribute('data-open', '1');
    burger.setAttribute('aria-expanded', 'true');
    d.body.style.overflow = 'hidden';
    d.addEventListener('keydown', ovlTrap);
    var a = ovl.querySelector('a[href]'); if (a) a.focus();
  }
  function closeOvl() {
    if (!ovl) return;
    ovl.setAttribute('data-open', '0');
    burger.setAttribute('aria-expanded', 'false');
    d.body.style.overflow = '';
    d.removeEventListener('keydown', ovlTrap);
    if (lastFocus) lastFocus.focus();
  }
  if (burger) burger.addEventListener('click', openOvl);
  if (ovlClose) ovlClose.addEventListener('click', closeOvl);
  if (ovl) {
    var oa = ovl.querySelectorAll('a[href^="#"]');
    for (var o = 0; o < oa.length; o++) oa[o].addEventListener('click', closeOvl);
  }

  /* ============ 6. Политика приватности ============ */
  var priv = d.getElementById('priv'), privBtn = d.getElementById('privBtn'), privClose = d.getElementById('privClose');
  if (priv && privBtn) {
    privBtn.addEventListener('click', function () { if (priv.showModal) priv.showModal(); else priv.setAttribute('open', ''); });
    privClose.addEventListener('click', function () { if (priv.close) priv.close(); else priv.removeAttribute('open'); });
  }

  /* ============ 7. Порука форме ============ */
  var fm = d.getElementById('formmsg');
  if (fm && (/[?&]sent=1/.test(location.search) || /sent=1/.test(location.hash))) {
    fm.setAttribute('data-on', '1');
  }

  /* ============ 8. Лина ============ */
  var lina = d.getElementById('lina'), log = d.getElementById('linaLog'),
      linaForm = d.getElementById('linaForm'), linaIn = d.getElementById('linaIn'),
      linaClose = d.getElementById('linaClose'), linaTrap = lina ? trap(lina) : null,
      linaLast = null, greeted = false;

  var HELLO = 'Ја сам Лина, асистент канцеларије. Могу да вам кажем радно време, адресу, области рада и како да закажете разговор. Не дајем правне савете.';
  var FALLBACK = 'За то је потребна консултација са адвокатом. Позовите или оставите број, јавићемо се.';
  var RULES = [
    { k: ['радно време', 'радно', 'кад', 'када', 'отворено', 'сати', 'сату'],
      a: 'Радним данима 09–17 [ПОТВРДИТИ]. Ако не добијете позив, оставите поруку и јавићемо се.' },
    { k: ['адреса', 'адреси', 'где', 'локациј', 'канцеларија', 'канцеларији', 'улица'],
      a: 'Канцеларија је у Панчеву, Војводе Радомира Путника 7.' },
    { k: ['области', 'област', 'чиме', 'кривич', 'малолет', 'одбран', 'бавите'],
      a: 'Кривично право и одбрана, као и заступање малолетника. Списак стоји у делу 01 Области.' },
    { k: ['заказ', 'термин', 'састанак', 'консултациј', 'договор', 'закажем'],
      a: 'Позовите 060 503 30 52 или попуните форму у делу 04 Контакт, па договарамо термин.' },
    { k: ['донети', 'документ', 'папир', 'понет', 'донесем', 'потребно да'],
      a: 'Понесите личну карту, сва решења и позиве које сте примили, кратак преглед догађаја и питања која имате.' },
    { k: ['цена', 'цену', 'колико', 'кошта', 'хонорар', 'плаћањ', 'тариф', 'наплаћ'],
      a: 'Цену и ток поступка адвокат договара на консултацији. Позовите 060 503 30 52 или оставите број.' }
  ];

  function norm(s) {
    s = s.toLowerCase();
    return s.replace(/[žšč]/g, function (c) { return { 'ž': 'z', 'š': 's', 'č': 'c' }[c]; })
            .replace(/ć/g, 'c').replace(/đ/g, 'd');
  }
  function hit(q, kw) { return q.indexOf(norm(kw)) > -1 || q.indexOf(norm(toLat(kw))) > -1; }

  function answer(msg) {
    var q = norm(msg);
    for (var i = 0; i < RULES.length; i++)
      for (var j = 0; j < RULES[i].k.length; j++)
        if (hit(q, RULES[i].k[j])) return { text: RULES[i].a, call: false };
    return { text: FALLBACK, call: true };
  }

  function bubble(txt, mine, withCall) {
    var b = d.createElement('div');
    b.className = 'bub' + (mine ? ' me' : '');
    var p = d.createElement('span'); p.textContent = T(txt); b.appendChild(p);
    if (withCall) {
      var a = d.createElement('a');
      a.className = 'btn btn-s'; a.href = 'tel:+381605033052';
      a.style.display = 'inline-flex'; a.textContent = T('Позови');
      b.appendChild(d.createElement('br')); b.appendChild(a);
    }
    log.appendChild(b); log.scrollTop = log.scrollHeight;
  }

  function openLina() {
    if (!lina) return;
    linaLast = d.activeElement;
    lina.setAttribute('data-open', '1');
    if (!greeted) { greeted = true; bubble(HELLO, false, false); }
    d.addEventListener('keydown', linaTrap);
    if (linaIn) linaIn.focus();
  }
  function closeLina() {
    if (!lina) return;
    lina.setAttribute('data-open', '0');
    d.removeEventListener('keydown', linaTrap);
    if (linaLast) linaLast.focus();
  }
  var lo = d.querySelectorAll('[data-lina-open]');
  for (var l = 0; l < lo.length; l++) lo[l].addEventListener('click', function () { closeOvl(); openLina(); });
  if (linaClose) linaClose.addEventListener('click', closeLina);

  if (linaForm) linaForm.addEventListener('submit', function (e) {
    e.preventDefault();
    var msg = (linaIn.value || '').trim();
    if (!msg) return;
    bubble(msg, true, false);
    linaIn.value = '';
    if (LINA.mode === 'live') {
      var hist = [];
      var bs = log.querySelectorAll('.bub');
      for (var i = 0; i < bs.length; i++)
        hist.push({ role: bs[i].classList.contains('me') ? 'user' : 'assistant', content: bs[i].textContent });
      fetch(LINA.endpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg, history: hist })
      }).then(function (r) { return r.json(); })
        .then(function (j) { bubble(j.reply || j.message || j.text || FALLBACK, false, false); })
        .catch(function () { bubble(FALLBACK, false, true); });
    } else {
      var a = answer(msg);
      bubble(a.text, false, a.call);
    }
  });

  /* ============ 9. Escape ============ */
  d.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (ovl && ovl.getAttribute('data-open') === '1') closeOvl();
    else if (lina && lina.getAttribute('data-open') === '1') closeLina();
  });
})();
