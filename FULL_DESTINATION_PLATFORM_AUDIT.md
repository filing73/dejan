# FULL DESTINATION PLATFORM AUDIT
## dlproject56.com — Scalable Visual Destination Platform
**Audit date:** 2026-06-19  
**Auditor:** Claude Code (automated analysis)

---

## AUDIT SCOPE & METHOD

**What was read directly:**
- Server backup (April 2026): `index.html`, all service pages, `global.css`, `global.js`, full `images/` inventory
- Python image processor script: `process_destination_images.py` (defines all 9 target destinations)

**What cannot be confirmed remotely:**
- Local active-site files not yet pushed to the repo: `destinations/`, `italy/`, `spain/`, `greece/`, `malta/` pages  
- The observations for those pages are marked **[INFERRED]** based on user-stated requirements and site patterns

**Source of truth for site style:** server backup index.html is the confirmed design standard.

---

## A) PAGE-BY-PAGE PROBLEMS

---

### 1. `index.html` — Main Homepage
**Source:** CONFIRMED (server backup, April 2026)  
**Status:** ⚠️ INCOMPLETE — Malta-only, not multi-destination

| Check | Finding |
|-------|---------|
| Hero image | ✅ Real image: `url('../images/crystal-clear-lagoon-malta.webp')` |
| Image breaks | ✅ Real images: mdina-old-city-malta.webp, luxury-rooftop-pool-sea-view.webp |
| Service card images | ✅ All 4 cards have real images |
| HERO IMAGE PLACEHOLDER | Not present |
| IMAGE PLACEHOLDER | Not present |
| Chat assistant | ❌ ABSENT — only WhatsApp floating button |
| Navigation to destinations | ❌ No link to destinations hub |
| Scope | Malta-only — no mention of Italy, Spain, Greece |

**Missing for platform goal:**
- The homepage is Malta-specific. Converting it to a multi-destination platform requires either: (a) a redesigned homepage with destinations grid, or (b) a persistent nav link to `/destinations/`
- No proactive assistant
- Footer nav links: Home, Pricing, Contact — destinations not linked

**Recommended HTML changes (when ready):**
- Add `<a href="/destinations/">Destinations</a>` to footer nav
- Add destinations section or hero subtitle pointing to `/destinations/`
- Add proactive chat script (see Section C)

**Priority:** HIGH (this is the entry point for all traffic)

---

### 2. `destinations/index.html` — All Destinations Hub
**Source:** [INFERRED] — page exists locally, not in repo or server backup  
**Status:** ⚠️ INCOMPLETE — destination card images likely missing

| Check | Finding |
|-------|---------|
| Hero image | [INFERRED] HERO IMAGE PLACEHOLDER — `/images/destinations/` folder does not exist yet |
| Destination cards | [INFERRED] IMAGE PLACEHOLDER — 9 card images not yet present |
| Images referenced | `/images/destinations/malta.webp`, `santorini.webp`, `sicily.webp`, `ibiza.webp`, `rome.webp`, `venice.webp`, `mallorca.webp`, `barcelona.webp` |
| Chat assistant | [INFERRED] ABSENT |

**What needs to happen:**
1. Run `process_destination_images.py` → creates all 9 `/images/destinations/*.webp` files
2. Verify each card's `background-image` URL matches the exact filenames above
3. Add proactive assistant (20s delay)

**Recommended image filenames:**
- Hero of this page: reuse `sandy-beach-aerial-view.webp` (already in `/images/`) as hub hero, OR add `/images/destinations/destinations-hub-hero.webp`
- Cards: the 9 files from the script

**Priority:** HIGH (gateway to all destination content)

---

### 3. `italy/index.html` — Italy Country Landing Page
**Source:** [INFERRED] — page exists locally  
**Status:** ⚠️ INCOMPLETE — hero and destination cards need images

| Check | Finding |
|-------|---------|
| Hero background | [INFERRED] HERO IMAGE PLACEHOLDER or references `/images/destinations/sicily.webp` or `/images/destinations/rome.webp` as a fallback |
| Sub-destination cards | [INFERRED] IMAGE PLACEHOLDER for Sicily card, Rome card, Venice card |
| Images that should appear | sicily.webp, rome.webp, venice.webp, taormina-amphitheatre-sicily.webp (already in /images/) |
| Chat assistant | [INFERRED] ABSENT |

**Recommended hero:** `/images/destinations/rome.webp` (Rome is the strongest Italy draw)  
**Recommended destination cards:** `sicily.webp`, `rome.webp`, `venice.webp`  
**Proactive assistant message:** "Thinking about Italy? I can help you choose between Sicily, Rome, and Venice — just tell me what kind of trip you have in mind."

**Priority:** MEDIUM

---

### 4. `spain/index.html` — Spain Country Landing Page
**Source:** [INFERRED] — page exists locally  
**Status:** ⚠️ INCOMPLETE — hero and destination cards need images

| Check | Finding |
|-------|---------|
| Hero background | [INFERRED] HERO IMAGE PLACEHOLDER or references `/images/destinations/barcelona.webp` |
| Sub-destination cards | [INFERRED] IMAGE PLACEHOLDER for Ibiza, Mallorca, Barcelona |
| Images needed | ibiza.webp, mallorca.webp, barcelona.webp |
| Chat assistant | [INFERRED] ABSENT |

**Recommended hero:** `/images/destinations/barcelona.webp`  
**Proactive assistant message:** "Planning Spain? Sun & beach or city & culture? I can help you choose between Ibiza, Mallorca, and Barcelona."

**Priority:** MEDIUM

---

### 5. `greece/index.html` — Greece Country Landing Page
**Source:** [INFERRED] — page exists locally  
**Status:** ⚠️ INCOMPLETE — images needed

| Check | Finding |
|-------|---------|
| Hero background | [INFERRED] HERO IMAGE PLACEHOLDER or references `/images/destinations/santorini.webp` |
| Sub-destination cards | [INFERRED] IMAGE PLACEHOLDER for Santorini card |
| Images needed | santorini.webp, santorini-oia-sunset-view.webp |
| Chat assistant | [INFERRED] ABSENT |

**Recommended hero:** `/images/destinations/santorini.webp`  
**Proactive assistant message:** "Ready for Greece? Santorini is unforgettable — let me help you plan your stay there."

**Priority:** MEDIUM

---

### 6. `malta/index.html` — Malta Destination Page
**Source:** [INFERRED] — page exists locally, separate from the main Malta homepage  
**Status:** ⚠️ INCOMPLETE — needs `/images/destinations/malta.webp`

| Check | Finding |
|-------|---------|
| Hero background | [INFERRED] HERO IMAGE PLACEHOLDER — references `/images/destinations/malta.webp` |
| Section images | ✅ Existing `/images/` has 6+ real Malta images that can be reused |
| Images ready to use | crystal-clear-lagoon-malta.webp, malta-blue-lagoon-boats.webp, mdina-old-city-malta.webp, malta-sea-cave-cliffs.webp, malta-traditional-balconies.webp, luxury-coastal-resort-malta.webp |
| Chat assistant | [INFERRED] ABSENT |

**This page is in the best position** — existing Malta images from `/images/` can fill section slots immediately.  
**Hero image:** `/images/destinations/malta.webp` (from the script)  
**All other slots:** already available from existing `/images/` folder

**Priority:** HIGH (Malta is the current business core)

---

### 7. `italy/sicily/index.html` — Sicily Destination Page
**Source:** [INFERRED] — page exists locally  
**Status:** ⚠️ INCOMPLETE — hero image missing, one usable image already exists

| Check | Finding |
|-------|---------|
| Hero background | [INFERRED] HERO IMAGE PLACEHOLDER — references `/images/destinations/sicily.webp` |
| Existing usable image | ✅ `taormina-amphitheatre-sicily.webp` is ALREADY in `/images/` — use for image break |
| Additional images needed | At least 2 more (beach, coast, or Cefalù) from source folder |
| Chat assistant | [INFERRED] ABSENT |

**Hero image:** `/images/destinations/sicily.webp`  
**Image break 1:** `/images/taormina-amphitheatre-sicily.webp` (already exists, ready to use)  
**Additional recommended filenames:** `sicily-cefalu-beach.webp`, `sicily-coast-aerial.webp`

**Priority:** HIGH

---

### 8. `italy/rome/index.html` — Rome Destination Page
**Source:** [INFERRED] — page exists locally  
**Status:** ⚠️ INCOMPLETE — no Rome images exist anywhere yet

| Check | Finding |
|-------|---------|
| Hero background | [INFERRED] HERO IMAGE PLACEHOLDER — references `/images/destinations/rome.webp` |
| Existing usable images | ❌ NONE — zero Rome images in current `/images/` folder |
| Images needed | rome.webp (hero), plus 2+ section images |
| Chat assistant | [INFERRED] ABSENT |

**Most image-starved page on the site.** After the script creates `rome.webp`, still need at least 2 more Rome images for a complete feel.  
**Recommended additional filenames:** `rome-colosseum.webp`, `rome-trevi-fountain.webp`  
**Source:** look for Colosseum, Forum, Trevi, Vatican shots in `H:\DL_AI_WORK\02_ACTIVE_PROJECTS\DLPROJECT56\Duplicat za rodju`

**Priority:** HIGH

---

### 9. `italy/venice/index.html` — Venice Destination Page
**Source:** [INFERRED] — page exists locally  
**Status:** ⚠️ INCOMPLETE — no Venice images exist yet

| Check | Finding |
|-------|---------|
| Hero background | [INFERRED] HERO IMAGE PLACEHOLDER — references `/images/destinations/venice.webp` |
| Existing usable images | ❌ NONE |
| Images needed | venice.webp (hero), plus 2+ section images |
| Chat assistant | [INFERRED] ABSENT |

**Recommended additional filenames:** `venice-grand-canal.webp`, `venice-rialto-bridge.webp`

**Priority:** MEDIUM

---

### 10. `spain/ibiza/index.html` — Ibiza Destination Page
**Source:** [INFERRED] — page exists locally  
**Status:** ⚠️ INCOMPLETE — no Ibiza images exist yet

| Check | Finding |
|-------|---------|
| Hero background | [INFERRED] HERO IMAGE PLACEHOLDER — references `/images/destinations/ibiza.webp` |
| Existing usable images | ❌ NONE |
| Images needed | ibiza.webp (hero), plus 2+ section images |
| Chat assistant | [INFERRED] ABSENT |

**Recommended additional filenames:** `ibiza-cala-conta-beach.webp`, `ibiza-dalt-vila-sunset.webp`

**Priority:** MEDIUM

---

### 11. `spain/mallorca/index.html` — Mallorca Destination Page
**Source:** [INFERRED] — page exists locally  
**Status:** ⚠️ INCOMPLETE — no Mallorca destination images yet (the Mallorca map is on maps.dlproject56.com)

| Check | Finding |
|-------|---------|
| Hero background | [INFERRED] HERO IMAGE PLACEHOLDER — references `/images/destinations/mallorca.webp` |
| Existing usable images | ❌ NONE in the main site `/images/` folder |
| Images needed | mallorca.webp (hero), plus 2+ section images |
| Chat assistant | [INFERRED] ABSENT |

**Note:** The Alcudia travel map (maps.dlproject56.com/kristijan/) is a separate product. The Mallorca destination page on dlproject56.com should feel like a visual destination guide, linking to or offering the interactive map as a feature.  
**Recommended additional filenames:** `mallorca-cala-agulla-beach.webp`, `mallorca-palma-cathedral.webp`

**Priority:** MEDIUM

---

### 12. `spain/barcelona/index.html` — Barcelona Destination Page
**Source:** [INFERRED] — page exists locally  
**Status:** ⚠️ INCOMPLETE — no Barcelona images exist yet

| Check | Finding |
|-------|---------|
| Hero background | [INFERRED] HERO IMAGE PLACEHOLDER — references `/images/destinations/barcelona.webp` |
| Existing usable images | ❌ NONE |
| Images needed | barcelona.webp (hero), plus 2+ section images |
| Chat assistant | [INFERRED] ABSENT |

**Recommended additional filenames:** `barcelona-sagrada-familia.webp`, `barcelona-park-guell.webp`

**Priority:** MEDIUM

---

### 13. `greece/santorini/index.html` — Santorini Destination Page
**Source:** [INFERRED] — page exists locally  
**Status:** ⚠️ INCOMPLETE — both required images are missing

| Check | Finding |
|-------|---------|
| Hero background | [INFERRED] HERO IMAGE PLACEHOLDER — references `/images/destinations/santorini.webp` |
| Second image (Oia) | [INFERRED] IMAGE PLACEHOLDER — references `/images/destinations/santorini-oia-sunset-view.webp` |
| Existing usable images | ❌ NONE |
| Images needed | santorini.webp + santorini-oia-sunset-view.webp + 1-2 more |
| Chat assistant | [INFERRED] ABSENT |

**Santorini is the highest visual-impact destination on the site.** Both hero images will be created by the script.  
**Recommended additional filenames:** `santorini-caldera-blue-dome.webp`

**Priority:** HIGH (Santorini is a top search-intent destination)

---

## B) IMAGE TASK LIST FOR DEJAN

### Step 1 — Run the script (creates the 9 hero images)

Run `process_destination_images.py` once. This handles the minimum required set.

### Step 2 — Verify the 9 outputs

After running the script, confirm these files exist in `images/destinations/`:

- [ ] `malta.webp` — hero for malta/index.html
- [ ] `santorini.webp` — hero for greece/santorini/index.html
- [ ] `santorini-oia-sunset-view.webp` — Oia sunset view on santorini page
- [ ] `sicily.webp` — hero for italy/sicily/index.html
- [ ] `ibiza.webp` — hero for spain/ibiza/index.html
- [ ] `rome.webp` — hero for italy/rome/index.html
- [ ] `venice.webp` — hero for italy/venice/index.html
- [ ] `mallorca.webp` — hero for spain/mallorca/index.html
- [ ] `barcelona.webp` — hero for spain/barcelona/index.html

### Step 3 — Minimum images needed NOW (already in `/images/`, usable immediately)

These existing images are ALREADY in the site and can be referenced by destination pages right now:

| File | Use on |
|------|--------|
| `crystal-clear-lagoon-malta.webp` | malta/index.html — image break or card |
| `malta-blue-lagoon-boats.webp` | malta/index.html — card or second break |
| `mdina-old-city-malta.webp` | malta/index.html — image break |
| `malta-sea-cave-cliffs.webp` | malta/index.html — card |
| `malta-traditional-balconies.webp` | malta/index.html — card or section |
| `luxury-coastal-resort-malta.webp` | malta/index.html — accommodation card |
| `restaurant-terrace-sea-view-malta.webp` | malta/index.html — card |
| `taormina-amphitheatre-sicily.webp` | italy/sicily/index.html — image break |
| `sandy-beach-aerial-view.webp` | destinations/index.html — hub hero |
| `coastal-road-seaside-europe.webp` | destinations/index.html — image break |

### Step 4 — Additional images needed per destination (MINIMUM for a complete feel)

| Destination | File | Purpose | Source |
|-------------|------|---------|--------|
| **Malta** | Already covered | — | `/images/` has 6+ files |
| **Santorini** | `santorini-caldera-blue-dome.webp` | Image break | Source folder |
| **Sicily** | `sicily-cefalu-beach.webp` | Image break or card | Source folder |
| **Sicily** | `sicily-coast-aerial.webp` | Second card | Source folder |
| **Rome** | `rome-colosseum.webp` | Image break | Source folder |
| **Rome** | `rome-trevi-fountain.webp` | Second image break or card | Source folder |
| **Venice** | `venice-grand-canal.webp` | Image break | Source folder |
| **Venice** | `venice-rialto-bridge.webp` | Card | Source folder |
| **Ibiza** | `ibiza-cala-beach.webp` | Image break | Source folder |
| **Ibiza** | `ibiza-sunset-coast.webp` | Card | Source folder |
| **Mallorca** | `mallorca-alcudia-beach.webp` | Image break | Source folder |
| **Mallorca** | `mallorca-palma-cathedral.webp` | Card | Source folder |
| **Barcelona** | `barcelona-sagrada-familia.webp` | Image break | Source folder |
| **Barcelona** | `barcelona-park-guell.webp` | Card | Source folder |
| **Hub hero** | `destinations-hub-hero.webp` | Hero for destinations/index.html | Source folder OR reuse sandy-beach |
| **Italy hub** | `italy-hub-hero.webp` | Hero for italy/index.html | Reuse rome.webp or new |
| **Spain hub** | `spain-hub-hero.webp` | Hero for spain/index.html | Reuse barcelona.webp or new |
| **Greece hub** | `greece-hub-hero.webp` | Hero for greece/index.html | Reuse santorini.webp or new |

### Step 5 — Ideal images LATER (for richness and conversion)

Per destination page, the ideal set is:
- 1 hero (wide, dramatic, landscape) → **already handled by script**
- 2 image breaks (atmospheric mid-page cinematic images)
- 4 service/area cards (beach, food, stay, activity)
- 1 "stay style" image (accommodation, rooftop, pool)
- 3 related destination thumbnails

That means roughly **10–12 images per destination** for a fully rich page. For 9 destinations: ~100 images total (ideal state). For Phase 1, the 9 heroes are enough to unblock.

---

## C) AI ASSISTANT TASK LIST

### Current state (CONFIRMED)
- **global.js** contains: scroll progress bar, cookie consent, GA4, Meta Pixel
- **NO chat assistant** exists anywhere on the site
- The only contact method is a WhatsApp floating button (`wa.me/35677922436`)
- There is no inline chat, popup, or proactive assistant

### How to add the proactive assistant safely

Add it to `global.js` (loads on every page). This way you write it once and every destination page gets it automatically.

The assistant triggers after 20 seconds if the visitor has not already clicked WhatsApp.

**Safe, non-destructive addition to `global.js`:**

```javascript
// ===== PROACTIVE ASSISTANT (20-second trigger) =====

(function () {
  // Respect: only show once per session, don't nag
  if (sessionStorage.getItem('dl_assistant_shown')) return;

  // Read per-page config (destination pages set window.DL_PAGE)
  const page = window.DL_PAGE || {};
  const message = page.assistantMessage ||
    "Planning a trip? I can help with accommodation, transfers, and what to do. Just send a message.";
  const ctaLabel = page.ctaLabel || "Ask on WhatsApp";
  const ctaUrl   = page.ctaUrl   || "https://wa.me/35677922436";

  const bubble = document.createElement('div');
  bubble.id = 'dl-assistant-bubble';
  bubble.setAttribute('role', 'dialog');
  bubble.setAttribute('aria-label', 'Travel assistant');
  bubble.innerHTML = `
    <div style="
      position:fixed; bottom:100px; right:24px; z-index:500;
      max-width:300px; background:#fff; border-radius:20px;
      box-shadow:0 16px 40px rgba(15,38,51,0.16);
      border:1px solid rgba(15,38,51,0.08);
      padding:20px; font-family:Inter,-apple-system,sans-serif;
      animation: dl_slideIn 0.4s cubic-bezier(0.34,1.56,0.64,1);
    ">
      <button id="dl-assistant-close" aria-label="Dismiss" style="
        position:absolute; top:12px; right:14px;
        background:none; border:none; cursor:pointer;
        font-size:18px; color:#5a7082; line-height:1;
      ">×</button>
      <p style="
        margin:0 0 14px; font-size:0.95rem; line-height:1.55;
        color:#0f2633; font-weight:500;
      ">${message}</p>
      <a href="${ctaUrl}" target="_blank" rel="noopener noreferrer" style="
        display:block; text-align:center; padding:12px 20px;
        background:#20a965; color:#fff; border-radius:10px;
        text-decoration:none; font-weight:700; font-size:0.9rem;
      ">${ctaLabel}</a>
    </div>
    <style>
      @keyframes dl_slideIn {
        from { opacity:0; transform:translateY(16px); }
        to   { opacity:1; transform:translateY(0); }
      }
    </style>
  `;

  const timer = setTimeout(() => {
    document.body.appendChild(bubble);
    sessionStorage.setItem('dl_assistant_shown', '1');

    document.getElementById('dl-assistant-close').addEventListener('click', () => {
      bubble.remove();
    });
  }, 20000);

  // Cancel if user already taps WhatsApp within 20s
  document.addEventListener('click', (e) => {
    if (e.target.closest('a[href*="wa.me"]')) {
      clearTimeout(timer);
      sessionStorage.setItem('dl_assistant_shown', '1');
    }
  }, { once: true });
})();
```

**To configure per page**, add this block BEFORE `<script src="/assets/js/global.js">`:

```html
<script>
window.DL_PAGE = {
  assistantMessage: "Thinking about Santorini? I can help you plan the best time to visit, where to stay, and how to get there.",
  ctaLabel: "Ask about Santorini",
  ctaUrl: "https://wa.me/35677922436?text=Hi%2C+I%27m+interested+in+Santorini"
};
</script>
<script src="/assets/js/global.js"></script>
```

### Per-destination assistant configuration

| Page | Message | CTA label | CTA type |
|------|---------|-----------|----------|
| `destinations/index.html` | "Not sure where to go? Tell me your travel style and I'll suggest the best match." | Ask for a suggestion | WhatsApp |
| `malta/index.html` | "Planning Malta? I can help with where to stay, transfers, and what to do." | Ask about Malta | WhatsApp |
| `italy/index.html` | "Thinking about Italy? I can help you choose between Sicily, Rome, and Venice." | Ask about Italy | WhatsApp |
| `italy/sicily/index.html` | "Sicily is one of Europe's most underrated destinations. Want help planning your stay?" | Ask about Sicily | WhatsApp |
| `italy/rome/index.html` | "Rome can be overwhelming without a plan. I can help you make the most of it." | Ask about Rome | WhatsApp |
| `italy/venice/index.html` | "Venice is magical — but timing matters. Want help planning the right stay?" | Ask about Venice | WhatsApp |
| `spain/index.html` | "Spain has so much to offer. Let me help you choose between Ibiza, Mallorca, and Barcelona." | Ask about Spain | WhatsApp |
| `spain/ibiza/index.html` | "Ibiza is more than clubs — it has quiet beaches too. Want help finding the right part?" | Ask about Ibiza | WhatsApp |
| `spain/mallorca/index.html` | "Mallorca has the best of everything. Want help planning accommodation and transfers?" | Ask about Mallorca | WhatsApp |
| `spain/barcelona/index.html` | "Barcelona is one of Europe's best cities. Want help making the most of your time there?" | Ask about Barcelona | WhatsApp |
| `greece/index.html` | "Greece is stunning. Santorini is the dream — want help planning your stay?" | Ask about Greece | WhatsApp |
| `greece/santorini/index.html` | "Santorini is bucket-list material. Let me help you plan the perfect stay in Oia or Fira." | Ask about Santorini | WhatsApp |
| `index.html` (homepage) | "Planning a Mediterranean trip? I can help with any destination." | Start a conversation | WhatsApp |

**When to show:** 20 seconds after page load, only if visitor has not already clicked WhatsApp.  
**When to cancel:** immediately if visitor clicks any WhatsApp link.  
**Session limit:** once per browser session (sessionStorage key: `dl_assistant_shown`).  
**Primary CTA:** WhatsApp (proven to convert for this business).  
**Expedia:** Do not add Expedia links to the assistant bubble — WhatsApp is the core conversion channel.

---

## D) SCALING SYSTEM FOR 50+ DESTINATIONS

### Folder structure (recommended)

```
images/
├── destinations/           ← flat set, all destination hero images
│   ├── malta.webp
│   ├── santorini.webp
│   ├── santorini-oia-sunset-view.webp
│   ├── sicily.webp
│   ├── ibiza.webp
│   ├── rome.webp
│   ├── venice.webp
│   ├── mallorca.webp
│   ├── barcelona.webp
│   └── [new destinations follow same pattern]
├── [existing service images remain here — do not move]
│   ├── crystal-clear-lagoon-malta.webp
│   ├── modern-bedroom-luxury-apartment.webp
│   └── ...

[destination pages]
destinations/index.html       ← hub, lists all destinations
italy/index.html              ← country landing
italy/sicily/index.html       ← city/island page
italy/rome/index.html
italy/venice/index.html
spain/index.html
spain/ibiza/index.html
spain/mallorca/index.html
spain/barcelona/index.html
greece/index.html
greece/santorini/index.html
malta/index.html
[future]
croatia/index.html
croatia/dubrovnik/index.html
portugal/index.html
portugal/algarve/index.html
```

### Filename rules

| Rule | Pattern | Example |
|------|---------|---------|
| Destination hero | `{destination}.webp` | `dubrovnik.webp` |
| Destination secondary | `{destination}-{area}-{descriptor}.webp` | `dubrovnik-old-town-sunset.webp` |
| All lowercase | no capitals | `rome.webp` not `Rome.webp` |
| Hyphens only | no underscores, no spaces | `san-vito-lo-capo.webp` |
| Max width | 1600px | enforced by the processor script |
| Format | WebP only | enforced by the processor script |
| Quality | 80 | enforced by the processor script |

### Required image slots per destination page

| Slot | File pattern | Required? |
|------|-------------|----------|
| Hero background | `{destination}.webp` | ✅ Required |
| Image break 1 (mid-page) | `{destination}-{descriptor}-1.webp` | ✅ Required for a complete page |
| Image break 2 | `{destination}-{descriptor}-2.webp` | ⚪ Recommended |
| Card 1 (beach/coast/landscape) | `{destination}-beach.webp` | ⚪ Recommended |
| Card 2 (landmark/culture) | `{destination}-landmark.webp` | ⚪ Recommended |
| Card 3 (stay/hotel/villa) | `{destination}-stay.webp` | ⚪ Optional |
| Card 4 (food/restaurant) | `{destination}-food.webp` | ⚪ Optional |
| Related card thumbnail | reuse hero | — auto-reuse |

### Optional image slots

| Slot | Purpose |
|------|---------|
| `{destination}-aerial.webp` | Dramatic aerial/overview shot |
| `{destination}-sunset.webp` | Golden hour mood image |
| `{destination}-map-preview.webp` | Screengrab of interactive map |

### CSV/JSON manifest fields (for future dynamic rendering)

When scaling beyond ~20 destinations, a manifest becomes essential. Recommended structure:

**`data/destinations.json`** (future file):

```json
[
  {
    "slug": "santorini",
    "name": "Santorini",
    "country": "greece",
    "country_name": "Greece",
    "tagline": "Blue domes, caldera views, and unforgettable sunsets.",
    "hero": "/images/destinations/santorini.webp",
    "secondary": "/images/destinations/santorini-oia-sunset-view.webp",
    "page": "/greece/santorini/",
    "whatsapp_text": "Hi%2C+I%27m+interested+in+Santorini",
    "active": true,
    "phase": 1
  }
]
```

Fields:
- `slug` — matches filename prefix and page folder name
- `name` — display name
- `country` / `country_name` — for grouping and breadcrumbs
- `tagline` — one-line description for cards
- `hero` — absolute path to hero image
- `secondary` — second image (for pages with two primary shots)
- `page` — URL path for linking
- `whatsapp_text` — URL-encoded pre-filled WhatsApp message
- `active` — `true/false` (hide destinations not yet ready)
- `phase` — `1/2/3` for rollout planning

---

## E) IMPLEMENTATION PHASES

### Phase 1 — Fix current placeholders (do NOW)
**Time estimate:** 1–2 hours  
**Dependency:** process_destination_images.py must run successfully first

- [ ] Run `process_destination_images.py` on local Windows machine
- [ ] Confirm all 9 files in `images/destinations/`
- [ ] Open each destination page and verify hero `background-image` loads (no grey box)
- [ ] Open each page and verify card images load
- [ ] For pages still showing grey boxes: set `background-image` URL to correct `/images/destinations/X.webp`
- [ ] For `malta/index.html`: verify all image slots use existing `/images/*.webp` files (they're already there)
- [ ] For `italy/sicily/index.html`: add `taormina-amphitheatre-sicily.webp` to second image slot
- [ ] For `destinations/index.html`: use `sandy-beach-aerial-view.webp` as hub hero if HERO IMAGE PLACEHOLDER still showing
- [ ] Do NOT edit any service pages (accommodation, transfers, itineraries, support)
- [ ] Do NOT touch index.html Malta homepage
- [ ] Do NOT edit global.css or global.js in Phase 1

**Definition of done:** No grey boxes. Every destination page has at least a real hero image.

---

### Phase 2 — Add proactive assistant after 20 seconds (do NEXT)
**Time estimate:** 30 minutes  
**Dependency:** Phase 1 complete

- [ ] Add the assistant code block from Section C to `assets/JS/global.js`
- [ ] Add `window.DL_PAGE = { ... }` config block to each destination page before the `global.js` script tag
- [ ] Test on each page: wait 20s, confirm bubble appears
- [ ] Test dismiss button
- [ ] Test that clicking WhatsApp cancels the timer
- [ ] Test that the bubble only shows once per session
- [ ] Do NOT add Expedia or booking widgets in Phase 2

**Definition of done:** Every destination page shows a relevant, dismissible assistant bubble after 20 seconds.

---

### Phase 3 — Create reusable destination template
**Time estimate:** 3–4 hours  
**Dependency:** Phase 2 complete, visual style confirmed

- [ ] Extract common destination page structure into a documented HTML template file (`_template-destination.html`)
- [ ] Template includes all image slots with clear `<!-- HERO IMAGE -->` / `<!-- IMAGE BREAK 1 -->` comments
- [ ] Template includes `window.DL_PAGE = { ... }` config stub
- [ ] Template includes `<meta>` SEO fields as stubs
- [ ] Template includes breadcrumb: `Destinations > Country > City`
- [ ] Test template by creating one new destination page from scratch
- [ ] Document: which CSS classes handle which visual component
- [ ] Do NOT change any existing destination pages in Phase 3

**Definition of done:** Anyone can create a new destination page in under 20 minutes by copying the template.

---

### Phase 4 — Prepare 50+ destination image system
**Time estimate:** 4–8 hours (spread over weeks)  
**Dependency:** Phase 3 template proven

- [ ] Expand `process_destination_images.py` TARGETS list with new destinations as source photos are added
- [ ] Create `data/destinations.json` manifest (structure in Section D)
- [ ] For each new destination: add 1 entry to TARGETS → run script → add 1 entry to JSON
- [ ] Priority order for next destinations (suggested):
  1. Croatia — Dubrovnik, Split, Hvar
  2. Portugal — Algarve, Lisbon, Porto
  3. Montenegro — Kotor
  4. France — French Riviera, Corsica
  5. Turkey — Istanbul, Bodrum
- [ ] Add additional images (image breaks, cards) after hero is live
- [ ] Add related destination cross-links between pages
- [ ] Do NOT upload source photos to git repository (they are large binaries)

**Definition of done:** The JSON manifest drives destination cards on `destinations/index.html`, making new pages self-registering.

---

### Phase 5 — Deploy safely
**Time estimate:** 1–2 hours per deployment  
**Dependency:** Phase 4 ongoing

- [ ] Pre-deployment checklist:
  - All images optimized (max 1600px, WebP, ≤200 KB per file)
  - No `background-image: url('')` empty strings
  - No grey hero boxes on any page
  - All WhatsApp links use correct number `35677922436`
  - Assistant bubble tested across Chrome, Firefox, Safari mobile
- [ ] Upload new files to server: upload only `images/destinations/*.webp` and the changed HTML files
- [ ] Do NOT overwrite `images/` root (service images are already correct on server)
- [ ] Do NOT overwrite `assets/CSS/global.css` unless specifically changed
- [ ] Verify on live site after upload
- [ ] Check Google Analytics: destination pages should appear as new pageviews
- [ ] Do NOT touch server `xmlrpc.php`, `index.php`, or any server-side files

**Deployment priority order:**
1. Upload `images/destinations/` folder (9 images first)
2. Upload `malta/index.html` (lowest risk, images already exist)
3. Upload `destinations/index.html` (hub page)
4. Upload `italy/`, `spain/`, `greece/` in one batch
5. Upload updated `assets/JS/global.js` with assistant code last (most impact, lowest risk)

---

## SUMMARY TABLE

| Page | Hero Image | Other Images | Chat | Priority |
|------|-----------|-------------|------|---------|
| `index.html` | ✅ Real | ✅ Real | ❌ Missing | HIGH |
| `destinations/index.html` | ⚠️ Placeholder | ⚠️ 9 cards missing | ❌ Missing | HIGH |
| `malta/index.html` | ⚠️ Needs malta.webp | ✅ 6 images ready | ❌ Missing | HIGH |
| `italy/sicily/index.html` | ⚠️ Needs sicily.webp | ⚠️ 1 image ready, need 1 more | ❌ Missing | HIGH |
| `italy/rome/index.html` | ⚠️ Needs rome.webp | ❌ 0 ready | ❌ Missing | HIGH |
| `greece/santorini/index.html` | ⚠️ Needs santorini.webp | ⚠️ Need santorini-oia-sunset-view.webp | ❌ Missing | HIGH |
| `italy/venice/index.html` | ⚠️ Needs venice.webp | ❌ 0 ready | ❌ Missing | MEDIUM |
| `spain/ibiza/index.html` | ⚠️ Needs ibiza.webp | ❌ 0 ready | ❌ Missing | MEDIUM |
| `spain/mallorca/index.html` | ⚠️ Needs mallorca.webp | ❌ 0 ready | ❌ Missing | MEDIUM |
| `spain/barcelona/index.html` | ⚠️ Needs barcelona.webp | ❌ 0 ready | ❌ Missing | MEDIUM |
| `italy/index.html` | ⚠️ Placeholder | ⚠️ Cards need images | ❌ Missing | MEDIUM |
| `spain/index.html` | ⚠️ Placeholder | ⚠️ Cards need images | ❌ Missing | MEDIUM |
| `greece/index.html` | ⚠️ Placeholder | ⚠️ Cards need images | ❌ Missing | MEDIUM |

**Single most impactful action:** Run `process_destination_images.py`. It resolves the hero image problem on all 9 destination pages in one shot.

**Second most impactful action:** Add proactive assistant to `global.js`. Instant conversion improvement across every page.

---

*Report generated from server backup (April 2026) and image processor script analysis. Destination sub-pages (italy/, spain/, greece/, malta/) were not in the repository and are assessed from stated requirements and site patterns.*
