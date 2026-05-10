"""Generate thesis figures from ILA CSV data and evidence."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import csv
import os

EVIDENCE = r"C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check"
THESIS = r"C:\Users\16084\Documents\Graduation_Design_Library\09_Thesis_Writing"
FIG_DIR = os.path.join(THESIS, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'figure.dpi': 150,
})

def plot_ila_pc_trace(csv_path, output_png):
    """Plot PC values from ILA capture to show CPU execution."""
    samples = []
    pcs = []
    with open(csv_path) as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        next(reader)  # skip radix
        for row in reader:
            try:
                samples.append(int(row[0]))
                pcs.append(int(row[3], 16))
            except (ValueError, IndexError):
                continue

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(samples, [p & 0xFFFF for p in pcs], 'b-', linewidth=0.5, markersize=1)
    ax.set_xlabel('Sample #')
    ax.set_ylabel('PC[15:0]')
    ax.set_title('CPU Program Counter Trace (cnn_accel_demo, ITCM region)')
    ax.grid(True, alpha=0.3)

    # Annotate
    unique_pcs = sorted(set(pcs))
    for upc in unique_pcs[:6]:
        mask = np.array(pcs) == upc
        if mask.any():
            idx = np.where(mask)[0][0]
            ax.annotate(f'0x{upc:08x}', (samples[idx], upc & 0xFFFF),
                       fontsize=7, alpha=0.7,
                       xytext=(5, 10), textcoords='offset points')

    plt.tight_layout()
    fig.savefig(output_png)
    plt.close(fig)
    print(f"  Figure saved: {output_png}")

def plot_ila_nice_activity(csv_path, output_png):
    """Plot NICE handshake and CSR activity."""
    samples = []
    nice_hs = []
    nice_csr = []
    with open(csv_path) as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for row in reader:
            try:
                samples.append(int(row[0]))
                nice_hs.append(int(row[7], 16))
                nice_csr.append(int(row[6], 16))
            except (ValueError, IndexError):
                continue

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5), sharex=True)

    ax1.plot(samples, nice_hs, 'g-', linewidth=0.8)
    ax1.set_ylabel('NICE Handshake')
    ax1.set_title('NICE Interface Activity (cnn_accel_demo ILA capture)')
    ax1.set_yticks([0, 2, 4, 6, 8, 10])
    ax1.grid(True, alpha=0.3)

    ax2.plot(samples, [c & 0xFFF for c in nice_csr], 'r-', linewidth=0.8)
    ax2.set_xlabel('Sample #')
    ax2.set_ylabel('NICE CSR (low 12 bits)')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    fig.savefig(output_png)
    plt.close(fig)
    print(f"  Figure saved: {output_png}")

def plot_speedup_bar(output_png):
    """Generate speedup comparison bar chart."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))

    # Cycles comparison
    metrics = ['CPU Reference', 'NICE Accelerator']
    cycles = [1516, 287]
    colors = ['#4472C4', '#ED7D31']

    bars = ax1.bar(metrics, cycles, color=colors, width=0.5)
    ax1.set_ylabel('Clock Cycles')
    ax1.set_title('Cycle Count Comparison')
    for bar, val in zip(bars, cycles):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                str(val), ha='center', fontsize=11, fontweight='bold')

    # Speedup
    ax2.bar(['Speedup'], [5.28], color='#70AD47', width=0.4)
    ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=1)
    ax2.set_ylabel('Speedup (x)')
    ax2.set_title('Acceleration Ratio')
    ax2.text(0, 5.28 + 0.1, '5.282x', ha='center', fontsize=13, fontweight='bold')

    plt.tight_layout()
    fig.savefig(output_png)
    plt.close(fig)
    print(f"  Figure saved: {output_png}")

def plot_verification_flow(output_png):
    """Generate a summary of the verification evidence chain."""
    fig, ax = plt.subplots(figsize=(8, 2.5))
    ax.axis('off')

    stages = [
        ('RTL Sim\n16/16 PASS', '#4472C4'),
        ('Full-SoC Sim\n7/7 PASS', '#4472C4'),
        ('hello_e203\nBoard PASS', '#70AD47'),
        ('cnn_sysclk_ila\nTiming Clean', '#70AD47'),
        ('cnn_accel_demo\nDEMO PASSED', '#ED7D31'),
    ]

    table_data = [
        ['Stage', 'Result', 'Evidence'],
        ['RTL Simulation', '16/16 PASSED', 'rtl_sim_results.txt'],
        ['Full-SoC Simulation', '7/7 PASSED', 'fullsoc_sim_results.txt'],
        ['hello_e203 Board', 'UART output PASS', 'conclusion.txt'],
        ['cnn_sysclk_ila Build', 'WNS 12.47ns', 'timing_summary_routed.rpt'],
        ['cnn_accel_demo Board', 'DEMO PASSED, 5.282x', 'uart_output.txt'],
    ]

    table = ax.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.0, 1.5)

    for i in range(6):
        for j in range(3):
            cell = table[i, j]
            if i == 0:
                cell.set_facecolor('#4472C4')
                cell.set_text_props(color='white', fontweight='bold')
            elif i >= 1 and j == 1 and 'PASS' in str(table_data[i][j]):
                cell.set_facecolor('#E2EFDA')

    ax.set_title('CNN Accelerator FPGA Verification Chain (v2.0)', fontsize=13, fontweight='bold', pad=20)

    plt.tight_layout()
    fig.savefig(output_png)
    plt.close(fig)
    print(f"  Figure saved: {output_png}")


if __name__ == "__main__":
    csv_path = os.path.join(EVIDENCE, "cnn_sysclk_ila_ila_capture", "ila_capture.csv")

    print("Generating thesis figures...")
    if os.path.exists(csv_path):
        plot_ila_pc_trace(csv_path, os.path.join(FIG_DIR, "fig4_2_ila_pc_trace.png"))
        plot_ila_nice_activity(csv_path, os.path.join(FIG_DIR, "fig4_3_ila_nice_activity.png"))
    else:
        print(f"  WARNING: CSV not found at {csv_path}")

    plot_speedup_bar(os.path.join(FIG_DIR, "fig4_6_speedup_bar.png"))
    plot_verification_flow(os.path.join(FIG_DIR, "fig3_7_verification_chain.png"))

    print(f"\nAll figures saved to: {FIG_DIR}")
    print("Figures ready to insert into thesis docx.")
