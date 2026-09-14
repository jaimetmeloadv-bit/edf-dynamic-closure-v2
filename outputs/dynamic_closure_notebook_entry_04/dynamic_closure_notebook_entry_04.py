"""
Dynamic Closure Notebook — Entry 04
Pair-Space Derivation, Combinatorial Controls, and Arithmetic Uniqueness

Purpose
-------
This notebook investigates the structural meaning of k^2.

The central question is not:
    "Can we choose a formula that gives k = 12?"

It is:
    "Which standard relational/operator-space count gives an exact
     Fibonacci closure, and what mathematical assumptions distinguish it?"

No target sector is hard-coded.

Mathematical structures tested
------------------------------
For a set S_k of k closure sectors:

1. Full ordered pair space, including self-relations:
       |S_k x S_k| = k^2

2. Ordered pairs excluding self-relations:
       k(k - 1)

3. Unordered pairs including self-relations:
       k(k + 1)/2

4. Unordered pairs excluding self-relations:
       k(k - 1)/2

5. Full traceless operator count:
       k^2 - 1

6. Linear count:
       k

The full ordered pair count is also the dimension of the full operator space
End(C^k), with matrix-unit basis E_ij = |i><j|, i,j = 1,...,k.

For Hermitian operators, the same real dimension k^2 can be counted as:
    k diagonal real components
    + 2 * C(k,2) real off-diagonal components
    = k + k(k-1)
    = k^2.

Trace normalization removes one identity direction and gives k^2 - 1
independent normalized-state coordinates. Therefore k^2 and k^2 - 1 must be
distinguished rather than conflated.

Candidate Fibonacci compatibility
---------------------------------
For each structural count C(k), define

    B_C(k) = |F_k - C(k)| / (F_k + C(k)).

Exact structural closure occurs when

    F_k = C(k).

Arithmetic uniqueness result for the k^2 hypothesis
----------------------------------------------------
A theorem of Bugeaud, Mignotte, and Siksek (Annals of Mathematics 163,
969-1018, 2006) proves that the only perfect powers in the Fibonacci sequence
are:

    F_0 = 0,
    F_1 = F_2 = 1,
    F_6 = 8,
    F_12 = 144.

If k >= 2 and F_k = k^2, then F_k is a perfect square and hence a perfect
power. Checking the theorem's finite list leaves only:

    F_12 = 144 = 12^2.

Thus, conditional on the full ordered-pair closure hypothesis C(k)=k^2,
k=12 is the unique nontrivial solution for k >= 2.

References
----------
Y. Bugeaud, M. Mignotte, and S. Siksek,
"Classical and modular approaches to exponential Diophantine equations I.
Fibonacci and Lucas perfect powers,"
Annals of Mathematics 163 (2006), 969-1018.
DOI: 10.4007/annals.2006.163.969

C. P. Moca et al.,
"Simulating Lindbladian evolution with non-Abelian symmetries:
Ballistic front propagation in the SU(2) Hubbard model with a localized loss,"
Physical Review B 105, 195144 (2022).
DOI: 10.1103/PhysRevB.105.195144

The literature references support the standard mathematical structures.
They do not by themselves establish the EDF-specific physical identification.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


@dataclass
class Config:
    k_min: int = 2
    k_max_table: int = 30
    k_max_verification: int = 500

    plot_k_min: int = 4
    plot_k_max: int = 24

    output_dir: str = "dynamic_closure_entry_04_output"


def fibonacci(n: int) -> int:
    """Return F_n with F_0 = 0 and F_1 = 1."""
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative.")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def normalized_residual(fibonacci_value: int, structural_count: int) -> float:
    """Return |F-C|/(F+C) for non-negative integer counts."""
    denominator = fibonacci_value + structural_count
    if denominator == 0:
        return 0.0
    return abs(fibonacci_value - structural_count) / denominator


def full_ordered_with_self(k: int) -> int:
    return k * k


def full_traceless(k: int) -> int:
    return k * k - 1


def ordered_without_self(k: int) -> int:
    return k * (k - 1)


def unordered_with_self(k: int) -> int:
    return k * (k + 1) // 2


def unordered_without_self(k: int) -> int:
    return k * (k - 1) // 2


def linear_count(k: int) -> int:
    return k


COUNT_MODELS: dict[str, Callable[[int], int]] = {
    "full_ordered_with_self_k2": full_ordered_with_self,
    "full_traceless_k2_minus_1": full_traceless,
    "ordered_without_self": ordered_without_self,
    "unordered_with_self": unordered_with_self,
    "unordered_without_self": unordered_without_self,
    "linear_count": linear_count,
}


def verify_hermitian_real_dimension(k: int) -> tuple[int, int, int]:
    """
    Count the real dimension of Hermitian k x k matrices.

    diagonal:
        k real entries

    off-diagonal:
        C(k,2) complex entries
        = 2*C(k,2) real components

    total:
        k + 2*C(k,2) = k^2
    """
    diagonal = k
    off_diagonal_real = k * (k - 1)
    total = diagonal + off_diagonal_real
    return diagonal, off_diagonal_real, total


def build_model_table(config: Config) -> pd.DataFrame:
    rows = []

    for k in range(config.k_min, config.k_max_table + 1):
        fib = fibonacci(k)

        diagonal, off_diagonal_real, hermitian_total = (
            verify_hermitian_real_dimension(k)
        )

        row = {
            "k": k,
            "F_k": fib,
            "hermitian_diagonal_real_components": diagonal,
            "hermitian_off_diagonal_real_components": off_diagonal_real,
            "hermitian_total_real_dimension": hermitian_total,
        }

        for model_name, count_function in COUNT_MODELS.items():
            count = count_function(k)
            row[f"{model_name}_count"] = count
            row[f"{model_name}_residual"] = normalized_residual(
                fib,
                count,
            )
            row[f"{model_name}_exact"] = fib == count

        rows.append(row)

    return pd.DataFrame(rows)


def find_exact_solutions(
    config: Config,
) -> pd.DataFrame:
    rows = []

    for model_name, count_function in COUNT_MODELS.items():
        for k in range(config.k_min, config.k_max_verification + 1):
            fib = fibonacci(k)
            count = count_function(k)

            if fib == count:
                rows.append(
                    {
                        "model": model_name,
                        "k": k,
                        "F_k": fib,
                        "structural_count": count,
                    }
                )

    if not rows:
        return pd.DataFrame(
            columns=[
                "model",
                "k",
                "F_k",
                "structural_count",
            ]
        )

    return pd.DataFrame(rows)


def find_minimum_residuals(
    table: pd.DataFrame,
) -> pd.DataFrame:
    rows = []

    for model_name in COUNT_MODELS:
        residual_column = f"{model_name}_residual"
        best_index = table[residual_column].idxmin()
        best_row = table.loc[best_index]

        rows.append(
            {
                "model": model_name,
                "best_k_in_table_range": int(best_row["k"]),
                "minimum_residual": float(best_row[residual_column]),
                "exact_in_table_range": bool(
                    best_row[f"{model_name}_exact"]
                ),
            }
        )

    return pd.DataFrame(rows)


def perfect_power_theorem_certificate() -> pd.DataFrame:
    """
    Encode the finite Fibonacci perfect-power list from the 2006 theorem
    and test the equation F_k = k^2 on that list.

    This function is not a computational proof of the theorem. It is a
    transparent check of the theorem's published finite classification.
    """
    theorem_indices = [0, 1, 2, 6, 12]

    rows = []

    for k in theorem_indices:
        fib = fibonacci(k)
        square = k * k

        rows.append(
            {
                "k": k,
                "F_k": fib,
                "k_squared": square,
                "F_k_equals_k_squared": fib == square,
            }
        )

    return pd.DataFrame(rows)


def make_residual_plot(
    table: pd.DataFrame,
    config: Config,
    output_dir: Path,
) -> None:
    subset = table[
        (table["k"] >= config.plot_k_min)
        & (table["k"] <= config.plot_k_max)
    ]

    plotted_models = [
        "full_ordered_with_self_k2",
        "full_traceless_k2_minus_1",
        "ordered_without_self",
        "unordered_with_self",
        "unordered_without_self",
    ]

    labels = {
        "full_ordered_with_self_k2": "Ordered + self: k^2",
        "full_traceless_k2_minus_1": "Traceless: k^2 - 1",
        "ordered_without_self": "Ordered, no self: k(k-1)",
        "unordered_with_self": "Unordered + self: k(k+1)/2",
        "unordered_without_self": "Unordered, no self: k(k-1)/2",
    }

    plt.figure(figsize=(10, 6))

    for model_name in plotted_models:
        plt.plot(
            subset["k"],
            subset[f"{model_name}_residual"],
            marker="o",
            label=labels[model_name],
        )

    plt.xlabel("Closure sector k")
    plt.ylabel("Normalized structural residual")
    plt.title("Fibonacci Residual Across Pair-Space Hypotheses")
    plt.legend(fontsize=8, frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / "pair_space_residual_comparison.png",
        dpi=180,
    )
    plt.close()


def make_k2_vs_traceless_plot(
    table: pd.DataFrame,
    config: Config,
    output_dir: Path,
) -> None:
    subset = table[
        (table["k"] >= config.plot_k_min)
        & (table["k"] <= config.plot_k_max)
    ]

    plt.figure(figsize=(9, 5))
    plt.plot(
        subset["k"],
        subset["full_ordered_with_self_k2_residual"],
        marker="o",
        label="Full operator space: k^2",
    )
    plt.plot(
        subset["k"],
        subset["full_traceless_k2_minus_1_residual"],
        marker="o",
        label="Traceless state coordinates: k^2 - 1",
    )
    plt.xlabel("Closure sector k")
    plt.ylabel("Normalized structural residual")
    plt.title("Full Operator Space vs Traceless Subspace")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / "k2_vs_k2_minus_1.png",
        dpi=180,
    )
    plt.close()


def make_exact_solution_plot(
    exact_solutions: pd.DataFrame,
    output_dir: Path,
) -> None:
    if exact_solutions.empty:
        return

    counts = (
        exact_solutions.groupby("model")
        .size()
        .reindex(COUNT_MODELS.keys(), fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.bar(
        np.arange(len(counts)),
        counts.to_numpy(),
    )
    plt.xticks(
        np.arange(len(counts)),
        [
            "k^2",
            "k^2-1",
            "k(k-1)",
            "k(k+1)/2",
            "k(k-1)/2",
            "k",
        ],
        rotation=25,
        ha="right",
    )
    plt.ylabel("Number of exact solutions")
    plt.title(
        "Exact Fibonacci-Closure Solutions "
        "for 2 <= k <= 500"
    )
    plt.tight_layout()
    plt.savefig(
        output_dir / "exact_solution_counts.png",
        dpi=180,
    )
    plt.close()


def main() -> None:
    config = Config()
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    table = build_model_table(config)
    table.to_csv(
        output_dir / "pair_space_model_table.csv",
        index=False,
    )

    exact_solutions = find_exact_solutions(config)
    exact_solutions.to_csv(
        output_dir / "exact_solutions_to_k500.csv",
        index=False,
    )

    minima = find_minimum_residuals(table)
    minima.to_csv(
        output_dir / "minimum_residuals.csv",
        index=False,
    )

    theorem_certificate = perfect_power_theorem_certificate()
    theorem_certificate.to_csv(
        output_dir / "perfect_power_theorem_certificate.csv",
        index=False,
    )

    make_residual_plot(
        table=table,
        config=config,
        output_dir=output_dir,
    )

    make_k2_vs_traceless_plot(
        table=table,
        config=config,
        output_dir=output_dir,
    )

    make_exact_solution_plot(
        exact_solutions=exact_solutions,
        output_dir=output_dir,
    )

    # Internal consistency check for Hermitian dimension.
    hermitian_dimension_ok = bool(
        np.all(
            table["hermitian_total_real_dimension"]
            == table["k"] ** 2
        )
    )

    print()
    print("Dynamic Closure Notebook — Entry 04")
    print("Pair-Space Derivation and Arithmetic Uniqueness")
    print("-" * 60)
    print()
    print(
        "Hermitian dimension identity verified over table range: "
        f"{hermitian_dimension_ok}"
    )
    print()
    print("Exact computational solutions for 2 <= k <= 500:")
    if exact_solutions.empty:
        print("    None")
    else:
        print(exact_solutions.to_string(index=False))
    print()
    print("Minimum normalized residuals for 2 <= k <= 30:")
    print(minima.to_string(index=False))
    print()
    print("Published perfect-power theorem certificate:")
    print(theorem_certificate.to_string(index=False))
    print()
    print(
        "Conditional uniqueness statement:"
    )
    print(
        "    If complete EDF closure requires the full ordered operator "
        "pair space C(k)=k^2 and Fibonacci compatibility F_k=C(k), "
        "then k=12 is the unique nontrivial solution for k>=2."
    )
    print()
    print(
        "Important distinction:"
    )
    print(
        "    k^2 counts the full operator space including the identity "
        "direction; k^2-1 counts normalized traceless state coordinates."
    )
    print()
    print(f"Outputs written to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
