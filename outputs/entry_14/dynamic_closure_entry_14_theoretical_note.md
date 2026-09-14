# Dynamic Closure Notebook — Entry 14
## Theorem Repair, Strengthening, and Prediction Reconstruction

Entry 14 does not score the earlier EDF theorem ledger. It rewrites it. The purpose is to take the mathematical structures that survived Entries 01–13 and replace weak, assumed, or incorrectly identified steps by the strongest statements that are now actually available. A theorem that cannot yet be carried to its original physical interpretation is not discarded; its mathematically valid core is isolated, proved, and the remaining physical bridge is stated separately.

This review also compares the current Version-2 working source with the completed Dynamic Closure pipeline. Several statements in that source were already cautious—for example, the compact-support form of the ultraviolet theorem and the Shannon coarse-graining proof. Other statements are now obsolete because the manuscript still treats \(\mathbb Z_{12}\) as a selected kernel rather than as the result of the Dynamic Closure Theorem. Two further corrections become visible only after the DCT harvest. First, averaging over \(\mathbb Z_3\) produces the invariant sector; it does not by itself mathematically represent three independent branches. Second, the number \(6\) computed from the closure of \((\sigma_1\sigma_2)^6\) is exactly the sum of pairwise linking numbers of a three-component link, but it is not automatically the self-linking integer of a single framed ribbon in the Călugăreanu--White--Fuller relation.

The repaired Version-2 logic should therefore be read as

\[
\text{EDF premises}
\longrightarrow
\text{DCT}
\longrightarrow
\text{exact internal structures}
\longrightarrow
\text{repaired EDF theorems}
\longrightarrow
\text{physical correspondence}.
\]

The Fibonacci condition is treated here as an explicit EDF compatibility branch, not as a claim that the manuscript derives the origin or ubiquity of Fibonacci or golden-ratio organization in nature.

---

# 1. Dependency review: what DCT now supplies before the seven-theorem ledger

For a finite cyclic phase kernel,

\[
A_k
=
\left\{
e^{2\pi i m/k}
:
m\in\mathbb Z_k
\right\},
\]

let

\[
\omega_k=e^{2\pi i/k},
\qquad
Z|m\rangle
=
\omega_k^m|m\rangle.
\]

Homogeneous coherent phase evolution is written

\[
\phi_{n+1}
=
\phi_n+\Delta\phi
\pmod{2\pi}.
\]

Preservation of \(A_k\) requires

\[
\Delta\phi
=
\frac{2\pi r}{k}
\pmod{2\pi}.
\]

The induced state traversal is

\[
U_r|m\rangle
=
|m+r\pmod{k}\rangle,
\]

and the orbit length is

\[
L(k,r)
=
\frac{k}{\gcd(k,r)}.
\]

Primitive recurrence after exactly \(k\) updates gives

\[
\gcd(k,r)=1.
\]

Therefore \(r^{-1}\) exists modulo \(k\), and

\[
(U_r)^{r^{-1}}
=
X,
\]

where

\[
X|m\rangle
=
|m+1\pmod{k}\rangle.
\]

The phase and traversal generators satisfy

\[
ZU_r
=
\omega_k^rU_rZ.
\]

The \(k^2\) Weyl monomials

\[
W_{a,b}^{(r)}
=
U_r^aZ^b
\]

obey

\[
\operatorname{Tr}
\left[
\left(W_{a,b}^{(r)}\right)^\dagger
W_{c,d}^{(r)}
\right]
=
k\delta_{ac}\delta_{bd}.
\]

They are linearly independent and span the ambient \(k^2\)-dimensional matrix algebra. Hence

\[
\boxed{
\operatorname{alg}(Z,U_r)
=
M_k(\mathbb C)
}
\]

and

\[
\boxed{
C(k)
=
k^2.
}
\]

This is the Dynamic Algebraic Closure Theorem and does not require Fibonacci compatibility.

EDF then asks for compatibility with the Fibonacci hierarchy,

\[
F_k=C(k).
\]

Because the operator capacity has already been derived,

\[
F_k=k^2.
\]

The perfect-power theorem of Bugeaud, Mignotte, and Siksek leaves, for \(k\ge2\),

\[
\boxed{
k=12,
\qquad
F_{12}=144=12^2.
}
\]

This replaces the old Version-2 statement that twelve is merely a kernel-selection hypothesis. The compatibility branch does not claim to derive why Fibonacci organization exists. Hopkins, Stillinger, and Torquato provide a useful geometric precedent: in their densest-local-packing/spherical-code problem, the golden ratio appears as an exact threshold in an optimization theorem. That work is motivational for geometric efficiency, not a derivation of EDF compatibility.

At \(k=12\),

\[
\mathcal H_{12}
\cong
\mathbb C^{12},
\qquad
\mathcal A_{12}
=
M_{12}(\mathbb C),
\]

and

\[
\dim_{\mathbb C}\mathcal A_{12}
=
144.
\]

The primitive residues are

\[
r\in
\mathbb Z_{12}^{\times}
=
\{1,5,7,11\},
\]

while the proper cyclic subclosure lengths are

\[
2,\quad3,\quad4,\quad6.
\]

Because

\[
12=3\cdot4,
\qquad
\gcd(3,4)=1,
\]

the Chinese remainder theorem also gives

\[
\mathbb Z_{12}
\cong
\mathbb Z_3\times\mathbb Z_4.
\]

If

\[
a=m\pmod3,
\qquad
b=m\pmod4,
\]

then

\[
m
\equiv
4a+9b
\pmod{12},
\]

and the basis map

\[
|m\rangle_{12}
\longleftrightarrow
|a\rangle_3\otimes|b\rangle_4
\]

yields

\[
\boxed{
\mathcal H_{12}
\cong
\mathcal H_3\otimes\mathcal H_4.
}
\]

Under this basis transformation,

\[
\boxed{
X_{12}
\longleftrightarrow
X_3\otimes X_4,
}
\]

and

\[
\boxed{
Z_{12}
\longleftrightarrow
Z_3\otimes Z_4^3.
}
\]

Consequently,

\[
\boxed{
M_{12}(\mathbb C)
\cong
M_3(\mathbb C)\otimes M_4(\mathbb C),
}
\]

with

\[
144
=
9\times16.
\]

Finite-dimensional Weyl systems and Chinese-remainder factorization have established mathematical precedents in the work of Vourdas and in the finite phase-space literature.

These results are the input to the repaired EDF theorem set.

---

# 2. Repaired Theorem 1 — Soliton Generation

The completed DCT pipeline does not derive a nonlinear partial differential equation. It does, however, correct one conceptual weakness in the old soliton argument. Entries 10 and 11 showed that eliminating transient degrees of freedom does not imply removal of their dynamical influence. If a microscopic state is eliminated by Schur reduction, the retained dynamics acquires terms

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

Thus a projected EDF worldline may consistently carry an effective residue whose coefficients encode eliminated modes. This does not determine the residue's continuum profile. To obtain the \(\operatorname{sech}^2\) profile, an effective nonlinear-dispersive evolution must still be specified or derived.

Take the standard representative

\[
u_t
+
a uu_x
+
b u_{xxx}
=
0,
\]

with

\[
a\ne0,
\qquad
b\ne0.
\]

For a traveling solution,

\[
u(x,t)
=
U(\xi),
\qquad
\xi=x-vt,
\]

we have

\[
u_t=-vU',
\qquad
u_x=U',
\qquad
u_{xxx}=U'''.
\]

The equation becomes

\[
-vU'
+
aUU'
+
bU'''
=
0.
\]

Integrating once, and taking a localized state satisfying

\[
U,U',U''
\longrightarrow0
\qquad
(|\xi|\to\infty),
\]

sets the integration constant to zero and gives

\[
bU''
-vU
+
\frac{a}{2}U^2
=
0.
\]

Set

\[
U(\xi)
=
A\operatorname{sech}^2(\kappa\xi).
\]

For

\[
f(\xi)
=
\operatorname{sech}^2(\kappa\xi),
\]

direct differentiation gives

\[
f''
=
4\kappa^2f
-
6\kappa^2f^2.
\]

Since

\[
U=Af,
\]

we have

\[
U''
=
4\kappa^2U
-
\frac{6\kappa^2}{A}U^2.
\]

Substitution into the stationary equation gives

\[
b
\left(
4\kappa^2U
-
\frac{6\kappa^2}{A}U^2
\right)
-vU
+
\frac{a}{2}U^2
=
0.
\]

The coefficients of the independent powers \(U\) and \(U^2\) vanish separately,

\[
4b\kappa^2-v=0,
\]

and

\[
-\frac{6b\kappa^2}{A}
+
\frac{a}{2}
=
0.
\]

Therefore

\[
\kappa
=
\frac12
\sqrt{\frac{v}{b}},
\]

and

\[
A
=
\frac{3v}{a}.
\]

Hence

\[
\boxed{
U(\xi)
=
\frac{3v}{a}
\operatorname{sech}^2
\left[
\frac12
\sqrt{\frac{v}{b}}
\,\xi
\right].
}
\]

The normalized positive profile is obtained from

\[
\int_{-\infty}^{\infty}
\operatorname{sech}^2
\left(
\frac{x-x_0}{\ell}
\right)dx
=
2\ell,
\]

which gives

\[
\boxed{
\rho_{\rm sol}(x)
=
\frac{1}{2\ell}
\operatorname{sech}^2
\left(
\frac{x-x_0}{\ell}
\right).
}
\]

For the KdV representative,

\[
\ell
=
\kappa^{-1}
=
2\sqrt{\frac{b}{v}}.
\]

The repaired theorem is therefore:

**Solitonic Residue Theorem.** If the EDF-reduced worldline dynamics is local at leading order and its dominant effective evolution belongs to the KdV-type nonlinear-dispersive class above, then the fundamental positive localized traveling residue is represented by a \(\operatorname{sech}^2\) profile with amplitude and width fixed by the effective coefficients. Schur boundary memory supplies a mathematically controlled reason why eliminated microscopic modes may remain encoded in those effective coefficients, but DCT does not derive \(a\), \(b\), or the KdV equation itself.

This is stronger than simply adopting a \(\operatorname{sech}^2\) strand and weaker than claiming that EDF uniquely derives KdV dynamics. Standard soliton references include Drazin and Johnson.

---

# 3. Repaired Theorem 2 — Soliton Triplication

The current working manuscript uses the \(\mathbb Z_3\) subgroup and the group average

\[
\Pi_{\rm inv}
=
\frac13
(I+R+R^2).
\]

This operator is correct, but its mathematical meaning is projection onto the invariant representation. It does not, by itself, produce three distinct branches. Entry 14 replaces that step by the complete character decomposition of the exact \(\mathbb Z_3\) factor already contained in DCT.

Let

\[
R|a\rangle
=
|a+1\pmod3\rangle
\]

act on \(\mathcal H_3\), and let

\[
\omega_3=e^{2\pi i/3}.
\]

The three characters of \(\mathbb Z_3\) are

\[
\chi_s(n)
=
\omega_3^{sn},
\qquad
s=0,1,2.
\]

Define

\[
\boxed{
\Pi_s
=
\frac13
\sum_{n=0}^{2}
\omega_3^{-sn}R^n.
}
\]

To establish that these are three orthogonal projectors, compute

\[
\Pi_s\Pi_t
=
\frac19
\sum_{n=0}^{2}
\sum_{m=0}^{2}
\omega_3^{-sn-tm}
R^{n+m}.
\]

Let

\[
q=n+m\pmod3,
\qquad
m=q-n.
\]

Then

\[
\Pi_s\Pi_t
=
\frac19
\sum_{q=0}^{2}
R^q
\omega_3^{-tq}
\sum_{n=0}^{2}
\omega_3^{-(s-t)n}.
\]

The finite Fourier sum is

\[
\sum_{n=0}^{2}
\omega_3^{-(s-t)n}
=
3\delta_{st}.
\]

Therefore

\[
\Pi_s\Pi_t
=
\delta_{st}
\frac13
\sum_{q=0}^{2}
\omega_3^{-sq}R^q,
\]

and hence

\[
\boxed{
\Pi_s\Pi_t
=
\delta_{st}\Pi_s.
}
\]

Summing the three projectors,

\[
\sum_{s=0}^{2}\Pi_s
=
\frac13
\sum_{n=0}^{2}
R^n
\sum_{s=0}^{2}
\omega_3^{-sn}.
\]

Again the Fourier sum gives

\[
\sum_{s=0}^{2}
\omega_3^{-sn}
=
3\delta_{n0},
\]

so

\[
\boxed{
\Pi_0+\Pi_1+\Pi_2
=
I_3.
}
\]

Thus

\[
\boxed{
\mathcal H_3
=
\operatorname{im}\Pi_0
\oplus
\operatorname{im}\Pi_1
\oplus
\operatorname{im}\Pi_2.
}
\]

This gives an exact three-sector decomposition, not merely one invariant average.

The CRT factorization now makes the connection with the full closure precise,

\[
\mathcal H_{12}
\cong
\mathcal H_3\otimes\mathcal H_4.
\]

A mathematically clean triplication map can therefore be defined as an isometry. Let

\[
|\psi\rangle\in\mathcal H_4
\]

and let \(U_a\) be unitary operators on \(\mathcal H_4\). Define

\[
\boxed{
V|\psi\rangle
=
\frac1{\sqrt3}
\sum_{a=0}^{2}
e^{i\theta_a}
|a\rangle
\otimes
U_a|\psi\rangle.
}
\]

Its norm is

\[
\langle V\psi|V\psi\rangle
=
\frac13
\sum_{a,b=0}^{2}
e^{i(\theta_b-\theta_a)}
\langle a|b\rangle
\langle\psi|
U_a^\dagger U_b
|\psi\rangle.
\]

Orthogonality of the branch labels gives

\[
\langle a|b\rangle
=
\delta_{ab}.
\]

Hence

\[
\langle V\psi|V\psi\rangle
=
\frac13
\sum_{a=0}^{2}
\langle\psi|
U_a^\dagger U_a
|\psi\rangle.
\]

Because

\[
U_a^\dagger U_a=I,
\]

we obtain

\[
\langle V\psi|V\psi\rangle
=
\frac13
\sum_{a=0}^{2}
\langle\psi|\psi\rangle
=
\langle\psi|\psi\rangle.
\]

Therefore

\[
\boxed{
V^\dagger V=I,
}
\]

and the three-branch map is norm preserving.

For identical branches,

\[
U_0=U_1=U_2=I,
\]

the map becomes

\[
V|\psi\rangle
=
\frac1{\sqrt3}
\left(
|0\rangle
+
e^{i\theta_1}|1\rangle
+
e^{i\theta_2}|2\rangle
\right)
\otimes|\psi\rangle.
\]

This is the rigorous replacement for the earlier raw concatenation \(A\oplus A\oplus A\) followed by an imposed \(1/\sqrt3\) normalization.

The repaired theorem is:

**Exact Triplication Theorem.** The DCT closure at \(k=12\) contains an exact coprime factor \(\mathcal H_3\) through \(\mathcal H_{12}\cong\mathcal H_3\otimes\mathcal H_4\). The \(\mathbb Z_3\) factor decomposes into three mutually orthogonal Fourier-character sectors \(\Pi_0,\Pi_1,\Pi_2\), and a three-branch EDF lift can be chosen as the isometry \(V\) above. Therefore triplication is an exact internal algebraic possibility of the twelve-sector closure rather than a numerical concatenation rule.

The theorem still does not identify these three sectors with the three observed fermion generations. That identification becomes a physical prediction only when EDF supplies a quantitative map to generation-dependent observables.

The projection construction is standard finite-group representation theory; Serre provides a general reference.

---

# 4. Repaired Theorem 3 — 12-Fold Quantization

The old theorem's weakest step was the prior insertion of the integer twelve. DCT removes that weakness.

The Dynamic Algebraic Closure Theorem gives

\[
C(k)=k^2.
\]

The EDF Fibonacci-compatible branch imposes

\[
F_k=C(k),
\]

so

\[
F_k=k^2.
\]

The Bugeaud--Mignotte--Siksek theorem then gives

\[
\boxed{k=12}.
\]

For the canonical primitive traversal,

\[
r=1,
\]

so

\[
\Delta\phi
=
\frac{2\pi}{12}
=
\frac{\pi}{6}.
\]

If \(\tau_*\) is the primitive update time and \(T_*\) the first complete recurrence,

\[
T_*
=
12\tau_*,
\]

and therefore

\[
\boxed{
\tau_*
=
\frac{T_*}{12}.
}
\]

The pregeometric two-level marginal used in EDF has

\[
S_0=\ln2.
\]

If this constant informational content is integrated over one full phase cycle,

\[
\mathcal S_{\rm cyc}
=
\int_0^{2\pi}
S_0\,d\phi,
\]

then

\[
\mathcal S_{\rm cyc}
=
2\pi\ln2.
\]

Equal DCT sectorization gives the dimensionless sector amount

\[
\boxed{
\mathfrak h_{12}
=
\frac{\mathcal S_{\rm cyc}}{12}
=
\frac{\pi\ln2}{6}.
}
\]

Dividing by the full angular factor,

\[
\boxed{
\bar{\mathfrak h}_{12}
=
\frac{\mathfrak h_{12}}{2\pi}
=
\frac{\ln2}{12}.
}
\]

The notation \(\mathfrak h_{12}\) is useful because the quantity above is dimensionless as written. A physical action requires a scale \(K_S\) carrying units of action,

\[
[K_S]
=
{\rm J\,s}.
\]

Then one may define the physical correspondence

\[
h_{\rm EDF}^{\rm phys}
=
K_S\mathfrak h_{12},
\]

and

\[
\hbar_{\rm EDF}^{\rm phys}
=
K_S\bar{\mathfrak h}_{12}.
\]

Because

\[
\mathfrak h_{12}
=
2\pi\bar{\mathfrak h}_{12},
\]

the two calibrations are equivalent,

\[
\frac{h}{\mathfrak h_{12}}
=
\frac{\hbar}{\bar{\mathfrak h}_{12}}.
\]

But if \(K_S\) is set by matching the measured Planck constant, that step is a calibration, not a prediction of \(h\).

The repaired theorem is:

**Twelve-Fold Informational Quantization Theorem.** Under DCT plus the EDF Fibonacci-compatibility branch, the fundamental finite closure has \(k=12\), primitive phase increment \(\pi/6\), and recurrence subdivision \(T_*/12\). For a constant two-level marginal entropy \(\ln2\), the phase-integrated cycle divides into the exact dimensionless sector amount \(\mathfrak h_{12}=\pi\ln2/6\) and reduced amount \(\bar{\mathfrak h}_{12}=\ln2/12\). Identification with SI action requires an independent dimensional scale.

This theorem now contains a genuine derivation of twelve. The physical action correspondence remains separate.

---

# 5. Repaired Theorem 4 — 12-Crossing Confinement

The old manuscript chose

\[
\beta
=
(\sigma_1\sigma_2)^6
\]

and then verified that the word has twelve generator events. DCT now supplies the integer twelve before the braid is introduced. The remaining bridge should be stated explicitly.

Assume that the exact \(\mathcal H_3\) factor of the DCT closure is represented by three braid strands and that one primitive twelve-sector event is represented by one positive adjacent-strand braid generator. If the retained positive schedule alternates the two adjacent generators,

\[
g_1=\sigma_1,
\quad
g_2=\sigma_2,
\quad
g_3=\sigma_1,
\quad\ldots,
\]

then twelve events give

\[
\beta
=
\prod_{n=1}^{12}g_n
=
(\sigma_1\sigma_2)^6.
\]

Thus the word length is

\[
\boxed{
|\beta|=12.
}
\]

Let

\[
\Delta
=
\sigma_1\sigma_2\sigma_1
\]

be the Garside half twist in \(B_3\). The braid relation

\[
\sigma_1\sigma_2\sigma_1
=
\sigma_2\sigma_1\sigma_2
\]

gives

\[
\Delta^2
=
(\sigma_1\sigma_2)^3.
\]

For \(B_3\),

\[
\Delta^2
\]

generates the center. Therefore

\[
\beta
=
(\sigma_1\sigma_2)^6
=
(\Delta^2)^2
\]

is central.

The induced permutation of

\[
\sigma_1\sigma_2
\]

is a three-cycle. Hence

\[
(\sigma_1\sigma_2)^6
\]

induces

\[
(123)^6
=
e.
\]

The braid is therefore pure at closure and gives three closed components.

The closure of

\[
(\sigma_1\sigma_2)^q
\]

is the torus link \(T(3,q)\). For

\[
q=6,
\]

we have

\[
T(3,6).
\]

The number of link components is

\[
\gcd(3,6)=3.
\]

The explicit strand tracking in the Entry-14 certificate gives four positive crossings between every pair of components,

\[
N_{12}
=
N_{13}
=
N_{23}
=
4.
\]

For two oriented components, the pairwise linking number is one half the signed crossing sum between those components. Therefore

\[
\operatorname{Lk}(K_1,K_2)
=
2,
\]

\[
\operatorname{Lk}(K_1,K_3)
=
2,
\]

and

\[
\operatorname{Lk}(K_2,K_3)
=
2.
\]

The total pairwise-link invariant used for bookkeeping is

\[
\boxed{
L_{\rm pair}
=
\sum_{a<b}
\operatorname{Lk}(K_a,K_b)
=
6.
}
\]

The repaired theorem is:

**Twelve-Event Central Braid Closure Theorem.** If the EDF three-sector factor is represented by three braid strands and the twelve primitive DCT events are mapped one-to-one to alternating positive adjacent-strand braid generators, the resulting braid is \((\sigma_1\sigma_2)^6=(\Delta^2)^2\). It is central in \(B_3\), closes as \(T(3,6)\), has three components, and has pairwise linking numbers \(2,2,2\), with total pairwise-link sum \(6\).

The word is therefore no longer arbitrary once the braid bridge and alternating-event rule are specified. But neither the braid bridge nor the identification of closed braid topology with QCD color confinement follows from DCT. Kassel and Turaev and Birman provide standard braid-group references.

This change also removes the need for the main article to present a synthetic crossing count as though it were an independent discovery.

---

# 6. Repaired Theorem 5 — Writhe-Bounded Gravity

The current gravity construction contains two exact mathematical quantities after DCT,

\[
C(12)=144,
\]

and, conditional on the repaired braid bridge,

\[
L_{\rm pair}=6.
\]

They are not the same kind of invariant.

For a three-component link

\[
K_1\cup K_2\cup K_3,
\]

the exact quantity computed above is

\[
L_{\rm pair}
=
\operatorname{Lk}(K_1,K_2)
+
\operatorname{Lk}(K_1,K_3)
+
\operatorname{Lk}(K_2,K_3).
\]

By contrast, the Călugăreanu--White--Fuller relation applies to a framed closed curve or ribbon. If \(K\) is the ribbon centerline and \(K_\epsilon\) its framed push-off, then the self-linking number is

\[
\operatorname{SL}(K)
=
\operatorname{Lk}(K,K_\epsilon).
\]

For a sufficiently regular framing,

\[
\boxed{
\operatorname{SL}
=
\operatorname{Tw}
+
\operatorname{Wr}.
}
\]

The writhe of the centerline is

\[
\operatorname{Wr}(K)
=
\frac1{4\pi}
\oint_K
\oint_K
\frac{
(d\mathbf r_1\times d\mathbf r_2)
\cdot
(\mathbf r_1-\mathbf r_2)
}{
\|\mathbf r_1-\mathbf r_2\|^3
}.
\]

The quantity

\[
L_{\rm pair}=6
\]

does not, by itself, imply

\[
\operatorname{SL}=6.
\]

A framing map is required to associate the three-component braid closure with a particular ribbon self-linking number. Likewise, a diagram with twelve positive generator crossings does not imply the geometric bound

\[
|\operatorname{Wr}|\le12
\]

for all spatial embeddings.

This distinction is important enough that the old theorem should not retain the phrase “writhe saturation” as an established DCT consequence.

What does survive exactly is the closure capacity,

\[
\boxed{
C_{12}=144,
}
\]

and the conditional braid invariant,

\[
\boxed{
L_{\rm pair}=6.
}
\]

A gravitational coupling may therefore be parameterized in the general dimensionless form

\[
g_G
=
\mathcal G
\left(
C_{12},
L_{\rm pair},
\operatorname{Wr},
\operatorname{Tw},
\ldots
\right),
\]

but DCT does not determine the function \(\mathcal G\).

If EDF adopts the inverse-capacity ansatz,

\[
g_G
=
\frac{\gamma_G}{C_{12}},
\]

then

\[
g_G
=
\frac{\gamma_G}{144}.
\]

This is an immediate consequence of the ansatz, not a derivation of the ansatz.

For a dimensionful Newton constant,

\[
[G]
=
{\rm m^3\,kg^{-1}\,s^{-2}},
\]

one additionally needs a dimensional scale \(G_*\),

\[
\boxed{
G_{\rm eff}
=
\frac{\gamma_G}{144}G_*.
}
\]

The repaired result is therefore best separated into an exact theorem and a physical hypothesis.

**Closure-Capacity Corollary.**

\[
\boxed{
C_{12}=144.
}
\]

**Topological Closure Corollary.** Under the repaired braid bridge,

\[
\boxed{
L_{\rm pair}=6.
}
\]

**Gravitational Scaling Hypothesis.** If EDF later derives an inverse-capacity coupling and an independent gravitational scale, then

\[
G_{\rm eff}
=
\gamma_G G_*/144.
\]

This is more reliable than calling \(1/144\) itself a first-principles derivation of Newton's constant.

White and Fuller remain the appropriate references for self-linking, twist, and writhe.

---

# 7. Repaired Theorem 6 — Hard UV Cutoff and Finiteness

DCT gives a finite internal algebra,

\[
M_{12}(\mathbb C),
\]

but finite internal dimension does not bound continuum momentum. The earlier working Version 2 already corrected this by stating a conditional compact-support theorem. Entry 14 retains that theorem and adds a softer asymptotic convergence criterion.

Suppose first that every independent Euclidean loop momentum satisfies

\[
\|p_j\|
\le
\Lambda_{\rm EDF}<\infty.
\]

If the regularized integrand is bounded on the compact integration domain, then for one loop,

\[
\left|
\int_{\|p\|\le\Lambda_{\rm EDF}}
d^Dp\,f(p)
\right|
\le
\operatorname{Vol}(B_D)
\Lambda_{\rm EDF}^D
\sup_{\|p\|\le\Lambda_{\rm EDF}}
|f(p)|,
\]

and therefore

\[
\boxed{
|I|<\infty.
}
\]

For finitely many loops, the same argument applies on the finite product of compact domains, provided non-UV singularities are separately controlled. Thus compact spectral support is sufficient for ultraviolet finiteness at every finite loop order.

A hard cutoff is not necessary. Consider instead

\[
I
=
\int_{\mathbb R^D}
d^Dp\,
K_{\rm EDF}(p)^n
F(p).
\]

Assume that for sufficiently large \(\|p\|\),

\[
|F(p)|
\le
C_F
(1+\|p\|)^\sigma,
\]

and

\[
|K_{\rm EDF}(p)|
\le
C_K
(1+\|p\|)^{-\alpha}.
\]

Then

\[
|K_{\rm EDF}(p)^nF(p)|
\le
C
(1+\|p\|)^{\sigma-n\alpha}.
\]

In radial coordinates,

\[
d^Dp
=
\Omega_{D-1}
r^{D-1}dr,
\]

so the asymptotic absolute integral is bounded by a constant times

\[
\int_R^\infty
r^{D-1+\sigma-n\alpha}
dr.
\]

The integral

\[
\int_R^\infty r^q\,dr
\]

converges exactly when

\[
q<-1.
\]

Hence

\[
D-1+\sigma-n\alpha<-1,
\]

which reduces to

\[
\boxed{
n\alpha
>
D+\sigma.
}
\]

At equality,

\[
n\alpha=D+\sigma,
\]

the radial tail behaves logarithmically,

\[
\int_R^\infty\frac{dr}{r},
\]

and diverges. Below the threshold it diverges by a positive power.

The Entry-14 certificate illustrates the criterion in \(D=4\) with \(n=2\) and \(\sigma=0\). For

\[
\alpha=2.5,
\]

the tail converges. For

\[
\alpha=2,
\]

it diverges logarithmically. For

\[
\alpha=1.5,
\]

it diverges linearly.

The repaired theorem is:

**EDF Ultraviolet Convergence Criterion.** A finite DCT internal algebra is not sufficient for ultraviolet finiteness. UV finiteness follows if EDF independently derives either compact spectral support or an asymptotic transfer kernel whose decay makes every graph and divergent subgraph satisfy the appropriate power-counting convergence condition. For the one-scale integral above, the sufficient and sharp radial condition is \(n\alpha>D+\sigma\).

This converts the old “hard cutoff follows from finite closure” claim into a definite mathematical target. EDF must still derive \(K_{\rm EDF}\) or \(\Lambda_{\rm EDF}\) from microscopic dynamics.

Weinberg's high-energy convergence theorem is the classical QFT reference for the necessity of controlling graph and subgraph asymptotics.

---

# 8. Repaired Theorem 7 — Entropic Arrow Hierarchy

The Shannon part of the current Version-2 theorem is already mathematically sound. Let

\[
p=(p_1,\ldots,p_N),
\qquad
\sum_i p_i=1,
\]

and partition the microstates into disjoint groups \(G_a\). Define

\[
q_a
=
\sum_{i\in G_a}
p_i.
\]

Inside each occupied group,

\[
p(i|a)
=
\frac{p_i}{q_a},
\]

so

\[
p_i
=
q_a p(i|a).
\]

The fine-grained entropy is

\[
H(p)
=
-\sum_i p_i\ln p_i.
\]

Substituting the conditional factorization,

\[
H(p)
=
-\sum_a
\sum_{i\in G_a}
q_a p(i|a)
\ln
\left[
q_a p(i|a)
\right].
\]

Expand the logarithm,

\[
\ln[q_ap(i|a)]
=
\ln q_a
+
\ln p(i|a).
\]

Then

\[
H(p)
=
-\sum_a
q_a\ln q_a
\sum_{i\in G_a}p(i|a)
-
\sum_a
q_a
\sum_{i\in G_a}
p(i|a)\ln p(i|a).
\]

Because each conditional distribution is normalized,

\[
\sum_{i\in G_a}p(i|a)=1,
\]

we obtain the Shannon chain rule in grouping form,

\[
\boxed{
H(p)
=
H(q)
+
\sum_a q_aH[p(\cdot|a)].
}
\]

Since

\[
H[p(\cdot|a)]
\ge0,
\]

it follows that

\[
\boxed{
H(q)\le H(p).
}
\]

The inequality is strict exactly when at least one occupied group has nonzero conditional entropy.

Dynamic Closure adds a second exact statement. Suppose the fine dynamical description contains transient states and one such state \(j\) is eliminated. The retained generator and sink become

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

If the original absorption matrix satisfies

\[
QB+R=0,
\]

block elimination gives

\[
Q_{\rm eff}B_A+R_{\rm eff}=0,
\]

and therefore

\[
\boxed{
B_A
=
(-Q_{\rm eff})^{-1}R_{\rm eff}.
}
\]

So explicit state reduction can decrease accessible Shannon information while preserving eliminated-state influence through renormalized effective couplings.

The repaired theorem is:

**Entropy Descent with Dynamical Memory Theorem.** Deterministic EDF aggregation of a probability distribution cannot increase Shannon entropy and decreases it strictly whenever a nontrivial occupied conditional sector is erased. In a coupled absorbing dynamical realization, elimination of transient states need not erase their causal influence: the Schur complement transfers it into effective retained couplings while preserving absorption statistics.

Thus

\[
\boxed{
\text{explicit information loss}
}
\]

and

\[
\boxed{
\text{dynamical memory}
}
\]

can coexist.

The mathematical result does not by itself identify the projection index with thermodynamic time. That physical identification remains an EDF hypothesis.

Cover and Thomas provide the standard information-theory reference; Meyer and Dörfler--Bullo provide established reduced-dynamics precedents.

---

# 9. Additional DCT proposition that should enter Version 2 outside the legacy seven-theorem numbering

The completed notebook also supplies a selection statement that does not belong naturally to only one of the seven older theorem names.

Define

\[
D_k
=
\left|
\ln\frac{F_k}{k^2}
\right|.
\]

Then

\[
D_k\ge0,
\]

and, under the DCT compatibility branch,

\[
D_k=0
\iff
k=12.
\]

Let

\[
w:[0,\infty)\to(0,\infty)
\]

be strictly decreasing and define

\[
\pi_k
=
\frac{w(D_k)}
{\sum_jw(D_j)}.
\]

Since

\[
D_{12}=0
<
D_k
\qquad
(k\ne12),
\]

we have

\[
w(D_{12})
>
w(D_k)
\qquad
(k\ne12),
\]

and therefore

\[
\boxed{
\pi_{12}
>
\pi_k
\qquad
(k\ne12).
}
\]

Thus the theorem-compatible structural preference for \(k=12\) does not depend on the exponential MaxEnt form.

For symmetric adjacency \(A_{jk}=A_{kj}\), let

\[
g_k=w(D_k)
\]

and define

\[
W_{j\to k}
=
\nu A_{jk}
\sqrt{\frac{g_k}{g_j}}.
\]

With

\[
\pi_k=\frac{g_k}{Z},
\]

we obtain

\[
\pi_jW_{j\to k}
=
\frac{\nu A_{jk}}{Z}
\sqrt{g_jg_k}
=
\pi_kW_{k\to j}.
\]

Hence

\[
\boxed{
\pi_jW_{j\to k}
=
\pi_kW_{k\to j}.
}
\]

The stationary structural preference and the pathway topology are therefore separable: the defect weights determine the stationary law, while adjacency determines relaxation pathways and timescales.

Environmental noise or loss terms can modify those pathways without changing the exact DCT zero unless they alter the structural premises themselves.

This proposition is one of the most useful bridges between the exact DCT theorem and the physical literature on metastable selection.

---

# 10. Revised seven-theorem dependency structure

After Entry 14, the seven-theorem ledger should no longer be understood as seven claims of equal epistemic strength.

The first theorem now has a mathematically developed nonlinear-dispersive representative and a new DCT reason for retaining effective residues after projection, but the continuum field equation remains to be derived.

The second theorem is substantially repaired. Triplication is no longer represented primarily by vector concatenation or only by an invariant group average. The exact DCT factorization

\[
\mathcal H_{12}
\cong
\mathcal H_3\otimes\mathcal H_4
\]

provides a genuine three-dimensional internal factor, three orthogonal character projectors, and a norm-preserving triplication isometry.

The third theorem is fundamentally strengthened. Twelve is no longer inserted as a kernel hypothesis. It follows from

\[
C(k)=k^2
\]

together with the EDF Fibonacci-compatible closure condition.

The fourth theorem is also strengthened mathematically. Once the explicit braid bridge is declared, the twelve-event alternating word follows and has a precise central \(B_3\), \(T(3,6)\), and pairwise-linking structure.

The fifth theorem undergoes the strongest correction of interpretation. The exact outputs are

\[
C_{12}=144
\]

and, conditionally,

\[
L_{\rm pair}=6.
\]

Neither is automatically a ribbon self-linking number or a gravitational coupling. The old writhe bound and inverse-capacity gravity law remain hypotheses unless separately derived.

The sixth theorem is repaired from an unsupported implication into an exact convergence criterion. Finite internal closure is insufficient; compact support or adequate high-momentum suppression is sufficient.

The seventh theorem becomes stronger conceptually: entropy reduction and dynamical memory are not contradictory. The former follows from the Shannon chain rule; the latter follows from exact Schur reduction.

The v2 manuscript can therefore present mature theorems rather than a PASS/FAIL audit. The repository can preserve the historical theorem-repair ledger.

---

# 11. What should be changed in the current Version-2 source

The current working source says that twelve is treated as a kernel-selection hypothesis whose consequences are then derived. That sentence is now obsolete and should be replaced by the DCT derivation.

The current triplication section should replace the single invariant group average as the principal triplication mechanism by the three Fourier-character projectors

\[
\Pi_0,\Pi_1,\Pi_2
\]

and the exact CRT factorization

\[
\mathcal H_{12}
\cong
\mathcal H_3\otimes\mathcal H_4.
\]

The earlier numerical operation

\[
A\oplus A\oplus A
\]

should remain, if at all, only as a simple implementation illustration of the exact isometric three-branch structure.

The braid section should say that \((\sigma_1\sigma_2)^6\) follows only after the explicit three-strand/event-map assumptions are stated. It should use the exact invariants

\[
T(3,6),
\qquad
\operatorname{Lk}_{12}
=
\operatorname{Lk}_{13}
=
\operatorname{Lk}_{23}
=
2,
\]

and

\[
L_{\rm pair}=6.
\]

The gravity section should no longer substitute this \(L_{\rm pair}\) directly into a Călugăreanu self-linking identity unless a ribbon framing is independently defined. The former software writhe proxy should be kept only in the repository as historical diagnostic material.

The UV section should retain the current compact-support theorem but add the asymptotic-decay criterion, which gives EDF a mathematically meaningful target even if the eventual regulator is soft rather than hard.

The entropy section should retain its chain-rule proof and add the boundary-memory proposition, preferably after the main entropy equation rather than as a separate visual block.

The main article should not contain the old PASS dashboard as a central validation figure. It belongs in the repository history.

---

# 12. Bibliography for the repaired theorem set

1. Y. Bugeaud, M. Mignotte, and S. Siksek, “Classical and modular approaches to exponential Diophantine equations I. Fibonacci and Lucas perfect powers,” *Annals of Mathematics* **163**, 969–1018 (2006). DOI: 10.4007/annals.2006.163.969.

2. M. A. Marchiolli and P. E. M. F. Mendonça, “Theoretical formulation of finite-dimensional discrete phase spaces: II. On the uncertainty principle for Schwinger unitary operators,” *Annals of Physics* **336**, 76–97 (2013). DOI: 10.1016/j.aop.2013.05.009.

3. R. A. Bertlmann and P. Krammer, “Bloch vectors for qudits,” *Journal of Physics A: Mathematical and Theoretical* **41**, 235303 (2008). DOI: 10.1088/1751-8113/41/23/235303; arXiv:0806.1174.

4. A. Vourdas, “Quantum systems with finite Hilbert space,” *Reports on Progress in Physics* **67**, 267–320 (2004). DOI: 10.1088/0034-4885/67/3/R03. In particular, this review discusses Heisenberg–Weyl methods and Chinese-remainder factorization of finite systems.

5. A. Vourdas, “Factorization in finite quantum systems,” *Journal of Physics A: Mathematical and General* **36**, 5645 (2003). DOI: 10.1088/0305-4470/36/20/319.

6. J.-P. Serre, *Linear Representations of Finite Groups*, Graduate Texts in Mathematics 42, Springer (1977). DOI: 10.1007/978-1-4684-9458-7.

7. A. B. Hopkins, F. H. Stillinger, and S. Torquato, “Spherical codes, maximal local packing density, and the golden ratio,” arXiv:1003.3604 (2010). This reference is used as a geometric optimization precedent for golden-ratio structure, not as a derivation of EDF Fibonacci compatibility.

8. P. G. Drazin and R. S. Johnson, *Solitons: An Introduction*, Cambridge Texts in Applied Mathematics, Cambridge University Press (1989; online 2012). DOI: 10.1017/CBO9781139172059.

9. J. S. Birman, *Braids, Links, and Mapping Class Groups*, Annals of Mathematics Studies 82, Princeton University Press (1974; digital edition DOI: 10.1515/9781400881420).

10. C. Kassel and V. Turaev, *Braid Groups*, Graduate Texts in Mathematics 247, Springer (2008). DOI: 10.1007/978-0-387-68548-9.

11. J. H. White, “Self-Linking and the Gauss Integral in Higher Dimensions,” *American Journal of Mathematics* **91**, 693–728 (1969). DOI: 10.2307/2373348.

12. F. B. Fuller, “The Writhing Number of a Space Curve,” *Proceedings of the National Academy of Sciences USA* **68**, 815–819 (1971). DOI: 10.1073/pnas.68.4.815.

13. S. Weinberg, “High-Energy Behavior in Quantum Field Theory,” *Physical Review* **118**, 838–849 (1960). DOI: 10.1103/PhysRev.118.838.

14. T. M. Cover and J. A. Thomas, *Elements of Information Theory*, 2nd ed., Wiley (2006). DOI: 10.1002/047174882X.

15. C. D. Meyer, “Stochastic Complementation, Uncoupling Markov Chains, and the Theory of Nearly Reducible Systems,” *SIAM Review* **31**, 240–272 (1989). DOI: 10.1137/1031050.

16. F. Dörfler and F. Bullo, “Kron Reduction of Graphs with Applications to Electrical Networks,” *IEEE Transactions on Circuits and Systems I* **60**, 150–163 (2013). DOI: 10.1109/TCSI.2012.2215780.

17. E. T. Jaynes, “Information Theory and Statistical Mechanics,” *Physical Review* **106**, 620–630 (1957). DOI: 10.1103/PhysRev.106.620.

18. G. Falasco and M. Esposito, “Local detailed balance across scales: From diffusions to jump processes and beyond,” *Physical Review E* **103**, 042114 (2021). DOI: 10.1103/PhysRevE.103.042114.

The external metastability, order-by-disorder, quasicrystal-pathway, and entropy-stabilization bibliography gathered in the DCT consolidation remains relevant to the later physical-discussion section, but those references are not needed to prove the repaired mathematical theorems above.

---

# 13. Entry-14 conclusion

The main result of Entry 14 is not that all seven old theorems have been proved in their original physical interpretation. It is that the mature EDF theorem set is now substantially stronger and cleaner than the earlier pipeline formulation.

The completed DCT work replaces the assumed \(\mathbb Z_{12}\) kernel by a conditional derivation,

\[
\boxed{
C(k)=k^2,
\qquad
F_k=C(k),
\qquad
k=12.
}
\]

It replaces numerical triplication by the exact internal factorization

\[
\boxed{
\mathcal H_{12}
\cong
\mathcal H_3\otimes\mathcal H_4
}
\]

and the three orthogonal projectors

\[
\boxed{
\Pi_0,\Pi_1,\Pi_2.
}
\]

It replaces a merely imposed twelve-crossing count by the conditional but exact central braid structure

\[
\boxed{
(\sigma_1\sigma_2)^6
=
(\Delta^2)^2
}
\]

with

\[
\boxed{
T(3,6),
\qquad
L_{\rm pair}=6.
}
\]

It separates that pairwise-link invariant from ribbon self-linking and therefore removes an unjustified writhe identification from the gravity argument.

It replaces “finite internal dimension implies UV finiteness” by the actual convergence alternatives

\[
\boxed{
\|p\|\le\Lambda_{\rm EDF}
}
\]

or, for the model tail developed here,

\[
\boxed{
n\alpha>D+\sigma.
}
\]

Finally, it combines

\[
\boxed{
H(q)\le H(p)
}
\]

with

\[
\boxed{
B_A=(-Q_{\rm eff})^{-1}R_{\rm eff}
}
\]

to show rigorously that explicit information reduction can coexist with retained dynamical memory.

These are the versions that should be carried into the Version-2 manuscript. The remaining physical identifications—fermion generations, QCD confinement, gravitational coupling, microscopic UV regulator, and the physical time interpretation of entropy descent—should be presented as the next predictive layer rather than being mixed into the mathematical proofs.
