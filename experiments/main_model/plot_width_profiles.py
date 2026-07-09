# PKN 宽度剖面对比画图脚本
# PINN vs FDM
# 严格遵循 scientific-figure-making / figures4papers API 风格

import os
import sys
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dataclasses import dataclass

# 导入训练脚本中的 PINN 模型
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PKN_comprehensive_final import PINN

# ============================================================
# scientific-figure-making API
# ============================================================

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

    # ---- 加载 FDM 数据 ----
    fdm_path = os.path.join(script_dir, "..", "FDM", "fdm_profiles.npz")
    fdm = None
    if os.path.exists(fdm_path):
        fdm = np.load(fdm_path)
        fdm_x = fdm["x_D"]
        print("[对比] 已加载 FDM 基准数据")
    else:
        print("[对比] 未找到 FDM 数据，将仅绘制 PINN")

    # ---- 加载 PINN 模型（仅推理，不训练）----
    model_path = os.path.join(script_dir, "pkn_pinn_model_final.pth")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pinn = PINN().to(device)
    if os.path.exists(model_path):
        pinn.load_state_dict(torch.load(model_path, map_location=device))
        pinn.eval()
        print("已加载 PINN 模型（仅推理）")
    else:
        print("[警告] 未找到 PINN 模型，将跳过 PINN 曲线")
        pinn = None

    target_times = [10, 30, 50, 80]

    # ==================== 定量对比: PINN vs FDM ====================
    if pinn is not None and fdm is not None:
        print("\n" + "=" * 52)
        print("PINN vs FDM 定量误差分析")
        print("=" * 52)
        print(f"{'t':>6s}  {'L2_err':>10s}  {'Rel_L2':>10s}  {'Max_err':>10s}")
        print("-" * 52)

        for t_val in target_times:
            fdm_key = f"W_t{t_val:.0f}"
            fdm_L_key = f"L_t{t_val:.0f}"
            fdm_W = fdm[fdm_key]
            fdm_L_val = fdm[fdm_L_key]
            mask = (fdm_x <= fdm_L_val) & (fdm_W > 1e-8)
            x_fdm_active = fdm_x[mask]
            W_fdm_active = fdm_W[mask]

            x_t = torch.tensor(x_fdm_active, dtype=torch.float32).reshape(-1, 1).to(device)
            t_t = torch.full_like(x_t, t_val)
            with torch.no_grad():
                W_pinn_on_fdm = pinn(x_t, t_t).cpu().numpy().flatten()

            diff = W_pinn_on_fdm - W_fdm_active
            l2_err = np.sqrt(np.mean(diff ** 2))
            rel_l2 = np.linalg.norm(diff) / (np.linalg.norm(W_fdm_active) + 1e-12)
            max_err = np.max(np.abs(diff))

            print(f"{t_val:6.1f}  {l2_err:10.2e}  {rel_l2:10.4f}  {max_err:10.2e}")

        print("=" * 52 + "\n")

    # ==================== 宽度剖面: PINN vs FDM（2×2 子图）====================
    print("生成宽度剖面对比图...")
    apply_publication_style(FigureStyle(font_size=9, axes_linewidth=0.8))

    subplot_labels = ['(a)', '(b)', '(c)', '(d)']
    color_pinn = PALETTE["blue_main"]
    color_fdm  = PALETTE["red_strong"]

    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    ax_flat = axes.flatten()

    for idx, (ax, t_val) in enumerate(zip(ax_flat, target_times)):
        # ---- PINN — 自有平滑网格，实线 ----
        if pinn is not None:
            t_np = float(t_val)
            term1 = 1.0 / ((1.3514 ** 2) * (t_np ** 1.6))
            term2 = 1.0 / ((0.6366 ** 2) * (t_np ** 1.0))
            L_pinn_val = 1.0 / np.sqrt(term1 + term2)
            x_pinn_grid = np.linspace(0, L_pinn_val, 200)
            x_t = torch.tensor(x_pinn_grid, dtype=torch.float32).reshape(-1, 1).to(device)
            t_t = torch.full_like(x_t, t_val)
            with torch.no_grad():
                w_pinn_curve = pinn(x_t, t_t).cpu().numpy().flatten()
            ax.plot(x_pinn_grid, w_pinn_curve, '-', color=color_pinn, linewidth=2.0,
                    zorder=2, label='PINN')

        # ---- FDM — 虚线 ----
        if fdm is not None:
            fdm_key = f"W_t{t_val:.0f}"
            fdm_L_key = f"L_t{t_val:.0f}"
            if fdm_key in fdm:
                fdm_W = fdm[fdm_key]
                fdm_L_val = fdm[fdm_L_key]
                mask = (fdm_x <= fdm_L_val) & (fdm_W > 1e-8)
                ax.plot(fdm_x[mask], fdm_W[mask], '--', color=color_fdm, linewidth=1.8,
                        zorder=1, label='FDM')

        ax.text(0.5, -0.18, f'{subplot_labels[idx]}  $t \\approx {t_val}$',
                transform=ax.transAxes, ha="center", va="top", fontsize=9)
        ax.set_xlabel('$x_D$')
        if idx in (0, 2):  # 左列两个子图显示 y 轴标签
            ax.set_ylabel('$W_D$')
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        ax.grid(True, linestyle='--', alpha=0.3, linewidth=0.6)
        ax.margins(x=0.08)

    # 统一图例
    handles, labels = ax_flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.02),
               ncol=2, frameon=False, fontsize=9)

    fig.tight_layout(pad=0.5, w_pad=1.0, h_pad=1.5, rect=[0, 0, 1, 0.94])
    finalize_figure(fig, os.path.join(output_dir, "width_profiles"),
                    formats=["png"], dpi=600)

    if fdm is not None:
        fdm.close()

    print(f"\n图表已保存至 {output_dir}/")
    print("  width_profiles.png — 宽度剖面 PINN vs FDM (2×2, t=10/30/50/80)")


if __name__ == "__main__":
    main()
