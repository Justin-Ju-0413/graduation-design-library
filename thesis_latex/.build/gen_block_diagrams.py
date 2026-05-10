"""Generate clean architecture diagrams for the thesis.

The diagrams are intentionally rebuilt from primitives instead of edited as
bitmaps. This keeps labels legible and makes line routing explicit.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"

INK = "#1F2933"
MUTED = "#64748B"
LINE = "#64748B"
BLUE = "#2F6FB3"
GREEN = "#23835A"
AMBER = "#B7791F"
RED = "#B42318"
VIOLET = "#6B46C1"
FILL_BLUE = "#DCEBFF"
FILL_GREEN = "#DDF4E7"
FILL_AMBER = "#FFF1C7"
FILL_GRAY = "#EEF2F6"
FILL_VIOLET = "#EDE7FF"
FILL_RED = "#FDE2E2"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "figure.dpi": 220,
        "savefig.dpi": 300,
        "text.color": INK,
    }
)


def save(fig, name: str):
    out = FIG_DIR / name
    fig.savefig(out, bbox_inches="tight", facecolor="white", pad_inches=0.08)
    plt.close(fig)
    print(f"  saved {out}")


def setup(figsize=(11, 6), xlim=(0, 16), ylim=(0, 9)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, title, body=None, fc=FILL_GRAY, ec=LINE, fs=11, lw=1.4):
    rect = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw)
    ax.add_patch(rect)
    if body:
        ax.text(x + w / 2, y + h * 0.62, title, ha="center", va="center", fontsize=fs, fontweight="bold")
        ax.text(x + w / 2, y + h * 0.30, body, ha="center", va="center", fontsize=fs - 1, color=MUTED, linespacing=1.25)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=fs, fontweight="bold", linespacing=1.25)
    return rect


def single_label_box(ax, x, y, w, h, lines, fc=FILL_GRAY, ec=LINE, fs=10.5, lw=1.4):
    rect = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, lines, ha="center", va="center", fontsize=fs, fontweight="bold", linespacing=1.25)
    return rect


def arrow(ax, xy1, xy2, color=LINE, lw=1.5, both=False, rad=0.0):
    style = "<|-|>" if both else "-|>"
    ax.add_patch(
        FancyArrowPatch(
            xy1,
            xy2,
            arrowstyle=style,
            mutation_scale=13,
            linewidth=lw,
            color=color,
            connectionstyle=f"arc3,rad={rad}",
            shrinkA=3,
            shrinkB=3,
        )
    )


def title(ax, main, sub):
    return


def fig3_1_soc_architecture():
    fig, ax = setup(figsize=(11.3, 6.2), xlim=(0, 16), ylim=(0, 9))
    title(ax, "E203 SoC with NICE CNN accelerator", "Custom instructions carry operands through NICE; memory and I/O stay on the system bus.")

    # Top compute path. The bus is intentionally kept below this row so that
    # peripheral drops cannot be mistaken for core-to-accelerator connections.
    box(ax, 0.7, 5.30, 3.0, 2.25, "E203 core", "RV32IMAC\nIFU / EXU / LSU", FILL_BLUE, BLUE, fs=12)
    box(ax, 5.35, 5.30, 3.35, 2.25, "NICE CNN accelerator", "decoder + FSM\n4x4 INT8 PE array", FILL_GREEN, GREEN, fs=12)
    arrow(ax, (3.76, 6.32), (5.30, 6.32), AMBER, lw=2.4, both=True)
    ax.text(
        4.53,
        6.84,
        "NICE\nreq/resp",
        ha="center",
        va="center",
        fontsize=9.0,
        linespacing=1.0,
        color=AMBER,
        fontweight="bold",
        bbox=dict(facecolor="white", edgecolor="none", pad=1.2),
    )

    # Memory blocks sit above the fabric and use separate short drops.
    box(ax, 9.80, 6.18, 2.85, 1.04, "ITCM", "128 KB\n0x8000_0000", FILL_VIOLET, VIOLET, fs=10.1)
    box(ax, 13.00, 6.18, 2.85, 1.04, "DTCM", "64 KB\n0x9000_0000", FILL_VIOLET, VIOLET, fs=10.1)

    # Peripheral row is below the bus. This prevents the CLINT, boot ROM, and
    # UART branches from visually overlapping the E203, NICE, and TCM paths.
    box(ax, 0.9, 1.95, 2.7, 0.85, "CLINT / PLIC", "interrupt subsystem", FILL_GRAY, LINE, fs=10.5)
    box(ax, 5.25, 1.95, 2.7, 0.85, "Boot ROM", "0x0000_0000", FILL_GRAY, LINE, fs=10.5)
    box(ax, 10.0, 1.95, 3.4, 0.85, "UART0 + GPIO", "board evidence output", FILL_GRAY, LINE, fs=10.5)

    # Central bus rail. Each branch is a distinct, non-overlapping orthogonal
    # segment with clear white space between the module and the fabric.
    bus_y = 3.55
    box(ax, 0.7, bus_y, 15.15, 0.46, "AHB system bus fabric", fc="#D9E2EC", ec=LINE, fs=10)
    bus_top = bus_y + 0.46
    bus_bottom = bus_y
    for x, y0 in [(2.20, 5.30), (11.22, 6.18), (14.42, 6.18)]:
        ax.plot([x, x], [bus_top, y0], color=LINE, linewidth=1.15, zorder=0)
    for x, y1 in [(2.25, 2.80), (6.60, 2.80), (11.70, 2.80)]:
        ax.plot([x, x], [bus_bottom, y1], color=LINE, linewidth=1.15, zorder=0)

    ax.text(0.7, 0.62, "Design boundary: accelerator control uses NICE; firmware, memories, UART, and GPIO remain observable through the SoC bus.", fontsize=10.2, color=INK)
    save(fig, "fig3_1_soc_architecture.png")


def fig3_3_pe_microarchitecture():
    fig, ax = setup(figsize=(8.8, 6.2), xlim=(0, 12), ylim=(0, 9))
    title(ax, "Processing element microarchitecture", "One PE performs signed INT8 multiply-accumulate into an INT32 output register.")

    box(ax, 4.1, 6.10, 3.8, 0.95, "INT8 signed multiplier", "W[7:0] x D[7:0] -> P[15:0]", FILL_BLUE, BLUE, fs=11)
    box(ax, 4.1, 4.55, 3.8, 0.90, "Control gate", "enable / clear / optional ReLU", FILL_RED, RED, fs=11)
    box(ax, 4.1, 2.85, 3.8, 1.05, "INT32 accumulator", "acc <= acc + sign_extend(P)", FILL_AMBER, AMBER, fs=11)

    ax.text(6.0, 7.80, "weight W", ha="center", fontsize=10.5, color=BLUE, fontweight="bold")
    arrow(ax, (6.0, 7.58), (6.0, 7.08), BLUE, lw=1.6)
    ax.text(1.45, 6.55, "activation D", ha="center", fontsize=10.5, color=GREEN, fontweight="bold")
    arrow(ax, (2.25, 6.55), (4.05, 6.55), GREEN, lw=1.6)
    arrow(ax, (6.0, 6.08), (6.0, 5.48), LINE)
    arrow(ax, (6.0, 4.52), (6.0, 3.92), LINE)
    arrow(ax, (6.0, 2.82), (6.0, 2.10), LINE)
    ax.text(6.0, 1.78, "result (INT32)", ha="center", fontsize=10.5, fontweight="bold")

    single_label_box(ax, 0.9, 3.35, 2.1, 1.45, "PE control\nacc_clr\nen_relu\nen", "#F8FAFC", LINE, fs=9.8)
    arrow(ax, (3.05, 4.05), (4.05, 4.05), LINE)

    # Feedback path is routed outside the processing boxes.
    ax.plot([8.02, 9.35, 9.35, 8.02], [3.38, 3.38, 6.55, 6.55], color=AMBER, linewidth=1.6)
    arrow(ax, (9.35, 6.55), (8.02, 6.55), AMBER, lw=1.6)
    ax.text(9.62, 4.95, "MAC\nfeedback", ha="center", va="center", fontsize=9.5, color=AMBER, fontweight="bold")

    save(fig, "fig3_3_pe_microarchitecture.png")


def fig3_4_pe_array():
    fig, ax = setup(figsize=(10.4, 5.4), xlim=(0, 15), ylim=(0.55, 8.05))
    title(ax, "4x4 PE array datapath", "WLOAD broadcasts columns, DLOAD broadcasts rows, and COMP triggers parallel output-stationary MACs.")

    gx, gy = 4.0, 2.3
    cell_w, cell_h, gap = 1.15, 0.76, 0.28
    centers = {}
    for r in range(4):
        for c in range(4):
            x = gx + c * (cell_w + gap)
            y = gy + (3 - r) * (cell_h + gap)
            centers[(r, c)] = (x + cell_w / 2, y + cell_h / 2)
            box(ax, x, y, cell_w, cell_h, f"PE{r},{c}", fc=FILL_GREEN if (r + c) % 2 == 0 else "#F8FFFB", ec=GREEN, fs=9.5)

    # Column weight routes.
    for c in range(4):
        x = centers[(0, c)][0]
        ax.text(x, 7.42, f"W{c}", ha="center", fontsize=10, color=BLUE, fontweight="bold")
        arrow(ax, (x, 7.20), (x, 6.72), BLUE, lw=1.4)
        ax.plot([x, x], [2.05, 6.68], color=BLUE, linewidth=0.9, alpha=0.45, zorder=0)

    # Row activation routes stay outside labels.
    for r in range(4):
        y = centers[(r, 0)][1]
        ax.text(2.68, y, f"D{r}", ha="center", va="center", fontsize=10, color=GREEN, fontweight="bold")
        arrow(ax, (3.05, y), (3.95, y), GREEN, lw=1.4)
        ax.plot([3.95, centers[(r, 3)][0]], [y, y], color=GREEN, linewidth=0.9, alpha=0.45, zorder=0)

    box(ax, 0.40, 7.13, 2.10, 0.72, "WLOAD x4", "loads W0-W3", "#F8FBFF", BLUE, fs=9.2)
    box(ax, 0.40, 3.81, 2.10, 0.86, "DLOAD x4", "loads D0-D3", "#FBFFFC", GREEN, fs=9.2)

    # Output routes are drawn below the array and collected at the right side,
    # so the readback wiring never crosses PE labels.
    merge_x = 11.15
    collector_x = 10.55
    single_label_box(ax, merge_x, 3.83, 1.95, 1.30, "reduction\nreadback", FILL_AMBER, AMBER, fs=10.3)
    for c in range(4):
        x0 = centers[(3, c)][0]
        y0 = 1.40 - c * 0.18
        ax.plot([x0, x0, collector_x], [2.22, y0, y0], color=LINE, linewidth=0.8, alpha=0.75, zorder=0)
    ax.plot([collector_x, collector_x, merge_x], [0.86, 4.48, 4.48], color=LINE, linewidth=0.9, alpha=0.75, zorder=0)
    arrow(ax, (13.12, 4.48), (13.85, 4.48), LINE, lw=1.4)
    ax.text(13.98, 4.48, "RSTAT", va="center", fontsize=10.5, fontweight="bold")
    box(ax, 10.35, 6.10, 3.3, 0.88, "COMP", "parallel INT32 accumulation", "#FFFDF7", AMBER, fs=10)

    save(fig, "fig3_4_pe_array.png")


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating clean architecture diagrams...")
    # Figures 3.1 and 3.3 are maintained from the author's SVG drawings.
    fig3_4_pe_array()
    print("Done.")


if __name__ == "__main__":
    main()
