# Dynamic Closure Notebook — Entry 05
# Weyl-Generated Closure Algebra
#
# Purpose:
# Derive the k^2 closure capacity from cyclic phase-and-shift dynamics.
#
# Assumptions:
# 1. k cyclic sectors labelled by Z_k.
# 2. A cyclic shift operator X.
# 3. A cyclic phase operator Z.
# 4. Unital associative closure under operator composition.
#
# Definitions:
# omega = exp(2*pi*i/k)
# X|m> = |m+1 mod k>
# Z|m> = omega^m |m>
# Z X = omega X Z
#
# Weyl monomials:
# W_(a,b) = X^a Z^b,  a,b in Z_k
#
# Multiplication:
# W_(a,b) W_(c,d) = omega^(b*c) W_(a+c,b+d)
#
# Therefore there are k^2 independent operator modes.

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


@dataclass
class Config:
    k_min: int = 2
    k_max: int = 24
    arithmetic_search_max: int = 500
    output_dir: str = "dynamic_closure_entry_05_output"


def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative.")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def detect_fibonacci_square_closure(k_max: int) -> list[int]:
    return [
        k for k in range(2, k_max + 1)
        if fibonacci(k) == k * k
    ]


def clock_and_shift(k: int):
    omega = np.exp(2j * np.pi / k)

    z = np.diag(
        np.array([omega**m for m in range(k)], dtype=complex)
    )

    x = np.zeros((k, k), dtype=complex)
    for m in range(k):
        x[(m + 1) % k, m] = 1.0

    return omega, x, z


def weyl_operator(x, z, a: int, b: int, k: int):
    return (
        np.linalg.matrix_power(x, a % k)
        @ np.linalg.matrix_power(z, b % k)
    )


def build_weyl_basis(k: int):
    _, x, z = clock_and_shift(k)
    return [
        (a, b, weyl_operator(x, z, a, b, k))
        for a in range(k)
        for b in range(k)
    ]


def analyze_dimension(k: int) -> dict:
    omega, x, z = clock_and_shift(k)
    relation_error = np.linalg.norm(
        z @ x - omega * x @ z,
        ord="fro",
    )

    basis = build_weyl_basis(k)
    flattened = np.column_stack(
        [operator.reshape(-1) for _, _, operator in basis]
    )
    rank = int(np.linalg.matrix_rank(flattened))

    # Hilbert-Schmidt orthogonality.
    max_orthogonality_error = 0.0
    for i, (_, _, wi) in enumerate(basis):
        for j, (_, _, wj) in enumerate(basis):
            value = np.trace(wi.conj().T @ wj) / k
            expected = 1.0 if i == j else 0.0
            max_orthogonality_error = max(
                max_orthogonality_error,
                float(abs(value - expected)),
            )

    max_nonidentity_trace = 0.0
    for a, b, operator in basis:
        if a == 0 and b == 0:
            continue
        max_nonidentity_trace = max(
            max_nonidentity_trace,
            float(abs(np.trace(operator))),
        )

    return {
        "k": k,
        "k_squared": k * k,
        "weyl_basis_count": len(basis),
        "numerical_span_rank": rank,
        "weyl_relation_error": float(relation_error),
        "maximum_orthogonality_error": max_orthogonality_error,
        "maximum_nonidentity_trace": max_nonidentity_trace,
    }


def verify_multiplication_law(k: int) -> float:
    omega, x, z = clock_and_shift(k)
    max_error = 0.0

    for a in range(k):
        for b in range(k):
            wab = weyl_operator(x, z, a, b, k)

            for c in range(k):
                for d in range(k):
                    wcd = weyl_operator(x, z, c, d, k)

                    lhs = wab @ wcd
                    rhs = (
                        omega ** (b * c)
                        * weyl_operator(
                            x,
                            z,
                            a + c,
                            b + d,
                            k,
                        )
                    )

                    max_error = max(
                        max_error,
                        float(np.linalg.norm(lhs - rhs, ord="fro")),
                    )

    return max_error


def verify_adjoint_law(k: int) -> float:
    omega, x, z = clock_and_shift(k)
    max_error = 0.0

    for a in range(k):
        for b in range(k):
            wab = weyl_operator(x, z, a, b, k)

            lhs = wab.conj().T
            rhs = (
                omega ** (a * b)
                * weyl_operator(x, z, -a, -b, k)
            )

            max_error = max(
                max_error,
                float(np.linalg.norm(lhs - rhs, ord="fro")),
            )

    return max_error


def verify_traceless_nonclosure(k: int) -> dict:
    omega, x, z = clock_and_shift(k)
    identity = np.eye(k, dtype=complex)

    tested = 0
    regenerated = 0
    max_error = 0.0

    for a in range(k):
        for b in range(k):
            if a == 0 and b == 0:
                continue

            left = weyl_operator(x, z, a, b, k)
            right = weyl_operator(x, z, -a, -b, k)
            product = left @ right

            expected = omega ** (-a * b) * identity
            error = float(np.linalg.norm(product - expected, ord="fro"))

            tested += 1
            max_error = max(max_error, error)
            if error < 1.0e-10:
                regenerated += 1

    return {
        "k": k,
        "nonidentity_elements_tested": tested,
        "products_regenerating_identity": regenerated,
        "identity_regeneration_fraction": regenerated / tested,
        "maximum_identity_regeneration_error": max_error,
    }


def verify_off_diagonal_nonclosure(k: int) -> dict:
    tested = 0
    regenerated = 0
    max_error = 0.0

    for i in range(k):
        for j in range(k):
            if i == j:
                continue

            e_ij = np.zeros((k, k), dtype=complex)
            e_ji = np.zeros((k, k), dtype=complex)
            e_ii = np.zeros((k, k), dtype=complex)

            e_ij[i, j] = 1.0
            e_ji[j, i] = 1.0
            e_ii[i, i] = 1.0

            error = float(
                np.linalg.norm(e_ij @ e_ji - e_ii, ord="fro")
            )

            tested += 1
            max_error = max(max_error, error)
            if error < 1.0e-12:
                regenerated += 1

    return {
        "k": k,
        "off_diagonal_inverse_pairs_tested": tested,
        "products_generating_self_relation": regenerated,
        "self_relation_regeneration_fraction": regenerated / tested,
        "maximum_matrix_unit_error": max_error,
    }


def make_weyl_lattice_table(k: int) -> pd.DataFrame:
    rows = []

    for a in range(k):
        for b in range(k):
            if a == 0 and b == 0:
                category = "identity"
                category_code = 0
            elif a != 0 and b == 0:
                category = "pure_shift"
                category_code = 1
            elif a == 0 and b != 0:
                category = "pure_phase"
                category_code = 2
            else:
                category = "mixed_phase_shift"
                category_code = 3

            rows.append({
                "shift_index_a": a,
                "phase_index_b": b,
                "category": category,
                "category_code": category_code,
            })

    return pd.DataFrame(rows)


def plot_dimension_scaling(diagnostics: pd.DataFrame, output_dir: Path):
    plt.figure(figsize=(9, 5))
    plt.plot(
        diagnostics["k"],
        diagnostics["weyl_basis_count"],
        marker="o",
        label="Weyl basis count",
    )
    plt.plot(
        diagnostics["k"],
        diagnostics["numerical_span_rank"],
        marker="x",
        label="Numerical span rank",
    )
    plt.plot(
        diagnostics["k"],
        diagnostics["k_squared"],
        linestyle="--",
        label="k^2",
    )
    plt.xlabel("Closure sector count k")
    plt.ylabel("Operator-space dimension")
    plt.title("Weyl-Generated Operator Dimension")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(output_dir / "weyl_dimension_scaling.png", dpi=180)
    plt.close()


def plot_errors(diagnostics: pd.DataFrame, output_dir: Path):
    plt.figure(figsize=(9, 5))
    plt.semilogy(
        diagnostics["k"],
        diagnostics["weyl_relation_error"] + 1.0e-18,
        marker="o",
        label="Weyl relation error",
    )
    plt.semilogy(
        diagnostics["k"],
        diagnostics["maximum_orthogonality_error"] + 1.0e-18,
        marker="o",
        label="Orthogonality error",
    )
    plt.xlabel("Closure sector count k")
    plt.ylabel("Numerical error")
    plt.title("Numerical Verification of the Finite Weyl Algebra")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(output_dir / "weyl_numerical_errors.png", dpi=180)
    plt.close()


def plot_lattice(lattice: pd.DataFrame, k: int, output_dir: Path):
    matrix = np.empty((k, k), dtype=float)

    for _, row in lattice.iterrows():
        matrix[
            int(row["phase_index_b"]),
            int(row["shift_index_a"]),
        ] = int(row["category_code"])

    plt.figure(figsize=(7, 6))
    image = plt.imshow(matrix, origin="lower", aspect="equal")

    colorbar = plt.colorbar(image, ticks=[0, 1, 2, 3])
    colorbar.ax.set_yticklabels(
        ["Identity", "Pure shift", "Pure phase", "Mixed"]
    )

    plt.xlabel("Shift index a")
    plt.ylabel("Phase index b")
    plt.title(
        f"Weyl Closure Lattice for Detected Fibonacci-Square Sector k={k}"
    )
    plt.tight_layout()
    plt.savefig(
        output_dir / "detected_closure_weyl_lattice.png",
        dpi=180,
    )
    plt.close()


def main():
    config = Config()
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    diagnostics = pd.DataFrame([
        analyze_dimension(k)
        for k in range(config.k_min, config.k_max + 1)
    ])
    diagnostics.to_csv(
        output_dir / "weyl_dimension_diagnostics.csv",
        index=False,
    )

    traceless = pd.DataFrame([
        verify_traceless_nonclosure(k)
        for k in range(config.k_min, config.k_max + 1)
    ])
    traceless.to_csv(
        output_dir / "traceless_nonclosure_diagnostics.csv",
        index=False,
    )

    off_diagonal = pd.DataFrame([
        verify_off_diagonal_nonclosure(k)
        for k in range(config.k_min, config.k_max + 1)
    ])
    off_diagonal.to_csv(
        output_dir / "matrix_unit_nonclosure_diagnostics.csv",
        index=False,
    )

    arithmetic_solutions = detect_fibonacci_square_closure(
        config.arithmetic_search_max
    )

    arithmetic = pd.DataFrame({
        "k": arithmetic_solutions,
        "F_k": [fibonacci(k) for k in arithmetic_solutions],
        "k_squared": [k * k for k in arithmetic_solutions],
    })
    arithmetic.to_csv(
        output_dir / "fibonacci_square_closure_scan.csv",
        index=False,
    )

    multiplication = pd.DataFrame([
        {
            "k": k,
            "maximum_multiplication_law_error":
                verify_multiplication_law(k),
        }
        for k in range(2, 13)
    ])
    multiplication.to_csv(
        output_dir / "multiplication_closure_diagnostics.csv",
        index=False,
    )

    adjoint = pd.DataFrame([
        {
            "k": k,
            "maximum_adjoint_law_error":
                verify_adjoint_law(k),
        }
        for k in range(2, 13)
    ])
    adjoint.to_csv(
        output_dir / "adjoint_closure_diagnostics.csv",
        index=False,
    )

    plot_dimension_scaling(diagnostics, output_dir)
    plot_errors(diagnostics, output_dir)

    detected_k = arithmetic_solutions[0] if arithmetic_solutions else None

    if detected_k is not None:
        lattice = make_weyl_lattice_table(detected_k)
        lattice.to_csv(
            output_dir / "detected_closure_weyl_lattice.csv",
            index=False,
        )
        plot_lattice(lattice, detected_k, output_dir)

    dimension_verified = bool(
        np.all(diagnostics["weyl_basis_count"] == diagnostics["k_squared"])
        and np.all(diagnostics["numerical_span_rank"] == diagnostics["k_squared"])
    )

    traceless_nonclosure_verified = bool(
        np.allclose(traceless["identity_regeneration_fraction"], 1.0)
    )

    off_diagonal_nonclosure_verified = bool(
        np.allclose(
            off_diagonal["self_relation_regeneration_fraction"],
            1.0,
        )
    )

    print()
    print("Dynamic Closure Notebook — Entry 05")
    print("Weyl-Generated Closure Algebra")
    print("-" * 50)
    print()
    print(
        f"Weyl basis dimension k^2 verified for "
        f"k={config.k_min},...,{config.k_max}: "
        f"{dimension_verified}"
    )
    print()
    print(
        "Traceless k^2-1 sector fails multiplicative closure "
        f"for every inverse pair: {traceless_nonclosure_verified}"
    )
    print()
    print(
        "Off-diagonal matrix-unit sector regenerates self-relations "
        f"E_ii for every inverse pair: {off_diagonal_nonclosure_verified}"
    )
    print()
    print(
        f"Computational solutions of F_k = k^2 for "
        f"2 <= k <= {config.arithmetic_search_max}: "
        f"{arithmetic_solutions}"
    )
    print()

    if detected_k is not None:
        row = diagnostics[diagnostics["k"] == detected_k].iloc[0]

        print("Detected closure sector:")
        print(f"    k = {detected_k}")
        print(f"    F_k = {fibonacci(detected_k)}")
        print(f"    k^2 = {detected_k ** 2}")
        print(
            f"    Weyl basis count = "
            f"{int(row['weyl_basis_count'])}"
        )
        print(
            f"    Numerical span rank = "
            f"{int(row['numerical_span_rank'])}"
        )
        print()

    print("Conditional algebraic conclusion:")
    print(
        "    Cyclic phase + cyclic shift + unital associative "
        "composition closure => M_k(C), dimension k^2."
    )
    print()
    print("Combined with Entry 04:")
    print(
        "    F_k = k^2 => unique nontrivial closure k = 12 "
        "using the published Fibonacci perfect-power theorem."
    )
    print()
    print(f"Outputs written to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
