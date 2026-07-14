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