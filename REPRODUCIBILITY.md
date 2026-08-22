# Reproducibility Guide

The Dynamic Closure Notebook is organized as a sequence of independent Python entries. Analytic proofs in the manuscript are authoritative; the scripts provide implementation certificates, countermodels, robustness tests, and the complete discovery history.

## Reference environment

- Python 3.11+
- NumPy
- pandas
- Matplotlib
- SciPy (required by the absorbing-chain finite-time checks in Entry 10)

Install the reference dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Fast exact certificates

The most compact final certificates are:

```bash
python notebook/entry_14/dynamic_closure_notebook_entry_14.py
python notebook/entry_16/dynamic_closure_notebook_entry_16.py
```

Entry 14 checks the CRT factorization, the three orthogonal Z3 character projectors, the norm-preserving triplication isometry, twelve-event braid bookkeeping, pairwise linking, and representative UV power counting.

Entry 16 checks the minimal simple-spectrum/transitive-cycle closure, exact nonprimitive subclosure dimensions, and explicit countermodels obtained by removing phase resolution, traversal, or multiplicative closure.

## Core Dynamic Closure certificate

```bash
python notebook/entry_08/dynamic_closure_notebook_entry_08.py
```

This verifies the exact traversal arithmetic, Euler-totient count of primitive generators, numerical Weyl span, and the Fibonacci-square scan implementing the published perfect-power classification.

## Environmental and robustness calculations

Entries 01–03 and 09–11 are model-dependent dynamical tests.

- Entry 01: unbiased stochastic null model.
- Entry 02: candidate Fibonacci pair-closure score and controls.
- Entry 03: local-pathway/noise robustness.
- Entry 09: defect representations, MaxEnt weighting, and detailed balance.
- Entry 10: absorbing dynamics, transient residence, interventions, and Schur boundary footprints.
- Entry 11: broad robustness/falsification suite.

Failure of one chosen kinetic realization does not alter the algebraic DCT theorem; the notebook therefore labels structural mathematics and dynamical model choices separately.

## Manuscript compilation

From the `manuscript/` directory:

```bash
pdflatex -interaction=nonstopmode EDF_V2_Complete_Dynamic_Closure.tex
pdflatex -interaction=nonstopmode EDF_V2_Complete_Dynamic_Closure.tex
```

## Interpretation rule

Where an analytic proof exists, the proof is the scientific claim. Numerical certificates are used to detect counterexamples, verify implementations, test robustness, and preserve the unbiased discovery path.
