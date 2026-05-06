#!/usr/bin/env python3
"""
update_dashboard.py

Rescan the Graduation Design Library and update dashboard_status.json
with current file counts. Preserves manually-set status fields
(thesis progress, FPGA status, deadlines) unless overridden.

Usage:
    python scripts/update_dashboard.py                    # update file counts only
    python scripts/update_dashboard.py --reset            # reset all fields from defaults
    python scripts/update_dashboard.py --scan-only        # print scan results only, no write
"""

import json
import os
import re
import sys
from pathlib import Path

# Root directory of the library
LIBRARY_DIR = Path(r"C:\Users\16084\Documents\Graduation_Design_Library")
STATUS_FILE = LIBRARY_DIR / "dashboard_status.json"

# Directories to scan (relative to LIBRARY_DIR)
SCAN_DIRS = [
    "01_Project_Overview",
    "02_Source_Repos",
    "03_Documents",
    "04_Experiments",
    "05_Presentation",
    "06_References",
    "07_Backups",
    "08_Todo_And_Notes",
    "09_Thesis_Writing",
    "10_Final_Defense",
    "11_FYP_requirement",
    "scripts",
    "_archive",
]

# Default status data (used on --reset or if file doesn't exist)
DEFAULT_STATUS = {
    "thesis": {
        "chapters": {
            "Abstract": "done",
            "Ch1_Introduction": "done",
            "Ch2_Background": "done",
            "Ch3_Methodology": "done",
            "Ch4_Results": "done",
            "Ch5_Discussion": "done",
            "Ch6_Conclusion": "done",
        },
        "references": 27,
        "figures": 13,
        "estimated_pages": 47,
        "words": 11750,
        "declaration": "done",
        "toc": "pending",
        "plagiarism_check": "pending",
    },
    "fpga": {
        "hello_e203_board": "done",
        "cpu_boot_debug": "done",
        "nice_ila_confirm": "done",
        "rstat_result": "debugging",
        "performance_data": "pending",
        "accuracy_verify": "pending",
    },
    "deadlines": {
        "thesis_submission": "2026-05-06",
        "oral_presentation": "2026-05-13",
        "final_pdf": "2026-05-20",
    },
}


def count_files(directory: Path) -> dict:
    """Count files in each subdirectory of the library."""
    counts = {}
    total = 0
    for subdir in SCAN_DIRS:
        target = directory / subdir
        if target.is_dir():
            n = len(list(target.rglob("*")))
            # Filter out directories, count only files
            file_count = sum(1 for p in target.rglob("*") if p.is_file())
            counts[subdir] = file_count
            total += file_count
        else:
            counts[subdir] = 0
    return counts, total


def get_thesis_metadata(library_dir: Path) -> dict:
    """Extract live metadata from thesis files."""
    meta = {"figures": 0, "references": 0, "estimated_pages": 0, "words": 0}

    # Count figures in 09_Thesis_Writing/Figures/
    figures_dir = library_dir / "09_Thesis_Writing" / "Figures"
    if figures_dir.is_dir():
        meta["figures"] = len(list(figures_dir.glob("*.png"))) + len(
            list(figures_dir.glob("*.jpg"))
        )

    # Count references in .bib file
    bib_file = library_dir / "09_Thesis_Writing" / "References" / "references.bib"
    if bib_file.is_file():
        bib_text = bib_file.read_text(encoding="utf-8", errors="ignore")
        # Count all common BibTeX entry types
        for entry_type in ["article", "inproceedings", "misc", "techreport",
                            "phdthesis", "mastersthesis", "book", "inbook",
                            "proceedings", "incollection", "manual", "unpublished"]:
            meta["references"] += bib_text.count(f"@{entry_type}{{")

    # Count words from thesis markdown chapters (exclude concatenated Full_Thesis.md)
    thesis_dir = library_dir / "09_Thesis_Writing" / "draft"
    if thesis_dir.is_dir():
        all_md = list(thesis_dir.glob("*.md"))
        # Skip .Xil, 00_Full_Thesis.md (concatenation), 00_Abstract.md (also in Full),
        # TECHNICAL_DEBRIEF.md (notes), and other junk
        skip_patterns = re.compile(
            r'(Full_Thesis|TECHNICAL_DEBRIEF|\.Xil|^\.)', re.IGNORECASE
        )
        all_md = [f for f in all_md if not skip_patterns.search(f.name)]
        total_words = 0
        for md_file in all_md:
            try:
                text = md_file.read_text(encoding="utf-8", errors="ignore")
                # Remove code blocks (``` ... ```)
                text = re.sub(r'```[\s\S]*?```', '', text)
                # Remove inline code
                text = re.sub(r'`[^`]+`', '', text)
                # Remove markdown headers markers
                text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
                # Remove markdown links: [text](url) -> text
                text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
                # Remove image references: ![alt](url)
                text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)
                # Remove HTML tags
                text = re.sub(r'<[^>]+>', '', text)
                # Remove horizontal rules
                text = re.sub(r'^---+\s*$', '', text, flags=re.MULTILINE)
                # Collapse whitespace and count
                words = text.split()
                total_words += len(words)
            except Exception:
                pass
        meta["words"] = total_words

    return meta


def load_status() -> dict:
    """Load existing status file, or return defaults."""
    if STATUS_FILE.is_file():
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Warning: Corrupt status file, using defaults.", file=sys.stderr)
    return dict(DEFAULT_STATUS)


def write_status(status: dict):
    """Write status to JSON file."""
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
    print(f"Written: {STATUS_FILE}")


def main():
    reset = "--reset" in sys.argv
    scan_only = "--scan-only" in sys.argv

    # Scan files
    counts, total = count_files(LIBRARY_DIR)
    meta = get_thesis_metadata(LIBRARY_DIR)

    if scan_only:
        print("=== File Scan Results ===")
        for k, v in counts.items():
            print(f"  {k}: {v} files")
        print(f"  Total: {total} files")
        print(f"\n=== Thesis Metadata ===")
        for k, v in meta.items():
            print(f"  {k}: {v}")
        return

    # Load existing or default status
    if reset or not STATUS_FILE.is_file():
        status = dict(DEFAULT_STATUS)
    else:
        status = load_status()

    # Update file counts
    status["file_counts"] = counts
    status["library_total_files"] = total

    # Update live metadata (only if we got non-zero values)
    if meta["figures"] > 0:
        status["thesis"]["figures"] = meta["figures"]
    if meta["references"] > 0:
        status["thesis"]["references"] = meta["references"]
    if meta["words"] > 0:
        status["thesis"]["words"] = meta["words"]

    # Update timestamp
    from datetime import datetime

    status["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    write_status(status)
    print(f"Updated: {total} files across {len(counts)} directories")
    print(f"Thesis metadata: {meta['figures']} figures, {meta['references']} refs, {meta['words']} words")


if __name__ == "__main__":
    main()
