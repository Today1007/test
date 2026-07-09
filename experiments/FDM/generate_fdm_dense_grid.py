# PKN FDM 密集网格生成器
# 保存所有时间步的 W(x) 剖面，用于与 PINN 做 2D 误差分布对比
# 与 PKN_comprehensive_FDM_final.py 数值格式完全一致

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
# 2. FDM 求解器 — 密集输出版本
# ==========================================
def solve_fdm_dense(N=201, L_D=8, T_total=80, dt_D=0.025,
                    save_interval=1, save_dir=None):
    """
    参数
    ----
    N : 空间网格点数
    L_D : 无量纲域长度
    T_total : 总时间
    dt_D : 时间步长
    save_interval : 每隔多少步保存一次 (默认1=每步保存)
    save_dir : 输出目录

    返回
    ----
    x_D (N,)
    t_save (N_t,)
    W_dense (N, N_t)  — 所有时刻的宽度剖面
    L_t_array (N_t,)  — 各时刻裂缝长度
    """
    if save_dir is None:
        save_dir = os.path.dirname(os.path.abspath(__file__))

    dx_D = L_D / (N - 1)
    x_D = np.linspace(0, L_D, N)

    time_steps = int(T_total / dt_D)

    W_D = np.zeros(N)
    tau_D = np.full(N, -1.0)
    tau_D[0] = 0.0
    L_prev = 0.0

    # 预估保存步数
    n_saves = time_steps // save_interval + 1
    W_list = []
    t_list = []
    L_list = []

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

            a[i] = -2 * (dt_D / (dx_D ** 2)) * (W_D[i - 1] ** 3)
            b[i] = 1 + 4 * (dt_D / (dx_D ** 2)) * (W_D[i] ** 3)
            c[i] = -2 * (dt_D / (dx_D ** 2)) * (W_D[i + 1] ** 3)
            d[i] = (dt_D / (dx_D ** 2)) * (W_D[i + 1] ** 4 - 2 * W_D[i] ** 4 + W_D[i - 1] ** 4) - loss_term

        # 左边界 (井口)
        if 0.0 <= tau_D[0] <= t_m:
            loss_term_well = 2.0 * (np.sqrt(t_next - tau_D[0]) - np.sqrt(t_m - tau_D[0]))
        else:
            loss_term_well = 0.0

        M_D = dt_D / (dx_D ** 2)
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

        # 按间隔保存
        if m % save_interval == 0 or m == time_steps:
            W_list.append(W_D.copy())
            t_list.append(current_time)
            L_list.append(current_length)

    # 拼接为 2D 数组
    W_dense = np.column_stack(W_list)   # (N, N_t)
    t_save = np.array(t_list)
    L_t_array = np.array(L_list)

    print(f"FDM 密集网格求解完成:")
    print(f"  时间步总数: {time_steps}")
    print(f"  实际保存: {len(t_list)} 个时刻 (间隔={save_interval})")
    print(f"  W_dense shape: {W_dense.shape}")
    print(f"  t 范围: [{t_save[0]:.3f}, {t_save[-1]:.3f}]")

    return x_D, t_save, W_dense, L_t_array


# ==========================================
# 3. 主程序
# ==========================================
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, 'fdm_dense.npz')

    x_D, t_save, W_dense, L_t_array = solve_fdm_dense(
        N=201, L_D=8, T_total=80, dt_D=0.025,
        save_interval=10,     # 每10步保存一次 → 约320个时刻
        save_dir=script_dir,
    )

    np.savez(save_path,
             x_D=x_D,
             t_save=t_save,
             W_dense=W_dense,
             L_t_array=L_t_array,
             description="FDM dense grid: W(x,t) at all saved time steps for 2D error comparison with PINN")

    print(f"\n密集网格已保存至 {save_path}")
    print(f"  内存大小: {os.path.getsize(save_path) / 1024:.1f} KB")
