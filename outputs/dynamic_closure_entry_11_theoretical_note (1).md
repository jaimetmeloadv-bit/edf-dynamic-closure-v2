# Dynamic Closure Notebook — Entry 11
## Robustness and Falsification Suite

### 1. Purpose

Entry 11 does not introduce a new EDF mechanism.

It attempts to falsify the post-theorem transient-memory result of Entry 10 by
changing the stochastic realization over a broad parameter and model grid.

The central distinction is between two claims.

### Structural transient-memory claim

A transient state may satisfy

\[
p_j(t\to\infty)=0
\]

while still having

\[
\tau_j>0
\]

and while leaving a nonzero Schur-complement footprint after elimination.

### Strong target-specific claim

Every transient state positively contributes to the probability of reaching

\[
k=12.
\]

Entry 11 deliberately tests these separately.

The result is asymmetric:

\[
\boxed{
\text{structural transient memory is robust in the tested architecture,}
}
\]

but

\[
\boxed{
\text{universal positive contribution to }k=12\text{ is not robust.}
}
\]

This is a useful falsification result.

---

# 2. Stress-test design

The broad core sweep varies:

\[
\lambda\in\{0,0.5,1,2,4\},
\]

\[
h_0\in\{0.02,0.10,0.50\},
\]

three symmetric transition topologies:

\[
\text{path},\qquad
\text{ring},\qquad
\text{complete},
\]

two initial conditions:

\[
\text{boundary pair},\qquad
\text{left boundary},
\]

and three monotone DCT-compatible defect representations:

\[
D_k
=
\left|
\ln\frac{F_k}{k^2}
\right|,
\]

\[
B_k
=
\tanh(D_k/2),
\]

\[
S_k
=
2\sinh(D_k/2).
\]

For numerical comparability across representations, each defect family is
normalized by its mean nonzero value before applying the common
\(\lambda\)-grid.

The broad grid contains

\[
\boxed{270}
\]

independent model configurations.

A second targeted sweep tests three commitment laws:

\[
h_k=h_0e^{-\lambda D_k},
\]

\[
h_k=\frac{h_0}{1+\lambda D_k},
\]

and

\[
h_k=h_0e^{-\lambda D_k^2},
\]

for another

\[
\boxed{45}
\]

configurations.

A third test varies the intervention/blockade strength continuously.

---

# 3. Structural extinction

For each configuration the transient generator is

\[
Q_{jk}=W_{j\to k},
\qquad j\ne k,
\]

with

\[
Q_{jj}
=
-\sum_{k\ne j}W_{j\to k}-h_j.
\]

Every tested transient generator had

\[
\max\operatorname{Re}\sigma(Q)<0.
\]

Therefore every configuration satisfies

\[
\boxed{
p_T(t)\to0.
}
\]

The measured success fraction was

\[
\boxed{1.000}.
\]

Thus terminal transient extinction survived every tested combination of
selection strength, commitment rate, topology, initial condition, and defect
representation.

---

# 4. Integrated residence survives terminal extinction

The expected residence vector remains

\[
\tau
=
\mu(-Q)^{-1}.
\]

Across all 270 configurations, every transient state had

\[
\boxed{\tau_j>0}
\]

in floating-point arithmetic.

Therefore the strict positive-residence success fraction was

\[
\boxed{1.000}.
\]

In nine extreme configurations the smallest residence fell below the chosen
numerical reporting threshold

\[
10^{-10},
\]

although it remained strictly positive.

Those cases occur primarily for the rapidly growing symmetric defect

\[
S_k=2\sinh(D_k/2)
\]

at strong selection.

Thus the earlier apparent 0.967 success rate under a fixed numerical threshold
was not a mathematical loss of reachability; it reflected extremely small but
positive residence values.

This distinction is important:

\[
\boxed{
\text{numerically negligible}
\neq
\text{mathematically zero}.
}
\]

---

# 5. Schur boundary memory survives every test

For an eliminated transient state \(j\),

\[
Q_{\rm eff}
=
Q_{AA}
-
Q_{Aj}Q_{jj}^{-1}Q_{jA},
\]

and

\[
R_{\rm eff}
=
R_A
-
Q_{Aj}Q_{jj}^{-1}R_j.
\]

Define the total footprint

\[
\mathcal B_j
=
\sqrt{
\|\Delta Q_j\|_F^2
+
\|\Delta R_j\|_F^2
}.
\]

Across the complete 270-configuration robustness grid,

\[
\boxed{
\mathcal B_j>0
}
\]

for every eliminated state in every configuration.

The all-state nonzero-footprint success fraction is therefore

\[
\boxed{1.000}.
\]

This is the strongest result of Entry 11.

Within the declared connected absorbing-Markov architecture, eliminating a
coupled transient state consistently transfers its influence into effective
boundary terms.

Thus the Entry 10 statement

\[
\boxed{
\text{state elimination}
\neq
\text{effect elimination}
}
\]

survives the stress test.

---

# 6. Target-specific causality does not survive universally

For each cleanly probed non-target sector \(j\), the Entry 10 intervention
measure remains

\[
\mathcal C_j
=
P_{12}^{\rm base}
-
P_{12}^{\rm block(j)}.
\]

A positive value means the sector helps the target pathway.

A negative value means suppressing that sector increases the target
probability, so the sector acts as a competitor or diversion in that
configuration.

Across the 270 broad configurations:

\[
\text{median positive-causal fraction}
=
\boxed{0.576},
\]

while the minimum observed positive-causal fraction is

\[
\boxed{0}.
\]

Only about

\[
\boxed{5.6\%}
\]

of all configurations had positive intervention effect for every cleanly
probed non-target sector.

Therefore the strong claim

> every transient sector positively assists \(k=12\)

is falsified by the robustness suite.

This does **not** falsify transient memory.

It shows instead that a transient state can have a real dynamical footprint
while helping, hindering, or being nearly neutral with respect to one
particular absorbing target.

---

# 7. Topology is a major discriminator

The mean fraction of positively target-directed transient sectors was:

\[
\text{complete graph}:
\quad
0.291,
\]

\[
\text{path graph}:
\quad
0.598,
\]

\[
\text{ring graph}:
\quad
0.666.
\]

The complete graph is particularly revealing.

At weak selection, many non-target states act primarily as alternative
commitment channels. Blocking them can increase

\[
P(A_{12}),
\]

which produces

\[
\mathcal C_j<0.
\]

For example, at

\[
\lambda=0,\qquad
h_0=0.02,
\]

on the complete graph, every cleanly probed non-target state has a small
negative intervention effect.

Thus local pathway structure matters.

The Entry 10 result that all 32 cleanly probed sectors positively contributed
to \(k=12\) is therefore a property of that local-path regime, not a universal
consequence of DCT.

---

# 8. Local pathway models preserve the Entry 10 effect much more strongly

Although universal positive causality fails globally, the targeted
path/boundary model remains comparatively stable.

For the commitment-law sensitivity tests on the path graph with boundary-pair
initialization, the mean positive-causal fractions were approximately

\[
0.929
\]

for exponential commitment,

\[
0.929
\]

for quadratic-exponential commitment, and

\[
0.921
\]

for reciprocal commitment.

The minimum over those targeted sweeps was

\[
0.78125.
\]

Thus the local-pathway interpretation is not specific to one particular
commitment-hazard formula.

---

# 9. Defect representation sensitivity

Averaged across the broad grid, the positive-causal fractions were

\[
B_k:\quad0.546,
\]

\[
D_k:\quad0.547,
\]

\[
S_k:\quad0.461.
\]

The three defects have identical ordering, but they do not have identical
dynamical curvature after finite-\(\lambda\) weighting.

This is an important distinction.

Monotone equivalence guarantees the same ranking:

\[
D_i<D_j
\iff
B_i<B_j
\iff
S_i<S_j.
\]

It does not guarantee identical stochastic kinetics under

\[
e^{-\lambda D}.
\]

Therefore the precise off-closure defect parameterization remains part of the
post-theorem dynamical model and must not be promoted into DCT.

---

# 10. Initial-condition sensitivity

The boundary-pair initial condition produced mean positive-causal fraction

\[
0.632,
\]

whereas left-boundary initialization produced

\[
0.405.
\]

Thus the causal role of intermediate states depends substantially on where the
trajectory begins.

Again, this does not change the Schur-memory result.

It changes only the target-conditioned pathway interpretation.

---

# 11. Intervention-strength test

For the reference local-path model

\[
\lambda=2,
\qquad
h_0=0.10,
\]

the positive-causal fraction remained

\[
\boxed{1.0}
\]

across the entire tested blockade range.

As suppression was weakened, the mean absolute intervention effect decreased
smoothly:

\[
95\%\text{ suppression}:
\quad
0.0181,
\]

\[
50\%\text{ suppression}:
\quad
0.00269,
\]

\[
20\%\text{ suppression}:
\quad
0.000735.
\]

At complete blockade the mean effect rises to approximately

\[
0.0363.
\]

This is consistent with a genuine intervention response rather than a binary
artifact of one arbitrary blockade strength.

---

# 12. Weak and strong regimes

The weakest mean intervention effect in the broad grid occurred approximately
at

\[
\lambda=0,
\qquad
h_0=0.5,
\]

with ring topology and boundary-pair initialization.

Its mean absolute effect was only

\[
7.4\times10^{-5}.
\]

This is a useful limiting regime: rapid commitment combined with no structural
selection leaves little time for intermediate pathway influence to accumulate.

The strongest tested configuration occurred approximately at

\[
\lambda=4,
\qquad
h_0=0.5,
\]

with path topology, boundary-pair initialization, and the bounded defect.

Its mean absolute intervention effect reached

\[
0.0902.
\]

Therefore transient causal influence has a real regime structure rather than
being an invariant constant of the model.

---

# 13. Refined Dynamic Closure memory statement

Entry 11 suggests replacing an overly strong version of the hypothesis,

\[
\text{all transient states positively select the final closure},
\]

with a more precise statement:

\[
\boxed{
\begin{gathered}
p_j(\infty)=0
\\
\not\Rightarrow
\\
\text{dynamical irrelevance of }j.
\end{gathered}
}
\]

A vanished transient sector may retain influence through:

\[
\tau_j>0,
\]

integrated flux,

\[
\Phi_j>0,
\]

target-conditioned intervention effects of either sign,

\[
\mathcal C_j\ne0,
\]

and effective reduced boundary terms,

\[
\mathcal B_j>0.
\]

The sign of

\[
\mathcal C_j
\]

is pathway- and target-dependent.

The existence of

\[
\mathcal B_j
\]

is much more structurally robust.

This is a stronger scientific formulation because it survived an explicit
attempt at falsification.

---

# 14. Interpretation of the user's boundary insight

The phrase

> zero final occupancy may reflect its boundaries at the lowest level

now has a robust mathematical interpretation.

The final explicit transient coordinate can vanish:

\[
p_j(\infty)=0.
\]

If the state is then integrated out, the reduced dynamics acquires

\[
\Delta Q_j
=
-Q_{Aj}Q_{jj}^{-1}Q_{jA},
\]

and

\[
\Delta R_j
=
-Q_{Aj}Q_{jj}^{-1}R_j.
\]

Therefore the reduced theory need not contain the state explicitly in order to
retain information about the pathways that passed through it.

What survives is not terminal occupancy but an **effective dynamical
constraint on the retained boundary variables**.

This statement remained true throughout the tested robustness grid.

---

# 15. Falsification outcome

Entry 11 produces both a survival and a failure.

### Survived

Across every tested configuration:

\[
\boxed{
\text{transient extinction}
}
\]

and

\[
\boxed{
\text{nonzero Schur boundary memory}
}
\]

coexisted.

Strictly positive residence also survived all configurations.

### Failed

The proposition

\[
\boxed{
\mathcal C_j>0
\quad
\text{for every non-target transient state}
}
\]

does not survive changes in topology, initial conditions, and selection
regime.

This is exactly the kind of result the falsification suite was designed to
detect.

---

# 16. Relation to sensitivity-analysis methodology

The Entry 11 sweep is a structured multi-factor stress test, not yet a full
variance-based global sensitivity analysis.

Established sensitivity-analysis literature distinguishes local or
one-factor-at-a-time perturbations from global methods that explore parameter
space and interactions. Global sensitivity methods are especially useful for
nonlinear models where interactions can materially change conclusions.

A later repository-polishing stage could add formal Morris screening or Sobol
indices if quantitative parameter-importance ranking becomes necessary.

For the present purpose, Entry 11 has already answered the first-order
scientific question:

> Which qualitative claims survive broad model perturbation?

---

# 17. Next step

The appropriate next entry is not another parameter sweep.

Entry 12 should return to the structural alternatives

\[
k^2-1,
\qquad
k(k-1),
\qquad
\frac{k(k+1)}2,
\qquad
\frac{k(k-1)}2,
\]

and evaluate them against the completed DCT premise chain.

The objective is no longer merely to show that alternative counts select
different Fibonacci matches.

The objective is to identify precisely:

\[
\boxed{
\text{which DCT premise each alternative violates or changes.}
}
\]

That will complete the main structural control suite before physical
correspondence begins.

---

# References

1. A. Saltelli, M. Ratto, S. Tarantola, and F. Campolongo, “Sensitivity analysis practices: Strategies for model-based inference,” *Reliability Engineering & System Safety* **91**, 1109–1125 (2006). DOI: 10.1016/j.ress.2005.11.014.

2. F. Pianosi et al., “Sensitivity analysis of environmental models: A systematic review with practical workflow,” *Environmental Modelling & Software* **79**, 214–232 (2016). DOI: 10.1016/j.envsoft.2016.02.008.

3. B. Iooss and P. Lemaître, “A review on global sensitivity analysis methods,” in *Uncertainty Management in Simulation-Optimization of Complex Systems* (2015); arXiv:1404.2405.

4. C. D. Meyer, “Stochastic Complementation, Uncoupling Markov Chains, and the Theory of Nearly Reducible Systems,” *SIAM Review* **31**, 240–272 (1989). DOI: 10.1137/1031050.

5. F. Dörfler and F. Bullo, “Kron Reduction of Graphs with Applications to Electrical Networks,” *IEEE Transactions on Circuits and Systems I* **60**, 150–163 (2013); arXiv:1102.2950.
