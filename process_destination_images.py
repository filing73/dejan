#!/usr/bin/env python3
"""
dlproject56.com — Destination Image Processor
Run this script locally on Windows to prepare source photos for production.

Requirements:
    pip install Pillow

Usage:
    python process_destination_images.py
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
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SOURCE_DIR = Path(r"H:\DL_AI_WORK\02_ACTIVE_PROJECTS\DLPROJECT56\Duplicat za rodju")
WORKSPACE  = Path(r"H:\DL_AI_WORK\02_ACTIVE_PROJECTS\DLPROJECT56\01_DLPROJECT56_COM_glavni sajt")
OUTPUT_DIR = WORKSPACE / "images" / "destinations"

WEBP_QUALITY = 80
MAX_WIDTH    = 1600
IMAGE_EXTS   = {".jpg", ".jpeg", ".png", ".webp"}

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
    "sicily":   "sicily",
    "sicilia":  "sicily",
    "rome":     "rome",
    "roma":     "rome",
    "venice":   "venice",
    "venezia":  "venice",

    # Sicily — areas
    "agrigento":          "agrigento",
    "cefalù":             "cefalu",
    "cefalu":             "cefalu",
    "cefalú":             "cefalu",
    "mondello":           "mondello",
    "palermo":            "palermo",
    "san vito lo capo":   "san-vito-lo-capo",
    "san_vito_lo_capo":   "san-vito-lo-capo",
    "san-vito-lo-capo":   "san-vito-lo-capo",
    "sanvitolocapo":      "san-vito-lo-capo",
    "siracusa":           "siracusa",
    "syracuse":           "siracusa",
    "taormina":           "taormina",

    # Spain
    "ibiza":     "ibiza",
    "mallorca":  "mallorca",
    "majorca":   "mallorca",
    "barcelona": "barcelona",
    "barsa":     "barcelona",
}

# Output folder tree (used to pre-create directories)
OUTPUT_TREE = {
    "malta": {},
    "greece": {
        "santorini": {},
    },
    "italy": {
        "sicily": {
            "agrigento":       {},
            "cefalu":          {},
            "mondello":        {},
            "palermo":         {},
            "san-vito-lo-capo": {},
            "siracusa":        {},
            "taormina":        {},
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

# Alt text per destination key
ALT_TEXT = {
    "malta":                          "Coastal landscape and historic architecture in Malta",
    "greece-santorini":               "Whitewashed buildings and caldera views in Santorini, Greece",
    "italy-rome":                     "Historic monuments and city streets in Rome, Italy",
    "italy-venice":                   "Grand Canal and gondolas in Venice, Italy",
    "italy-sicily":                   "Coastline and landscape in Sicily, Italy",
    "italy-sicily-agrigento":         "Ancient Greek temples in the Valley of the Temples, Agrigento, Sicily",
    "italy-sicily-cefalu":            "Sandy beach and Norman cathedral in Cefalù, Sicily",
    "italy-sicily-mondello":          "Turquoise water and sandy beach in Mondello, Sicily",
    "italy-sicily-palermo":           "Street market and historic buildings in Palermo, Sicily",
    "italy-sicily-san-vito-lo-capo":  "Clear turquoise water and white sand beach in San Vito Lo Capo, Sicily",
    "italy-sicily-siracusa":          "Ancient Greek theatre and harbour in Siracusa, Sicily",
    "italy-sicily-taormina":          "Greek theatre with sea views in Taormina, Sicily",
    "spain-ibiza":                    "Coastal scenery and beach in Ibiza, Spain",
    "spain-mallorca":                 "Beach and turquoise coastline in Mallorca, Spain",
    "spain-barcelona":                "Gaudí architecture and city views in Barcelona, Spain",
}

# Destination keys eligible for a hero image (first image per key = hero)
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
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def map_folder(name: str) -> str:
    key = name.strip().lower()
    if key in AREA_MAP:
        return AREA_MAP[key]
    stripped = slugify(name)
    if stripped in AREA_MAP:
        return AREA_MAP[stripped]
    spaced = key.replace("_", " ").replace("-", " ")
    if spaced in AREA_MAP:
        return AREA_MAP[spaced]
    return stripped


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def process_image(src: Path, dst: Path):
    """Load, resize, convert to WebP (metadata stripped), save. Returns (w, h, orig_kb, out_kb)."""
    orig_kb = src.stat().st_size // 1024
    img = Image.open(src)

    if img.mode == "P":
        img = img.convert("RGBA")
    if img.mode == "RGBA":
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg.convert("RGB")
    elif img.mode != "RGB":
        img = img.convert("RGB")

    if img.width > MAX_WIDTH:
        new_h = int(img.height * MAX_WIDTH / img.width)
        img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)

    w, h = img.size
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "WEBP", quality=WEBP_QUALITY, method=6)
    out_kb = dst.stat().st_size // 1024
    return w, h, orig_kb, out_kb


def classify_path(rel_parts: list) -> tuple:
    """Map source folder path components to (country, dest, area) slugs."""
    if not rel_parts:
        return "unknown", None, None
    country = COUNTRY_MAP.get(rel_parts[0].lower(), slugify(rel_parts[0]))
    dest = map_folder(rel_parts[1]) if len(rel_parts) >= 2 else None
    area = map_folder(rel_parts[2]) if len(rel_parts) >= 3 else None
    return country, dest, area


def dest_key(country, dest, area) -> str:
    parts = [country]
    if dest:
        parts.append(dest)
    if area:
        parts.append(area)
    return "-".join(parts)


def build_filename(country, dest, area, n: int) -> str:
    return dest_key(country, dest, area) + f"-{n:02d}.webp"


def output_rel_path(country, dest, area) -> Path:
    p = Path(country)
    if dest:
        p = p / dest
    if area:
        p = p / area
    return p


def get_alt(country, dest, area) -> str:
    return ALT_TEXT.get(dest_key(country, dest, area), f"Travel photo — {country.title()}")


def get_use(dk: str, n: int) -> str:
    if n == 1 and dk in HERO_KEYS:
        return "hero"
    if n <= 3:
        return "card"
    return "gallery"


# ═══════════════════════════════════════════════════════════════════════════════
# FOLDER TREE CREATION
# ═══════════════════════════════════════════════════════════════════════════════

def create_output_tree():
    def walk(node, base):
        for name, children in node.items():
            folder = base / name
            folder.mkdir(parents=True, exist_ok=True)
            if children:
                walk(children, folder)
    walk(OUTPUT_TREE, OUTPUT_DIR)
    print(f"  Output tree created under {OUTPUT_DIR}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# SOURCE COLLECTION
# ═══════════════════════════════════════════════════════════════════════════════

def collect_source(source_dir: Path):
    images = []
    empty_folders = []

    def recurse(folder: Path, rel_parts: list):
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


def write_csv(rows: list, path: Path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"  Written: {path.name}")


def write_json(rows: list, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"  Written: {path.name}")


def write_report(path: Path, rows, duplicates, empty_folders, failed,
                 total_source, total_processed):
    # Hero map
    hero_map = {}
    for r in rows:
        if r.get("suggested_use") == "hero":
            dk = r["country"]
            if r["destination"]:
                dk += "/" + r["destination"]
            if r["area"]:
                dk += "/" + r["area"]
            hero_map[dk] = r["filename"]

    # Images by destination
    by_dest = defaultdict(list)
    for r in rows:
        if r.get("duplicate_of") or not r.get("output_path"):
            continue
        dk = r["country"]
        if r["destination"]:
            dk += "/" + r["destination"]
        if r["area"]:
            dk += "/" + r["area"]
        by_dest[dk].append(r["filename"])

    lines = [
        "# dlproject56.com — Image Processing Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Source images found | {total_source} |",
        f"| Successfully processed | {total_processed} |",
        f"| Duplicate files skipped | {len(duplicates)} |",
        f"| Empty folders | {len(empty_folders)} |",
        f"| Failed | {len(failed)} |",
        "",
        "---",
        "",
        "## Final Folder Structure",
        "",
        "```",
        "images/destinations/",
        "  malta/",
        "  greece/",
        "    santorini/",
        "  italy/",
        "    sicily/",
        "      agrigento/",
        "      cefalu/",
        "      mondello/",
        "      palermo/",
        "      san-vito-lo-capo/",
        "      siracusa/",
        "      taormina/",
        "    rome/",
        "    venice/",
        "  spain/",
        "    ibiza/",
        "    mallorca/",
        "    barcelona/",
        "```",
        "",
        "---",
        "",
        "## Processed Images by Destination",
        "",
    ]

    for dk in sorted(by_dest):
        files = by_dest[dk]
        lines += [f"### {dk}", "", f"Count: {len(files)}", ""]
        for fn in files:
            lines.append(f"- `{fn}`")
        lines.append("")

    lines += [
        "---",
        "",
        "## Recommended Hero Images",
        "",
        "| Destination page | Hero filename |",
        "|------------------|---------------|",
    ]
    for page_key in [
        "malta", "greece/santorini", "italy/rome", "italy/venice",
        "italy/sicily", "spain/mallorca", "spain/ibiza", "spain/barcelona",
    ]:
        hero_fn = hero_map.get(page_key, "*(no image processed)*")
        lines.append(f"| /{page_key}/ | `{hero_fn}` |")

    lines += ["", "---", "", "## Duplicate Files Skipped", ""]
    if duplicates:
        lines += ["| Source file | Duplicate of |", "|-------------|--------------|"]
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
        lines += ["| File | Error |", "|------|-------|"]
        for fi in failed:
            lines.append(f"| `{fi['file']}` | {fi['error']} |")
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
    print("=" * 64)
    print("  dlproject56.com — Destination Image Processor")
    print("=" * 64)
    print(f"  Source    : {SOURCE_DIR}")
    print(f"  Workspace : {WORKSPACE}")
    print(f"  Output    : {OUTPUT_DIR}")
    print(f"  Started   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    if not SOURCE_DIR.exists():
        print(f"ERROR: Source folder not found:\n  {SOURCE_DIR}")
        sys.exit(1)

    if not WORKSPACE.exists():
        print(f"ERROR: Workspace folder not found:\n  {WORKSPACE}")
        sys.exit(1)

    print("Creating output folder structure …")
    create_output_tree()

    print("Scanning source images …")
    source_images, empty_folders = collect_source(SOURCE_DIR)
    print(f"  Found {len(source_images)} image file(s).")
    if empty_folders:
        print(f"  {len(empty_folders)} empty folder(s) detected.")
    print()

    rows       = []
    duplicates = []
    failed     = []
    hash_seen  = {}
    counters   = defaultdict(int)

    for src_path, country, dest, area in source_images:
        rel_src = str(src_path.relative_to(SOURCE_DIR))

        # Hash / duplicate check
        try:
            h = file_md5(src_path)
        except Exception as e:
            failed.append({"file": rel_src, "error": str(e)})
            continue

        if h in hash_seen:
            first_fn = hash_seen[h]
            print(f"  [SKIP DUP] {rel_src}  →  {first_fn}")
            duplicates.append({"source": rel_src, "duplicate_of": first_fn})
            rows.append({
                "source_path": rel_src, "output_path": "", "country": country,
                "destination": dest or "", "area": area or "", "filename": "",
                "alt_text": "", "suggested_use": "duplicate",
                "width": "", "height": "",
                "original_size_kb": src_path.stat().st_size // 1024,
                "output_size_kb": "", "duplicate_of": first_fn,
            })
            continue

        # Build output path
        dk = dest_key(country, dest, area)
        counters[dk] += 1
        n        = counters[dk]
        filename = build_filename(country, dest, area, n)
        out_path = OUTPUT_DIR / output_rel_path(country, dest, area) / filename

        # Process
        try:
            w, h, orig_kb, out_kb = process_image(src_path, out_path)
        except Exception as e:
            failed.append({"file": rel_src, "error": str(e)})
            print(f"  [FAIL] {rel_src}: {e}")
            continue

        hash_seen[h] = filename
        use = get_use(dk, n)
        alt = get_alt(country, dest, area)
        rel_out = str(out_path.relative_to(WORKSPACE)).replace("\\", "/")

        rows.append({
            "source_path": rel_src, "output_path": rel_out,
            "country": country, "destination": dest or "", "area": area or "",
            "filename": filename, "alt_text": alt, "suggested_use": use,
            "width": w, "height": h,
            "original_size_kb": orig_kb, "output_size_kb": out_kb,
            "duplicate_of": "",
        })

        tag = f"{orig_kb}KB → {out_kb}KB  ({w}×{h})  [{use}]"
        print(f"  [OK] {filename}  —  {tag}")

    total_source    = len(source_images)
    total_processed = sum(1 for r in rows if r["suggested_use"] != "duplicate" and r.get("output_path"))

    print()
    print("Writing output files …")
    write_csv(rows,  WORKSPACE / "image-map.csv")
    write_json(rows, WORKSPACE / "image-map.json")
    write_report(
        path=WORKSPACE / "processing-report.md",
        rows=rows, duplicates=duplicates, empty_folders=empty_folders,
        failed=failed, total_source=total_source, total_processed=total_processed,
    )

    print()
    print("=" * 64)
    print("  DONE")
    print(f"  Source images scanned : {total_source}")
    print(f"  Processed             : {total_processed}")
    print(f"  Duplicates skipped    : {len(duplicates)}")
    print(f"  Empty folders         : {len(empty_folders)}")
    print(f"  Failed                : {len(failed)}")
    print()
    print(f"  Output → {WORKSPACE}")
    print(f"    image-map.csv")
    print(f"    image-map.json")
    print(f"    processing-report.md")
    print(f"    images\\destinations\\  (all WebP files)")
    print("=" * 64)
    print()


if __name__ == "__main__":
    main()
