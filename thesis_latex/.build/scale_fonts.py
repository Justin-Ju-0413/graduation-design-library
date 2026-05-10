"""Scale all font sizes in figure generation scripts by a coordinated factor."""
import re
from pathlib import Path


def scale_inline_fontsizes(text: str, factor: float) -> str:
    """Find all fontsize=XX.N patterns and scale them."""
    def repl(m):
        val = float(m.group(1))
        new_val = val * factor
        # Round to 1 decimal place, but keep integer if it's close
        if abs(new_val - round(new_val)) < 0.05:
            return f"fontsize={int(round(new_val))}"
        return f"fontsize={new_val:.1f}"
    return re.sub(r"fontsize=([0-9]+(?:\.[0-9]+)?)", repl, text)


def scale_fs_defaults(text: str, factor: float) -> str:
    """Find fs=XX.N in function definitions and scale."""
    def repl(m):
        val = float(m.group(1))
        new_val = val * factor
        if abs(new_val - round(new_val)) < 0.05:
            return f"fs={int(round(new_val))}"
        return f"fs={new_val:.1f}"
    return re.sub(r"fs=([0-9]+(?:\.[0-9]+)?)", repl, text)


def scale_rcparams(text: str, factor: float) -> str:
    """Scale font size values in plt.rcParams."""
    def repl(m):
        key = m.group(1)
        val = float(m.group(2))
        new_val = val * factor
        if abs(new_val - round(new_val)) < 0.05:
            return f'"{key}": {int(round(new_val))}'
        return f'"{key}": {new_val:.1f}'
    return re.sub(r'"(font\.size|axes\.titlesize|axes\.labelsize|xtick\.labelsize|ytick\.labelsize|legend\.fontsize)":\s*([0-9]+(?:\.[0-9]+)?)', repl, text)


def process_file(path: Path, factor: float):
    text = path.read_text(encoding="utf-8")
    original = text
    text = scale_rcparams(text, factor)
    text = scale_fs_defaults(text, factor)
    text = scale_inline_fontsizes(text, factor)
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"Updated {path.name}")
    else:
        print(f"No changes in {path.name}")


if __name__ == "__main__":
    ROOT = Path(__file__).resolve().parent
    process_file(ROOT / "gen_block_diagrams.py", 1.20)
    process_file(ROOT / "fix_figures.py", 1.20)
    print("Done.")
