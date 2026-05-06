"""Generate architecture diagrams for thesis using matplotlib patches."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np
import os

FIG_DIR = r"C:\Users\16084\Documents\Graduation_Design_Library\09_Thesis_Writing\figures"
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 9

def draw_box(ax, x, y, w, h, text, color='#D6E4F0', edgecolor='#2F5496', fontsize=9, bold=False):
    """Draw a rounded rectangle with text."""
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                         facecolor=color, edgecolor=edgecolor, linewidth=1.5)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize,
            weight=weight, wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, color='#333333', lw=1.2):
    """Draw an arrow from (x1,y1) to (x2,y2)."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
               arrowprops=dict(arrowstyle='->', color=color, lw=lw))

def draw_line(ax, x1, y1, x2, y2, color='#333333', lw=1.0, ls='-'):
    """Draw a line."""
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, linestyle=ls)


def fig3_1_soc_architecture(output_png):
    """Figure 3.1: System-level block diagram of E203 SoC with CNN NICE accelerator."""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('Figure 3.1: E203 SoC with CNN NICE Accelerator', fontsize=14, fontweight='bold', y=1.02)

    # SoC boundary
    soc_box = FancyBboxPatch((0.3, 0.2), 9.4, 6.5, boxstyle="round,pad=0.2",
                             facecolor='none', edgecolor='#2F5496', linewidth=2.5, linestyle='-')
    ax.add_patch(soc_box)
    ax.text(5, 6.9, 'E203 Hummingbird v2 SoC', ha='center', va='bottom', fontsize=12, fontweight='bold', color='#2F5496')

    # E203 Core
    draw_box(ax, 0.6, 2.5, 4.0, 3.5, '', color='#D6E4F0', edgecolor='#2F5496')
    ax.text(2.6, 5.8, 'E203 Core (RV32IMAC)', ha='center', fontsize=11, fontweight='bold', color='#2F5496')

    # Core sub-blocks
    draw_box(ax, 0.8, 2.8, 3.6, 0.7, 'Instruction Fetch Unit\n(IFU)', color='#BDD7EE', edgecolor='#4472C4', fontsize=8)
    draw_box(ax, 0.8, 3.7, 3.6, 0.7, 'Execution Unit (EXU)\n- ALU, MULDIV, NICE Interface', color='#BDD7EE', edgecolor='#4472C4', fontsize=8)
    draw_box(ax, 0.8, 4.6, 3.6, 0.7, 'Load/Store Unit (LSU)\n+ Bus Interface Unit (BIU)', color='#BDD7EE', edgecolor='#4472C4', fontsize=8)
    draw_arrow(ax, 2.6, 4.6, 2.6, 4.4)

    # CNN Accelerator
    draw_box(ax, 5.2, 3.5, 4.3, 2.8, '', color='#E2EFDA', edgecolor='#548235')
    ax.text(7.35, 6.1, 'CNN Accelerator', ha='center', fontsize=11, fontweight='bold', color='#548235')
    draw_box(ax, 5.5, 3.7, 3.8, 0.6, 'cnn_nice_core\nNICE Decoder + Control FSM', color='#C5E0B4', edgecolor='#70AD47', fontsize=8)
    draw_box(ax, 5.5, 4.5, 3.8, 1.4, 'PE Array (4x4)\n16 Processing Elements\nINT8 MAC + INT32 Accumulator', color='#C5E0B4', edgecolor='#70AD47', fontsize=8)

    # NICE connection
    draw_arrow(ax, 4.6, 5.0, 5.2, 5.2)
    ax.text(4.9, 5.3, 'NICE\nInterface', ha='center', fontsize=7, color='#C00000')

    # Memories
    draw_box(ax, 0.6, 1.0, 4.0, 1.0, 'ITCM (64KB @ 0x80000000)\n64-bit Instruction Memory', color='#FCE4D6', edgecolor='#ED7D31', fontsize=8)
    draw_box(ax, 5.2, 1.0, 4.3, 1.0, 'DTCM (64KB @ 0x90000000)\n32-bit Data Memory', color='#FCE4D6', edgecolor='#ED7D31', fontsize=8)
    draw_arrow(ax, 2.6, 2.5, 2.6, 2.0)

    # Peripherals
    draw_box(ax, 0.6, 0.3, 2.0, 0.5, 'UART0 + GPIO', color='#E4DFEC', edgecolor='#7030A0', fontsize=7)
    draw_box(ax, 2.8, 0.3, 2.0, 0.5, 'CLINT + PLIC', color='#E4DFEC', edgecolor='#7030A0', fontsize=7)
    draw_box(ax, 5.2, 0.3, 2.0, 0.5, 'Debug Module (JTAG)', color='#E4DFEC', edgecolor='#7030A0', fontsize=7)

    # System bus
    ax.plot([0.6, 9.7], [0.95, 0.95], 'k-', linewidth=1.5, color='#888888')
    ax.text(9.35, 1.1, 'System Bus (ICB)', ha='right', fontsize=7, color='#888888')

    plt.tight_layout()
    fig.savefig(output_png, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f"  Saved: {output_png}")


def fig3_2_instruction_format(output_png):
    """Figure 3.2: RISC-V custom instruction format for NICE."""
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.5)
    ax.axis('off')
    ax.set_title('Figure 3.2: NICE Custom Instruction Encoding (opcode 0x0B)', fontsize=13, fontweight='bold')

    # Bit fields
    fields = [
        (0, 7, 'opcode\n0x0B', '#FF6B6B'),
        (7, 12, 'rd\n5-bit', '#BDD7EE'),
        (12, 15, 'xd/xs1/\nxs2', '#C5E0B4'),
        (15, 20, 'rs1\n5-bit', '#BDD7EE'),
        (20, 25, 'rs2\n5-bit', '#BDD7EE'),
        (25, 32, 'funct7\n7-bit', '#FCE4D6'),
    ]

    for start, end, label, color in fields:
        draw_box(ax, start*0.31, 1.0, (end-start)*0.31, 1.2, label, color=color, edgecolor='#333333', fontsize=8)

    # Bit numbers
    for i in range(32):
        x = i * 0.31 + 0.155
        ax.text(x, 2.4, str(31-i), ha='center', fontsize=6, color='#666666')

    # Width labels
    ax.text(3.5*0.31, 0.5, '7 bits', ha='center', fontsize=7, color='#666666')
    ax.text((25+20)/2*0.31, 0.5, '5 bits', ha='center', fontsize=7, color='#666666')
    ax.text((20+15)/2*0.31, 0.5, '5 bits', ha='center', fontsize=7, color='#666666')
    ax.text((15+12)/2*0.31, 0.5, '3 bits', ha='center', fontsize=7, color='#666666')
    ax.text((12+7)/2*0.31, 0.5, '5 bits', ha='center', fontsize=7, color='#666666')
    ax.text((7+0)/2*0.31, 0.5, '7 bits', ha='center', fontsize=7, color='#666666')

    # NICE-specific annotation
    ax.annotate('xd=1: write rd\nxs1=1: read rs1\nxs2=1: read rs2',
                xy=(4.2, 0.3), fontsize=8, color='#C00000',
                bbox=dict(boxstyle='round', facecolor='#FFF2CC', edgecolor='#C00000', alpha=0.8))

    plt.tight_layout()
    fig.savefig(output_png, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f"  Saved: {output_png}")


def fig3_3_pe_microarchitecture(output_png):
    """Figure 3.3: PE microarchitecture."""
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_title('Figure 3.3: Processing Element (PE) Microarchitecture', fontsize=13, fontweight='bold')

    # Weight input
    draw_box(ax, 0.5, 4.0, 1.5, 0.6, 'Weight W[j]\nINT8', color='#D6E4F0', edgecolor='#2F5496', fontsize=8)
    # Activation input
    draw_box(ax, 0.5, 2.8, 1.5, 0.6, 'Activation D[i]\nINT8', color='#E2EFDA', edgecolor='#548235', fontsize=8)

    # Multiplier
    draw_box(ax, 2.5, 3.2, 2.0, 1.0, 'Multiplier\nW[j] x D[i]\n= INT16', color='#FFF2CC', edgecolor='#BF8F00', fontsize=8)

    # Accumulator
    draw_box(ax, 5.0, 3.2, 1.5, 1.8, 'Accumulator\nINT32\nAcc +=\n(W x D)', color='#FCE4D6', edgecolor='#ED7D31', fontsize=8)

    # Clear/Enable
    draw_box(ax, 3.0, 1.5, 2.0, 0.5, 'clear / enable', color='#E4DFEC', edgecolor='#7030A0', fontsize=7)
    draw_arrow(ax, 4.0, 2.0, 5.5, 3.2)

    # Arrows
    draw_arrow(ax, 2.0, 4.3, 2.5, 3.9)
    draw_arrow(ax, 2.0, 3.1, 2.5, 3.5)
    draw_arrow(ax, 4.5, 3.7, 5.0, 3.7)
    # Result output
    draw_arrow(ax, 6.5, 4.1, 7.0, 4.1)
    ax.text(6.8, 4.3, 'Result[31:0]', fontsize=8, color='#C00000', ha='center')

    # Clock
    ax.text(5.0, 0.8, 'clk + rst_n', ha='center', fontsize=8, color='#666666')
    draw_arrow(ax, 5.0, 1.0, 5.0, 1.5)

    plt.tight_layout()
    fig.savefig(output_png, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f"  Saved: {output_png}")


def fig3_4_pe_array(output_png):
    """Figure 3.4: 4x4 PE Array organization."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('Figure 3.4: 4x4 PE Array Organization (Output Stationary)', fontsize=13, fontweight='bold')

    # PE grid
    pe_w, pe_h = 1.0, 0.8
    start_x, start_y = 1.5, 1.5

    for i in range(4):  # rows (D)
        for j in range(4):  # cols (W)
            x = start_x + j * 1.2
            y = start_y + (3-i) * 1.0
            draw_box(ax, x, y, pe_w, pe_h,
                    f'PE{i}{j}\nW[{j}]*D[{i}]',
                    color='#C5E0B4', edgecolor='#548235', fontsize=6.5)

            if i == 0:  # Top row - weight broadcast
                draw_box(ax, x, y + 1.1, pe_w, 0.35,
                        f'W[{j}]', color='#D6E4F0', edgecolor='#2F5496', fontsize=7)
                draw_arrow(ax, x + pe_w/2, y + 1.1, x + pe_w/2, y + pe_h)

        # Left column - activation broadcast
        draw_box(ax, 0.3, y, 0.9, pe_h,
                f'D[{3-i}]', color='#E2EFDA', edgecolor='#548235', fontsize=7)
        draw_arrow(ax, 1.2, y + pe_h/2, start_x, y + pe_h/2)

    # Accumulator sum
    draw_box(ax, 1.5, 0.3, 5.0, 0.6,
            'Tree Adder: Sum of all 16 PE outputs -> Result[31:0]',
            color='#FFF2CC', edgecolor='#BF8F00', fontsize=8)

    # Sum arrows from each PE
    for j in range(4):
        draw_arrow(ax, start_x + j*1.2 + pe_w/2, start_y, start_x + j*1.2 + pe_w/2, 0.9)

    plt.tight_layout()
    fig.savefig(output_png, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f"  Saved: {output_png}")


def fig3_5_packed_format(output_png):
    """Figure 3.5: INT8 packed data format."""
    fig, ax = plt.subplots(figsize=(10, 2.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.5)
    ax.axis('off')
    ax.set_title('Figure 3.5: Packed INT8 Data Format (WLOAD / DLOAD)', fontsize=13, fontweight='bold')

    fields = [
        (0, 8, 'Value 0\nINT8', '#BDD7EE'),
        (8, 16, 'Value 1\nINT8', '#C5E0B4'),
        (16, 24, 'Value 2\nINT8', '#FCE4D6'),
        (24, 32, 'Value 3\nINT8', '#E4DFEC'),
    ]

    for start, end, label, color in fields:
        draw_box(ax, (31-end)*0.3 + 0.5, 0.8, (end-start)*0.3, 1.0, label, color=color, edgecolor='#333333', fontsize=9)

    # Bit numbers
    bit_positions = [31, 24, 23, 16, 15, 8, 7, 0]
    for bp in bit_positions:
        x = (31-bp)*0.3 + 0.5
        ax.text(x, 2.0, str(bp), ha='center', fontsize=7, color='#666666')

    ax.text(5.3, 0.4, '32-bit register (rs1)', ha='center', fontsize=9, color='#333333')

    plt.tight_layout()
    fig.savefig(output_png, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f"  Saved: {output_png}")


def fig3_6_build_pipeline(output_png):
    """Figure 3.6: FPGA Build Pipeline."""
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis('off')
    ax.set_title('Figure 3.6: FPGA Bitstream Build Pipeline', fontsize=13, fontweight='bold')

    # Software path
    draw_box(ax, 0.3, 2.8, 2.0, 0.8, 'C Source\n(.c + .S)', color='#D6E4F0', edgecolor='#2F5496', fontsize=8, bold=True)
    draw_box(ax, 2.8, 2.8, 1.8, 0.8, 'RISC-V GCC\nCompile + Link', color='#BDD7EE', edgecolor='#4472C4', fontsize=8)
    draw_box(ax, 5.1, 2.8, 1.8, 0.8, 'objcopy\nELF -> Verilog Hex', color='#BDD7EE', edgecolor='#4472C4', fontsize=8)
    draw_box(ax, 7.4, 2.8, 2.3, 0.8, 'ITCM/DTCM\nHex Files\n(64-bit format)', color='#D6E4F0', edgecolor='#2F5496', fontsize=8)

    # Hardware path
    draw_box(ax, 0.3, 0.8, 2.0, 0.8, 'RTL Source\n(.v)', color='#E2EFDA', edgecolor='#548235', fontsize=8, bold=True)
    draw_box(ax, 2.8, 0.8, 1.8, 0.8, 'Vivado\nSynthesis', color='#C5E0B4', edgecolor='#70AD47', fontsize=8)
    draw_box(ax, 5.1, 0.8, 1.8, 0.8, 'Place & Route\n(+ ILA cores)', color='#C5E0B4', edgecolor='#70AD47', fontsize=8)
    draw_box(ax, 7.4, 0.8, 2.3, 0.8, 'Bitstream\nsystem.bit\n+ system.ltx', color='#E2EFDA', edgecolor='#548235', fontsize=8)

    # Merge
    draw_box(ax, 7.4, 2.0, 0.5, 0.5, 'Merge', color='#FFF2CC', edgecolor='#BF8F00', fontsize=7)

    # FPGA
    draw_box(ax, 8.8, 1.5, 1.0, 2.0, 'FPGA\nConfig', color='#FF6B6B', edgecolor='#C00000', fontsize=8, bold=True)

    # Arrows
    draw_arrow(ax, 2.3, 3.2, 2.8, 3.2)
    draw_arrow(ax, 4.6, 3.2, 5.1, 3.2)
    draw_arrow(ax, 6.9, 3.2, 7.4, 3.2)
    draw_arrow(ax, 2.3, 1.2, 2.8, 1.2)
    draw_arrow(ax, 4.6, 1.2, 5.1, 1.2)
    draw_arrow(ax, 6.9, 1.2, 7.4, 1.2)
    draw_arrow(ax, 7.65, 2.5, 7.65, 2.8)
    draw_arrow(ax, 7.65, 1.6, 7.65, 2.0)
    draw_arrow(ax, 7.9, 2.25, 8.8, 2.25)

    # Labels
    ax.text(1.3, 3.8, 'Software Path', fontsize=9, fontweight='bold', color='#2F5496')
    ax.text(1.3, 1.8, 'Hardware Path', fontsize=9, fontweight='bold', color='#548235')

    # PowerShell label
    ax.annotate('Build-CnnAccelDemo.ps1', xy=(3.7, 3.6), fontsize=7, color='#666666')
    ax.annotate('Invoke-Vivado-Fpga.ps1\n-BuildMode cnn_sysclk_ila', xy=(3.7, 1.6), fontsize=7, color='#666666')

    plt.tight_layout()
    fig.savefig(output_png, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f"  Saved: {output_png}")


if __name__ == "__main__":
    print("Generating architecture diagrams...")
    fig3_1_soc_architecture(os.path.join(FIG_DIR, "fig3_1_soc_architecture.png"))
    fig3_2_instruction_format(os.path.join(FIG_DIR, "fig3_2_instruction_format.png"))
    fig3_3_pe_microarchitecture(os.path.join(FIG_DIR, "fig3_3_pe_microarchitecture.png"))
    fig3_4_pe_array(os.path.join(FIG_DIR, "fig3_4_pe_array.png"))
    fig3_5_packed_format(os.path.join(FIG_DIR, "fig3_5_packed_format.png"))
    fig3_6_build_pipeline(os.path.join(FIG_DIR, "fig3_6_build_pipeline.png"))
    print(f"\nAll 6 diagrams saved to: {FIG_DIR}")
