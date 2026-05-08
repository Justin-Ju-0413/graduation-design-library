"""Generate report-ready thesis figures from real project evidence.

All measured values are taken from existing logs, CSV exports, or recorded
board output. This script intentionally avoids random or synthetic data.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path
from textwrap import wrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT.parent
FIG_DIR = ROOT / "figures"
BOARD_0428 = LIB / "04_Experiments" / "Board_BringUp" / "2026-04-28_board_connection_check"
BOARD_0509 = LIB / "04_Experiments" / "Board_BringUp" / "2026-05-09_nice_rs2_fix_verification"

INK = "#1F2933"
MUTED = "#5B6773"
GRID = "#CBD5E1"
BLUE = "#2F6FB3"
GREEN = "#23835A"
AMBER = "#B7791F"
RED = "#B42318"
VIOLET = "#6B46C1"
LIGHT_BLUE = "#D7E8FF"
LIGHT_GREEN = "#DDF4E7"
LIGHT_AMBER = "#FFF0C2"
LIGHT_GRAY = "#EEF2F6"

plt.rcParams.update(
    {
        "font.family": "DejaVu Serif",
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.labelsize": 10,
        "figure.dpi": 220,
        "savefig.dpi": 260,
        "axes.edgecolor": "#94A3B8",
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
    }
)


def save(fig, name: str):
    out = FIG_DIR / name
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved {out}")


def load_ila_csv(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        next(reader)
        rows.extend(row for row in reader if len(row) >= 3)
    samples = np.arange(len(rows))
    probes = {h.split("[")[0].strip(): np.zeros(len(rows), dtype=np.int64) for h in header[3:]}
    trigger_idx = -1
    for i, row in enumerate(rows):
        if row[2] == "1":
            trigger_idx = i
        for j, name in enumerate(probes.keys()):
            probes[name][i] = int(row[3 + j], 16)
    return samples, probes, trigger_idx


def label_panel(ax, text, loc=(0.01, 0.94), color=INK):
    ax.text(
        loc[0],
        loc[1],
        text,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8.5,
        color=color,
        bbox=dict(facecolor="white", edgecolor="#CBD5E1", boxstyle="square,pad=0.25", alpha=0.95),
    )


def gen_fig3_2():
    fig, ax = plt.subplots(figsize=(10.2, 3.0))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.text(0, 3.72, "RISC-V custom0 encoding used by the NICE accelerator", fontsize=14, fontweight="bold")
    ax.text(0, 3.38, "Instruction identity is carried by funct7; bits [14:12] are interpreted as xd/xs1/xs2 control flags.", fontsize=8.8, color=MUTED)

    fields = [
        (31, 25, "funct7\ninstruction ID", LIGHT_BLUE, BLUE),
        (24, 20, "rs2\nindex/data", LIGHT_GREEN, GREEN),
        (19, 15, "rs1\ndata", LIGHT_GREEN, GREEN),
        (14, 12, "xd xs1 xs2\nNICE flags", LIGHT_AMBER, AMBER),
        (11, 7, "rd\nresult", LIGHT_GREEN, GREEN),
        (6, 0, "opcode\ncustom0=0x0B", "#FDE2E2", RED),
    ]
    y, h = 1.25, 1.4
    for msb, lsb, label, fc, ec in fields:
        x = lsb
        w = msb - lsb + 1
        ax.add_patch(patches.Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=1.5))
        ax.text(x + w / 2, y + h / 2 + 0.12, label, ha="center", va="center", fontsize=8.4, fontweight="bold")
        ax.text(x + w / 2, y - 0.20, f"[{msb}:{lsb}]", ha="center", va="top", fontsize=8, color=MUTED)
    ax.set_xlim(32, 0)
    ax.text(16, 0.28, "xs2=1 forces rs2 capture for WLOAD/DLOAD, including index 0 after the decoder fix.", ha="center", fontsize=8.6, color=RED)
    save(fig, "fig3_2_instruction_format.png")


def gen_fig3_2b_instruction_table():
    rows = [
        ("CFG", "0x0A00100B", "funct7=5", "rs1=config", "Set ReLU/config"),
        ("CLEAR", "0x0800000B", "funct7=4", "-", "Clear accumulators"),
        ("WLOAD", "0x0001800B", "funct7=0", "rs1=data, rs2=index", "Load one weight column"),
        ("DLOAD", "0x0201800B", "funct7=1", "rs1=data, rs2=index", "Load one activation row"),
        ("COMP", "0x0400000B", "funct7=2", "-", "Start 4x4 MAC"),
        ("RSTAT", "0x0600250B", "funct7=3", "rd=result", "Read result/status"),
    ]
    fig, ax = plt.subplots(figsize=(10.2, 4.4))
    ax.axis("off")
    ax.text(0.0, 1.04, "NICE custom instruction set", transform=ax.transAxes, fontsize=14, fontweight="bold")
    ax.text(0.0, 0.985, "Six custom0 instructions expose configuration, data loading, compute, and readback.", transform=ax.transAxes, fontsize=8.8, color=MUTED)
    table = ax.table(
        cellText=rows,
        colLabels=["Instruction", "Encoding", "Selector", "Operands", "Role"],
        cellLoc="left",
        colLoc="left",
        colWidths=[0.14, 0.19, 0.17, 0.24, 0.26],
        bbox=[0, 0, 1, 0.90],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.8)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#CBD5E1")
        cell.set_linewidth(0.7)
        if r == 0:
            cell.set_facecolor("#E2E8F0")
            cell.set_text_props(fontweight="bold", color=INK)
        elif r in (3, 4):
            cell.set_facecolor("#F7FCFA")
        else:
            cell.set_facecolor("white")
        if c == 0 and r > 0:
            cell.set_text_props(fontweight="bold", color=BLUE)
    save(fig, "fig3_2b_instruction_table.png")


def gen_ila_pc_trace():
    samples, probes, trigger_idx = load_ila_csv(BOARD_0428 / "hello_e203_board_artifacts" / "ila_capture.csv")
    pc = probes["probe0_pc"]
    status = probes["probe1_status"]
    uart = probes["probe5_uart"]

    fig, axes = plt.subplots(3, 1, figsize=(11.2, 6.0), sharex=True, gridspec_kw={"height_ratios": [1.7, 1, 1]})
    fig.suptitle("hello_e203 board execution observed by ILA", x=0.02, y=0.995, ha="left", fontsize=14, fontweight="bold")
    axes[0].plot(samples, pc, color=BLUE, linewidth=1.0, drawstyle="steps-post")
    axes[0].set_ylabel("PC")
    axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"0x{int(v):08X}"))
    axes[0].set_yticks([pc.min(), pc.max()])
    axes[0].grid(True, color=GRID, alpha=0.35)
    label_panel(axes[0], "PC stays in ITCM code region\n0x800000a0-0x800000be", color=BLUE)

    axes[1].plot(samples, status, color=GREEN, linewidth=0.9, drawstyle="steps-post")
    axes[1].set_ylabel("Status")
    axes[1].set_yticks(sorted(set(int(x) for x in status)))
    axes[1].grid(True, color=GRID, alpha=0.35)
    label_panel(axes[1], "reset released + MMCM locked", color=GREEN)

    axes[2].plot(samples, uart, color=AMBER, linewidth=0.9, drawstyle="steps-post")
    axes[2].set_ylabel("UART")
    axes[2].set_xlabel("Sample index (50 MHz ILA clock)")
    axes[2].grid(True, color=GRID, alpha=0.35)
    label_panel(axes[2], "UART TX activity detected", color=AMBER)

    if trigger_idx >= 0:
        for ax in axes:
            ax.axvline(trigger_idx, color=RED, linestyle="--", linewidth=1.0, alpha=0.8)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    save(fig, "fig4_1_ila_pc_trace.png")


def gen_ila_nice_activity():
    samples, probes, trigger_idx = load_ila_csv(BOARD_0509 / "ila_capture.csv")
    pc = probes["probe0_pc"]
    mem = probes["probe3_pc_activity"]
    nice_hs = probes["probe5_nice_hs"]
    mem_status = probes["probe6_mem_status"]

    fig, axes = plt.subplots(4, 1, figsize=(11.2, 7.2), sharex=True, gridspec_kw={"height_ratios": [1.45, 1.0, 0.9, 0.9]})
    fig.suptitle("CNN v1 board regression after NICE rs2 decoder fix", x=0.02, y=0.995, ha="left", fontsize=14, fontweight="bold")
    axes[0].plot(samples, pc, color=BLUE, linewidth=0.8, drawstyle="steps-post")
    axes[0].set_ylabel("PC")
    axes[0].set_yticks([pc.min(), pc.max()])
    axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"0x{int(v):08X}"))
    axes[0].grid(True, color=GRID, alpha=0.35)
    label_panel(axes[0], "CPU executes CNN firmware in ITCM", color=BLUE)

    axes[1].plot(samples, mem, color=AMBER, linewidth=0.8, drawstyle="steps-post")
    axes[1].set_ylabel("Mem ref")
    axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"0x{int(v):08X}"))
    axes[1].grid(True, color=GRID, alpha=0.35)
    label_panel(axes[1], "memory activity continues through the run", color=AMBER)

    axes[2].plot(samples, nice_hs, color=VIOLET, linewidth=0.9, drawstyle="steps-post")
    axes[2].set_ylabel("NICE HS")
    axes[2].set_yticks(sorted(set(int(x) for x in nice_hs)))
    axes[2].grid(True, color=GRID, alpha=0.35)
    label_panel(axes[2], "capture window shows stable idle handshake", color=VIOLET)

    axes[3].plot(samples, mem_status, color=GREEN, linewidth=0.9, drawstyle="steps-post")
    axes[3].set_ylabel("Bus")
    axes[3].set_xlabel("Sample index (50 MHz ILA clock)")
    axes[3].set_yticks(sorted(set(int(x) for x in mem_status)))
    axes[3].grid(True, color=GRID, alpha=0.35)
    label_panel(axes[3], "board run verified by UART output", color=GREEN)

    if trigger_idx >= 0:
        for ax in axes:
            ax.axvline(trigger_idx, color=RED, linestyle="--", linewidth=1.0, alpha=0.8)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    save(fig, "fig4_2_ila_nice_activity.png")


def gen_speedup():
    fig, ax = plt.subplots(figsize=(8.0, 4.3))
    labels = ["CPU reference", "NICE accelerator"]
    values = [1516, 287]
    bars = ax.bar(labels, values, color=["#94A3B8", BLUE], width=0.42)
    ax.set_ylabel("Clock cycles")
    ax.set_title("Convolution benchmark: 5.282x speedup", loc="left", fontsize=14, fontweight="bold")
    ax.text(0.0, 1.02, "3x3 convolution on a 4x4 INT8 input; measured on the board demo.", transform=ax.transAxes, fontsize=8.8, color=MUTED)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 45, f"{val:,}", ha="center", fontsize=11, fontweight="bold")
    ax.annotate("5.282x faster", xy=(1, 287), xytext=(0.58, 1050), arrowprops=dict(arrowstyle="->", color=RED, lw=1.4), color=RED, fontsize=11, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=GRID, alpha=0.35)
    ax.set_ylim(0, 1750)
    save(fig, "fig4_3_speedup_bar.png")


def gen_resource_pie():
    labels = ["LUT", "FF", "BRAM", "Other headroom"]
    sizes = [20.8, 10.1, 26.3, 42.8]
    colors = [BLUE, GREEN, AMBER, "#E2E8F0"]
    fig, ax = plt.subplots(figsize=(6.8, 5.4))
    wedges, texts, autotexts = ax.pie(
        sizes,
        colors=colors,
        startangle=120,
        counterclock=False,
        autopct="%1.1f%%",
        pctdistance=0.73,
        wedgeprops=dict(width=0.42, edgecolor="white"),
    )
    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(0.98, 0.50), frameon=False, fontsize=9)
    for t in autotexts:
        t.set_fontsize(9)
        t.set_fontweight("bold")
        t.set_color(INK)
    ax.text(0, 0.08, "A7-100T\nfit", ha="center", va="center", fontsize=18, fontweight="bold")
    ax.text(0, -0.18, "post-placement", ha="center", va="center", fontsize=8.5, color=MUTED)
    ax.set_title("Complete SoC resource footprint", loc="left", fontsize=14, fontweight="bold")
    save(fig, "fig4_4_resource_pie.png")


def gen_utilization():
    resources = ["LUT", "LUTRAM", "FF", "BRAM", "DSP", "BUFG"]
    pct = [20.8, 14.8, 10.1, 26.7, 0.0, 12.5]
    used = ["13,187", "2,843", "12,807", "36", "0", "4"]
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    y = np.arange(len(resources))
    bars = ax.barh(y, pct, color=[BLUE, BLUE, GREEN, AMBER, "#94A3B8", VIOLET], height=0.52)
    ax.set_yticks(y)
    ax.set_yticklabels(resources)
    ax.invert_yaxis()
    ax.set_xlim(0, 35)
    ax.set_xlabel("Utilization (%)")
    ax.set_title("FPGA utilization leaves headroom for future expansion", loc="left", fontsize=14, fontweight="bold")
    ax.text(0.0, 1.02, "Post-implementation complete SoC on xc7a100tfgg484-2.", transform=ax.transAxes, fontsize=8.8, color=MUTED)
    for bar, p, u in zip(bars, pct, used):
        ax.text(max(p + 0.8, 1.0), bar.get_y() + bar.get_height() / 2, f"{p:.1f}%  ({u} used)", va="center", fontsize=9, fontweight="bold" if p > 0 else "normal")
    ax.axvline(30, color=GRID, linestyle="--", linewidth=1.0)
    ax.text(30.2, -0.55, "30% reference", fontsize=8, color=MUTED)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", color=GRID, alpha=0.35)
    save(fig, "fig4_5_utilization.png")


def gen_timing():
    builds = ["hb_mmcm", "soc_ila", "bootdiag", "bootvec", "hello", "cnn_ila"]
    wns = [13.887, 13.515, 13.337, 13.677, 14.204, 13.512]
    whs = [0.061, 0.058, 0.039, 0.061, 0.060, 0.056]
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    x = np.arange(len(builds))
    ax.plot(x, wns, marker="o", color=BLUE, linewidth=2.0, label="WNS setup slack")
    ax.set_ylabel("WNS (ns)", color=BLUE)
    ax.tick_params(axis="y", labelcolor=BLUE)
    ax.set_xticks(x)
    ax.set_xticklabels(builds, rotation=15, ha="right")
    ax.grid(axis="y", color=GRID, alpha=0.35)
    ax2 = ax.twinx()
    ax2.bar(x, whs, color=AMBER, alpha=0.35, width=0.42, label="WHS hold slack")
    ax2.set_ylabel("WHS (ns)", color=AMBER)
    ax2.tick_params(axis="y", labelcolor=AMBER)
    for xi, val in zip(x, wns):
        ax.text(xi, val + 0.18, f"{val:.2f}", ha="center", fontsize=8.2, color=BLUE)
    ax.set_title("All FPGA build modes meet timing", loc="left", fontsize=14, fontweight="bold")
    ax.text(0.0, 1.02, "Positive setup and hold slack across diagnostic and CNN board builds.", transform=ax.transAxes, fontsize=8.8, color=MUTED)
    ax.spines[["top", "right"]].set_visible(False)
    ax2.spines[["top"]].set_visible(False)
    save(fig, "fig4_6_timing.png")


def gen_uart_output():
    text_path = BOARD_0509 / "uart_output.txt"
    lines = text_path.read_text(encoding="utf-8").strip().splitlines()
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.axis("off")
    ax.text(0.0, 1.02, "UART result summary: CNN v1 demo passed on FPGA", transform=ax.transAxes, fontsize=14, fontweight="bold")
    ax.text(0.0, 0.965, "Rendered from recorded serial output; original terminal log is preserved in the evidence package.", transform=ax.transAxes, fontsize=8.8, color=MUTED)

    ax.add_patch(patches.Rectangle((0.02, 0.12), 0.96, 0.75, transform=ax.transAxes, facecolor="#0B1220", edgecolor="#334155", linewidth=1.4))
    y = 0.80
    for line in lines:
        color = "#D1FAE5" if "PASSED" in line else "#E5E7EB"
        weight = "bold" if "PASSED" in line or "Speedup" in line or "HW output" in line else "normal"
        if line.startswith("SW output") or line.startswith("HW output") or line.startswith("Expected"):
            color = "#BFDBFE"
        if line.startswith("Speedup"):
            color = "#FDE68A"
        ax.text(0.06, y, line, transform=ax.transAxes, fontfamily="DejaVu Sans Mono", fontsize=10.5, color=color, fontweight=weight)
        y -= 0.055
    ax.text(0.06, 0.065, "Key result: HW output = SW reference = expected values; measured speedup = 5.282x.", transform=ax.transAxes, fontsize=9.2, color=INK, fontweight="bold")
    save(fig, "fig_uart_output.png")


def gen_verification_chain():
    fig, ax = plt.subplots(figsize=(10.5, 4.0))
    ax.axis("off")
    ax.text(0.0, 1.03, "Verification chain closed from RTL to board demo", transform=ax.transAxes, fontsize=14, fontweight="bold")
    ax.text(0.0, 0.97, "Each stage is backed by a specific log, CSV capture, UART output, or commit pair.", transform=ax.transAxes, fontsize=8.8, color=MUTED)
    stages = [
        ("RTL", "NICE unit tests\npassed", BLUE),
        ("Full-SoC", "SDK simulation\nclosed", BLUE),
        ("hello_e203", "UART + ILA\nboard pass", GREEN),
        ("CNN v1", "HW/SW match\n5.282x", GREEN),
        ("rs2 fix", "decoder patch\nboard regression", RED),
    ]
    xs = np.linspace(0.09, 0.91, len(stages))
    for i, (x, (title, body, color)) in enumerate(zip(xs, stages)):
        ax.add_patch(patches.Circle((x, 0.56), 0.055, transform=ax.transAxes, facecolor=color, edgecolor="white", linewidth=2))
        ax.text(x, 0.56, str(i + 1), transform=ax.transAxes, ha="center", va="center", color="white", fontweight="bold", fontsize=12)
        ax.text(x, 0.38, title, transform=ax.transAxes, ha="center", va="center", fontsize=10.5, fontweight="bold")
        ax.text(x, 0.26, body, transform=ax.transAxes, ha="center", va="center", fontsize=8.4, color=MUTED)
        if i < len(stages) - 1:
            ax.annotate("", xy=(xs[i + 1] - 0.06, 0.56), xytext=(x + 0.06, 0.56), xycoords=ax.transAxes, arrowprops=dict(arrowstyle="->", lw=1.5, color="#94A3B8"))
    ax.text(0.5, 0.075, "Reporting line: completed results are separated from future work on FC acceleration and higher-frequency operation.", transform=ax.transAxes, ha="center", fontsize=8.6, color=INK)
    save(fig, "fig3_7_verification_chain.png")


def gen_build_pipeline():
    fig, ax = plt.subplots(figsize=(10.2, 4.1))
    ax.axis("off")
    ax.text(0.0, 1.03, "Reproducible FPGA build pipeline", transform=ax.transAxes, fontsize=14, fontweight="bold")
    ax.text(0.0, 0.97, "Software image, RTL, constraints, and ILA probes are assembled into a board-programmable bitstream.", transform=ax.transAxes, fontsize=8.8, color=MUTED)
    stages = [
        ("C / ASM\nfirmware", "ELF + map"),
        ("Image\nconversion", "ITCM/DTCM\nword hex"),
        ("RTL + NICE\nintegration", "E203 SoC\ncnn_nice_core"),
        ("Vivado\nimplementation", "synth/place/route"),
        ("Board\nprogramming", "system.bit\nsystem.ltx"),
        ("Evidence\ncapture", "UART + ILA CSV"),
    ]
    xs = np.linspace(0.08, 0.92, len(stages))
    for i, (x, (title, body)) in enumerate(zip(xs, stages)):
        ax.add_patch(patches.Rectangle((x - 0.065, 0.42), 0.13, 0.25, transform=ax.transAxes, facecolor=[LIGHT_BLUE, LIGHT_AMBER, LIGHT_GREEN, LIGHT_GRAY, "#FDE2E2", "#E9E2FF"][i], edgecolor="#64748B", linewidth=1.2))
        ax.text(x, 0.575, title, transform=ax.transAxes, ha="center", va="center", fontsize=8.5, fontweight="bold")
        ax.text(x, 0.475, body, transform=ax.transAxes, ha="center", va="center", fontsize=7.6, color=MUTED)
        if i < len(stages) - 1:
            ax.annotate("", xy=(xs[i + 1] - 0.073, 0.545), xytext=(x + 0.073, 0.545), xycoords=ax.transAxes, arrowprops=dict(arrowstyle="->", lw=1.2, color="#64748B"))
    ax.text(0.5, 0.20, "Diagnostic modes: soc_sysclk_ila, bootdiag, bootvec, hello, cnn_sysclk_ila", transform=ax.transAxes, ha="center", fontsize=8.6, color=INK)
    save(fig, "fig3_6_build_pipeline.png")


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating unified report figures into {FIG_DIR}")
    gen_fig3_2()
    gen_fig3_2b_instruction_table()
    gen_build_pipeline()
    gen_verification_chain()
    gen_ila_pc_trace()
    gen_ila_nice_activity()
    gen_uart_output()
    gen_speedup()
    gen_resource_pie()
    gen_utilization()
    gen_timing()
    print("Done.")


if __name__ == "__main__":
    main()
