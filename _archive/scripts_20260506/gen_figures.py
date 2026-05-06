"""
Generate high-quality thesis figures from ILA CSV data and other sources.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

FIG_DIR = r'C:\Users\16084\Documents\Graduation_Design_Library\09_Thesis_Writing\Figures'
DATA_DIR = r'C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check'

# Style settings for thesis-quality figures
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

# ================================================================
# Figure 1: ILA PC Trace Waveform (hello_e203 boot)
# ================================================================
print("Generating ILA PC trace waveform...")

csv_path = os.path.join(DATA_DIR, 'bootvec_sysclk_ila_ila_capture', 'ila_capture.csv')

# Read CSV
with open(csv_path, 'r') as f:
    header = f.readline().strip().split(',')
    radix = f.readline().strip().split(',')

data = np.genfromtxt(csv_path, delimiter=',', skip_header=2, dtype=str)

# Extract columns
sample = data[:, 0].astype(int)
trigger = data[:, 2].astype(int)
pc = data[:, 3]  # HEX
status = data[:, 4]  # HEX
membus_live = data[:, 5]
uart = data[:, 8]  # probe5_uart
flags = data[:, 9]  # probe6_flags

# Convert PC from hex to int
pc_int = np.array([int(x, 16) for x in pc])
status_int = np.array([int(x, 16) for x in status])
uart_int = np.array([int(x, 16) for x in uart])

# Find trigger point
trig_idx = np.where(trigger == 1)[0]
trig_sample = trig_idx[0] if len(trig_idx) > 0 else 0

# Limit to interesting range: around trigger
window = 300
start = max(0, trig_sample - 50)
end = min(len(sample), trig_sample + window)
x_range = sample[start:end]

fig, axes = plt.subplots(4, 1, figsize=(6, 3.5), sharex=True,
                          gridspec_kw={'height_ratios': [1, 1, 1, 1]})

# PC trace
ax = axes[0]
ax.step(x_range, pc_int[start:end], where='mid', linewidth=0.6, color='#2196F3')
ax.set_ylabel('PC [hex]')
ax.set_ylim(pc_int[start:end].min() - 0x100, pc_int[start:end].max() + 0x100)
ax.grid(True, alpha=0.3)

# Format PC ticks as hex
locs = ax.get_yticks()
ax.set_yticklabels([f'0x{int(x):08X}' for x in locs])

# Status
ax = axes[1]
ax.step(x_range, status_int[start:end], where='mid', linewidth=0.6, color='#4CAF50')
ax.set_ylabel('Status')
ax.set_yticks([0, 4, 8, 12, 13])
ax.set_yticklabels(['0x0', '0x4', '0x8', '0xC', '0xD'])
ax.grid(True, alpha=0.3)

# UART
ax = axes[2]
ax.step(x_range, uart_int[start:end], where='mid', linewidth=0.6, color='#FF9800')
ax.set_ylabel('UART')
ax.set_yticks([0, 4])
ax.set_yticklabels(['0x0', '0x4'])
ax.grid(True, alpha=0.3)

# Membus Live
ax = axes[3]
mb_live = np.array([int(x, 16) for x in membus_live[start:end]])
ax.step(x_range, mb_live, where='mid', linewidth=0.6, color='#9C27B0')
ax.set_ylabel('Membus\nLive')
ax.set_xlabel('Sample')
ax.grid(True, alpha=0.3)

# Mark trigger
for ax in axes:
    ax.axvline(x=trig_sample, color='red', linestyle='--', alpha=0.5, linewidth=0.5)

fig.suptitle('ILA Capture: hello_e203 Boot Sequence (PC Progression)', fontsize=11, y=1.01)
plt.tight_layout()

out_path = os.path.join(FIG_DIR, 'fig_ila_pc_trace.png')
plt.savefig(out_path, bbox_inches='tight', dpi=150)
plt.close()
print(f"  Saved: {out_path}")


# ================================================================
# Figure 2: ILA NICE Activity Waveform
# ================================================================
print("Generating ILA NICE activity waveform...")

csv_path = os.path.join(DATA_DIR, 'cnn_sysclk_ila_ila_capture', 'ila_capture.csv')

data = np.genfromtxt(csv_path, delimiter=',', skip_header=2, dtype=str)

sample = data[:, 0].astype(int)
trigger = data[:, 2].astype(int)
pc = data[:, 3]
reset_uart = data[:, 4]
liveness = data[:, 5]
pc_activity = data[:, 6]
nice_csr = data[:, 7]
nice_hs = data[:, 8]
mem_status = data[:, 9]

pc_int = np.array([int(x, 16) for x in pc])
nice_csr_int = np.array([int(x, 16) for x in nice_csr])
nice_hs_int = np.array([int(x, 16) for x in nice_hs])
liveness_int = np.array([int(x, 16) for x in liveness])

trig_idx = np.where(trigger == 1)[0]
trig_sample = trig_idx[0] if len(trig_idx) > 0 else 0

window = 400
start = max(0, trig_sample - 50)
end = min(len(sample), trig_sample + window)
x_range = sample[start:end]

fig, axes = plt.subplots(4, 1, figsize=(6, 3.5), sharex=True,
                          gridspec_kw={'height_ratios': [1, 1, 1, 1]})

# PC
ax = axes[0]
ax.step(x_range, pc_int[start:end], where='mid', linewidth=0.6, color='#2196F3')
ax.set_ylabel('PC')
ax.grid(True, alpha=0.3)

# NICE CSR
ax = axes[1]
ax.step(x_range, nice_csr_int[start:end], where='mid', linewidth=0.6, color='#E91E63')
ax.set_ylabel('NICE CSR')
ax.grid(True, alpha=0.3)

# NICE Handshake
ax = axes[2]
ax.step(x_range, nice_hs_int[start:end], where='mid', linewidth=0.6, color='#00BCD4')
ax.set_ylabel('NICE HS')
ax.set_yticks([0, 1, 4])
ax.set_yticklabels(['0x0', '0x1', '0x4'])
ax.grid(True, alpha=0.3)

# Liveness
ax = axes[3]
ax.step(x_range, liveness_int[start:end], where='mid', linewidth=0.6, color='#CDDC39')
ax.set_ylabel('Liveness')
ax.set_xlabel('Sample')
ax.grid(True, alpha=0.3)

for ax in axes:
    ax.axvline(x=trig_sample, color='red', linestyle='--', alpha=0.5, linewidth=0.5)

fig.suptitle('ILA Capture: NICE CNN Accelerator Instruction Execution', fontsize=11, y=1.01)
plt.tight_layout()

out_path = os.path.join(FIG_DIR, 'fig_ila_nice_activity.png')
plt.savefig(out_path, bbox_inches='tight', dpi=150)
plt.close()
print(f"  Saved: {out_path}")


# ================================================================
# Figure 3: Speedup Bar Chart
# ================================================================
print("Generating speedup bar chart...")

fig, ax = plt.subplots(figsize=(4.5, 2.5))

# Data based on thesis content
benchmarks = ['4x4 MatMul', '2x2 Conv', '3x3 Conv']
cpu_cycles = [198, 342, 576]
accel_cycles = [37, 68, 109]
speedup = [c/a for c, a in zip(cpu_cycles, accel_cycles)]

x = np.arange(len(benchmarks))
width = 0.25

bars1 = ax.bar(x - width, cpu_cycles, width, label='CPU Only (SW)', color='#607D8B', edgecolor='white')
bars2 = ax.bar(x, accel_cycles, width, label='NICE Accel (HW)', color='#2196F3', edgecolor='white')
bars3 = ax.bar(x + width, [s*20 for s in speedup], width, label='Speedup (x20)', color='#FF5722', edgecolor='white', alpha=0.7)

# Annotate speedup values
for i, s in enumerate(speedup):
    ax.text(x[i] + width, s*20 + 2, f'{s:.1f}x', ha='center', fontsize=9, fontweight='bold')

ax.set_ylabel('Clock Cycles')
ax.set_xticks(x)
ax.set_xticklabels(benchmarks)
ax.legend(loc='upper right', fontsize=8)
ax.grid(axis='y', alpha=0.3)
ax.set_title('CNN Accelerator Performance Speedup', fontsize=12)

plt.tight_layout()

out_path = os.path.join(FIG_DIR, 'fig_speedup_bar.png')
plt.savefig(out_path, bbox_inches='tight', dpi=150)
plt.close()
print(f"  Saved: {out_path}")


# ================================================================
# Figure 4: Verification Flow Diagram (schematic)
# ================================================================
print("Generating verification flow diagram...")

fig, ax = plt.subplots(figsize=(5.5, 2.0))
ax.set_xlim(0, 10)
ax.set_ylim(0, 3)
ax.axis('off')

# Define flow boxes
boxes = [
    (0.3, 1.4, 'RTL\nSimulation\n(iverilog)', '#E3F2FD'),
    (2.6, 1.4, 'Full SoC\nSimulation\n(RSTAT=19)', '#BBDEFB'),
    (4.9, 1.4, 'FPGA\nBitstream\n(Vivado)', '#90CAF9'),
    (7.2, 1.4, 'Board\nValidation\n(ILA+UART)', '#42A5F5'),
]

for x, y, text, color in boxes:
    rect = mpatches.FancyBboxPatch((x, y-0.4), 2.0, 1.2,
                                     boxstyle="round,pad=0.1",
                                     facecolor=color, edgecolor='#1565C0',
                                     linewidth=1.2, alpha=0.9)
    ax.add_patch(rect)
    ax.text(x + 1.0, y + 0.2, text, ha='center', va='center', fontsize=8, fontweight='bold')

# Arrows between boxes
for i in range(len(boxes) - 1):
    x1 = boxes[i][0] + 2.0
    x2 = boxes[i+1][0]
    y = boxes[i][1] + 0.2
    ax.annotate('', xy=(x2, y), xytext=(x1 + 0.1, y),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))

# Feedback arrow from Board back to RTL
ax.annotate('Debug Loop', xy=(0.5, 2.2), xytext=(8.0, 2.2),
            arrowprops=dict(arrowstyle='->', color='#F44336', lw=1.2,
                          connectionstyle='arc3,rad=0.5'),
            fontsize=7, color='#F44336', ha='center')

ax.set_title('Multi-Stage Verification Methodology', fontsize=12, y=1.05)

plt.tight_layout()

out_path = os.path.join(FIG_DIR, 'fig_verification_chain.png')
plt.savefig(out_path, bbox_inches='tight', dpi=150)
plt.close()
print(f"  Saved: {out_path}")

print("\nAll figures regenerated successfully!")
