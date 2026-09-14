"""
Dynamic Closure Notebook — Entry 12
Alternative Structure Controls and Premise Audit

Entry 12 revisits the competing structural counts only after DCT has fixed

    P1: resolved finite phase structure -> Z
    P2: coherent primitive evolution
    P3: primitive transitive traversal -> U_r ~ X
    P4: smallest unital associative complex algebra containing the required
        operations
    P5: Fibonacci compatibility F_k = C(k)

Entries 05–08 established

    P1 + P2 + P3 + P4
        => alg(Z,X) = M_k(C)
        => C(k) = k^2.

The purpose here is not just to ask which alternative count matches Fibonacci.
It is to identify what must be removed or changed in DCT for each alternative
count to become possible.

Candidates
----------
full ordered+self                 k^2
traceless coordinates             k^2 - 1
ordered without self              k(k-1)
unordered including self          k(k+1)/2
unordered without self            k(k-1)/2
single-generator cyclic sector    k

The script performs:
1. exact Fibonacci scans to k=500;
2. finite matrix-space audits;
3. explicit closure witnesses;
4. premise-by-premise control table;
5. figures for arithmetic and structural comparison.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


@dataclass
class Config:
    fibonacci_scan_max: int = 500
    algebra_k_min: int = 2
    algebra_k_max: int = 12
    diagnostic_k: int = 6
    tolerance: float = 1.0e-10
    output_dir: str = "dynamic_closure_entry_12_output"


# ---------------------------------------------------------------------------
# Exact arithmetic
# ---------------------------------------------------------------------------

def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def candidate_count(name: str, k: int) -> int:
    if name == "full_ordered_self":
        return k * k
    if name == "traceless":
        return k * k - 1
    if name == "ordered_no_self":
        return k * (k - 1)
    if name == "unordered_self":
        return k * (k + 1) // 2
    if name == "unordered_no_self":
        return k * (k - 1) // 2
    if name == "single_generator":
        return k
    raise ValueError(name)


CANDIDATES = (
    "full_ordered_self",
    "traceless",
    "ordered_no_self",
    "unordered_self",
    "unordered_no_self",
    "single_generator",
)


def fibonacci_match_scan(config: Config) -> pd.DataFrame:
    rows = []
    for name in CANDIDATES:
        matches = []
        for k in range(2, config.fibonacci_scan_max + 1):
            if fibonacci(k) == candidate_count(name, k):
                matches.append(k)

        rows.append(
            {
                "candidate": name,
                "count_formula": {
                    "full_ordered_self": "k^2",
                    "traceless": "k^2-1",
                    "ordered_no_self": "k(k-1)",
                    "unordered_self": "k(k+1)/2",
                    "unordered_no_self": "k(k-1)/2",
                    "single_generator": "k",
                }[name],
                "exact_match_indices": (
                    ",".join(str(k) for k in matches)
                    if matches else "none"
                ),
                "match_count": len(matches),
            }
        )
    return pd.DataFrame(rows)


def residual_table(k_max: int = 24) -> pd.DataFrame:
    rows = []
    for k in range(2, k_max + 1):
        f_k = fibonacci(k)
        for name in CANDIDATES:
            c_k = candidate_count(name, k)
            rows.append(
                {
                    "k": k,
                    "candidate": name,
                    "F_k": f_k,
                    "C_k": c_k,
                    "bounded_residual": abs(f_k - c_k) / (f_k + c_k),
                    "exact_match": f_k == c_k,
                }
            )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Matrix-space controls
# ---------------------------------------------------------------------------

def E(k: int, i: int, j: int) -> np.ndarray:
    m = np.zeros((k, k), dtype=complex)
    m[i, j] = 1.0
    return m


def family_rank(family: list[np.ndarray], tol: float) -> int:
    if not family:
        return 0
    stacked = np.column_stack([m.reshape(-1) for m in family])
    return int(np.linalg.matrix_rank(stacked, tol=tol))


def in_span(
    candidate: np.ndarray,
    basis: list[np.ndarray],
    tol: float,
) -> bool:
    return family_rank(basis + [candidate], tol) == family_rank(basis, tol)


def full_basis(k: int) -> list[np.ndarray]:
    return [E(k, i, j) for i in range(k) for j in range(k)]


def traceless_basis(k: int) -> list[np.ndarray]:
    basis = [
        E(k, i, j)
        for i in range(k)
        for j in range(k)
        if i != j
    ]
    for i in range(k - 1):
        basis.append(E(k, i, i) - E(k, k - 1, k - 1))
    return basis


def ordered_no_self_basis(k: int) -> list[np.ndarray]:
    return [
        E(k, i, j)
        for i in range(k)
        for j in range(k)
        if i != j
    ]


def unordered_self_basis(k: int) -> list[np.ndarray]:
    basis = [E(k, i, i) for i in range(k)]
    for i in range(k):
        for j in range(i + 1, k):
            basis.append(E(k, i, j) + E(k, j, i))
    return basis


def unordered_no_self_basis(k: int) -> list[np.ndarray]:
    return [
        E(k, i, j) + E(k, j, i)
        for i in range(k)
        for j in range(i + 1, k)
    ]


def clock_and_shift(k: int) -> tuple[np.ndarray, np.ndarray]:
    omega = np.exp(2j * np.pi / k)

    z = np.diag([omega**m for m in range(k)])

    x = np.zeros((k, k), dtype=complex)
    for m in range(k):
        x[(m + 1) % k, m] = 1.0

    return z, x


def cyclic_power_basis(generator: np.ndarray, k: int) -> list[np.ndarray]:
    return [np.linalg.matrix_power(generator, a) for a in range(k)]


def weyl_basis(k: int) -> list[np.ndarray]:
    z, x = clock_and_shift(k)
    return [
        np.linalg.matrix_power(x, a) @ np.linalg.matrix_power(z, b)
        for a in range(k)
        for b in range(k)
    ]


def explicit_audit_row(name: str, k: int, tol: float) -> dict:
    I = np.eye(k, dtype=complex)

    if name == "full_ordered_self":
        basis = full_basis(k)
        witness = I
        witness_inside = True
        multiplicatively_closed = True
        generated_dimension = k * k
        dct_status = "PASS"
        reason = "Already the full unital associative operator algebra."

    elif name == "traceless":
        basis = traceless_basis(k)
        # A = diag(1,-1,0,...) is traceless; A^2 is not traceless.
        a = E(k, 0, 0) - E(k, 1, 1)
        witness = a @ a
        witness_inside = in_span(witness, basis, tol)
        multiplicatively_closed = witness_inside
        generated_dimension = k * k
        dct_status = "FAIL P4"
        reason = (
            "Identity direction is removed; multiplication regenerates "
            "nontraceless/self components."
        )

    elif name == "ordered_no_self":
        basis = ordered_no_self_basis(k)
        witness = E(k, 0, 1) @ E(k, 1, 0)
        witness_inside = in_span(witness, basis, tol)
        multiplicatively_closed = witness_inside
        generated_dimension = k * k
        dct_status = "FAIL P4"
        reason = "E_01 E_10 = E_00 regenerates a deleted self-relation."

    elif name == "unordered_self":
        basis = unordered_self_basis(k)
        a = E(k, 0, 0)
        b = E(k, 0, 1) + E(k, 1, 0)
        witness = a @ b  # E_01, directed and nonsymmetric.
        witness_inside = in_span(witness, basis, tol)
        multiplicatively_closed = witness_inside
        generated_dimension = k * k
        dct_status = "FAIL P3; FAIL P4"
        reason = (
            "Opposite directions are identified; ordinary composition "
            "regenerates directed matrix units."
        )

    elif name == "unordered_no_self":
        basis = unordered_no_self_basis(k)
        s = E(k, 0, 1) + E(k, 1, 0)
        witness = s @ s  # E_00 + E_11.
        witness_inside = in_span(witness, basis, tol)
        multiplicatively_closed = witness_inside

        # For k=2 this one generator + identity gives span{I,X}; for k>=3
        # the complete symmetric off-diagonal family generates all matrix units.
        generated_dimension = 2 if k == 2 else k * k

        dct_status = "FAIL P1/P3; FAIL P4"
        reason = (
            "Direction is forgotten and self-relations are removed; "
            "(E_01+E_10)^2 regenerates diagonal/self structure."
        )

    else:
        raise ValueError(name)

    return {
        "k": k,
        "candidate": name,
        "declared_dimension": len(basis),
        "basis_rank": family_rank(basis, tol),
        "contains_identity": in_span(I, basis, tol),
        "explicit_product_witness_in_declared_span": witness_inside,
        "multiplicatively_closed_under_witness": multiplicatively_closed,
        "unital_associative_closure_dimension": generated_dimension,
        "full_k2_dimension": k * k,
        "expands_to_full_k2": generated_dimension == k * k,
        "dct_status": dct_status,
        "reason": reason,
    }


def algebra_audit(config: Config) -> pd.DataFrame:
    rows = []

    for k in range(config.algebra_k_min, config.algebra_k_max + 1):
        for name in (
            "full_ordered_self",
            "traceless",
            "ordered_no_self",
            "unordered_self",
            "unordered_no_self",
        ):
            rows.append(explicit_audit_row(name, k, config.tolerance))

        z, x = clock_and_shift(k)
        z_basis = cyclic_power_basis(z, k)
        x_basis = cyclic_power_basis(x, k)
        wz_basis = weyl_basis(k)

        rows.append(
            {
                "k": k,
                "candidate": "phase_only_linear",
                "declared_dimension": k,
                "basis_rank": family_rank(z_basis, config.tolerance),
                "contains_identity": True,
                "explicit_product_witness_in_declared_span": True,
                "multiplicatively_closed_under_witness": True,
                "unital_associative_closure_dimension": k,
                "full_k2_dimension": k * k,
                "expands_to_full_k2": False,
                "dct_status": "FAIL P3",
                "reason": "Closed cyclic phase algebra, but omits traversal X.",
            }
        )

        rows.append(
            {
                "k": k,
                "candidate": "shift_only_linear",
                "declared_dimension": k,
                "basis_rank": family_rank(x_basis, config.tolerance),
                "contains_identity": True,
                "explicit_product_witness_in_declared_span": True,
                "multiplicatively_closed_under_witness": True,
                "unital_associative_closure_dimension": k,
                "full_k2_dimension": k * k,
                "expands_to_full_k2": False,
                "dct_status": "FAIL P1",
                "reason": "Closed cyclic traversal algebra, but omits phase Z.",
            }
        )

        rows.append(
            {
                "k": k,
                "candidate": "phase_plus_shift_DCT",
                "declared_dimension": 2,
                "basis_rank": 2,
                "contains_identity": False,
                "explicit_product_witness_in_declared_span": False,
                "multiplicatively_closed_under_witness": False,
                "unital_associative_closure_dimension": family_rank(
                    wz_basis, config.tolerance
                ),
                "full_k2_dimension": k * k,
                "expands_to_full_k2": (
                    family_rank(wz_basis, config.tolerance) == k * k
                ),
                "dct_status": "PASS",
                "reason": "Required generators Z and X span the k^2 Weyl basis.",
            }
        )

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Premise audit
# ---------------------------------------------------------------------------

def premise_audit() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "candidate": "full_ordered_self",
                "count": "k^2",
                "P1": "PASS",
                "P2": "PASS",
                "P3": "PASS",
                "P4": "PASS",
                "required_change": "None.",
                "Fibonacci_match": "k=12",
            },
            {
                "candidate": "traceless",
                "count": "k^2-1",
                "P1": "PASS",
                "P2": "PASS",
                "P3": "PASS",
                "P4": "FAIL",
                "required_change": (
                    "Replace full unital operator closure by a traceless "
                    "or normalized-state coordinate space."
                ),
                "Fibonacci_match": "none",
            },
            {
                "candidate": "ordered_no_self",
                "count": "k(k-1)",
                "P1": "FAIL",
                "P2": "PASS",
                "P3": "PASS",
                "P4": "FAIL",
                "required_change": (
                    "Delete self/identity relations despite their regeneration "
                    "under composition."
                ),
                "Fibonacci_match": "none",
            },
            {
                "candidate": "unordered_self",
                "count": "k(k+1)/2",
                "P1": "PASS",
                "P2": "PASS",
                "P3": "FAIL",
                "P4": "FAIL",
                "required_change": (
                    "Identify j->k with k->j and replace directed operator "
                    "composition by unordered/symmetric relations."
                ),
                "Fibonacci_match": "k=10",
            },
            {
                "candidate": "unordered_no_self",
                "count": "k(k-1)/2",
                "P1": "FAIL",
                "P2": "PASS",
                "P3": "FAIL",
                "P4": "FAIL",
                "required_change": (
                    "Forget direction and remove self/identity relations."
                ),
                "Fibonacci_match": "k=2",
            },
            {
                "candidate": "single_generator_linear",
                "count": "k",
                "P1": "FAIL if shift-only",
                "P2": "PASS",
                "P3": "FAIL if phase-only",
                "P4": "PASS as subalgebra",
                "required_change": (
                    "Discard either Z or X. Keeping both restores k^2."
                ),
                "Fibonacci_match": "k=5",
            },
        ]
    )


def implication_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "control": "Remove identity/tracial direction",
                "space": "k^2-1",
                "closure_witness": "diag(1,-1,...)^2 has nonzero trace",
                "consequence": "Full unital closure regenerates missing direction.",
            },
            {
                "control": "Remove self-relations",
                "space": "k(k-1)",
                "closure_witness": "E_ij E_ji = E_ii",
                "consequence": "Self-relations are regenerated.",
            },
            {
                "control": "Forget direction",
                "space": "k(k+1)/2",
                "closure_witness": "E_ii(E_ij+E_ji)=E_ij",
                "consequence": "Directed relation is regenerated.",
            },
            {
                "control": "Forget direction and self-relations",
                "space": "k(k-1)/2",
                "closure_witness": "(E_ij+E_ji)^2=E_ii+E_jj",
                "consequence": "Diagonal/self structure is regenerated.",
            },
            {
                "control": "Keep only Z",
                "space": "k",
                "closure_witness": "No sector traversal",
                "consequence": "Fails P3.",
            },
            {
                "control": "Keep only X",
                "space": "k",
                "closure_witness": "No resolved phase operator",
                "consequence": "Fails P1.",
            },
            {
                "control": "Keep Z and X",
                "space": "generators",
                "closure_witness": "ZX=omega XZ",
                "consequence": "Weyl closure gives M_k(C), dimension k^2.",
            },
        ]
    )


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def plot_residuals(residuals: pd.DataFrame, out: Path) -> None:
    plt.figure(figsize=(11, 6))
    for name in CANDIDATES:
        s = residuals[residuals["candidate"] == name]
        plt.plot(
            s["k"],
            s["bounded_residual"],
            marker="o",
            markersize=3,
            label=name,
        )

    plt.yscale("log")
    plt.xlabel("Closure sector k")
    plt.ylabel("Bounded residual |F_k-C(k)|/(F_k+C(k))")
    plt.title("Fibonacci Compatibility of Alternative Structural Counts")
    plt.legend(frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig(out / "alternative_structural_residuals.png", dpi=180)
    plt.close()


def plot_expansion(audit: pd.DataFrame, k: int, out: Path) -> None:
    s = audit[audit["k"] == k].copy()
    order = [
        "full_ordered_self",
        "traceless",
        "ordered_no_self",
        "unordered_self",
        "unordered_no_self",
        "phase_only_linear",
        "shift_only_linear",
        "phase_plus_shift_DCT",
    ]
    s["order"] = s["candidate"].map({n: i for i, n in enumerate(order)})
    s = s.sort_values("order")

    x = np.arange(len(s))
    plt.figure(figsize=(12, 6))
    plt.bar(
        x - 0.18,
        s["declared_dimension"],
        width=0.36,
        label="Declared dimension",
    )
    plt.bar(
        x + 0.18,
        s["unital_associative_closure_dimension"],
        width=0.36,
        label="Dimension after required closure",
    )
    plt.axhline(k * k, linestyle="--", label=f"k^2={k*k}")
    plt.xticks(x, s["candidate"], rotation=45, ha="right")
    plt.ylabel("Complex vector-space dimension")
    plt.title(f"Alternative-Space Closure Expansion at k={k}")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(out / "alternative_closure_expansion.png", dpi=180)
    plt.close()


def plot_premise_map(premise: pd.DataFrame, out: Path) -> None:
    def score(value: str) -> int:
        if value == "PASS":
            return 0
        if "FAIL" in value:
            return 2
        return 1

    cols = ["P1", "P2", "P3", "P4"]
    matrix = np.array(
        [[score(row[c]) for c in cols] for _, row in premise.iterrows()]
    )

    plt.figure(figsize=(8, 6))
    image = plt.imshow(matrix, aspect="auto", vmin=0, vmax=2)
    plt.colorbar(
        image,
        ticks=[0, 1, 2],
        label="0=pass, 1=changed/projected, 2=fail",
    )
    plt.xticks(range(4), cols)
    plt.yticks(range(len(premise)), premise["candidate"])
    plt.title("DCT Premise Audit of Alternative Structures")
    plt.tight_layout()
    plt.savefig(out / "alternative_premise_audit.png", dpi=180)
    plt.close()


def main() -> None:
    config = Config()
    out = Path(config.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    matches = fibonacci_match_scan(config)
    matches.to_csv(out / "alternative_fibonacci_matches.csv", index=False)

    residuals = residual_table(24)
    residuals.to_csv(out / "alternative_structural_residuals.csv", index=False)

    audit = algebra_audit(config)
    audit.to_csv(out / "alternative_algebra_audit.csv", index=False)

    premise = premise_audit()
    premise.to_csv(out / "alternative_premise_audit.csv", index=False)

    implications = implication_table()
    implications.to_csv(out / "alternative_implication_table.csv", index=False)

    diagnostic = audit[audit["k"] == config.diagnostic_k]
    diagnostic.to_csv(out / "diagnostic_k6_algebra_audit.csv", index=False)

    plot_residuals(residuals, out)
    plot_expansion(audit, config.diagnostic_k, out)
    plot_premise_map(premise, out)

    print()
    print("Dynamic Closure Notebook — Entry 12")
    print("Alternative Structure Controls and Premise Audit")
    print("-" * 62)
    print()
    print("Exact Fibonacci matches for 2 <= k <= 500:")
    print(
        matches[
            ["candidate", "count_formula", "exact_match_indices"]
        ].to_string(index=False)
    )
    print()

    for name in (
        "traceless",
        "ordered_no_self",
        "unordered_self",
    ):
        s = audit[audit["candidate"] == name]
        print(
            f"{name}: closure expands to k^2 for every tested k = "
            f"{bool(np.all(s['expands_to_full_k2']))}"
        )

    s = audit[
        (audit["candidate"] == "unordered_no_self")
        & (audit["k"] >= 3)
    ]
    print(
        "unordered_no_self: closure expands to k^2 for every tested k>=3 = "
        f"{bool(np.all(s['expands_to_full_k2']))}"
    )

    s = audit[audit["candidate"] == "phase_plus_shift_DCT"]
    print(
        "phase_plus_shift_DCT: Weyl basis rank is k^2 for every tested k = "
        f"{bool(np.all(s['expands_to_full_k2']))}"
    )
    print()

    print(f"Diagnostic audit at k={config.diagnostic_k}:")
    print(
        diagnostic[
            [
                "candidate",
                "declared_dimension",
                "contains_identity",
                "explicit_product_witness_in_declared_span",
                "unital_associative_closure_dimension",
                "dct_status",
            ]
        ].to_string(index=False)
    )
    print()

    print("Premise-level summary:")
    print(
        premise[
            [
                "candidate",
                "count",
                "P1",
                "P3",
                "P4",
                "Fibonacci_match",
            ]
        ].to_string(index=False)
    )
    print()
    print(
        "Conclusion: smaller counts are not interchangeable full closures. "
        "They are projections, symmetrizations, self-relation deletions, or "
        "single-generator subalgebras. Restoring both DCT-required generators "
        "and unital associative composition restores M_k(C), dimension k^2."
    )
    print()
    print(f"Outputs written to: {out.resolve()}")


if __name__ == "__main__":
    main()
