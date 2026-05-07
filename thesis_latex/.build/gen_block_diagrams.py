"""
Generate professional block diagrams for thesis — FIXED VERSION.
- Fig 3.1: System Architecture (fixed line routing, bidirectional NICE arrow)
- Fig 3.3: PE Microarchitecture (fixed ReLU placement, no text overlap)
- Fig 3.4: PE Array
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

FIG_DIR = r"C:\Users\16084\Documents\Graduation_Design_Library\thesis_latex\figures"

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 9,
    'figure.dpi': 200, 'savefig.dpi': 200,
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.05,
})

def draw_block(ax, x, y, w, h, text, color, fontsize=8, fontweight='bold'):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                          facecolor=color, edgecolor='#37474F', linewidth=1.0)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, fontweight=fontweight, color='#263238')
    return rect

def draw_label(ax, x, y, text, fontsize=7, color='#37474F', ha='center'):
    ax.text(x, y, text, ha=ha, va='center', fontsize=fontsize, color=color)

def draw_arrow(ax, x1, y1, x2, y2, color='#37474F', lw=1.0, style='->'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))

# ================================================================
# Fig 3.1: System Architecture (COMPLETELY REWRITTEN)
# ================================================================
print("Generating Fig 3.1: System Architecture...")

fig, ax = plt.subplots(figsize=(8.5, 5.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis('off')

CPU_C = '#E3F2FD'; ACC_C = '#E8F5E9'; MEM_C = '#F3E5F5'; IO_C = '#ECEFF1'
BUS_C = '#B0BEC5'; NICE_C = '#E65100'; LINE_C = '#546E7A'
INNER_CPU = '#90CAF9'; INNER_ACC = '#A5D6A7'

# ---- CPU Block (left) ----
draw_block(ax, 0.4, 2.6, 3.2, 3.8, '', CPU_C)
draw_block(ax, 0.6, 5.3, 2.8, 0.85, 'E203 RISC-V Core\n(RV32IMAC)', CPU_C, 9)
draw_label(ax, 2.0, 5.05, '2-stage pipeline, Machine Mode', 6.5, '#37474F')
draw_block(ax, 1.0, 4.1, 2.2, 0.55, 'IFU (Instruction Fetch)', INNER_CPU, 7)
draw_block(ax, 1.0, 3.1, 2.2, 0.55, 'EXU (Execute + NICE)', INNER_CPU, 7)

# ---- Accelerator Block (middle) ----
draw_block(ax, 4.3, 2.6, 2.7, 3.8, '', ACC_C)
draw_block(ax, 4.5, 5.3, 2.3, 0.85, 'CNN Accelerator', ACC_C, 9)
draw_label(ax, 5.65, 5.05, 'NICE Interface', 6.5, '#1B5E20')
draw_block(ax, 4.7, 4.1, 1.9, 0.55, 'NICE Decoder\n+ Control FSM', INNER_ACC, 7)
draw_block(ax, 4.7, 3.1, 1.9, 0.55, '4x4 PE Array\n(INT8 MAC)', INNER_ACC, 7)

# ---- Memory (right top) ----
draw_block(ax, 7.7, 4.2, 2.5, 2.2, '', MEM_C)
draw_block(ax, 7.85, 5.15, 2.2, 1.0, 'ITCM 128KB (64-bit)\n@ 0x8000_0000', MEM_C, 7.5)
draw_block(ax, 7.85, 4.35, 2.2, 0.55, 'DTCM 64KB\n@ 0x9000_0000', '#CE93D8', 7)

# ---- IO (right bottom) ----
draw_block(ax, 7.7, 1.2, 2.5, 1.6, '', IO_C)
draw_block(ax, 7.85, 2.05, 2.2, 0.50, 'UART0\n@ 0x1001_3000', IO_C, 7)
draw_block(ax, 7.85, 1.35, 2.2, 0.45, 'GPIO (LED, UART pins)', '#CFD8DC', 6.5)

# ---- AHB Bus (bottom) ----
draw_block(ax, 0.4, 0.15, 10.5, 0.40, 'AHB Bus Fabric', BUS_C, 8, 'bold')

# ---- Peripherals ABOVE bus with vertical drops ----
peri_y = 0.75
p_w, p_h = 1.6, 0.65
draw_block(ax, 1.0, peri_y, p_w, p_h, 'CLINT\n@0x0200_0000', IO_C, 7)
draw_block(ax, 3.2, peri_y, p_w, p_h, 'PLIC\n@0x0C00_0000', IO_C, 7)
draw_block(ax, 5.3, peri_y, 2.2, p_h, 'Boot ROM (MROM)\n@0x0000_0000', IO_C, 7)

# Peripheral → bus vertical drops
for px in [1.8, 4.0, 6.4]:
    draw_arrow(ax, px, peri_y - 0.05, px, 0.22, LINE_C, 2.5, "-")

# ---- NICE arrow: bidirectional between CPU EXU and Acc ----
# Gap between CPU (right edge x=3.6) and Acc (left edge x=4.3)
ax.annotate('', xy=(4.25, 3.375), xytext=(3.65, 3.375),
            arrowprops=dict(arrowstyle='<->', color=NICE_C, lw=5.0))
draw_label(ax, 3.95, 3.85, 'NICE Req / Rsp', 9, NICE_C)

# ---- Bus connections: route through gaps between peripherals ----
# Gaps: left[0.4-1.0], CLINT-PLIC[2.6-3.2], PLIC-BootROM[4.8-5.3], right[7.5-10.9]
# CPU → bus (through gap left of CLINT)
draw_arrow(ax, 0.8, 2.6, 0.8, 0.22, LINE_C, 2.5, '-')
# Acc → bus (through gap between PLIC and Boot ROM)
draw_arrow(ax, 5.05, 2.6, 5.05, 0.22, LINE_C, 2.5, '-')
# Memory → bus: horizontal stub from block edge, then vertical drop right of IO
ax.plot([10.2, 10.4], [4.2, 4.2], '-', color=LINE_C, lw=2.5)
draw_arrow(ax, 10.4, 4.2, 10.4, 0.22, LINE_C, 2.5, '-')
# IO → bus (through gap right of Boot ROM, left of memory drop)
draw_arrow(ax, 8.95, 1.2, 8.95, 0.22, LINE_C, 2.5, '-')

# ---- Title ----
draw_label(ax, 6.0, 7.6, 'E203 SoC with NICE CNN Accelerator — System Architecture', 11, '#263238')

plt.tight_layout()
out = os.path.join(FIG_DIR, 'fig3_1_soc_architecture.png')
plt.savefig(out, bbox_inches='tight', dpi=200)
plt.close()
print(f"  Saved: {out}")


# ================================================================
# Fig 3.3: PE Microarchitecture (FIXED: ReLU outs Multiplier)
# ================================================================
print("Generating Fig 3.3: PE Microarchitecture...")

fig, ax = plt.subplots(figsize=(5.5, 4.5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 8)
ax.axis('off')

# Layout (top to bottom): Input → Multiplier → ReLU → Accumulator → Result
# Multiplier: y=4.5, h=1.0
draw_block(ax, 3.0, 4.5, 4.5, 1.0,
           'INT8 Multiplier\n  W[7:0] × D[7:0] → P[15:0]', '#E3F2FD', 7.5)

# ReLU block: CLEARLY SEPARATE below multiplier
draw_block(ax, 3.0, 3.5, 4.5, 0.65,
           'ReLU (optional)\n  if en_relu && result < 0 then 0', '#FFEBEE', 7, 'normal')

# Accumulator: below ReLU
draw_block(ax, 3.0, 1.8, 4.5, 1.2,
           'INT32 Accumulator\n  acc ≤ acc + P (signed)\n  (reset on acc_clr)', '#FFF8E1', 7.5)

# ---- Inputs ----
# W input (top)
draw_label(ax, 5.25, 7.5, 'W (INT8, 8-bit signed weight)', 8, '#1565C0')
draw_arrow(ax, 5.25, 7.2, 5.25, 5.55, '#1565C0', 1.2)

# D input (left)
draw_label(ax, 1.3, 5.0, 'D\n(INT8,\n8-bit\nactivation)', 7.5, '#2E7D32')
draw_arrow(ax, 2.0, 5.3, 2.95, 5.0, '#2E7D32', 1.0)

# ---- Internal data flow arrows ----
# Multiplier → ReLU
draw_arrow(ax, 5.25, 4.5, 5.25, 4.2, '#37474F', 1.0)
# ReLU → Accumulator
draw_arrow(ax, 5.25, 3.5, 5.25, 3.05, '#37474F', 1.0)
# Accumulator → Result
draw_arrow(ax, 5.25, 1.8, 5.25, 0.3, '#37474F', 1.2)
draw_label(ax, 5.25, 0.15, 'Result (INT32)', 8, '#263238')

# ---- Feedback loop ----
ax.annotate('', xy=(8.5, 2.4), xytext=(8.5, 4.0),
            arrowprops=dict(arrowstyle='->', color='#E65100', lw=1.5,
                          connectionstyle='arc3,rad=0.6'))
draw_label(ax, 9.35, 3.2, 'accumulate', 6.5, '#E65100')

# ---- Control signals ----
draw_label(ax, 1.5, 2.8, 'acc_clr', 7, '#C62828')
draw_arrow(ax, 2.2, 2.8, 2.95, 2.4, '#C62828', 0.8)
draw_label(ax, 1.5, 2.2, 'en', 7, '#546E7A')
draw_arrow(ax, 2.4, 2.2, 2.95, 2.0, '#546E7A', 0.8)

# ---- Title ----
draw_label(ax, 5.5, 7.8, 'Processing Element (PE) Microarchitecture', 10, '#263238')

plt.tight_layout()
out = os.path.join(FIG_DIR, 'fig3_3_pe_microarchitecture.png')
plt.savefig(out, bbox_inches='tight', dpi=200)
plt.close()
print(f"  Saved: {out}")


# ================================================================
# Fig 3.4: 4x4 PE Array
# ================================================================
print("Generating Fig 3.4: PE Array...")

fig, ax = plt.subplots(figsize=(7, 5.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8.5)
ax.axis('off')

pe_w, pe_h = 1.4, 1.0
grid_x0, grid_y0 = 2.5, 2.5

for col in range(4):
    for row in range(4):
        x = grid_x0 + col * (pe_w + 0.2)
        y = grid_y0 + (3 - row) * (pe_h + 0.2)
        color = '#E8F5E9' if (col + row) % 2 == 0 else '#C8E6C9'
        draw_block(ax, x, y, pe_w, pe_h, f'PE{row},{col}', color, 8.5)

# Weight inputs (top) → flow DOWN (position ABOVE grid, not inside top row)
for col in range(4):
    x = grid_x0 + col * (pe_w + 0.2) + pe_w/2
    grid_top = grid_y0 + 4*(pe_h+0.2) - 0.2
    draw_label(ax, x, grid_top + 0.35, f'W[{col}]', 7.5, '#1565C0')
    draw_arrow(ax, x, grid_top + 0.05, x, grid_top - 0.05, '#1565C0', 0.8)

# Weight broadcast arrows (along left of each column)
for col in range(4):
    x = grid_x0 + col * (pe_w + 0.2) + pe_w + 0.08
    y_top = grid_y0 + 3*(pe_h+0.2) + pe_h
    draw_arrow(ax, x, y_top, x, grid_y0 - 0.1, '#1565C0', 0.4, '-')

# Activation inputs (left) → flow RIGHT
for row in range(4):
    y = grid_y0 + (3 - row) * (pe_h + 0.2) + pe_h/2
    draw_label(ax, grid_x0 - 1.2, y, f'D[{row}]', 8, '#2E7D32')
    draw_arrow(ax, grid_x0 - 0.3, y, grid_x0 - 0.05, y, '#2E7D32', 0.8)

# Activation flow arrows
for row in range(4):
    y = grid_y0 + (3 - row) * (pe_h + 0.2) + pe_h + 0.08
    draw_arrow(ax, grid_x0 - 0.1, y, grid_x0 + 4*(pe_w+0.2), y, '#2E7D32', 0.4, '-')

# Results → Tree adder
tree_x = grid_x0 + 4*(pe_w+0.2) + 1.5
tree_y = grid_y0 + 1.5*(pe_h+0.2)
for col in range(4):
    x = grid_x0 + col * (pe_w + 0.2) + pe_w/2
    draw_arrow(ax, x, grid_y0 - 0.1, x, grid_y0 - 0.5, '#37474F', 0.6)
    ax.plot([x, tree_x - 0.5], [grid_y0 - 0.5, grid_y0 - 0.5], '-', lw=0.4, color='#78909C')
    ax.plot([tree_x - 0.5, tree_x - 0.5], [grid_y0 - 0.5, tree_y + 0.7], '-', lw=0.4, color='#78909C')

draw_block(ax, tree_x - 0.8, tree_y, 1.6, 0.7, 'Tree\nAdder', '#FFF3E0', 7.5)
draw_arrow(ax, tree_x, tree_y, tree_x, tree_y - 0.5, '#37474F', 1.0)
draw_label(ax, tree_x, tree_y - 0.7, 'Result (INT32)', 8, '#263238')

draw_label(ax, 6, 8.2, '4×4 Systolic Processing Element Array', 10, '#263238')
draw_label(ax, 6, 7.85, 'Output-Stationary Dataflow', 7.5, '#546E7A')

plt.tight_layout()
out = os.path.join(FIG_DIR, 'fig3_4_pe_array.png')
plt.savefig(out, bbox_inches='tight', dpi=200)
plt.close()
print(f"  Saved: {out}")

print("\nAll 3 diagrams regenerated!")
