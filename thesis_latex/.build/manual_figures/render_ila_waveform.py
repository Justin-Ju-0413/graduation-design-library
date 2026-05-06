"""
ILA CSV → 论文波形 PNG 渲染器
用法: python render_ila_waveform.py <csv路径> <输出png路径> <模式>
模式: pc_trace | nice_activity
"""

import csv
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ---------- 解析 ILA CSV ----------

def parse_ila_csv(path):
    with open(path) as f:
        reader = csv.reader(f)
        rows = list(reader)

    headers = rows[0]
    radix   = rows[1]

    # 解析采样点
    samples = {}
    for h in headers[3:]:  # 跳过头三列 (Sample in Buffer, Sample in Window, TRIGGER)
        samples[h] = []

    for row in rows[2:]:
        for i, h in enumerate(headers[3:], start=3):
            val = row[i].strip()
            # 处理 X (unknown) 状态
            if all(c in 'xXzZ' for c in val):
                val = '0'
            samples[h].append(val)

    return headers, radix, samples, len(rows) - 2

# ---------- 值转换 ----------

def hex_to_int(hex_str):
    try:
        return int(hex_str, 16)
    except ValueError:
        return 0

def hex_to_bits(hex_str, width):
    """将 hex 转为 bit 列表 [MSB ... LSB]"""
    try:
        val = int(hex_str, 16)
        bits = [(val >> i) & 1 for i in range(width - 1, -1, -1)]
        return bits
    except ValueError:
        return [0] * width

# ---------- 绘图 ----------

def setup_academic_style():
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "figure.dpi": 200,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
    })


def draw_bus_signal(ax, t, values, y_pos, label, radix="HEX", color="#1a1a2e"):
    """绘制总线信号 (如 PC 地址)"""
    int_vals = []
    for v in values:
        if radix == "HEX":
            int_vals.append(hex_to_int(v))
        else:
            try:
                int_vals.append(int(v))
            except ValueError:
                int_vals.append(0)

    int_vals = np.array(int_vals)
    ax.step(t, int_vals, where="mid", color=color, linewidth=0.6)

    ax.set_ylabel(label, fontsize=8)
    ax.yaxis.set_label_position("left")

    # 根据数据范围自动设 y 轴
    vmin, vmax = int_vals.min(), int_vals.max()
    margin = max((vmax - vmin) * 0.1, 1)
    ax.set_ylim(vmin - margin, vmax + margin)

    ax.tick_params(axis="y", labelsize=7)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"0x{int(v):08X}" if abs(v) >= 2**20 else f"0x{int(v):X}"))
    ax.grid(True, alpha=0.2, linewidth=0.3)


def draw_bit_signal(ax, t, values, y_pos, label, bit_idx, color="#1a1a2e"):
    """绘制单 bit 数字信号 (0/1)"""
    bits = []
    for v in values:
        bits.append(hex_to_int(v) if isinstance(v, str) else v)
    bits = np.array(bits)

    # 对于多 bit 总线，提取指定位
    if bits.dtype == np.int64 or bits.dtype == np.int32:
        # 单值，画 0/1
        pass
    else:
        pass

    # 将值转为 bit 并阶梯绘制
    ax.step(t, bits, where="mid", color=color, linewidth=0.8)
    ax.set_ylabel(label, fontsize=8)
    ax.set_ylim(-0.2, max(bits.max(), 1) + 0.5)
    ax.set_yticks([0, 1])
    ax.grid(True, alpha=0.2, linewidth=0.3)


def draw_multi_bit(ax, t, values, label, width, color="#1a1a2e"):
    """绘制窄总线信号 (2-8 bit)"""
    int_vals = [hex_to_int(v) for v in values]
    int_vals = np.array(int_vals)
    ax.step(t, int_vals, where="mid", color=color, linewidth=0.6)
    ax.set_ylabel(label, fontsize=8)
    vmin, vmax = 0, max(int_vals.max(), 1)
    ax.set_ylim(vmin - 0.2, vmax + 0.5)
    ax.grid(True, alpha=0.2, linewidth=0.3)


# ---------- 渲染模式 ----------

def render_pc_trace(samples, n_samples, out_path):
    """Fig 4.1: PC 追踪波形"""
    t = np.arange(n_samples)
    n_signals = 1
    fig, axes = plt.subplots(n_signals, 1, figsize=(7, 1.8), sharex=True)
    if n_signals == 1:
        axes = [axes]

    probe_name = "probe0_pc[31:0]"
    values = samples[probe_name]
    int_vals = np.array([hex_to_int(v) for v in values])
    axes[0].step(t, int_vals, where="mid", color="#1a1a2e", linewidth=0.5)
    axes[0].set_ylabel("PC", fontsize=9)
    axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"0x{int(v):08X}"))
    axes[0].grid(True, alpha=0.2, linewidth=0.3)

    # 标出 MROM 和 ITCM 区域
    ymin, ymax = int_vals.min(), int_vals.max()
    if ymax == ymin:
        ymin -= 4
        ymax += 4
    margin = max((ymax - ymin) * 0.15, 4)
    axes[0].set_ylim(ymin - margin, ymax + margin)

    # 触发标记
    trig_sample = n_samples // 2
    axes[0].axvline(x=trig_sample, color="#e74c3c", linewidth=0.8, linestyle="--", alpha=0.5)
    axes[0].text(trig_sample + 5, ymax, "Trigger", fontsize=7, color="#e74c3c", va="top")

    axes[0].set_xlabel("Sample", fontsize=9)
    axes[0].set_xlim(0, n_samples - 1)

    plt.tight_layout()
    plt.savefig(out_path, facecolor="white", edgecolor="none")
    plt.close()
    print(f"[OK] Saved: {out_path}")


def render_nice_activity(samples, n_samples, out_path):
    """Fig 4.2: NICE CSR + Handshake 波形"""
    t = np.arange(n_samples)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 2.5), sharex=True)

    # 上: nice_csr (32-bit 总线)
    csr_name = "probe4_nice_csr[31:0]"
    csr_vals = np.array([hex_to_int(v) for v in samples[csr_name]])
    ax1.step(t, csr_vals, where="mid", color="#1a1a2e", linewidth=0.5)
    ax1.set_ylabel("nice_csr", fontsize=9)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"0x{int(v):08X}"))
    ax1.grid(True, alpha=0.2, linewidth=0.3)

    # 下: nice_hs (手握手信号)
    hs_name = "probe5_nice_hs[3:0]"
    hs_vals = np.array([hex_to_int(v) for v in samples[hs_name]])
    ax2.step(t, hs_vals, where="mid", color="#2196F3", linewidth=0.8)
    ax2.set_ylabel("nice_hs", fontsize=9)
    ax2.set_ylim(-0.2, max(hs_vals.max(), 1) + 0.5)
    ax2.grid(True, alpha=0.2, linewidth=0.3)

    # 触发标记
    trig_sample = n_samples // 2
    for ax in [ax1, ax2]:
        ax.axvline(x=trig_sample, color="#e74c3c", linewidth=0.8, linestyle="--", alpha=0.5)

    ax2.set_xlabel("Sample", fontsize=9)
    ax2.set_xlim(0, n_samples - 1)

    plt.tight_layout()
    plt.savefig(out_path, facecolor="white", edgecolor="none")
    plt.close()
    print(f"[OK] Saved: {out_path}")


# ---------- 入口 ----------

def main():
    if len(sys.argv) < 3:
        print("用法: python render_ila_waveform.py <csv路径> <输出png路径> [模式]")
        print("模式: pc_trace | nice_activity (默认根据 csv 内容自动判断)")
        sys.exit(1)

    csv_path  = sys.argv[1]
    out_path  = sys.argv[2]
    mode      = sys.argv[3] if len(sys.argv) > 3 else "auto"

    setup_academic_style()

    headers, radix, samples, n = parse_ila_csv(csv_path)

    # 自动判断模式
    if mode == "auto":
        probe_names = " ".join(headers)
        if "nice_csr" in probe_names or "nice_hs" in probe_names:
            mode = "nice_activity"
        else:
            mode = "pc_trace"

    print(f"Mode: {mode} | Samples: {n} | Probes: {len(samples)}")

    if mode == "pc_trace":
        render_pc_trace(samples, n, out_path)
    elif mode == "nice_activity":
        render_nice_activity(samples, n, out_path)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
