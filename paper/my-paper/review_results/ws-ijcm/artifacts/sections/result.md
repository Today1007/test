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