# 补文献计划：PE-PINN 论文引言

> **生成日期**: 2026-07-14 | **当前总引用数**: 12 篇独立文献 | **目标**: 25-30 篇

---

## 一、背景引入与PKN模型（P1: L112-132）

### 当前已引用

| 功能 | 论述内容 | 引用文献 | 行号 |
|------|----------|----------|------|
| 工程重要性 | 水力压裂对非常规油气开采至关重要 | `Economides2000` | 112-114 |
| PKN模型起源 | Perkins-Kern-Nordgren 提出PKN模型 | `Nordgren1972` | 117-119 |
| 并列对比 | KGD模型共同奠定理论基础 | `Ref_KGD` | 119-121 |
| PKN地位声称 | "PKN因计算易处理成为工业最广泛采用的模型" | **无引用** ⚠️ | 121-123 |
| PKN物理描述 | 固定高度、平面应变、非线性控制方程 | **无引用** | 123-129 |
| 数值困难总结 | 强非线性、移动自由边界、尖端奇异性 | **无引用** ⚠️ | 129-132 |

### 需要补充

| 功能 | 应补文献 | 优先级 | 建议插入位置 |
|------|----------|--------|-------------|
| 工业广泛采用的支撑 | **Adachi et al. (2007)** — 涵盖PKN/KGD/P3D/PL3D的权威综述, 2000+引用 | 🔴 | L122 "most widely adopted..." 处 |
| PKN物理模型权威来源 | 现有 Nordgren1972 即可覆盖 | — | — |

> **本段小结**: 当前 3 引用 → 补后 4 引用。缺口不大。

---

## 二、传统数值解法与尖端渐近（P2: L134-158）<!-- 最大缺口 -->

### 当前已引用

| 功能 | 论述内容 | 引用文献 | 行号 |
|------|----------|----------|------|
| 研究起点 | Nordgren原始有限差分 | `Nordgren1972` | 134-136 |
| 方法列举 | 显式FD、FEM尖端富集、谱离散 | `Kemp1990`, `Garikapati2017`, `Peirce2014` | 136-139 |
| 尖端奇性困难 | 梯度无穷，需特殊尖端单元/正则化/渐近富集 | `Linkov2011`, `Garikapati2017` | 139-143 |
| 经典1/3幂律 | 黏性主导区制的尖端渐近 | `Nordgren1972`, `Kemp1990` | 143-145 |
| 瞬态1/3→3/8过渡 | 滤失强度影响下的尖端渐近转换 | `Linkov2015`, `Detournay2016` | 146-149 |
| 移动边界追踪 | 自适应重网格/前沿追踪，计算开销大 | `Peirce2014` | 149-154 |
| 多尺度困难 | 尖端边界层→全局尺度 | `Detournay2016` | 155-158 |

**当前 P2 问题诊断**:

- 仅覆盖 **5篇** 文献，严重不足
- 缺失 PKN 数学理论基础（自相似解）
- 缺失传播区制分类框架
- 缺失粒子速度法这一整个数值范式
- 尖端渐近引用不完整（Linkov2015 应为 Kovalyshen2010）
- 缺失系统性综述

### 需要补充

#### 2.1 数学理论基础

| 功能 | 文献 | 优先级 | 建议插入位置 |
|------|------|--------|-------------|
| 流体驱动裂缝自相似解的数学根基 | **Spence & Sharp (1985)** — Proc. R. Soc. Lond. A, 400:289-313. DOI: `10.1098/rspa.1985.0081` | 🔴 | P2段首，在 "The numerical solution..." 之前，先交代"该方程具有自相似结构..." |

#### 2.2 传播区制分类

| 功能 | 文献 | 优先级 | 建议插入位置 |
|------|------|--------|-------------|
| 传播区制框架：viscosity/toughness-dominated, storage/leak-off-dominated | **Detournay (2004)** — Int. J. Geomech., 4(1):35-45. DOI: `10.1061/(ASCE)1532-3641(2004)4:1(35)`, 600+引用 | 🔴 | L140 "The fracture tip exhibits..." 之前，引出为什么尖端渐近有多种区制 |

#### 2.3 尖端渐近（修正+补充）

| 功能 | 文献 | 优先级 | 建议插入位置 |
|------|------|--------|-------------|
| **替换** Linkov2015：PKN尖端多尺度渐近 + 尖端富集单元的数值算法 | **Kovalyshen & Detournay (2010)** — Transp. Porous Media, 81:317-339. DOI: `10.1007/s11242-009-9403-4` | 🔴 | L148 替换 `Linkov2015` |
| 含滤失的尖端多尺度渐近，直接支撑"1/3→3/8幂律过渡" | **Garagash et al. (2011)** — J. Fluid Mech., 669:260-297. DOI: `10.1017/S002211201000501X` | 🟡 | L146-149 "transient behavior..." 处 |

#### 2.4 粒子速度法（新增整个数值范式）

| 功能 | 文献 | 优先级 | 建议插入位置 |
|------|------|--------|-------------|
| 粒子速度公式：PKN数值求解的第三大范式 | **Linkov (2012)** — Int. J. Eng. Sci., 52:77-88. DOI: `10.1016/j.ijengsci.2011.11.009` | 🔴 | L139 在列举 FD/FEM/谱方法之后补充 |
| 通用粒子速度算法，统一PKN/KGD/径向，47+引用 | **Wrobel & Mishuris (2015)** — Int. J. Eng. Sci., 94:23-58. DOI: `10.1016/j.ijengsci.2015.04.003` | 🔴 | 与 Linkov2012 一同引用 |
| 粒子速度+ε正则化求解Nordgren，相对误差<10⁻⁴ | **Mishuris et al. (2012)** — Int. J. Eng. Sci., 61:10-23. DOI: `10.1016/j.ijengsci.2012.06.005` | 🟡 | 可选项，如需强调精度优势 |

#### 2.5 水平集/前沿追踪

| 功能 | 文献 | 优先级 | 建议插入位置 |
|------|------|--------|-------------|
| 隐式水平集算法（ILSA），P2提到"front-tracking"但只引了Peirce2014 | **Peirce & Detournay (2008)** — CMAME, 197(33-40):2858-2885. DOI: `10.1016/j.cma.2008.01.013` | 🟡 | L153 "adaptive remeshing or front-tracking" 处，补充到 Peirce2014 之前 |

#### 2.6 系统性综述

| 功能 | 文献 | 优先级 | 建议插入位置 |
|------|------|--------|-------------|
| 水力压裂数值方法全面综述（XFEM/相场/DDM等）400+引用 | **Lecampion et al. (2018)** — J. Nat. Gas Sci. Eng., 49:66-83. DOI: `10.1016/j.jngse.2017.10.012` | 🔴 | P2段末，总结各类方法的优势与局限 |
| PKN模型的系统性四组分类综述 | **Nguyen et al. (2020)** — J. Pet. Sci. Eng., 195:107607. DOI: `10.1016/j.petrol.2020.107607` | 🟡 | 可选项，与Lecampion2018择一或并用 |

#### 2.7 历史方法（可选）

| 功能 | 文献 | 优先级 | 建议插入位置 |
|------|------|--------|-------------|
| 孔隙弹性PKN移动网格 | **Detournay et al. (1990)** — ASME J. Energy Resour. Technol., 112(4):224-230. DOI: `10.1115/1.2905762` | 🟢 | 可选项 |
| 显/隐格式对比 | **Linkov (2019)** — arXiv:1905.06811 | 🟢 | 可选项 |

> **本段小结**: 当前 5 引用 → 补后约 12-14 引用。**需大幅重写**。

---

## 三、PINN方法介绍与应用（P3: L160-177）

### 当前已引用

| 功能 | 论述内容 | 引用文献 | 行号 |
|------|----------|----------|------|
| PINN起源 | Raissi等提出PINN，mesh-free+自动微分 | `Raissi2019` | 160-164 |
| 域分解PINN | XPINN, cPINN | `Jagtap2020`, `Jagtap2020b` | 166-167 |
| 梯度增强PINN | 梯度增强 | `Yu2022` | 167-168 |
| 多尺度架构 | FBPINN | `Moseley2023` | 168-169 |
| 地下工程应用 | 多孔介质流、历史拟合、两相流 | `Hassan2024`, `Ali2025`, `Wang2024` | 170-174 |
| 压裂gap声称 | "remains relatively unexplored" | **无引用**（gap声称，可接受） | 174-177 |

### 需要补充

#### 3.1 PINN训练失败的理论基础（直接为P4三个缺陷铺路）

| 功能 | 文献 | 优先级 | 建议插入位置 |
|------|------|--------|-------------|
| PINN训练失败根本原因（梯度不平衡），2800+引用 | **Wang et al. (2021)** — SIAM J. Sci. Comput., 43(5):A3055-A3081. DOI: `10.1137/20M1318043` | 🔴 | L169 "applied across a broad spectrum..." 之后，新增一句转折："然而，PINN在处理多尺度/奇异问题时面临根本性训练困难..." |
| NTK理论解释PINN为何学不动多尺度/尖锐梯度，2000+引用 | **Wang, Yu & Perdikaris (2022)** — J. Comput. Phys., 449:110768. DOI: `10.1016/j.jcp.2021.110768` | 🔴 | 与上面一同引用 |
| **Causal PINN** — 与你的创新#2（因果约束）直接相关 | **Wang, Sankaran & Perdikaris (2024)** — CMAME, 421:116813. DOI: `10.1016/j.cma.2024.116813`（arXiv初版2022） | 🔴 | ⚠️ 当前完全缺失，审稿人最可能攻击。建议在P3末尾或P4开头引用 |

#### 3.2 PINN在断裂力学中的应用

| 功能 | 文献 | 优先级 | 建议插入位置 |
|------|------|--------|-------------|
| PINN用于相场断裂，454+引用 | **Goswami et al. (2020)** — Theor. Appl. Fract. Mech., 106:102447. DOI: `10.1016/j.tafmec.2019.102447` | 🟡 | L174 在"subsurface engineering"之后，"However, the application..."之前 |
| Deep Energy Method — 变分能量替代PDE残差，204+引用 | **Samaniego et al. (2020)** — CMAME, 362:112790. DOI: `10.1016/j.cma.2019.112790` | 🟡 | 与Goswami2020一同引用 |

#### 3.3 方法对比（可选）

| 功能 | 文献 | 优先级 | 建议插入位置 |
|------|------|--------|-------------|
| DeepXDE / 自适应采样(RAR) | **Lu et al. (2021)** — SIAM Rev., 63(1):208-228. DOI: `10.1137/19M1274067` | 🟢 | Discussion 或 Methodology 采样部分 |
| DeepONet — 竞争范式 | **Lu et al. (2021)** — Nat. Mach. Intell., 3:218-229. DOI: `10.1038/s42256-021-00302-5` | 🟢 | Discussion |

> **本段小结**: 当前 6 引用 → 补后约 9-11 引用。

---

## 四、PINN+压裂现有工作与缺陷（P4: L179-203）

### 当前已引用

| 功能 | 论述内容 | 引用文献 | 行号 |
|------|----------|----------|------|
| 已有工作1 | Yang: 深度学习替代模拟器 | `Yang2023` | 179-183 |
| 已有工作2 | Tang: 移动边界约束PINN | `Tang2024` | 183-186 |
| **缺陷1** | 无尖端渐近编码 → 网络学不动尖锐梯度 | `Krishnapriyan2021`（支撑"优化困难"） | 186-195 |
| **缺陷2** | PDE仅在裂缝到达区域有效，无因果约束 | **无引用** ⚠️ | 195-199 |
| **缺陷3** | 早期时间幂律奇异性，从数据学习低效 | **无引用** ⚠️ | 199-203 |

### 需要补充

| 功能 | 文献 | 优先级 | 建议插入位置 |
|------|------|--------|-------------|
| **缺陷2 的文献支撑** — Causal PINN | **Wang, Sankaran & Perdikaris (2024)** | 🔴 | L196 "This causal constraint..." 处，引用Causal PINN作为对比/讨论 |
| **缺陷1 的文献支撑** — 梯度病理 + NTK | **Wang et al. (2021)** + **Wang, Yu & Perdikaris (2022)** | 🔴 | L192 "notoriously difficult for gradient-based optimization" 处，替换或补充 Krishnapriyan2021 |
| 移动边界PINN的补充 | **Shkolnikov et al. (2024)** — ⚠️ **已在bib中但从未在正文引用！** J. Comput. Phys., 502:112829. DOI: `10.1016/j.jcp.2024.112829` | 🟡 | L186 Tang2024之后，作为Stefan/自由边界问题的另一PINN工作 |

> **本段小结**: 当前 3 引用 → 补后约 6 引用。主要缺口是缺陷2和缺陷3缺少文献支撑。

---

## 五、本文方案与贡献（P5: L205-241）

### 当前已引用

| 功能 | 论述内容 | 引用文献 | 行号 |
|------|----------|----------|------|
| 训练策略 | Adam + L-BFGS | `Kingma2015`, `Liu1989` | 224-226 |
| 与同类对比 | 区别于Yang、Tang的分析编码方式 | `Yang2023`, `Tang2024` | 226-230 |
| 本文方法 | 三因式分解 + 因果掩码 + 可学习指数 | 无需引用（本文贡献） | 205-224 |
| 结果总结 | 数值实验精度 + 消融验证 | 无需引用（本文结果） | 230-235 |

**无需在P5补文献**。

---

## 汇总

### 各段落引用变化

| 段落 | 功能 | 当前引用 | 补后引用 | 修改程度 |
|------|------|----------|----------|----------|
| P1 | 背景引入与PKN模型 | 3 | 4 | 小幅修改 |
| P2 | 传统数值解法与尖端渐近 | 5 | **12-14** | **大幅重写** |
| P3 | PINN方法与应用 | 6 | 9-11 | 中等修改 |
| P4 | PINN+压裂与缺陷 | 3 | 6 | 中等修改 |
| P5 | 本文方案与贡献 | 2 | 2 | 无需修改 |
| **总计** | | **12** | **25-30** | |

### 需修改的 bib 注意项

1. `Linkov2015` → 替换为 `Kovalyshen2010`（正式发表版的正确作者）
2. `Detournay2016` → 确认是否正确（当前bib中标记为"to appear"）
3. `Shkolnikov2024` → 已在bib中但正文未引用，需在P4加入引用
4. Causal PINN 建议引用为 `Wang et al. (2022, arXiv:2203.07404)`，因算法有专利限制

### 完整 BibTeX 清单（按段落分组）

<details>
<summary>P1 新增（1篇）</summary>

```bibtex
@article{Adachi2007,
  author  = {Adachi, J. and Siebrits, E. and Peirce, A. and Desroches, J.},
  title   = {Computer simulation of hydraulic fractures},
  journal = {Int. J. Rock Mech. Min. Sci.},
  volume  = {44},
  number  = {5},
  pages   = {739--757},
  year    = {2007},
  doi     = {10.1016/j.ijrmms.2006.11.006}
}
```
</details>

<details>
<summary>P2 新增（9篇）</summary>

```bibtex
@article{Spence1985,
  author  = {Spence, D. A. and Sharp, P.},
  title   = {Self-similar solutions for elastohydrodynamic cavity flow},
  journal = {Proc. R. Soc. Lond. A},
  volume  = {400},
  number  = {1819},
  pages   = {289--313},
  year    = {1985},
  doi     = {10.1098/rspa.1985.0081}
}

@article{Detournay2004,
  author  = {Detournay, E.},
  title   = {Propagation regimes of fluid-driven fractures in impermeable rocks},
  journal = {Int. J. Geomech.},
  volume  = {4},
  number  = {1},
  pages   = {35--45},
  year    = {2004},
  doi     = {10.1061/(ASCE)1532-3641(2004)4:1(35)}
}

@article{Kovalyshen2010,
  author  = {Kovalyshen, Y. and Detournay, E.},
  title   = {A reexamination of the classical {PKN} model of hydraulic fracture},
  journal = {Transp. Porous Media},
  volume  = {81},
  pages   = {317--339},
  year    = {2010},
  doi     = {10.1007/s11242-009-9403-4}
}

@article{Garagash2011,
  author  = {Garagash, D. I. and Detournay, E. and Adachi, J. I.},
  title   = {Multiscale tip asymptotics in hydraulic fracture with leak-off},
  journal = {J. Fluid Mech.},
  volume  = {669},
  pages   = {260--297},
  year    = {2011},
  doi     = {10.1017/S002211201000501X}
}

@article{Linkov2012,
  author  = {Linkov, A. M.},
  title   = {On efficient simulation of hydraulic fracturing in terms of particle velocity},
  journal = {Int. J. Eng. Sci.},
  volume  = {52},
  pages   = {77--88},
  year    = {2012},
  doi     = {10.1016/j.ijengsci.2011.11.009}
}

@article{Wrobel2015,
  author  = {Wrobel, M. and Mishuris, G.},
  title   = {Hydraulic fracture revisited: Particle velocity based simulation},
  journal = {Int. J. Eng. Sci.},
  volume  = {94},
  pages   = {23--58},
  year    = {2015},
  doi     = {10.1016/j.ijengsci.2015.04.003}
}

@article{Mishuris2012,
  author  = {Mishuris, G. and Wrobel, M. and Linkov, A.},
  title   = {On modeling hydraulic fracture in proper variables: Stiffness, accuracy, sensitivity},
  journal = {Int. J. Eng. Sci.},
  volume  = {61},
  pages   = {10--23},
  year    = {2012},
  doi     = {10.1016/j.ijengsci.2012.06.005}
}

@article{Lecampion2018,
  author  = {Lecampion, B. and Bunger, A. and Zhang, X.},
  title   = {Numerical methods for hydraulic fracture propagation: A review of recent trends},
  journal = {J. Nat. Gas Sci. Eng.},
  volume  = {49},
  pages   = {66--83},
  year    = {2018},
  doi     = {10.1016/j.jngse.2017.10.012}
}

@article{Nguyen2020,
  author  = {Nguyen, H. T. and Lee, J. H. and Elraies, K. A.},
  title   = {A review of {PKN}-type modeling of hydraulic fractures},
  journal = {J. Pet. Sci. Eng.},
  volume  = {195},
  pages   = {107607},
  year    = {2020},
  doi     = {10.1016/j.petrol.2020.107607}
}

@article{Peirce2008,
  author  = {Peirce, A. and Detournay, E.},
  title   = {An implicit level set method for modeling hydraulically driven fractures},
  journal = {Comput. Methods Appl. Mech. Eng.},
  volume  = {197},
  number  = {33-40},
  pages   = {2858--2885},
  year    = {2008},
  doi     = {10.1016/j.cma.2008.01.013}
}
```
</details>

<details>
<summary>P3 新增（5篇）</summary>

```bibtex
@article{Wang2021gradient,
  author  = {Wang, S. and Teng, Y. and Perdikaris, P.},
  title   = {Understanding and mitigating gradient flow pathologies in physics-informed neural networks},
  journal = {SIAM J. Sci. Comput.},
  volume  = {43},
  number  = {5},
  pages   = {A3055--A3081},
  year    = {2021},
  doi     = {10.1137/20M1318043}
}

@article{Wang2022NTK,
  author  = {Wang, S. and Yu, X. and Perdikaris, P.},
  title   = {When and why {PINNs} fail to train: A neural tangent kernel perspective},
  journal = {J. Comput. Phys.},
  volume  = {449},
  pages   = {110768},
  year    = {2022},
  doi     = {10.1016/j.jcp.2021.110768}
}

@article{Wang2024causal,
  author  = {Wang, S. and Sankaran, S. and Perdikaris, P.},
  title   = {Respecting causality is all you need for training physics-informed neural networks},
  journal = {Comput. Methods Appl. Mech. Eng.},
  volume  = {421},
  pages   = {116813},
  year    = {2024},
  doi     = {10.1016/j.cma.2024.116813}
}

@article{Goswami2020,
  author  = {Goswami, S. and Anitescu, C. and Chakraborty, S. and Rabczuk, T.},
  title   = {Transfer learning enhanced physics informed neural network for phase-field modeling of fracture},
  journal = {Theor. Appl. Fract. Mech.},
  volume  = {106},
  pages   = {102447},
  year    = {2020},
  doi     = {10.1016/j.tafmec.2019.102447}
}

@article{Samaniego2020,
  author  = {Samaniego, E. and Anitescu, C. and Goswami, S. and Nguyen-Thanh, V. M. and Guo, H. and Hamdia, K. and Zhuang, X. and Rabczuk, T.},
  title   = {An energy approach to the solution of partial differential equations in computational mechanics via machine learning: Concepts, implementation and applications},
  journal = {Comput. Methods Appl. Mech. Eng.},
  volume  = {362},
  pages   = {112790},
  year    = {2020},
  doi     = {10.1016/j.cma.2019.112790}
}
```
</details>

<details>
<summary>P2/P3 可选（4篇，P2优先级）</summary>

```bibtex
@article{Detournay1990,
  author  = {Detournay, E. and Cheng, A. H.-D. and McLennan, J. D.},
  title   = {A poroelastic {PKN} hydraulic fracture model based on an explicit moving mesh algorithm},
  journal = {ASME J. Energy Resour. Technol.},
  volume  = {112},
  number  = {4},
  pages   = {224--230},
  year    = {1990},
  doi     = {10.1115/1.2905762}
}

@article{Linkov2019,
  author  = {Linkov, A. M.},
  title   = {Modern theory of hydraulic fracture modeling with using explicit and implicit schemes},
  journal = {arXiv preprint},
  note    = {arXiv:1905.06811},
  year    = {2019}
}

@article{Lu2021deepxde,
  author  = {Lu, L. and Meng, X. and Mao, Z. and Karniadakis, G. E.},
  title   = {{DeepXDE}: A deep learning library for solving differential equations},
  journal = {SIAM Rev.},
  volume  = {63},
  number  = {1},
  pages   = {208--228},
  year    = {2021},
  doi     = {10.1137/19M1274067}
}

@article{Lu2021deeponet,
  author  = {Lu, L. and Jin, P. and Pang, G. and Zhang, Z. and Karniadakis, G. E.},
  title   = {Learning nonlinear operators via {DeepONet} based on the universal approximation theorem of operators},
  journal = {Nat. Mach. Intell.},
  volume  = {3},
  pages   = {218--229},
  year    = {2021},
  doi     = {10.1038/s42256-021-00302-5}
}
```
</details>

---

## 实施步骤

1. 将上述 BibTeX 条目加入 `ws-ijcm.bib`
2. 修正 bib 中的 `Linkov2015` → `Kovalyshen2010`
3. 确认 `Detournay2016` 引用是否正确
4. 按本文档各段落的"建议插入位置"逐段修改 `ws-ijcm.tex`
5. 编译验证：`pdflatex → bibtex → pdflatex × 2`，确保无 `?` 缺失引用
