# Адвокат Бојана Ђаковић — статични сајт (v1)

Статичан једностранични сајт + `/vizitka/` страна. Без билд корака, без фрејмворка,
без npm зависности у испоруци. Спреман за директан upload у Hestia `public_html`.

---

## 1. Структура

```
public_html/
├─ index.html                  једна страна: hero + 01–04 секције, футер, Лина
├─ vizitka/index.html          дигитална визит-карта (navy, за ходник суда)
├─ kontakt.php                 обрада форме (mail + honeypot + rate-limit)
├─ .htaccess                   безбедносна заглавља, CSP, кеш, компресија
├─ robots.txt
├─ sitemap.xml                 2 URL-а (домен https://advokatdjakovic.rs)
├─ favicon.svg                 монограм „Ђ" на navy подлози
└─ assets/
   ├─ css/site.css             сав CSS (17,6 KB)
   ├─ js/site.js               сав JS (13,5 KB)
   ├─ kontakt.vcf              vCard 3.0, UTF-8
   ├─ fonts/                   5 self-hosted woff2 фајлова (122,4 KB укупно)
   │  ├─ noto-serif-400.woff2      Noto Serif regular
   │  ├─ noto-serif-400i.woff2     Noto Serif italic  ← српски курзивни облици
   │  ├─ noto-serif-700.woff2      Noto Serif bold
   │  ├─ plex-sans-400.woff2       IBM Plex Sans regular (UI ситнице)
   │  └─ plex-sans-500.woff2       IBM Plex Sans medium
   └─ img/
      ├─ logo.svg              теразије (прецртано са визитке)
      ├─ cursor-tas.svg        курсор — тас, 20×20, само на desktop hover
      ├─ qr-vcard.svg          QR ка https://advokatdjakovic.rs/assets/kontakt.vcf
      └─ og.png                1200×630 OG слика (кремаста, navy знак и име)
```

**Величине (некомпримовано)**

| фајл | KB |
|---|---|
| index.html | 16,1 |
| vizitka/index.html | 3,1 |
| assets/css/site.css | 17,6 |
| assets/js/site.js | 13,5 |
| **CSS + JS укупно** | **31,1** (лимит 60) |
| фонтови (5 фајлова) | 122,4 |
| assets/img/og.png | 75,4 |
| assets/img/qr-vcard.svg | 8,7 |
| kontakt.php | 2,6 |
| **све укупно** | **263,5** |

---

## 2. Upload у Hestia

1. У Hestia: **Web → advokatdjakovic.rs → File Manager** (или SFTP/rsync).
2. Копирај **садржај** фолдера `public_html/` у `/home/<korisnik>/web/advokatdjakovic.rs/public_html/`
   — дакле `index.html` мора да буде директно у `public_html`, не у подфолдеру.
   Обавезно пренеси и скривени `.htaccess`.
3. Дозволе: фолдери `755`, фајлови `644`.
4. У Hestia укључи **SSL (Let's Encrypt)** и **Force HTTPS** — `.htaccess` шаље HSTS заглавље,
   па сајт мора да ради на HTTPS-у пре него што се то заглавље пусти у продукцију.
5. PHP мора да буде укључен за домен (због `kontakt.php`). Ако `mail()` није дозвољен,
   форма ће редиректовати на `/?sent=0#kontakt` — тада треба подесити SMTP на серверу.
6. Провери: `https://advokatdjakovic.rs/` и `https://advokatdjakovic.rs/vizitka/`.

**Верзионисање кеша.** Сви `assets` се кеширају годину дана (`immutable`).
Кад мењаш `site.css` или `site.js`, повећај `?v=1` → `?v=2` у `index.html`
и `vizitka/index.html` (има их 5 места: css, js, 2× preload фонта, qr слика).

---

## 3. Где се мења телефон / адреса / радно време

Ово је статичан сајт, па не постоји база — али сви подаци стоје на **тачно
одређеним, пописаним местима** и мењају се једном командом.

### Телефон (`060 503 30 52` / `+381605033052`)
| фајл | линије |
|---|---|
| `index.html` | meta description (7), JSON-LD (26), мени (72, 73), hero (98), контакт (177), политика приватности (231), sticky трака (237) |
| `vizitka/index.html` | meta description (7), og:description (12), контакт (42) |
| `assets/js/site.js` | Лина одговори (213, 217), дугме „Позови" (241) |
| `assets/kontakt.vcf` | `TEL;TYPE=CELL,VOICE:` (7) |

Замена из фолдера `public_html`:

```bash
# приказ формата (за људе) и tel: формата (за линкове)
grep -rl "060 503 30 52" . | xargs sed -i 's/060 503 30 52/НОВИ БРОЈ/g'
grep -rl "+381605033052" . | xargs sed -i 's/+381605033052/+381НОВИБРОЈ/g'
```

### Адреса (`Војводе Радомира Путника 7`)
`index.html`, `vizitka/index.html`, `assets/js/site.js` (одговор Лине), `assets/kontakt.vcf`.

```bash
grep -rl "Војводе Радомира Путника 7" . | xargs sed -i 's/Војводе Радомира Путника 7/НОВА АДРЕСА/g'
```
Уз то ручно измени и **maps линк** у `index.html` (`https://maps.google.com/?q=...`)
и `streetAddress` у JSON-LD.

### Радно време (`Радним данима 09–17 [ПОТВРДИТИ]`)
| фајл | место |
|---|---|
| `index.html` | линија 179 (`<dt>Радно време</dt>`) и `openingHours` у JSON-LD (линија 26) |
| `assets/js/site.js` | линија 207 (Лина, правило „радно време") |

### Мејл примаоца форме
Само `kontakt.php`, у блоку `ПОДЕШАВАЊА` на врху: `$PRIMALAC`.

---

## 4. Лина — demo → live

На врху `assets/js/site.js`:

```js
var LINA = { mode: 'demo', endpoint: '/ai-proxy.php' };
```

- `mode: 'demo'` (тренутно) — одговара локално, по кључним речима, **без иједног мрежног
  захтева**. Правила су у низу `RULES` (6 типова питања + fallback).
- `mode: 'live'` — на сваку поруку шаље `POST` JSON `{message, history}` на `endpoint`
  и приказује `reply` (или `message` / `text`) из одговора. Ако захтев падне, приказује
  fallback поруку са дугметом „Позови".

Прелазак у live:
1. Промени `mode` у `'live'`.
2. Направи `ai-proxy.php` на серверу — **API кључ стоји само тамо, у серверском
   фајлу или у окружењу; нигде у фронтенду.**
3. `connect-src 'self'` у CSP већ дозвољава позив ка сопственом домену. Ако прокси
   буде на другом домену, мораш да га додаш у `connect-src`.

Лина ради и на латиници — одговори се транслитерирају истим механизмом као и остатак сајта,
а кључне речи се препознају и ћирилицом и латиницом (са и без квачица).

---

## 5. CSP hash

`.htaccess` садржи:

```
script-src 'self' 'sha256-d/h/mX4TA2LAtmmuPfNzC5PWPpxX1S6rv77V0/ec2EU='
```

Тај hash припада **inline boot скрипту** у `<head>` (исти је у `index.html` и
`vizitka/index.html`). Boot скрипт скида класу `no-js`, ставља `js`, и пре првог
исцртавања примењује сачувани избор писма (`localStorage.pismo`), да нема треперења.

Ако тај скрипт икада промениш (макар и један размак), израчунај нови hash:

```bash
python3 - <<'PY'
import re, hashlib, base64
s = open('public_html/index.html', encoding='utf-8').read()
code = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
print('sha256-' + base64.b64encode(hashlib.sha256(code.encode()).digest()).decode())
PY
```
и упиши га у `.htaccess`.

---

## 6. Шта клијент треба да попуни (placeholder-и)

Сви су у угластим заградама и **видљиви су на сајту**, намерно, да се не заборави.

| место | placeholder | шта треба |
|---|---|---|
| `index.html` 01 Области, картица 3 | `[ДОПУНИТИ: област]` + `[ДОПУНИТИ]` | назив области + 2 реченице |
| `index.html` 01 Области, картица 4 | `[ДОПУНИТИ: област]` + `[ДОПУНИТИ]` | назив области + 2 реченице |
| `index.html` 02 О мени | `[ДОПУНИТИ: образовање]` | факултет, година дипломирања |
| `index.html` 02 О мени | `[ДОПУНИТИ: година уписа у АКВ]` | година уписа у именик АКВ |
| `index.html` 02 О мени | `[ДОПУНИТИ: кратка биографија]` | 2–3 реченице |
| `index.html` 02 О мени | `[ФОТОГРАФИЈА]` | црно-бели портрет 3:4; замени `<figure class="portrait">` са `<img>` |
| `index.html` 04 Контакт | `Радним данима 09–17 [ПОТВРДИТИ]` | потврдити или исправити радно време |
| `assets/js/site.js` линија 207 | исто радно време у Лининим одговорима | исто |
| `index.html` JSON-LD | `"openingHours":"Mo-Fr 09:00-17:00"` | ускладити са стварним |

Домен `advokatdjakovic.rs` је коришћен у canonical/OG/sitemap/QR. Ако домен буде други,
мења се на тим местима **и QR се мора регенерисати** (тренутни QR води на
`https://advokatdjakovic.rs/assets/kontakt.vcf`).

---

## 7. Шта је проверено (Playwright, локално, `file://`)

Скрипт: `<scratchpad>/advokat_build/shots.mjs`, снимци у `<scratchpad>/advokat_build/shots/`.

| провера | резултат |
|---|---|
| Нема хоризонталног скрола (320 / 360 / 390 / 414 / 768 / 1024 / 1440 px) | ✅ `scrollWidth == innerWidth` на свим ширинама |
| Нула екстерних мрежних захтева (desktop, Лина, визитка) | ✅ `[]` |
| Прекидач писма мења текст, `lang`, `title` | ✅ `sr-Cyrl` → `sr-Latn`, „Бојана Ђаковић" → „Bojana Đaković" |
| Избор писма опстаје после reload-а | ✅ (localStorage, примењен boot скриптом) |
| Повратак на ћирилицу | ✅ |
| Без JS-а: страна читљива, све секције видљиве, ћирилица | ✅ `opacity:1`, `lang=sr-Cyrl` |
| Све 4 ставке раила скролују на секцију и активна се мења | ✅ `sectionTop=0px`, `.on` прати секцију |
| Мека мембрана раила (mousemove, ≤2px, радијални градијент) | ✅ помак −2px…+2px, `--my` се поставља |
| Лина: 6 типова питања + fallback | ✅ ћирилицом и латиницом, без мрежних захтева |
| Лина fallback има дугме „Позови" | ✅ |
| Escape затвара мени; focus trap | ✅ |
| HTML валидан (`html5lib`, strict) | ✅ обе стране, тачно један `<h1>` по страни |
| `prefers-reduced-motion` | ✅ reveal одмах видљив, лого одмах нацртан (`stroke-dashoffset: 0px`) |
| Српски курзивни облици (`locl` / `SRB`) | ✅ проверено у самом woff2: `б г д п т` (курзив), `б` (усправно) |
| Валидан XML у SVG-овима и sitemap-у | ✅ |
| `kontakt.php` — исправан унос | ✅ `303 → /?sent=1#kontakt`, мејл састављен исправно |
| `kontakt.php` — honeypot попуњен | ✅ тихо одбијено (`sent=1`, мејл се не шаље) |
| `kontakt.php` — без сагласности / празно име / лош телефон | ✅ `sent=0`, нема слања |
| `kontakt.php` — rate-limit (2 слања у истој сесији) | ✅ друго слање одбијено |
| `kontakt.php` — CRLF у пољу „име" (header injection) | ✅ неутралисано, нема `Bcc` заглавља |
| `kontakt.php` — синтакса | ✅ `php -l`: нема грешака |
| `kontakt.php` — GET уместо POST | ✅ редирект на `/#kontakt` |

Снимци екрана:
`desktop-1440-hero.png`, `desktop-1440-full.png`, `desktop-1440-lina.png`, `desktop-1440-lat.png`,
`mobile-390-hero.png`, `mobile-390-full.png`, `mobile-390-menu.png`, `mobile-390-lina.png`,
`mobile-390-nojs.png`, `vizitka-390.png`, `vizitka-1440.png`.

---

## 8. Није проверено / одступања

**Није проверено**
- **Стварно слање мејла.** `kontakt.php` је извршен и тестиран (PHP 8, уграђени сервер,
  `sendmail_path` замењен стубом) — валидација, honeypot, rate-limit, UTF-8 наслов,
  `Reply-To` и заштита од убацивања заглавља раде како треба (види табелу изнад).
  Оно што **није** проверено јесте да ли Hestia сервер уопште испоручује пошту
  преко `mail()` — то се види тек на серверу.
- `.htaccess` није тестиран под Apache-ом (нема Apache-а овде). Синтакса је писана
  дефанзивно (`<IfModule>`), али провери након upload-а да ли заглавља стижу:
  `curl -I https://advokatdjakovic.rs/`.
- Прави изглед у Safari / iOS није проверен (тестирано само у Chromium-у).
  Пажња: SVG курсор и `<dialog>` раде у свим актуелним прегледачима, али на старијем
  iOS-у `<dialog>` има fallback (`open` атрибут) — визуелно је прихватљиво, али није виђено уживо.
- Скенирање QR кода правим телефоном није урађено (генерисан је библиотеком `qrcode`,
  ECC ниво M, 33×33 модула, бела зона 2 модула).

**Одступања од спеца (свесна, минимална)**
1. **Боја navy није узета директно са фотографије визитке.** Фотографија је снимљена
   на дневном светлу и подекспонирана — бело у логоу мери се као `#8A9394`, а плава као
   `#4E5D6C`, што није боја штампе него осветљења. Узет је **тон** (нијанса 207°, поклапа
   се са спецификованим `#17324D` = 210°) и коришћена је вредност из спеца: **`#17324D`**.
2. **Редирект после слања форме је `/?sent=1#kontakt`**, а не `#kontakt?sent=1`.
   Разлог: у `#kontakt?sent=1` цео стринг `kontakt?sent=1` је фрагмент, па прегледач
   не би скроловао на секцију. JS препознаје `sent=1` и у `search` и у `hash`,
   па оба облика раде.
3. **Фонтови нису скинути преко `fonts.googleapis.com/css2` URL-ова.** Тај API враћа
   засебан woff2 по писму (cyrillic и latin одвојено), што би било 10 фајлова —
   изнад лимита од 6. Уместо тога скинути су варијабилни TTF-ови из Google Fonts
   репозиторијума, инстанцирани на `wght 400/700`, subset-овани на latin+cyrillic и
   компримовани у woff2 (`fontTools`). Резултат: **5 фајлова, 122,4 KB**.
4. **Изабран је Noto Serif, не Literata.** Провера `fontTools`-ом: Literata **нема**
   `locl` са тагом `SRB` (`cyrl` скрипт без LangSys записа), па не би дала српске
   курзивне облике. Noto Serif Italic има тачно тражених пет: `б г д п т`.
   Source Serif 4 има `SRB` LangSys али без одговарајућих глифова.
5. **„Једно место" за телефон/адресу.** Статични HTML нема једно место — уместо тога
   у одељку 3 постоји потпун попис свих појава са бројевима линија и готова `sed` команда.

**Није урађено**
- Ништа из спеца није изостављено осим горе наведеног.
- Нема git commit-а (по инструкцији).
