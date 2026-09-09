/* Адвокат Бојана Ђаковић — site.js */
var LINA = { mode: 'live', endpoint: '/ai-proxy.php' };

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

  var L2C = { 'dž':'џ','lj':'љ','nj':'њ','Dž':'Џ','DŽ':'Џ','Lj':'Љ','LJ':'Љ','Nj':'Њ','NJ':'Њ',
    'a':'а','b':'б','c':'ц','č':'ч','ć':'ћ','d':'д','đ':'ђ','e':'е','f':'ф','g':'г','h':'х','i':'и','j':'ј','k':'к','l':'л','m':'м','n':'н','o':'о','p':'п','r':'р','s':'с','š':'ш','t':'т','u':'у','v':'в','z':'з','ž':'ж',
    'A':'А','B':'Б','C':'Ц','Č':'Ч','Ć':'Ћ','D':'Д','Đ':'Ђ','E':'Е','F':'Ф','G':'Г','H':'Х','I':'И','J':'Ј','K':'К','L':'Л','M':'М','N':'Н','O':'О','P':'П','R':'Р','S':'С','Š':'Ш','T':'Т','U':'У','V':'В','Z':'З','Ž':'Ж' };
  function toCyr(s) {
    /* URL-ове и мејлове не дирамо */
    return s.split(/(https?:\/\/[^\s<>"')\]]+|[\w.+-]+@[\w-]+\.[\w.]+)/g).map(function (seg, i) {
      if (i % 2) return seg;
      var out = '', k = 0, two;
      while (k < seg.length) {
        two = seg.substr(k, 2);
        if (L2C[two] && (two === 'dž' || two === 'lj' || two === 'nj' || two === 'Dž' || two === 'DŽ' || two === 'Lj' || two === 'LJ' || two === 'Nj' || two === 'NJ')) { out += L2C[two]; k += 2; continue; }
        var ch = seg.charAt(k); out += (L2C[ch] !== undefined ? L2C[ch] : ch); k++;
      }
      return out;
    }).join('');
  }
  var HAS_CYR = /[Ѐ-џ]/, HAS_LAT = /[A-Za-zČĆŠŽĐčćšžđ]/;
  function matchScript(reply, userMsg) {
    if (HAS_CYR.test(userMsg)) return HAS_CYR.test(reply) ? reply : toCyr(reply);
    if (HAS_LAT.test(userMsg)) return HAS_CYR.test(reply) ? toLat(reply) : reply;
    return reply;
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
  var SID = '', IDLE_MS = 30 * 60 * 1000, lastMsg = 0;
  function newSid() { SID = 's' + Date.now().toString(36) + Math.random().toString(36).slice(2, 10); try { sessionStorage.setItem('lina_sid', SID); } catch (e) {} return SID; }
  try { SID = sessionStorage.getItem('lina_sid') || ''; } catch (e) {}
  if (!SID) newSid();
  var lina = d.getElementById('lina'), log = d.getElementById('linaLog'),
      linaForm = d.getElementById('linaForm'), linaIn = d.getElementById('linaIn'),
      linaClose = d.getElementById('linaClose'), linaTrap = lina ? trap(lina) : null,
      linaLast = null, greeted = false;

  var HELLO = 'Добар дан. Ја сам Lina, асистент канцеларије адвоката Бојане Ђаковић. Могу да Вам дам адресу, области рада, информацију шта понети на први разговор и начин заказивања. Правне савете даје искључиво адвокат.';
  var OFF = 'Овај асистент одговара искључиво на питања о раду канцеларије. За заказивање разговора: 060 503 30 52.';
  var TEL = '060 503 30 52';
  var RADNO = 'Термин се договара телефоном';

  function norm(s) {
    s = toLat(String(s || '')).toLowerCase();
    s = s.replace(/[žšč]/g, function (c) { return { 'ž': 'z', 'š': 's', 'č': 'c' }[c]; }).replace(/ć/g, 'c').replace(/đ/g, 'd');
    return ' ' + s.replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim() + ' ';
  }
  function sada() {
    try {
      return new Intl.DateTimeFormat('sr-Latn', { timeZone: 'Europe/Belgrade', hour: '2-digit', minute: '2-digit', hour12: false }).format(new Date());
    } catch (e) { var t = new Date(); return ('0' + t.getHours()).slice(-2) + ':' + ('0' + t.getMinutes()).slice(-2); }
  }
  /* Намере: редослед = приоритет при изједначеном скору. p = регекси, a = одговор (стринг или функција), call = дугме Позови */
  function datum() {
    try { return new Intl.DateTimeFormat('sr-Cyrl-RS', { timeZone: 'Europe/Belgrade', weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }).format(new Date()); }
    catch (e) { var t = new Date(); return t.getDate() + '.' + (t.getMonth() + 1) + '.' + t.getFullYear() + '.'; }
  }
  /* Безбедан рачун: само цифре, размаци, + - * / x × ( ) , . */
  function racun(q) {
    var m = q.match(/(\d[\d\s+\-*\/x×().,]*\d)/); if (!m) return null;
    var ex = m[1].replace(/[x×]/g, '*').replace(/,/g, '.');
    if (!/[+\-*\/]/.test(ex) || !/^[\d\s+\-*\/().]+$/.test(ex)) return null;
    try { var r = Function('"use strict";return (' + ex + ')')(); if (typeof r !== 'number' || !isFinite(r)) return null; return { ex: ex.replace(/\s+/g, ' ').trim(), r: Math.round(r * 1000) / 1000 }; } catch (e) { return null; }
  }
  var ENG = /\b(the|is|are|you|your|do|does|can|what|where|when|how|hello|hi|please|thanks|thank|office|lawyer|speak|english|open|address|phone)\b/g;

  /* Намере: редослед = приоритет при изједначеном скору. p = регекси, a = одговор (стринг или функција), call = дугме Позови */
  var INTENTS = [
    { id: 'hitno', p: [/hitno/, /uhaps/, /pritvor/, /policij/, /saslusanj/, /privedn/, /zadrzan/],
      a: 'У хитним ситуацијама позовите одмах ' + TEL + '. Ако се не јави, пошаљите СМС и јавићемо се у најкраћем року.', call: true },
    { id: 'vreme', p: [/koliko je sati/, /koliko ima sati/, /koje je vreme/, /koliko je sada/, /koliko je sat/, /tacno vreme/],
      a: function () { return OFF; } },
    { id: 'datum', p: [/koji je dan/, /koji je danas/, /koji je datum/, /danas je/, /koji dan/, /koji datum/, /koja je godina/],
      a: function () { return OFF; } },
    { id: 'prognoza', p: [/kakvo je vreme/, /prognoz/, /kisa/, /pada li/, /sneg/, /toplo/, /hladno/, /temperatur/, /sunc/],
      a: function () { return OFF; } },
    { id: 'provok', p: [/peder/, / gej/, /lezb/, /homo/, /transic/, /kurv/, /drolj/, /jesi li glup/, /glupa/, /tupa/, /glupac/, /idiot/, /kreten/, /debil/, /budal/, /retard/, /jeb/, /pick/, /sranje/, /govn/, /mrs /, /sit /, /odjeb/, /mamu/, /kur[ac]/],
      a: OFF },
    { id: 'kakosi', p: [/kako si/, /kako ste/, /sta radis/, /sta ima/, /kako ide/, /jesi tu/, /jesi li tu/, /ima li koga/, /dosadno/],
      a: OFF },
    { id: 'flert', p: [/volim te/, /udaj se/, /hoces kafu/, /kafu/, /pivo/, /izlazak/, /lepa si/, /slatka/, /simpatic/, /brak sa mnom/, /devojk/, /decko/],
      a: OFF },
    { id: 'vic', p: [/vic/, /salu/, /sala /, /nasmej/, /smesno/, /zabav/],
      a: OFF },
    { id: 'pancevo', p: [/gde je pancevo/, /koliko je daleko/, /od beograda/, /do pancev/, /kako do pancev/, /autobus/, /voz /],
      a: 'Панчево је око 15 км североисточно од Београда, преко Панчевачког моста. Канцеларија је у центру, Војводе Радомира Путника 7.' },
    { id: 'bojana', p: [/ko je bojana/, /ko je advokat/, /o advokat/, /o bojani/, /koja je ona/, /iskustv/, /biograf/, /obrazovanj/, /fakultet/],
      a: 'Бојана Ђаковић је адвокат у Панчеву, члан Адвокатске коморе Војводине од 2018. године. Области рада: имовинско право, катастар непокретности и радно право. Више у делу 02 О мени.' },
    { id: 'radno', p: [/radno vreme/, /radno/, /kad radi/, /kada radi/, /radite li/, /radi li/, /do kad/, /do koliko/, /od koliko/, /otvoren/, /kad ste tu/, /vikend/, /subot/, /nedelj/],
      a: 'Термин се договара позивом на ' + TEL + ' или путем форме у делу 04 Контакт.' },
    { id: 'adresa', p: [/adres/, /gde se nalaz/, /gde ste/, /gde je kancelarij/, /lokacij/, /kancelarij/, /ulic/, /kako da dod/, /kako do vas/, /parking/],
      a: 'Канцеларија је у Панчеву, Војводе Радомира Путника 7. Мапа: https://maps.google.com/?q=Vojvode+Radomira+Putnika+7,+Pancevo' },
    { id: 'cena', p: [/koliko kosta/, /koliko je cena/, /kolika je cena/, /cen[aeu] /, /cenovnik/, /kosta/, /honorar/, /tarif/, /plac/, /naplac/, /koliko novca/, /skupo/, /jeftin/, /besplatn/],
      a: 'Цену и ток поступка адвокат договара на консултацији, у складу са адвокатском тарифом. Позовите ' + TEL + ' или оставите број.' },
    { id: 'zakaz', p: [/zakaz/, /termin/, /sastanak/, /konsultacij/, /dogovor/, /javiti se/, /kako da vas kontaktir/, /prijem/],
      a: 'Позовите ' + TEL + ' или попуните форму у делу 04 Контакт, па договарамо термин који вам одговара.' },
    { id: 'doneti', p: [/donet/, /dones/, /ponet/, /pones/, /dokument/, /papir/, /sta mi treba/, /sta treba da/, /sta da nosim/],
      a: 'Понесите личну карту, уговоре, решења, лист непокретности и другу документацију коју имате, кратак хронолошки преглед догађаја и питања која имате.' },
    { id: 'kontakt', p: [/telefon/, /broj telefona/, /mejl/, /mail/, /kontakt/, /kako da pozovem/, /viber/, /whatsapp/],
      a: 'Телефон: ' + TEL + '. Мејл: advokat.bdjakovic@gmail.com. Најбрже је позивом.', call: true },
    { id: 'oblasti', p: [/oblast/, /cime se bav/, /bavite/, /bavi se/, /imovin/, /katastar/, /nepokretn/, /radno pravo/, /gradjansk/, /zastup/, /svojin/, /ugovor/, /nekretnin/, /otkaz/, /radni spor/, /zarad/, /plac[eu] /, /deob/, /uknjiz/, /list nepokretnosti/],
      a: 'Области рада су имовинско право, катастар непокретности и радно право. Списак стоји у делу 01 Области.' },
    { id: 'druge', p: [/razvod/, /brak /, /aliment/, /starateljstv/, /krivic/, /malolet/, /prekrsaj/, /saobracaj/, /kazn[ae] /, /prijav[au] /],
      a: 'Наведене области рада су имовинско право, катастар непокретности и радно право. За ово питање најбоље је да позовете ' + TEL + ', адвокат ће Вам рећи да ли може да помогне или да Вас упути.', call: true },
    { id: 'pravni', p: [/da li mogu/, /mogu li/, /sta da radim/, /moj slucaj/, /tuzb/, /kazn/, / sud /, /presud/, /zalb/, /optuz/, /prijav/, /svedok/, /dokaz/, /rok za/],
      a: 'Не могу да процењујем ваш случај, то ради адвокат на консултацији. Могу да вам помогнем да је закажете: позовите ' + TEL + ' или оставите број у форми.', call: true },
    { id: 'ko', p: [/ ko si/, / sta si ti/, /jesi li robot/, /jesi li bot/, /jesi ti robot/, /jesi ti bot/, /zensko/, /musko/, /covek/, /kako se zoves/, /jesi li prav/, /jesi li ziv/, / ai /, /vestack/, /lina/],
      a: 'Ја сам Lina, асистент канцеларије. Помажем око адресе, области рада и заказивања. Правне савете даје искључиво адвокат.' },
    { id: 'hvala', p: [/hvala/, /fala/, /zahvalj/, /super/, /odlicno/, / ok /, /okej/, /vazi/, /bravo/],
      a: 'Молим. За разговор са адвокатом позовите ' + TEL + '.' },
    { id: 'zdravo', p: [/zdravo/, / cao/, /dobar dan/, /dobro jutro/, /dobro vece/, /pozdrav/, /hej /, /hello/, /halo/, / ej /],
      a: 'Добар дан. Изволите: адреса, области рада или заказивање разговора.' },
    { id: 'dovidjenja', p: [/dovidjenja/, /vidimo se/, /prijatno/, /zbogom/],
      a: 'Пријатно. Заказивање: ' + TEL + '.' }
  ];
  var FALLBACK1 = 'Нисам разумела питање. Могу да одговорим о адреси, областима рада, шта понети и како да закажете разговор.';
  var FALLBACK2 = 'Изгледа да је питање за адвоката. Позовите ' + TEL + ' или оставите број у форми, јавићемо се.';
  var misses = 0;

  function answer(msg) {
    var q = norm(msg);
    /* 1) рачун */
    var rc = racun(String(msg).toLowerCase()); if (rc) { misses = 0; return { text: OFF, call: false }; }
    /* 2) енглески */
    var em = q.match(ENG); if (em && em.length >= 2 && !/[đžćčš]/.test(msg) && !/(kad|gde|koliko|sta|kako|zakaz|adres)/.test(q)) {
      misses = 0;
      return { text: "Good day. I am Lina, the office assistant of attorney Bojana Đaković. Address: Vojvode Radomira Putnika 7, Pančevo. To arrange a consultation call +381 60 503 30 52 or use the form in section 04. Legal advice is given only by the attorney.", call: true, raw: true };
    }
    /* 3) намере по скору */
    var best = null, bestScore = 0;
    for (var i = 0; i < INTENTS.length; i++) {
      var sc = 0;
      for (var k = 0; k < INTENTS[i].p.length; k++) if (INTENTS[i].p[k].test(q)) sc++;
      if (sc > bestScore) { bestScore = sc; best = INTENTS[i]; }
    }
    if (!best) { misses++; return misses >= 2 ? { text: FALLBACK2, call: true } : { text: FALLBACK1, call: false }; }
    misses = 0;
    var t = typeof best.a === 'function' ? best.a(q) : best.a;
    return { text: t, call: !!best.call };
  }

  function bubble(txt, mine, withCall, raw) {
    var b = d.createElement('div');
    b.className = 'bub' + (mine ? ' me' : '');
    var p = d.createElement('span'), full = (mine || raw) ? txt : T(txt);
    if (!mine) {
      /* markdown [текст](url) -> url, **bold** -> обичан текст */
      full = full.replace(/\[([^\]]*)\]\((https?:\/\/[^\s)]+)\)/g, '$2').replace(/\*\*([^*]+)\*\*/g, '$1').replace(/^\s*[-*]\s+/gm, '');
    }
    if (!mine && /https?:\/\/\S+/.test(full)) {
      var parts = full.split(/(https?:\/\/[^\s<>"'\])]+)/g);
      for (var pi = 0; pi < parts.length; pi++) {
        if (/^https?:\/\//.test(parts[pi])) {
          var u = parts[pi].replace(/[.,;:!?]+$/, ''), tail = parts[pi].slice(u.length);
          var an = d.createElement('a'); an.href = u; an.target = '_blank'; an.rel = 'noopener';
          an.textContent = /maps\.google|goo\.gl\/maps|maps\.app/.test(u) ? T('Отвори мапу') : u;
          p.appendChild(an); if (tail) p.appendChild(d.createTextNode(tail));
        } else if (parts[pi]) p.appendChild(d.createTextNode(parts[pi]));
      }
    } else p.textContent = full;
    b.appendChild(p);
    if (withCall) {
      var a = d.createElement('a');
      a.className = 'btn btn-s'; a.href = 'tel:+381605033052';
      a.style.display = 'inline-flex'; a.textContent = T('Позови');
      b.appendChild(d.createElement('br')); b.appendChild(a);
    }
    log.appendChild(b); log.scrollTop = log.scrollHeight;
  }

  function resetLina() {
    if (!log) return;
    log.innerHTML = ''; newSid(); greeted = false; misses = 0; lastMsg = 0;
    greeted = true; bubble(HELLO, false, false);
    if (linaIn) { linaIn.value = ''; linaIn.focus(); }
  }
  function openLina() {
    if (!lina) return;
    linaLast = d.activeElement;
    lina.setAttribute('data-open', '1');
    if (greeted && lastMsg && Date.now() - lastMsg > IDLE_MS) { resetLina(); }
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
  var linaReset = d.getElementById('linaReset');
  if (linaReset) linaReset.addEventListener('click', resetLina);

  if (linaForm) linaForm.addEventListener('submit', function (e) {
    e.preventDefault();
    var msg = (linaIn.value || '').trim();
    if (!msg) return;
    bubble(msg, true, false);
    linaIn.value = ''; lastMsg = Date.now();
    if (LINA.mode === 'live') {
      var typing = d.createElement('div'); typing.className = 'bub typing'; typing.setAttribute('aria-label', 'Lina куца');
      typing.innerHTML = '<i></i><i></i><i></i>'; log.appendChild(typing); log.scrollTop = log.scrollHeight;
      var ctrl = ('AbortController' in window) ? new AbortController() : null;
      var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 15000);
      var done = function () { clearTimeout(timer); if (typing.parentNode) typing.parentNode.removeChild(typing); };
      var hist = [];
      var bs = log.querySelectorAll('.bub:not(.typing)');
      for (var i = 0; i < bs.length; i++)
        hist.push({ role: bs[i].classList.contains('me') ? 'user' : 'assistant', content: bs[i].textContent });
      fetch(LINA.endpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg, session_id: SID, history: hist }),
        signal: ctrl ? ctrl.signal : undefined
      }).then(function (r) { if (r.status === 429) return { reply: FALLBACK2 }; return r.json(); })
        .then(function (j) {
          done();
          var t = j && (j.reply || j.answer || j.message || j.text);
          if (t) bubble(matchScript(String(t), msg), false, false, true); else { var a0 = answer(msg); bubble(a0.text, false, a0.call, a0.raw); }
        })
        .catch(function () { done(); var a1 = answer(msg); bubble(a1.text, false, a1.call, a1.raw); });
    } else {
      var a = answer(msg);
      bubble(a.text, false, a.call, a.raw);
    }
  });

  /* ============ 9. Escape ============ */
  d.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (ovl && ovl.getAttribute('data-open') === '1') closeOvl();
    else if (lina && lina.getAttribute('data-open') === '1') closeLina();
  });
})();
