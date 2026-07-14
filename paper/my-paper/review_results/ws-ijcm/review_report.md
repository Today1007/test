# 深度审稿报告

**论文**: `E:\PKN Sesearch\paper\my-paper\ws-ijcm.tex` | **语言**: ZH | **模式**: deep-review
**生成时间**: 2026-07-14 21:55
**审稿焦点**: `methodology`
**工件目录**: `E:\PKN Sesearch\paper\my-paper\review_results\ws-ijcm`

## 总体评估

Deep review found 0 major, 2 moderate, 0 minor issues. The highest-priority concerns are: Cross-section numeric consistency should be reconciled.

- **主要**: 0
- **中等**: 2
- **次要**: 0

## 学术预审委员会

### 评审 2（方法与透明度）

## Methodology Transparency Review (SRQR-aware)

### MUST-FIX (submission blockers)
- No methodology blocker was surfaced by the fallback pass.

### SHOULD-FIX (quality improvements)
- (introduction) "Section~2 formulates the PKN governing equations." — Multiple sections contain numeric claims. Confirm that the same quantities reconcile across main text, tables, and appendix material.
- (method) "A finite difference (FD) solver is implemented as the reference baseline for evaluating the accuracy of the proposed method." — Comparative evaluation language was detected. Deep review should verify that baseline tuning, data splits, and reporting conventions are described symmetrically.

### SRQR Checklist Deltas
- Sampling rationale: clarify how the evidence base supports the paper's strongest claims.
- Data collection details (time/place/duration): add context when results depend on specific settings.
- Coding process (stages, coders, disagreement resolution): specify if qualitative or hybrid analysis is used.
- Saturation: state whether the evidence scope is exhaustive or bounded.
- Triangulation: explain whether multiple evidence sources were reconciled.
- Reflexivity: acknowledge researcher choices that shape interpretation.

## 论文摘要

# Paper Summary: ws-ijcm

## Research Question
- sec:intro Hydraulic fracturing is a crucial technology for enhancing hydrocarbon recovery from unconventional reservoirs Economides2000

## Core Thesis
- To address these challenges, this paper proposes PE-PINN (Physics-Enhanced PINN), a novel framework for the PKN model that explicitly embeds physical prior knowledge into the network architecture.

## Headline Claims
- To address these challenges, this paper proposes PE-PINN (Physics-Enhanced PINN), a novel framework for the PKN model that explicitly embeds physical prior knowledge into the network architecture.
- The remainder of this paper is organized as follows.

## Section Map
- introduction (110-245): 1071 words
- method (408-649): 1521 words
- result (650-732): 520 words
- conclusion (733-747): 97 words

## Closure Targets
- sec:conclusion This paper presented PE-PINN, a Physics-Enhanced PINN framework for the PKN model of hydraulic fracture propagation.

## 中等问题

### M1: Cross-section numeric consistency should be reconciled
- **类型**: presentation
- **来源**: [LLM] via `notation_and_numeric_consistency`
- **置信度**: medium
- **章节**: introduction
- **关联章节**: introduction, method, result
- **根因键**: `cross-section-numeric-consistency-should-be-reconciled`
- **原文已核对**: 否
- **原文**: `Section~2 formulates the PKN governing equations.`
- **说明**: Multiple sections contain numeric claims. Confirm that the same quantities reconcile across main text, tables, and appendix material.

### M2: Comparison protocol should make fairness assumptions explicit
- **类型**: methodology
- **来源**: [LLM] via `evaluation_fairness_and_reproducibility`
- **置信度**: medium
- **章节**: method
- **关联章节**: method
- **根因键**: `comparison-protocol-should-make-fairness-assumptions-explicit`
- **原文已核对**: 否
- **原文**: `A finite difference (FD) solver is implemented as the reference baseline for evaluating the accuracy of the proposed method.`
- **说明**: Comparative evaluation language was detected. Deep review should verify that baseline tuning, data splits, and reporting conventions are described symmetrically.

## Phase 0 自动审查发现

### [Script] BIB

| 行号 | 严重度 | 问题 |
|------|--------|------|
| --- | Minor | Check: E:\PKN Sesearch\paper\my-paper\ws-ijcm.tex |
| --- | Minor | PASS |
| --- | Minor | entries: 0 |
| --- | Minor | entries: 0 |

### [Script] CITATIONS

| 行号 | 严重度 | 问题 |
|------|--------|------|
| --- | Minor | No citation stacking issues found. |

### [Script] DEAI

| 行号 | 严重度 | 问题 |
|------|--------|------|
| --- | Minor | Use --analyze for full analysis |

### [Script] EXPERIMENT

| 行号 | 严重度 | 问题 |
|------|--------|------|
| 660 | Major | Performance claim is not tied to a concrete metric or numeric result. |
| 708 | Major | Performance claim lacks an explicit baseline or comparator. |
| 650 | Minor | No statistical significance, variance, or confidence information is mentioned. |
| 733 | Minor | Conclusion lacks implications or broader impact statement. |
| 733 | Minor | Conclusion lacks explicit summary of core findings. |

### [Script] FIGURES

| 行号 | 严重度 | 问题 |
|------|--------|------|
| --- | Minor | figures in E:\PKN Sesearch\paper\my-paper\ws-ijcm.tex... |
| --- | Minor | 1 figures. |
| --- | Minor | Line 443: figs/network-architecture.pdf |
| --- | Minor | All figures passed check. |

### [Script] FORMAT

| 行号 | 严重度 | 问题 |
|------|--------|------|
| --- | Minor | ============================================================ |
| --- | Minor | Format Check Report |
| --- | Minor | ============================================================ |
| --- | Minor | E:\PKN Sesearch\paper\my-paper\ws-ijcm.tex |
| --- | Minor | WARNING |
| --- | Minor | Found 55 issues |
| --- | Minor | Found |
| --- | Minor | (1 issues) |
| --- | Minor | 613: You should perhaps use `\max' instead. |
| --- | Minor | (3 issues) |
| --- | Minor | 371: You should enclose the previous parenthesis with `{}'. |
| --- | Minor | 533: You should enclose the previous parenthesis with `{}'. |
| --- | Minor | 552: You should enclose the previous parenthesis with `{}'. |
| --- | Minor | (1 issues) |
| --- | Minor | 65: Wrong length of dash may have been used. |
| --- | Minor | (50 issues) |
| --- | Minor | 41: Command terminated with space. |
| --- | Minor | 41: Intersentence spacing (`\@') should perhaps be used. |
| --- | Minor | 101: Command terminated with space. |
| --- | Minor | 101: Command terminated with space. |
| --- | Minor | 101: Command terminated with space. |
| --- | Minor | ... and 45 more |
| --- | Minor | ============================================================ |

### [Script] GRAMMAR

| 行号 | 严重度 | 问题 |
|------|--------|------|
| --- | Minor | No rule-based issues detected in selected scope. |

### [Script] LOGIC

| 行号 | 严重度 | 问题 |
|------|--------|------|
| --- | Major | (Lines 733-747) : [Script] Cross-section logic chain may be incomplete |
| --- | Minor | 1 contribution claim(s) in Introduction but no explicit answer language in Conclusion. |
| --- | Minor | Add statements that explicitly address each contribution. |
| --- | Minor | Conclusion should close the logic chain opened in Introduction. |
| --- | Major | Abstract, contribution claims, and conclusion may be misaligned. |
| --- | Minor | abstract missing contribution claim; conclusion missing contribution response. |
| --- | Minor | Make sure all three sections consistently state the problem, method, key results, and contribution. |
| --- | Minor | These sections should tell the same core story with different emphasis, not diverge. |

### [Script] PRESUBMISSION

| 行号 | 严重度 | 问题 |
|------|--------|------|
| --- | Major | [A1] Abstract five-element check is incomplete; missing background, quantitative results. |
| 112 | Minor | [G2] Long paragraph detected (191 words, 8 sentences); split or add a clearer topic sentence. |
| 179 | Minor | [G2] Long paragraph detected (221 words, 11 sentences); split or add a clearer topic sentence. |
| 205 | Minor | [G2] Long paragraph detected (262 words, 10 sentences); split or add a clearer topic sentence. |
| 114 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 119 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 120 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 136 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 137 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 138 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 139 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 142 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 143 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 145 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 149 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 154 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 158 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 161 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 167 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 167 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 168 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 169 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 172 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 173 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 174 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 193 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 224 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 225 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 227 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 253 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 269 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 279 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 340 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 368 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 384 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 387 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 477 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 582 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 586 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 621 | Minor | [L1] LaTeX citation should use a non-breaking tie before citation, e.g. `Method~\cite{key}`. |
| 346 | Minor | [L3] LaTeX label `eq:nordgren-dim` uses hyphens; prefer underscores for portability. |
| 353 | Minor | [L3] LaTeX label `eq:bc-dim` uses hyphens; prefer underscores for portability. |
| 490 | Minor | [L3] LaTeX label `eq:tau-inversion` uses hyphens; prefer underscores for portability. |
| 524 | Minor | [L3] LaTeX label `eq:pde-residual` uses hyphens; prefer underscores for portability. |
| 534 | Minor | [L3] LaTeX label `eq:loss-pde` uses hyphens; prefer underscores for portability. |
| 553 | Minor | [L3] LaTeX label `eq:loss-bc` uses hyphens; prefer underscores for portability. |
| 561 | Minor | [L3] LaTeX label `eq:loss-total` uses hyphens; prefer underscores for portability. |
| 696 | Minor | [L3] LaTeX label `tab:sensitivity-time` uses hyphens; prefer underscores for portability. |
| 316 | Minor | [L5] Numbered equation label `eq:bc` is never referenced in text. |
| 332 | Minor | [L5] Numbered equation label `eq:dimless` is never referenced in text. |
| 519 | Minor | [L5] Numbered equation label `eq:pde-residual` is never referenced in text. |
| 529 | Minor | [L5] Numbered equation label `eq:loss-pde` is never referenced in text. |
| 545 | Minor | [L5] Numbered equation label `eq:loss-bc` is never referenced in text. |
| 557 | Minor | [L5] Numbered equation label `eq:loss-total` is never referenced in text. |
| 684 | Minor | [F1] Caption lacks a concrete finding or comparison cue; add the specific result the figure/table is meant to communicate. |
| 696 | Minor | [F1] Caption lacks a concrete finding or comparison cue; add the specific result the figure/table is meant to communicate. |

### [Script] REFERENCES

| 行号 | 严重度 | 问题 |
|------|--------|------|
| 320 | Minor | Unreferenced label: \label{eq:bc} is never cited in text |
| 337 | Minor | Unreferenced label: \label{eq:dimless} is never cited in text |
| 524 | Minor | Unreferenced label: \label{eq:pde-residual} is never cited in text |
| 534 | Minor | Unreferenced label: \label{eq:loss-pde} is never cited in text |
| 553 | Minor | Unreferenced label: \label{eq:loss-bc} is never cited in text |
| 561 | Minor | Unreferenced label: \label{eq:loss-total} is never cited in text |
| 598 | Minor | Reference before definition: \ref{tab:params} at line 598 appears before label definition at line 605 |
| 679 | Minor | Reference before definition: \ref{tab:sensitivity} at line 679 appears before label definition at line 684 |

### [Script] SENTENCES

| 行号 | 严重度 | 问题 |
|------|--------|------|
| --- | Minor | SENTENCE (Line 112, 42 words, 4 clauses) |
| --- | Minor | Under this assumption, the local elasticity relation yields a nonlinear governing equation that balances the temporal evolution of fracture width, the fluid leak-off into the surrounding formation, and the longitudinal gradient of the volumetric flow rate governed by the fluid's viscous resistance. |
| --- | Minor | Under this assumption. the local elasticity relation yields a nonlinear governing equation that balances the temporal evolution of fracture width. the fluid leak-off into the surrounding formation. and the longitudinal gradient of the volumetric flow rate governed by the fluid's viscous resistance.. |
| --- | Minor | Sentence exceeds complexity threshold, split for readability. |
| --- | Minor | SENTENCE (Line 134, 26 words, 4 clauses) |
| --- | Minor | The fracture tip exhibits a singular gradient that tends to infinity, requiring special tip elements, regularization techniques , or asymptotic enrichment functions to avoid severe accuracy degradation. |
| --- | Minor | The fracture tip exhibits a singular gradient that tends to infinity. requiring special tip elements. regularization techniques. or asymptotic enrichment functions to avoid severe accuracy degradation.. |
| --- | Minor | Sentence exceeds complexity threshold, split for readability. |
| --- | Minor | SENTENCE (Line 160, 28 words, 4 clauses) |
| --- | Minor | Recently, PINNs have been applied to the field of subsurface engineering, including flow and transport in porous media  , history-matching in fractured reservoirs  , and two-phase flow in heterogeneous formations  . |
| --- | Minor | Recently. PINNs have been applied to the field of subsurface engineering. including flow and transport in porous media. history-matching in fractured reservoirs. and two-phase flow in heterogeneous formations  .. |
| --- | Minor | Sentence exceeds complexity threshold, split for readability. |
| --- | Minor | SENTENCE (Line 237, 18 words, 4 clauses) |
| --- | Minor | Section~3 describes the proposed PE-PINN framework, including the network design, loss function, training strategy, and experimental configuration. |
| --- | Minor | Section~3 describes the proposed PE-PINN framework. including the network design. loss function. training strategy. and experimental configuration.. |
| --- | Minor | Sentence exceeds complexity threshold, split for readability. |
| --- | Minor | SENTENCE (Line 417, 49 words, 5 clauses) |
| --- | Minor | Rather than directly approximating the fracture width with a generic neural network, the proposed method decomposes the solution into three physically meaningful components: \begin{equation} \widehat{W}(x, t; \theta, \alpha) = t^{\alpha}\; \Omega_{\rm tip}\!\left(1 - \frac{x}{L(t)}\right)\; \mathcal{N}_{\theta}(x, t), |
| --- | Minor | Rather than directly approximating the fracture width with a generic neural network. the proposed method decomposes the solution into three physically meaningful components: \begin{equation} \widehat{W}(x. t; \theta. \alpha) = t^{\alpha}\; \Omega_{\rm tip}\!\left(1 - \frac{x}{L(t)}\right)\; \mathcal{N}_{\theta}(x. t). |
| --- | Minor | Sentence exceeds complexity threshold, split for readability. |
| --- | Minor | SENTENCE (Line 479, 34 words, 4 clauses) |
| --- | Minor | To enforce this causal constraint, the arrival time at each spatial coordinate is computed by numerically inverting the crack-length evolution Eq.~  using Brent's root-finding method: \begin{equation} \tau(x) = \{\,t \mid L(t) = x\,\}, |
| --- | Minor | To enforce this causal constraint. the arrival time at each spatial coordinate is computed by numerically inverting the crack-length evolution Eq.~  using Brent's root-finding method: \begin{equation} \tau(x) = \{\. t \mid L(t) = x\. \}. |
| --- | Minor | Sentence exceeds complexity threshold, split for readability. |
| --- | Minor | SENTENCE (Line 564, 36 words, 5 clauses) |
| --- | Minor | The sampling strategy employs a three-tier scheme: 10,000 points in the early-time region ( ), 20,000 points in the late-time region ( ), and 10,000 points in the near-tip refinement zone ( ) to resolve the sharp spatial gradients. |
| --- | Minor | The sampling strategy employs a three-tier scheme: 10. 000 points in the early-time region ( ). 20. 000 points in the late-time region ( ). and 10. 000 points in the near-tip refinement zone ( ) to resolve the sharp spatial gradients.. |
| --- | Minor | Sentence exceeds complexity threshold, split for readability. |
| --- | Minor | SENTENCE (Line 625, 66 words, 6 clauses) |
| --- | Minor | To isolate the contribution of each component of the proposed framework, four model variants are constructed: (i) the full PE-PINN incorporating all three enhancements; (ii) a variant without the time-power factor, i.e.,   in Eq.~ ; (iii) a variant without the transient tip shape function, i.e.,  ; and (iv) a plain PINN without any of the proposed components, equivalent to directly approximating   with a standard neural network. |
| --- | Minor | To isolate the contribution of each component of the proposed framework. four model variants are constructed: (i) the full PE-PINN incorporating all three enhancements; (ii) a variant without the time-power factor. i.e.. in Eq.~ ; (iii) a variant without the transient tip shape function. i.e.. ; and (iv) a plain PINN without any of the proposed components. equivalent to directly approximating   with a standard neural network.. |
| --- | Minor | Sentence exceeds complexity threshold, split for readability. |
| --- | Minor | SENTENCE (Line 707, 26 words, 5 clauses) |
| --- | Minor | Notably, the shallowest network   performs an order of magnitude worse, while excessively wide shallow networks (e.g.,  ) fail to converge effectively, as evidenced by the   loss. |
| --- | Minor | Notably. the shallowest network   performs an order of magnitude worse. while excessively wide shallow networks (e.g.. ) fail to converge effectively. as evidenced by the   loss.. |
| --- | Minor | Sentence exceeds complexity threshold, split for readability. |

## 决策信号

- **审稿推荐**: 小修
- **问题包**: 主要 0 / 中等 2 / 次要 0

## 修订路线图

### 优先级 2 --- 强烈建议

- [ ] Cross-section numeric consistency should be reconciled ([LLM]; introduction)
- [ ] Comparison protocol should make fairness assumptions explicit ([LLM]; method)
