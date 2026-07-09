# 裂缝形态结果图：2D 等高线
# 用 PINN 模型在细网格上预测 W(x,t)，尖端外区域置零

import os
import sys
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PKN_comprehensive_final import PINN


PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE", "green_2": "#AADCA9", "green_3": "#8BCF8B",
    "red_1": "#F6CFCB", "red_2": "#E9A6A1", "red_strong": "#B64342",
    "neutral": "#CFCECE", "highlight": "#FFD700",
    "teal": "#42949E", "violet": "#9A4D8E",
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

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # ---- 加载 PINN 模型 ----
    model_path = os.path.join(script_dir, "pkn_pinn_model_final.pth")
    model = PINN().to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    print("已加载 PINN 模型")

    # ---- 构建预测网格 ----
    n_points_x = 60
    n_points_t = 800
    x_1d = torch.linspace(0, 6, n_points_x)
    t_1d = torch.linspace(0, 80, n_points_t)
    X_t, T_t = torch.meshgrid(x_1d, t_1d, indexing="ij")
    x_flat = X_t.reshape(-1, 1).to(device)
    t_flat = T_t.reshape(-1, 1).to(device)

    # ---- PINN 前向推理 ----
    with torch.no_grad():
        W_flat = model(x_flat, t_flat)
    W_grid = W_flat.reshape(n_points_x, n_points_t).cpu().numpy()
    X_np = X_t.numpy()
    T_np = T_t.numpy()

    # ---- 计算 L(t) 并屏蔽尖端外区域 ----
    t_safe = T_np + 1e-8
    term1 = 1.0 / ((1.3514 ** 2) * (t_safe ** 1.6))
    term2 = 1.0 / ((0.6366 ** 2) * (t_safe ** 1.0))
    L_t_grid = 1.0 / np.sqrt(term1 + term2)
    W_grid[X_np > L_t_grid] = 0.0

    print(f"W 范围: [{W_grid.min():.4f}, {W_grid.max():.4f}]")

    # ---- 画图 ----
    apply_publication_style(FigureStyle(font_size=15, axes_linewidth=2.0))

    fig, ax = plt.subplots(figsize=(8, 5.5))

    contour = ax.contourf(X_np, T_np, W_grid, levels=50, cmap="viridis")
    # 不设主标题，遵循论文图惯例
    ax.set_xlabel("Dimensionless Distance ($x^*$)")
    ax.set_ylabel("Dimensionless Time ($t^*$)")

    cbar = fig.colorbar(contour, ax=ax, fraction=0.046, pad=0.02)
    cbar.set_label("Width ($W^*$)", fontsize=14)
    cbar.ax.tick_params(labelsize=11)

    finalize_figure(fig, os.path.join(output_dir, "crack_width_field"),
                    formats=["png"], dpi=300)

    print(f"\n图表已保存至 {output_dir}/")
    print("  crack_width_field.png  — 裂缝宽度 2D 等高线")


if __name__ == "__main__":
    main()
