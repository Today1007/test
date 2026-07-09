# 误差随时间演化图
# 评估 4 个变体在 t=10,30,50,80 四个时刻的 FDM 精度

import json
import os
import sys
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ablation_study import PINN

PALETTE = {
    "blue_main":      "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE", "green_2": "#AADCA9", "green_3": "#8BCF8B",
    "red_1":   "#F6CFCB", "red_2":   "#E9A6A1", "red_strong": "#B64342",
    "neutral":  "#CFCECE", "highlight": "#FFD700",
    "teal":     "#42949E", "violet":    "#9A4D8E",
}

VARIANT_CONFIG = [
    # (label, color, marker, linestyle)
    ("Full Model",      PALETTE["blue_main"],     "o", "-"),
    ("Plain MLP",       PALETTE["violet"],        "s", "--"),
    ("w/o time power",  PALETTE["red_strong"],    "D", ":"),
    ("w/o tip shape",   PALETTE["teal"],          "^", "-."),
]

VARIANT_KEYS = ["Full_Model", "Plain_MLP", "No_Time_Power", "No_Tip_Shape"]
PREFIX_MAP = {"Full_Model": "full", "No_Time_Power": "no_time",
              "No_Tip_Shape": "no_tip", "Plain_MLP": "plain"}
ABLATION_MAP = {
    "Full_Model": None, "No_Time_Power": "no_time_power",
    "No_Tip_Shape": "no_tip_shape", "Plain_MLP": "plain",
}

TIME_POINTS = [10.0, 30.0, 50.0, 80.0]


@dataclass(frozen=True)
class FigureStyle:
    font_size: int = 16
    axes_linewidth: float = 2.5
    use_tex: bool = False


def apply_publication_style(style=None):
    if style is None:
        style = FigureStyle()
    plt.rcParams.update({
        "font.family":          "serif",
        "font.serif":           ["Times New Roman", "Times", "STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset":     "stix",
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


def compute_error(model, x_tensor, t_tensor, W_fdm):
    """对单一时刻计算误差指标"""
    with torch.no_grad():
        W_pinn = model(x_tensor, t_tensor).cpu().numpy().flatten()

    diff = W_pinn - W_fdm
    l2_err = np.sqrt(np.mean(diff ** 2))
    rel_l2 = np.linalg.norm(diff) / (np.linalg.norm(W_fdm) + 1e-12)
    max_err = np.max(np.abs(diff))
    return l2_err, rel_l2, max_err


# ============================================================
# 主程序
# ============================================================

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "figures")
    os.makedirs(output_dir, exist_ok=True)

    fdm_path = os.path.join(script_dir, "..", "FDM", "fdm_profiles.npz")
    if not os.path.exists(fdm_path):
        print(f"[错误] 未找到 FDM 数据: {fdm_path}")
        return

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # ---- 加载模型 ----
    models = {}
    for key in VARIANT_KEYS:
        model = PINN(ablation=ABLATION_MAP[key]).to(device)
        model_path = os.path.join(script_dir, f"pkn_pinn_{PREFIX_MAP[key]}.pth")
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.eval()
        models[key] = model

    # ---- 加载 FDM 基准，计算各时刻误差 ----
    fdm = np.load(fdm_path)
    fdm_x = fdm["x_D"]

    # 存结果: result[key][metric] = [t10, t30, t50, t80]
    result = {key: {"L2_err": [], "Rel_L2": [], "Max_err": []} for key in VARIANT_KEYS}

    print(f"\n{'='*70}")
    print(f"误差随时间演化")
    print(f"{'='*70}")

    for t_val in TIME_POINTS:
        # 准备 FDM 基准
        W_key = f"W_t{t_val:.0f}"
        L_key = f"L_t{t_val:.0f}"
        fdm_W_full = fdm[W_key]
        fdm_L = fdm[L_key]
        mask = (fdm_x <= fdm_L) & (fdm_W_full > 1e-8)
        x_fdm = fdm_x[mask]
        W_fdm = fdm_W_full[mask]

        x_t = torch.tensor(x_fdm, dtype=torch.float32).reshape(-1, 1).to(device)
        t_t = torch.full_like(x_t, t_val)

        print(f"\n  t = {t_val:.0f}")
        print(f"  {'变体':<18s} {'L2_err':>10s} {'Rel_L2':>10s} {'Max_err':>10s}")
        print(f"  {'-'*52}")

        for key in VARIANT_KEYS:
            l2_err, rel_l2, max_err = compute_error(models[key], x_t, t_t, W_fdm)
            result[key]["L2_err"].append(l2_err)
            result[key]["Rel_L2"].append(rel_l2)
            result[key]["Max_err"].append(max_err)
            print(f"  {key:<18s} {l2_err:10.2e} {rel_l2:10.4f} {max_err:10.2e}")

    fdm.close()
    print(f"\n{'='*70}\n")

    # ---- 画图 ----
    metrics = [
        ("L2_err",   "L2 Error"),
        ("Rel_L2",   "Relative L2 Error"),
        ("Max_err",  "Max Error"),
    ]

    apply_publication_style(FigureStyle(font_size=13, axes_linewidth=1.6))

    fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    ax_flat = axes.flatten()

    # ---- 前三子图：误差时间演化 ----
    for col, (metric, ylabel) in enumerate(metrics):
        ax = ax_flat[col]
        for (label, color, marker, ls), key in zip(VARIANT_CONFIG, VARIANT_KEYS):
            vals = result[key][metric]
            ax.plot(TIME_POINTS, vals, color=color, marker=marker, linestyle=ls,
                    markersize=8, linewidth=2.0, label=label,
                    markerfacecolor="white", markeredgewidth=1.6)

        ax.set_xlabel("Time t")
        ax.set_ylabel(ylabel)
        ax.set_xticks(TIME_POINTS)
        ax.set_xlim(TIME_POINTS[0] - 2, TIME_POINTS[-1] + 2)

    # ---- 第四子图：最终损失柱状图 ----
    ax_loss = ax_flat[3]
    summary_path = os.path.join(script_dir, "ablation_summary.json")
    with open(summary_path, "r") as f:
        summary = json.load(f)

    x_positions = np.arange(len(VARIANT_KEYS))
    bar_labels = [cfg[0] for cfg in VARIANT_CONFIG]
    bar_colors = [cfg[1] for cfg in VARIANT_CONFIG]
    bar_values = [summary[key]["best_loss"] for key in VARIANT_KEYS]

    bars = ax_loss.bar(x_positions, bar_values, color=bar_colors,
                       edgecolor="white", linewidth=0.8, width=0.5)

    # 柱顶标注数值
    for bar, val in zip(bars, bar_values):
        ax_loss.text(bar.get_x() + bar.get_width() / 2, val * 2.0,
                     f"{val:.3e}", ha="center", va="bottom", fontsize=9)

    ax_loss.set_xticks(x_positions)
    ax_loss.set_xticklabels(bar_labels, rotation=15, ha="right")
    ax_loss.set_ylabel("Best Loss")
    ax_loss.set_yscale("log")
    ax_loss.set_ylim(top=20)  # 给标注留空间

    # ---- 面板标签 (a)(b)(c)(d) ----
    for idx, letter in enumerate(["a", "b", "c", "d"]):
        ax_flat[idx].text(0.5, -0.18, f"({letter})", transform=ax_flat[idx].transAxes,
                          fontsize=14, fontweight="bold", va="top", ha="center")

    # ---- 共享图例（置于图内顶部） ----
    lines_labels = ax_flat[0].get_legend_handles_labels()
    fig.legend(lines_labels[0], lines_labels[1],
               loc="outside upper center", ncol=4, fontsize=11,
               frameon=False)

    finalize_figure(fig, os.path.join(output_dir, "ablation"),
                    formats=["png"], dpi=300)

    print(f"图表已保存至 {output_dir}/")
    print("  ablation.png  — 2×2 消融实验图（误差时间演化 + 最终损失）")


if __name__ == "__main__":
    main()
