#!/bin/bash
# =============================================================================
# Thesis Build Pipeline
# Usage: bash build.sh [pdf|docx|all]
#
# Workflow:
#   1. Edit chapters/*.tex and main.tex
#   2. Run: bash build.sh all
#   3. Output: main_final.pdf + FYP_FINAL.docx
# =============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

PANDOC="/c/Users/16084/AppData/Local/Pandoc/pandoc"
PYTHON="/c/Users/16084/AppData/Local/Programs/Python/Python313/python"
BUILD_DIR="$SCRIPT_DIR/.build"
CHAPTERS_DIR="$SCRIPT_DIR/chapters"
FIGURES_DIR="$SCRIPT_DIR/figures"

MODE="${1:-all}"

echo "=== Thesis Build Pipeline ==="
echo "Mode: $MODE"
echo ""

# ---- Build PDF ----
build_pdf() {
    echo "[0/3] Generating figures..."
    "$PYTHON" "$BUILD_DIR/gen_block_diagrams.py" 2>&1
    "$PYTHON" "$BUILD_DIR/fix_figures.py" 2>&1

    echo "[1/3] Building PDF..."
    xelatex -interaction=nonstopmode -job-name=main_final main.tex > /dev/null 2>&1
    biber main_final > /dev/null 2>&1
    xelatex -interaction=nonstopmode -job-name=main_final main.tex > /dev/null 2>&1
    xelatex -interaction=nonstopmode -job-name=main_final main.tex > /dev/null 2>&1

    # Move build artifacts to .build/
    for ext in aux bbl bcf blg lof log lot out run.xml toc; do
        mv -f "main_final.$ext" "$BUILD_DIR/" 2>/dev/null || true
    done
    echo "   -> main_final.pdf"
}

# ---- Build DOCX ----
build_docx() {
    echo "[2/3] Building DOCX (Pandoc)..."

    CSL_FILE="$SCRIPT_DIR/ieee.csl"
    if [ ! -f "$CSL_FILE" ]; then
        CSL_FILE=$(find "$SCRIPT_DIR" -name "ieee.csl" 2>/dev/null | head -1)
    fi

    # Pandoc: LaTeX -> DOCX with embedded images, IEEE citations
    "$PANDOC" main.tex -o "$BUILD_DIR/_pandoc_raw.docx" \
        --reference-doc="$BUILD_DIR/pandoc-reference.docx" \
        --bibliography=references.bib \
        --csl="$CSL_FILE" \
        --citeproc \
        --number-sections \
        --resource-path="figures" \
        --resource-path="chapters" \
        -M reference-section-title=References 2>&1

    echo "   -> _pandoc_raw.docx"

    # Post-process: enforce fonts, styles, clean up
    echo "[3/3] Post-processing DOCX..."
    "$PYTHON" "$BUILD_DIR/post_process_final.py" 2>&1
    echo "   -> FYP_FINAL.docx"
}

case "$MODE" in
    pdf)
        build_pdf
        ;;
    docx)
        build_docx
        ;;
    all)
        build_pdf
        build_docx
        ;;
    *)
        echo "Usage: bash build.sh [pdf|docx|all]"
        exit 1
        ;;
esac

echo ""
echo "=== Done ==="
ls -lh main_final.pdf FYP_FINAL.docx 2>/dev/null
