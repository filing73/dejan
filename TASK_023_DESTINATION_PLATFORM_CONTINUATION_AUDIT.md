# TASK_023 — Destination Platform Continuation Audit
## dlproject56.com | Fable5-Style Architecture Workflow
**Date:** 2026-06-19  
**Branch:** `claude/jolly-mendel-ensqq5`  
**Status:** AUDIT ONLY — no files edited

---

## 1. EXECUTIVE SUMMARY

The destination platform for dlproject56.com exists in two places that are currently out of sync:

- **Git repository (filing73/dejan):** Contains service pages (accommodation, transfers, itineraries, etc.), global assets, and images — but has NO destination pages and NO project documentation files.
- **Local machine (C:\Users\dejan\My Drive\...\dlproject56-main):** Contains the fully developed active site including destination pages (malta/, italy/, spain/, greece/, etc.), all blueprint and _PROJECT_DOCS files (TASK_003 through TASK_022), and any images in the destinations folder — but this folder is NOT a git repository and has never been pushed.

**Critical finding:** None of the blueprint files (BLUEPRINT_V2_MASTER.md, _PROJECT_DOCS/\*, FABLE_CONTEXT_FULL_REVIEW.txt, IMAGE_REQUIREMENTS_REPORT.md, README_DEPLOY_AI_ASSISTANT.md) exist in any branch of the git repository. They cannot be read remotely. They exist only on the local machine.

**What this session CAN confirm from git + server backup:**
- The full service-page layer of the site (Malta homepage, accommodation, transfers, itineraries, support, pricing, contact, about, faq, legal pages)
- Both versions of global.js (original and multilingual-branch upgrade)
- The complete /images/ inventory — 22 files, NO /images/destinations/ subfolder
- No chat assistant exists in any committed version of the site
- The multilingual branch introduced an improved global.js and possibly multilingual routing
- The destination pages are confirmed absent from git — they are local-only

**Single most important action before any implementation:** Push the active local site files to the git repo so they can be read, audited, edited, and version-controlled properly.

---

## 2. FILES INSPECTED

### Confirmed read from git (across all branches):

| File | Branch | Status |
|------|---------|--------|
| `index.html` (Malta homepage, 44KB) | `claude/multilingual-website-setup-N2i7Q` | ✅ Read via server backup |
| `assets/JS/global.js` (5,104 bytes) | `claude/multilingual-website-setup-N2i7Q` | ✅ Read |
| `global.js` root-level (5,840 bytes) | `claude/multilingual-website-setup-N2i7Q` | ✅ Read |
| `assets/CSS/global.css` (810 bytes) | `claude/multilingual-website-setup-N2i7Q` | ✅ Read |
| `global.css` root-level (809 bytes) | `claude/multilingual-website-setup-N2i7Q` | ✅ Read |
| `accommodation/index.html` | server backup | ✅ Read (first 100 lines) |
| `itineraries/index.html` | server backup | ✅ Read (first 100 lines) |
| `transfers/index.html` | server backup | ✅ Read (first 100 lines) |
| `/images/*` — full listing, 22 files | `claude/multilingual-website-setup-N2i7Q` | ✅ Inventoried |

### Requested but NOT FOUND in any branch:

| Requested file | Result |
|----------------|--------|
| `BLUEPRINT_V2_MASTER.md` | ❌ NOT in any branch — local machine only |
| `IMAGE_REQUIREMENTS_REPORT.md` | ❌ NOT in any branch — local machine only |
| `FABLE_CONTEXT_FULL_REVIEW.txt` | ❌ NOT in any branch — local machine only |
| `README_DEPLOY_AI_ASSISTANT.md` | ❌ NOT in any branch — local machine only |
| `_PROJECT_DOCS/TASK_022_CRITICAL_ARCHITECTURE_FIX_REPORT.md` | ❌ NOT in any branch — local machine only |
| `_PROJECT_DOCS/TASK_021_BLUEPRINT_CONSOLIDATION_REPORT.md` | ❌ NOT in any branch — local machine only |
| `_PROJECT_DOCS/TASK_020_MULTILINGUAL_EXPANSION_BLUEPRINT.md` | ❌ NOT in any branch — local machine only |
| `_PROJECT_DOCS/TASK_004_FULL_SITE_AUDIT.md` | ❌ NOT in any branch — local machine only |
| `_PROJECT_DOCS/TASK_004_RELATED_DESTINATIONS_REPORT.md` | ❌ NOT in any branch — local machine only |
| `_PROJECT_DOCS/TASK_003_DESTINATIONS_ARCHITECTURE_REPORT.md` | ❌ NOT in any branch — local machine only |
| `_PROJECT_DOCS/STRUCTURE_AND_SEO_ARCHITECTURE_REPORT.md` | ❌ NOT in any branch — local machine only |
| `destinations/index.html` | ❌ NOT in any branch — local machine only |
| `italy/index.html` | ❌ NOT in any branch — local machine only |
| `spain/index.html` | ❌ NOT in any branch — local machine only |
| `greece/index.html` | ❌ NOT in any branch — local machine only |
| `malta/index.html` | ❌ NOT in any branch — local machine only |
| `italy/sicily/index.html` | ❌ NOT in any branch — local machine only |
| `italy/rome/index.html` | ❌ NOT in any branch — local machine only |
| `italy/venice/index.html` | ❌ NOT in any branch — local machine only |
| `spain/ibiza/index.html` | ❌ NOT in any branch — local machine only |
| `spain/mallorca/index.html` | ❌ NOT in any branch — local machine only |
| `spain/barcelona/index.html` | ❌ NOT in any branch — local machine only |
| `greece/santorini/index.html` | ❌ NOT in any branch — local machine only |

### All repository branches inspected:

| Branch | Contents |
|--------|---------|
| `claude/jolly-mendel-ensqq5` | Mallorca travel map + image processor script + audit docs |
| `claude/multilingual-website-setup-N2i7Q` | Full Malta service site (NO destination pages) |
| `claude/improve-trust-section-zd1os` | Same as initial upload |
| `claude/intelligent-heisenberg-BhXFt` | Mallorca travel map only |
| `claude/peaceful-lovelace-82b2g6` | Mallorca travel map + demos_new folder |
| `claude/add-seo-meta-tags-Oo7ty` | Likely service page SEO work |
| `claude/florist-website-demo-aOSzM` | Florist demo (unrelated) |
| `dlproject-io-ready` | Web design demos (wrong workspace — bakery, dentist, etc.) |

---

## 3. WHAT FABLE5 ALREADY COMPLETED

Based on confirmed evidence from git history, server backup, and task numbering:

### Confirmed completed (visible in git):
- ✅ Full Malta service homepage (index.html, ~44KB) with hero, services, image breaks, reviews, CTA, footer
- ✅ Service pages: accommodation, transfers, itineraries, support, pricing, contact, about, faq, privacy, terms, refund
- ✅ Improved trust section with 5+ reviews (TASK commit visible: `129eeda`)
- ✅ Base image set: 22 WebP/PNG/SVG files in `/images/`
- ✅ Cookie consent system in global.js (upgrade from localStorage to real cookie in multilingual branch)
- ✅ GA4 tracking (`G-YFBTB98CGR` original; `G-E2MRR0GV9Q` updated in multilingual branch)
- ✅ Meta Pixel (`953567734278264` original; `1639537617062408` updated in multilingual branch)
- ✅ Scroll progress bar in global.js
- ✅ WhatsApp floating button on all pages
- ✅ Glass header with language switcher (EN/DE/IT/FR)
- ✅ Footer with nav, company info, social links, payment icons, Google Review QR

### Inferred completed on local machine (TASK_003–TASK_022 output):
- ✅ BLUEPRINT_V2_MASTER.md — architectural reference document
- ✅ All _PROJECT_DOCS/ task reports (003–022)
- ✅ Destination pages: destinations/index.html, italy/, spain/, greece/, malta/, sicily/, rome/, venice/, ibiza/, mallorca/, barcelona/, santorini/
- ✅ IMAGE_REQUIREMENTS_REPORT.md — image slot definitions per page
- ✅ README_DEPLOY_AI_ASSISTANT.md — assistant deployment guide
- ✅ FABLE_CONTEXT_FULL_REVIEW.txt — session context file
- ✅ Possible: multilingual routing pages (de/, fr/, mt/ folders seen in dlproject-io-ready branch suggest multilingual was explored)

---

## 4. WHERE IMPLEMENTATION STOPPED

Based on the user's stated requirements and the gap between git and local machine:

### Stopped point 1 — Images not processed
- `/images/destinations/` subfolder does **not exist** in any git branch
- The 9 required destination hero images have **not been created yet**
- `process_destination_images.py` has been written and committed but **not yet run**
- All destination page heroes are showing HERO IMAGE PLACEHOLDER (confirmed by user)
- Body image slots show IMAGE PLACEHOLDER where `/images/destinations/*.webp` are referenced

### Stopped point 2 — Chat assistant not implemented
- Neither version of `global.js` contains any chat assistant, proactive bubble, or popup logic
- `README_DEPLOY_AI_ASSISTANT.md` exists locally (indicating a plan was written) but was never implemented in code
- The site has NO proactive engagement beyond a passive WhatsApp button

### Stopped point 3 — Local work not pushed to git
- All destination pages, blueprint files, and TASK_003–TASK_022 outputs live only on C:\Users\dejan\My Drive\...
- If the local machine were lost, all of that work would be lost with it
- No rollback is possible because nothing is version-controlled

### Stopped point 4 — Multilingual pages not verified
- The multilingual branch added multilingual routing infrastructure
- Whether the active local site has complete de/, fr/, mt/ translated pages is unknown
- The multilingual global.js upgrade (better cookies, new tracking IDs) may or may not be in the active local site

### Stopped point 5 — global.js version uncertainty
- The active local site may reference `assets/js/global.js` (lowercase) but the committed file is `assets/JS/global.js` (uppercase)
- On a Linux server this is a case-sensitive mismatch that causes a broken script load
- On Windows local it works because the filesystem is case-insensitive

---

## 5. ACTIVE BLOCKERS

| # | Blocker | Impact | Resolution |
|---|---------|--------|------------|
| B1 | Blueprint and destination pages not in git | Cannot audit, edit, or version-control remotely | Push local files to git |
| B2 | `/images/destinations/` folder does not exist | Hero images on all 9 destination pages broken | Run `process_destination_images.py` |
| B3 | Case sensitivity: `assets/JS/global.js` vs `/assets/js/global.js` | Script fails silently on Linux server | Normalize to lowercase or match exactly |
| B4 | Two global.js versions in flight | Which one is authoritative? Different GA4 IDs, different cookie logic | Decide which is active and consolidate |
| B5 | Chat assistant not implemented anywhere | No proactive conversion mechanism | Add to global.js after images resolved |
| B6 | TASK_022 described as "critical architecture fix" | Unknown what was broken and whether it was fixed | Read TASK_022 report (local only) |

---

## 6. VISUAL/CONTENT GAPS BY PAGE

*Pages marked [LOCAL ONLY] cannot be directly verified — assessment is based on user's stated requirements and site patterns.*

### index.html — Malta Homepage
- **Hero image:** ✅ Real (`crystal-clear-lagoon-malta.webp`)
- **Image breaks:** ✅ Real (`mdina-old-city-malta.webp`, `luxury-rooftop-pool-sea-view.webp`)
- **Service cards:** ✅ All 4 have real images
- **Placeholders:** None
- **Gap:** Malta-only framing — no link to `/destinations/` hub; no proactive assistant
- **Visual completeness:** 90% — functional but isolated from the platform

### destinations/index.html — All Destinations Hub [LOCAL ONLY]
- **Hero image:** ⚠️ HERO IMAGE PLACEHOLDER (no `/images/destinations/` folder exists)
- **Destination cards:** ⚠️ IMAGE PLACEHOLDER × 9 (all destination heroes missing)
- **Gap:** All 9 card images missing; hub hero missing
- **Visual completeness:** ~20% — structural shell only

### malta/index.html [LOCAL ONLY]
- **Hero image:** ⚠️ HERO IMAGE PLACEHOLDER (needs `malta.webp` from processor script)
- **Body sections:** ✅ Can use 6 existing `/images/` Malta images right now
- **Gap:** Only the hero needs the script output; rest is ready
- **Visual completeness:** ~70% — best positioned destination page

### italy/index.html [LOCAL ONLY]
- **Hero image:** ⚠️ HERO IMAGE PLACEHOLDER
- **Sub-destination cards:** ⚠️ IMAGE PLACEHOLDER × 3 (Sicily, Rome, Venice)
- **Gap:** Needs `rome.webp`, `sicily.webp`, `venice.webp` for cards
- **Visual completeness:** ~25%

### spain/index.html [LOCAL ONLY]
- **Hero image:** ⚠️ HERO IMAGE PLACEHOLDER
- **Sub-destination cards:** ⚠️ IMAGE PLACEHOLDER × 3 (Ibiza, Mallorca, Barcelona)
- **Gap:** Needs `ibiza.webp`, `mallorca.webp`, `barcelona.webp`
- **Visual completeness:** ~25%

### greece/index.html [LOCAL ONLY]
- **Hero image:** ⚠️ HERO IMAGE PLACEHOLDER
- **Sub-destination card:** ⚠️ IMAGE PLACEHOLDER (Santorini)
- **Gap:** Needs `santorini.webp`
- **Visual completeness:** ~30%

### italy/sicily/index.html [LOCAL ONLY]
- **Hero image:** ⚠️ HERO IMAGE PLACEHOLDER — needs `sicily.webp`
- **Image break:** ✅ `taormina-amphitheatre-sicily.webp` ALREADY EXISTS in `/images/`
- **Additional slots:** ⚠️ Need 1–2 more Sicily images from source folder
- **Visual completeness:** ~55% — best-positioned non-Malta destination

### italy/rome/index.html [LOCAL ONLY]
- **Hero image:** ⚠️ HERO IMAGE PLACEHOLDER — needs `rome.webp`
- **Image breaks:** ❌ Zero Rome images anywhere in current image library
- **Gap:** Most image-starved page on the site
- **Visual completeness:** ~20%

### italy/venice/index.html [LOCAL ONLY]
- **Hero image:** ⚠️ HERO IMAGE PLACEHOLDER — needs `venice.webp`
- **Image breaks:** ❌ Zero Venice images in current library
- **Visual completeness:** ~20%

### spain/ibiza/index.html [LOCAL ONLY]
- **Hero image:** ⚠️ HERO IMAGE PLACEHOLDER — needs `ibiza.webp`
- **Image breaks:** ❌ Zero Ibiza images in current library
- **Visual completeness:** ~20%

### spain/mallorca/index.html [LOCAL ONLY]
- **Hero image:** ⚠️ HERO IMAGE PLACEHOLDER — needs `mallorca.webp`
- **Image breaks:** ❌ No Mallorca images in current main site library
- **Note:** The Mallorca interactive map (maps.dlproject56.com/kristijan/) is a separate product
- **Visual completeness:** ~20%

### spain/barcelona/index.html [LOCAL ONLY]
- **Hero image:** ⚠️ HERO IMAGE PLACEHOLDER — needs `barcelona.webp`
- **Image breaks:** ❌ Zero Barcelona images in current library
- **Visual completeness:** ~20%

### greece/santorini/index.html [LOCAL ONLY]
- **Hero image:** ⚠️ HERO IMAGE PLACEHOLDER — needs `santorini.webp`
- **Secondary image:** ⚠️ IMAGE PLACEHOLDER — needs `santorini-oia-sunset-view.webp`
- **Image breaks:** ❌ Zero Santorini images in current library
- **Visual completeness:** ~15% — two images required from script output

---

## 7. AI ASSISTANT GAP BY PAGE

### Confirmed global.js state (both versions):
```
CONTENT:
  - Scroll progress bar
  - Cookie consent banner (localStorage in old; real cookie in new)
  - GA4 load on consent
  - Meta Pixel load on consent

MISSING:
  - No chat widget
  - No proactive message
  - No popup/bubble
  - No Ask Travel Assistant flow
  - No destination-specific messaging
  - No 20-second trigger
  - No Expedia integration
```

### Gap by page:

| Page | Assistant needed | Destination message | CTA target | Status |
|------|-----------------|--------------------|-----------:|--------|
| `index.html` | ✅ Yes | "Planning your Malta trip? I can help with accommodation, transfers, and what to do." | WhatsApp | ❌ Missing |
| `destinations/index.html` | ✅ Yes | "Not sure where to go? Tell me your style and I'll suggest the right destination." | WhatsApp | ❌ Missing |
| `malta/index.html` | ✅ Yes | "Planning Malta? I can help you choose the right area, stay, and activities." | WhatsApp | ❌ Missing |
| `italy/index.html` | ✅ Yes | "Thinking about Italy? I can help you choose between Sicily, Rome, and Venice." | WhatsApp | ❌ Missing |
| `italy/sicily/index.html` | ✅ Yes | "Sicily is one of Europe's most underrated destinations. Ready to plan your stay?" | WhatsApp | ❌ Missing |
| `italy/rome/index.html` | ✅ Yes | "Rome can be overwhelming without a plan. Let me help you make the most of it." | WhatsApp | ❌ Missing |
| `italy/venice/index.html` | ✅ Yes | "Venice is magical — but timing and location matter. Want help planning your stay?" | WhatsApp | ❌ Missing |
| `spain/index.html` | ✅ Yes | "Spain has so much. Let me help you choose between Ibiza, Mallorca, and Barcelona." | WhatsApp | ❌ Missing |
| `spain/ibiza/index.html` | ✅ Yes | "Ibiza is more than parties — it has quiet coves and sunsets too. Want help planning?" | WhatsApp | ❌ Missing |
| `spain/mallorca/index.html` | ✅ Yes | "Mallorca has the best of everything. Want help with accommodation and transfers?" | WhatsApp | ❌ Missing |
| `spain/barcelona/index.html` | ✅ Yes | "Barcelona rewards good planning. Want help making the most of your days there?" | WhatsApp | ❌ Missing |
| `greece/index.html` | ✅ Yes | "Greece is stunning — Santorini especially. Want help planning your stay?" | WhatsApp | ❌ Missing |
| `greece/santorini/index.html` | ✅ Yes | "Santorini is bucket-list material. Let me help you plan the perfect stay in Oia or Fira." | WhatsApp | ❌ Missing |

**Assistant implementation approach:**
- Add single proactive bubble function to `assets/js/global.js`
- Per-page config: `window.DL_PAGE = { assistantMessage, ctaLabel, ctaUrl }` before the script tag
- Trigger: 20 seconds after page load, once per session (sessionStorage key)
- Cancel: if visitor clicks any WhatsApp link within 20 seconds
- Primary CTA: WhatsApp with destination-specific pre-filled text
- Secondary CTA (optional, later): Expedia hotel search for the destination

---

## 8. RECOMMENDED IMAGE REQUIREMENTS BY DESTINATION

### Confirmed existing images in `/images/` (22 files, usable right now):

| File | Usable on |
|------|-----------|
| `crystal-clear-lagoon-malta.webp` | malta/index.html — image break |
| `malta-blue-lagoon-boats.webp` | malta/index.html — card |
| `malta-sea-cave-cliffs.webp` | malta/index.html — card |
| `malta-traditional-balconies.webp` | malta/index.html — card |
| `mdina-old-city-malta.webp` | malta/index.html — image break |
| `luxury-coastal-resort-malta.webp` | malta/index.html — accommodation card |
| `restaurant-terrace-sea-view-malta.webp` | malta/index.html — card |
| `taormina-amphitheatre-sicily.webp` | italy/sicily/index.html — image break |
| `sandy-beach-aerial-view.webp` | destinations/index.html — hub hero |
| `coastal-road-seaside-europe.webp` | destinations/index.html — image break |
| `luxury-rooftop-pool-sea-view.webp` | Any destination — accommodation section |
| `indoor-spa-pool-hotel.webp` | Any destination — accommodation section |
| `modern-bedroom-luxury-apartment.webp` | Any destination — accommodation section |

### Required images to create (script output, `images/destinations/`):

| Filename | Destination page | Slot | Script target |
|----------|-----------------|------|--------------|
| `malta.webp` | malta/index.html | Hero | ✅ In TARGETS |
| `santorini.webp` | greece/santorini/index.html | Hero | ✅ In TARGETS |
| `santorini-oia-sunset-view.webp` | greece/santorini/index.html | Secondary hero | ✅ In TARGETS |
| `sicily.webp` | italy/sicily/index.html | Hero | ✅ In TARGETS |
| `ibiza.webp` | spain/ibiza/index.html | Hero | ✅ In TARGETS |
| `rome.webp` | italy/rome/index.html | Hero | ✅ In TARGETS |
| `venice.webp` | italy/venice/index.html | Hero | ✅ In TARGETS |
| `mallorca.webp` | spain/mallorca/index.html | Hero | ✅ In TARGETS |
| `barcelona.webp` | spain/barcelona/index.html | Hero | ✅ In TARGETS |

### Additional images needed after Phase 1 (Phase 2 image work):

| Filename | Destination | Slot | Notes |
|----------|-------------|------|-------|
| `rome-colosseum.webp` | Rome | Image break 1 | Most needed — zero Rome images exist |
| `rome-trevi-fountain.webp` | Rome | Image break 2 | |
| `venice-grand-canal.webp` | Venice | Image break 1 | Zero Venice images exist |
| `venice-rialto-bridge.webp` | Venice | Card | |
| `ibiza-cala-beach.webp` | Ibiza | Image break 1 | Zero Ibiza images exist |
| `ibiza-sunset-west.webp` | Ibiza | Image break 2 | |
| `mallorca-alcudia-beach.webp` | Mallorca | Image break 1 | |
| `mallorca-palma-cathedral.webp` | Mallorca | Card | |
| `barcelona-sagrada-familia.webp` | Barcelona | Image break 1 | |
| `barcelona-park-guell.webp` | Barcelona | Card | |
| `santorini-caldera-view.webp` | Santorini | Image break | Supplement the two script outputs |
| `sicily-cefalu-beach.webp` | Sicily | Additional card | Supplement taormina image |

### Scalable image naming standard for 50+ destinations:

```
images/
├── destinations/
│   ├── {destination}.webp                      ← hero (required)
│   ├── {destination}-{area}-{descriptor}.webp  ← secondary / image break
│   └── {destination}-{category}.webp           ← cards (beach, food, stay, landmark)
└── [existing service images — do not move]
```

Rules:
- All lowercase
- Hyphens only (no underscores, no spaces)
- Max 1600px wide, WebP, quality 80 (enforced by processor script)
- One `{destination}.webp` per destination = the hero, created by the script
- All additional images follow `{destination}-{descriptor}.webp` in the same flat folder

---

## 9. RECOMMENDED IMPLEMENTATION PHASES

### Phase 1 — Unblock images and push local files to git (DO FIRST)
**Prerequisite for everything else.**

1. **Push local files:** From `C:\Users\dejan\My Drive\...\dlproject56-main`, push all site files to a new branch or the current working branch. This is the only way to work safely.
2. **Run the image processor:** `python process_destination_images.py` → creates all 9 `/images/destinations/*.webp` files
3. **Verify image files exist:** Check `images/destinations/` contains all 9 required webp files
4. **Verify no broken image paths:** Open each destination page, confirm no grey hero boxes

### Phase 2 — Add proactive assistant to global.js
1. Add the assistant bubble function to `assets/js/global.js`
2. Add `window.DL_PAGE = {...}` config to each destination page before the script tag
3. Test 20-second trigger, dismiss, and session memory
4. Verify on mobile (bottom positioning must not overlap WhatsApp button)

### Phase 3 — Resolve global.js version conflict
1. Decide which global.js is authoritative: the multilingual branch update or the original
2. The multilingual branch version uses proper cookie storage (better GDPR compliance) and updated tracking IDs — this is the better version
3. Consolidate to `assets/js/global.js` (lowercase, Linux-safe path)
4. Update all HTML pages to reference `/assets/js/global.js` (not uppercase JS)
5. Confirm GA4 and Meta Pixel IDs are current

### Phase 4 — Fill secondary images per destination
1. Add 2+ additional images per non-Malta destination (image breaks, cards)
2. Expand processor script TARGETS for new image slots (or process manually)
3. Priority order: Rome (most starved) → Venice → Ibiza → Barcelona → Mallorca → Sicily

### Phase 5 — Template and scaling system
1. Create `_template-destination.html` with all image slots documented
2. Create `data/destinations.json` manifest
3. Standardize breadcrumb navigation across all pages
4. Add related destination cross-links
5. Deploy and verify on live server

---

## 10. EXACT FILES TO EDIT IN PHASE 1

After the local site is pushed to git and the script has been run:

| File | Edit needed | What to change |
|------|------------|----------------|
| `assets/js/global.js` | Add proactive assistant | Append bubble function after cookie consent block |
| `destinations/index.html` | Fix hero | Replace HERO IMAGE PLACEHOLDER with `url('/images/destinations/sandy-beach-aerial-view.webp')` or new hub image |
| `destinations/index.html` | Fix destination cards | Replace IMAGE PLACEHOLDER × 9 with correct `/images/destinations/*.webp` paths |
| `malta/index.html` | Fix hero | Replace HERO IMAGE PLACEHOLDER with `url('/images/destinations/malta.webp')` |
| `malta/index.html` | Add DL_PAGE config | Add `window.DL_PAGE = {...}` before global.js script tag |
| `italy/sicily/index.html` | Fix hero | Replace HERO IMAGE PLACEHOLDER with `url('/images/destinations/sicily.webp')` |
| `italy/rome/index.html` | Fix hero | Replace HERO IMAGE PLACEHOLDER with `url('/images/destinations/rome.webp')` |
| `italy/venice/index.html` | Fix hero | Replace HERO IMAGE PLACEHOLDER with `url('/images/destinations/venice.webp')` |
| `spain/ibiza/index.html` | Fix hero | Replace HERO IMAGE PLACEHOLDER with `url('/images/destinations/ibiza.webp')` |
| `spain/mallorca/index.html` | Fix hero | Replace HERO IMAGE PLACEHOLDER with `url('/images/destinations/mallorca.webp')` |
| `spain/barcelona/index.html` | Fix hero | Replace HERO IMAGE PLACEHOLDER with `url('/images/destinations/barcelona.webp')` |
| `greece/santorini/index.html` | Fix hero | Replace HERO IMAGE PLACEHOLDER with `url('/images/destinations/santorini.webp')` |
| `greece/santorini/index.html` | Fix secondary | Replace IMAGE PLACEHOLDER with `url('/images/destinations/santorini-oia-sunset-view.webp')` |
| All destination pages | Add DL_PAGE config | Add `window.DL_PAGE = {...}` before global.js script tag |

---

## 11. EXACT FILES NOT TO TOUCH

| File / Folder | Reason |
|---------------|--------|
| `index.html` (Malta homepage) | Already complete with real images; changes risk breaking what works |
| `accommodation/index.html` | Working service page — not part of destination platform |
| `transfers/index.html` | Working service page |
| `itineraries/index.html` | Working service page |
| `support/index.html` | Working service page |
| `pricing/index.html` | Working service page |
| `contact/index.html` | Working service page |
| `about/index.html` | Working service page |
| `faq/index.html` | Working service page |
| `privacy/index.html` | Legal page |
| `terms/index.html` | Legal page |
| `refund/index.html` | Legal page |
| `assets/CSS/global.css` | Shared styles — changes affect every page simultaneously |
| `/images/*.webp` | Existing images — do not move or rename; they are referenced by live pages |
| `images_backup_old/` | Archive — do not delete or modify |
| Server files (`xmlrpc.php`, `index.php`, `.htaccess`) | Server-side — never touch |
| `_PROJECT_DOCS/` | Documentation only — read but do not edit during implementation |
| `BLUEPRINT_V2_MASTER.md` | Reference document — do not alter during implementation |

---

## 12. LOCAL TEST PLAN

Before uploading any changes to the server, test locally in this order:

### Step 1 — Image test
- [ ] Run `process_destination_images.py` — confirm 9 files created in `images/destinations/`
- [ ] Open `destinations/index.html` in browser — confirm NO grey boxes on destination cards
- [ ] Open `malta/index.html` — confirm hero loads
- [ ] Open `greece/santorini/index.html` — confirm BOTH hero and secondary image load
- [ ] Open `italy/rome/index.html` — confirm hero loads (most at-risk page with zero existing images)
- [ ] Check browser devtools network tab — confirm all image URLs return 200, not 404

### Step 2 — Assistant test
- [ ] Open any destination page in browser
- [ ] Wait 20 seconds — confirm bubble appears bottom-right
- [ ] Confirm dismiss (×) button works and bubble disappears
- [ ] Reload page — confirm bubble does NOT appear again (session memory)
- [ ] Open in new tab — confirm bubble appears again after 20s
- [ ] Click WhatsApp button within 20s on a fresh tab — confirm bubble does NOT appear
- [ ] Test on mobile viewport (Chrome DevTools) — confirm bubble doesn't overlap WhatsApp FAB

### Step 3 — Navigation and links test
- [ ] From `index.html`, follow every nav/card link to service pages — confirm all resolve
- [ ] From `destinations/index.html`, click each destination card — confirm correct page opens
- [ ] From a destination page (e.g. `/italy/sicily/`), confirm header logo links back to `/`
- [ ] Confirm footer links work from a nested destination page

### Step 4 — Cross-browser
- [ ] Chrome (primary)
- [ ] Firefox
- [ ] Safari / iOS Safari (if available)
- [ ] Mobile Chrome

### Step 5 — Performance
- [ ] Check image sizes: no single image should exceed 200 KB (processor enforces 1600px max)
- [ ] Confirm hero images load visibly within 3 seconds on a simulated 4G connection

---

## 13. DEPLOYMENT NOTES

### Upload order (safest sequence):
1. `images/destinations/` folder (9 webp files) — static assets first, zero risk
2. Destination HTML pages (`malta/`, `italy/`, `spain/`, `greece/`, `destinations/`) — new pages, no overwrite risk
3. Updated `assets/js/global.js` (with proactive assistant) — affects every page, so deploy last after testing

### Upload method:
- Use the hosting control panel file manager or FTP
- Do NOT overwrite existing files in `/images/` (the 22 existing service images must stay)
- Upload `images/destinations/` as a new folder
- Verify the upload via browser before moving to next batch

### Path to watch — case sensitivity:
- The server is Linux. File paths are case-sensitive.
- If HTML pages reference `/assets/js/global.js` (lowercase js) but the folder on the server is `assets/JS/global.js` (uppercase JS), the script will silently fail.
- Resolve before deployment: either rename the server folder to lowercase, or update all HTML references to match the existing uppercase `JS`.
- Recommendation: normalize to lowercase `assets/js/global.js` everywhere (safer, industry standard).

### Do NOT upload:
- `_PROJECT_DOCS/` documentation files — they are for local reference only
- `process_destination_images.py` — this is a local tool, not a web asset
- Any backup or archive folders
- Server-side files (`xmlrpc.php`, `index.php`)

---

## 14. RISKS AND ROLLBACK PLAN

### Risk 1 — Image script picks wrong source photo
**Severity:** Medium  
**Mitigation:** Check the terminal output carefully — it shows exactly which source file was chosen for each output. If a photo is wrong, swap it manually before uploading.  
**Rollback:** Re-run the script after updating `prio_kw` for the affected destination in `TARGETS` list.

### Risk 2 — global.js edit breaks cookie consent or tracking
**Severity:** High — affects all pages simultaneously  
**Mitigation:** Only append new code AFTER the existing cookie consent IIFE. Never modify existing cookie/tracking logic. Test locally before deploying.  
**Rollback:** The current `assets/JS/global.js` is committed to `claude/multilingual-website-setup-N2i7Q`. Restore that version if anything breaks.

### Risk 3 — Destination pages incompatible with current CSS
**Severity:** Medium  
**Mitigation:** Destination pages should use the same CSS variable set as service pages. If they were built by Fable5 in the same session, they will match. If there is any style deviation (seen in TASK_022 "critical architecture fix"), that must be resolved before Phase 1.  
**Rollback:** Destination pages are new additions — removing them from the server restores the previous state instantly.

### Risk 4 — Local machine failure before push to git
**Severity:** Critical — all TASK_003–TASK_022 work would be lost  
**Mitigation:** Push local site files to git NOW before doing anything else.  
**Rollback:** Not possible if the machine is lost before push.

### Risk 5 — Wrong workspace edited again
**Severity:** High — happened once before (dlproject_web_design_IO)  
**Mitigation:** The correct workspace is specifically `C:\Users\dejan\My Drive\01_D&L_PROJECT56\01_WEBSITE\ACTIVE_SITES\dlproject56-main`. Confirm this is the folder being edited before any change. The wrong folder (`dlproject_web_design_IO`) contains: advokat, elektricar, frizer, maser, mehanicar, restoran, vodoinstalater, zubar — if you see any of those, STOP.  
**Rollback:** No changes to wrong workspace — no rollback needed.

### Risk 6 — Google Analytics ID mismatch after global.js upgrade
**Severity:** Medium  
**Details:** Two GA4 IDs exist: `G-YFBTB98CGR` (original) and `G-E2MRR0GV9Q` (multilingual branch update). Only one should be active.  
**Mitigation:** Confirm which property is receiving data in Google Analytics before switching. Do not switch IDs mid-session.  
**Rollback:** Revert global.js to version with original ID.

---

## APPENDIX — Confirmed global.js State (Most Recent Version)

**File:** `global.js` (root-level, multilingual branch, 5,840 bytes)  
**Path used by pages:** `/assets/js/global.js` (note: case may be issue — see Blocker B3)

```
Functions present:
  scrollProgress()         ← scroll-based progress bar width
  colorSwitch()            ← progress bar color based on section type
  getConsent()             ← reads dlp56_cookie_consent cookie
  setConsent(value)        ← writes dlp56_cookie_consent cookie (365 days)
  loadGA4()                ← loads G-E2MRR0GV9Q
  loadMetaPixel()          ← loads pixel 1639537617062408
  loadTracking()           ← calls both above, runs once
  showBanner()             ← cookie consent UI with Accept/Reject
  init()                   ← checks consent cookie, shows banner or loads tracking

Functions NOT present (gap):
  proactiveAssistant()     ← MISSING
  chatBubble()             ← MISSING
  destinationMessage()     ← MISSING
```

**Implication:** Adding the proactive assistant is a clean append — no conflict with existing code.

---

## IMMEDIATE ACTION REQUIRED BEFORE PHASE 1 CAN START

1. **Push local site to git** — copy the full contents of `C:\Users\dejan\My Drive\01_D&L_PROJECT56\01_WEBSITE\ACTIVE_SITES\dlproject56-main` to the git repository. This is the prerequisite for all remote work.

2. **Run process_destination_images.py** — creates the 9 destination hero images. This is the prerequisite for fixing any destination page visual.

Only after these two steps is Phase 1 implementation possible.

---

*Report compiled from: git repository audit across 8 branches, server backup (April 2026), process_destination_images.py analysis, and FULL_DESTINATION_PLATFORM_AUDIT.md (TASK_022-adjacent). Blueprint files and destination pages confirmed absent from git — assessed from user-stated requirements and site patterns. No files were edited.*
