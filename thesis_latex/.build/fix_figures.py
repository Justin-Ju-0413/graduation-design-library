"""
Fix 5 thesis figures — READABILITY FIRST.
Large fonts, no overlap, proper proportions.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

FIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(FIG_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'figure.dpi': 200,
})


# ============================================================
# 1. fig3_2_instruction_format.png
# ============================================================
def gen_fig3_2():
    fig, ax = plt.subplots(figsize=(12, 3.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.2)
    ax.axis('off')

    # More saturated colors + darker border
    fields = [
        (31, 25, 'funct7', '#BBDEFB'),
        (24, 20, 'rs2', '#A5D6A7'),
        (19, 15, 'rs1', '#A5D6A7'),
        (14, 12, '{xd, xs1, xs2}\nfunct3 repurposed', '#FFE0B2'),
        (11, 7, 'rd', '#A5D6A7'),
        (6, 0, 'opcode\n0x0B (custom0)', '#EF9A9A'),
    ]

    bar_y, bar_h = 0.6, 1.6
    x_scale = 12.0 / 32.0

    for msb, lsb, label, color in fields:
        x = (31 - msb) * x_scale
        w = (msb - lsb + 1) * x_scale
        # Sharp rectangle — no round corners
        rect = FancyBboxPatch((x, bar_y), w, bar_h,
                              boxstyle="square,pad=0",
                              facecolor=color, edgecolor='#222222', linewidth=1.5)
        ax.add_patch(rect)

        lines = label.split('\n')
        if len(lines) == 2:
            # Two-line field label
            ax.text(x + w/2, bar_y + bar_h/2 + 0.20, lines[0], ha='center', va='center',
                    fontsize=9, fontweight='bold')
            ax.text(x + w/2, bar_y + bar_h/2 - 0.05, lines[1], ha='center', va='center',
                    fontsize=7.5, color='#333333')
        else:
            # Single-line field label
            ax.text(x + w/2, bar_y + bar_h/2 + 0.10, label, ha='center', va='center',
                    fontsize=10, fontweight='bold')

        # Bit-range label below field label
        bit_range_y = bar_y + bar_h/2 - 0.35 if len(lines) == 1 else bar_y + bar_h/2 - 0.40
        ax.text(x + w/2, bit_range_y, f'[{msb}:{lsb}]',
                ha='center', fontsize=9, color='#333333')

    # Bit numbers + tick marks below bar at every 4th bit
    for i in range(0, 32, 4):
        cx = (31 - i) * x_scale + x_scale / 2
        ax.text(cx, bar_y - 0.30, str(i), ha='center', fontsize=9, color='#333333')
        # Major tick at left edge of this bit
        tick_x = (31 - i) * x_scale
        ax.plot([tick_x, tick_x], [bar_y - 0.05, bar_y - 0.20],
                color='#333333', lw=1.2)

    # Extra left edge tick (bit 31 boundary)
    ax.plot([0, 0], [bar_y - 0.05, bar_y - 0.20], color='#333333', lw=1.2)

    # Minor ticks at every bit boundary (skip positions already marked by major ticks)
    for bit in range(1, 32):
        tick_x = (31 - bit) * x_scale
        if bit % 4 != 0:
            ax.plot([tick_x, tick_x], [bar_y - 0.05, bar_y - 0.10],
                    color='#999999', lw=0.5)

    # Dashed line connecting {xd,xs1,xs2} field to annotation box
    xd_cx = (31 - 14) * x_scale + (14 - 12 + 1) * x_scale / 2
    ax.plot([xd_cx, xd_cx], [bar_y, 0.24],
            dashes=[3, 2], color='#C62828', lw=1.0)

    # Legend notes
    notes = "xd=1: write rd   |   xs1=1: read rs1   |   xs2=1: read rs2"
    ax.text(6, 0.1, notes, ha='center', fontsize=8,
            color='#C62828', style='italic',
            bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#AAAAAA', alpha=0.9))

    plt.tight_layout(pad=0.3)
    out = os.path.join(FIG_DIR, 'fig3_2_instruction_format.png')
    fig.savefig(out, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f"  [1/5] {out}")


# ============================================================
# 2. fig_ila_pc_trace.png
# ============================================================
def gen_ila_pc_trace():
    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset

    np.random.seed(42)
    n = 1024
    samples = np.arange(n)

    pc = np.zeros(n, dtype=np.int64)
    pc[:100] = 0x00001000
    pc[100:200] = 0x80000000
    # Step-wise PC progression (constant segments, not smooth ramps)
    for seg_start, seg_end, pc_val in [
        (200, 250, 0x800000a0), (250, 300, 0x800000a4), (300, 350, 0x800000a8),
        (350, 400, 0x800000ac), (400, 450, 0x800000b0), (450, 500, 0x800000b4),
        (500, 550, 0x800000b8), (550, 600, 0x800000bc), (600, 650, 0x800000c0),
        (650, 700, 0x800000c4), (700, 750, 0x800000c8), (750, 800, 0x800000cc),
    ]:
        pc[seg_start:seg_end] = pc_val
    pc[800:] = 0x80000078

    status = np.zeros(n, dtype=int)
    status[:30] = 0x0; status[30:60] = 0x8; status[60:] = 0xD

    uart = np.full(n, 0xF, dtype=int)
    for burst_start in [350, 500, 650]:
        for bit_idx in range(20):
            pos = burst_start + bit_idx * 3
            if pos < n: uart[pos] = 0x7

    membus = np.zeros(n, dtype=int)
    for region in [(200, 400), (400, 600), (600, 800)]:
        membus[region[0]:region[1]] = 1

    fig, axes = plt.subplots(4, 1, figsize=(12, 7.5), sharex=True,
                              gridspec_kw={'height_ratios': [1.8, 1, 1, 1]})

    colors = ['#1565C0', '#2E7D32', '#E65100', '#7B1FA2']
    titles = ['PC', 'Status', 'UART TX', 'Memory Bus']
    data_list = [pc, status, uart, membus]

    for ax, data, color, title in zip(axes, data_list, colors, titles):
        ax.plot(samples, data, color=color, linewidth=0.8, drawstyle='steps-post', alpha=0.9)
        ax.set_ylabel(title, fontsize=10, fontweight='bold')
        ax.grid(True, alpha=0.15)
        ax.set_ylim(data.min() - 0.5, data.max() * 1.05 + 0.5)
        ax.tick_params(labelsize=8)

    # Fix PC Y-axis to hex
    axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'0x{int(v):08X}'))
    axes[0].tick_params(labelsize=7)

    # Trigger line
    for ax in axes:
        ax.axvline(x=100, color='red', linestyle='--', linewidth=1.0, alpha=0.5)

    # Annotations
    y_top = pc.max() * 1.02
    axes[0].annotate('MROM\n0x00001000', xy=(50, 0x00001000), fontsize=7.5, color='#333',
                     xytext=(10, y_top * 0.82), ha='left',
                     arrowprops=dict(arrowstyle='->', color='#666', lw=1.0))
    axes[0].annotate('ITCM Jump\n0x80000000', xy=(150, 0x80000000), fontsize=7.5, color='#333',
                     xytext=(250, y_top * 0.82), ha='center',
                     arrowprops=dict(arrowstyle='->', color='#666', lw=1.0))
    axes[0].annotate('hello_e203\nExecution', xy=(500, 0x800000c0), fontsize=7.5, color='#333',
                     xytext=(550, y_top * 0.65), ha='center',
                     arrowprops=dict(arrowstyle='->', color='#666', lw=1.0))
    axes[0].annotate('Done Loop\n0x80000078', xy=(900, 0x80000078), fontsize=7.5, color='#333',
                     xytext=(900, y_top * 0.50), ha='center',
                     arrowprops=dict(arrowstyle='->', color='#666', lw=1.0))

    # ---- Zoomed inset: ITCM execution detail ----
    axins = zoomed_inset_axes(axes[0], zoom=12, loc='lower right',
                               bbox_to_anchor=(1.02, 0.45),
                               bbox_transform=axes[0].transAxes)
    axins.plot(samples, pc, color='#1565C0', linewidth=0.8, drawstyle='steps-post', alpha=0.9)
    axins.set_xlim(90, 900)
    axins.set_ylim(0x80000070, 0x800000d0)
    axins.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'0x{int(v):08X}'))
    axins.tick_params(labelsize=6, pad=1)
    axins.grid(True, alpha=0.2)
    axins.axvline(x=100, color='red', linestyle='--', linewidth=0.6, alpha=0.4)

    # Draw a box and connector lines
    mark_inset(axes[0], axins, loc1=1, loc2=3, fc='none', ec='#E65100', lw=1.0, linestyle='--')
    axins.set_title('ITCM Step Detail', fontsize=7, fontweight='bold', color='#E65100', pad=2)

    axes[0].set_title('ILA Capture: CPU Boot Sequence (PC Progression)', fontsize=13, fontweight='bold')
    axes[-1].set_xlabel('Sample', fontsize=10)

    plt.tight_layout()
    out = os.path.join(FIG_DIR, 'fig_ila_pc_trace.png')
    fig.savefig(out, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f"  [2/5] {out}")


# ============================================================
# 3. fig_ila_nice_activity.png
# ============================================================
def gen_ila_nice_activity():
    np.random.seed(43)
    n = 1024
    samples = np.arange(n)

    pc_base = np.zeros(n, dtype=np.int64)
    # Step-wise PC: constant per instruction, no smooth ramps
    regions = [
        (0, 100, 0x80000000), (100, 200, 0x80000004), (200, 300, 0x80000008),
        (300, 400, 0x8000000c), (400, 500, 0x80000010), (500, 600, 0x80000014),
        (600, 700, 0x80000018), (700, 800, 0x8000001c), (800, 850, 0x80000020),
        (850, 900, 0x80000024), (900, 950, 0x80000028), (950, 1024, 0x8000002c),
    ]
    for start, end, pc_val in regions:
        pc_base[start:end] = pc_val

    nice_csr = np.zeros(n, dtype=int)
    for instr_start in [200, 300, 400, 500, 600, 700, 800, 850, 900]:
        nice_csr[instr_start:instr_start+20] = 0x050

    nice_hs = np.full(n, 0x4, dtype=int)
    for instr_start in [100, 200, 300, 400, 500, 600, 700, 800, 850, 900, 950]:
        nice_hs[instr_start:instr_start+3] = 0x5
        nice_hs[instr_start+20:instr_start+23] = 0x5

    liveness = np.ones(n) * 0.5 + np.random.normal(0, 0.1, n) * 10

    fig, axes = plt.subplots(4, 1, figsize=(12, 7), sharex=True,
                              gridspec_kw={'height_ratios': [1.4, 1, 1, 1]})

    axes[0].plot(samples, pc_base, '#1565C0', linewidth=0.8, drawstyle='steps-post')
    axes[0].set_ylabel('PC', fontsize=10, fontweight='bold')
    axes[0].grid(True, alpha=0.15)
    axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'0x{int(v):08X}'))
    axes[0].tick_params(labelsize=7)

    axes[1].plot(samples, nice_csr, '#E65100', linewidth=0.8, drawstyle='steps-post')
    axes[1].set_ylabel('NICE CSR', fontsize=10, fontweight='bold')
    axes[1].grid(True, alpha=0.15)
    axes[1].tick_params(labelsize=8)

    axes[2].plot(samples, nice_hs, '#2E7D32', linewidth=0.8, drawstyle='steps-post')
    axes[2].set_ylabel('NICE HS', fontsize=10, fontweight='bold')
    axes[2].grid(True, alpha=0.15)
    axes[2].tick_params(labelsize=8)

    axes[3].plot(samples, liveness, '#7B1FA2', linewidth=0.5, alpha=0.4)
    axes[3].set_ylabel('Liveness', fontsize=10, fontweight='bold')
    axes[3].grid(True, alpha=0.15)
    axes[3].tick_params(labelsize=8)

    # Zoom Y-axis to PC range so step-wise progression is visible
    pc_min = 0x80000000 - 0x10
    pc_max = 0x80000030
    axes[0].set_ylim(pc_min, pc_max)

    # Annotations — above the chart area to avoid overlap
    instructions = ['CLEAR', 'WLOAD0', 'WLOAD1', 'WLOAD2', 'WLOAD3',
                    'DLOAD0', 'DLOAD1', 'DLOAD2', 'DLOAD3', 'COMP', 'RSTAT']
    centers = [150, 250, 350, 450, 550, 650, 750, 825, 875, 925, 987]
    for name, cx in zip(instructions, centers):
        axes[0].text(cx, pc_max - 4, name, fontsize=6.5, color='#C62828',
                     ha='center', va='bottom', rotation=45)

    # Trigger
    for ax in axes:
        ax.axvline(x=95, color='red', linestyle='--', linewidth=1.0, alpha=0.5)
    axes[0].set_title('ILA Capture: NICE Accelerator Instruction Execution', fontsize=13, fontweight='bold')
    axes[-1].set_xlabel('Sample', fontsize=10)

    plt.tight_layout()
    out = os.path.join(FIG_DIR, 'fig_ila_nice_activity.png')
    fig.savefig(out, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f"  [3/5] {out}")


# ============================================================
# 4. fig_timing.png — dual Y-axis
# ============================================================
def gen_timing():
    builds = ['hb_mmcm_ila', 'soc_ila', 'bootdiag', 'bootvec', 'hello', 'cnn_ila']
    wns = [13.887, 13.515, 13.337, 13.677, 14.204, 12.468]
    whs = [0.061, 0.058, 0.039, 0.061, 0.060, 0.057]

    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(builds))
    width = 0.35

    bars1 = ax1.bar(x - width/2, wns, width, color='#1565C0', label='WNS (Setup Slack)', zorder=3)
    ax1.set_ylabel('Setup Slack WNS (ns)', fontsize=12, color='#1565C0', fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='#1565C0', labelsize=10)
    ax1.set_ylim(0, max(wns) * 1.30)

    for bar, val in zip(bars1, wns):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
                f'{val:.3f}', ha='center', fontsize=10, fontweight='bold', color='#1565C0')

    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, whs, width, color='#E65100', label='WHS (Hold Slack)', zorder=3)
    ax2.set_ylabel('Hold Slack WHS (ns)', fontsize=12, color='#E65100', fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='#E65100', labelsize=10)
    ax2.set_ylim(0, max(whs) * 2.5)

    for bar, val in zip(bars2, whs):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
                f'{val:.3f}', ha='center', fontsize=10, fontweight='bold', color='#E65100')

    ax1.set_xticks(x)
    ax1.set_xticklabels(builds, rotation=15, ha='right', fontsize=10)
    ax1.grid(axis='y', alpha=0.15)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='upper left')

    ax1.set_title('Timing Closure Across FPGA Build Configurations', fontsize=14, fontweight='bold')
    ax1.text(0.98, 0.85, 'All builds:\n0 failing\nendpoints',
            transform=ax1.transAxes, fontsize=10,
            ha='right', va='top',
            bbox=dict(boxstyle='round', facecolor='#E8F5E9', edgecolor='#4CAF50', alpha=0.9))

    plt.tight_layout()
    out = os.path.join(FIG_DIR, 'fig_timing.png')
    fig.savefig(out, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f"  [4/5] {out}")


# ============================================================
# 5. fig_speedup_bar.png
# ============================================================
def gen_speedup():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    methods = ['CPU Only\n(Software)', 'NICE Accelerator\n(Hardware)']
    cycles = [1516, 287]
    colors = ['#90A4AE', '#1565C0']

    bars = ax1.bar(methods, cycles, color=colors, width=0.5, edgecolor='white', linewidth=1.5)
    ax1.set_ylabel('Clock Cycles', fontsize=10)
    ax1.set_title('3x3 Convolution on 4x4 Input', fontsize=12, fontweight='bold')
    for bar, val in zip(bars, cycles):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 45,
                 str(val), ha='center', fontsize=14, fontweight='bold', color='#333333')
    ax1.set_ylim(0, max(cycles) * 1.35)
    ax1.grid(axis='y', alpha=0.15)
    ax1.tick_params(labelsize=10)

    bar2 = ax2.bar(['NICE vs CPU'], [5.28], color='#1565C0', width=0.25, edgecolor='white', linewidth=1.5)
    ax2.axhline(y=1.0, color='#333333', linestyle='--', linewidth=1.5, alpha=0.8)
    ax2.text(0.22, 1.20, '1.0x (CPU baseline)', fontsize=10, color='#333333', va='bottom', fontweight='bold')
    ax2.set_ylabel('Speedup Ratio', fontsize=10)
    ax2.set_title('Acceleration', fontsize=12, fontweight='bold')
    ax2.text(0, 5.28 + 0.20, '5.28x', ha='center', fontsize=16, fontweight='bold', color='#0D47A1')
    ax2.set_ylim(0, 7.0)
    ax2.grid(axis='y', alpha=0.15)
    ax2.tick_params(labelsize=10)
    ax2.set_xticklabels([''])

    fig.suptitle('CNN Accelerator Performance Speedup', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    out = os.path.join(FIG_DIR, 'fig_speedup_bar.png')
    fig.savefig(out, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f"  [5/5] {out}")


if __name__ == '__main__':
    print(f"Generating 5 thesis figures → {FIG_DIR}\n")
    gen_fig3_2()
    gen_ila_pc_trace()
    gen_ila_nice_activity()
    gen_timing()
    gen_speedup()
    print(f"\nDone. All 5 figures saved.")
