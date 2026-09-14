# Dynamic Closure Notebook — Entry 16
## Premise Minimality, Independence, and Exact Subclosure Algebra

Entry 16 asks a question that is mathematically prior to publication: does the final Dynamic Closure Theorem use more assumptions than are actually needed? The answer is yes in a useful way. The EDF phase law remains physically meaningful, but the algebraic statement \(C(k)=k^2\) requires less structure than the earlier P1--P4 formulation suggested. At the same time, primitive recurrence is not merely convenient: when it is removed, the generated algebra has an exact lower-dimensional block form that can be calculated for every nonprimitive step.

This entry therefore separates three levels that should no longer be compressed into one premise list:

\[
\boxed{
\text{minimal operator theorem}
}
\]

\[
\boxed{
\text{EDF dynamical realization of its hypotheses}
}
\]

and

\[
\boxed{
\text{Fibonacci-compatible selection of }k.
}
\]

The last of these is better called the **Fibonacci Compatibility Condition** rather than “P5,” because it is a compatibility branch applied after the algebraic closure theorem, not an assumption needed to derive the operator algebra itself.

---

## 1. The original premise structure

The completed DCT pipeline was summarized by

\[
P_1:
\quad
A_k=
\left\{
e^{2\pi i m/k}:m\in\mathbb Z_k
\right\},
\]

\[
P_2:
\quad
\phi_{n+1}
=
\phi_n+\Delta\phi
\pmod{2\pi},
\]

\[
P_3:
\quad
\text{first complete recurrence after exactly }k\text{ updates},
\]

\[
P_4:
\quad
\text{unital associative complex operator closure},
\]

followed by

\[
P_5:
\quad
F_k=C(k).
\]

Entries 05--08 showed that \(P_1\)--\(P_4\) imply

\[
C(k)=k^2,
\]

while the last condition gives

\[
F_k=k^2
\]

and hence

\[
k=12.
\]

Entry 16 refines this dependency structure.

---

## 2. Minimal operator closure theorem

Let \(\mathcal H\cong\mathbb C^k\). Suppose \(D\) is a diagonalizable operator with \(k\) distinct eigenvalues,

\[
D|j\rangle
=
\lambda_j|j\rangle,
\qquad
\lambda_i\ne\lambda_j
\quad(i\ne j).
\]

Suppose also that \(S\) acts transitively as one \(k\)-cycle,

\[
S|j\rangle
=
|j+1\pmod{k}\rangle.
\]

Let \(\mathcal A\subseteq M_k(\mathbb C)\) be a complex-linear subspace containing \(D\) and \(S\) and closed under ordinary operator multiplication.

No separate assumption of a unit is needed. Since

\[
S^k=I,
\]

multiplicative closure already gives

\[
I\in\mathcal A.
\]

No separate assumption of associativity is needed either: multiplication in \(M_k(\mathbb C)\) is associative, and \(\mathcal A\) inherits that operation.

Because the eigenvalues of \(D\) are distinct, define for each \(j\) the Lagrange polynomial

\[
p_j(x)
=
\prod_{\substack{m=0\\m\ne j}}^{k-1}
\frac{x-\lambda_m}{\lambda_j-\lambda_m}.
\]

By construction,

\[
p_j(\lambda_n)
=
\delta_{jn}.
\]

Therefore

\[
p_j(D)|n\rangle
=
\delta_{jn}|n\rangle,
\]

so

\[
\boxed{
p_j(D)=E_{jj}=|j\rangle\langle j|.
}
\]

Since \(\mathcal A\) contains \(D\), \(I\), and is closed under linear combinations and multiplication, it contains every polynomial \(p_j(D)\). Thus every diagonal matrix unit belongs to \(\mathcal A\).

For arbitrary \(i,j\), choose

\[
a=i-j\pmod{k}.
\]

Then

\[
S^aE_{jj}
=
S^a|j\rangle\langle j|
=
|i\rangle\langle j|
=
E_{ij}.
\]

Hence every matrix unit belongs to the algebra,

\[
E_{ij}\in\mathcal A
\qquad
\forall i,j.
\]

Because the \(k^2\) matrix units form a basis of \(M_k(\mathbb C)\),

\[
\boxed{
\mathcal A=M_k(\mathbb C).
}
\]

Therefore

\[
\boxed{
\dim_{\mathbb C}\mathcal A=k^2.
}
\]

This gives the following theorem.

**Minimal Dynamic Matrix-Closure Theorem.** A simple-spectrum sector resolver, a transitive cyclic traversal, and complex-linear closure under ordinary operator multiplication generate the complete matrix algebra \(M_k(\mathbb C)\).

The exact root-of-unity form of the EDF phase kernel is therefore stronger than what is required merely to obtain \(k^2\). It remains important because it supplies the phase meaning, the quantized phase increment, and the finite Weyl relation.

---

## 3. EDF specialization: the matrix-unit proof becomes even simpler

For EDF,

\[
D=Z,
\]

with

\[
Z|m\rangle
=
\omega_k^m|m\rangle,
\qquad
\omega_k=e^{2\pi i/k}.
\]

Instead of Lagrange interpolation, the diagonal projectors can be written directly by finite Fourier inversion,

\[
\boxed{
E_{jj}
=
\frac1k
\sum_{b=0}^{k-1}
\omega_k^{-jb}Z^b.
}
\]

To verify this, act on \(|n\rangle\):

\[
\frac1k
\sum_{b=0}^{k-1}
\omega_k^{-jb}Z^b|n\rangle
=
\frac1k
\sum_{b=0}^{k-1}
\omega_k^{(n-j)b}|n\rangle.
\]

The finite root-of-unity sum gives

\[
\sum_{b=0}^{k-1}
\omega_k^{(n-j)b}
=
k\delta_{nj}.
\]

Hence

\[
E_{jj}|n\rangle
=
\delta_{jn}|n\rangle.
\]

For primitive traversal \(U_r=X^r\), with

\[
\gcd(k,r)=1,
\]

there exists \(s=r^{-1}\pmod{k}\), so

\[
X=(U_r)^s.
\]

Therefore

\[
\boxed{
E_{ij}
=
X^{i-j}E_{jj}
}
\]

belongs to the generated algebra for every \(i,j\).

This provides a compact matrix-unit proof of

\[
\boxed{
\operatorname{alg}(Z,U_r)
=
M_k(\mathbb C),
}
\]

without first requiring the Hilbert--Schmidt orthogonality argument. The Weyl-basis proof remains correct and useful, but the matrix-unit derivation may be more economical in the Version-2 manuscript.

---

## 4. Which old premises are genuinely algebraic necessities?

The previous formulation made the homogeneous phase law look like a direct algebraic requirement. It is not.

The algebraic closure theorem needs a transitive cyclic traversal \(S\). It does not care how that traversal was generated.

Thus the old phase-evolution condition

\[
\phi_{n+1}
=
\phi_n+\Delta\phi
\pmod{2\pi}
\]

belongs to the **EDF dynamical realization** of the theorem, not to the minimal matrix-algebra theorem itself.

In EDF, the homogeneous law plus phase-kernel preservation gives

\[
\Delta\phi
=
\frac{2\pi r}{k},
\]

and therefore

\[
U_r=X^r.
\]

Primitive recurrence then imposes

\[
\gcd(k,r)=1,
\]

which makes \(U_r\) a transitive \(k\)-cycle.

The logic is therefore better written as

\[
\boxed{
\text{EDF phase kernel + homogeneous evolution + primitive recurrence}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{simple-spectrum resolver + transitive cyclic traversal}
}
\]

\[
\Downarrow
\]

\[
\boxed{
M_k(\mathbb C),\quad C(k)=k^2.
}
\]

This separation strengthens the paper because the algebraic theorem no longer depends unnecessarily on a particular dynamical parametrization.

---

## 5. Primitive recurrence is necessary for full matrix closure

Now remove primitive recurrence while keeping the EDF phase resolver

\[
Z|m\rangle
=
\omega_k^m|m\rangle
\]

and traversal

\[
U_r=X^r.
\]

Let

\[
d=\gcd(k,r),
\]

and write

\[
k=d\ell.
\]

Repeated addition of \(r\) partitions \(\mathbb Z_k\) into \(d\) disjoint orbits, each of length

\[
\ell
=
\frac{k}{d}.
\]

Because \(r=dr'\), the update preserves the residue of \(m\) modulo \(d\). Thus no power of \(U_r\) connects two different orbits.

The phase operator \(Z\) is diagonal and also cannot connect different orbits. Therefore every operator generated from \(Z\) and \(U_r\) is block diagonal with respect to the orbit decomposition.

However, within each orbit the traversal is transitive. The Fourier projector formula still gives every diagonal matrix unit \(E_{jj}\), and multiplying by powers of \(U_r\) gives

\[
U_r^nE_{jj}
=
|j+nr\rangle\langle j|.
\]

As \(n\) ranges over \(0,\ldots,\ell-1\), the ket label ranges over every state in the orbit containing \(j\). Hence all matrix units connecting states inside the same orbit are generated.

Therefore each orbit carries a complete copy of

\[
M_\ell(\mathbb C).
\]

Since there are \(d\) disjoint orbits,

\[
\boxed{
\operatorname{alg}(Z,U_r)
\cong
\bigoplus_{\alpha=1}^{d}
M_{\ell}(\mathbb C),
\qquad
\ell=\frac{k}{d}.
}
\]

Its dimension is

\[
\dim\operatorname{alg}(Z,U_r)
=
d\ell^2.
\]

Substituting

\[
\ell=\frac{k}{d}
\]

gives the exact formula

\[
\boxed{
C_r(k)
=
\dim\operatorname{alg}(Z,X^r)
=
\frac{k^2}{\gcd(k,r)}.
}
\]

This is a new closed-form subclosure result extracted from the earlier DCT pipeline.

For primitive traversal,

\[
\gcd(k,r)=1,
\]

so

\[
C_r(k)=k^2.
\]

For nonprimitive traversal,

\[
\gcd(k,r)>1,
\]

and therefore

\[
C_r(k)<k^2.
\]

Thus primitive recurrence is exactly the condition that prevents the operator algebra from decomposing into disconnected matrix blocks.

---

## 6. Complete \(k=12\) subclosure algebra

At \(k=12\),

\[
C_r(12)
=
\frac{144}{\gcd(12,r)}.
\]

For

\[
r\in\{1,5,7,11\},
\]

\[
\gcd(12,r)=1,
\]

so

\[
C_r(12)=144.
\]

For

\[
r=2,10,
\]

\[
\gcd(12,r)=2,
\]

so

\[
C_r(12)=72.
\]

These dynamics consist of two six-cycles,

\[
\operatorname{alg}(Z,X^r)
\cong
M_6(\mathbb C)\oplus M_6(\mathbb C),
\]

with

\[
2(6^2)=72.
\]

For

\[
r=3,9,
\]

\[
\gcd(12,r)=3,
\]

and

\[
C_r(12)=48.
\]

The algebra is

\[
M_4(\mathbb C)
\oplus
M_4(\mathbb C)
\oplus
M_4(\mathbb C),
\]

with

\[
3(4^2)=48.
\]

For

\[
r=4,8,
\]

\[
\gcd(12,r)=4,
\]

so

\[
C_r(12)=36.
\]

The dynamics consists of four independent three-cycles,

\[
\boxed{
\operatorname{alg}(Z,X^4)
\cong
M_3(\mathbb C)^{\oplus4},
}
\]

and

\[
4(3^2)=36.
\]

For

\[
r=6,
\]

\[
\gcd(12,6)=6,
\]

so

\[
C_6(12)=24,
\]

with

\[
\operatorname{alg}(Z,X^6)
\cong
M_2(\mathbb C)^{\oplus6}.
\]

Finally, for

\[
r=0,
\]

there is no traversal. The algebra is purely diagonal,

\[
\operatorname{alg}(Z)
\cong
\mathbb C^{12},
\]

and

\[
C_0(12)=12.
\]

Thus the full hierarchy is

\[
\boxed{
12,\quad24,\quad36,\quad48,\quad72,\quad144.
}
\]

The associated orbit lengths are

\[
1,\quad2,\quad3,\quad4,\quad6,\quad12.
\]

This provides an exact algebraic meaning for effective subclosures: lower cyclic order is accompanied by a correspondingly block-decomposed operator algebra.

---

## 7. Independence countermodel I: remove resolved phase

Suppose the traversal remains primitive,

\[
X|m\rangle
=
|m+1\rangle,
\]

but no independent phase-resolving operator is present.

The algebra generated by \(X\) is

\[
\operatorname{alg}(X)
=
\operatorname{span}
\left\{
I,X,\ldots,X^{k-1}
\right\}.
\]

Since

\[
X^k=I,
\]

its dimension is

\[
\boxed{
\dim\operatorname{alg}(X)=k.
}
\]

Thus primitive traversal alone does not imply

\[
k^2.
\]

A resolved sector observable is genuinely required.

A still sharper countermodel uses a completely degenerate resolver,

\[
D=I.
\]

Although \(D\) is present and \(X\) remains transitive,

\[
\operatorname{alg}(D,X)
=
\operatorname{alg}(X),
\]

so

\[
\dim\operatorname{alg}(D,X)=k.
\]

Therefore the nondegeneracy of sector resolution matters; merely adding a diagonal operator is insufficient.

---

## 8. Independence countermodel II: remove transitive traversal

Suppose the phase resolver \(Z\) is retained, but no traversal occurs.

Then

\[
\operatorname{alg}(Z)
=
\operatorname{span}
\left\{
I,Z,\ldots,Z^{k-1}
\right\},
\]

and

\[
\boxed{
\dim\operatorname{alg}(Z)=k.
}
\]

More generally, if traversal is nonprimitive,

\[
U_r=X^r,
\qquad
d=\gcd(k,r)>1,
\]

then

\[
\boxed{
\dim\operatorname{alg}(Z,U_r)
=
\frac{k^2}{d}
<
k^2.
}
\]

Thus transitivity is not cosmetic. It is exactly what combines the \(d\) independent orbit blocks into one irreducible \(k\)-state closure.

---

## 9. Independence countermodel III: remove multiplicative closure

Suppose both one-generator cyclic algebras are present but mixed products are not required. Consider the complex-linear space

\[
\mathcal V
=
\operatorname{span}
\left(
\{I,X,\ldots,X^{k-1}\}
\cup
\{I,Z,\ldots,Z^{k-1}\}
\right).
\]

For \(k>1\), the intersection of the two cyclic spans is only the scalar identity, so

\[
\dim\mathcal V
=
k+k-1.
\]

Hence

\[
\boxed{
\dim\mathcal V
=
2k-1.
}
\]

For \(k>1\),

\[
2k-1<k^2.
\]

The missing directions are precisely the mixed phase--shift products

\[
X^aZ^b.
\]

Therefore requiring the physically available operators to be composable is essential to obtaining the full dynamic algebra.

This shows that the old P4 can be simplified, but not removed. The minimal condition is not “unital associative algebra” as a separate abstract package. It is simply:

\[
\boxed{
\text{complex-linear closure under ordinary operator composition}.
}
\]

The unit and associativity then follow automatically from the finite-cycle representation and matrix multiplication.

---

## 10. Revised DCT assumption hierarchy

Entry 16 suggests replacing the old P1--P5 list by a cleaner hierarchy.

### EDF dynamical assumptions

The EDF-specific phase structure is

\[
A_k
=
\left\{
e^{2\pi im/k}
:
m\in\mathbb Z_k
\right\}.
\]

The coherent update is

\[
\phi_{n+1}
=
\phi_n+\Delta\phi
\pmod{2\pi}.
\]

Exact kernel preservation gives

\[
\Delta\phi
=
\frac{2\pi r}{k}.
\]

Primitive recurrence requires

\[
\gcd(k,r)=1.
\]

These statements derive the two objects required by the minimal operator theorem:

\[
Z
\]

with simple spectrum, and

\[
U_r
\]

acting as one transitive \(k\)-cycle.

### Minimal closure assumption

The physically available operators are closed under complex linear combination and ordinary operator composition.

This alone gives

\[
\operatorname{alg}(Z,U_r)
=
M_k(\mathbb C)
\]

and

\[
C(k)=k^2.
\]

### Fibonacci Compatibility Condition

Only after the algebraic theorem is complete, EDF asks for the compatibility

\[
\boxed{
\mathrm{FC}:
\qquad
F_k=C(k).
}
\]

Then

\[
F_k=k^2,
\]

and the Bugeaud--Mignotte--Siksek theorem gives

\[
\boxed{k=12.}
\]

Calling this condition **FC** rather than “P5” has two advantages. It prevents the reader from interpreting Fibonacci compatibility as necessary for deriving \(M_k(\mathbb C)\), and it avoids implying that EDF must explain the universal origin of Fibonacci organization in order to study this exact compatibility branch.

---

## 11. What Entry 16 changes in the Version-2 proof

The Version-2 proof can now be shorter and more transparent.

After deriving primitive traversal, one may write

\[
E_{jj}
=
\frac1k
\sum_{b=0}^{k-1}
\omega_k^{-jb}Z^b.
\]

Then

\[
E_{ij}
=
X^{i-j}E_{jj}.
\]

Therefore all

\[
E_{ij}
\]

belong to the generated algebra, so

\[
\operatorname{alg}(X,Z)
=
M_k(\mathbb C).
\]

This gives

\[
C(k)=k^2
\]

in only a few equations while still showing every logical step.

The Hilbert--Schmidt Weyl proof may remain in the repository as an independent certificate or appear briefly as an equivalent formulation,

\[
W_{a,b}=X^aZ^b.
\]

The manuscript should then introduce FC explicitly,

\[
F_k=C(k),
\]

and continue to

\[
k=12.
\]

This avoids a long premise list and makes clear which steps belong to finite operator algebra and which belong to EDF compatibility.

---

## 12. Consequence for the triplication theorem

The new subclosure formula also refines the interpretation of the order-three dynamics.

For

\[
r=4
\]

or

\[
r=8,
\]

the traversal has four disjoint three-cycles,

\[
d=4,
\qquad
\ell=3.
\]

Hence

\[
\operatorname{alg}(Z,X^4)
\cong
M_3(\mathbb C)^{\oplus4},
\]

and

\[
\dim=36.
\]

This is different from, but compatible with, the CRT tensor factorization

\[
M_{12}(\mathbb C)
\cong
M_3(\mathbb C)\otimes M_4(\mathbb C).
\]

The direct-sum form describes what happens when the **dynamics itself is restricted to a nonprimitive three-cycle traversal**. The tensor-product form describes the **factorization of the full primitive twelve-sector Hilbert space**.

Thus there are two mathematically distinct appearances of the number three:

\[
\boxed{
\mathcal H_{12}
\cong
\mathcal H_3\otimes\mathcal H_4
}
\]

as a factorization of the full space, and

\[
\boxed{
\operatorname{alg}(Z,X^4)
\cong
M_3(\mathbb C)^{\oplus4}
}
\]

as a nonprimitive dynamical subclosure.

This distinction should be preserved in Version 2 and may become useful if EDF later derives a physical selector for triplication.

---

## 13. Consequence for fundamental versus effective symmetry

The earlier qualitative distinction

\[
k_{\rm fundamental}
\ne
k_{\rm effective}
\]

can now be sharpened algebraically.

For fundamental primitive closure,

\[
k_{\rm fundamental}=12,
\]

and

\[
C_{\rm fundamental}=144.
\]

If the effective dynamics is governed by a nonprimitive step \(r\), then

\[
k_{\rm orbit}
=
\frac{12}{\gcd(12,r)},
\]

and

\[
C_r(12)
=
\frac{144}{\gcd(12,r)}.
\]

Thus a lower observed cyclic order need not merely be a visual projection. It can correspond, within the finite operator model, to an exact block reduction of the accessible dynamic algebra.

This still does not prove that a particular physical system realizes one of these reductions. It gives the mathematical structure that such an EDF correspondence would have to use.

---

## 14. Final premise-independence summary

The conclusion \(C(k)=k^2\) fails in explicit nearby models when any one of the three minimal operator conditions is removed.

Without a simple-spectrum resolver,

\[
\dim\operatorname{alg}(X)=k.
\]

Without transitive traversal,

\[
\dim\operatorname{alg}(Z,X^r)
=
\frac{k^2}{\gcd(k,r)}
<
k^2
\]

for nonprimitive \(r\).

Without multiplicative closure,

\[
\dim\operatorname{span}
\left[
\operatorname{alg}(X)
\cup
\operatorname{alg}(Z)
\right]
=
2k-1.
\]

Thus the minimal algebraic structure is not overdetermined.

The homogeneous EDF phase law is not itself algebraically necessary; it is the physical mechanism used by EDF to derive the transitive traversal.

The exact root-of-unity spectrum is likewise stronger than the minimum algebraic requirement of distinct sector eigenvalues, but it is required for the specific EDF phase interpretation and the finite Weyl relation.

The Fibonacci condition is not part of the algebraic closure theorem at all. It should be stated separately as

\[
\mathrm{FC}:F_k=C(k).
\]

Without FC,

\[
C(k)=k^2
\]

holds but no unique value of \(k\) is selected.

With FC,

\[
F_k=k^2,
\]

and therefore

\[
\boxed{k=12}.
\]

---

## 15. Bibliographic anchors

The finite phase/shift and Weyl-operator framework is supported by:

M. A. Marchiolli and P. E. M. F. Mendonça, “Theoretical formulation of finite-dimensional discrete phase spaces: II. On the uncertainty principle for Schwinger unitary operators,” *Annals of Physics* **336**, 76--97 (2013), DOI 10.1016/j.aop.2013.05.009.

R. A. Bertlmann and P. Krammer, “Bloch vectors for qudits,” *Journal of Physics A: Mathematical and Theoretical* **41**, 235303 (2008), DOI 10.1088/1751-8113/41/23/235303, arXiv:0806.1174.

A. Vourdas, “Quantum systems with finite Hilbert space,” *Reports on Progress in Physics* **67**, 267--320 (2004), DOI 10.1088/0034-4885/67/3/R03.

For finite-dimensional matrix algebra and polynomial spectral projectors, a standard reference is:

R. A. Horn and C. R. Johnson, *Matrix Analysis*, 2nd ed., Cambridge University Press (2013).

The arithmetic compatibility step continues to use:

Y. Bugeaud, M. Mignotte, and S. Siksek, “Classical and modular approaches to exponential Diophantine equations I. Fibonacci and Lucas perfect powers,” *Annals of Mathematics* **163**, 969--1018 (2006), DOI 10.4007/annals.2006.163.969.

For the geometric-optimization motivation of golden-ratio structure, without treating it as a derivation of FC:

A. B. Hopkins, F. H. Stillinger, and S. Torquato, “Spherical codes, maximal local packing density, and the golden ratio,” arXiv:1003.3604 (2010).

---

## 16. Entry-16 conclusion

Entry 16 strengthens DCT in three ways.

First, it shows that the algebraic theorem is more general than the original EDF construction:

\[
\boxed{
\text{simple spectrum}
+
\text{transitive cycle}
+
\text{operator composition}
\Rightarrow
M_k(\mathbb C).
}
\]

Second, it derives the exact algebra for every nonprimitive traversal,

\[
\boxed{
\operatorname{alg}(Z,X^r)
\cong
\bigoplus_{\alpha=1}^{\gcd(k,r)}
M_{k/\gcd(k,r)}(\mathbb C),
}
\]

with

\[
\boxed{
C_r(k)
=
\frac{k^2}{\gcd(k,r)}.
}
\]

Third, it clarifies the role of Fibonacci compatibility. The notation “P5” should be retired in the manuscript and replaced by the explicitly separate condition

\[
\boxed{
\mathrm{FC}:F_k=C(k).
}
\]

The final theorem architecture is therefore

\[
\boxed{
\text{EDF phase dynamics}
\Rightarrow
\text{simple-spectrum resolver + primitive traversal}
}
\]

\[
\boxed{
\Rightarrow
M_k(\mathbb C)
\Rightarrow
C(k)=k^2
}
\]

followed by

\[
\boxed{
\mathrm{FC}
\Rightarrow
F_k=k^2
\Rightarrow
k=12.
}
\]

This version is both shorter and logically stronger than the earlier P1--P5 presentation.
