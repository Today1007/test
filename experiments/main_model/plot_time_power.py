# PKN PINN time_power 参数收敛曲线
import json
import os
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


@dataclass(frozen=True)
class FigureStyle:
    font_size: int = 16
    axes_linewidth: float = 2.5
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
        "legend.fontsize":      style.font_size - 2,
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

    loss_path = os.path.join(script_dir, "loss_history.json")
    if not os.path.exists(loss_path):
        print(f"[错误] 找不到 {loss_path}，请先运行训练脚本！")
        return

    with open(loss_path, "r") as f:
        loss_history = json.load(f)
    adam = loss_history["adam"]
    lbfgs = loss_history["lbfgs"]

    lbfgs_offset = adam["iter"][-1] + 1 if adam["iter"] else 0

    # time_power 收敛曲线
    print("time_power 收敛...")
    apply_publication_style(FigureStyle(font_size=14, axes_linewidth=2.0))

    ap = adam["time_power"]
    lp = lbfgs["time_power"]
    all_power = ap + lp

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(all_power, color=PALETTE["blue_main"], linewidth=1.5)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Time factor")

    if adam["iter"]:
        ax.axvline(x=lbfgs_offset, color="#999999", linestyle="--",
                   linewidth=1.0, alpha=0.7)
        y_mid = (max(all_power) + min(all_power)) / 2
        ax.text(lbfgs_offset * 0.5, y_mid, "Adam",
                ha="center", fontsize=11, color="#666666")
        ax.text(lbfgs_offset + (len(all_power) - lbfgs_offset) * 0.5, y_mid,
                "L-BFGS", ha="center", fontsize=11, color="#666666")

    finalize_figure(fig, os.path.join(output_dir, "time_power_convergence"),
                    formats=["png"], dpi=300)

    print(f"图表已保存至 {output_dir}/")
    print("  time_power_convergence.png  — time_power 参数收敛")


if __name__ == "__main__":
    main()
