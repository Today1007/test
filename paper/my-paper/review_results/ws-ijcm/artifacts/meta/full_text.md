cas-sc
natbib
algorithm
algpseudocode
xcolor
caption
float
hyperref
colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue
#1#1#1
WGM
QE
document
1
.001
PE-PINN for PKN Hydraulic Fracture Modeling
[Authors]
 [mode = title]PE-PINN: A Physics-Enhanced Physics-Informed Neural Network \\
for Solving the PKN Model of Hydraulic Fracturing
[1]
For the title, try not to use more than 3 lines.
[Author 1]
[1]
[1]
[email]
Conceptualization, Methodology, Software, Writing
organization=[Department, University],
 city=[City],
 country=[Country]
[Author 2]
[2]
[email]
Validation, Writing - Review \& Editing
organization=[Department, University],
 city=[City],
 country=[Country]
Corresponding author
Typeset names in 8~pt Roman.
State completely without abbreviations.
abstract
This paper presents PE-PINN, a Physics-Enhanced Physics-Informed Neural
Network framework for solving the PKN model of hydraulic fracturing.
The governing Nordgren equation is solved by embedding physical priors
directly into the network architecture, including a transient tip shape
function that analytically interpolates asymptotic regimes, a causal
arrival-time constraint, and a learnable time-power exponent. Numerical
experiments demonstrate competitive accuracy against finite difference
solutions while maintaining a mesh-free formulation.
abstract
highlights
 A physics-enhanced PINN framework (PE-PINN) is proposed for the PKN model of hydraulic fracturing.
 A transient tip shape function analytically encodes the transition between asymptotic crack-tip regimes.
 A causal arrival-time constraint restricts PDE residual evaluation to the physically valid region.
 A learnable time-power exponent automatically discovers the correct temporal scaling behavior.
highlights
keywords
Physics-informed neural network PKN model hydraulic fracturing 
Nordgren equation moving boundary tip singularity
keywords
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
## Problem Formulation
sec:problem
Consider a vertical hydraulic fracture of constant height 
propagating within a homogeneous, isotropic, and linear elastic
reservoir. A Newtonian fracturing fluid is injected at a constant
volumetric rate at the wellbore, driving the fracture to extend
perpendicular to the minimum in-situ stress. The following assumptions
are adopted Nordgren1972,Detournay2016: (i) the fracture length
 is much larger than its height (), and the height is
much larger than the maximum opening (), so that plane-strain
deformation prevails in each vertical cross-section; (ii) the fluid
flow within the narrow fracture channel is laminar and governed by
lubrication theory; (iii) fluid leak-off from the fracture faces into
the surrounding permeable formation follows Carter's one-dimensional
leak-off law, under which the leak-off velocity at a given location
decays inversely with the square root of the elapsed time since the
fracture tip first reached that location.
Under plane-strain conditions, the net pressure --- the
difference between the fluid pressure inside the fracture and the
far-field confining stress --- is linearly proportional to the local
maximum fracture opening . For a fracture of elliptical
vertical cross-section, this relation takes the form
Nordgren1972
where is the plane-strain Young's modulus, is
the Young's modulus, and is the Poisson's ratio. The volumetric
flow rate within the fracture is governed by Poiseuille flow
in a narrow elliptical conduit. Exploiting , the flow rate
relates to the longitudinal gradient of as
Nordgren1972,Kemp1990
where is the dynamic viscosity of the fracturing fluid.
Local mass conservation balances the temporal change in the elliptical
cross-sectional area , the longitudinal flux gradient,
and the fluid volume lost to the formation through both fracture faces:
where is the Carter leak-off coefficient and is the
arrival time --- the instant at which the propagating fracture tip first
reaches the spatial coordinate .
Substituting Eqs.~eq:flow and~eq:elasticity into
Eq.~eq:continuity yields the Nordgren equation, a nonlinear
diffusion-type PDE governing the spatiotemporal evolution of the
fracture width:
The initial and boundary conditions are
where the inlet condition follows from . The arrival
time is defined implicitly by , ensuring that
the leak-off term in Eq.~eq:nordgren is evaluated only after
the fracture has reached a given location.
To expose the self-similar structure of the problem and eliminate
dimensional parameters, characteristic scales , , and 
are introduced such that the dimensionless diffusion and leak-off
coefficients equal unity and the dimensionless inlet flux equals one.
Defining
Eq.~eq:nordgren reduces to the compact dimensionless form
Kemp1990,Detournay2016
with the normalized boundary condition
where . Hereafter, the bars on
dimensionless quantities are omitted for brevity; all symbols
 denote the dimensionless variables unless
otherwise stated.
The fracture length follows distinct power-law regimes depending
on the dominant physical mechanism. In the storage-dominated regime,
where most of the injected fluid remains within the fracture, the tip
propagation obeys . In the leak-off-dominated
regime, where fluid loss governs the volume balance, the propagation
slows to Nordgren1972,Kemp1990. Between
these two limits, the length evolution is well approximated by a
harmonic mean interpolation of the asymptotic solutions
Detournay2016:
where and are dimensionless constants determined
by the self-similar solutions of the two limiting regimes.
A defining feature of the PKN model is the singular near-tip structure
of the fracture width. As from below, the width vanishes
but its longitudinal gradient becomes unbounded. Defining the
dimensionless distance from the tip as , the
near-tip width follows a one-third power law ()
in the storage-dominated regime and a three-eighths power law
() in the leak-off-dominated regime
Linkov2015,Detournay2016. In the general transient case, where
both fluid storage and leak-off contribute, the tip shape transitions
smoothly between the two limiting asymptotes. An analytical expression
capturing this transition was derived by Linkov2015:
where is a smooth modulation function satisfying
 as (recovering the classical one-third
behavior at the very tip) and at larger
 (yielding the three-eighths behavior farther from the tip).
In summary, Eqs.~eq:nordgren-dim,~eq:ic,
eq:bc-dim,~eq:length, and~eq:tipshape form a
fully coupled system that governs the spatiotemporal evolution of the
fracture width. This system constitutes the forward problem that the
PE-PINN framework developed in Section~sec:method is designed
to solve.
## Methodology
sec:method
This section presents the proposed PE-PINN framework for solving
the PKN model of hydraulic fracture propagation. The framework
design, loss function, training strategy, and experimental
configuration are detailed in the following subsections.
### PE-PINN design
sec:design
The PKN model poses three fundamental challenges for conventional
PINNs: the singular near-tip gradient, the moving free boundary, and
the power-law temporal scaling at early times. To address these
challenges, this paper proposes a physics-enhanced representation
that embeds prior physical knowledge directly into the network
architecture. Rather than directly approximating the fracture width
 with a generic neural network, the proposed method
decomposes the solution into three physically meaningful components:
where is a time-power factor that captures the
early-time singular scaling, is the
transient tip shape function defined in
Eq.~eq:tipshape that analytically encodes the transition
between the one-third and three-eighths asymptotic regimes, and
 is a neural network that learns the
remaining smooth component. This decomposition explicitly separates
the singular temporal and spatial dependencies, allowing the network
to learn only a well-behaved residual function.
center
figs/network-architecture.pdf
figureSchematic of the PE-PINN architecture. The network input
consists of the dimensionless spatial and temporal coordinates
. The output is a positive scalar field combined with the
time-power factor and the transient tip shape function
 to produce the fracture width
. The PDE residual and boundary condition are
embedded in the loss function, and the network is trained using a
two-stage Adam + L-BFGS strategy.fig:architecture
center
Figure~fig:architecture shows the proposed architecture, which
integrates a fully connected neural network with the
physics-enhanced ansatz and physical constraints. The neural network
component maps the spatial and temporal
coordinates to a positive scalar output
through four hidden layers, each containing 128 neurons with the
hyperbolic tangent (Tanh) activation function. The output layer
contains a single neuron followed by a Softplus activation
() to ensure strict
positivity of the predicted width. The network weights are
initialized using the Xavier normal scheme and the biases are
initialized to zero. The time-power factor and the transient tip
shape function are then multiplied with the network output to
produce the final prediction , as defined in
Eq.~eq:ansatz.
The transient tip shape function provides
an analytical description of the near-tip width profile that smoothly
interpolates between the one-third power-law in the
storage-dominated regime and the three-eighths power-law in the
leak-off-dominated regime. By encoding this asymptotic structure
explicitly, the network is relieved from learning the sharp near-tip
gradient, which is a well-documented failure mode of conventional
PINNs Krishnapriyan2021.
A further physical constraint is imposed through the arrival time
. The Nordgren equation eq:nordgren-dim is
physically valid only in the region where the fracture has already
arrived, i.e., where and . Evaluating the
PDE residual outside this region introduces non-physical penalties
that can distort the learned solution. To enforce this causal
constraint, the arrival time at each spatial coordinate is computed
by numerically inverting the crack-length evolution
Eq.~eq:length using Brent's root-finding method:
which is solved separately for each collocation point prior to
training. During training, the PDE residual is evaluated only at
points satisfying the validity condition .
The exponent in Eq.~eq:ansatz is treated as a
trainable parameter initialized at and constrained
to the physically plausible range via hard clipping
after each gradient update. This parameter is optimized jointly with
the network weights, allowing the model to automatically discover
the correct temporal scaling behavior. In the storage-dominated
regime, the expected value is , while deviations
from this value indicate a transition toward leak-off-dominated
propagation. The converged value of thus provides
interpretable physical insight into the dominant flow regime.
### Loss function and training
sec:training
The network parameters and the time-power exponent
 are optimized by minimizing a physics-informed loss
function that enforces the governing PDE and boundary conditions
without requiring labeled training data. The training of the
network is realized by minimizing a loss function that combines
the PDE residual and the boundary condition constraint.
The PDE residual is defined by the dimensionless Nordgren equation
eq:nordgren-dim:
where all derivatives are computed exactly via automatic
differentiation. The PDE loss is computed only over the causally
valid region :
The inlet boundary condition eq:bc-dim requires
 at .
However, at the spacetime origin , the initial condition
 and the boundary condition are incompatible. To
reconcile this conflict, a smooth temporal ramp function
 with is introduced,
which gradually activates the boundary condition as increases.
The boundary condition loss is formulated as
The total loss is the sum of the two contributions:
Collocation points are generated using Latin Hypercube Sampling
(LHS) to ensure uniform coverage of the spatiotemporal domain. The
sampling strategy employs a three-tier scheme: 10,000 points in the
early-time region (), 20,000 points in the late-time
region (), and 10,000 points in the near-tip
refinement zone () to resolve the sharp
spatial gradients. The spatial coordinates are mapped to the
physical domain via , ensuring that
the collocation points adapt to the evolving fracture length. For
the boundary condition loss, 2,000 points are sampled at 
with time values drawn from via LHS. The arrival
time is precomputed for all PDE collocation points using
Eq.~eq:tau-inversion prior to training, and the validity
mask is applied at each loss evaluation.
Training proceeds in two stages to combine the global exploration
capability of first-order stochastic methods with the fast local
convergence of second-order quasi-Newton methods. In the first
stage, the Adam optimizer Kingma2015 is employed for 5,000
epochs with an initial learning rate of and exponential
decay with factor per epoch. Gradient clipping
with a maximum norm of is applied to ensure training
stability. In the second stage, the L-BFGS optimizer Liu1989
with strong Wolfe line search is applied for up to 10,000 epochs,
starting from the Adam-converged parameters. The L-BFGS optimizer
uses a learning rate of , a history size of 100, and
convergence tolerances of (gradient) and 
(parameter change). Early stopping is triggered when the loss
stagnates for 200 consecutive L-BFGS iterations with a tolerance
of .
### Experimental configuration
sec:expt
The physical parameters adopted in the numerical experiments are
summarized in Table~tab:params. All computations are
performed in dimensionless form using the scaling introduced in
Section~sec:problem, and results are converted back to
physical units for comparison.
A finite difference (FD) solver is implemented as the reference
baseline for evaluating the accuracy of the proposed method. The FD
scheme employs a uniform spatial grid with explicit time stepping
and a velocity-based tip propagation condition, following the
classical formulation of Nordgren1972. The same physical
parameters and dimensionless scaling are used for both the FD solver
and the PE-PINN framework to ensure a consistent comparison.
To isolate the contribution of each component of the proposed
framework, four model variants are constructed: (i) the full
PE-PINN incorporating all three enhancements; (ii) a variant
without the time-power factor, i.e., in
Eq.~eq:ansatz; (iii) a variant without the transient tip
shape function, i.e., ; and
(iv) a plain PINN without any of the proposed components, equivalent
to directly approximating with a standard neural network.
All variants share the same network architecture, collocation
points, and training protocol, differing only in the presence or
absence of the physics-enhanced components.
A systematic sensitivity analysis is conducted to characterize the
influence of network depth and width on prediction accuracy.
The number of hidden layers is varied over 
and the number of neurons per hidden layer over
, yielding 25 configurations. For
each configuration, the full training protocol described in
Section~sec:training is executed, and the final L-BFGS loss
and training time are recorded. The optimal configuration is
selected to balance accuracy and computational cost.
## Results and Discussion
sec:results
### Model validation
sec:validation
The proposed method is evaluated against the finite difference
baseline. Fracture width profiles at representative times and the
crack length evolution are compared.
### Ablation study
sec:ablation
The ablation study quantifies the individual contribution of each
component of the proposed framework.
### Sensitivity analysis
sec:sensitivity
The sensitivity analysis characterizes the influence of network depth
 and width on prediction accuracy. Table~tab:sensitivity
reports the final L-BFGS loss for 25 configurations spanning
 and .
The results reveal a clear trend: increasing depth and width generally
improves accuracy, but with diminishing returns beyond and .
The optimal configuration is , with a final loss of
, achieving near-optimal accuracy (within
 of the global best , ) with only 
parameters. Notably, the shallowest network performs an
order of magnitude worse, while excessively wide shallow networks
(e.g., ) fail to converge effectively, as evidenced by
the loss. Deeper networks exhibit
greater robustness, with all configurations achieving losses within a
factor of two of the optimum.
Table~tab:sensitivity-time reports the corresponding training
times. The computational cost grows roughly linearly with the number
of parameters, with the shallowest network completing in
~s and the largest requiring ~s. The optimal
, configuration trains in ~s, representing a practical
balance between accuracy and computational efficiency. The converged
values of the learnable time-power exponent consistently fall
within the physically plausible range of , confirming
that the viscosity-dominated regime () is correctly
identified across all configurations.
## Conclusion
sec:conclusion
This paper presented PE-PINN, a Physics-Enhanced PINN framework for the PKN
model of hydraulic fracture propagation. The proposed method addresses
three fundamental challenges of applying PINNs to moving boundary
problems: the transient tip shape function analytically encodes the
transition between asymptotic regimes, the causal arrival-time
constraint restricts the PDE residual to the physically valid region,
and the learnable time-power exponent adaptively captures the temporal
scaling behavior. Numerical experiments demonstrate competitive
accuracy against a conventional finite difference solver while
maintaining a mesh-free formulation. Future work will extend the
framework to more complex fracture propagation scenarios.
## Acknowledgments
This work was supported by [FUNDING INFORMATION TO BE ADDED].
cas-model2-names
ws-ijcm
document