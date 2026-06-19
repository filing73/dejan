#!/usr/bin/env python3
"""
dlproject56.com — Destination Image Processor
Run this script locally on Windows to prepare source photos for production.

Requirements:
    pip install Pillow

Usage:
    python process_destination_images.py

Output:
    - images/destinations/<country>/<area>/*.webp
    - image-map.csv
    - image-map.json
    - processing-report.md
"""

import os
import sys
import json
import csv
import hashlib
import unicodedata
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ── Verify Pillow ─────────────────────────────────────────────────────────────
try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is not installed.")
    print("       Run:  pip install Pillow")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION — edit paths if needed
# ═══════════════════════════════════════════════════════════════════════════════

SOURCE_DIR  = Path(r"C:\Users\dejan\Desktop\Duplicat za rodju")
WORKSPACE   = Path(r"C:\Users\dejan\My Drive\01_D&L_PROJECT56\01_WEBSITE\ACTIVE_SITES\dlproject56-main")
OUTPUT_DIR  = WORKSPACE / "images" / "destinations"

WEBP_QUALITY   = 80
MAX_WIDTH      = 1600
IMAGE_EXTS     = {".jpg", ".jpeg", ".png", ".webp"}

# ═══════════════════════════════════════════════════════════════════════════════
# FOLDER NAME MAPPINGS
# ═══════════════════════════════════════════════════════════════════════════════

# Source top-level folder → canonical country slug
COUNTRY_MAP = {
    "01_malta":  "malta",
    "02_grece":  "greece",
    "02_greece": "greece",
    "03_italy":  "italy",
    "04_spain":  "spain",
}

# Source sub-folder names → canonical output slug
AREA_MAP = {
    # Greece
    "santorini": "santorini",

    # Italy — destinations
    "sicily":    "sicily",
    "sicilia":   "sicily",
    "rome":      "rome",
    "roma":      "rome",
    "venice":    "venice",
    "venezia":   "venice",

    # Sicily — areas
    "agrigento":        "agrigento",
    "cefalù":           "cefalu",
    "cefalu":           "cefalu",
    "cefalú":           "cefalu",
    "cefalù":      "cefalu",
    "mondello":         "mondello",
    "palermo":          "palermo",
    "san vito lo capo": "san-vito-lo-capo",
    "san_vito_lo_capo": "san-vito-lo-capo",
    "san-vito-lo-capo": "san-vito-lo-capo",
    "sanvitolocapo":    "san-vito-lo-capo",
    "siracusa":         "siracusa",
    "syracuse":         "siracusa",
    "taormina":         "taormina",

    # Spain
    "ibiza":     "ibiza",
    "mallorca":  "mallorca",
    "majorca":   "mallorca",
    "barcelona": "barcelona",
    "barsa":     "barcelona",
}

# Output folder structure (used to create directories)
# country → dest → area (None = leaf)
OUTPUT_TREE = {
    "malta": {},
    "greece": {
        "santorini": {},
    },
    "italy": {
        "sicily": {
            "agrigento":      {},
            "cefalu":         {},
            "mondello":       {},
            "palermo":        {},
            "san-vito-lo-capo": {},
            "siracusa":       {},
            "taormina":       {},
        },
        "rome":   {},
        "venice": {},
    },
    "spain": {
        "ibiza":     {},
        "mallorca":  {},
        "barcelona": {},
    },
}

# Natural-language alt text per destination key
ALT_TEXT = {
    "malta":                        "Coastal landscape and historic architecture in Malta",
    "greece-santorini":             "Whitewashed buildings and caldera views in Santorini, Greece",
    "italy-rome":                   "Historic monuments and city streets in Rome, Italy",
    "italy-venice":                 "Grand Canal and gondolas in Venice, Italy",
    "italy-sicily":                 "Coastline and landscape in Sicily, Italy",
    "italy-sicily-agrigento":       "Ancient Greek temples in the Valley of the Temples, Agrigento, Sicily",
    "italy-sicily-cefalu":          "Sandy beach and Norman cathedral in Cefalù, Sicily",
    "italy-sicily-mondello":        "Turquoise water and sandy beach in Mondello, Sicily",
    "italy-sicily-palermo":         "Street market and historic buildings in Palermo, Sicily",
    "italy-sicily-san-vito-lo-capo":"Clear turquoise water and white sand beach in San Vito Lo Capo, Sicily",
    "italy-sicily-siracusa":        "Ancient Greek theatre and harbour in Siracusa, Sicily",
    "italy-sicily-taormina":        "Greek theatre with sea views in Taormina, Sicily",
    "spain-ibiza":                  "Coastal scenery and beach in Ibiza, Spain",
    "spain-mallorca":               "Beach and turquoise coastline in Mallorca, Spain",
    "spain-barcelona":              "Gaudí architecture and city views in Barcelona, Spain",
}

# Destination keys that get a hero image (first image per key = hero)
HERO_KEYS = {
    "malta",
    "greece-santorini",
    "italy-rome",
    "italy-venice",
    "italy-sicily",
    "spain-mallorca",
    "spain-ibiza",
    "spain-barcelona",
}

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def slugify(text: str) -> str:
    """Remove accents and non-ASCII, lowercase, replace non-alphanum with hyphens."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text


def map_folder(name: str) -> str:
    """Map a source folder name to a canonical slug."""
    key = name.strip().lower()
    if key in AREA_MAP:
        return AREA_MAP[key]
    # Try with accents stripped
    stripped = slugify(name)
    if stripped in AREA_MAP:
        return AREA_MAP[stripped]
    # Spaces variant
    spaced = key.replace("_", " ").replace("-", " ")
    if spaced in AREA_MAP:
        return AREA_MAP[spaced]
    return stripped  # fallback: best-effort slug


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def process_image(src: Path, dest: Path) -> tuple:
    """
    Load, resize, convert to WebP with stripped metadata, save.
    Returns (width, height, original_size_kb, output_size_kb).
    """
    original_kb = src.stat().st_size // 1024

    img = Image.open(src)

    # Convert palette / RGBA → RGB
    if img.mode == "P":
        img = img.convert("RGBA")
    if img.mode == "RGBA":
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg.convert("RGB")
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # Resize if wider than MAX_WIDTH
    if img.width > MAX_WIDTH:
        ratio     = MAX_WIDTH / img.width
        new_h     = int(img.height * ratio)
        img       = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)

    width, height = img.size

    # Save WebP — no exif/metadata
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)

    output_kb = dest.stat().st_size // 1024
    return width, height, original_kb, output_kb


def dest_key_from_parts(country: str, dest: str | None, area: str | None) -> str:
    parts = [country]
    if dest:
        parts.append(dest)
    if area:
        parts.append(area)
    return "-".join(parts)


def output_subpath(country: str, dest: str | None, area: str | None) -> Path:
    """Return the relative output folder path under OUTPUT_DIR."""
    p = Path(country)
    if dest:
        p = p / dest
    if area:
        p = p / area
    return p


def build_filename(country: str, dest: str | None, area: str | None, n: int) -> str:
    parts = [country]
    if dest:
        parts.append(dest)
    if area:
        parts.append(area)
    parts.append(f"{n:02d}")
    return "-".join(parts) + ".webp"


def get_alt(country: str, dest: str | None, area: str | None) -> str:
    key = dest_key_from_parts(country, dest, area)
    return ALT_TEXT.get(key, f"Travel photo from {country.title()}")


def suggested_use(dest_key: str, counter: int) -> str:
    if counter == 1 and dest_key in HERO_KEYS:
        return "hero"
    if counter <= 3:
        return "card"
    return "gallery"


# ═══════════════════════════════════════════════════════════════════════════════
# FOLDER STRUCTURE CREATION
# ═══════════════════════════════════════════════════════════════════════════════

def create_output_tree():
    def walk(node, base):
        for name, children in node.items():
            folder = base / name
            folder.mkdir(parents=True, exist_ok=True)
            if children:
                walk(children, folder)

    walk(OUTPUT_TREE, OUTPUT_DIR)
    print(f"Output folder structure created under:\n  {OUTPUT_DIR}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# SOURCE TRAVERSAL
# ═══════════════════════════════════════════════════════════════════════════════

def classify_path(rel_parts: list[str]) -> tuple[str, str | None, str | None]:
    """
    Given path components below the source root (e.g. ['01_ITALY', 'SICILY', 'TAORMINA']),
    return (country, dest, area) canonical slugs.

    Handles 1, 2, or 3 levels of nesting.
    """
    if not rel_parts:
        return ("unknown", None, None)

    country = COUNTRY_MAP.get(rel_parts[0].lower(), slugify(rel_parts[0]))

    dest = None
    area = None

    if len(rel_parts) >= 2:
        dest = map_folder(rel_parts[1])

    if len(rel_parts) >= 3:
        area = map_folder(rel_parts[2])

    # For Malta images directly in 01_MALTA (no sub-folders),
    # dest and area stay None — that's correct.

    return country, dest, area


def iter_source_images(source_dir: Path):
    """
    Yield (filepath, country, dest, area) for every image in the source tree.
    Yields folder paths for empty-folder detection.
    """
    empty_folders = []

    def recurse(folder: Path, rel_parts: list[str]):
        entries = sorted(folder.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        images  = [e for e in entries if e.is_file() and e.suffix.lower() in IMAGE_EXTS]
        subdirs = [e for e in entries if e.is_dir()]
        non_images = [e for e in entries if e.is_file() and e.suffix.lower() not in IMAGE_EXTS]

        if not images and not subdirs:
            empty_folders.append(str(folder))
            return

        for img_path in images:
            country, dest, area = classify_path(rel_parts)
            yield img_path, country, dest, area

        for sub in subdirs:
            yield from recurse(sub, rel_parts + [sub.name])

    for top in sorted(source_dir.iterdir()):
        if top.is_dir() and top.name.lower() in COUNTRY_MAP or \
           top.is_dir() and not top.name.startswith("."):
            yield from recurse(top, [top.name])

    return empty_folders  # won't reach via yield — handled separately


def collect_source(source_dir: Path):
    """Collect all source images, return list and empty folder list."""
    images = []
    empty_folders = []

    def recurse(folder: Path, rel_parts: list[str]):
        try:
            entries = sorted(folder.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except PermissionError:
            return

        imgs    = [e for e in entries if e.is_file() and e.suffix.lower() in IMAGE_EXTS]
        subdirs = [e for e in entries if e.is_dir() and not e.name.startswith(".")]

        if not imgs and not subdirs:
            empty_folders.append(str(folder))
            return

        for img_path in imgs:
            country, dest, area = classify_path(rel_parts)
            images.append((img_path, country, dest, area))

        for sub in subdirs:
            recurse(sub, rel_parts + [sub.name])

    for top in sorted(source_dir.iterdir()):
        if top.is_dir() and not top.name.startswith("."):
            recurse(top, [top.name])

    return images, empty_folders


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT FILE WRITERS
# ═══════════════════════════════════════════════════════════════════════════════

CSV_FIELDS = [
    "source_path", "output_path", "country", "destination", "area",
    "filename", "alt_text", "suggested_use",
    "width", "height", "original_size_kb", "output_size_kb", "duplicate_of",
]


def write_csv(rows: list[dict], path: Path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"  Written: {path.name}")


def write_json(rows: list[dict], path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"  Written: {path.name}")


def write_report(path: Path, rows, duplicates, empty_folders, failed,
                 total_source, total_processed):
    hero_map = {r["country"] + ("/" + r["destination"] if r["destination"] else "") +
                ("/" + r["area"] if r["area"] else ""): r["filename"]
                for r in rows if r.get("suggested_use") == "hero"}

    lines = [
        "# dlproject56.com — Image Processing Report",
        f"",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"",
        f"---",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Source images found | {total_source} |",
        f"| Successfully processed | {total_processed} |",
        f"| Duplicate files skipped | {len(duplicates)} |",
        f"| Empty folders | {len(empty_folders)} |",
        f"| Failed | {len(failed)} |",
        f"",
        f"---",
        f"",
        f"## Final Folder Structure",
        f"",
        f"```",
        f"images/destinations/",
        f"  malta/",
        f"  greece/",
        f"    santorini/",
        f"  italy/",
        f"    sicily/",
        f"      agrigento/",
        f"      cefalu/",
        f"      mondello/",
        f"      palermo/",
        f"      san-vito-lo-capo/",
        f"      siracusa/",
        f"      taormina/",
        f"    rome/",
        f"    venice/",
        f"  spain/",
        f"    ibiza/",
        f"    mallorca/",
        f"    barcelona/",
        f"```",
        f"",
        f"---",
        f"",
        f"## Processed Images by Destination",
        f"",
    ]

    by_dest = defaultdict(list)
    for r in rows:
        if r.get("duplicate_of"):
            continue
        key = r["country"]
        if r["destination"]:
            key += "/" + r["destination"]
        if r["area"]:
            key += "/" + r["area"]
        by_dest[key].append(r["filename"])

    for dest_key in sorted(by_dest):
        files = by_dest[dest_key]
        lines.append(f"### {dest_key}")
        lines.append(f"")
        lines.append(f"Count: {len(files)}")
        lines.append(f"")
        for fn in files:
            lines.append(f"- `{fn}`")
        lines.append(f"")

    lines += [
        f"---",
        f"",
        f"## Recommended Hero Images",
        f"",
        f"| Destination page | Hero image |",
        f"|------------------|------------|",
    ]
    for page_key in [
        "malta", "greece/santorini", "italy/rome", "italy/venice",
        "italy/sicily", "spain/mallorca", "spain/ibiza", "spain/barcelona",
    ]:
        hero_fn = hero_map.get(page_key, "*(no image processed)*")
        lines.append(f"| /{page_key}/ | `{hero_fn}` |")

    lines += ["", "---", "", "## Duplicate Files Skipped", ""]
    if duplicates:
        lines.append(f"| Source file | Duplicate of |")
        lines.append(f"|-------------|--------------|")
        for d in duplicates:
            lines.append(f"| `{d['source']}` | `{d['duplicate_of']}` |")
    else:
        lines.append("*(none)*")

    lines += ["", "---", "", "## Empty Folders", ""]
    if empty_folders:
        for ef in empty_folders:
            lines.append(f"- `{ef}`")
    else:
        lines.append("*(none)*")

    lines += ["", "---", "", "## Failed Files", ""]
    if failed:
        lines.append(f"| File | Error |")
        lines.append(f"|------|-------|")
        for f_item in failed:
            lines.append(f"| `{f_item['file']}` | {f_item['error']} |")
    else:
        lines.append("*(none)*")

    lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Written: {path.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print()
    print("=" * 62)
    print("  dlproject56.com — Destination Image Processor")
    print("=" * 62)
    print(f"  Source : {SOURCE_DIR}")
    print(f"  Output : {OUTPUT_DIR}")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Validate source
    if not SOURCE_DIR.exists():
        print(f"ERROR: Source folder not found:\n  {SOURCE_DIR}")
        print("\nCheck that the path is correct and the folder exists.")
        sys.exit(1)

    # Create all output folders
    create_output_tree()

    # Collect source images
    print("Scanning source images …")
    source_images, empty_folders = collect_source(SOURCE_DIR)
    print(f"  Found {len(source_images)} image file(s) across source folders.")
    if empty_folders:
        print(f"  {len(empty_folders)} empty folder(s) detected.")
    print()

    # Process
    rows        = []
    duplicates  = []
    failed      = []
    hash_seen   = {}       # md5 → first output filename
    counters    = defaultdict(int)  # dest_key → sequential counter

    for src_path, country, dest, area in source_images:
        rel_src = str(src_path.relative_to(SOURCE_DIR))

        # Hash check
        try:
            h = file_md5(src_path)
        except Exception as e:
            failed.append({"file": rel_src, "error": str(e)})
            continue

        if h in hash_seen:
            first_fn = hash_seen[h]
            print(f"  [SKIP DUPLICATE] {rel_src}  →  {first_fn}")
            duplicates.append({"source": rel_src, "duplicate_of": first_fn})
            rows.append({
                "source_path":    rel_src,
                "output_path":    "",
                "country":        country,
                "destination":    dest or "",
                "area":           area or "",
                "filename":       "",
                "alt_text":       "",
                "suggested_use":  "duplicate",
                "width":          "",
                "height":         "",
                "original_size_kb": src_path.stat().st_size // 1024,
                "output_size_kb": "",
                "duplicate_of":   first_fn,
            })
            continue

        # Build output path
        dk = dest_key_from_parts(country, dest, area)
        counters[dk] += 1
        n = counters[dk]

        filename    = build_filename(country, dest, area, n)
        sub_path    = output_subpath(country, dest, area)
        output_path = OUTPUT_DIR / sub_path / filename

        # Process image
        try:
            w, h, orig_kb, out_kb = process_image(src_path, output_path)
        except Exception as e:
            failed.append({"file": rel_src, "error": str(e)})
            print(f"  [FAIL] {rel_src}: {e}")
            continue

        hash_seen[h] = filename
        use = suggested_use(dk, n)
        alt = get_alt(country, dest, area)

        rel_out = str(output_path.relative_to(WORKSPACE)).replace("\\", "/")

        rows.append({
            "source_path":    rel_src,
            "output_path":    rel_out,
            "country":        country,
            "destination":    dest or "",
            "area":           area or "",
            "filename":       filename,
            "alt_text":       alt,
            "suggested_use":  use,
            "width":          w,
            "height":         h,
            "original_size_kb": orig_kb,
            "output_size_kb": out_kb,
            "duplicate_of":   "",
        })

        size_tag = f"{orig_kb}KB → {out_kb}KB"
        print(f"  [OK] {rel_src}")
        print(f"       → {rel_out}  ({w}×{h}, {size_tag})")

    total_source    = len(source_images)
    total_processed = sum(1 for r in rows if r["suggested_use"] != "duplicate" and r["output_path"])

    print()
    print("Writing output files …")
    write_csv(rows, WORKSPACE / "image-map.csv")
    write_json(rows, WORKSPACE / "image-map.json")
    write_report(
        path            = WORKSPACE / "processing-report.md",
        rows            = rows,
        duplicates      = duplicates,
        empty_folders   = empty_folders,
        failed          = failed,
        total_source    = total_source,
        total_processed = total_processed,
    )

    print()
    print("=" * 62)
    print("  DONE")
    print(f"  Source images scanned : {total_source}")
    print(f"  Processed successfully: {total_processed}")
    print(f"  Duplicates skipped    : {len(duplicates)}")
    print(f"  Empty folders found   : {len(empty_folders)}")
    print(f"  Failed                : {len(failed)}")
    print()
    print(f"  Output files in: {WORKSPACE}")
    print(f"    image-map.csv")
    print(f"    image-map.json")
    print(f"    processing-report.md")
    print("=" * 62)
    print()


if __name__ == "__main__":
    main()
