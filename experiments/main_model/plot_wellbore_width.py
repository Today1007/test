# PKN 井口宽度 W(0,t) 对比图
# PINN vs FDM — log-log 图，展示早期/晚期幂律渐近行为

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

    # ---- 加载 FDM 密集数据 ----
    fdm_path = os.path.join(script_dir, "..", "FDM", "fdm_dense.npz")
    fdm = None
    if os.path.exists(fdm_path):
        fdm = np.load(fdm_path)
        fdm_t = fdm["t_save"]        # (320,)  t=0.25 → 80
        fdm_W0 = fdm["W_dense"][0, :]  # W(0,t)  for all saved times
        print(f"[对比] 已加载 FDM 密集数据 ({len(fdm_t)} 个时间点)")
    else:
        print("[对比] 未找到 FDM 密集数据，将仅绘制 PINN")

    # ---- 加载 PINN 模型 ----
    model_path = os.path.join(script_dir, "pkn_pinn_model_final.pth")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pinn = PINN().to(device)
    if os.path.exists(model_path):
        pinn.load_state_dict(torch.load(model_path, map_location=device))
        pinn.eval()
        print("已加载 PINN 模型（仅推理）")
    else:
        print("[警告] 未找到 PINN 模型！")
        pinn = None

    # ---- 在 FDM 时间点上评估 PINN，做定量对比 ----
    if pinn is not None and fdm is not None:
        x0 = torch.zeros(len(fdm_t), 1, dtype=torch.float32).to(device)
        t_fdm_tensor = torch.tensor(fdm_t, dtype=torch.float32).reshape(-1, 1).to(device)
        with torch.no_grad():
            pinn_W0_on_fdm = pinn(x0, t_fdm_tensor).cpu().numpy().flatten()

        diff = pinn_W0_on_fdm - fdm_W0
        l2_err = np.sqrt(np.mean(diff ** 2))
        rel_l2 = np.linalg.norm(diff) / (np.linalg.norm(fdm_W0) + 1e-12)
        max_err = np.max(np.abs(diff))

        print("\n" + "=" * 52)
        print("W(0,t) PINN vs FDM 定量误差")
        print("=" * 52)
        print(f"  L2 error:      {l2_err:.4e}")
        print(f"  Relative L2:   {rel_l2:.4f}")
        print(f"  Max error:     {max_err:.4e}")
        print("=" * 52 + "\n")

    # ---- PINN 在密集时间网格上评估（平滑曲线）----
    t_pinn_dense = np.logspace(np.log10(0.02), np.log10(80), 400)
    if pinn is not None:
        x0_dense = torch.zeros(len(t_pinn_dense), 1, dtype=torch.float32).to(device)
        t_dense_tensor = torch.tensor(t_pinn_dense, dtype=torch.float32).reshape(-1, 1).to(device)
        with torch.no_grad():
            pinn_W0_dense = pinn(x0_dense, t_dense_tensor).cpu().numpy().flatten()

    # ==================== 画图 ====================
    print("生成 W(0,t) 对比图...")
    apply_publication_style(FigureStyle(font_size=11, axes_linewidth=1.2))

    color_pinn = PALETTE["blue_main"]
    color_fdm  = PALETTE["red_strong"]

    fig, ax = plt.subplots(figsize=(6.5, 5))

    # PINN — 连续曲线
    if pinn is not None:
        ax.plot(t_pinn_dense, pinn_W0_dense, '-', color=color_pinn, linewidth=1.8,
                zorder=2, label='PINN')

    # FDM — 散点（每5个点画一个，避免过密）
    if fdm is not None:
        skip = 5
        ax.plot(fdm_t[::skip], fdm_W0[::skip], 'o', color=color_fdm, markersize=4.5,
                markeredgewidth=0.6, markeredgecolor='white',
                zorder=1, label='FDM')

    ax.set_yscale("log")
    ax.set_xlabel(r'$t$')
    ax.set_ylabel(r'$W_D(0, t)$')
    ax.set_xlim(left=0)
    ax.grid(True, linestyle='--', alpha=0.3, linewidth=0.6)

    ax.legend(loc='lower right', fontsize=10)

    fig.tight_layout(pad=0.3)
    finalize_figure(fig, os.path.join(output_dir, "wellbore_width"),
                    formats=["png"], dpi=600)

    if fdm is not None:
        fdm.close()

    print(f"\n图表已保存至 {output_dir}/")
    print("  wellbore_width.png — W(0,t) PINN vs FDM (log-log)")


if __name__ == "__main__":
    main()
