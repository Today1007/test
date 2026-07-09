# PKN 综合模型 PINN 消融实验
# 与 PKN_comprehensive_final.py 结构完全一致，仅增加消融控制
import torch
import torch.nn as nn
import numpy as np
from scipy.stats import qmc
import torch.optim as optim
from tqdm import tqdm
import time
import sys
import math
import random
import json
from scipy.optimize import brentq
import os


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def get_L_t(t):
    """计算裂缝长度 L(t)：体积主导与滤失主导的调和平均拼接"""
    t_safe = t + 1e-8
    term1 = 1.0 / ((1.3514 ** 2) * (t_safe ** 1.6))   # 早期体积主导分量
    term2 = 1.0 / ((0.6366 ** 2) * (t_safe ** 1.0))   # 晚期滤失主导分量 (0.6366 ≈ 2/π)
    return 1.0 / torch.sqrt(term1 + term2)


def get_transient_tip_shape(xi_hat):
    """
    计算平滑过渡的瞬态尖端无量纲宽度
    当 xi_hat → 0 时，表现为 1/3 次幂 (体积主导)
    当 xi_hat 变大时，退化为 3/8 次幂 (滤失主导)
    """
    xi_hat_safe = torch.clamp(xi_hat, min=1e-12)
    a = 8.0 * (xi_hat_safe ** (1.0 / 6.0))
    b = (9.0 + torch.sqrt(81.0 + 256.0 * (xi_hat_safe ** 0.5))) ** (1.0 / 3.0)
    m = (2.0 ** (1.0 / 3.0)) * b - a / b
    term1 = 1.0 / (2.0 * (6.0 ** (1.0 / 3.0)) * torch.sqrt(m))
    term2 = m + torch.sqrt(torch.clamp(12.0 - m ** 1.5, min=1e-8))
    omega_0 = term1 * term2
    Omega_0 = (3.0 ** (1.0 / 3.0)) * (xi_hat_safe ** (1.0 / 3.0))
    return omega_0 * Omega_0


def compute_exact_tau(x_tensor, t_tensor):
    """
    利用 scipy 数值求根，根据 get_L_t 的逻辑反解出每个空间点 x 对应的真实到达时间 tau
    """
    x_np = x_tensor.cpu().numpy().flatten()
    t_np = t_tensor.cpu().numpy().flatten()
    tau_np = np.zeros_like(x_np)

    def f_root(t_val, x_target):
        t_safe = t_val + 1e-8
        term1 = 1.0 / ((1.3514 ** 2) * (t_safe ** 1.6))
        term2 = 1.0 / ((0.6366 ** 2) * (t_safe ** 1.0))
        L_t = 1.0 / math.sqrt(term1 + term2)
        return L_t - x_target

    for i in range(len(x_np)):
        xi = x_np[i]
        ti = t_np[i]

        if xi <= 1e-8:
            tau_np[i] = 0.0
            continue

        # tau 必定在 [0, 当前时间 t] 之间
        try:
            tau_np[i] = brentq(f_root, 0.0, ti + 1e-4, args=(xi,))
        except ValueError:
            tau_np[i] = ti

    return torch.tensor(tau_np, dtype=torch.float32, device=x_tensor.device).view(-1, 1)


class PINN(nn.Module):
    def __init__(self, ablation=None):
        """
        ablation: None=完整模型, 'no_time_power'=去除时间幂律,
                  'no_tip_shape'=去除尖端形状, 'plain'=纯MLP
        """
        super(PINN, self).__init__()
        self.ablation = ablation
        self.time_power = nn.Parameter(torch.tensor([0.20]))
        self.net = nn.Sequential(
            nn.Linear(2, 128), nn.Tanh(),
            nn.Linear(128, 128), nn.Tanh(),
            nn.Linear(128, 128), nn.Tanh(),
            nn.Linear(128, 128), nn.Tanh(),
            nn.Linear(128, 1)
        )
        self._initialize_weights()

    def _initialize_weights(self):
        for module in self.net.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_normal_(module.weight)
                nn.init.zeros_(module.bias)
        nn.init.constant_(self.net[-1].bias, 0.0)

    def forward(self, x, t):
        x_norm = x
        t_norm = t
        L_t = get_L_t(t)
        xi = x / (L_t + 1e-8)                     # 防止除零
        out = self.net(torch.cat([t_norm, x_norm], dim=1))
        nn_out = torch.nn.functional.softplus(out) # 网络拟合 expansion 多项式

        # ---- 消融控制 ----
        if self.ablation == 'plain':
            return nn_out  # 纯 MLP，无物理结构

        t_safe = t + 1e-10
        power = torch.clamp(self.time_power, min=0.1, max=0.3)
        time_factor = 1.0 if self.ablation == 'no_time_power' else t_safe ** power

        term_1_xi = torch.clamp(1.0 - xi, min=1e-8)
        tip_factor = 1.0 if self.ablation == 'no_tip_shape' else get_transient_tip_shape(term_1_xi)

        W_star = time_factor * tip_factor * nn_out
        return W_star


def physics_loss(model, x, t, tau):
    W_star = model(x, t)
    L_t = get_L_t(t)

    # 有效区域掩码：x 在裂缝内且当前时刻已过到达时间
    valid_mask = (x <= L_t) & (t > tau)

    # 滤失项，仅在有效区域计算
    eps = 1e-8
    sqrt_arg = torch.clamp(t - tau, min=eps)
    leak_off = 1.0 / torch.sqrt(sqrt_arg)
    leak_off = torch.where(valid_mask, leak_off, torch.zeros_like(leak_off))

    # W 对 t 的一阶导
    W_t = torch.autograd.grad(W_star, t, grad_outputs=torch.ones_like(W_star), create_graph=True)[0]
    # V = W^4，求对 x 的二阶导
    V = W_star ** 4
    V_x = torch.autograd.grad(V, x, grad_outputs=torch.ones_like(V), create_graph=True)[0]
    V_xx = torch.autograd.grad(V_x, x, grad_outputs=torch.ones_like(V_x), create_graph=True)[0]

    pde_residual = W_t + leak_off - V_xx

    if valid_mask.any():
        loss = pde_residual[valid_mask].pow(2).mean()
    else:
        loss = torch.tensor(0.0, device=x.device, requires_grad=True)
    return loss


def boundary_loss(model, x_left, t):
    """左边界条件：引入平滑因子解决 (0,0) 处边界条件与初始条件冲突"""
    W_star_boundary = model(x_left, t)
    W_star4_boundary = W_star_boundary ** 4
    W_star4_boundary_x = torch.autograd.grad(
        W_star4_boundary, x_left,
        grad_outputs=torch.ones_like(W_star4_boundary), create_graph=True
    )[0]
    alpha = 100.0
    smooth_factor = 1.0 - torch.exp(-alpha * t)
    boundary_residual = W_star4_boundary_x + smooth_factor
    return boundary_residual.pow(2).mean()


def train(model, adam_epochs, lbfgs_epochs, device):
    # ========== 损失记录 ==========
    loss_history = {
        'adam': {'iter': [], 'f_loss': [], 'bc_loss': [], 'total': [], 'time_power': []},
        'lbfgs': {'iter': [], 'f_loss': [], 'bc_loss': [], 'total': [], 'time_power': []}
    }

    # ========== 采样器初始化 ==========
    sampler_pde = qmc.LatinHypercube(d=2, seed=42)
    sampler_bc = qmc.LatinHypercube(d=1, seed=42)

    # ========== PDE 域内采样 ==========
    # 早期 (t ∈ [0, 10])
    raw_pts_early = sampler_pde.random(n=10000)
    pde_pts_early = torch.tensor([0.0, 0.0], device=device) + \
                    torch.tensor([1.0, 10.0], device=device) * \
                    torch.tensor(raw_pts_early, dtype=torch.float32, device=device)

    # 晚期 (t ∈ [10, 80])
    raw_pts_late = sampler_pde.random(n=20000)
    pde_pts_late = torch.tensor([0.0, 10.0], device=device) + \
                   torch.tensor([1.0, 70.0], device=device) * \
                   torch.tensor(raw_pts_late, dtype=torch.float32, device=device)

    pde_pts = torch.cat([pde_pts_early, pde_pts_late], dim=0)
    t_raw = pde_pts[:, 1:2]
    x_std = pde_pts[:, 0:1]

    L_t_pde = get_L_t(t_raw)
    x_raw = x_std * L_t_pde

    # 尖端加密 (x ∈ [0.95L, 0.999L])
    raw_pts_tip = sampler_pde.random(n=10000)
    pde_pts_std_tip = torch.tensor(raw_pts_tip, dtype=torch.float32, device=device)
    t_tip_raw = 80.0 * pde_pts_std_tip[:, 1:2]
    x_std_tip = 0.95 + 0.049 * pde_pts_std_tip[:, 0:1]
    L_t_tip = get_L_t(t_tip_raw)
    x_tip_raw = x_std_tip * L_t_tip

    x_raw = torch.cat([x_raw, x_tip_raw], dim=0)
    t_raw = torch.cat([t_raw, t_tip_raw], dim=0)

    tau_raw = compute_exact_tau(x_raw, t_raw)

    x = x_raw.clone().detach().requires_grad_(True)
    t = t_raw.clone().detach().requires_grad_(True)
    tau = tau_raw.clone().detach()

    # ========== 边界条件采样 ==========
    t_bc_std_early = torch.tensor(sampler_bc.random(n=1000), dtype=torch.float32, device=device)
    t_bc_early = 0.0 + (10 - 0.0) * t_bc_std_early

    t_bc_std_late = torch.tensor(sampler_bc.random(n=1000), dtype=torch.float32, device=device)
    t_bc_late = 10 + (80 - 10) * t_bc_std_late

    t_bc_pts = torch.cat([t_bc_early, t_bc_late], dim=0)
    t_bc = t_bc_pts.requires_grad_(True)

    x_left = torch.zeros(2000, 1, device=device, requires_grad=True)

    # ========== 第一阶段：Adam ==========
    print("=== 第一阶段：使用 Adam 优化器训练 ===")
    optimizer_adam = optim.Adam(model.parameters(), lr=1e-3)
    scheduler = optim.lr_scheduler.ExponentialLR(optimizer_adam, gamma=0.9995)

    pbar = tqdm(range(adam_epochs), desc="Adam Training", unit="iter")
    start_time = time.time()

    for it in pbar:
        optimizer_adam.zero_grad()
        f_loss = physics_loss(model, x, t, tau)
        bc_left_loss = boundary_loss(model, x_left, t_bc)

        loss = f_loss + bc_left_loss

        # 记录损失
        loss_history['adam']['iter'].append(it)
        loss_history['adam']['f_loss'].append(f_loss.item())
        loss_history['adam']['bc_loss'].append(bc_left_loss.item())
        loss_history['adam']['total'].append(loss.item())
        loss_history['adam']['time_power'].append(
            torch.clamp(model.time_power, min=0.1, max=0.3).item())

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer_adam.step()
        scheduler.step()

        if it % 100 == 0:
            elapsed = time.time() - start_time
            current_lr = optimizer_adam.param_groups[0]['lr']
            current_power = torch.clamp(model.time_power, min=0.1, max=0.3).item()
            print(f"Adam Iter {it}: "
                  f"f_loss={f_loss.item():.3e}, bc_l={bc_left_loss.item():.3e}, "
                  f"total={loss.item():.3e}, "
                  f"LR={current_lr:.3e}, Power={current_power:.4f}, Time={elapsed:.2f}s")
            start_time = time.time()
    pbar.close()

    # ========== 第二阶段：L-BFGS ==========
    print("=== 第二阶段：使用 L-BFGS 优化器训练 ===")
    pbar_lbfgs = tqdm(range(lbfgs_epochs), desc="LBFGS Training", unit="iter", file=sys.stdout)
    optimizer_lbfgs = optim.LBFGS(
        model.parameters(),
        lr=0.5,
        max_iter=1,
        max_eval=50,
        history_size=100,
        tolerance_grad=1e-6,
        tolerance_change=1e-9,
        line_search_fn="strong_wolfe"
    )

    cur_f, cur_bc_l, cur_total = 0.0, 0.0, 0.0

    def closure():
        nonlocal cur_f, cur_bc_l, cur_total
        optimizer_lbfgs.zero_grad()
        f_loss = physics_loss(model, x, t, tau)
        bc_left_loss = boundary_loss(model, x_left, t_bc)
        loss = f_loss + bc_left_loss

        cur_f = f_loss.item()
        cur_bc_l = bc_left_loss.item()
        cur_total = loss.item()

        loss.backward()
        return loss

    start_time = time.time()
    prev_loss = float('inf')
    stagnant_steps = 0

    for it in pbar_lbfgs:
        loss = optimizer_lbfgs.step(closure)
        loss_val = loss.item()

        # 记录损失
        loss_history['lbfgs']['iter'].append(it)
        loss_history['lbfgs']['f_loss'].append(cur_f)
        loss_history['lbfgs']['bc_loss'].append(cur_bc_l)
        loss_history['lbfgs']['total'].append(cur_total)
        loss_history['lbfgs']['time_power'].append(
            torch.clamp(model.time_power, min=0.05, max=0.5).item())

        current_power = torch.clamp(model.time_power, min=0.05, max=0.5).item()

        if abs(prev_loss - loss_val) < 1e-10:
            stagnant_steps += 1
        else:
            stagnant_steps = 0

        if stagnant_steps >= 200:
            print(f"\n[Early Stopping] L-BFGS 在第 {it} 步达到收敛条件，提前结束训练！")
            break

        prev_loss = loss_val

        if it % 100 == 0:
            elapsed = time.time() - start_time
            print(f"LBFGS Iter {it}:  "
                  f"f_loss={cur_f:.3e}, bc_l={cur_bc_l:.3e}, "
                  f"total={cur_total:.3e}, "
                  f"Power={current_power:.4f}, Time={elapsed:.2f}s")
            start_time = time.time()
    pbar_lbfgs.close()

    return loss_history


# ========== 损失数据保存 ==========
def save_loss_history(loss_history, save_path=None):
    """将训练损失数据保存为 JSON 文件，供后续画图脚本读取"""
    if save_path is None:
        save_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(save_dir, 'loss_history.json')
    with open(save_path, 'w') as f:
        json.dump(loss_history, f)
    print(f"损失数据已保存至 {save_path}")
    return save_path




# ========== 主程序：批量消融训练 ==========
if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 消融配置
    ABLATION_CONFIGS = [
        # (名称,        ablation 参数,       文件名前缀)
        ("Full_Model",       None,               "full"),
        ("No_Time_Power",    "no_time_power",    "no_time"),
        ("No_Tip_Shape",     "no_tip_shape",     "no_tip"),
        ("Plain_MLP",        "plain",            "plain"),
    ]

    results_summary = {}

    for ab_name, ab_flag, ab_prefix in ABLATION_CONFIGS:
        print(f"\n{'#'*60}")
        print(f"#  消融变体: {ab_name}")
        print(f"{'#'*60}")

        set_seed(42)

        model = PINN(ablation=ab_flag).to(device)
        n_params = sum(p.numel() for p in model.parameters())

        t_start = time.time()
        loss_history = train(model=model, adam_epochs=5000, lbfgs_epochs=10000, device=device)
        elapsed = time.time() - t_start

        # 保存损失数据（与主模型完全一致）
        loss_path = os.path.join(script_dir, f"loss_history_{ab_prefix}.json")
        save_loss_history(loss_history, save_path=loss_path)

        # 保存模型
        model_path = os.path.join(script_dir, f"pkn_pinn_{ab_prefix}.pth")
        torch.save(model.state_dict(), model_path)

        # 记录结果
        final_adam = loss_history['adam']['total'][-1] if loss_history['adam']['total'] else float('nan')
        final_lbfgs = loss_history['lbfgs']['total'][-1] if loss_history['lbfgs']['total'] else final_adam
        best_loss = min(final_adam, final_lbfgs)
        final_power = (loss_history['adam']['time_power'][-1]
                       if loss_history['adam']['time_power']
                       else float('nan'))

        results_summary[ab_name] = {
            'ablation': ab_flag,
            'final_adam': final_adam,
            'final_lbfgs': final_lbfgs,
            'best_loss': best_loss,
            'time_power': final_power,
            'n_params': n_params,
            'time_seconds': elapsed,
        }

        print(f"\n  ✓ {ab_name} 完成")
        print(f"    Adam 终损: {final_adam:.4e}  |  L-BFGS 终损: {final_lbfgs:.4e}")
        print(f"    time_power: {final_power:.4f}  |  耗时: {elapsed:.1f}s")

    # 汇总保存
    summary_path = os.path.join(script_dir, "ablation_summary.json")
    with open(summary_path, "w") as f:
        json.dump(results_summary, f, indent=2)

    print(f"\n{'='*60}")
    print("消融实验全部完成！")
    print(f"{'='*60}")
    print(f"\n{'变体':<20s} {'Best Loss':>12s} {'Time':>8s} {'Params':>8s}")
    print("-" * 52)
    for name, r in results_summary.items():
        print(f"{name:<20s} {r['best_loss']:>12.4e} {r['time_seconds']:>7.0f}s {r['n_params']:>8,}")
    print(f"\n结果已保存至 {summary_path}")
