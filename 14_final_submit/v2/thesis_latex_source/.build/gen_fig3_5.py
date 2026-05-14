"""Generate Figure 3.5: Packed INT8 Data Format (fixed ticks)"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

FIG_DIR = r"C:\Users\16084\Documents\Graduation_Design_Library\thesis_latex\figures"

plt.rcParams.update({'font.family': 'serif', 'font.size': 11, 'figure.dpi': 200})

fig, ax = plt.subplots(figsize=(10, 3.5))
ax.set_xlim(0, 14)
ax.set_ylim(0, 4.5)
ax.axis('off')

# Draw 32-bit register bar
bar_y, bar_h = 2.0, 1.2
colors = ['#E3F2FD', '#C8E6C9', '#FFF3E0', '#FFCDD2']
labels = ['Value[3] (INT8)\n[31:24]', 'Value[2] (INT8)\n[23:16]',
          'Value[1] (INT8)\n[15:8]', 'Value[0] (INT8)\n[7:0]']

for i, (label, color) in enumerate(zip(labels, colors)):
    x = 1.5 + i * 2.8
    w = 2.6
    rect = FancyBboxPatch((x, bar_y), w, bar_h, boxstyle="round,pad=0.08",
                          facecolor=color, edgecolor='#333333', linewidth=1.2)
    ax.add_patch(rect)
    ax.text(x + w/2, bar_y + bar_h/2, label, ha='center', va='center',
            fontsize=10, fontweight='bold')

# Bit range labels above
for i, bit_range in enumerate(['Bits 31-24', 'Bits 23-16', 'Bits 15-8', 'Bits 7-0']):
    x = 1.5 + i * 2.8 + 1.3
    ax.text(x, bar_y + bar_h + 0.35, bit_range, ha='center', fontsize=9, color='#555555')

# Byte labels below
for i, byte_label in enumerate(['Byte 3', 'Byte 2', 'Byte 1', 'Byte 0']):
    x = 1.5 + i * 2.8 + 1.3
    ax.text(x, bar_y - 0.35, byte_label, ha='center', fontsize=9, color='#555555')

# Example row
ax.text(7, 0.8, 'Example: rs1 = 0x12_34_AB_CD  →  Value[3]=0x12, Value[2]=0x34, Value[1]=0xAB, Value[0]=0xCD',
        ha='center', fontsize=9.5,
        bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#CCCCCC', alpha=0.9))

# Title
ax.text(7, 4.1, 'Packed INT8 Data Format for WLOAD and DLOAD Instructions',
        ha='center', fontsize=13, fontweight='bold')

# Arrow annotation
ax.annotate('WLOAD / DLOAD packs\n4× INT8 → 32-bit register',
            xy=(0.8, 2.6), fontsize=9, color='#1565C0', fontweight='bold',
            xytext=(0.5, 3.5),
            arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))

plt.tight_layout(pad=0.5)
out = os.path.join(FIG_DIR, 'fig3_5_packed_format.png')
plt.savefig(out, bbox_inches='tight', dpi=200)
plt.close()
print(f"Saved: {out}")
