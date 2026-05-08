"""Generate report-ready thesis figures from recorded evidence.

Principles:
- no random or synthetic measurement data;
- one visual scale per chart;
- minimum readable font size for A4 thesis placement;
- explicit QA artifacts for visual review.
"""
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT.parent
FIG_DIR = ROOT / "figures"
QA_DIR = ROOT / ".build" / "figure_qa"
BOARD_0428 = LIB / "04_Experiments" / "Board_BringUp" / "2026-04-28_board_connection_check"
BOARD_0509 = LIB / "04_Experiments" / "Board_BringUp" / "2026-05-09_nice_rs2_fix_verification"

INK = "#1F2933"
MUTED = "#64748B"
GRID = "#CBD5E1"
LINE = "#64748B"
BLUE = "#2F6FB3"
GREEN = "#23835A"
AMBER = "#B7791F"
RED = "#B42318"
VIOLET = "#6B46C1"
GRAY = "#94A3B8"
LIGHT_BLUE = "#DCEBFF"
LIGHT_GREEN = "#DDF4E7"
LIGHT_AMBER = "#FFF1C7"
LIGHT_GRAY = "#EEF2F6"
LIGHT_RED = "#FDE2E2"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 15,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.dpi": 220,
        "savefig.dpi": 300,
        "axes.edgecolor": "#94A3B8",
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
    }
)


@dataclass(frozen=True)
class Resource:
    name: str
    used: float
    available: float
    unit: str
    color: str

    @property
    def pct(self) -> float:
        return 100.0 * self.used / self.available if self.available else 0.0


RESOURCES = [
    Resource("LUT", 13187, 63400, "cells", BLUE),
    Resource("LUTRAM", 2843, 19200, "cells", "#4F83CC"),
    Resource("FF", 12807, 126800, "regs", GREEN),
    Resource("BRAM", 36, 135, "tiles", AMBER),
    Resource("DSP", 0, 240, "slices", GRAY),
    Resource("BUFG", 4, 32, "buffers", VIOLET),
]

TIMING_BUILDS = [
    ("hb_mmcm", 13.887, 0.058, "heartbeat_mmcm_sysclk_ila timing report"),
    ("soc_ila", 13.515, 0.058, "soc_sysclk_ila timing report"),
    ("bootdiag", 13.337, 0.039, "soc_bootdiag_sysclk_ila timing report"),
    ("bootvec", 13.677, 0.061, "bootvec timing_summary.txt"),
    ("hello", 14.204, 0.060, "hello_sysclk_ila timing report"),
    ("cnn_ila", 12.472, 0.057, "cnn_sysclk_ila system_timing_summary_routed.rpt"),
]


def save(fig, name: str):
    out = FIG_DIR / name
    fig.savefig(out, bbox_inches="tight", facecolor="white", pad_inches=0.08)
    plt.close(fig)
    print(f"  saved {out}")


def add_title(ax, title: str, subtitle: str | None = None):
    ax.set_title(title, loc="left", pad=18, fontweight="bold")
    if subtitle:
        ax.text(0.0, 1.015, subtitle, transform=ax.transAxes, ha="left", va="bottom", fontsize=10, color=MUTED)


def clean_axes(ax, grid_axis="y"):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, alpha=0.45, linewidth=0.8)


def load_uart_result():
    text = (BOARD_0509 / "uart_output.txt").read_text(encoding="utf-8")
    def grab(pattern: str) -> str:
        m = re.search(pattern, text)
        if not m:
            raise ValueError(f"Missing UART pattern: {pattern}")
        return m.group(1)

    return {
        "lines": text.strip().splitlines(),
        "cpu_cycles": int(grab(r"CPU reference done, cycles=(\d+)")),
        "acc_cycles": int(grab(r"Accelerator done, cycles=(\d+)")),
        "speedup": float(grab(r"Speedup:\s*([0-9.]+)")),
        "sw": grab(r"SW output:\s*([0-9 ]+)").strip(),
        "hw": grab(r"HW output:\s*([0-9 ]+)").strip(),
        "expected": grab(r"Expected\s*:\s*([0-9 ]+)").strip(),
    }


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


def gen_fig3_2():
    fig, ax = plt.subplots(figsize=(11.2, 3.5))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    ax.text(0, 4.25, "RISC-V custom0 encoding used by the NICE accelerator", fontsize=16, fontweight="bold")
    ax.text(0, 3.88, "funct7 selects the accelerator operation; bits [14:12] carry the NICE xd/xs1/xs2 operand flags.", fontsize=10, color=MUTED)

    fields = [
        (31, 25, "funct7\noperation", LIGHT_BLUE, BLUE),
        (24, 20, "rs2\nindex", LIGHT_GREEN, GREEN),
        (19, 15, "rs1\ndata", LIGHT_GREEN, GREEN),
        (14, 12, "xd xs1 xs2\nflags", LIGHT_AMBER, AMBER),
        (11, 7, "rd\nresult", LIGHT_GREEN, GREEN),
        (6, 0, "opcode\ncustom0", LIGHT_RED, RED),
    ]
    y, h = 1.55, 1.45
    for msb, lsb, label, fc, ec in fields:
        x = lsb
        w = msb - lsb + 1
        ax.add_patch(patches.Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=1.45))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=9.2, fontweight="bold")
        ax.text(x + w / 2, y - 0.28, f"[{msb}:{lsb}]", ha="center", va="top", fontsize=8.6, color=MUTED)
    ax.set_xlim(32, 0)
    ax.text(16, 0.45, "For WLOAD/DLOAD, rs2 is a vector-bank index; index 0 must still be captured after the decoder fix.", ha="center", fontsize=9.5, color=RED, fontweight="bold")
    save(fig, "fig3_2_instruction_format.png")


def gen_fig3_2b_instruction_table():
    rows = [
        ("CFG", "0x0A00100B", "funct7=5", "rs1=config", "Set ReLU/config"),
        ("CLEAR", "0x0800000B", "funct7=4", "-", "Clear accumulators"),
        ("WLOAD", "0x0001800B", "funct7=0", "rs1=data, rs2=index", "Load weight column"),
        ("DLOAD", "0x0201800B", "funct7=1", "rs1=data, rs2=index", "Load activation row"),
        ("COMP", "0x0400000B", "funct7=2", "-", "Start 4x4 MAC"),
        ("RSTAT", "0x0600250B", "funct7=3", "rd=result", "Read result/status"),
    ]
    fig, ax = plt.subplots(figsize=(11.0, 4.7))
    ax.axis("off")
    ax.text(0.0, 1.05, "NICE custom instruction set", transform=ax.transAxes, fontsize=16, fontweight="bold")
    ax.text(0.0, 0.99, "Six custom0 instructions expose configuration, data loading, compute, and readback.", transform=ax.transAxes, fontsize=10, color=MUTED)
    table = ax.table(
        cellText=rows,
        colLabels=["Instruction", "Encoding", "Selector", "Operands", "Role"],
        cellLoc="left",
        colLoc="left",
        colWidths=[0.14, 0.19, 0.17, 0.25, 0.25],
        bbox=[0, 0, 1, 0.91],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(GRID)
        cell.set_linewidth(0.75)
        cell.PAD = 0.12
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


def gen_fig3_5_packed_format():
    fig, ax = plt.subplots(figsize=(11.2, 3.8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.text(0.3, 4.62, "Packed INT8 data format for WLOAD and DLOAD", fontsize=16, fontweight="bold")
    ax.text(0.3, 4.25, "A 32-bit rs1 operand carries four signed INT8 values; rs2 selects the column or row bank.", fontsize=10, color=MUTED)

    x0, y0, w, h = 1.0, 2.18, 3.0, 1.12
    labels = [
        ("Value[3]", "[31:24]", "Byte 3", LIGHT_BLUE, BLUE),
        ("Value[2]", "[23:16]", "Byte 2", LIGHT_GREEN, GREEN),
        ("Value[1]", "[15:8]", "Byte 1", LIGHT_AMBER, AMBER),
        ("Value[0]", "[7:0]", "Byte 0", LIGHT_RED, RED),
    ]
    for i, (name, bits, byte, fc, ec) in enumerate(labels):
        x = x0 + i * w
        ax.add_patch(patches.Rectangle((x, y0), w - 0.08, h, facecolor=fc, edgecolor=ec, linewidth=1.35))
        ax.text(x + (w - 0.08) / 2, y0 + 0.70, f"{name} (INT8)", ha="center", va="center", fontsize=10.2, fontweight="bold")
        ax.text(x + (w - 0.08) / 2, y0 + 0.38, bits, ha="center", va="center", fontsize=10)
        ax.text(x + (w - 0.08) / 2, y0 - 0.28, byte, ha="center", va="top", fontsize=9.2, color=MUTED)
    ax.text(7, 1.02, "Example: rs1 = 0x12_34_AB_CD -> Value[3]=0x12, Value[2]=0x34, Value[1]=0xAB, Value[0]=0xCD", ha="center", fontsize=9.8, bbox=dict(boxstyle="square,pad=0.25", facecolor="#FFF7D6", edgecolor="#D6C27A"))
    ax.annotate("one WLOAD/DLOAD\ntransfers four INT8 values", xy=(1.0, 2.74), xytext=(0.35, 3.65), fontsize=10, color=BLUE, fontweight="bold", arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.4))
    save(fig, "fig3_5_packed_format.png")


def gen_build_pipeline():
    fig, ax = plt.subplots(figsize=(11.6, 4.6))
    ax.axis("off")
    ax.text(0.0, 1.05, "Reproducible FPGA build pipeline", transform=ax.transAxes, fontsize=16, fontweight="bold")
    ax.text(0.0, 0.99, "Inputs, build steps, and evidence outputs are separated so that board results can be reproduced.", transform=ax.transAxes, fontsize=10, color=MUTED)
    stages = [
        ("C / ASM\nfirmware", "ELF + map", LIGHT_BLUE, BLUE),
        ("Image\nconversion", "ITCM/DTCM\nword hex", LIGHT_AMBER, AMBER),
        ("RTL + NICE\nintegration", "E203 SoC\ncnn_nice_core", LIGHT_GREEN, GREEN),
        ("Vivado\nimplementation", "synth / place /\nroute", LIGHT_GRAY, MUTED),
        ("Board\nprogramming", "system.bit\nsystem.ltx", LIGHT_RED, RED),
        ("Evidence\ncapture", "UART log\nILA CSV", "#EDE7FF", VIOLET),
    ]
    xs = np.linspace(0.085, 0.915, len(stages))
    for i, (x, (head, body, fc, ec)) in enumerate(zip(xs, stages)):
        ax.add_patch(patches.Rectangle((x - 0.065, 0.44), 0.13, 0.27, transform=ax.transAxes, facecolor=fc, edgecolor=ec, linewidth=1.25))
        ax.text(x, 0.605, head, transform=ax.transAxes, ha="center", va="center", fontsize=9.4, fontweight="bold", linespacing=1.1)
        ax.text(x, 0.492, body, transform=ax.transAxes, ha="center", va="center", fontsize=8.3, color=MUTED, linespacing=1.1)
        if i < len(stages) - 1:
            ax.annotate("", xy=(xs[i + 1] - 0.073, 0.575), xytext=(x + 0.073, 0.575), xycoords=ax.transAxes, arrowprops=dict(arrowstyle="->", lw=1.3, color=LINE))
    ax.text(0.5, 0.19, "Build modes: soc_sysclk_ila, bootdiag, bootvec, hello, cnn_sysclk_ila", transform=ax.transAxes, ha="center", fontsize=9.3, color=INK)
    save(fig, "fig3_6_build_pipeline.png")


def gen_verification_chain():
    fig, ax = plt.subplots(figsize=(11.4, 4.6))
    ax.axis("off")
    ax.text(0.0, 1.05, "Verification chain closed from RTL to board demo", transform=ax.transAxes, fontsize=16, fontweight="bold")
    ax.text(0.0, 0.99, "Every stage maps to a recorded log, CSV capture, UART output, or commit pair.", transform=ax.transAxes, fontsize=10, color=MUTED)
    stages = [
        ("RTL", "NICE unit\ntests passed", BLUE),
        ("Full-SoC", "SDK simulation\nclosed", BLUE),
        ("hello_e203", "UART + ILA\nboard pass", GREEN),
        ("CNN v1", "HW/SW match\n5.282x", GREEN),
        ("rs2 fix", "decoder patch\nboard regression", RED),
    ]
    xs = np.linspace(0.10, 0.90, len(stages))
    for i, (x, (head, body, color)) in enumerate(zip(xs, stages)):
        ax.add_patch(patches.Circle((x, 0.60), 0.055, transform=ax.transAxes, facecolor=color, edgecolor="white", linewidth=2))
        ax.text(x, 0.60, str(i + 1), transform=ax.transAxes, ha="center", va="center", color="white", fontweight="bold", fontsize=12)
        ax.text(x, 0.41, head, transform=ax.transAxes, ha="center", va="center", fontsize=11, fontweight="bold")
        ax.text(x, 0.28, body, transform=ax.transAxes, ha="center", va="center", fontsize=9, color=MUTED, linespacing=1.15)
        if i < len(stages) - 1:
            ax.annotate("", xy=(xs[i + 1] - 0.065, 0.60), xytext=(x + 0.065, 0.60), xycoords=ax.transAxes, arrowprops=dict(arrowstyle="->", lw=1.5, color=LINE))
    ax.text(0.5, 0.08, "The defense storyline reports completed evidence first; FC acceleration and higher clocking remain future work.", transform=ax.transAxes, ha="center", fontsize=9.2, color=INK)
    save(fig, "fig3_7_verification_chain.png")


def label_panel(ax, text, loc=(0.015, 0.88), color=INK):
    ax.text(
        loc[0],
        loc[1],
        text,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        color=color,
        bbox=dict(facecolor="white", edgecolor=GRID, boxstyle="square,pad=0.18", alpha=0.96),
    )


def gen_ila_pc_trace():
    samples, probes, trigger_idx = load_ila_csv(BOARD_0428 / "hello_e203_board_artifacts" / "ila_capture.csv")
    pc = probes["probe0_pc"]
    status = probes["probe1_status"]
    uart = probes["probe5_uart"]

    fig, axes = plt.subplots(3, 1, figsize=(11.8, 6.4), sharex=True, gridspec_kw={"height_ratios": [1.65, 1, 1]})
    fig.suptitle("hello_e203 board execution observed by ILA", x=0.08, y=0.985, ha="left", fontsize=16, fontweight="bold")
    axes[0].plot(samples, pc, color=BLUE, linewidth=1.0, drawstyle="steps-post")
    axes[0].set_ylabel("PC")
    axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"0x{int(v):08X}"))
    axes[0].set_yticks([pc.min(), pc.max()])
    label_panel(axes[0], "PC remains in ITCM code region", color=BLUE)

    axes[1].plot(samples, status, color=GREEN, linewidth=0.9, drawstyle="steps-post")
    axes[1].set_ylabel("Status")
    axes[1].set_yticks(sorted(set(int(x) for x in status)))
    label_panel(axes[1], "reset released + MMCM locked", color=GREEN)

    axes[2].plot(samples, uart, color=AMBER, linewidth=0.9, drawstyle="steps-post")
    axes[2].set_ylabel("UART")
    axes[2].set_xlabel("Sample index (50 MHz ILA clock)")
    axes[2].set_ylim(float(uart.min()) - 1, float(uart.max()) + 1)
    label_panel(axes[2], "UART TX state captured", color=AMBER)

    if trigger_idx >= 0:
        for ax in axes:
            ax.axvline(trigger_idx, color=RED, linestyle="--", linewidth=1.0, alpha=0.75)
            clean_axes(ax)
    fig.tight_layout(rect=[0.04, 0, 1, 0.94], h_pad=1.0)
    save(fig, "fig4_1_ila_pc_trace.png")


def gen_ila_nice_activity():
    samples, probes, trigger_idx = load_ila_csv(BOARD_0509 / "ila_capture.csv")
    pc = probes["probe0_pc"]
    mem = probes["probe3_pc_activity"]
    nice_hs = probes["probe5_nice_hs"]
    mem_status = probes["probe6_mem_status"]

    fig, axes = plt.subplots(4, 1, figsize=(11.8, 7.4), sharex=True, gridspec_kw={"height_ratios": [1.35, 1.0, 0.88, 0.88]})
    fig.suptitle("CNN v1 board regression after NICE rs2 decoder fix", x=0.08, y=0.985, ha="left", fontsize=16, fontweight="bold")
    axes[0].plot(samples, pc, color=BLUE, linewidth=0.9, drawstyle="steps-post")
    axes[0].set_ylabel("PC")
    axes[0].set_yticks([pc.min(), pc.max()])
    axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"0x{int(v):08X}"))
    label_panel(axes[0], "CPU executes CNN firmware in ITCM", color=BLUE)

    axes[1].plot(samples, mem, color=AMBER, linewidth=0.9, drawstyle="steps-post")
    axes[1].set_ylabel("Mem ref")
    axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"0x{int(v):08X}"))
    label_panel(axes[1], "memory activity counter progresses", color=AMBER)

    axes[2].plot(samples, nice_hs, color=VIOLET, linewidth=1.0, drawstyle="steps-post")
    axes[2].set_ylabel("NICE HS")
    axes[2].set_yticks(sorted(set(int(x) for x in nice_hs)))
    label_panel(axes[2], "sampled window: stable idle handshake", color=VIOLET)

    axes[3].plot(samples, mem_status, color=GREEN, linewidth=1.0, drawstyle="steps-post")
    axes[3].set_ylabel("Bus")
    axes[3].set_xlabel("Sample index (50 MHz ILA clock)")
    axes[3].set_yticks(sorted(set(int(x) for x in mem_status)))
    label_panel(axes[3], "UART log provides pass/fail result", color=GREEN)

    if trigger_idx >= 0:
        for ax in axes:
            ax.axvline(trigger_idx, color=RED, linestyle="--", linewidth=1.0, alpha=0.75)
    for ax in axes:
        clean_axes(ax)
    fig.tight_layout(rect=[0.04, 0, 1, 0.94], h_pad=1.0)
    save(fig, "fig4_2_ila_nice_activity.png")


def gen_uart_output():
    result = load_uart_result()
    fig, ax = plt.subplots(figsize=(10.6, 5.4))
    ax.axis("off")
    ax.text(0.0, 1.05, "UART result summary: CNN v1 demo passed on FPGA", transform=ax.transAxes, fontsize=16, fontweight="bold")
    ax.text(0.0, 0.99, "Rendered from recorded serial output; original UART log is preserved in the evidence package.", transform=ax.transAxes, fontsize=10, color=MUTED)

    ax.add_patch(patches.Rectangle((0.03, 0.16), 0.94, 0.70, transform=ax.transAxes, facecolor="#0B1220", edgecolor="#334155", linewidth=1.4))
    y = 0.79
    for line in result["lines"]:
        color = "#E5E7EB"
        weight = "normal"
        if line.startswith(("SW output", "HW output", "Expected")):
            color = "#BFDBFE"
        if line.startswith("Speedup"):
            color = "#FDE68A"
            weight = "bold"
        if "PASSED" in line:
            color = "#D1FAE5"
            weight = "bold"
        ax.text(0.07, y, line, transform=ax.transAxes, fontfamily="DejaVu Sans Mono", fontsize=11.2, color=color, fontweight=weight)
        y -= 0.057
    ax.text(0.07, 0.075, "Key result: HW output = SW reference = expected values; measured speedup = 5.282x.", transform=ax.transAxes, fontsize=10, color=INK, fontweight="bold")
    save(fig, "fig_uart_output.png")


def gen_speedup():
    result = load_uart_result()
    cpu, acc, speed = result["cpu_cycles"], result["acc_cycles"], result["speedup"]
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    x = np.arange(2)
    labels = ["CPU reference", "NICE accelerator"]
    values = [cpu, acc]
    bars = ax.bar(x, values, color=[GRAY, BLUE], width=0.48)
    add_title(ax, "Convolution benchmark speedup", "Recorded UART cycle counters for the 3x3-on-4x4 INT8 board demo.")
    ax.set_ylabel("Clock cycles")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max(values) * 1.22)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 35, f"{val:,}", ha="center", fontsize=12, fontweight="bold")
    ax.annotate(f"{speed:.3f}x faster", xy=(1, acc), xytext=(1.10, cpu * 0.62), arrowprops=dict(arrowstyle="->", color=RED, lw=1.35), color=RED, fontsize=12, fontweight="bold")
    clean_axes(ax)
    fig.tight_layout()
    save(fig, "fig4_3_speedup_bar.png")


def gen_resource_fit():
    fig, ax = plt.subplots(figsize=(9.6, 5.2))
    names = [r.name for r in RESOURCES]
    pct = [r.pct for r in RESOURCES]
    headroom = [100 - p for p in pct]
    y = np.arange(len(RESOURCES))
    ax.barh(y, pct, color=[r.color for r in RESOURCES], height=0.58, label="Used")
    ax.barh(y, headroom, left=pct, color="#E5EAF1", height=0.58, label="Available headroom")
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Device capacity (%)")
    add_title(ax, "FPGA resource fit on A7-100T", "Each row uses its own Vivado resource capacity; percentages are not mixed across resource types.")
    for yi, r in zip(y, RESOURCES):
        label = f"{r.used:g}/{r.available:g} {r.unit}  ({r.pct:.1f}%)"
        ax.text(min(r.pct + 1.5, 78), yi, label, va="center", fontsize=9.8, fontweight="bold" if r.pct > 0 else "normal")
    ax.legend(loc="lower right", frameon=False)
    clean_axes(ax, "x")
    fig.tight_layout()
    save(fig, "fig4_4_resource_pie.png")


def gen_utilization():
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    resources = [r.name for r in RESOURCES]
    pct = [r.pct for r in RESOURCES]
    y = np.arange(len(resources))
    bars = ax.barh(y, pct, color=[r.color for r in RESOURCES], height=0.58)
    ax.set_yticks(y)
    ax.set_yticklabels(resources)
    ax.invert_yaxis()
    ax.set_xlim(0, 35)
    ax.set_xlabel("Utilization (%)")
    add_title(ax, "Resource utilization by type", "Post-implementation complete SoC; the highest used class remains below 30%.")
    for bar, r in zip(bars, RESOURCES):
        label = f"{r.pct:.1f}%  ({r.used:g} used)"
        ax.text(max(r.pct + 0.8, 1.0), bar.get_y() + bar.get_height() / 2, label, va="center", fontsize=9.8, fontweight="bold" if r.used else "normal")
    ax.axvline(30, color=GRID, linestyle="--", linewidth=1.1)
    ax.text(30.3, -0.55, "30% reference", fontsize=9, color=MUTED)
    clean_axes(ax, "x")
    fig.tight_layout()
    save(fig, "fig4_5_utilization.png")


def gen_timing():
    fig, ax = plt.subplots(figsize=(10.2, 5.4))
    builds = [b[0] for b in TIMING_BUILDS]
    wns = [b[1] for b in TIMING_BUILDS]
    whs = [b[2] for b in TIMING_BUILDS]
    x = np.arange(len(builds))
    ax.plot(x, wns, marker="o", color=BLUE, linewidth=2.0, label="WNS setup slack")
    ax.set_ylabel("WNS setup slack (ns)", color=BLUE)
    ax.tick_params(axis="y", labelcolor=BLUE)
    ax.set_xticks(x)
    ax.set_xticklabels(builds, rotation=20, ha="right")
    ax.set_ylim(12.0, 14.7)
    for xi, val in zip(x, wns):
        ax.text(xi, val + 0.09, f"{val:.2f}", ha="center", fontsize=9.2, color=BLUE)
    ax2 = ax.twinx()
    ax2.bar(x, whs, color=AMBER, alpha=0.38, width=0.42, label="WHS hold slack")
    ax2.set_ylabel("WHS hold slack (ns)", color=AMBER)
    ax2.tick_params(axis="y", labelcolor=AMBER)
    ax2.set_ylim(0, 0.08)
    add_title(ax, "Timing closure across FPGA build modes", "All recorded builds have positive setup and hold slack; no failing endpoints.")
    clean_axes(ax, "y")
    ax2.spines[["top"]].set_visible(False)
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc="upper left", frameon=False)
    fig.tight_layout()
    save(fig, "fig4_6_timing.png")


def write_data_provenance():
    result = load_uart_result()
    data = {
        "uart": {
            "source": str((BOARD_0509 / "uart_output.txt").relative_to(LIB)),
            "cpu_cycles": result["cpu_cycles"],
            "accelerator_cycles": result["acc_cycles"],
            "speedup": result["speedup"],
            "sw_output": result["sw"],
            "hw_output": result["hw"],
            "expected": result["expected"],
        },
        "resources": [
            {"name": r.name, "used": r.used, "available": r.available, "unit": r.unit, "pct": round(r.pct, 3)}
            for r in RESOURCES
        ],
        "timing": [
            {"build": name, "wns_ns": wns, "whs_ns": whs, "source": src}
            for name, wns, whs, src in TIMING_BUILDS
        ],
        "ila": {
            "hello_csv": str((BOARD_0428 / "hello_e203_board_artifacts" / "ila_capture.csv").relative_to(LIB)),
            "cnn_csv": str((BOARD_0509 / "ila_capture.csv").relative_to(LIB)),
        },
    }
    out = QA_DIR / "figure_data_provenance.json"
    QA_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"  saved {out}")


def make_contact_sheet():
    files = [
        "fig3_1_soc_architecture.png",
        "fig3_2_instruction_format.png",
        "fig3_2b_instruction_table.png",
        "fig3_3_pe_microarchitecture.png",
        "fig3_4_pe_array.png",
        "fig3_5_packed_format.png",
        "fig3_6_build_pipeline.png",
        "fig3_7_verification_chain.png",
        "fig4_1_ila_pc_trace.png",
        "fig4_2_ila_nice_activity.png",
        "fig_uart_output.png",
        "fig4_3_speedup_bar.png",
        "fig4_4_resource_pie.png",
        "fig4_5_utilization.png",
        "fig4_6_timing.png",
    ]
    QA_DIR.mkdir(parents=True, exist_ok=True)
    label_font = ImageFont.truetype("arial.ttf", 22)
    meta_font = ImageFont.truetype("arial.ttf", 16)
    thumbs = []
    for name in files:
        path = FIG_DIR / name
        im = Image.open(path).convert("RGB")
        th = im.copy()
        th.thumbnail((760, 470), Image.LANCZOS)
        canvas = Image.new("RGB", (820, 545), "white")
        canvas.paste(th, ((820 - th.width) // 2, 42))
        draw = ImageDraw.Draw(canvas)
        draw.text((20, 10), name, fill=(0, 0, 0), font=label_font)
        draw.text((20, 515), f"{im.width}x{im.height}", fill=(80, 80, 80), font=meta_font)
        thumbs.append(canvas)
    cols = 2
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 820, rows * 545), "white")
    for i, th in enumerate(thumbs):
        sheet.paste(th, ((i % cols) * 820, (i // cols) * 545))
    out = QA_DIR / "all_figures_contact_sheet.png"
    sheet.save(out)
    print(f"  saved {out}")


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating thesis figures into {FIG_DIR}")
    gen_fig3_2()
    gen_fig3_2b_instruction_table()
    gen_fig3_5_packed_format()
    gen_build_pipeline()
    gen_verification_chain()
    gen_ila_pc_trace()
    gen_ila_nice_activity()
    gen_uart_output()
    gen_speedup()
    gen_resource_fit()
    gen_utilization()
    gen_timing()
    write_data_provenance()
    make_contact_sheet()
    print("Done.")


if __name__ == "__main__":
    main()
