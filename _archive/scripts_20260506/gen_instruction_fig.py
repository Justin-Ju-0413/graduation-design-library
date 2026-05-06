"""
Generate professional RISC-V custom instruction format diagrams.
Figure 3.2a: Bit-field layout
Figure 3.2b: Six NICE instructions encoding table
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

FIG_DIR = r'C:\Users\16084\Documents\Graduation_Design_Library\09_Thesis_Writing\Figures'

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 9,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

# ================================================================
# Figure 3.2: RISC-V Custom Instruction Bit-field Diagram
# ================================================================

# Bit field definition: (start_bit, end_bit, label_top, label_bottom, color)
# MSB is 31, LSB is 0
fields = [
    (31, 25, 'funct7', '7-bit', '#E3F2FD'),
    (24, 20, 'rs2', '5-bit', '#FFF3E0'),
    (19, 15, 'rs1', '5-bit', '#E8F5E9'),
    (14, 12, 'xd|xs1|xs2', '3-bit', '#FCE4EC'),
    (11,  7, 'rd', '5-bit', '#F3E5F5'),
    (6,   0, 'opcode', '0x0B (custom0)', '#ECEFF1'),
]

fig, ax = plt.subplots(figsize=(7, 1.8))
ax.set_xlim(-1, 33)
ax.set_ylim(0, 3.5)
ax.axis('off')

# Draw the main bit-field boxes
box_height = 1.0
box_y = 1.5

for start, end, label, sublabel, color in fields:
    width = start - end + 1
    x = end

    # Main box
    rect = FancyBboxPatch((x, box_y), width, box_height,
                          boxstyle="round,pad=0.08",
                          facecolor=color, edgecolor='#37474F',
                          linewidth=1.2)
    ax.add_patch(rect)

    # Bit range label (inside box, top)
    ax.text(x + width/2, box_y + box_height - 0.25,
            label, ha='center', va='center', fontsize=9, fontweight='bold',
            color='#263238')

    # Sub-label (inside box, bottom)
    ax.text(x + width/2, box_y + 0.25,
            sublabel, ha='center', va='center', fontsize=7.5,
            color='#546E7A')

    # Bit indices
    ax.text(x, box_y - 0.15, str(end), ha='center', va='top', fontsize=7, color='#37474F')
    ax.text(x + width, box_y - 0.15, str(start), ha='center', va='top', fontsize=7, color='#37474F')

# Bit ruler at top
for i in range(32):
    ax.plot([i, i], [box_y + box_height + 0.15, box_y + box_height + 0.35],
            'k-', linewidth=0.4, alpha=0.5)
    if i % 4 == 0:
        ax.text(i, box_y + box_height + 0.45, str(i), ha='center', va='bottom',
                fontsize=6.5, color='#546E7A')

# Add NICE-specific annotation
ax.annotate('E203 NICE\nrepurposing', xy=(13, box_y + box_height/2),
            xytext=(13, box_y - 0.85),
            ha='center', fontsize=7, color='#C62828',
            arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.2))

# Title
ax.text(16, 3.2, 'RISC-V Custom Instruction Format (opcode = custom0, 0x0B)',
        ha='center', fontsize=11, fontweight='bold')

# NICE control bit legend at bottom
legend_y = 0.3
ax.text(16, legend_y,
        'E203 NICE control bits [14:12]:  xd = write rd (bit 14)  |  xs1 = read rs1 (bit 13)  |  xs2 = read rs2 (bit 12)',
        ha='center', fontsize=7.5, style='italic', color='#546E7A')

plt.tight_layout()
out_path = os.path.join(FIG_DIR, 'fig3_2_instruction_format.png')
plt.savefig(out_path, bbox_inches='tight', dpi=150)
plt.close()
print(f"Saved: {out_path}")


# ================================================================
# Figure 3.2b: Instruction Encoding Table (visual)
# ================================================================
# Six NICE custom instructions
instructions = [
    ('CFG',    '0x00', 'Configure ReLU',       'xd=1,xs1=1,xs2=0'),
    ('CLEAR',  '0x01', 'Reset accumulators',    'xd=0,xs1=0,xs2=0'),
    ('WLOAD',  '0x02', 'Load weight column',    'xd=0,xs1=1,xs2=1'),
    ('DLOAD',  '0x03', 'Load activation row',   'xd=0,xs1=1,xs2=1'),
    ('COMP',   '0x04', 'Compute (PE array)',    'xd=1,xs1=0,xs2=0'),
    ('RSTAT',  '0x05', 'Read result',           'xd=1,xs1=0,xs2=0'),
]

fig, ax = plt.subplots(figsize=(6.5, 2.2))
ax.set_xlim(0, 32)
ax.set_ylim(0, 6.5)
ax.axis('off')

col_starts = [0, 7, 14, 24]
col_widths = [6, 6, 9, 7]
col_headers = ['Mnemonic', 'funct7', 'Description', 'NICE Flags']
header_colors = ['#37474F'] * 4

# Draw header
for i, (header, start, width) in enumerate(zip(col_headers, col_starts, col_widths)):
    rect = FancyBboxPatch((start, 5.5), width, 0.7,
                          boxstyle="round,pad=0.05",
                          facecolor='#37474F', edgecolor='#263238', linewidth=0.8)
    ax.add_patch(rect)
    ax.text(start + width/2, 5.85, header, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='white')

# Draw rows
row_colors = ['#FAFAFA', '#F5F5F5']
for row_idx, (mnemonic, funct7, desc, flags) in enumerate(instructions):
    y = 4.6 - row_idx * 0.7
    bg = row_colors[row_idx % 2]

    # Row background
    rect = FancyBboxPatch((0, y - 0.02), 31, 0.66,
                          boxstyle="round,pad=0.02",
                          facecolor=bg, edgecolor='none')
    ax.add_patch(rect)

    # Cells
    texts = [mnemonic, funct7, desc, flags]
    for col_idx, (text, start, width) in enumerate(zip(texts, col_starts, col_widths)):
        ax.text(start + width/2, y + 0.3, text, ha='center', va='center',
                fontsize=8.5 if col_idx > 1 else 9,
                fontweight='bold' if col_idx < 2 else 'normal',
                color='#263238' if col_idx > 1 else '#1565C0',
                family='monospace' if col_idx < 2 else 'serif')

    # Vertical separator lines
    for sep_x in [7, 14, 24]:
        ax.plot([sep_x, sep_x], [y - 0.1, y + 0.6], '-', color='#E0E0E0', linewidth=0.5)

ax.set_title('NICE Custom Instruction Set for CNN Accelerator', fontsize=11, fontweight='bold', y=1.02)

plt.tight_layout()
out_path = os.path.join(FIG_DIR, 'fig3_2b_instruction_table.png')
plt.savefig(out_path, bbox_inches='tight', dpi=150)
plt.close()
print(f"Saved: {out_path}")

print("Done!")
