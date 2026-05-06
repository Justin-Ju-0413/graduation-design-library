#!/usr/bin/env python
"""ILA Waveform Renderer — Publication-quality figures for academic papers.
Usage: python render_ila_waveforms.py <csv_path> <mode> [output.png]
Modes: pc_trace | nice_activity
"""
import csv, sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

plt.rcParams.update({
    "font.family": "serif", "font.size": 9,
    "axes.titlesize": 10, "axes.labelsize": 9,
    "figure.dpi": 200, "savefig.dpi": 200,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.08,
})


def parse_csv(path):
    with open(path, encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    headers = rows[0]
    data = {h: [] for h in headers[3:]}
    for row in rows[2:]:
        for i, h in enumerate(headers[3:], start=3):
            v = row[i].strip()
            if v and all(c in "xXzZ" for c in v):
                v = "0"
            data[h].append(v)
    return headers, data, len(rows) - 2


def find_probe(data, fragment):
    for k in data:
        if fragment in k.lower():
            return k
    return None


def to_int_arr(data, key):
    return np.array([int(v, 16) if v.strip() else 0 for v in data[key]])


def _draw_trigger(axes, pos):
    for ax in axes:
        ax.axvline(x=pos, color="#E53935", linewidth=0.8, linestyle="--", alpha=0.6)


# ═══════════════════════════════════════════════
# Fig 4.1: PC Boot Trace
# ═══════════════════════════════════════════════
def render_pc_trace(csv_path, out_path):
    _, data, n = parse_csv(csv_path)

    probes = {
        "pc": find_probe(data, "pc"),
        "status": find_probe(data, "status"),
        "uart": find_probe(data, "uart"),
        "membus": find_probe(data, "membus_live"),
    }
    if not all(probes.values()):
        print("[!] Missing probes:", list(data.keys()))
        sys.exit(1)

    pc = to_int_arr(data, probes["pc"])
    status = to_int_arr(data, probes["status"])
    uart = to_int_arr(data, probes["uart"])
    membus = to_int_arr(data, probes["membus"])
    t = np.arange(n)
    trg = n // 10

    fig, axes = plt.subplots(4, 1, figsize=(10, 6.5))

    ax = axes[0]
    ax.step(t, pc, where="mid", color="#333333", linewidth=0.6)
    ax.set_ylabel("PC [hex]", fontsize=9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"0x{int(v):08X}"))
    ax.yaxis.set_major_locator(MaxNLocator(5))
    ax.grid(True, alpha=0.15, linewidth=0.3)
    ax.set_title("ILA Capture: hello_e203 Boot Sequence (PC Progression)", fontsize=10, fontweight="bold")

    ax = axes[1]
    ax.step(t, status, where="mid", color="#4CAF50", linewidth=0.8)
    ax.set_ylabel("Status", fontsize=9)
    ax.yaxis.set_major_locator(MaxNLocator(5))
    ax.grid(True, alpha=0.15, linewidth=0.3)

    ax = axes[2]
    ax.step(t, uart, where="mid", color="#FF9800", linewidth=0.8)
    ax.set_ylabel("UART", fontsize=9)
    ax.yaxis.set_major_locator(MaxNLocator(5))
    ax.grid(True, alpha=0.15, linewidth=0.3)

    ax = axes[3]
    ax.step(t, membus, where="mid", color="#9C27B0", linewidth=0.8)
    ax.set_ylabel("Membus Live", fontsize=9)
    ax.set_xlabel("Sample", fontsize=9)
    ax.yaxis.set_major_locator(MaxNLocator(5))
    ax.grid(True, alpha=0.15, linewidth=0.3)

    _draw_trigger(axes, trg)
    plt.subplots_adjust(hspace=0.25)
    plt.savefig(out_path, facecolor="white", edgecolor="none")
    plt.close()
    print(f"[OK] PC trace: {out_path}")


# ═══════════════════════════════════════════════
# Fig 4.2: NICE CNN Accelerator Activity
# ═══════════════════════════════════════════════
def render_nice_activity(csv_path, out_path):
    _, data, n = parse_csv(csv_path)

    probes = {
        "pc": find_probe(data, "pc"),
        "csr": find_probe(data, "nice_csr"),
        "hs": find_probe(data, "nice_hs"),
        "live": find_probe(data, "liveness") or find_probe(data, "mem_status") or find_probe(data, "flags"),
    }
    if not all([probes["pc"], probes["csr"], probes["hs"]]):
        print("[!] Missing probes:", list(data.keys()))
        sys.exit(1)

    pc = to_int_arr(data, probes["pc"])
    csr = to_int_arr(data, probes["csr"])
    hs = to_int_arr(data, probes["hs"])
    live = to_int_arr(data, probes["live"]) if probes["live"] else np.zeros(n)
    t = np.arange(n)
    trg = n // 10

    fig, axes = plt.subplots(4, 1, figsize=(10, 6.5))

    ax = axes[0]
    ax.step(t, pc, where="mid", color="#1E88E5", linewidth=0.6)
    ax.set_ylabel("PC [hex]", fontsize=9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"0x{int(v):08X}"))
    ax.yaxis.set_major_locator(MaxNLocator(4))
    ax.grid(True, alpha=0.15, linewidth=0.3)
    ax.set_title("ILA Capture: NICE CNN Accelerator Instruction Execution", fontsize=10, fontweight="bold")

    ax = axes[1]
    ax.step(t, csr, where="mid", color="#FF9800", linewidth=0.8)
    ax.set_ylabel("NICE CSR", fontsize=9)
    ax.yaxis.set_major_locator(MaxNLocator(4))
    ax.grid(True, alpha=0.15, linewidth=0.3)

    ax = axes[2]
    ax.step(t, hs, where="mid", color="#4CAF50", linewidth=0.8)
    ax.set_ylabel("NICE HS", fontsize=9)
    ax.yaxis.set_major_locator(MaxNLocator(4))
    ax.grid(True, alpha=0.15, linewidth=0.3)

    ax = axes[3]
    ax.step(t, live, where="mid", color="#AB47BC", linewidth=0.6)
    ax.set_ylabel("Liveness", fontsize=9)
    ax.set_xlabel("Sample", fontsize=9)
    ax.yaxis.set_major_locator(MaxNLocator(4))
    ax.grid(True, alpha=0.15, linewidth=0.3)

    _draw_trigger(axes, trg)
    plt.subplots_adjust(hspace=0.25)
    plt.savefig(out_path, facecolor="white", edgecolor="none")
    plt.close()
    print(f"[OK] NICE activity: {out_path}")


# ═══════════════════════════════════════════════
def main():
    if len(sys.argv) < 3:
        print("Usage: python render_ila_waveforms.py <csv> <pc_trace|nice_activity> [out.png]")
        sys.exit(1)
    csv_path = sys.argv[1]
    mode = sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else csv_path.replace(".csv", f"_{mode}.png")
    if mode == "pc_trace":
        render_pc_trace(csv_path, out)
    elif mode == "nice_activity":
        render_nice_activity(csv_path, out)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
