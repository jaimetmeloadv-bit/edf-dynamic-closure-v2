# Dynamic Closure Notebook — Entry 09
## Closure Defect and Theorem-Compatible Selection Functional

### Scientific status

Entry 09 begins the post-theorem phase.

The Dynamic Closure Theorem fixes the exact structural condition

\[
F_k=C(k)=k^2.
\]

Therefore any admissible closure-defect functional must satisfy

\[
D_k\ge0,
\qquad
D_k=0
\iff
F_k=k^2.
\]

The theorem fixes the exact zero set. It does **not** uniquely determine how
nonzero structural mismatch should be converted into a dynamical selection
penalty.

Entry 09 therefore separates:

1. the theorem-compatible structural defect;
2. the maximum-entropy inference law;
3. the detailed-balance jump-process embedding;
4. the still-undetermined microscopic EDF coupling strength.

No premise of DCT is modified.

---

# 1. Exact structural mismatch

From DCT,

\[
C(k)=k^2.
\]

Define the signed integer mismatch

\[
\Delta_k
=
F_k-k^2.
\]

Then

\[
\Delta_k=0
\iff
F_k=k^2.
\]

The signed quantity identifies whether Fibonacci count lies above or below the
operator closure capacity, but its magnitude grows with the scale of the
numbers. A dimensionless structural mismatch is therefore preferable for
cross-\(k\) comparison.

---

# 2. Canonical multiplicative defect

For \(k\ge2\), both \(F_k\) and \(k^2\) are positive.

Define the ratio

\[
\rho_k
=
\frac{F_k}{k^2}.
\]

The canonical log-ratio defect is

\[
\boxed{
D_k
=
\left|
\ln \rho_k
\right|
=
\left|
\ln\frac{F_k}{k^2}
\right|.
}
\]

This choice has several useful properties:

\[
D_k\ge0,
\]

\[
D_k=0
\iff
F_k=k^2,
\]

and exchanging the two positive structural counts leaves the defect unchanged:

\[
D(F,C)
=
D(C,F).
\]

Multiplicative mismatch is additive in logarithmic coordinates. Thus the
defect measures distance from exact closure in the positive ratio coordinate.

The important theorem-level property is only the zero condition. The logarithmic
form is a natural dimensionless representation, not an additional DCT theorem.

---

# 3. Recovery of the earlier bounded residual

The earlier exploratory notebook used

\[
B_k
=
\frac{|F_k-k^2|}{F_k+k^2}.
\]

Let

\[
x=\frac{F_k}{k^2}>0.
\]

Then

\[
B_k
=
\frac{|x-1|}{x+1}.
\]

Writing

\[
x=e^{\pm D_k},
\]

gives

\[
\boxed{
B_k
=
\tanh\left(\frac{D_k}{2}\right).
}
\]

Therefore the earlier bounded residual is not an unrelated fitted score. It is
a bounded monotone representation of the log-ratio defect.

A second symmetric representation is

\[
S_k
=
\frac{|F_k-k^2|}{\sqrt{F_k k^2}},
\]

which satisfies

\[
\boxed{
S_k
=
2\sinh\left(\frac{D_k}{2}\right).
}
\]

Since both \(\tanh(D/2)\) and \(2\sinh(D/2)\) are strictly increasing for
\(D\ge0\), all three defects produce exactly the same sector ordering:

\[
D_i<D_j
\iff
B_i<B_j
\iff
S_i<S_j.
\]

For the configured range \(2\le k\le36\), the unique zero remains

\[
\boxed{k=12}.
\]

---

# 4. What DCT does and does not determine

DCT determines

\[
D_{12}=0,
\]

and

\[
D_k>0
\qquad
(k\ne12).
\]

However, DCT alone does not determine a probability law over imperfect
closures.

In particular, the theorem does not determine a physical temperature, an
energy scale, a rate constant, or a coupling strength.

Those quantities belong to the dynamical layer.

The selection law must therefore be introduced transparently.

---

# 5. Maximum-entropy selection family

Consider a finite candidate set

\[
\mathcal K.
\]

Let

\[
p_k\ge0,
\qquad
\sum_{k\in\mathcal K}p_k=1.
\]

Assume a uniform prior over candidate sectors and constrain only the ensemble
mean defect

\[
\sum_k p_kD_k
=
\bar D.
\]

Maximize Shannon entropy

\[
H[p]
=
-\sum_k p_k\ln p_k.
\]

Using Lagrange multipliers for normalization and mean defect gives

\[
\delta
\left[
-\sum_k p_k\ln p_k
-\alpha\left(\sum_kp_k-1\right)
-\lambda\left(\sum_kp_kD_k-\bar D\right)
\right]
=
0.
\]

Therefore

\[
\ln p_k
=
-1-\alpha-\lambda D_k,
\]

so

\[
\boxed{
\pi_k(\lambda)
=
\frac{e^{-\lambda D_k}}
{Z(\lambda)},
}
\]

where

\[
Z(\lambda)
=
\sum_j e^{-\lambda D_j}.
\]

This is the least-committal exponential family subject to the declared
constraint.

The use of maximum entropy as a constructive inference principle goes back to
Jaynes' statistical-mechanical formulation.

The parameter

\[
\lambda\ge0
\]

is a dimensionless selection-strength parameter.

It is not identified with inverse temperature unless a later microscopic EDF
derivation supplies that physical meaning.

---

# 6. Exact properties of the MaxEnt family

Define

\[
\langle D\rangle_\lambda
=
\sum_k
\pi_k(\lambda)D_k.
\]

The partition function satisfies

\[
\frac{d\ln Z}{d\lambda}
=
-\langle D\rangle_\lambda.
\]

Differentiating again,

\[
\frac{d^2\ln Z}{d\lambda^2}
=
\operatorname{Var}_\lambda(D).
\]

Hence

\[
\boxed{
\frac{d\langle D\rangle_\lambda}{d\lambda}
=
-\operatorname{Var}_\lambda(D)
\le0.
}
\]

Thus increasing selection strength cannot increase the mean closure defect.

The entropy is

\[
H(\lambda)
=
\ln Z(\lambda)
+
\lambda\langle D\rangle_\lambda.
\]

Therefore

\[
\boxed{
\frac{dH}{d\lambda}
=
-\lambda
\operatorname{Var}_\lambda(D)
\le0
\qquad
(\lambda\ge0).
}
\]

So stronger defect resolution decreases selection entropy.

For the exact closure sector \(k_*=12\),

\[
D_{k_*}=0.
\]

Then

\[
\frac{d\ln\pi_{k_*}}{d\lambda}
=
\langle D\rangle_\lambda-D_{k_*}
=
\langle D\rangle_\lambda.
\]

Therefore

\[
\boxed{
\frac{d\ln\pi_{12}}{d\lambda}
=
\langle D\rangle_\lambda
>0
}
\]

until the distribution has fully concentrated.

Because \(k=12\) is the unique zero-defect sector,

\[
\boxed{
\lim_{\lambda\rightarrow\infty}
\pi_{12}(\lambda)
=
1.
}
\]

At

\[
\lambda=0,
\]

the distribution is uniform.

Thus the direction of selection is mathematically fixed once the defect family
is chosen.

---

# 7. Numerical selection certificate

For the candidate range

\[
2\le k\le36,
\]

there are \(35\) sectors.

At

\[
\lambda=0,
\]

\[
\pi_k
=
\frac1{35}
\approx0.0285714.
\]

The Entry 09 run gives:

| \(\lambda\) | \(\pi_{12}\) | Gain over uniform |
|---:|---:|---:|
| 0.00 | 0.028571 | 1.000 |
| 0.25 | 0.056268 | 1.969 |
| 0.50 | 0.085265 | 2.984 |
| 1.00 | 0.146431 | 5.125 |
| 2.00 | 0.286017 | 10.011 |
| 4.00 | 0.550155 | 19.255 |
| 8.00 | 0.849254 | 29.724 |

Across this grid:

\[
\pi_{12}
\]

is monotone increasing,

\[
\langle D\rangle
\]

is monotone decreasing, and

\[
H
\]

is monotone decreasing.

These numerical results match the exact derivative identities above.

---

# 8. Detailed-balance jump-process embedding

The MaxEnt distribution can be embedded in a continuous-time Markov jump
process.

Let

\[
A_{jk}=A_{kj}\ge0
\]

be a symmetric connected adjacency matrix describing which closure sectors are
kinetically connected.

Define

\[
\boxed{
W_{j\rightarrow k}
=
\nu
A_{jk}
\exp
\left[
-\frac{\lambda}{2}
(D_k-D_j)
\right],
}
\]

where

\[
\nu>0
\]

is an attempt-frequency scale.

Then

\[
\frac{W_{j\rightarrow k}}
{W_{k\rightarrow j}}
=
e^{-\lambda(D_k-D_j)}.
\]

But

\[
\frac{\pi_k}{\pi_j}
=
e^{-\lambda(D_k-D_j)}.
\]

Therefore

\[
\boxed{
\pi_jW_{j\rightarrow k}
=
\pi_kW_{k\rightarrow j}.
}
\]

Hence the process satisfies detailed balance with stationary distribution
\(\pi\).

Local detailed balance and Markov jump processes are standard tools in
stochastic thermodynamics. The EDF-specific content here is the structural
defect \(D_k\), not the general detailed-balance framework.

---

# 9. Topology separates stationary selection from pathways

Entry 09 tests two symmetric connected graphs:

1. a complete graph;
2. a nearest-neighbor path graph in ordered \(k\)-space.

Both yield the same stationary MaxEnt distribution because the same defect
potential enters the detailed-balance ratio.

However, their generator spectral gaps differ.

Therefore:

\[
\boxed{
\text{structural defect controls stationary preference,}
}
\]

while

\[
\boxed{
\text{graph topology controls kinetics and pathways.}
}
\]

This distinction is important for Entry 10, where transient and metastable
pathways will become the primary object of study.

---

# 10. Selection-functional proposition

## Proposition — DCT-Compatible MaxEnt Selection

Let the DCT closure defect be

\[
D_k
=
\left|
\ln\frac{F_k}{k^2}
\right|.
\]

On a finite candidate set with uniform prior, constrain only the ensemble mean
defect.

Then the maximum-entropy distribution is

\[
\boxed{
\pi_k(\lambda)
=
\frac{e^{-\lambda D_k}}
{\sum_j e^{-\lambda D_j}}.
}
\]

If \(k=12\) is the unique zero-defect sector, then for \(\lambda\ge0\):

\[
\frac{d\langle D\rangle}{d\lambda}
\le0,
\]

\[
\frac{dH}{d\lambda}
\le0,
\]

\[
\frac{d\pi_{12}}{d\lambda}
\ge0,
\]

and

\[
\lim_{\lambda\rightarrow\infty}
\pi_{12}=1.
\]

This proposition is exact once the MaxEnt constraint model is declared.

It is not a new premise of DCT.

---

# 11. Epistemic status registry

### Exact DCT consequence

\[
F_k=k^2
\]

is the closure condition, with unique solution \(k=12\).

### Exact defect identities

\[
D_k=0
\iff
F_k=k^2,
\]

\[
B_k=\tanh(D_k/2),
\]

and

\[
S_k=2\sinh(D_k/2).
\]

### Inference principle

The exponential family

\[
\pi_k\propto e^{-\lambda D_k}
\]

follows from maximum entropy under the declared mean-defect constraint.

### Standard stochastic embedding

The symmetric exponential rate family satisfies detailed balance with
\(\pi\).

### Still phenomenological

The value and microscopic meaning of

\[
\lambda
\]

and the attempt scale

\[
\nu
\]

remain undetermined.

The kinetic graph topology also remains a model choice until EDF dynamics
selects it.

---

# 12. Falsification and sensitivity gates

Entry 09 should be revised if:

1. a more primitive EDF derivation produces a different dimensionless mismatch
   measure and supplies additional constraints beyond mean defect;
2. EDF derives a nonuniform prior over closure sectors;
3. the physical closure dynamics is intrinsically nonequilibrium and cannot be
   represented by a detailed-balance stationary process;
4. a microscopic EDF law fixes transition rates incompatible with the declared
   exponential symmetric form;
5. empirical dynamics requires path-dependent or non-Markovian selection.

Importantly, failure of the Entry 09 dynamical model would not by itself
invalidate DCT.

The theorem and its stochastic realization are separate layers.

---

# 13. Transition to Entry 10

The next question is no longer:

> Which sector has the smallest structural defect?

DCT has already answered that.

The next question is:

> Do transient sectors that disappear from the final state causally modify the
> probability and pathway by which the exact closure is reached?

Entry 10 should therefore introduce intervention-based pathway measures such
as

\[
\mathcal C_j
=
P_{\rm sel}(12)
-
P_{\rm sel}^{(-j)}(12),
\]

together with residence, first-passage, pathway-flux, and sector-removal
diagnostics.

This is where Dynamic Closure becomes genuinely dynamical.

---

# References

1. E. T. Jaynes, “Information Theory and Statistical Mechanics,” *Physical Review* **106**, 620–630 (1957). DOI: 10.1103/PhysRev.106.620.

2. E. T. Jaynes, “Information Theory and Statistical Mechanics. II,” *Physical Review* **108**, 171–190 (1957). DOI: 10.1103/PhysRev.108.171.

3. G. Falasco and M. Esposito, “Local detailed balance across scales: From diffusions to jump processes and beyond,” *Physical Review E* **103**, 042114 (2021). DOI: 10.1103/PhysRevE.103.042114.

4. G. Falasco and M. Esposito, “Macroscopic stochastic thermodynamics,” *Reviews of Modern Physics* **97**, 015002 (2025). DOI: 10.1103/RevModPhys.97.015002.

5. Y. Bugeaud, M. Mignotte, and S. Siksek, “Classical and modular approaches to exponential Diophantine equations I. Fibonacci and Lucas perfect powers,” *Annals of Mathematics* **163**, 969–1018 (2006). DOI: 10.4007/annals.2006.163.969.
