"""
Fig 3.4: 4x4 PE Systolic Array — precise rendering with matplotlib
Matches AI reference exactly: 4x4 PE grid, W top→down (dashed), D left→right (solid),
Tree Adder with horizontal bus, Result (INT32).
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

matplotlib.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

N = 4
pe_w, pe_h = 1.0, 0.7
gap_x, gap_y = 0.25, 0.2

total_w = N * pe_w + (N - 1) * gap_x
total_h = N * pe_h + (N - 1) * gap_y

fig, ax = plt.subplots(figsize=(10, 9))
ax.set_xlim(-1.5, total_w + 0.5)
ax.set_ylim(-0.5, total_h + 3.0)
ax.set_aspect("equal")
ax.axis("off")

pe_color = "white"
pe_edge = "#333333"
adder_color = "#FFF9C4"


def draw_arrow(x1, y1, x2, y2, dashed=False, color="#555555", lw=0.8):
    style = "Simple, tail_width=0.5, head_width=4, head_length=5"
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color,
                                linestyle="--" if dashed else "-",
                                linewidth=lw))


def draw_pe(x, y):
    rect = mpatches.FancyBboxPatch(
        (x, y), pe_w, pe_h, boxstyle="round,pad=0.02",
        facecolor=pe_color, edgecolor=pe_edge, linewidth=1.2
    )
    ax.add_patch(rect)
    ax.text(x + pe_w / 2, y + pe_h / 2, "PE",
            ha="center", va="center", fontsize=9, fontweight="bold", color="#333333")


# Compute PE centers
pe_cx = {}  # (row, col) → center (x, y)
for r in range(N):
    py = (N - 1 - r) * (pe_h + gap_y) + 1.5  # row 0 at top
    for c in range(N):
        px = c * (pe_w + gap_x)
        draw_pe(px, py)
        pe_cx[(r, c)] = (px + pe_w / 2, py + pe_h / 2)

# ── W[0..3] at TOP, dashed arrows down ──
for c in range(N):
    px = c * (pe_w + gap_x) + pe_w / 2
    top_y = pe_cx[(0, c)][1] + pe_h / 2
    wy = top_y + 0.6
    ax.text(px, wy + 0.12, f"W[{c}]", ha="center", va="bottom", fontsize=10, fontweight="bold", color="#333")
    draw_arrow(px, wy, px, top_y, dashed=True, color="#888888", lw=0.8)

# ── D[0..3] at LEFT, dashed arrows to first PE, solid between PEs ──
for r in range(N):
    py = pe_cx[(r, 0)][1]
    left_x = pe_cx[(r, 0)][0] - pe_w / 2
    dx = left_x - 0.8
    ax.text(dx - 0.12, py, f"D[{r}]", ha="right", va="center", fontsize=10, fontweight="bold", color="#333")
    draw_arrow(dx, py, left_x, py, dashed=True, color="#888888", lw=0.8)

# ── Intra-column: dashed (W flow, down) ──
for c in range(N):
    for r in range(N - 1):
        p1 = pe_cx[(r, c)]
        p2 = pe_cx[(r + 1, c)]
        draw_arrow(p1[0], p1[1] - pe_h / 2 - 0.02, p2[0], p2[1] + pe_h / 2 + 0.02, dashed=True, color="#888888", lw=0.8)

# ── Intra-row: solid (D flow, right) ──
for r in range(N):
    for c in range(N - 1):
        p1 = pe_cx[(r, c)]
        p2 = pe_cx[(r, c + 1)]
        draw_arrow(p1[0] + pe_w / 2 + 0.02, p1[1], p2[0] - pe_w / 2 - 0.02, p2[1], dashed=False, color="#555555", lw=1.0)

# ── Tree Adder ──
bottom_y = pe_cx[(N - 1, 0)][1] - pe_h / 2
adder_top = bottom_y - 1.0
adder_h = 0.5
adder_w = total_w * 0.85
adder_x = (total_w - adder_w) / 2

# Horizontal bus line
bus_y = adder_top + adder_h + 0.3

# Vertical lines from each PE to bus
for r in range(N):
    for c in range(N):
        px = pe_cx[(r, c)][0]
        pe_bottom = pe_cx[(r, c)][1] - pe_h / 2
        ax.plot([px, px], [pe_bottom, bus_y], color="#999999", linewidth=0.6)
        # small arrowhead
        ax.plot(px, bus_y, marker="v", markersize=5, color="#999999",
                clip_on=False)

# Horizontal bus
ax.plot([adder_x - 0.2, adder_x + adder_w + 0.2], [bus_y, bus_y],
        color="#555555", linewidth=1.2)

# Center arrow bus → Tree Adder
center_x = total_w / 2
draw_arrow(center_x, bus_y, center_x, adder_top + adder_h, color="#555555", lw=1.0)

# Adder box
rect = mpatches.FancyBboxPatch(
    (adder_x, adder_top), adder_w, adder_h,
    boxstyle="round,pad=0.03",
    facecolor=adder_color, edgecolor="#333333", linewidth=1.5
)
ax.add_patch(rect)
ax.text(adder_x + adder_w / 2, adder_top + adder_h / 2,
        "Tree Adder (16-input)",
        ha="center", va="center", fontsize=10, fontweight="bold", color="#333333")

# ── Result (INT32) ──
result_y = adder_top - 0.7
draw_arrow(center_x, adder_top, center_x, result_y + 0.15, color="#555555", lw=1.0)
ax.text(center_x, result_y, "Result (INT32)",
        ha="center", va="top", fontsize=10, fontweight="bold", color="#333333")

plt.tight_layout()
out = r"C:\Users\16084\Desktop\fig3_4_pe_array.png"
plt.savefig(out, facecolor="white", edgecolor="none")
print(f"[OK] Saved: {out}")
