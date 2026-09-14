"""
Dynamic Closure Notebook — Entry 16
Premise Minimality, Independence, and Subclosure Algebra Certificate

This script verifies:
1. A simple-spectrum sector resolver plus a transitive k-cycle generates M_k(C).
2. For nonprimitive U_r = X^r,
       alg(Z, U_r) ~= direct sum_{j=1}^{d} M_{k/d}(C),
   where d = gcd(k,r), hence
       dim alg(Z,U_r) = k^2/d.
3. Removing phase resolution, traversal, or multiplicative closure gives
   explicit lower-dimensional countermodels.
4. At k=12, every step r is classified by orbit length, block number,
   and exact generated-algebra dimension.
"""

import math
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path("/mnt/data/dynamic_closure_entry_16_output")
OUT.mkdir(parents=True, exist_ok=True)

TOL = 1e-10


def shift(k: int) -> np.ndarray:
    X = np.zeros((k, k), dtype=complex)
    for m in range(k):
        X[(m + 1) % k, m] = 1.0
    return X


def clock(k: int) -> np.ndarray:
    omega = np.exp(2j * np.pi / k)
    return np.diag([omega**m for m in range(k)])


def matrix_family_rank(mats) -> int:
    M = np.column_stack([A.reshape(-1) for A in mats])
    return int(np.linalg.matrix_rank(M, tol=TOL))


def generated_weyl_family(k: int, r: int):
    X = shift(k)
    Z = clock(k)
    U = np.linalg.matrix_power(X, r)
    mats = []
    for a in range(k):
        Ua = np.linalg.matrix_power(U, a)
        for b in range(k):
            mats.append(Ua @ np.linalg.matrix_power(Z, b))
    return mats


def nonprimitive_dimension_scan(max_k=24):
    rows = []
    for k in range(2, max_k + 1):
        for r in range(k):
            d = math.gcd(k, r)
            if r == 0:
                d = k
            ell = k // d
            rank = matrix_family_rank(generated_weyl_family(k, r))
            predicted = k * k // d
            rows.append({
                "k": k,
                "r": r,
                "gcd_k_r": d,
                "number_orbits": d,
                "orbit_length": ell,
                "predicted_dimension": predicted,
                "computed_dimension": rank,
                "formula_verified": rank == predicted,
            })
    return pd.DataFrame(rows)


def simple_spectrum_cycle_scan(max_k=12):
    rows = []
    for k in range(2, max_k + 1):
        # Generic distinct spectrum, deliberately not roots of unity.
        lambdas = np.array(
            [1.3 + 0.37*m + 0.05j*(m+1)**2 for m in range(k)],
            dtype=complex
        )
        D = np.diag(lambdas)
        S = shift(k)

        # {S^a D^b : 0<=a,b<k}. Distinct eigenvalues make the
        # Vandermonde diagonal powers span all diagonal matrix units.
        mats = []
        for a in range(k):
            Sa = np.linalg.matrix_power(S, a)
            for b in range(k):
                mats.append(Sa @ np.linalg.matrix_power(D, b))
        rank = matrix_family_rank(mats)

        rows.append({
            "k": k,
            "spectrum_distinct": len(np.unique(lambdas)) == k,
            "computed_rank": rank,
            "expected_rank": k*k,
            "full_matrix_algebra_rank": rank == k*k,
        })
    return pd.DataFrame(rows)


def linear_nonmultiplicative_span_rank(k: int) -> int:
    X = shift(k)
    Z = clock(k)

    # Smallest obvious linear span containing both cyclic one-generator
    # algebras, but not their mixed products.
    mats = [np.eye(k, dtype=complex)]
    mats += [np.linalg.matrix_power(X, a) for a in range(1, k)]
    mats += [np.linalg.matrix_power(Z, b) for b in range(1, k)]
    return matrix_family_rank(mats)


def countermodels(max_k=12):
    rows = []
    for k in range(2, max_k + 1):
        X = shift(k)
        Z = clock(k)

        shift_only = matrix_family_rank(
            [np.linalg.matrix_power(X, a) for a in range(k)]
        )
        phase_only = matrix_family_rank(
            [np.linalg.matrix_power(Z, b) for b in range(k)]
        )
        linear_span = linear_nonmultiplicative_span_rank(k)

        # Degenerate resolver D=I plus transitive shift.
        degenerate_resolver = shift_only

        rows.append({
            "k": k,
            "phase_only_dim": phase_only,
            "shift_only_dim": shift_only,
            "degenerate_resolver_plus_shift_dim": degenerate_resolver,
            "nonmultiplicative_union_span_dim": linear_span,
            "expected_nonmultiplicative_dim": 2*k - 1,
            "full_dim": k*k,
        })
    return pd.DataFrame(rows)


def k12_table():
    k = 12
    scan = nonprimitive_dimension_scan(max_k=12)
    scan = scan[scan["k"] == 12].copy()
    scan["primitive"] = scan["gcd_k_r"] == 1
    return scan[
        [
            "r",
            "gcd_k_r",
            "number_orbits",
            "orbit_length",
            "computed_dimension",
            "primitive",
        ]
    ].reset_index(drop=True)


def main():
    nonprim = nonprimitive_dimension_scan()
    nonprim.to_csv(
        OUT / "nonprimitive_subclosure_dimension_scan.csv", index=False
    )

    simple = simple_spectrum_cycle_scan()
    simple.to_csv(
        OUT / "simple_spectrum_transitive_cycle_scan.csv", index=False
    )

    counters = countermodels()
    counters.to_csv(
        OUT / "premise_countermodels.csv", index=False
    )

    k12 = k12_table()
    k12.to_csv(
        OUT / "k12_step_algebra_classification.csv", index=False
    )

    summary = pd.DataFrame([{
        "nonprimitive_formula_all_verified":
            bool(nonprim["formula_verified"].all()),
        "simple_spectrum_full_rank_all_verified":
            bool(simple["full_matrix_algebra_rank"].all()),
        "nonmultiplicative_span_formula_all_verified":
            bool(
                np.all(
                    counters["nonmultiplicative_union_span_dim"]
                    == counters["expected_nonmultiplicative_dim"]
                )
            ),
        "max_k_nonprimitive_scan": int(nonprim["k"].max()),
        "max_k_simple_spectrum_scan": int(simple["k"].max()),
    }])
    summary.to_csv(OUT / "entry16_summary.csv", index=False)

    print("ENTRY 16 — PREMISE MINIMALITY CERTIFICATE")
    print("----------------------------------------")
    print(summary.to_string(index=False))
    print()
    print("k=12 step classification:")
    print(k12.to_string(index=False))
    print()
    print("Representative countermodels:")
    print(counters.head(8).to_string(index=False))


if __name__ == "__main__":
    main()
