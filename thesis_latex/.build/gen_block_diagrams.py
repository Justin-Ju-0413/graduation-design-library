"""Generate thesis block diagrams with a consistent academic style."""
from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(ROOT, "figures")

COLORS = {
    "ink": "#1F2933",
    "muted": "#5B6773",
    "line": "#64748B",
    "blue": "#D7E8FF",
    "blue_edge": "#2F6FB3",
    "green": "#DDF4E7",
    "green_edge": "#23835A",
    "amber": "#FFF0C2",
    "amber_edge": "#B7791F",
    "violet": "#E9E2FF",
    "violet_edge": "#6B46C1",
    "gray": "#EEF2F6",
    "gray_edge": "#64748B",
    "red": "#FDE2E2",
    "red_edge": "#B42318",
}

plt.rcParams.update(
    {
        "font.family": "DejaVu Serif",
        "font.size": 10,
        "figure.dpi": 220,
        "savefig.dpi": 260,
        "axes.edgecolor": COLORS["line"],
        "text.color": COLORS["ink"],
    }
)


def setup_ax(figsize=(9, 5.4), xlim=(0, 12), ylim=(0, 7.2)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, label, fc, ec=None, fs=9, weight="bold", lw=1.4):
    ec = ec or COLORS["line"]
    rect = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, fontweight=weight)
    return rect


def arrow(ax, start, end, color=None, lw=1.6, style="-|>", rad=0):
    color = color or COLORS["line"]
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=style,
            mutation_scale=12,
            linewidth=lw,
            color=color,
            connectionstyle=f"arc3,rad={rad}",
            shrinkA=2,
            shrinkB=2,
        )
    )


def fig3_1_soc_architecture():
    fig, ax = setup_ax(figsize=(9.5, 5.6), ylim=(0, 7.4))

    ax.text(0.15, 7.05, "E203 SoC with NICE CNN Accelerator", fontsize=15, fontweight="bold")
    ax.text(0.15, 6.72, "Custom instructions carry control and operands; standard bus fabric connects memory and I/O.", fontsize=8.5, color=COLORS["muted"])

    box(ax, 0.45, 3.2, 2.6, 2.65, "E203 Core\nRV32IMAC\n2-stage pipeline", COLORS["blue"], COLORS["blue_edge"], fs=9.5)
    box(ax, 0.75, 4.35, 2.0, 0.42, "IFU", "#F8FBFF", COLORS["blue_edge"], fs=8)
    box(ax, 0.75, 3.72, 2.0, 0.42, "EXU + NICE dispatch", "#F8FBFF", COLORS["blue_edge"], fs=8)

    box(ax, 4.15, 3.2, 2.6, 2.65, "CNN Accelerator\n4x4 INT8 PE array", COLORS["green"], COLORS["green_edge"], fs=9.5)
    box(ax, 4.45, 4.42, 2.0, 0.42, "NICE decoder + FSM", "#FBFFFC", COLORS["green_edge"], fs=8)
    box(ax, 4.45, 3.78, 2.0, 0.42, "Register-fed MAC array", "#FBFFFC", COLORS["green_edge"], fs=8)

    box(ax, 8.0, 4.65, 2.75, 1.0, "ITCM 128 KB\n0x8000_0000", COLORS["violet"], COLORS["violet_edge"], fs=8.5)
    box(ax, 8.0, 3.38, 2.75, 1.0, "DTCM 64 KB\n0x9000_0000", COLORS["violet"], COLORS["violet_edge"], fs=8.5)
    box(ax, 8.0, 1.45, 2.75, 1.0, "UART0 + GPIO\nboard evidence output", COLORS["gray"], COLORS["gray_edge"], fs=8.5)
    box(ax, 4.6, 1.45, 1.9, 1.0, "Boot ROM\n0x0000_0000", COLORS["gray"], COLORS["gray_edge"], fs=8.5)
    box(ax, 0.7, 1.45, 2.2, 1.0, "CLINT / PLIC\ninterrupt system", COLORS["gray"], COLORS["gray_edge"], fs=8.5)

    box(ax, 0.45, 0.45, 10.3, 0.38, "AHB system bus fabric", "#D9E2EC", COLORS["gray_edge"], fs=8.5)

    arrow(ax, (3.08, 4.35), (4.10, 4.35), COLORS["amber_edge"], lw=3.0, style="<|-|>")
    ax.text(3.59, 4.63, "NICE request / response", ha="center", fontsize=8.5, color=COLORS["amber_edge"], fontweight="bold")

    for x in [1.8, 5.55, 9.35]:
        arrow(ax, (x, 1.42), (x, 0.86), COLORS["line"], style="-")
    arrow(ax, (1.75, 3.17), (1.75, 0.86), COLORS["line"], style="-")
    arrow(ax, (5.45, 3.17), (5.45, 0.86), COLORS["line"], style="-")
    arrow(ax, (9.35, 3.35), (9.35, 0.86), COLORS["line"], style="-")
    arrow(ax, (9.35, 1.42), (9.35, 0.86), COLORS["line"], style="-")

    out = os.path.join(FIG_DIR, "fig3_1_soc_architecture.png")
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved {out}")


def fig3_3_pe_microarchitecture():
    fig, ax = setup_ax(figsize=(7.0, 5.0), xlim=(0, 10), ylim=(0, 7.2))

    ax.text(0.2, 6.82, "Processing Element Microarchitecture", fontsize=15, fontweight="bold")
    ax.text(0.2, 6.48, "Each PE multiplies one INT8 weight and activation, then accumulates into an INT32 output.", fontsize=8.5, color=COLORS["muted"])

    box(ax, 3.05, 4.75, 3.9, 0.72, "INT8 signed multiplier\nW[7:0] x D[7:0] -> P[15:0]", COLORS["blue"], COLORS["blue_edge"], fs=8.5)
    box(ax, 3.05, 3.62, 3.9, 0.62, "Optional ReLU gate\napplied after accumulation path control", COLORS["red"], COLORS["red_edge"], fs=8)
    box(ax, 3.05, 2.10, 3.9, 0.92, "INT32 accumulator\nacc <= acc + sign_extend(P)", COLORS["amber"], COLORS["amber_edge"], fs=8.5)

    ax.text(4.98, 6.0, "Weight W", ha="center", fontsize=8.5, color=COLORS["blue_edge"], fontweight="bold")
    arrow(ax, (4.98, 5.92), (4.98, 5.49), COLORS["blue_edge"])
    ax.text(1.24, 5.06, "Activation D", ha="center", fontsize=8.5, color=COLORS["green_edge"], fontweight="bold")
    arrow(ax, (1.92, 5.06), (3.02, 5.06), COLORS["green_edge"])
    arrow(ax, (4.98, 4.73), (4.98, 4.27), COLORS["line"])
    arrow(ax, (4.98, 3.59), (4.98, 3.05), COLORS["line"])
    arrow(ax, (4.98, 2.08), (4.98, 1.33), COLORS["line"])
    ax.text(4.98, 1.06, "Result (INT32)", ha="center", fontsize=8.5, fontweight="bold")

    arrow(ax, (7.03, 2.58), (8.05, 3.5), COLORS["amber_edge"], rad=0.28)
    arrow(ax, (8.05, 3.5), (6.95, 4.05), COLORS["amber_edge"], rad=0.25)
    ax.text(8.24, 3.25, "feedback\nfor MAC", fontsize=7.5, color=COLORS["amber_edge"], ha="center")

    box(ax, 0.62, 2.0, 1.75, 1.08, "Control\nacc_clr\nen_relu\nen", "#F8FAFC", COLORS["gray_edge"], fs=8, weight="normal")
    arrow(ax, (2.38, 2.55), (3.02, 2.55), COLORS["gray_edge"])

    out = os.path.join(FIG_DIR, "fig3_3_pe_microarchitecture.png")
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved {out}")


def fig3_4_pe_array():
    fig, ax = setup_ax(figsize=(8.2, 5.4), xlim=(0, 12), ylim=(0, 7.4))

    ax.text(0.2, 7.0, "4x4 Systolic PE Array", fontsize=15, fontweight="bold")
    ax.text(0.2, 6.66, "Four WLOAD and four DLOAD instructions populate the array before COMP triggers parallel MACs.", fontsize=8.5, color=COLORS["muted"])

    gx, gy = 3.05, 1.9
    w, h, gap = 1.15, 0.72, 0.22
    for r in range(4):
        for c in range(4):
            x = gx + c * (w + gap)
            y = gy + (3 - r) * (h + gap)
            fc = "#F8FFFB" if (r + c) % 2 else COLORS["green"]
            box(ax, x, y, w, h, f"PE{r},{c}", fc, COLORS["green_edge"], fs=8)

    for c in range(4):
        x = gx + c * (w + gap) + w / 2
        ax.text(x, 6.02, f"W{c}", ha="center", fontsize=8.5, color=COLORS["blue_edge"], fontweight="bold")
        arrow(ax, (x, 5.78), (x, 5.38), COLORS["blue_edge"])
        ax.plot([x, x], [1.74, 5.34], color=COLORS["blue_edge"], linewidth=0.8, alpha=0.65)

    for r in range(4):
        y = gy + (3 - r) * (h + gap) + h / 2
        ax.text(1.82, y, f"D{r}", ha="center", va="center", fontsize=8.5, color=COLORS["green_edge"], fontweight="bold")
        arrow(ax, (2.14, y), (2.98, y), COLORS["green_edge"])
        ax.plot([2.98, 8.6], [y, y], color=COLORS["green_edge"], linewidth=0.8, alpha=0.6)

    box(ax, 9.0, 2.88, 1.55, 1.05, "tree\nadder", COLORS["amber"], COLORS["amber_edge"], fs=8.5)
    for c in range(4):
        x = gx + c * (w + gap) + w / 2
        ax.plot([x, x, 8.85], [1.78, 1.35 + c * 0.18, 3.40], color=COLORS["line"], linewidth=0.55, alpha=0.75)
    arrow(ax, (10.55, 3.40), (11.28, 3.40), COLORS["line"])
    ax.text(11.34, 3.40, "RSTAT", va="center", fontsize=8.5, fontweight="bold")

    box(ax, 0.65, 4.75, 1.75, 0.78, "WLOAD x4\ncolumns", "#F8FBFF", COLORS["blue_edge"], fs=8, weight="normal")
    box(ax, 0.65, 1.50, 1.75, 0.78, "DLOAD x4\nrows", "#FBFFFC", COLORS["green_edge"], fs=8, weight="normal")
    box(ax, 8.75, 4.92, 2.2, 0.66, "Output-stationary\nINT32 accumulation", "#FFFDF7", COLORS["amber_edge"], fs=8, weight="normal")

    out = os.path.join(FIG_DIR, "fig3_4_pe_array.png")
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved {out}")


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    print("Generating academic block diagrams...")
    fig3_1_soc_architecture()
    fig3_3_pe_microarchitecture()
    fig3_4_pe_array()
    print("Done.")


if __name__ == "__main__":
    main()
