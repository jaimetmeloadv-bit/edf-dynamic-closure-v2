# Dynamic Closure Notebook — Entry 08
## Consolidation of the Dynamic Closure Theorem (DCT)

### Scientific status

Entry 08 introduces no new physical mechanism.

Its purpose is to consolidate Entries 04–07 into a formal theorem package with explicit separation among:

1. **EDF structural premises**;
2. **exact mathematical lemmas and theorems**;
3. **published external mathematical results**;
4. **computational verification**;
5. **later empirical correspondence**.

The numerical implementation is a computational certificate of the formal chain. It is not the proof itself.

---

# 1. Definitions

## Definition 1 — Finite EDF phase kernel

Let

\[
A_k=
\left\{
e^{2\pi i m/k}
:
m\in\mathbb Z_k
\right\},
\qquad
k\ge2.
\]

Let

\[
\mathcal H_k
=
\operatorname{span}
\{
|m\rangle:
m\in\mathbb Z_k
\},
\]

and define the primitive root of unity

\[
\omega_k=e^{2\pi i/k}.
\]

---

## Definition 2 — Phase operator

The phase-resolved cyclic kernel is represented by

\[
\boxed{
Z|m\rangle
=
\omega_k^m|m\rangle.
}
\]

Therefore

\[
Z^k=I.
\]

---

## Definition 3 — Primitive coherent phase evolution

Let the primitive phase update be

\[
\boxed{
\phi_{n+1}
=
\phi_n+\Delta\phi
\pmod{2\pi}.
}
\]

A homogeneous update preserves \(A_k\) only if

\[
e^{i\Delta\phi}
\]

is itself a \(k\)-th root of unity.

---

## Definition 4 — Primitive traversal operator

If

\[
\Delta\phi
=
\frac{2\pi r}{k},
\]

then the induced update of sector labels is

\[
m\mapsto m+r\pmod{k}.
\]

Define

\[
U_r|m\rangle
=
|m+r\pmod{k}\rangle.
\]

Writing

\[
X|m\rangle=|m+1\pmod{k}\rangle,
\]

we have

\[
\boxed{
U_r=X^r.
}
\]

---

## Definition 5 — Dynamic structural closure capacity

Define

\[
C(k)
\]

as the complex dimension of the smallest unital associative operator algebra containing all operations required by primitive EDF closure.

Thus \(C(k)\) is not assigned in advance. It is derived from the required generators.

---

# 2. EDF premise registry

The theorem chain depends on five explicit structural premises.

### P1 — Finite cyclic phase resolution

EDF resolves the \(k\) phases of

\[
A_k.
\]

### P2 — Homogeneous coherent primitive evolution

Primitive evolution is additive in phase:

\[
\phi_{n+1}
=
\phi_n+\Delta\phi
\pmod{2\pi}.
\]

### P3 — Primitive recurrence order \(k\)

The first complete recurrence occurs after exactly \(k\) primitive updates.

### P4 — Unital associative dynamic closure

The operations required by fundamental closure belong to the smallest unital associative complex operator algebra closed under composition.

### P5 — Fibonacci compatibility

Exact EDF structural compatibility requires

\[
\boxed{
F_k=C(k).
}
\]

Premises P1–P4 determine the operator-space closure. P5 is introduced only afterward.

---

# 3. Lemma I — Kernel-preserving phase quantization

If the homogeneous phase update preserves the finite kernel \(A_k\), then

\[
e^{i\Delta\phi}
=
\omega_k^r
\]

for some

\[
r\in\mathbb Z_k.
\]

Therefore

\[
\boxed{
\Delta\phi
=
\frac{2\pi r}{k}
\pmod{2\pi}.
}
\]

This result depends on P1 and P2.

---

# 4. Lemma II — Primitive recurrence implies transitivity

Repeated application of the phase step \(r\) generates

\[
m_n
=
m_0+nr
\pmod{k}.
\]

The orbit length is

\[
L(k,r)
=
\frac{k}{\gcd(k,r)}.
\]

P3 requires

\[
L(k,r)=k.
\]

Therefore

\[
\boxed{
\gcd(k,r)=1.
}
\]

Thus \(r\) belongs to the unit group

\[
\mathbb Z_k^\times.
\]

Consequently the orbit visits every element of \(\mathbb Z_k\) exactly once before recurrence.

---

# 5. Lemma III — Primitive traversal generates the canonical shift

From Definition 4,

\[
U_r=X^r.
\]

Since

\[
\gcd(k,r)=1,
\]

there exists an integer \(s\) such that

\[
rs\equiv1\pmod{k}.
\]

Therefore

\[
(U_r)^s
=
X^{rs}
=
X.
\]

Hence

\[
\boxed{
X\in\operatorname{alg}(U_r).
}
\]

Conversely,

\[
U_r=X^r
\in\operatorname{alg}(X).
\]

Therefore

\[
\boxed{
\operatorname{alg}(U_r)
=
\operatorname{alg}(X).
}
\]

This is stronger than mere relabeling equivalence: every primitive traversal directly generates the canonical shift by taking an appropriate positive group power.

---

# 6. Lemma IV — Primitive phase–traversal Weyl relation

Since

\[
U_r=X^r,
\]

and

\[
ZX=\omega_kXZ,
\]

we obtain

\[
ZU_r
=
ZX^r
=
\omega_k^rX^rZ.
\]

Therefore

\[
\boxed{
ZU_r
=
\omega_k^rU_rZ.
}
\]

Because

\[
\gcd(k,r)=1,
\]

\[
\omega_k^r
\]

is itself a primitive \(k\)-th root of unity.

Thus the actual primitive traversal \(U_r\), not merely the canonical \(X\), forms a finite Weyl pair with \(Z\).

---

# 7. Lemma V — Completeness of the primitive phase–traversal basis

Define

\[
W^{(r)}_{a,b}
=
U_r^aZ^b,
\qquad
(a,b)\in\mathbb Z_k^2.
\]

Since multiplication by the unit \(r\) permutes \(\mathbb Z_k\),

\[
\{U_r^a:a\in\mathbb Z_k\}
=
\{X^a:a\in\mathbb Z_k\}.
\]

Therefore

\[
\{
U_r^aZ^b
\}
=
\{
X^aZ^b
\}
\]

as an operator set up to index permutation.

The finite Weyl operators satisfy Hilbert–Schmidt orthogonality,

\[
\operatorname{Tr}
\left[
\left(W^{(r)}_{a,b}\right)^\dagger
W^{(r)}_{c,d}
\right]
=
k\,
\delta_{ac}\delta_{bd}.
\]

Hence the \(k^2\) operators are linearly independent.

Since

\[
\dim_{\mathbb C}M_k(\mathbb C)=k^2,
\]

they constitute a complete basis.

Therefore

\[
\boxed{
\operatorname{alg}(U_r,Z)
=
M_k(\mathbb C).
}
\]

---

# 8. Theorem A — Dynamic Algebraic Closure Theorem

### Statement

Let a finite EDF closure kernel contain \(k\ge2\) phase-resolved cyclic sectors.

Assume P1–P4:

1. finite cyclic phase resolution;
2. homogeneous coherent primitive phase evolution;
3. primitive recurrence order \(k\);
4. unital associative dynamic closure.

Then the primitive traversal \(U_r\) and the phase operator \(Z\) generate the full matrix algebra:

\[
\boxed{
\operatorname{alg}(U_r,Z)
=
M_k(\mathbb C).
}
\]

Consequently,

\[
\boxed{
C(k)=k^2.
}
\]

### Proof

By Lemma I,

\[
\Delta\phi
=
\frac{2\pi r}{k}.
\]

By Lemma II,

\[
\gcd(k,r)=1.
\]

By Lemma III,

\[
X\in\operatorname{alg}(U_r).
\]

By Lemma IV, \((U_r,Z)\) obeys a primitive finite Weyl relation.

By Lemma V, the \(k^2\) operators

\[
U_r^aZ^b
\]

form a basis of

\[
M_k(\mathbb C).
\]

P4 therefore gives

\[
\operatorname{alg}(U_r,Z)
=
M_k(\mathbb C),
\]

so

\[
C(k)
=
\dim_{\mathbb C}M_k(\mathbb C)
=
k^2.
\]

\[
\boxed{\text{QED}}
\]

No Fibonacci assumption appears in Theorem A.

---

# 9. Proposition — Reduced spaces do not satisfy full composition closure

The traceless \(k^2-1\) Weyl sector excludes the identity.

For every nonidentity Weyl element,

\[
W_{a,b}W_{-a,-b}
=
\omega_k^{-ab}I.
\]

Thus ordinary operator composition regenerates the excluded identity.

Therefore the \(k^2-1\) traceless sector is not a unital associative algebra under ordinary multiplication.

Likewise, in the matrix-unit basis

\[
E_{ij}=|i\rangle\langle j|,
\]

removing the self-relations \(E_{ii}\) fails because

\[
E_{ij}E_{ji}=E_{ii}.
\]

Hence full dynamic operator closure requires the identity/self sector.

This distinguishes the full operator capacity

\[
k^2
\]

from reduced normalized-state coordinates

\[
k^2-1.
\]

---

# 10. Fibonacci compatibility

Only after the algebraic closure capacity has been derived do we invoke P5:

\[
F_k=C(k).
\]

Theorem A gives

\[
C(k)=k^2.
\]

Therefore

\[
\boxed{
F_k=k^2.
}
\]

This separates the operator-algebra derivation from the Fibonacci condition.

---

# 11. Theorem B — Arithmetic uniqueness

Bugeaud, Mignotte, and Siksek proved that the only perfect powers in the Fibonacci sequence are

\[
0,\quad 1,\quad 8,\quad 144.
\]

Assume

\[
k\ge2
\]

and

\[
F_k=k^2.
\]

Then \(F_k\) is a perfect power and must belong to that published classification.

The relevant Fibonacci indices are

\[
k=2,\quad6,\quad12.
\]

Direct evaluation gives

\[
F_2=1\ne4,
\]

\[
F_6=8\ne36,
\]

and

\[
F_{12}=144=144=12^2.
\]

Hence

\[
\boxed{
F_k=k^2
\iff
k=12,
\qquad
k\ge2.
}
\]

This arithmetic result is exact and does not depend on numerical scanning.

---

# 12. Main result — Dynamic Closure Theorem

## Dynamic Closure Theorem (DCT)

Let \(k\ge2\). Suppose the EDF closure kernel satisfies premises P1–P5:

1. the finite cyclic phases of \(A_k\) are resolved;
2. primitive evolution is homogeneous coherent phase accumulation;
3. the first complete recurrence occurs after exactly \(k\) primitive updates;
4. fundamental dynamic closure is the smallest unital associative complex operator algebra containing the required phase and traversal operations;
5. exact EDF Fibonacci compatibility requires \(F_k=C(k)\).

Then

\[
\boxed{
k=12.
}
\]

### Proof

Entries 1–4 of the theorem chain give

\[
\Delta\phi
=
\frac{2\pi r}{k},
\]

\[
\gcd(k,r)=1,
\]

\[
U_r=X^r,
\]

and

\[
ZU_r=\omega_k^rU_rZ.
\]

By Theorem A,

\[
C(k)=k^2.
\]

By P5,

\[
F_k=C(k)=k^2.
\]

By Theorem B,

\[
k=12.
\]

\[
\boxed{\text{QED}}
\]

---

# 13. Corollary 1 — Primitive traversal multiplicity

The number of admissible primitive traversal indices is the number of units of \(\mathbb Z_k\):

\[
\boxed{
N_{\rm primitive}(k)
=
\varphi(k).
}
\]

For

\[
k=12,
\]

\[
\varphi(12)=4,
\]

and the primitive traversal generators are

\[
\boxed{
r\in\{1,5,7,11\}.
}
\]

---

# 14. Corollary 2 — Primitive-generator invariance of the closure algebra

For every

\[
r\in\mathbb Z_k^\times,
\]

there exists

\[
s=r^{-1}\pmod{k}
\]

such that

\[
(U_r)^s=X.
\]

Therefore

\[
\boxed{
\operatorname{alg}(U_r,Z)
=
M_k(\mathbb C)
}
\]

for every primitive generator \(r\).

The closure algebra does not depend on which generator of the primitive cyclic traversal is chosen.

---

# 15. Corollary 3 — Nonprimitive steps produce subclosure

If

\[
\gcd(k,r)=d>1,
\]

then the orbit length is

\[
L(k,r)=\frac{k}{d}<k,
\]

and the sector set decomposes into \(d\) disjoint cycles.

Thus nonunit values of \(r\) generate subclosures rather than the primitive full closure.

For \(k=12\):

\[
r=2
\Rightarrow
2\text{ cycles of length }6,
\]

\[
r=3
\Rightarrow
3\text{ cycles of length }4,
\]

\[
r=4
\Rightarrow
4\text{ cycles of length }3,
\]

\[
r=6
\Rightarrow
6\text{ cycles of length }2.
\]

This result may later provide a natural bridge between fundamental closure and lower-order effective symmetries.

---

# 16. Computational certificate

The Entry 08 implementation contains two distinct classes of verification.

## 16.1 Exact integer verification

For

\[
k=2,\ldots,72,
\]

the code verifies exactly:

\[
L(k,r)
=
\frac{k}{\gcd(k,r)},
\]

primitive recurrence iff

\[
\gcd(k,r)=1,
\]

existence of the modular inverse

\[
s=r^{-1}\pmod{k},
\]

and

\[
rs\equiv1\pmod{k}.
\]

It also verifies exactly that the number of primitive generators equals

\[
\varphi(k).
\]

For \(k=12\) the exact primitive set is

\[
\{1,5,7,11\}.
\]

A direct Fibonacci scan through

\[
k=500
\]

finds only

\[
k=12
\]

as a solution of

\[
F_k=k^2.
\]

That finite scan is a computational check; global uniqueness follows from the published Bugeaud–Mignotte–Siksek theorem.

## 16.2 Operator-space verification

For

\[
k=2,\ldots,16,
\]

the code tests every primitive traversal generator and verifies that

\[
\operatorname{rank}
\{
U_r^aZ^b
\}
=
k^2.
\]

The maximum Weyl-relation residual in the present run is approximately

\[
3.91\times10^{-15}.
\]

The modular-inverse recovery

\[
(U_r)^s=X
\]

has zero permutation-matrix residual.

The maximum sampled Hilbert–Schmidt orthogonality residual is approximately

\[
1.20\times10^{-14}.
\]

These are numerical implementation checks consistent with floating-point precision.

---

# 17. Assumption-dependency matrix

The theorem must remain auditable.

| Result | Depends on | Epistemic status |
|---|---|---|
| \(\Delta\phi=2\pi r/k\) | P1, P2 | Exact conditional lemma |
| \(\gcd(k,r)=1\) | P3 + phase quantization | Exact conditional lemma |
| \(U_r=X^r,\;X=(U_r)^s\) | primitive \(r\) | Exact group result |
| \(ZU_r=\omega_k^rU_rZ\) | phase + traversal | Exact operator identity |
| \(C(k)=k^2\) | P1–P4 | Exact conditional theorem |
| \(F_k=k^2\) | P5 + Theorem A | Exact conditional proposition |
| \(k=12\) | BMS theorem | Exact arithmetic consequence |
| Dynamic stochastic preference | later entries | Numerical |
| Real-world correspondence | later entries | Empirical |

This table is part of the scientific argument, not merely documentation.

---

# 18. Falsification gates

The DCT chain does not follow if any indispensable premise fails.

### Gate G1

If the finite phases of \(A_k\) are not physically resolved, the operator \(Z\) is not forced by the EDF kernel.

### Gate G2

If primitive evolution is not homogeneous coherent phase accumulation, the quantization

\[
\Delta\phi=2\pi r/k
\]

need not follow.

### Gate G3

If the first recurrence order is smaller than \(k\), then

\[
\gcd(k,r)>1
\]

may be allowed and full primitive traversal fails.

### Gate G4

If fundamental dynamic closure is not unital and associative under operator composition, the full matrix-algebra theorem need not apply.

### Gate G5

If the Fibonacci compatibility condition

\[
F_k=C(k)
\]

cannot be independently justified by EDF, then

\[
C(k)=k^2
\]

still follows from P1–P4, but

\[
k=12
\]

does not.

### Gate G6

The arithmetic uniqueness step is tied to the published perfect-power classification. Any valid mathematical revision of that classification would require re-evaluation of Theorem B.

Explicit falsification gates prevent conditional premises from being misrepresented as unconditional facts.

---

# 19. Final internal proof chain

The consolidated exact chain is

\[
\boxed{
\begin{aligned}
A_k
&\xrightarrow{\text{P1}}
Z,
\\
\text{coherent primitive evolution}
&\xrightarrow{\text{P2}}
\Delta\phi=\frac{2\pi r}{k},
\\
\text{primitive recurrence}
&\xrightarrow{\text{P3}}
\gcd(k,r)=1,
\\
&\Rightarrow
U_r=X^r,
\\
&\Rightarrow
X=(U_r)^{r^{-1}},
\\
(Z,U_r)
&\Rightarrow
ZU_r=\omega_k^rU_rZ,
\\
\text{P4}
&\Rightarrow
\operatorname{alg}(U_r,Z)=M_k(\mathbb C),
\\
&\Rightarrow
C(k)=k^2,
\\
\text{P5}
&\Rightarrow
F_k=k^2,
\\
\text{BMS theorem}
&\Rightarrow
\boxed{k=12}.
\end{aligned}
}
\]

At this point the internal DCT derivation is consolidated.

The notebook can now change character from foundational derivation to:

\[
\boxed{
\text{dynamics}
\rightarrow
\text{falsification}
\rightarrow
\text{robustness}
\rightarrow
\text{physical correspondence}.
}
\]

---

# References

1. Y. Bugeaud, M. Mignotte, and S. Siksek, “Classical and modular approaches to exponential Diophantine equations I. Fibonacci and Lucas perfect powers,” *Annals of Mathematics* **163** (2006), 969–1018. DOI: 10.4007/annals.2006.163.969.

2. R. A. Bertlmann and P. Krammer, “Bloch vectors for qudits,” *Journal of Physics A: Mathematical and Theoretical* **41**, 235303 (2008). arXiv:0806.1174.

3. S. M. Carroll and A. Singh, “Quantum mereology: Factorizing Hilbert space into subsystems with quasiclassical dynamics,” *Physical Review A* **103**, 022213 (2021). DOI: 10.1103/PhysRevA.103.022213.

---

# Repository status after Entry 08

**Foundational derivation:** consolidated.

**Next phase:** derive a theorem-compatible closure-defect/selection functional and begin systematic dynamic falsification without modifying the DCT premises after observing the numerical outcomes.
