import sys
from pathlib import Path

CHAPTERS = Path(__file__).resolve().parents[1] / "chapters"

mapping = {
    "0.60": "0.72",
    "0.65": "0.76",
    "0.70": "0.82",
    "0.75": "0.86",
    "0.80": "0.92",
    "0.85": "0.96",
}

for fname in ["03_3_methodology.tex", "04_4_results.tex"]:
    path = CHAPTERS / fname
    text = path.read_text(encoding="utf-8")
    for old, new in mapping.items():
        text = text.replace(f"width={old}\\textwidth", f"width={new}\\textwidth")
    path.write_text(text, encoding="utf-8")
    print(f"Updated {fname}")
