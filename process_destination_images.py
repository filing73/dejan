#!/usr/bin/env python3
"""
dlproject56.com — Flat Destination Image Processor

Selects the best source image for each required destination,
backs up any existing output files, converts to WebP, and
writes a flat image set + report.

Requirements:
    pip install Pillow

Usage:
    python process_destination_images.py
"""

import os
import sys
import shutil
import unicodedata
import re
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is not installed.  Run:  pip install Pillow")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════════════════════════════════════

SOURCE_DIR = Path(r"H:\DL_AI_WORK\02_ACTIVE_PROJECTS\DLPROJECT56\Duplicat za rodju")
WORKSPACE  = Path(r"C:\Users\dejan\My Drive\01_D&L_PROJECT56\01_WEBSITE\ACTIVE_SITES\dlproject56-main")
OUTPUT_DIR = WORKSPACE / "images" / "destinations"

WEBP_QUALITY = 80
MAX_WIDTH    = 1600
IMAGE_EXTS   = {".jpg", ".jpeg", ".png", ".webp"}

# ═══════════════════════════════════════════════════════════════════════════════
# TARGET DEFINITIONS
#
# path_kw   — at least one must appear somewhere in the source file's path
#             (slugified: lowercase, accents stripped, non-ascii removed)
# prio_kw   — score +10 per match in the filename stem; used to prefer
#             the most representative shot when multiple candidates exist
# exclude   — list of output filenames whose chosen source must not be reused
#             (prevents santorini.webp and santorini-oia-sunset-view.webp
#             pointing to the same source file)
# ═══════════════════════════════════════════════════════════════════════════════

TARGETS = [
    {
        "output":  "malta.webp",
        "path_kw": ["malta"],
        "prio_kw": ["blue", "lagoon", "valletta", "coast", "sea", "cliff",
                    "harbour", "harbor", "mdina", "comino"],
        "exclude": [],
    },
    {
        "output":  "santorini.webp",
        "path_kw": ["santorini"],
        "prio_kw": ["caldera", "white", "oia", "fira", "dome", "blue", "building", "village"],
        "exclude": [],
    },
    {
        "output":  "santorini-oia-sunset-view.webp",
        "path_kw": ["santorini"],
        "prio_kw": ["oia", "sunset", "view", "caldera", "evening", "dusk", "golden"],
        "exclude": ["santorini.webp"],   # must differ from the santorini hero
    },
    {
        "output":  "sicily.webp",
        "path_kw": ["sicily", "sicilia", "taormina", "cefalu", "cefal",
                    "mondello", "palermo", "sanvito", "san-vito", "san_vito",
                    "siracusa", "agrigento"],
        "prio_kw": ["taormina", "cefalu", "sanvito", "coast", "sea", "beach",
                    "greek", "temple", "theatre", "theater"],
        "exclude": [],
    },
    {
        "output":  "ibiza.webp",
        "path_kw": ["ibiza"],
        "prio_kw": ["beach", "coast", "cala", "bay", "sea", "sunset", "water"],
        "exclude": [],
    },
    {
        "output":  "rome.webp",
        "path_kw": ["rome", "roma"],
        "prio_kw": ["colosseum", "coliseum", "forum", "vatican", "trevi",
                    "pantheon", "piazza", "navona", "landmark"],
        "exclude": [],
    },
    {
        "output":  "venice.webp",
        "path_kw": ["venice", "venezia"],
        "prio_kw": ["canal", "gondola", "rialto", "grand", "bridge",
                    "san marco", "sanmarco", "lagoon"],
        "exclude": [],
    },
    {
        "output":  "mallorca.webp",
        "path_kw": ["mallorca", "majorca"],
        "prio_kw": ["beach", "coast", "cala", "bay", "sea", "water", "cliff"],
        "exclude": [],
    },
    {
        "output":  "barcelona.webp",
        "path_kw": ["barcelona"],
        "prio_kw": ["sagrada", "familia", "gaudi", "park", "guell",
                    "gothic", "city", "barceloneta", "rambla"],
        "exclude": [],
    },
]

REQUIRED_OUTPUTS = [t["output"] for t in TARGETS]

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def slug(text: str) -> str:
    """Lowercase, strip accents, keep only a-z0-9 and spaces/hyphens."""
    text = unicodedata.normalize("NFKD", str(text))
    text = text.encode("ascii", "ignore").decode("ascii")
    return text.lower()


def path_slug(p: Path) -> str:
    """All parts of a path joined and slugified — used for keyword matching."""
    return " ".join(slug(part) for part in p.parts)


def score(img_path: Path, path_kw: list, prio_kw: list) -> tuple:
    """
    Return (matches: bool, keyword_score: int, file_size: int).
    A candidate must match at least one path_kw to be eligible.
    """
    full = path_slug(img_path)
    if not any(kw in full for kw in path_kw):
        return False, 0, 0
    name = slug(img_path.stem)
    kw_score = sum(10 for kw in prio_kw if kw in name)
    return True, kw_score, img_path.stat().st_size


def collect_images(source_dir: Path) -> list:
    """Recursively collect all image files from source_dir."""
    found = []
    for root, dirs, files in os.walk(source_dir):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for fname in sorted(files):
            if Path(fname).suffix.lower() in IMAGE_EXTS:
                found.append(Path(root) / fname)
    return found


def convert(src: Path, dst: Path) -> tuple:
    """
    Open src, resize to MAX_WIDTH (preserving ratio), strip metadata,
    save as WebP at WEBP_QUALITY. Returns (width, height, orig_kb, out_kb).
    """
    orig_kb = src.stat().st_size // 1024
    img = Image.open(src)

    # Normalise colour mode
    if img.mode == "P":
        img = img.convert("RGBA")
    if img.mode == "RGBA":
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg.convert("RGB")
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # Resize if needed
    if img.width > MAX_WIDTH:
        new_h = int(img.height * MAX_WIDTH / img.width)
        img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)

    w, h = img.size
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "WEBP", quality=WEBP_QUALITY, method=6)
    out_kb = dst.stat().st_size // 1024
    return w, h, orig_kb, out_kb


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT WRITER
# ═══════════════════════════════════════════════════════════════════════════════

def write_report(path: Path, results: list, backup_dir, ts: str):
    created    = [r for r in results if r["status"] == "OK" and not r["overwritten"]]
    overwritten = [r for r in results if r["status"] == "OK" and r["overwritten"]]
    missing    = [r for r in results if r["status"] == "MISSING"]
    failed     = [r for r in results if r["status"] not in ("OK", "MISSING")]

    lines = [
        "# dlproject56.com — Destination Image Flat Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Required output files | {len(REQUIRED_OUTPUTS)} |",
        f"| Files created (new) | {len(created)} |",
        f"| Files overwritten | {len(overwritten)} |",
        f"| Backups created | {len(overwritten)} |",
        f"| Missing source categories | {len(missing)} |",
        f"| Failed | {len(failed)} |",
        f"| HTML/CSS/JS edited | No |",
        f"| Server files touched | No |",
        f"| Source images deleted | No |",
        "",
        "---",
        "",
        "## Files Created or Updated",
        "",
        "| Output file | Source image used | Original size | Final size | Dimensions | Status |",
        "|-------------|-------------------|---------------|------------|------------|--------|",
    ]

    for r in results:
        if r["status"] == "OK":
            verb = "overwritten" if r["overwritten"] else "new"
            lines.append(
                f"| `{r['output']}` | `{r['source']}` "
                f"| {r['orig_kb']} KB | {r['out_kb']} KB "
                f"| {r['width']}×{r['height']} | {verb} |"
            )
        elif r["status"] == "MISSING":
            lines.append(
                f"| `{r['output']}` | *(no source found)* | — | — | — | MISSING |"
            )
        else:
            lines.append(
                f"| `{r['output']}` | `{r.get('source','')}` | — | — | — | FAILED |"
            )

    lines += ["", "---", "", "## Backups", ""]
    if backup_dir:
        lines.append(f"Backup folder: `{backup_dir}`")
        lines.append("")
        lines.append("| Backed-up file |")
        lines.append("|----------------|")
        for r in overwritten:
            lines.append(f"| `{r['output']}` |")
    else:
        lines.append("*(no existing files were present — no backup needed)*")

    lines += ["", "---", "", "## Missing Source Categories", ""]
    if missing:
        for r in missing:
            lines.append(f"- `{r['output']}` — no matching source images found")
    else:
        lines.append("*(none — all destinations had source images)*")

    lines += ["", "---", "", "## Failed Files", ""]
    if failed:
        for r in failed:
            lines.append(f"- `{r['output']}`: {r['status']}")
    else:
        lines.append("*(none)*")

    lines += [
        "",
        "---",
        "",
        "## Confirmation",
        "",
        "- HTML files: **not edited**",
        "- CSS files: **not edited**",
        "- JS files: **not edited**",
        "- Server files: **not touched**",
        "- Source images: **not deleted or modified**",
        "",
    ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print()
    print("=" * 66)
    print("  dlproject56.com — Flat Destination Image Processor")
    print("=" * 66)
    print(f"  Source    : {SOURCE_DIR}")
    print(f"  Output    : {OUTPUT_DIR}")
    print(f"  Started   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # ── Validate paths ────────────────────────────────────────────────────────
    if not SOURCE_DIR.exists():
        print(f"ERROR: Source folder not found:\n  {SOURCE_DIR}")
        sys.exit(1)
    if not WORKSPACE.exists():
        print(f"ERROR: Workspace not found:\n  {WORKSPACE}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ── Backup existing output files ──────────────────────────────────────────
    existing = [OUTPUT_DIR / name for name in REQUIRED_OUTPUTS
                if (OUTPUT_DIR / name).exists()]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = None
    if existing:
        backup_dir = OUTPUT_DIR / f"_backup_{ts}"
        backup_dir.mkdir()
        for f in existing:
            shutil.copy2(f, backup_dir / f.name)
        print(f"  Backed up {len(existing)} existing file(s) →  {backup_dir.name}/")
        for f in existing:
            print(f"    {f.name}")
        print()

    # ── Scan source ───────────────────────────────────────────────────────────
    print("Scanning source images …")
    all_images = collect_images(SOURCE_DIR)
    print(f"  {len(all_images)} image file(s) found.\n")

    if not all_images:
        print("ERROR: No source images found. Check SOURCE_DIR path.")
        sys.exit(1)

    # ── Process each target ───────────────────────────────────────────────────
    used_sources: dict[str, Path] = {}   # output_name → chosen source Path
    results = []

    for tgt in TARGETS:
        out_name = tgt["output"]
        excluded = {used_sources[k] for k in tgt["exclude"] if k in used_sources}

        candidates = []
        for img in all_images:
            if img in excluded:
                continue
            ok, kw_score, fsize = score(img, tgt["path_kw"], tgt["prio_kw"])
            if ok:
                candidates.append((kw_score, fsize, img))

        if not candidates:
            print(f"  [MISSING] {out_name}")
            results.append({"output": out_name, "status": "MISSING", "source": None,
                            "orig_kb": None, "out_kb": None, "width": None,
                            "height": None, "overwritten": False})
            continue

        # Highest keyword score wins; largest file breaks ties
        candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
        best = candidates[0][2]
        was_over = (OUTPUT_DIR / out_name).exists()

        try:
            w, h, orig_kb, out_kb = convert(best, OUTPUT_DIR / out_name)
        except Exception as e:
            print(f"  [FAIL]    {out_name}: {e}")
            results.append({"output": out_name, "status": str(e),
                            "source": str(best.relative_to(SOURCE_DIR)),
                            "orig_kb": None, "out_kb": None,
                            "width": None, "height": None, "overwritten": was_over})
            continue

        used_sources[out_name] = best
        rel_src = str(best.relative_to(SOURCE_DIR))
        verb = "overwritten" if was_over else "new      "
        print(f"  [OK] {out_name:<42} [{verb}]")
        print(f"       {orig_kb:>5} KB → {out_kb:>5} KB   {w}×{h}")
        print(f"       ← {rel_src}")
        results.append({"output": out_name, "status": "OK", "source": rel_src,
                        "orig_kb": orig_kb, "out_kb": out_kb,
                        "width": w, "height": h, "overwritten": was_over})

    # ── Write report ──────────────────────────────────────────────────────────
    print()
    report_path = WORKSPACE / "destination-image-flat-report.md"
    write_report(report_path, results, backup_dir, ts)
    print(f"  Written: destination-image-flat-report.md")

    # ── Final directory listing ───────────────────────────────────────────────
    print()
    print("Final contents of images/destinations/:")
    webp_files = sorted(f for f in OUTPUT_DIR.iterdir()
                        if f.is_file() and f.suffix == ".webp")
    for f in webp_files:
        marker = " ✓" if f.name in REQUIRED_OUTPUTS else "  "
        print(f"  {marker} {f.name:<48} {f.stat().st_size // 1024:>5} KB")

    # ── Required file confirmation ────────────────────────────────────────────
    print()
    print("Required file check:")
    all_present = True
    for name in REQUIRED_OUTPUTS:
        present = (OUTPUT_DIR / name).exists()
        mark = "OK" if present else "MISSING"
        print(f"  [{mark}] {name}")
        if not present:
            all_present = False

    ok_count = sum(1 for r in results if r["status"] == "OK")
    missing  = [r["output"] for r in results if r["status"] == "MISSING"]
    print()
    print("=" * 66)
    print(f"  Processed  : {ok_count} / {len(TARGETS)}")
    if missing:
        print(f"  MISSING    : {', '.join(missing)}")
    if backup_dir:
        print(f"  Backup     : {backup_dir}")
    print(f"  Report     : {report_path}")
    print("=" * 66)
    print()


if __name__ == "__main__":
    main()
