"""
Generate remaining professional figures:
- Fig 3.5: Packed INT8 data format
- Fig 3.6: FPGA build pipeline
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

FIG_DIR = r'C:\Users\16084\Documents\Graduation_Design_Library\09_Thesis_Writing\Figures'

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 9,
    'figure.dpi': 150, 'savefig.dpi': 150,
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.1,
})

# ================================================================
# Fig 3.5: Packed INT8 Data Format
# ================================================================
print("Generating Fig 3.5: Packed INT8 format...")

fig, ax = plt.subplots(figsize=(7, 2.2))
ax.set_xlim(-0.5, 33)
ax.set_ylim(0, 4.5)
ax.axis('off')

# 32-bit word: 4 x INT8
fields = [
    (31, 24, 'Value [3]', 'INT8', '#E3F2FD'),
    (23, 16, 'Value [2]', 'INT8', '#BBDEFB'),
    (15,  8, 'Value [1]', 'INT8', '#90CAF9'),
    (7,   0, 'Value [0]', 'INT8', '#64B5F6'),
]

box_height = 1.2
box_y = 2.0

for start, end, label, sublabel, color in fields:
    width = start - end + 1
    x = end
    rect = FancyBboxPatch((x, box_y), width, box_height,
                          boxstyle="round,pad=0.08",
                          facecolor=color, edgecolor='#37474F', linewidth=1.2)
    ax.add_patch(rect)
    ax.text(x + width/2, box_y + box_height - 0.35, label, ha='center', va='center',
            fontsize=9, fontweight='bold', color='#263238')
    ax.text(x + width/2, box_y + 0.35, sublabel, ha='center', va='center',
            fontsize=8, color='#546E7A')
    ax.text(x, box_y - 0.15, str(end), ha='center', va='top', fontsize=7, color='#37474F')
    ax.text(x + width, box_y - 0.15, str(start), ha='center', va='top', fontsize=7, color='#37474F')

# Ruler
for i in range(32):
    ax.plot([i, i], [box_y + box_height + 0.1, box_y + box_height + 0.3], 'k-', linewidth=0.3, alpha=0.5)
    if i % 4 == 0:
        ax.text(i, box_y + box_height + 0.4, str(i), ha='center', va='bottom', fontsize=6.5, color='#546E7A')

# Example below
example_y = 0.6
ax.text(16, example_y + 0.3,
        'Example: WLOAD(column=1, w3=0x12, w2=0x34, w1=0xAB, w0=0xCD) → rs1 = 0x1234ABCD',
        ha='center', fontsize=8.5, family='monospace', color='#1565C0')
ax.text(16, example_y - 0.1,
        'Each WLOAD/DLOAD packs 4×INT8 into one 32-bit register, transferred via the NICE rs1 operand.',
        ha='center', fontsize=8, style='italic', color='#546E7A')

ax.set_title('Packed INT8 Data Format for WLOAD/DLOAD Instructions', fontsize=11, fontweight='bold', y=1.02)
plt.tight_layout()
out_path = os.path.join(FIG_DIR, 'fig3_5_packed_format.png')
plt.savefig(out_path, bbox_inches='tight', dpi=150)
plt.close()
print(f"  Saved: {out_path}")


# ================================================================
# Fig 3.6: FPGA Build Pipeline
# ================================================================
print("Generating Fig 3.6: FPGA build pipeline...")

fig, ax = plt.subplots(figsize=(6.5, 3.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis('off')

# Pipeline stages
stages = [
    (0.5, 5.5, 'C/C++ Source\n(.c / .S)', '#E3F2FD', 'GCC RISC-V\nToolchain'),
    (0.5, 4.2, 'ELF Binary\n(.elf)', '#BBDEFB', 'objcopy'),
    (0.5, 2.9, 'Verilog Hex\n(.verilog)', '#90CAF9', ''),
    (3.5, 5.5, 'RTL Source\n(.v / .sv)', '#FFF3E0', 'Vivado\nSynthesis'),
    (3.5, 4.2, 'Gate Netlist\n(.edf)', '#FFE0B2', 'Vivado\nImplementation'),
    (3.5, 2.9, 'Routed Design\n(.dcp)', '#FFCC80', ''),
    (6.5, 4.5, 'Bitstream\n(.bit)', '#E8F5E9', 'Vivado\nBitGen'),
    (6.5, 2.9, 'Debug Probes\n(.ltx)', '#C8E6C9', ''),
]

# Draw stage boxes
for x, y, label, color, tool in stages:
    w, h = 2.3, 1.0
    if 'Bitstream' in label:
        w, h = 2.3, 1.5
    if 'Debug Probes' in label:
        w, h = 2.3, 1.2

    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.08",
                          facecolor=color, edgecolor='#546E7A', linewidth=1.0)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, label, ha='center', va='center',
            fontsize=8, fontweight='bold', color='#263238')
    if tool:
        ax.text(x + w/2, y - 0.25, tool, ha='center', va='top', fontsize=6.5, color='#78909C', style='italic')

# Arrows between stages
# SW flow (left side, vertical)
arrow_y_pairs = [(5.5, 5.2), (4.2, 3.9)]
for y1, y2 in arrow_y_pairs:
    ax.annotate('', xy=(1.65, y2), xytext=(1.65, y1),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))

# HW flow (center, vertical)
for y1, y2 in [(5.5, 5.2), (4.2, 3.9)]:
    ax.annotate('', xy=(4.65, y2), xytext=(4.65, y1),
                arrowprops=dict(arrowstyle='->', color='#E65100', lw=1.5))

# SW → HW → Bitstream flow (horizontal merge)
ax.annotate('', xy=(6.5, 3.5), xytext=(5.8, 3.5),
            arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2.0))
ax.annotate('', xy=(7.0, 4.5), xytext=(5.8, 3.5),
            arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2.0))

# Merge label
ax.text(5.5, 3.9, 'Merge', ha='center', fontsize=7, color='#2E7D32', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#2E7D32', alpha=0.8))

# Labels for tracks
ax.text(1.65, 6.2, 'Software Track', ha='center', fontsize=9, fontweight='bold', color='#1565C0')
ax.text(4.65, 6.2, 'Hardware Track', ha='center', fontsize=9, fontweight='bold', color='#E65100')

# Bottom: board
rect = FancyBboxPatch((0.5, 0.5), 8.3, 1.5,
                      boxstyle="round,pad=0.1",
                      facecolor='#ECEFF1', edgecolor='#37474F', linewidth=1.5)
ax.add_patch(rect)
ax.text(4.65, 1.7, 'FPGA Board (Davinci Pro A7-100T)', ha='center', fontsize=10, fontweight='bold', color='#263238')
ax.text(4.65, 1.2, 'Program via JTAG  →  ILA Capture  →  UART Output  →  LED Status',
        ha='center', fontsize=8, color='#546E7A')

# Arrow to board
ax.annotate('', xy=(7.65, 2.0), xytext=(7.65, 2.9),
            arrowprops=dict(arrowstyle='->', color='#37474F', lw=1.8))

# Feedback loop
ax.annotate('Debug Loop', xy=(0.3, 1.2), xytext=(0.3, 5.0),
            arrowprops=dict(arrowstyle='->', color='#F44336', lw=1.2,
                          connectionstyle='arc3,rad=-0.4'),
            fontsize=7, color='#F44336', ha='center')

ax.set_title('FPGA Build and Verification Pipeline', fontsize=12, fontweight='bold', y=1.02)
plt.tight_layout()
out_path = os.path.join(FIG_DIR, 'fig3_6_build_pipeline.png')
plt.savefig(out_path, bbox_inches='tight', dpi=150)
plt.close()
print(f"  Saved: {out_path}")

print("\nDone!")
