# Dynamic Closure Notebook — Entry 05
## Weyl-Generated Closure Algebra

### 1. Objective

Entry 04 established that the Fibonacci-square equation

\[
F_k=k^2
\]

has the unique nontrivial solution \(k=12\), conditional on the EDF closure capacity being \(k^2\).

Entry 05 addresses the remaining structural question:

> Why should the complete dynamic closure algebra of a \(k\)-sector cyclic kernel have \(k^2\) independent modes?

The derivation below does not begin with pair counting. It begins with the two elementary operations naturally associated with a cyclic phase kernel:

1. cyclic displacement among the \(k\) sectors;
2. cyclic phase multiplication.

These operations generate the finite Weyl algebra.

---

## 2. Cyclic sector space

Let

\[
\mathcal H_k=\operatorname{span}\{|m\rangle:m\in\mathbb Z_k\},
\]

and define the primitive root

\[
\omega_k=e^{2\pi i/k}.
\]

Introduce the cyclic shift operator

\[
X|m\rangle=|m+1\pmod k\rangle,
\]

and the cyclic phase operator

\[
Z|m\rangle=\omega_k^m|m\rangle.
\]

Both satisfy

\[
X^k=Z^k=I.
\]

Direct action on a basis state gives

\[
ZX|m\rangle
=
\omega_k^{m+1}|m+1\rangle,
\]

whereas

\[
XZ|m\rangle
=
\omega_k^m|m+1\rangle.
\]

Therefore

\[
\boxed{ZX=\omega_k XZ.}
\]

This is the finite Weyl relation.

---

## 3. Two independent cyclic indices

Define

\[
W_{a,b}=X^aZ^b,
\qquad
(a,b)\in\mathbb Z_k\times\mathbb Z_k.
\]

The two indices have distinct roles:

- \(a\): cyclic displacement index;
- \(b\): cyclic phase index.

Using \(Z^bX^c=\omega_k^{bc}X^cZ^b\),

\[
W_{a,b}W_{c,d}
=
X^aZ^bX^cZ^d
=
\omega_k^{bc}X^{a+c}Z^{b+d}.
\]

Hence

\[
\boxed{
W_{a,b}W_{c,d}
=
\omega_k^{bc}
W_{a+c,b+d},
}
\]

with both indices understood modulo \(k\).

Thus composition does not collapse the pair \((a,b)\) to a single index. The full product structure lives on

\[
\mathbb Z_k\times\mathbb Z_k.
\]

Consequently,

\[
\boxed{
|\mathbb Z_k\times\mathbb Z_k|=k^2.
}
\]

---

## 4. Linear independence and completeness

The Weyl operators satisfy Hilbert–Schmidt orthogonality:

\[
\operatorname{Tr}
\left(
W_{a,b}^{\dagger}W_{c,d}
\right)
=
k\,\delta_{ac}\delta_{bd}.
\]

Therefore the \(k^2\) operators are linearly independent.

But

\[
\dim_{\mathbb C} M_k(\mathbb C)=k^2.
\]

Thus the Weyl family is not merely a \(k^2\)-element subset. It is a complete operator basis:

\[
\boxed{
\operatorname{span}\{W_{a,b}\}
=
M_k(\mathbb C).
}
\]

This result is standard in finite-dimensional quantum mechanics. Bertlmann and Krammer explicitly construct \(d^2\) Weyl operators for a general \(d\)-dimensional system and show that they form an orthonormal Hilbert–Schmidt basis. Carroll and Singh likewise employ finite-dimensional clock and shift generators obeying the Weyl relation and describe their \(d^2\)-element Schwinger unitary basis.

---

# 5. Weyl-Closure Theorem

### Theorem

Let \(\mathcal A\subseteq M_k(\mathbb C)\) be a complex unital associative algebra containing the cyclic shift \(X\) and cyclic phase \(Z\) defined above.

Then

\[
\boxed{\mathcal A=M_k(\mathbb C)}
\]

and therefore

\[
\boxed{\dim_{\mathbb C}\mathcal A=k^2.}
\]

### Proof

Since \(X,Z\in\mathcal A\) and \(\mathcal A\) is closed under multiplication,

\[
X^aZ^b\in\mathcal A
\]

for every

\[
(a,b)\in\mathbb Z_k\times\mathbb Z_k.
\]

The \(k^2\) operators \(X^aZ^b\) are Hilbert–Schmidt orthogonal and hence linearly independent. Therefore

\[
\dim\mathcal A\ge k^2.
\]

But

\[
\mathcal A\subseteq M_k(\mathbb C),
\qquad
\dim M_k(\mathbb C)=k^2.
\]

Hence

\[
\dim\mathcal A=k^2
\]

and

\[
\mathcal A=M_k(\mathbb C).
\]

\[
\boxed{\text{QED}}
\]

This theorem is independent of Fibonacci arithmetic.

---

## 6. Why the identity and self-sector cannot simply be removed

The operator

\[
W_{0,0}=I
\]

is one member of the Weyl basis.

Suppose one tries to replace the full \(k^2\)-dimensional algebra by the \(k^2-1\) traceless sector obtained by deleting \(I\).

For every nonidentity Weyl element,

\[
W_{a,b}W_{-a,-b}
=
\omega_k^{-ab}I.
\]

Thus multiplication immediately regenerates the identity.

Therefore

\[
\boxed{
\{W_{a,b}:(a,b)\ne(0,0)\}
}
\]

is not closed under ordinary operator multiplication.

The same fact appears in the matrix-unit basis. Let

\[
E_{ij}=|i\rangle\langle j|.
\]

If all self-relations \(E_{ii}\) are removed, then

\[
E_{ij}E_{ji}=E_{ii}.
\]

Thus off-diagonal transition composition regenerates a self-relation.

This clarifies the distinction introduced in Entry 04:

- \(k^2-1\) is appropriate for normalized traceless state coordinates;
- \(k^2\) is required for a complete **unital associative operator algebra**.

If EDF dynamic closure is closure under composition of phase/shift processes, the relevant object is the latter.

---

## 7. Numerical verification

The Entry 05 code independently constructs \(X\), \(Z\), and all Weyl monomials for

\[
k=2,\ldots,24.
\]

It verifies:

\[
ZX=\omega_kXZ,
\]

\[
\operatorname{rank}
\{W_{a,b}\}
=
k^2,
\]

\[
\operatorname{Tr}
(W_{a,b}^{\dagger}W_{c,d})/k
=
\delta_{ac}\delta_{bd},
\]

the Weyl multiplication law, the adjoint law, identity regeneration from the \(k^2-1\) sector, and self-relation regeneration from off-diagonal matrix units.

The largest numerical errors in the present run were approximately

\[
4.03\times10^{-14}
\]

for the multiplication law,

\[
5.89\times10^{-14}
\]

for the adjoint law,

\[
1.47\times10^{-15}
\]

for the Weyl commutation relation, and

\[
2.48\times10^{-14}
\]

for Hilbert–Schmidt orthogonality.

These are floating-point residuals consistent with numerical precision.

---

# 8. Connection to the Fibonacci closure

The Weyl-closure result gives

\[
C(k)=k^2
\]

without using Fibonacci numbers.

Only afterward is the EDF Fibonacci compatibility condition introduced:

\[
F_k=C(k).
\]

Therefore

\[
F_k=k^2.
\]

Bugeaud, Mignotte, and Siksek proved that the only perfect powers in the Fibonacci sequence are

\[
0,\;1,\;8,\;144.
\]

For \(k\ge2\), the equation

\[
F_k=k^2
\]

therefore has the unique nontrivial solution

\[
\boxed{k=12},
\]

because

\[
F_{12}=144=12^2.
\]

The complete logical chain is now

\[
\boxed{
\begin{aligned}
\text{cyclic sector kernel}
&\rightarrow
(X,Z)
\\
&\rightarrow
ZX=\omega_kXZ
\\
&\rightarrow
\{X^aZ^b\}_{(a,b)\in\mathbb Z_k^2}
\\
&\rightarrow
M_k(\mathbb C)
\\
&\rightarrow
C(k)=k^2
\\
&\rightarrow
F_k=k^2
\\
&\rightarrow
k=12.
\end{aligned}
}
\]

The first five steps are algebraic. The final step is arithmetic.

---

## 9. Precise status inside EDF

Entry 05 establishes the following conditional implication:

\[
\boxed{
\begin{gathered}
\text{EDF cyclic closure requires both phase and shift generators,}
\\
\text{and dynamic closure is unital and associative under composition}
\\[2mm]
\Longrightarrow
\\[2mm]
C(k)=k^2.
\end{gathered}}
\]

The remaining EDF-specific task is therefore narrower than before:

> derive from the foundational EDF dynamics why both cyclic phase and cyclic displacement are physically necessary generators of the closure process.

Once that internal identification is established, the \(k^2\) count no longer functions as an external combinatorial assumption.

---

## 10. Repository pipeline

The replacement repository should preserve the distinction between proof and numerical validation:

\[
\text{Definitions}
\rightarrow
\text{Weyl-closure theorem}
\rightarrow
\text{Fibonacci compatibility}
\rightarrow
\text{arithmetic uniqueness}
\rightarrow
\text{stochastic closure dynamics}
\rightarrow
\text{robustness scans}
\rightarrow
\text{real-world correspondences}.
\]

The numerical notebooks verify implementations, finite-range behavior, robustness, and physical consequences. They do not replace the exact algebraic and number-theoretic steps.

---

## References

1. R. A. Bertlmann and P. Krammer, “Bloch vectors for qudits,” *Journal of Physics A: Mathematical and Theoretical* **41**, 235303 (2008). DOI: 10.1088/1751-8113/41/23/235303.

2. S. M. Carroll and A. Singh, “Quantum mereology: Factorizing Hilbert space into subsystems with quasiclassical dynamics,” *Physical Review A* **103**, 022213 (2021). DOI: 10.1103/PhysRevA.103.022213.

3. Y. Bugeaud, M. Mignotte, and S. Siksek, “Classical and modular approaches to exponential Diophantine equations I. Fibonacci and Lucas perfect powers,” *Annals of Mathematics* **163**, 969–1018 (2006). DOI: 10.4007/annals.2006.163.969.
