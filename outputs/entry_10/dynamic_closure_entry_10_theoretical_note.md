# Dynamic Closure Notebook — Entry 10
## Transient-State Causality and Boundary Footprints

### Scientific status

Entry 10 tests the original Dynamic Closure hypothesis in a form that can be
distinguished from terminal-state occupancy.

The central question is:

> Can a closure sector disappear completely from the final transient
> population and still contribute causally to the selected closure?

The answer in the present theorem-compatible absorbing pathway model is yes.

The result is model-causal, not yet an empirical statement about nature.

---

# 1. Transient states and committed outcomes

For each candidate closure sector \(k\), introduce:

1. a transient search state \(T_k\);
2. an absorbing committed outcome \(A_k\).

The transient states communicate through local detailed-balance rates derived
from the Entry 09 closure defect,

\[
D_k=
\left|
\ln\frac{F_k}{k^2}
\right|.
\]

For nearest-neighbor sectors,

\[
W_{j\to k}
=
\nu A_{jk}
\exp
\left[
-\frac{\lambda}{2}
(D_k-D_j)
\right].
\]

Each transient state also has an irreversible commitment hazard

\[
h_k
=
h_0e^{-\lambda D_k}.
\]

The hazard law is a declared modeling assumption. It is not part of DCT.

---

# 2. Continuous-time absorbing generator

Let \(Q\) denote the transient generator and \(R\) the transient-to-absorbing
rate matrix.

For \(j\neq k\),

\[
Q_{jk}=W_{j\to k},
\]

while

\[
Q_{jj}
=
-\sum_{k\neq j}W_{j\to k}-h_j.
\]

The absorbing rate matrix is

\[
R=\operatorname{diag}(h_j).
\]

The row sums of the full generator vanish because

\[
Q\mathbf 1+R\mathbf 1=0.
\]

For the configured model every eigenvalue of \(Q\) has negative real part.
Therefore

\[
e^{Qt}\to0
\qquad
(t\to\infty),
\]

and hence

\[
\boxed{
p_{\rm transient}(t)\to0.
}
\]

The final transient occupancy is therefore exactly zero in the asymptotic
limit.

The finite-time numerical check at

\[
t=1000
\]

gave total remaining transient probability

\[
1.70\times10^{-18}.
\]

---

# 3. Fundamental matrix: zero terminal occupancy does not imply zero residence

For a transient continuous-time generator \(Q\), define

\[
\boxed{
N=(-Q)^{-1}.
}
\]

For an initial row distribution \(\mu\),

\[
\tau
=
\mu N
\]

is the vector of expected residence times in the transient sectors before
commitment.

The final absorption matrix is

\[
\boxed{
B=NR.
}
\]

Thus the final outcome probabilities are

\[
a=\mu B.
\]

This is the continuous-time analogue of the standard absorbing-chain
fundamental-matrix construction.

The Entry 10 run found:

\[
\boxed{
\tau_j>0
}
\]

for every one of the 35 transient sectors, despite

\[
p_j(\infty)=0
\]

for all 35.

Therefore

\[
\boxed{
p_j(\infty)=0
\not\Rightarrow
\tau_j=0.
}
\]

---

# 4. Integrated pathway flux

The expected number of transitions along edge \(j\to k\) before absorption is

\[
\boxed{
J_{jk}
=
\tau_j W_{j\to k}.
}
\]

Define node throughflow

\[
\Phi_j
=
\sum_kJ_{jk}
+
\sum_iJ_{ij}.
\]

A transient state can therefore have zero final occupancy while carrying
nonzero integrated pathway flux.

This distinguishes a terminal snapshot from the dynamical history.

---

# 5. Intervention-based pathway contribution

The default initial condition places probability only at the two outer
boundaries,

\[
k=2
\quad\text{and}\quad
k=36,
\]

with equal weight.

Every interior state therefore begins with zero initial probability.

For an interior non-target sector \(j\), apply a soft blockade by multiplying
every incident transition rate by

\[
\epsilon=0.05.
\]

The commitment hazard is left unchanged.

Define the intervention effect on the DCT target as

\[
\boxed{
\mathcal C_j
=
P_{\rm target}^{\rm base}
-
P_{\rm target}^{\rm block(j)}.
}
\]

The baseline target probability is

\[
P_{\rm target}^{\rm base}
=
P(A_{12})
\approx0.480253.
\]

Every one of the 32 interior non-target sectors produced

\[
\boxed{
\mathcal C_j>0.
}
\]

The strongest intervention effects were:

\[
k=13:
\quad
\mathcal C_{13}\approx0.126805,
\]

\[
k=10:
\quad
\mathcal C_{10}\approx0.114683,
\]

\[
k=14:
\quad
\mathcal C_{14}\approx0.107093,
\]

\[
k=11:
\quad
\mathcal C_{11}\approx0.106175.
\]

Thus states that have exactly zero asymptotic transient occupancy can still
alter the probability of reaching the final \(k=12\) closure.

Within this declared model,

\[
\boxed{
\text{terminal absence}
\neq
\text{causal irrelevance}.
}
\]

---

# 6. Boundary memory under exact state elimination

The stronger result comes from exact algebraic elimination.

Partition one transient state \(j\) from all retained transient states \(A\).

Write

\[
Q=
\begin{pmatrix}
Q_{AA} & Q_{Aj}\\
Q_{jA} & Q_{jj}
\end{pmatrix},
\]

and

\[
R=
\begin{pmatrix}
R_A\\
R_j
\end{pmatrix}.
\]

The absorption matrix satisfies

\[
QB+R=0.
\]

The eliminated-state row gives

\[
Q_{jA}B_A+Q_{jj}B_j+R_j=0,
\]

so

\[
B_j
=
-Q_{jj}^{-1}
\left(
Q_{jA}B_A+R_j
\right).
\]

Substitution into the retained equations yields

\[
\boxed{
Q_{\rm eff}
=
Q_{AA}
-
Q_{Aj}Q_{jj}^{-1}Q_{jA},
}
\]

and

\[
\boxed{
R_{\rm eff}
=
R_A
-
Q_{Aj}Q_{jj}^{-1}R_j.
}
\]

Therefore the eliminated state leaves the corrections

\[
\Delta Q
=
-Q_{Aj}Q_{jj}^{-1}Q_{jA},
\]

\[
\Delta R
=
-Q_{Aj}Q_{jj}^{-1}R_j.
\]

The state has disappeared from the explicit state vector, but its influence
has not disappeared. It has been transferred into effective couplings among
the retained boundary states and into effective absorption terms.

This is the precise mathematical sense in which a removed transient state can
survive as a boundary footprint.

---

# 7. Exact preservation of absorption statistics

Define

\[
B_{\rm eff}
=
(-Q_{\rm eff})^{-1}R_{\rm eff}.
\]

The Schur-complement derivation implies

\[
\boxed{
B_{\rm eff}=B_A.
}
\]

Thus all absorption probabilities from retained starting states are preserved
exactly after the eliminated state is integrated out, provided the induced
boundary terms are retained.

The numerical Entry 10 test eliminated each transient state independently.

The largest Frobenius residual in absorption-statistics preservation was

\[
7.83\times10^{-15},
\]

consistent with floating-point precision.

Every one of the 35 transient sectors had a nonzero Schur-complement boundary
footprint.

Therefore

\[
\boxed{
\text{state elimination}
\neq
\text{effect elimination}.
}
\]

Instead,

\[
\boxed{
\text{state elimination}
\rightarrow
\text{effective boundary renormalization}.
}
\]

---

# 8. Boundary-footprint measure

Define

\[
\mathcal B_j^{(Q)}
=
\|\Delta Q_j\|_F,
\]

\[
\mathcal B_j^{(R)}
=
\|\Delta R_j\|_F,
\]

and

\[
\boxed{
\mathcal B_j
=
\sqrt{
\left(\mathcal B_j^{(Q)}\right)^2
+
\left(\mathcal B_j^{(R)}\right)^2
}.
}
\]

All tested sectors satisfy

\[
\mathcal B_j>0.
\]

This gives a quantitative measure of how much effective reduced dynamics must
be added when a transient sector is removed.

The largest total footprint in the configured model occurs at

\[
k=12,
\]

with

\[
\mathcal B_{12}\approx1.28746.
\]

Several high-\(k\) sectors also have large generic transition footprints.

---

# 9. Two different forms of dynamical memory

The intervention measure

\[
\mathcal C_j
\]

and the Schur footprint

\[
\mathcal B_j
\]

do not measure the same thing.

The run found:

\[
\operatorname{corr}
(
\mathcal C_j,\tau_j
)
\approx0.812,
\]

and

\[
\operatorname{corr}
(
\mathcal C_j,\Phi_j
)
\approx0.819.
\]

Thus target-directed causal contribution is strongly associated with residence
and pathway flow.

However,

\[
\operatorname{corr}
(
\mathcal C_j,\mathcal B_j
)
\approx-0.824
\]

in the present parameterization.

This does not contradict the boundary-memory hypothesis.

It shows that:

- \(\mathcal C_j\) is **target-specific**: it measures influence on commitment
  to \(k=12\);
- \(\mathcal B_j\) is **global and target-independent**: it measures the total
  effective correction required to eliminate a state from the generator.

A sector can therefore be structurally important to the reduced dynamics
without being strongly aligned with the particular target outcome.

This distinction should be preserved in later robustness tests.

---

# 10. Transient Boundary Memory Proposition

## Proposition

Consider a finite continuous-time absorbing process with transient generator
\(Q\), absorbing-rate matrix \(R\), and \(Q\) Hurwitz.

Then:

1. transient probability satisfies

   \[
   p_T(t)\to0;
   \]

2. expected transient residence is

   \[
   \tau=\mu(-Q)^{-1},
   \]

   which can remain strictly positive;

3. eliminating a transient state \(j\) by Schur complement yields induced
   effective terms

   \[
   \Delta Q_j
   =
   -Q_{Aj}Q_{jj}^{-1}Q_{jA},
   \]

   \[
   \Delta R_j
   =
   -Q_{Aj}Q_{jj}^{-1}R_j;
   \]

4. retaining these induced terms preserves the absorption statistics exactly.

Therefore zero asymptotic occupancy of a transient state does not imply zero
dynamical contribution.

Instead, its influence can survive in integrated residence, pathway flux, and
effective reduced boundary conditions.

---

# 11. Relation to the user's boundary insight

The phrase "the zero final occupancy is not zero at all" can now be stated more
precisely:

\[
\boxed{
p_j(\infty)=0
}
\]

is only a statement about one terminal coordinate.

It says nothing by itself about

\[
\int_0^\infty p_j(t)\,dt,
\]

about integrated flux,

\[
\int_0^\infty p_j(t)W_{jk}\,dt,
\]

about intervention sensitivity,

\[
\mathcal C_j,
\]

or about the effective boundary terms created when \(j\) is eliminated,

\[
\Delta Q_j,\Delta R_j.
\]

Thus a state that is absent from the final explicit configuration can remain
encoded in the lowest-level effective boundary dynamics.

This is the mathematical form of the Dynamic Closure memory hypothesis.

---

# 12. Literature anchors

The fundamental-matrix interpretation of absorbing Markov chains is standard:
the fundamental matrix records expected visits/residence before absorption,
while multiplication by the transient-to-absorbing block gives absorption
probabilities.

State elimination through stochastic complementation and Schur-complement
reduction is also well established in Markov-chain and network-reduction
theory.

Kron reduction provides a broader graph-theoretic example of the same
structural principle: eliminating internal nodes generates effective couplings
among retained boundary nodes rather than simply deleting their influence.

These mathematical precedents support the reduction mechanism used here.
They do not establish EDF-specific physical reality; that remains an empirical
and foundational question.

---

# 13. Falsification gates

The Entry 10 model should be revised if:

1. EDF transition topology is not local in closure-sector space;
2. commitment is not well represented by absorbing outcomes;
3. the hazard law

   \[
   h_k=h_0e^{-\lambda D_k}
   \]

   is incompatible with a later microscopic EDF derivation;
4. memory is intrinsically non-Markovian and cannot be represented by a finite
   generator;
5. intervention results disappear under reasonable topology and parameter
   perturbations;
6. real systems show no measurable pathway dependence despite matching the
   static closure structure.

Failure of this stochastic pathway realization does not invalidate DCT.

---

# 14. Transition to robustness testing

Entry 10 establishes a proof-of-principle distinction:

\[
\boxed{
\text{terminal occupancy}
\neq
\text{dynamical memory}.
}
\]

The next task is to determine whether this distinction survives systematic
changes in:

\[
\lambda,
\quad
h_0,
\quad
\nu,
\quad
\text{initial conditions},
\quad
\text{graph topology},
\quad
\text{block strength},
\quad
\text{candidate range},
\]

and alternative commitment laws.

That is the appropriate subject of the robustness/falsification suite.

---

# References

1. J. G. Kemeny and J. L. Snell, *Finite Markov Chains*, Springer-Verlag, 1976.

2. E. Milliken, “Applications of the fundamental matrix to mean absorption and conditional mean absorption problems,” *Statistics & Probability Letters* **151**, 106–115 (2019). DOI: 10.1016/j.spl.2019.04.001.

3. C. D. Meyer, “Stochastic Complementation, Uncoupling Markov Chains, and the Theory of Nearly Reducible Systems,” *SIAM Review* **31**, 240–272 (1989). DOI: 10.1137/1031050.

4. F. Dörfler and F. Bullo, “Kron Reduction of Graphs with Applications to Electrical Networks,” *IEEE Transactions on Circuits and Systems I* **60**, 150–163 (2013); arXiv:1102.2950.

5. G. Falasco and M. Esposito, “Local detailed balance across scales: From diffusions to jump processes and beyond,” *Physical Review E* **103**, 042114 (2021). DOI: 10.1103/PhysRevE.103.042114.
