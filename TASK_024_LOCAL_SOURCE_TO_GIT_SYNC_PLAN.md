# TASK_024 — LOCAL SOURCE → GIT SYNC PLAN

**Date:** 2026-06-19
**Status:** PLAN ONLY — do not execute
**Branch:** claude/jolly-mendel-ensqq5
**Purpose:** Bring the active local Google Drive website source into the git repo so Claude Code can read and edit destination pages remotely.

> **This is NOT deployment.** No server is touched. No upload to `public_html`. No file is copied or edited as part of this document. This is a written plan to be reviewed and approved before any action.

---

## 0. CRITICAL CONTEXT — READ FIRST

### 0.1 The local source is not a git repo
`C:\Users\dejan\My Drive\01_D&L_PROJECT56\01_WEBSITE\ACTIVE_SITES\dlproject56-main` is a plain folder on Google Drive. It is **not** under version control. Nothing in it has ever been pushed. This is why Claude Code cannot read the destination pages.

### 0.2 The current git branch does NOT contain the website
The branch you are on right now — `claude/jolly-mendel-ensqq5` — contains at its root:

| File | What it actually is |
|---|---|
| `index.html` | The **maps/POI app** for `maps.dlproject56.com/kristijan/` (Alcudia POI map), NOT the website homepage |
| `data/poi.json` | POI data for that maps app |
| `README_UPLOAD.txt` | Upload instructions for the maps app |
| `archive.zip` | Server backup snapshot |
| `process_destination_images.py` | The image processor |
| `FULL_DESTINATION_PLATFORM_AUDIT.md`, `TASK_023*.md` | Audit reports |

**The website (Malta service site) lives on OTHER branches**, e.g. `claude/multilingual-website-setup-N2i7Q`, which has `index.html` (website homepage), `about/`, `accommodation/`, `assets/`, etc. — but still **no destination pages and no `/images/destinations/`**.

### 0.3 Decision required before sync (BLOCKER)
Because the current branch root is the maps app, dropping the full website into this branch root would **mix two unrelated projects** in one place. You must decide the sync target. See **Section 9 — Target Branch Decision** before executing anything. Do not run the sync until this is resolved.

---

## 1. WHAT EXISTS IN LOCAL ACTIVE SOURCE BUT NOT IN GIT

Based on prior audits (TASK_023, FULL_DESTINATION_PLATFORM_AUDIT) and the user's confirmations. The local folder cannot be inspected remotely, so this is the **expected** inventory to be confirmed during the pre-sync checklist (Section 8).

### 1.1 Completely absent from every git branch
| Path | Notes |
|---|---|
| `destinations/` | Destination platform pages — the whole reason for this sync |
| `italy/` | Country hub (per user, may contain inline AI chat widget) |
| `spain/` | Country hub |
| `greece/` | Country hub |
| `malta/` | Country hub / destination |
| `images/destinations/` | Now contains 9 webp files created by `process_destination_images.py` |
| `BLUEPRINT_V2_MASTER.md` | Architecture blueprint — local-only |
| `IMAGE_REQUIREMENTS_REPORT.md` | Image spec — local-only |
| `_PROJECT_DOCS/` | TASK_003–TASK_022 outputs — local-only |
| `sitemap.xml` | If present locally |
| `robots.txt` | If present locally |

### 1.2 Present in some branches but NOT in current working branch
| Path | Present in branch |
|---|---|
| `about/`, `accommodation/`, `contact/`, `faq/`, `itineraries/`, `pricing/`, `privacy/`, `refund/`, `support/`, `terms/`, `transfers/` | `claude/multilingual-website-setup-N2i7Q` |
| `assets/` | `claude/multilingual-website-setup-N2i7Q` |
| `de/`, `fr/`, `it/` | Referenced by hreflang in that branch's homepage; folder presence to confirm during checklist |
| Website `index.html` | `claude/multilingual-website-setup-N2i7Q` (root `index.html` on current branch is the maps app, not this) |

---

## 2. WHAT SHOULD BE COPIED INTO GIT (APPROVED SYNC LIST)

Exactly the list you specified. Nothing added, nothing removed.

```
index.html
assets/
images/destinations/
destinations/
italy/
spain/
greece/
malta/
about/
accommodation/
contact/
faq/
itineraries/
pricing/
privacy/
refund/
support/
terms/
transfers/
de/
fr/
it/
sitemap.xml
robots.txt
BLUEPRINT_V2_MASTER.md
IMAGE_REQUIREMENTS_REPORT.md
_PROJECT_DOCS/
```

### 2.1 Notes per item
| Item | Note |
|---|---|
| `index.html` | This is the **website** homepage from local source. ⚠️ It will collide with the maps app `index.html` currently at this branch root — see Section 6 (Risk R1) and Section 9. |
| `images/destinations/` | Only the `destinations/` subfolder of images is in scope. Do NOT pull all of `images/` — unrelated service images and `images_backup_old/` must stay out. |
| `_PROJECT_DOCS/` | Documentation only. Safe to version. |
| `de/ fr/ it/` | Localized site copies. Confirm they exist locally before including (checklist 8.x). |

---

## 3. WHAT MUST NOT BE COPIED (HARD EXCLUDE)

| Pattern / folder | Reason |
|---|---|
| `backups/` | Local backup churn, not source |
| `_local_archive/` | Archive, not source |
| `_ARCHIVE_BACKUPS/` | Archive, not source |
| `images_backup_old/` | Old image backup — confirmed present in server snapshot; must never enter git |
| `_backup_YYYYMMDD_HHMMSS/` | Created by `process_destination_images.py` before overwriting — exclude |
| `*.rar` | Compressed archives |
| `*.zip` | Compressed archives (incl. any `archive.zip`) |
| Raw image source folders | e.g. `Duplicat za rodju` and any unprocessed photo dump — huge, not web assets |
| Any server backup folder | e.g. anything mirroring `web/dlproject56.com/public_html` |
| `images/` (except `images/destinations/`) | Unrelated service images out of scope for this sync |
| Temporary processing reports | The `_REPORT.md` / run logs emitted by the image script, unless explicitly approved |
| OS / sync cruft | `Thumbs.db`, `desktop.ini`, `.DS_Store`, Google Drive `*.gdoc/.gsheet` stubs, `~$*` lock files |
| `node_modules/`, `.cache/`, build temp | If any exist |

---

## 4. PROPOSED .gitignore ADDITIONS

There is currently **no `.gitignore`** in the working directory of this branch. Create one. (Note: `claude/multilingual-website-setup-N2i7Q` has a `.gitignore`; reconcile if syncing there.)

```gitignore
# ── Backups & archives ──────────────────────────────
backups/
_local_archive/
_ARCHIVE_BACKUPS/
images_backup_old/
_backup_*/
*.rar
*.zip

# ── Raw / unprocessed image sources ─────────────────
Duplicat za rodju/
raw_images/
**/RAW/

# ── Server backup mirrors ───────────────────────────
web/dlproject56.com/public_html/
public_html/

# ── Out-of-scope image trees (keep only destinations) ─
images/*
!images/destinations/
!images/destinations/**

# ── Temp processing reports ─────────────────────────
*_RUN_LOG.md
image_processing_report*.md

# ── OS / Drive / editor cruft ───────────────────────
Thumbs.db
desktop.ini
.DS_Store
*.gdoc
*.gsheet
*.gslides
~$*
```

> The `images/*` + `!images/destinations/` whitelist pattern keeps every other image folder out while allowing only the destination webp set in. Verify behaviour with `git status` before the first add (checklist 8.x).

---

## 5. EXACT COMMAND PLAN (WINDOWS) — DO NOT RUN YET

Two equivalent options. **robocopy** is recommended on Windows because it handles long Google Drive paths and gives a clean mirror with explicit excludes. A **per-folder copy** alternative is given for users who prefer no mirror semantics.

### 5.0 Variables (set once in the terminal)
```bat
set "SRC=C:\Users\dejan\My Drive\01_D&L_PROJECT56\01_WEBSITE\ACTIVE_SITES\dlproject56-main"
set "DST=C:\path\to\your\git\checkout"   :: the local clone of filing73/dejan on the sync target branch
```
> Replace `DST` with wherever you have the git repo checked out locally on the **chosen target branch** (Section 9). `SRC` and `DST` must be different folders.

### 5.1 OPTION A — robocopy per approved folder (RECOMMENDED)

Each command copies ONE approved tree. `/E` includes subfolders, `/XD`/`/XF` exclude. `/L` = **list-only dry run** (no files written). Run the dry run first, review, then remove `/L`.

```bat
:: Shared exclude switches
set "XD=/XD backups _local_archive _ARCHIVE_BACKUPS images_backup_old"
set "XF=/XF *.rar *.zip Thumbs.db desktop.ini .DS_Store ~$* *.gdoc *.gsheet"

:: ── DRY RUN (note the /L) — copies NOTHING, just lists ──
robocopy "%SRC%\assets"             "%DST%\assets"             /E %XD% %XF% /L
robocopy "%SRC%\images\destinations" "%DST%\images\destinations" /E %XF% /L
robocopy "%SRC%\destinations"       "%DST%\destinations"       /E %XD% %XF% /L
robocopy "%SRC%\italy"              "%DST%\italy"              /E %XD% %XF% /L
robocopy "%SRC%\spain"              "%DST%\spain"              /E %XD% %XF% /L
robocopy "%SRC%\greece"            "%DST%\greece"            /E %XD% %XF% /L
robocopy "%SRC%\malta"             "%DST%\malta"             /E %XD% %XF% /L
robocopy "%SRC%\about"             "%DST%\about"             /E %XD% %XF% /L
robocopy "%SRC%\accommodation"     "%DST%\accommodation"     /E %XD% %XF% /L
robocopy "%SRC%\contact"           "%DST%\contact"           /E %XD% %XF% /L
robocopy "%SRC%\faq"               "%DST%\faq"               /E %XD% %XF% /L
robocopy "%SRC%\itineraries"       "%DST%\itineraries"       /E %XD% %XF% /L
robocopy "%SRC%\pricing"           "%DST%\pricing"           /E %XD% %XF% /L
robocopy "%SRC%\privacy"           "%DST%\privacy"           /E %XD% %XF% /L
robocopy "%SRC%\refund"            "%DST%\refund"            /E %XD% %XF% /L
robocopy "%SRC%\support"           "%DST%\support"           /E %XD% %XF% /L
robocopy "%SRC%\terms"             "%DST%\terms"             /E %XD% %XF% /L
robocopy "%SRC%\transfers"         "%DST%\transfers"         /E %XD% %XF% /L
robocopy "%SRC%\de"                "%DST%\de"                /E %XD% %XF% /L
robocopy "%SRC%\fr"                "%DST%\fr"                /E %XD% %XF% /L
robocopy "%SRC%\it"                "%DST%\it"                /E %XD% %XF% /L

:: ── Single files (copy /-Y prompts before overwrite) ──
copy "%SRC%\index.html"                 "%DST%\index.html"
copy "%SRC%\sitemap.xml"                "%DST%\sitemap.xml"
copy "%SRC%\robots.txt"                 "%DST%\robots.txt"
copy "%SRC%\BLUEPRINT_V2_MASTER.md"     "%DST%\BLUEPRINT_V2_MASTER.md"
copy "%SRC%\IMAGE_REQUIREMENTS_REPORT.md" "%DST%\IMAGE_REQUIREMENTS_REPORT.md"

:: ── _PROJECT_DOCS folder ──
robocopy "%SRC%\_PROJECT_DOCS"     "%DST%\_PROJECT_DOCS"     /E %XF% /L
```

**To execute for real:** remove every `/L`. Re-run. robocopy exit codes 0–7 are success (≥8 is an error).

> ⚠️ `index.html` line above will overwrite the maps app `index.html` if `DST` is this branch's checkout. Do NOT run that single line until Section 9 is resolved.

### 5.2 OPTION B — git Bash / rsync (if available on the machine)
```bash
SRC="/c/Users/dejan/My Drive/01_D&L_PROJECT56/01_WEBSITE/ACTIVE_SITES/dlproject56-main"
DST="/c/path/to/your/git/checkout"

rsync -av --dry-run \
  --exclude 'backups/' --exclude '_local_archive/' \
  --exclude '_ARCHIVE_BACKUPS/' --exclude 'images_backup_old/' \
  --exclude '_backup_*/' --exclude '*.zip' --exclude '*.rar' \
  --exclude 'Thumbs.db' --exclude 'desktop.ini' --exclude '.DS_Store' \
  --include 'images/' --include 'images/destinations/***' --exclude 'images/*' \
  --relative \
  "$SRC/./assets" "$SRC/./destinations" "$SRC/./italy" "$SRC/./spain" \
  "$SRC/./greece" "$SRC/./malta" "$SRC/./about" "$SRC/./accommodation" \
  "$SRC/./contact" "$SRC/./faq" "$SRC/./itineraries" "$SRC/./pricing" \
  "$SRC/./privacy" "$SRC/./refund" "$SRC/./support" "$SRC/./terms" \
  "$SRC/./transfers" "$SRC/./de" "$SRC/./fr" "$SRC/./it" \
  "$SRC/./images/destinations" "$SRC/./_PROJECT_DOCS" \
  "$SRC/./index.html" "$SRC/./sitemap.xml" "$SRC/./robots.txt" \
  "$SRC/./BLUEPRINT_V2_MASTER.md" "$SRC/./IMAGE_REQUIREMENTS_REPORT.md" \
  "$DST/"
```
`--dry-run` prints what would change. Remove it to execute.

### 5.3 After copy — stage and review (still local, no push)
```bash
cd "$DST"
git status            # review every new/changed path
git add -A
git status            # confirm NOTHING from the exclude list got staged
# Do NOT commit or push until checklist Section 8 is fully green
```

---

## 6. RISK ASSESSMENT

| ID | Risk | Severity | Likelihood | Mitigation |
|---|---|---|---|---|
| **R1** | `index.html` from website overwrites the maps-app `index.html` at this branch root | **High** | High if synced to this branch | Resolve target branch (Section 9). Use a website branch, not the maps branch. Diff before overwrite. |
| **R2** | Whole `images/` tree pulled in (service images, `images_backup_old/`) bloating repo | High | Medium | `.gitignore` whitelist `images/*` + `!images/destinations/`; verify with `git status` before `add` |
| **R3** | Raw photo source / archives committed (hundreds of MB) | High | Medium | `*.zip`,`*.rar`, raw-folder excludes; inspect `git status` byte counts |
| **R4** | Google Drive placeholder stubs (`.gdoc`, partial-sync files) copied | Medium | Medium | Ensure Drive files are fully downloaded (green check, not cloud icon) before sync; `.gitignore` stub extensions |
| **R5** | Country-hub pages with inline AI chat widget get versioned then accidentally edited in Phase 2 (duplicate chat) | Medium | Medium | Sync is read-only intake; chat-widget audit happens AFTER sync, BEFORE any edit (TASK_023 correction) |
| **R6** | Case-sensitivity drift: `assets/JS` vs `assets/js` enters git as-is and breaks on Linux server later | Medium | Medium | Note for Phase 1; do not rename during sync — record actual casing in checklist 8.x |
| **R7** | Mixing maps app + website + docs in one branch root creates a confusing tree | Medium | High | Section 9 decision; consider dedicated branch |
| **R8** | Wrong source folder (the `dlproject_web_design_IO` look-alike with advokat/frizer/zubar) synced by mistake | **High** | Low | Checklist 8.1 hard stop — verify folder contents before SRC is trusted |
| **R9** | Large binary images make repo heavy / slow clones | Low | High | Acceptable for webp (already compressed); only `images/destinations/` in scope keeps it small |

---

## 7. ROLLBACK PLAN

Because the sync only writes into a **local git checkout** and we do **not** push until the checklist is green, rollback is cheap at every stage.

### 7.1 Before `git add` (files copied, not staged)
```bash
git status                 # see what landed
git clean -nd              # DRY: list untracked files that would be removed
git clean -fd              # remove copied untracked files/folders
git checkout -- index.html # restore any overwritten tracked file (e.g. maps index.html)
```

### 7.2 After `git add`, before commit
```bash
git restore --staged .     # unstage everything
git clean -fd              # then remove untracked as above
```

### 7.3 After a LOCAL commit, before push
```bash
git reset --hard HEAD~1    # drop the sync commit entirely
# (the remote is untouched because nothing was pushed)
```

### 7.4 Safety net regardless of stage
- The **Google Drive source is never modified** by this plan (copy is one-directional SRC→DST). The authoritative website always survives in Google Drive.
- Take a manual Drive copy of `dlproject56-main` before starting if extra assurance is wanted (out of scope but recommended).
- **Nothing touches the live server / `public_html`** at any point.

---

## 8. PRE-EXECUTION CONFIRMATION CHECKLIST

Do not run any copy command until every box is checked.

### 8.1 Source verification (hard stops)
- [ ] `SRC` points to `...\ACTIVE_SITES\dlproject56-main` (the travel site), NOT `dlproject_web_design_IO`
- [ ] `SRC` does **NOT** contain `advokat/`, `elektricar/`, `frizer/`, `maser/`, `mehanicar/`, `restoran/`, `vodoinstalater/`, `zubar/` — if any appear, **STOP**, wrong folder
- [ ] `SRC` **does** contain `destinations/` and `images/destinations/` with 9 webp files
- [ ] Google Drive shows all target files fully downloaded (green check, not cloud-only)

### 8.2 Target verification
- [ ] Target branch decided (Section 9) and checked out in `DST`
- [ ] `DST` is a clean working tree (`git status` clean) before sync
- [ ] `DST` is a different folder from `SRC`

### 8.3 Exclusion verification
- [ ] `.gitignore` (Section 4) is in place in `DST` **before** first `git add`
- [ ] Dry run (`/L` or `--dry-run`) reviewed — no `backups/`, `_ARCHIVE_BACKUPS/`, `images_backup_old/`, `*.zip`, `*.rar`, raw image folders, or server-backup mirror listed
- [ ] `images/` whitelist confirmed: only `images/destinations/**` would be staged

### 8.4 Collision verification
- [ ] Decided what happens to maps-app `index.html` vs website `index.html` (R1)
- [ ] Casing of `assets/JS` vs `assets/js` recorded (R6) — no rename during sync

### 8.5 Post-stage verification (before commit)
- [ ] `git status` shows only approved paths from Section 2
- [ ] Repo size sanity-checked (no unexpected hundreds-of-MB additions)
- [ ] No `.gdoc/.gsheet/.DS_Store/Thumbs.db/~$*` staged

### 8.6 Sign-off
- [ ] Dejan approves the staged set
- [ ] Commit locally
- [ ] Push only after approval

---

## 9. TARGET BRANCH DECISION (MUST RESOLVE BEFORE EXECUTION)

The website source needs a home. Three options — pick one before running anything:

| Option | What it means | Pros | Cons |
|---|---|---|---|
| **A. Sync into a website branch** (e.g. base off `claude/multilingual-website-setup-N2i7Q`) | Website lives with its existing siblings (`about/`, `assets/`, …) | No collision with maps app; coherent website tree | Need to branch/checkout that branch locally |
| **B. New dedicated branch** (e.g. `website-source-import`) off the website branch | Clean import isolated for review | Easiest to review and roll back; no mixing | One more branch to manage |
| **C. Sync into current branch** `claude/jolly-mendel-ensqq5` | Everything in one place | None meaningful | **Collides** maps app + website `index.html` (R1); mixes unrelated projects (R7). Not recommended. |

**Recommendation:** **Option B** — a dedicated import branch cut from the website branch. It keeps the maps app, the audit docs, and the website cleanly separable, and gives the simplest rollback (`git reset --hard` / delete branch).

> This decision is the single remaining blocker. Once chosen, fill `DST`, run the dry run, work the checklist, then execute.

---

## 10. WHAT THIS PLAN DELIBERATELY DOES NOT DO

- Does **not** copy any file (plan only)
- Does **not** edit any HTML/CSS/JS
- Does **not** push to remote
- Does **not** touch the live server or `public_html`
- Does **not** delete anything from Google Drive
- Does **not** resolve the two `global.js` versions or GA4 IDs (that is Phase 3)
- Does **not** replace hero/card placeholders (that is Phase 1, after sync)

---

*TASK_024_LOCAL_SOURCE_TO_GIT_SYNC_PLAN.md — created 2026-06-19. Plan only. Await approval and Section 9 decision before any copy.*
