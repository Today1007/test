# PKN 综合模型 FDM 求解（基准解）
# 仅保存目标时刻的宽度剖面 W(x)，用于与 PINN 对比

import numpy as np
import os


# ==========================================
# 1. 追赶法 (Thomas Algorithm)
# ==========================================
def thomas_algorithm(a, b, c, d):
    n = len(d)
    c_prime = np.zeros(n)
    d_prime = np.zeros(n)
    x = np.zeros(n)

    c_prime[0] = c[0] / b[0]
    d_prime[0] = d[0] / b[0]
    for i in range(1, n):
        m = 1.0 / (b[i] - a[i] * c_prime[i - 1])
        c_prime[i] = c[i] * m
        d_prime[i] = (d[i] - a[i] * d_prime[i - 1]) * m

    x[n - 1] = d_prime[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = d_prime[i] - c_prime[i] * x[i + 1]
    return x


# ==========================================
# 2. FDM 求解器
# ==========================================
def solve_fdm(N=201, L_D=8, T_total=80, dt_D=0.025,
              target_times=(10.0, 30.0, 50.0, 80.0),
              save_dir=None):
    """
    返回
    ----
    x_D (N,)           : 空间网格
    W_profiles (dict)  : {t: W(x)} 各目标时刻剖面
    L_at_target (dict) : {t: L} 各目标时刻裂缝长度
    """
    if save_dir is None:
        save_dir = os.path.dirname(os.path.abspath(__file__))

    dx_D = L_D / (N - 1)
    x_D = np.linspace(0, L_D, N)

    time_steps = int(T_total / dt_D)
    M_D = dt_D / (dx_D ** 2)

    W_D = np.zeros(N)
    tau_D = np.full(N, -1.0)
    tau_D[0] = 0.0
    L_prev = 0.0

    saved_profiles = {}
    saved_lengths = {}

    current_time = 0.0

    for m in range(1, time_steps + 1):
        t_m = current_time
        t_next = current_time + dt_D

        a = np.zeros(N)
        b = np.zeros(N)
        c = np.zeros(N)
        d = np.zeros(N)

        # 内点
        for i in range(1, N - 1):
            if 0.0 <= tau_D[i] <= t_m:
                loss_term = 2.0 * (np.sqrt(t_next - tau_D[i]) - np.sqrt(t_m - tau_D[i]))
            else:
                loss_term = 0.0

            a[i] = -2 * M_D * (W_D[i - 1] ** 3)
            b[i] = 1 + 4 * M_D * (W_D[i] ** 3)
            c[i] = -2 * M_D * (W_D[i + 1] ** 3)
            d[i] = M_D * (W_D[i + 1] ** 4 - 2 * W_D[i] ** 4 + W_D[i - 1] ** 4) - loss_term

        # 左边界 (井口)
        if 0.0 <= tau_D[0] <= t_m:
            loss_term_well = 2.0 * (np.sqrt(t_next - tau_D[0]) - np.sqrt(t_m - tau_D[0]))
        else:
            loss_term_well = 0.0

        a[0] = 0.0
        b[0] = 1 + 2 * M_D * (W_D[0] ** 3)
        c[0] = -2 * M_D * (W_D[1] ** 3)
        d[0] = M_D * (W_D[1] ** 4 - W_D[0] ** 4) + (dt_D / dx_D) - loss_term_well

        # 右边界 (尖端 W=0)
        a[N - 1] = 0.0
        b[N - 1] = 1.0
        c[N - 1] = 0.0
        d[N - 1] = 0.0

        delta_W = thomas_algorithm(a, b, c, d)
        W_D = W_D + delta_W
        W_D = np.maximum(W_D, 0.0)

        # 更新到达时间
        for i in range(1, N):
            if tau_D[i] < 0.0 and W_D[i] > 1e-8:
                tau_D[i] = t_next

        # 裂缝长度
        active_nodes = np.where(W_D > 1e-8)[0]
        current_length = x_D[active_nodes[-1]] if len(active_nodes) > 0 else 0.0
        current_length = max(current_length, L_prev)
        L_prev = current_length

        current_time += dt_D

        # 保存目标时刻剖面
        for t_target in target_times:
            if abs(t_next - t_target) < (dt_D / 2.0):
                saved_profiles[t_target] = W_D.copy()
                saved_lengths[t_target] = current_length

    # ---- 保存 ----
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, 'fdm_profiles.npz')
    np.savez(save_path,
             x_D=x_D,
             **{f'W_t{t:.0f}': saved_profiles[t] for t in target_times},
             **{f'L_t{t:.0f}': saved_lengths[t] for t in target_times},
             )
    print(f"FDM 剖面已保存至 {save_path}")
    for t_val in target_times:
        print(f"  t={t_val:.0f}: L={saved_lengths[t_val]:.3f}, W(0)={saved_profiles[t_val][0]:.4f}")

    return x_D, saved_profiles, saved_lengths


# ==========================================
# 3. 主程序
# ==========================================
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    solve_fdm(save_dir=script_dir)