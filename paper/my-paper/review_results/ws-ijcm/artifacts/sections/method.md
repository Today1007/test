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