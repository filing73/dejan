# TASK_024 — BRANCH PREP AND DRY-RUN REPORT

**Date:** 2026-06-19
**Status:** REPORT ONLY — no website files copied, no content edited, no deployment
**Task ref:** TASK_024_LOCAL_SOURCE_TO_GIT_SYNC_PLAN.md (Option B)

---

## 1. BRANCH STATUS SUMMARY

| Field | Value |
|---|---|
| Branch before this task | `claude/jolly-mendel-ensqq5` (maps/POI app branch) |
| Base branch used | `claude/multilingual-website-setup-N2i7Q` |
| New branch created | `fable5/travel-local-source-import-TASK024` |
| Branch pushed to remote | Yes — `origin/fable5/travel-local-source-import-TASK024` |
| New branch tracks | `origin/claude/multilingual-website-setup-N2i7Q` (remote tracking set at creation) |
| Files on new branch | 44 tracked files (website content, no maps app) |

The `fable5/` prefix is preserved. Future implementation work for the destination platform should continue on this branch or branches cut from it.

---

## 2. ROOT INDEX.HTML VERIFICATION — HARD STOP RESULT

**PASSED — branch is safe to receive the website sync.**

All four hard-stop strings were checked against the branch root `index.html`:

| Check string | Found? | Result |
|---|---|---|
| `Alcudia` | Not found | PASS |
| `POI map` | Not found | PASS |
| `maps.dlproject56.com/kristijan` | Not found | PASS |
| `Leaflet` (Leaflet-only map app) | Not found | PASS |

**Confirmed content of root `index.html`:**
- Title: `Malta Travel Planning & Local Assistance | D&L Project56`
- Description: `Plan your Malta stay with practical help — accommodation, transfers, itineraries, and direct travel assistance.`
- Hero: `crystal-clear-lagoon-malta.webp`
- This is the Malta travel service homepage. The maps app is on a different branch and is not at risk.

---

## 3. DRY-RUN SIMULATION — EXPECTED SYNC RESULTS

> **Note on this dry-run:** The remote environment cannot execute robocopy or rsync against the local Windows path `C:\Users\dejan\My Drive\...`. The dry-run below is a structural simulation based on the approved sync list (TASK_024, Section 2) crossed against the actual current branch tree. It precisely reflects what `robocopy /L` or `rsync --dry-run` would report in each category.
>
> **Before executing the real sync:** run `robocopy /L` (Section 5.1 of TASK_024 plan) on Windows first and compare its output against Section 3.2 below.

### 3.1 Files/folders ALREADY on branch — would be UPDATED (not added fresh)

These exist on the branch from the base `claude/multilingual-website-setup-N2i7Q`. If the local source versions are newer or different, sync will overwrite them. **Dejan must decide whether local source is authoritative over these** (recommended: yes, local source is the working copy).

| Path | On branch now | Sync action |
|---|---|---|
| `index.html` | YES — Malta homepage (44 KB) | OVERWRITE with local version |
| `about/index.html` | YES | OVERWRITE with local version |
| `accommodation/index.html` | YES | OVERWRITE with local version |
| `contact/index.html` | YES | OVERWRITE with local version |
| `faq/index.html` | YES | OVERWRITE with local version |
| `itineraries/index.html` | YES | OVERWRITE with local version |
| `pricing/index.html` | YES | OVERWRITE with local version |
| `privacy/index.html` | YES | OVERWRITE with local version |
| `refund/index.html` | YES | OVERWRITE with local version |
| `support/index.html` | YES | OVERWRITE with local version |
| `terms/index.html` | YES | OVERWRITE with local version |
| `transfers/index.html` | YES | OVERWRITE with local version |
| `assets/CSS/global.css` | YES — 810 bytes | OVERWRITE with local version |
| `assets/JS/global.js` | YES — 5,104 bytes | OVERWRITE with local version |

> ⚠️ **Overwrite risk on `assets/JS/global.js`:** The branch currently holds 5,104 bytes. The root-level `global.js` (newer version, 5,840 bytes, with real cookie consent) is also on this branch as a loose file. If the local source has a third version, the sync will overwrite the branch copy. See Section 5, Risk RF1.

### 3.2 Files/folders MISSING from branch — would be ADDED fresh (new to git)

These are the core destination-platform assets that don't exist in any git branch. After sync, they will be visible and editable remotely.

| Path | Expected content | Status |
|---|---|---|
| `destinations/` | All destination pages (HTML files, at least 13 pages) | NEW |
| `italy/` | Country hub — may include inline AI chat widget | NEW |
| `spain/` | Country hub | NEW |
| `greece/` | Country hub | NEW |
| `malta/` | Country hub or destination sub-section | NEW |
| `images/destinations/` | 9 webp files from `process_destination_images.py` | NEW |
| `images/destinations/malta.webp` | 1600px max, WebP quality 80 | NEW |
| `images/destinations/santorini.webp` | | NEW |
| `images/destinations/santorini-oia-sunset-view.webp` | | NEW |
| `images/destinations/sicily.webp` | | NEW |
| `images/destinations/ibiza.webp` | | NEW |
| `images/destinations/rome.webp` | | NEW |
| `images/destinations/venice.webp` | | NEW |
| `images/destinations/mallorca.webp` | | NEW |
| `images/destinations/barcelona.webp` | | NEW |
| `de/` | German localized site copy | NEW (if exists locally) |
| `fr/` | French localized site copy | NEW (if exists locally) |
| `it/` | Italian localized site copy | NEW (if exists locally) |
| `_PROJECT_DOCS/` | TASK_003 through TASK_022 outputs | NEW |
| `BLUEPRINT_V2_MASTER.md` | Full architecture blueprint | NEW |
| `IMAGE_REQUIREMENTS_REPORT.md` | Image spec doc | NEW |
| `sitemap.xml` | If present in local source | NEW (if exists locally) |
| `robots.txt` | If present in local source | NEW (if exists locally) |

### 3.3 Files/folders EXCLUDED from sync (must never appear in `git status`)

| Pattern | Reason | gitignore covers it? |
|---|---|---|
| `backups/` | Backup churn | NO — needs adding (Section 4.1) |
| `_local_archive/` | Archive | NO — needs adding |
| `_ARCHIVE_BACKUPS/` | Archive | NO — needs adding |
| `images_backup_old/` | Old image backup | YES — already in `.gitignore` |
| `_backup_YYYYMMDD_HHMMSS/` | Script backup output | NO — needs adding (`_backup_*/`) |
| `*.rar` | Compressed archives | NO — needs adding |
| `*.zip` | Compressed archives | `archive.zip` is individually listed, not a pattern |
| Raw image source folders | Photo dumps | NO — needs adding (see Section 4.1) |
| `images/*` (non-destinations) | Service images already on branch | NO — whitelist needed (see Section 4.1) |
| `Thumbs.db`, `desktop.ini`, `.DS_Store` | OS cruft | NO — needs adding |
| `*.gdoc`, `*.gsheet`, `~$*` | Google Drive stubs | NO — needs adding |
| Server backup mirror (`web/dlproject56.com/`) | Server snapshot | `web_extracted/` listed; full pattern may differ |

---

## 4. .GITIGNORE STATUS ON NEW BRANCH

### 4.1 Current `.gitignore` — what's already covered

```
archive.zip           ← individual file, not a pattern
images_backup_old/    ← covered
web_extracted/        ← server backup variant covered
web_dlproject_io/     ← wrong-workspace variant covered
```

### 4.2 Gaps — additions needed BEFORE first `git add` on this branch

The following block must be appended to `.gitignore` before the sync is staged. Do not `git add` any website files until this is in place and `git status` has been spot-checked.

```gitignore
# ── Backups & archives (TASK_024 additions) ─────────
backups/
_local_archive/
_ARCHIVE_BACKUPS/
_backup_*/

# ── Additional archive patterns ──────────────────────
*.rar
*.zip

# ── Raw / unprocessed image source folders ───────────
Duplicat za rodju/
raw_images/
**/RAW/

# ── images/ whitelist: only destinations subfolder ───
images/*
!images/destinations/
!images/destinations/**

# ── OS / Google Drive / editor cruft ─────────────────
Thumbs.db
desktop.ini
.DS_Store
*.gdoc
*.gsheet
*.gslides
~$*
```

> **Important:** The `images/*` + `!images/destinations/` pattern prevents the 26 existing service images (Malta webps, SVG payment icons, social PNGs) from being accidentally added again via the sync, while allowing the new `images/destinations/` subfolder through. The existing service images are already tracked — the exclude just prevents re-adding them via mass `git add`.

---

## 5. RISKS FOUND ON THIS BRANCH

| ID | Risk | Severity | Detail |
|---|---|---|---|
| **RF1** | Two `global.js` files on branch with different versions | High | `assets/JS/global.js` = 5,104 bytes (older, localStorage cookies, GA4: G-YFBTB98CGR); root `global.js` = 5,840 bytes (newer, real cookies, GA4: G-E2MRR0GV9Q). Both tracked. Sync may bring a third version from local source. Must be resolved in Phase 3 — do NOT resolve during this sync. |
| **RF2** | `assets/` path is uppercase `assets/JS/` but `index.html` links to lowercase `/assets/js/` | Medium | `index.html` line 39: `href="/assets/css/global.css"` (lowercase). File on disk: `assets/CSS/global.css` (uppercase). Works on Windows, fails silently on Linux server. Do NOT rename during sync — record actual casing from local source and address in a dedicated fix commit. |
| **RF3** | `assets/index.html` is an unexpected file in `assets/` | Low | Present on branch — likely a development stub or mistake. Confirm it's safe before sync overwrites (or not). |
| **RF4** | Country hub pages (italy/spain/greece/malta) already have inline AI chat widget | Medium | Per user correction (TASK_023_AUDIT_CORRECTION). Once synced, these pages are visible remotely. Phase 2 proactive assistant must NOT add a second chat UI over the existing one. Audit hub pages immediately after sync. |
| **RF5** | `de/`, `fr/`, `it/` folder existence unconfirmed | Low | hreflang links exist in homepage; folders may or may not be in the local source. Confirm during local checklist before running robocopy for these. |
| **RF6** | Sync will overwrite 12 service pages with local versions | Low-Medium | The branch versions were committed from server backup. Local versions may be more advanced OR may have diverged. Diff-check the critical pages (at minimum `index.html` and `accommodation/index.html`) before committing the sync. |

---

## 6. FINAL RECOMMENDATION

### Branch preparation: COMPLETE
The branch `fable5/travel-local-source-import-TASK024` exists, is website-verified (not maps app), and is pushed to remote. No maps app content is at risk.

### Ready for real sync after these two actions:
1. **Append `.gitignore` additions** (Section 4.2) to the `.gitignore` on this branch first. Commit the `.gitignore` update alone (no website files yet).
2. **Run the robocopy `/L` dry run on Windows** (TASK_024 Section 5.1) and review its output for any unexpected file in the list before removing `/L` and executing.

### After real sync and `git add`:
- `git status` check: confirm only approved paths appear, no backup folders, no raw images, no Google Drive stubs
- Spot-check that `images/destinations/` shows all 9 webp files
- Spot-check that `images/` service files are NOT re-staged (should already be tracked)
- Commit website files with message: `Sync TASK_024: import destination pages and local source`
- Push
- Notify Claude Code to begin Phase 1 HTML edits

### What comes next (Phase 1, after sync is committed):
Replace hero image placeholders on destination pages with real webp paths. Country hub AI chat audit. No global.js changes until Phase 2.

---

*TASK_024_BRANCH_PREP_AND_DRY_RUN_REPORT.md — 2026-06-19*
*Branch created, verified, pushed. No website files copied. No content edited. No server touched.*
