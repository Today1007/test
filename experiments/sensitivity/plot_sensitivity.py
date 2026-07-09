# PKN PINN 敏感性分析画图脚本
# 网络结构 (深度 × 宽度) 全因子网格 — 25 个配置
# 1×2 子图布局: (a) 损失 vs 宽度 + (b) 训练耗时 vs 精度

import json
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dataclasses import dataclass

PALETTE = {
    "blue_main":      "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE", "green_2": "#AADCA9", "green_3": "#8BCF8B",
    "red_1":   "#F6CFCB", "red_2":   "#E9A6A1", "red_strong": "#B64342",
    "neutral":  "#CFCECE", "highlight": "#FFD700",
    "teal":     "#42949E", "violet":    "#9A4D8E",
}

# 深度映射到颜色 (浅→深)
DEPTH_COLORS = {
    2: "#E9A6A1",               # 浅红
    3: "#F0B060",               # 橙
    4: PALETTE["blue_main"],    # 蓝 (主模型)
    5: PALETTE["teal"],         # 青
    6: PALETTE["violet"],       # 紫
}

DEPTHS = [2, 3, 4, 5, 6]
WIDTHS = [32, 64, 128, 256, 512]
MARKERS = ["o", "s", "D", "^", "v"]


@dataclass(frozen=True)
class FigureStyle:
    font_size: int = 14
    axes_linewidth: float = 1.2
    use_tex: bool = False
    font_family: tuple = ("DejaVu Sans", "Helvetica", "Arial", "sans-serif")


def apply_publication_style(style=None):
    if style is None:
        style = FigureStyle()
    plt.rcParams.update({
        "font.family":          style.font_family[0],
        "font.sans-serif":      list(style.font_family),
        "font.size":            style.font_size,
        "axes.titlesize":       style.font_size + 2,
        "axes.labelsize":       style.font_size,
        "xtick.labelsize":      style.font_size - 2,
        "ytick.labelsize":      style.font_size - 2,
        "legend.fontsize":      style.font_size - 3,
        "axes.linewidth":       style.axes_linewidth,
        "axes.spines.top":      False,
        "axes.spines.right":    False,
        "legend.frameon":       False,
        "legend.edgecolor":     "none",
        "savefig.bbox":         "tight",
        "savefig.pad_inches":   0.05,
        "text.usetex":          style.use_tex,
    })


def finalize_figure(fig, out_path, formats=None, dpi=300, close=True, pad=0.05):
    if formats is None:
        formats = ["png"]
    os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else ".", exist_ok=True)
    saved = []
    for fmt in formats:
        path = f"{out_path}.{fmt}"
        fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=pad)
        saved.append(path)
        print(f"  -> {path}")
    if close:
        plt.close(fig)
    return saved


# ============================================================
# 主程序
# ============================================================

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "figures")
    os.makedirs(output_dir, exist_ok=True)

    # ---- 加载汇总表 ----
    summary_path = os.path.join(script_dir, "sensitivity_summary.json")
    with open(summary_path, "r") as f:
        summary = json.load(f)

    # ---- 构建数据矩阵 ----
    f_loss_matrix = np.full((len(DEPTHS), len(WIDTHS)), np.nan)
    loss_matrix   = np.full((len(DEPTHS), len(WIDTHS)), np.nan)  # total loss
    time_matrix   = np.full((len(DEPTHS), len(WIDTHS)), np.nan)  # 训练耗时 (秒)

    for idepth, d in enumerate(DEPTHS):
        for iwidth, w in enumerate(WIDTHS):
            name = f"D{d}_W{w}"
            if name in summary and summary[name].get("status") == "completed":
                r = summary[name]
                f_loss_matrix[idepth, iwidth] = r["final_f_loss"]
                loss_matrix[idepth, iwidth]   = r["final_lbfgs_loss"]
                time_matrix[idepth, iwidth]   = r["time_seconds"]

    # ============================================================
    # Console 表格: f_loss (深度 × 宽度)
    # ============================================================
    HEADER = ["Depth\\Width"] + [f"W={w}" for w in WIDTHS]
    COL_WIDTHS = [12] + [12] * len(WIDTHS)

    def fmt_cell(v):
        if isinstance(v, str):
            return v
        if np.isnan(v):
            return "   N/A"
        return f"{v:.4e}"

    def print_sep():
        line = "+"
        for cw in COL_WIDTHS:
            line += "-" * cw + "+"
        print("  " + line)

    def print_row(label, values):
        cells = [label] + [fmt_cell(v) for v in values]
        parts = " | ".join(f"{c:>{cw}}" if i == 0 else f"{c:>{cw}}"
                          for i, (c, cw) in enumerate(zip(cells, COL_WIDTHS)))
        print(f"  | {parts} |")

    def print_table(title, matrix, fmt="e"):
        print(f"\n  {title}")
        print_sep()
        print_row(HEADER[0], HEADER[1:])
        print_sep()
        for idepth, d in enumerate(DEPTHS):
            cells = [f"D={d}"]
            for v in matrix[idepth, :]:
                if np.isnan(v):
                    cells.append("        N/A")
                elif fmt == "e":
                    cells.append(f"{v:.4e}")
                else:
                    cells.append(f"{v:>8.0f}")
            parts = " | ".join(f"{c:>{cw}}" if i == 0 else f"{c:>{cw}}"
                              for i, (c, cw) in enumerate(zip(cells, COL_WIDTHS)))
            print(f"  | {parts} |")
            if idepth < len(DEPTHS) - 1:
                print_sep()
        print_sep()

    print_table("PDE 残差 f_loss (深度×宽度)", f_loss_matrix, fmt="e")
    print_table("Total Loss (深度×宽度)", loss_matrix, fmt="e")
    print_table("训练耗时 / s (深度×宽度)", time_matrix, fmt="d")

    # ============================================================
    # 画图: 1×2 布局
    # ============================================================
    print("\n生成敏感性分析图...")
    apply_publication_style(FigureStyle(font_size=10, axes_linewidth=1.1))

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 5))

    # ---- (a) Total Loss vs Width ----
    for idepth, d in enumerate(DEPTHS):
        vals = loss_matrix[idepth, :]
        color = DEPTH_COLORS[d]
        ax_a.semilogy(WIDTHS, vals, color=color, marker=MARKERS[idepth],
                     markersize=8, linewidth=1.8, label=f"D = {d}",
                     markerfacecolor="white", markeredgewidth=1.4)

    ax_a.set_xlabel("Width")
    ax_a.set_ylabel("Total Loss")
    ax_a.set_xticks(WIDTHS)
    ax_a.set_xticklabels([str(w) for w in WIDTHS])
    ax_a.legend(loc="upper right", ncol=2, fontsize=8)
    ax_a.grid(True, linestyle="--", alpha=0.3, linewidth=0.6)

    # ---- (b) 训练耗时 vs Width ----
    for idepth, d in enumerate(DEPTHS):
        vals = time_matrix[idepth, :]
        color = DEPTH_COLORS[d]
        ax_b.semilogy(WIDTHS, vals, color=color, marker=MARKERS[idepth],
                     markersize=8, linewidth=1.8, label=f"D = {d}",
                     markerfacecolor="white", markeredgewidth=1.4)

    ax_b.set_xlabel("Width")
    ax_b.set_ylabel("Training Time (s)")
    ax_b.set_xticks(WIDTHS)
    ax_b.set_xticklabels([str(w) for w in WIDTHS])
    ax_b.legend(loc="upper right", ncol=2, fontsize=8)
    ax_b.grid(True, linestyle="--", alpha=0.3, linewidth=0.6)

    # ---- 面板标签：下方居中 ----
    for ax, label in zip([ax_a, ax_b], ["(a)", "(b)"]):
        ax.text(0.5, -0.18, label, transform=ax.transAxes,
               fontsize=13, fontweight="bold", va="top", ha="center")

    fig.tight_layout(pad=1.0, w_pad=2.0)
    finalize_figure(fig, os.path.join(output_dir, "sensitivity"),
                    formats=["png"], dpi=600)

    print(f"\n图表已保存至 {output_dir}/")
    print("  sensitivity.png — 敏感性分析 1×2")


if __name__ == "__main__":
    main()
