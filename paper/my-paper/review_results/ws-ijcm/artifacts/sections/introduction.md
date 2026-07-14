## Introduction
sec:intro
Hydraulic fracturing is a crucial technology for enhancing
hydrocarbon recovery from unconventional reservoirs
Economides2000. Accurate prediction of fracture geometry ---
the spatial and temporal evolution of fracture width, length, and net
pressure --- is essential for optimizing treatment design and evaluating
well performance. Perkins and Kern and Nordgren first proposed the PKN
model to describe the evolution of fracture length and width during
hydraulic fracturing Nordgren1972. This classical model, together
with the KGD model Ref_KGD, established the theoretical basis for
the simulation of hydraulic fracturing. Among these models, the PKN
model remains one of the most widely adopted in industrial practice due
to its computational tractability. The PKN model assumes a fracture of
fixed height that is much larger than its vertical extent, with
plane-strain deformation in each cross-section. Under this assumption,
the local elasticity relation yields a nonlinear governing equation that
balances the temporal evolution of fracture width, the fluid leak-off
into the surrounding formation, and the longitudinal gradient of the
volumetric flow rate governed by the fluid's viscous resistance. Despite
its apparent simplicity, this equation poses significant computational
challenges due to its strong nonlinearity, moving free boundary, and
singular behavior at the propagating tip.
The numerical solution of the PKN model has been an active research
topic since Nordgren's original finite-difference formulation
Nordgren1972. Traditional grid-based approaches include explicit
finite-difference schemes Kemp1990, finite element methods with
tip enrichment Garikapati2017, and spectral discretizations
Peirce2014. However, these methods face persistent difficulties.
The fracture tip exhibits a singular gradient that tends to infinity,
requiring special tip elements, regularization techniques
Linkov2011, or asymptotic enrichment functions
Garikapati2017 to avoid severe accuracy degradation. The
classical PKN tip asymptote follows a one-third power-law in the
viscosity-dominated regime Nordgren1972,Kemp1990, but a more
complex transient behavior --- smoothly transitioning from a one-third
to a three-eighths power-law depending on the local leak-off intensity
--- has been recognized in recent re-examinations
Linkov2015,Detournay2016. Furthermore, the moving free boundary
evolves nonlinearly with time, following different power-law regimes
depending on whether the propagation is dominated by fluid storage or
leak-off. Accurately tracking this evolving crack front typically
requires adaptive remeshing or front-tracking algorithms
Peirce2014, which introduce significant computational overhead.
Additionally, a multi-scale structure arises from the thin boundary
layer near the tip to the global fracture scale, demanding dense local
grids that can make parametric studies and real-time applications
prohibitive Detournay2016.
Physics-Informed Neural Networks (PINNs) were introduced by Raissi
et al. Raissi2019 as a mesh-free framework that embeds
the governing partial differential equations directly into the loss
function of a neural network. PINNs exploit automatic differentiation
for exact derivative computation and can naturally incorporate sparse
observational data. Since their introduction, PINNs and their variants
--- including domain-decomposition extensions such as XPINN
Jagtap2020 and cPINN Jagtap2020b, gradient-enhanced
formulations Yu2022, and multi-scale architectures
Moseley2023 --- have been successfully applied across a broad
spectrum of problems in computational mechanics. Recently, PINNs have
been applied to the field of subsurface engineering, including flow and
transport in porous media Hassan2024, history-matching in
fractured reservoirs Ali2025, and two-phase flow in heterogeneous
formations Wang2024. However, the application of PINNs to
hydraulic fracture propagation --- characterized by its unique
combination of a moving free boundary, singular tip asymptotics, and
multi-regime transient behavior --- remains relatively unexplored.
A small number of recent studies have begun to bridge PINNs with
hydraulic fracture modeling. Yang2023 developed a
physics-informed surrogate model for predicting hydraulic fracture
geometry using deep learning, demonstrating the feasibility of replacing
computationally expensive simulators with trained neural networks.
Tang2024 proposed a PINN formulation with moving boundary
constraints for modeling hydraulic fracturing, making an important step
toward handling the free-boundary nature of the problem. However,
existing PINN-based approaches for hydraulic fracturing still face
critical limitations. First, most existing PINN formulations for
fracture problems do not explicitly encode the asymptotic tip behavior
into the network architecture. Without such prior knowledge, the network
must learn sharp near-tip gradients purely from PDE residuals, which is
notoriously difficult for gradient-based optimization
Krishnapriyan2021. The transient transition between the
one-third and three-eighths power-law tip asymptotics has not been
addressed in any existing PINN work. Second, the PKN governing equation
is physically valid only in the region where the fracture has already
arrived. Existing PINN formulations do not enforce this causal
constraint, leading to non-physical residuals being minimized in regions
not yet reached by the fracture front. Third, the early-time behavior
of fracture width exhibits a power-law singularity whose exponent
depends on the dominant physical regime. Learning this temporal scaling
directly from data is inefficient and limits generalization to time
ranges not covered during training.
To address these challenges, this paper proposes PE-PINN
(Physics-Enhanced PINN), a novel framework for the PKN model that
explicitly embeds physical prior knowledge into the network architecture.
The proposed method decomposes the fracture width into three physically
meaningful components: a learnable time-power term that captures the
early-time singular scaling, an analytically derived transient tip shape
function that smoothly interpolates between the one-third and
three-eighths asymptotic regimes, and a neural network that learns the
remaining smooth component. This physics-enhanced representation
explicitly separates the singular time and space dependencies, allowing
the network to learn only a well-behaved residual function. Building on
this decomposition, the arrival time of the crack tip at each spatial
location is computed by numerically inverting the crack-length evolution
relation, and the PDE residual evaluation is restricted to the physically
meaningful region where the fracture has already arrived. This causal
masking ensures
physical consistency. Additionally, the time-power exponent is
constrained to a physically plausible range and optimized jointly with
the network parameters, automatically discovering the correct temporal
scaling. A two-stage training strategy combining Adam Kingma2015
for global exploration with L-BFGS Liu1989 for fine local
convergence is employed. In contrast to existing PINN formulations for
hydraulic fracturing Yang2023,Tang2024, the proposed method
encodes the asymptotic tip structure analytically rather than relying on
the optimizer to discover it, which significantly reduces the learning
burden on the network. Numerical experiments demonstrate that the
proposed method achieves competitive accuracy against conventional
finite difference solutions while maintaining a mesh-free formulation.
Systematic ablation studies and sensitivity analyses further confirm
that each component of the proposed framework contributes measurably to
overall accuracy.
The remainder of this paper is organized as follows. Section~2 formulates
the PKN governing equations. Section~3 describes the proposed PE-PINN
framework, including the network design, loss function, training
strategy, and experimental configuration. Section~4 presents the
numerical results. Section~5 concludes the paper.