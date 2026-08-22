# EDF Dynamic Closure — Version 2

This repository is the mathematical and computational companion to the Version-2 manuscript:

**The Entropic Dimensional Framework: Dynamic Matrix Closure, Twelve-Fold Compatibility, and Transient Boundary Memory**

It preserves the Dynamic Closure Notebook (Entries 01–16), including null controls, exploratory residuals, local/noisy pathway dynamics, operator-algebra certificates, premise audits, theorem repairs, robustness tests, and the theorem-led Version-2 manuscript.

## Central theorem chain

The mature closure result is

\[
\text{resolved finite phase}
\rightarrow
\text{primitive transitive traversal}
\rightarrow
M_k(\mathbb C)
\rightarrow
C(k)=k^2.
\]

EDF then applies the separately stated **Fibonacci Compatibility Condition**

\[
F_k=C(k),
\]

so

\[
F_k=k^2,
\]

whose unique nontrivial solution for \(k\ge2\) is

\[
\boxed{k=12}.
\]

The notebook also derives the exact nonprimitive subclosure formula

\[
\operatorname{alg}(Z,X^r)
\cong
\bigoplus_{\alpha=1}^{d}M_{k/d}(\mathbb C),
\qquad
d=\gcd(k,r),
\]

with

\[
C_r(k)=\frac{k^2}{d}.
\]

For \(k=12\), the exact accessible capacities are

\[
12,\;24,\;36,\;48,\;72,\;144.
\]

## Why this repository exists

The paper is theorem-led and does not reproduce the notebook chronology. This repository carries the full audit trail:

- neutral stochastic control showing that environmental noise does not manufacture \(k=12\);
- candidate closure dynamics and local-pathway robustness;
- alternative structural counts and countermodels;
- finite Weyl/matrix closure certificates;
- primitive and nonprimitive traversal tests;
- defect and detailed-balance selection models;
- absorbing-state residence, intervention, and Schur-memory analysis;
- robustness and falsification tests;
- repaired EDF theorem-to-prediction correspondence;
- premise-minimality and exact subclosure algebra;
- the complete Version-2 manuscript source.

Failed stronger formulations are retained rather than silently removed.

## Notebook map

| Entry | Main role |
|---|---|
| 01 | Null stochastic dynamics |
| 02 | Candidate Fibonacci pair-closure functional |
| 03 | Local pathway and environmental robustness |
| 04 | Pair-space derivation and arithmetic uniqueness |
| 05 | Weyl-generated closure algebra |
| 06 | Phase and traversal generators |
| 07 | Primitive phase evolution |
| 08 | Dynamic Closure Theorem consolidation |
| 09 | Closure defect and selection functional |
| 10 | Transient-state causality and boundary memory |
| 11 | Robustness and falsification |
| 12 | Alternative-structure premise audit |
| 13 | EDF theorem-prediction correspondence |
| 14 | Theorem repair and prediction reconstruction |
| 15 | Repository/manuscript consolidation |
| 16 | Premise minimality and exact subclosure algebra |

## Scientific status

The repository deliberately separates exact/conditional mathematics from EDF-to-physics identifications. In particular:

- the exact \(\mathbb Z_3\) factor does not yet derive the observed fermion generations;
- the conditional braid closure does not yet derive QCD confinement;
- \(C(12)=144\) does not by itself derive Newton's constant;
- finite internal dimension does not by itself imply ultraviolet finiteness;
- Shannon entropy descent does not by itself identify the projection hierarchy with physical time.

These are stated limitations of the present framework, not hidden assumptions.

## Key external mathematical references

The closure construction uses standard finite Weyl/Schwinger operator theory and the Fibonacci perfect-power theorem of Bugeaud, Mignotte, and Siksek. The geometric-optimization discussion also cites A. B. Hopkins, F. H. Stillinger, and S. Torquato, arXiv:1003.3604, as a precedent for golden-ratio structure arising in an extremal packing problem; it is not used as a derivation of the EDF Fibonacci Compatibility Condition.

## Reproducibility

See [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) and [`docs/CLAIM_STATUS.md`](docs/CLAIM_STATUS.md).

## Manuscript

The theorem-led Version-2 LaTeX manuscript is maintained under `manuscript/`.

## Citation

Please cite the Version-2 manuscript and this repository together when using the Dynamic Closure derivations or computational certificates. Citation metadata are provided in `CITATION.cff`.

## License

No open-source license is imposed in this repository at present. Until the author chooses a license, ordinary copyright restrictions apply.
